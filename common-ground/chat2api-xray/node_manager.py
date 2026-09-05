#!/usr/bin/env python3
"""
xray 节点管理器：健康检查 + 自动故障切换
==========================================
读取 /tmp/nodes.json（节点列表，由 entrypoint.sh 从 NODE_CONFIG_URL 拉取，
或从环境变量生成），常驻运行：
  1. 启动探测：依次尝试节点，第一个探活成功的留在当前
  2. 主循环：每 interval 秒用当前节点探活（走本地 HTTP 代理）
  3. 连续失败 fail_threshold 次 → 自动切换到下一个节点 → 重启 xray

配合 chat2api：xray 本地代理端口由 LOCAL_HTTP_PORT 指定，chat2api 的
PROXY_URL / EXPORT_PROXY_URL 由 entrypoint.sh 设为同一端口。
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

XRAY_CONFIG_PATH = "/tmp/xray_config.json"
XRAY_BIN = "/usr/local/bin/xray"
LOCAL_HTTP_PORT = int(os.environ.get("LOCAL_HTTP_PORT", "10809"))
DEFAULT_PROBE_URL = "https://www.gstatic.com/generate_204"


def load_nodes():
    with open("/tmp/nodes.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)
    nodes = cfg.get("nodes", [])
    if not nodes:
        sys.exit("ERROR: no nodes in /tmp/nodes.json")
    return nodes, cfg.get("check", {})


def build_xray_config(node):
    host = node.get("host") or node.get("sni") or "magicovo.pages.dev"
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
                        "serverName": node.get("sni", "magicovo.pages.dev"),
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


def probe(url, timeout):
    """通过本地 HTTP 代理探活；成功返回 True。"""
    proxy = f"http://127.0.0.1:{LOCAL_HTTP_PORT}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Linux; Android 14)")]
    try:
        with opener.open(url, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False


def main():
    nodes, check_cfg = load_nodes()
    interval = int(check_cfg.get("interval_sec", 30))
    timeout = int(check_cfg.get("timeout_sec", 6))
    threshold = int(check_cfg.get("fail_threshold", 3))
    probe_url = check_cfg.get("probe_url", DEFAULT_PROBE_URL)

    idx = 0
    xray_proc = None
    fail_count = 0

    # ---- 启动探测：找到第一个可用节点 ----
    while True:
        node = nodes[idx % len(nodes)]
        write_xray_config(node)
        xray_proc = start_xray()
        time.sleep(2)
        if probe(probe_url, timeout):
            print(f"[node-mgr] ACTIVE node[{idx}] {node['addr']}", flush=True)
            break
        print(f"[node-mgr] node[{idx}] {node['addr']} dead on startup, try next", flush=True)
        stop_xray(xray_proc)
        xray_proc = None
        idx += 1

    # ---- 主循环：健康检查 + 自动切换 ----
    while True:
        time.sleep(interval)
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
        print(f"[node-mgr] SWITCHED to node[{idx}] {node['addr']}", flush=True)


if __name__ == "__main__":
    main()