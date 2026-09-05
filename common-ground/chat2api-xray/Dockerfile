# chat2api + xray（VLESS 代理）定制镜像
# 用途：让 chat2api 出站走 VLESS 节点，避免数据中心 IP 被 ChatGPT 风控（cf_chl_opt）
#
# 基于官方镜像 lanqian528/chat2api:latest，内置 xray 并在入口脚本中启动
# 节点参数完全由环境变量控制（VLESS_ADDR / VLESS_UUID / VLESS_SNI ...），可随时替换
#
# 维护与排查：见同目录 DEPLOY.md（部署/换节点/MCP patch/踩坑记录）

FROM lanqian528/chat2api:latest

ARG TARGETARCH=amd64

# 安装 xray-core（按架构选择对应版本）
# amd64 -> Xray-linux-64.zip | arm64 -> Xray-linux-arm64-v8a.zip
RUN set -eux; \
    case "${TARGETARCH}" in \
      amd64) XRAY_ARCH="64" ;; \
      arm64) XRAY_ARCH="arm64-v8a" ;; \
      *) echo "Unsupported arch: ${TARGETARCH}" >&2; exit 1 ;; \
    esac; \
    apt-get update && \
    apt-get install -y --no-install-recommends curl unzip ca-certificates && \
    curl -fL -o /tmp/xray.zip "https://github.com/XTLS/Xray-core/releases/download/v26.3.27/Xray-linux-${XRAY_ARCH}.zip" && \
    unzip -o /tmp/xray.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/xray && \
    rm -f /tmp/xray.zip && \
    apt-get purge -y --auto-remove curl unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 消息级 MCP 连接器自动挂载 patch（2026-09-05）
# 在 chatFormat.py 的 api_messages_to_chat() 给每条消息注入
# metadata.developer_mode_connector_ids，使 GPT 无需页面手动加号即可调用 MCP 工具。
# 匹配失败即构建失败（防镜像版本漂移静默改错）。
COPY patch_chatformat.py /patch_chatformat.py
RUN python /patch_chatformat.py && rm /patch_chatformat.py

# 节点管理器（健康检查 + 自动故障切换，2026-09-05）
COPY node_manager.py /node_manager.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5005

ENTRYPOINT ["/entrypoint.sh"]