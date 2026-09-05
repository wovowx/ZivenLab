#!/bin/bash
set -e

# ============================================================
# chat2api + xray（VLESS 代理）入口脚本
# 让 chat2api 出站走 VLESS 节点，避免数据中心 IP 被 ChatGPT 风控
#
# 节点管理（2026-09-05 版）：
#   A. NODE_CONFIG_URL 已设置 → 启动时从该 URL 拉取节点列表 JSON
#      格式：{"nodes":[{"addr","port","uuid","sni","host","path"}],"check":{...}}
#      多个节点 = 自动健康检查 + 失效自动切换（由 node_manager.py 常驻管理）
#   B. 未设置 NODE_CONFIG_URL → 回退用环境变量生成单节点列表（兼容旧版）
#
# 节点参数随时改：改配置源里的 JSON（或改环境变量）→ 重启 Revision 生效。
# 详见同目录 DEPLOY.md §节点自动轮换。
# ============================================================

VLESS_ADDR="${VLESS_ADDR:-}"
VLESS_PORT="${VLESS_PORT:-443}"
VLESS_UUID="${VLESS_UUID:-}"
VLESS_SNI="${VLESS_SNI:-magicovo.pages.dev}"
VLESS_HOST="${VLESS_HOST:-magicovo.pages.dev}"
VLESS_PATH="${VLESS_PATH:-/}"
LOCAL_HTTP_PORT="${LOCAL_HTTP_PORT:-10809}"
NODE_CONFIG_URL="${NODE_CONFIG_URL:-}"

# ---- 生成节点列表 /tmp/nodes.json ----
if [ -n "$NODE_CONFIG_URL" ]; then
  echo "Fetching node config from $NODE_CONFIG_URL ..."
  # 用 python3 拉取（python:3.11-slim 自带 urllib，镜像里没有 curl）
  cat > /tmp/fetch_config.py <<'PY'
import sys, urllib.request
url = sys.argv[1]
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=20) as r:
    data = r.read()
with open("/tmp/nodes.json", "wb") as f:
    f.write(data)
PY
  if ! python3 /tmp/fetch_config.py "$NODE_CONFIG_URL"; then
    echo "ERROR: failed to fetch NODE_CONFIG_URL. Fallback to env vars." >&2
    exit 1
  fi
  if [ -s /tmp/nodes.json ]; then
    echo "Node config fetched OK:"
    python3 -c "import json;d=json.load(open('/tmp/nodes.json'));print('  nodes:',len(d.get('nodes',[]) or []))" || true
  else
    echo "ERROR: empty node config from URL, exit." >&2
    exit 1
  fi
else
  if [ -z "$VLESS_ADDR" ] || [ -z "$VLESS_UUID" ]; then
    echo "ERROR: VLESS_ADDR and VLESS_UUID are required (or set NODE_CONFIG_URL)" >&2
    exit 1
  fi
  echo "NODE_CONFIG_URL not set; building single-node config from env vars"
  python3 - "$VLESS_ADDR" "$VLESS_PORT" "$VLESS_UUID" "$VLESS_SNI" "$VLESS_HOST" "$VLESS_PATH" <<'PY'
import json, sys
addr, port, uuid, sni, host, path = sys.argv[1:7]
cfg = {"nodes": [{"addr": addr, "port": int(port), "uuid": uuid, "sni": sni, "host": host, "path": path}]}
with open("/tmp/nodes.json", "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2)
print("  env single-node config written")
PY
fi

echo "LOCAL_HTTP_PORT=${LOCAL_HTTP_PORT}"
echo "PROXY_URL=http://127.0.0.1:${LOCAL_HTTP_PORT}"

# ---- 启动节点管理器（健康检查 + 自动切换，内部启动 xray）----
echo "Starting node_manager.py ..."
python3 /node_manager.py &

# 等代理就绪
sleep 3

# ---- 启动 chat2api（原入口，端口 5005）----
echo "Starting chat2api ..."
cd /app
exec python app.py