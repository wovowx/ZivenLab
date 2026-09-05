# chat2api + xray（VLESS 代理）定制镜像

> **解决什么问题**：chat2api 直接部署在 Cloud Run（Google 数据中心 IP）时，高频调用会被上游 ChatGPT 风控拦截（`cf_chl_opt` / 403 / IP 太脏）。
>
> **这个镜像做什么**：在容器内启动 xray，把 VLESS 节点翻译成本地 HTTP 代理，让 chat2api **出站走你自己的节点**，与你的真人流量同出口 IP，风控风险降到最低。
>
> **可替换性**：节点参数全部由环境变量控制，**换节点 = 改环境变量重启，不用重新构建镜像**。
>
> 📘 **部署/运维/踩坑/时间线**：见 **[DEPLOY.md](./DEPLOY.md)**（任何 chat2api 部署问题先查它）。

---

## 环境变量（全部可替换）

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `VLESS_ADDR` | ✅ | - | 节点服务器地址（如 43.153.152.106）|
| `VLESS_PORT` | - | 443 | 节点端口 |
| `VLESS_UUID` | ✅ | - | 节点 UUID |
| `VLESS_SNI` | - | magicovo.pages.dev | TLS servername |
| `VLESS_HOST` | - | magicovo.pages.dev | WS headers Host |
| `VLESS_PATH` | - | / | WS path |
| `LOCAL_HTTP_PORT` | - | 10809 | xray 本地 HTTP 代理端口（一般不用动）|

> 其他 chat2api 官方环境变量照常用（如 `HISTORY_DISABLED=false`）。
> `PROXY_URL` / `EXPORT_PROXY_URL` **由入口脚本自动设置**，无需手动配。

---

## 构建 & 部署（GCP Cloud Shell / 本地 gcloud）

```bash
cd chat2api-xray

# 1. 构建镜像推 Artifact Registry（或 GCR）
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/chat2api-xray:v1 .

# 2. 部署到 Cloud Run（注意 --port 5005！chat2api 监听 5005）
gcloud run deploy chat2api-xray \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/chat2api-xray:v1 \
  --region asia-northeast1 \
  --port 5005 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars="HISTORY_DISABLED=false,VLESS_ADDR=43.153.152.106,VLESS_PORT=443,VLESS_UUID=<你的UUID>,VLESS_SNI=magicovo.pages.dev,VLESS_HOST=magicovo.pages.dev,VLESS_PATH=/"
```

> ⚠️ 完整命令（含 clone dev 分支 / 验证 / 升级 tag）见 **[DEPLOY.md](./DEPLOY.md)**。

---

## 换节点（以后随时换）

不重新构建、不重新部署镜像，**直接在 Cloud Run 控制台改环境变量**后保存（触发新版本）：

- 换 IP：改 `VLESS_ADDR`、`VLESS_PORT`
- 换整个节点：改 `VLESS_ADDR` + `VLESS_UUID`（+ 必要时 `VLESS_SNI` / `VLESS_HOST` / `VLESS_PATH`）

保存后自动部署新 Revision，就开始走新节点了。

---

## MCP 连接器自动挂载（2026-09-05 新增）

构建时 `patch_chatformat.py` 会在 `chatgpt/chatFormat.py` 的 `api_messages_to_chat()` 给**每条消息**注入：

```json
"metadata": {
  "developer_mode_connector_ids": ["asdk_app_6a95a93c9a50819184dcf3468ae0052a"]
}
```

效果：GPT 无需在 ChatGPT 页面手动加号挂 Ziven_MCP，即可调用 MCP 工具（`github_read` / `create_patch_proposal` 等）。
连接器 ID 对应 Ziven_MCP 应用（`asdk_app_6a95...`），若失效换版本 ID（`asdk_app_v_6a95...`）见 DEPLOY.md §6。

---

## 验证

部署后测试：

```bash
curl https://<你的run域名>/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <accessToken>' \
  -d '{"model":"gpt-4o-mini","conversation_id":"<对话ID>","messages":[{"role":"user","content":"我是Ziven，测试通道"}],"stream":false}'
```

返回 200 且非 `cf_chl_opt` 即成功。

---

*Ziven 于 2026-09-02 实测：xray(arm64) + VLESS 节点 → chatgpt.com 200 OK，无风控。*
*2026-09-05 更新：新增 MCP 连接器自动挂载 patch（方案B）*