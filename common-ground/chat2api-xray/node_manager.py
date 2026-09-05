#!/usr/bin/env python3
"""
xray 节点管理器 v2：多来源 + 自动容灾 + 订阅自动刷新
====================================================
节点来源分层：
  1. specified_nodes（优先）：node-config.json 里手动指定的快节点
     （柳柳挑好的 IP，哥哥维护）
  2. subscription（兜底）：环境变量 SUBSCRIPTION_URL 指向订阅链接
     （edgetunnel vless 订阅；内容隔几小时刷新，管理器定时重拉自动跟上）

行为：
  - 启动：先试 specified，全不通则拉订阅、试订阅节点，直到找到可用节点
  - 主循环：每 interval 秒探活；连续 fail_threshold 次失败 → 自动切下一个
  - 订阅刷新：每 subscription_refresh_sec 秒重新拉一次订阅（默认 3600）

配合 chat2api：xray 本地代理端口由 LOCAL_HTTP_PORT 指定，chat2api 的
PROXY_URL / EXPORT_PROXY_URL 由 entrypoint.sh 设为同一端口。
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.parse

XRAY_CONFIG_PATH = "/tmp/xray_config.json"
XRAY_BIN = "/usr/local/bin/xray"
LOCAL_HTTP_PORT = int(os.environ.get("LOCAL_HTTP_PORT", "10809"))
DEFAULT_PROBE_URL = "https://www.gstatic.com/generate_204"
DEFAULT_SNI = "magicovo.pages.dev"
DEFAULT_HOST = "magicovo.pages.dev"


# ---------------------------------------------------------------
# 节点加载 / 订阅解析
# ---------------------------------------------------------------
def load_config():
    with open("/tmp/nodes.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # 新格式用 specified_nodes；兼容旧格式 nodes
    specified = cfg.get("specified_nodes") or cfg.get("nodes") or []
    return specified, cfg.get("check", {})


def parse_vless(uri):
    """解析单条 vless:// 链接为节点 dict；非 vless 返回 None。"""
    uri = uri.strip()
    if not uri.startswith("vless://"):
        return None
    try:
        userinfo, _, _frag = uri[len("vless://"):].partition("#")
        query = ""
        if "?" in userinfo:
            userinfo, _, query = userinfo.partition("?")
        uuid, _, hostport = userinfo.rpartition("@")
        if not uuid or not hostport:
            return None
        host, _, port_s = hostport.rpartition(":")
        if not host:
            return None
        try:
            port = int(port_s) if port_s else 443
        except ValueError:
            port = 443
        params = urllib.parse.parse_qs(query)
        node = {
            "addr": host,
            "port": port,
            "uuid": uuid,
            "sni": (params.get("sni") or [None])[0] or DEFAULT_SNI,
            "host": (params.get("host") or [None])[0] or DEFAULT_HOST,
            "path": (params.get("path") or ["/"])[0] or "/",
        }
        return node
    except Exception:
        return None


def fetch_subscription(url):
    """拉取订阅链接 → 解析出全部 vless 节点（支持裸文本或 base64）。"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Android 14)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[node-mgr] subscription fetch failed: {e}", flush=True)
        return []
    text = raw.strip()
    # 尝试 base64（去掉空白后解码，若内容含 vless:// 则用解码结果）
    try:
        stripped = "".join(text.split())
        padded = stripped + "=" * (-len(stripped) % 4)
        decoded = base64.b64decode(padded).decode("utf-8", errors="ignore")
        if "vless://" in decoded:
            text = decoded
    except Exception:
        pass
    nodes = []
    for line in text.splitlines():
        node = parse_vless(line)
        if node:
            nodes.append(node)
    return nodes


# ---------------------------------------------------------------
# xray 生命周期
# ---------------------------------------------------------------
def build_xray_config(node):
    host = node.get("host") or node.get("sni") or DEFAULT_HOST
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": "http",
                "port": LOCAL_HTTP_PORT,
                "listen": "127.0.0.1",
                "protocol": "http",
                "settings": {},
            }
        ],
        "outbounds": [
            {
                "tag": "node",
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": node["addr"],
                            "port": int(node.get("port", 443)),
                            "users": [{"id": node["uuid"], "encryption": "none"}],
                        }
                    ]
                },
                "streamSettings": {
                    "network": "ws",
                    "security": "tls",
                    "tlsSettings": {
                        "serverName": node.get("sni", DEFAULT_SNI),
                        "allowInsecure": False,
                        "fingerprint": "chrome",
                    },
                    "wsSettings": {"path": node.get("path", "/"), "headers": {"Host": host}},
                },
            },
            {"tag": "direct", "protocol": "freedom"},
        ],
        "routing": {
            "rules": [{"type": "field", "outboundTag": "direct", "network": "tcp,udp", "port": 1}]
        },
    }


def write_xray_config(node):
    with open(XRAY_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(build_xray_config(node), f, indent=2)


def start_xray():
    proc = subprocess.Popen(
        [XRAY_BIN, "run", "-c", XRAY_CONFIG_PATH],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc


def stop_xray(proc):
    if proc is None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


# ---------------------------------------------------------------
# 探活
# ---------------------------------------------------------------
def probe(url, timeout):
    """通过本地 HTTP 代理探活；成功返回 True。"""
    proxy = f"http://127.0.0.1:{LOCAL_HTTP_PORT}"
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": proxy, "https": proxy})
    )
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Linux; Android 14)")]
    try:
        with opener.open(url, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False


# ---------------------------------------------------------------
# 节点池
# ---------------------------------------------------------------
class NodePool:
    """合并 specified + subscription，去重后按序轮换。"""

    def __init__(self, specified, subscription_url):
        self.specified = specified
        self.subscription_url = subscription_url
        self.subscription = []
        self.last_sub_refresh = 0

    def _dedupe(self, nodes):
        seen = set()
        out = []
        for n in nodes:
            key = f"{n.get('addr')}|{n.get('uuid')}"
            if key not in seen:
                seen.add(key)
                out.append(n)
        return out

    def nodes(self):
        return self._dedupe(self.specified + self.subscription)

    def refresh_subscription(self, force=False):
        if not self.subscription_url:
            return
        if not force and time.time() - self.last_sub_refresh < refresh_interval:
            return
        fetched = fetch_subscription(self.subscription_url)
        if fetched:
            self.subscription = fetched
            self.last_sub_refresh = time.time()
            print(f"[node-mgr] subscription refreshed: {len(fetched)} nodes", flush=True)
        else:
            print("[node-mgr] subscription refresh returned empty; keep old list", flush=True)


# ---------------------------------------------------------------
# 全局配置
# ---------------------------------------------------------------
refresh_interval = 3600  # 默认订阅刷新秒数，main 里会被 check 覆盖


def main():
    global refresh_interval
    specified, check_cfg = load_config()
    subscription_url = os.environ.get("SUBSCRIPTION_URL", "").strip()
    interval = int(check_cfg.get("interval_sec", 30))
    timeout = int(check_cfg.get("timeout_sec", 6))
    threshold = int(check_cfg.get("fail_threshold", 3))
    probe_url = check_cfg.get("probe_url", DEFAULT_PROBE_URL)
    refresh_interval = int(check_cfg.get("subscription_refresh_sec", 3600))

    pool = NodePool(specified, subscription_url)
    if not pool.specified:
        print("[node-mgr] WARN: no specified_nodes, falling back to subscription only", flush=True)
    if not pool.specified and not subscription_url:
        sys.exit("ERROR: no specified_nodes and no SUBSCRIPTION_URL")
    print(f"[node-mgr] specified_nodes={len(pool.specified)}, subscription_url={'set' if subscription_url else 'none'}", flush=True)

    # 启动时先拉一次订阅（如有）
    pool.refresh_subscription(force=True)

    nodes = pool.nodes()
    if not nodes:
        sys.exit("ERROR: node pool empty after startup refresh")

    idx = 0
    xray_proc = None
    fail_count = 0
    probe_cursor = 0  # 启动探测用：防止无限循环刷同节点

    # ---- 启动探测：找到第一个可用节点 ----
    while True:
        nodes = pool.nodes()
        if not nodes:
            print("[node-mgr] node pool empty, retry subscription in 30s", flush=True)
            time.sleep(30)
            pool.refresh_subscription(force=True)
            continue
        node = nodes[idx % len(nodes)]
        write_xray_config(node)
        xray_proc = start_xray()
        time.sleep(2)
        if probe(probe_url, timeout):
            print(f"[node-mgr] ACTIVE node[{idx}] {node['addr']} ({'specified' if idx < len(pool.specified) else 'subscription'})", flush=True)
            break
        print(f"[node-mgr] node[{idx}] {node['addr']} dead on startup, try next", flush=True)
        stop_xray(xray_proc)
        xray_proc = None
        idx += 1
        probe_cursor += 1
        # 完整轮过一轮还没通 → 重新拉订阅（内容可能已刷新）
        if probe_cursor >= max(1, len(nodes)):
            pool.refresh_subscription(force=True)
            probe_cursor = 0

    # ---- 主循环：健康检查 + 自动切换 + 订阅定时刷新 ----
    while True:
        time.sleep(interval)

        # 定时刷新订阅（内容隔几小时会变）
        pool.refresh_subscription()
        new_nodes = pool.nodes()
        if len(new_nodes) != len(nodes):
            nodes = new_nodes
            idx = min(idx, max(0, len(nodes) - 1))
            print(f"[node-mgr] node pool size changed -> {len(nodes)}", flush=True)
        if not nodes:
            print("[node-mgr] node pool empty, waiting ...", flush=True)
            continue

        ok = probe(probe_url, timeout)
        if ok:
            if fail_count:
                fail_count = 0
            continue
        fail_count += 1
        print(f"[node-mgr] probe fail {fail_count}/{threshold} on {nodes[idx % len(nodes)]['addr']}", flush=True)
        if fail_count < threshold:
            continue

        # 切换下一个节点
        print("[node-mgr] switching to next node ...", flush=True)
        stop_xray(xray_proc)
        xray_proc = None
        fail_count = 0
        idx += 1
        node = nodes[idx % len(nodes)]
        write_xray_config(node)
        xray_proc = start_xray()
        time.sleep(2)
        source = "specified" if idx < len(pool.specified) else "subscription"
        print(f"[node-mgr] SWITCHED to node[{idx}] {node['addr']} ({source})", flush=True)


if __name__ == "__main__":
    main()