#!/bin/bash
set -e

# ============================================================
# chat2api + xray（VLESS 代理）入口脚本
# 让 chat2api 出站走 VLESS 节点，避免数据中心 IP 被 ChatGPT 风控
#
# 所有节点参数通过环境变量传入，换节点 = 改环境变量重启，无需重新构建
# ============================================================

# ---- 可替换节点配置（环境变量） ----
# VLESS_ADDR  节点服务器地址（必填）
# VLESS_PORT  节点端口（默认 443）
# VLESS_UUID  用户 UUID（必填）
# VLESS_SNI   TLS servername（默认 magicovo.pages.dev）
# VLESS_HOST   WS headers Host（默认 magicovo.pages.dev）
# VLESS_PATH   WS path（默认 /）
# LOCAL_HTTP_PORT  xray 本地 HTTP 代理端口（默认 10809）

VLESS_ADDR="${VLESS_ADDR:-}"
VLESS_PORT="${VLESS_PORT:-443}"
VLESS_UUID="${VLESS_UUID:-}"
VLESS_SNI="${VLESS_SNI:-magicovo.pages.dev}"
VLESS_HOST="${VLESS_HOST:-magicovo.pages.dev}"
VLESS_PATH="${VLESS_PATH:-/}"
LOCAL_HTTP_PORT="${LOCAL_HTTP_PORT:-10809}"

if [ -z "$VLESS_ADDR" ] || [ -z "$VLESS_UUID" ]; then
  echo "ERROR: VLESS_ADDR and VLESS_UUID are required (set as env vars)" >&2
  exit 1
fi

# ---- 生成 xray 配置 ----
cat > /tmp/xray_config.json <<EOF
{
  "log": {"loglevel": "warning"},
  "inbounds": [
    {
      "tag": "http",
      "port": ${LOCAL_HTTP_PORT},
      "listen": "127.0.0.1",
      "protocol": "http",
      "settings": {}
    }
  ],
  "outbounds": [
    {
      "tag": "node",
      "protocol": "vless",
      "settings": {
        "vnext": [
          {
            "address": "${VLESS_ADDR}",
            "port": ${VLESS_PORT},
            "users": [
              {"id": "${VLESS_UUID}", "encryption": "none"}
            ]
          }
        ]
      },
      "streamSettings": {
        "network": "ws",
        "security": "tls",
        "tlsSettings": {
          "serverName": "${VLESS_SNI}",
          "allowInsecure": false,
          "fingerprint": "chrome"
        },
        "wsSettings": {
          "path": "${VLESS_PATH}",
          "headers": {"Host": "${VLESS_HOST}"}
        }
      }
    },
    {"tag": "direct", "protocol": "freedom"}
  ],
  "routing": {
    "rules": [
      {"type": "field", "outboundTag": "direct", "network": "tcp,udp", "port": 1}
    ]
  }
}
EOF

# ---- 启动 xray（后台）----
echo "Starting xray via ${VLESS_ADDR}:${VLESS_PORT} (${VLESS_SNI}) ..."
/usr/local/bin/xray run -c /tmp/xray_config.json &
XRAY_PID=$!

sleep 2

# ---- chat2api 出站走本地代理 ----
export PROXY_URL="http://127.0.0.1:${LOCAL_HTTP_PORT}"
export EXPORT_PROXY_URL="${PROXY_URL}"

echo "PROXY_URL=${PROXY_URL}"
echo "Starting chat2api ..."

# ---- 启动 chat2api（原入口，端口 5005）----
cd /app
exec python app.py
