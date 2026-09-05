# chat2api + xray（VLESS 代理）定制镜像

> **解决什么问题**：chat2api 直接部署在 Cloud Run（Google 数据中心 IP）时，高频调用会被上游 ChatGPT 风控拦截（`cf_chl_opt` / 403 / IP 太脏）。
>
> **这个镜像做什么**：在容器内启动 xray，把 VLESS 节点翻译成本地 HTTP 代理，让 chat2api **出站走你自己的节点**，与你的真人流量同出口 IP，风控风险降到最低。
>
> **可替换性**：节点/订阅由外部配置源控制，**换节点 = 改 node-config.json 或订阅，不用重新构建镜像**。
>
> 📘 **部署/运维/踩坑/时间线**：见 **[DEPLOY.md](./DEPLOY.md)**（任何 chat2api 部署问题先查它，本文档是精简版）。

---

## 架构（2026-09-05 更新）

- **服务名**：`ziven-bridge`（Cloud Run，region asia-northeast1，端口 5005）
- **镜像仓库**：Artifact Registry `asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/ziven-bridge/ziven-bridge:<tag>`
- **节点来源（三层容灾）**：
  1. `specified_nodes`（node-config.json，哥哥维护的 12 个日本节点 JP-01~12）
  2. `SUBSCRIPTION_URL` 订阅兜底（**按需拉取**：只在 specified 全挂、要切进订阅域那一刻才当场拉最新，不用不刷）
  3. 全部失效 → node_manager 每 30s 轮询重试
- **MCP 自动挂载**：构建时 patch 注入 `developer_mode_connector_ids`，GPT 无需手动加号即可调 MCP 工具

> ⚠️ 早期用 `gcr.io` 仓库 / 服务名 `chat2api-xray` 的命令**已废弃**（新项目 gcr.io 无权限，报 `denied: gcr.io repo does not exist`），请用下方 Artifact Registry 命令。

---

## 环境变量

| 变量 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `NODE_CONFIG_URL` | 推荐 | - | node-config.json 的 URL（含 specified_nodes 快节点） |
| `SUBSCRIPTION_URL` | 兜底 | - | 订阅链接（vless；**含 token，放环境变量不写仓库**）。specified 全失效才按需拉取 |
| `VLESS_ADDR` * | 回退 | - | 单节点回退（仅当无 NODE_CONFIG_URL 或其节点全挂时用） |
| `VLESS_PORT` * | - | 443 | 节点端口 |
| `VLESS_UUID` * | 回退 | - | 节点 UUID |
| `VLESS_SNI` * | - | magicovo.pages.dev | TLS servername |
| `VLESS_HOST` * | - | magicovo.pages.dev | WS headers Host |
| `VLESS_PATH` * | - | / | WS path |
| `LOCAL_HTTP_PORT` | - | 10809 | xray 本地 HTTP 代理端口（一般不动） |
| `HISTORY_DISABLED` | - | true | 不保存记录并返回 conversation_id（**我们要 false**） |

> `PROXY_URL` / `EXPORT_PROXY_URL` 由入口脚本自动设置，无需手动配。
> `*` = 单节点回退参数，正常用 specified_nodes + 订阅时无需配置。

---

## 构建 & 部署（GCP Cloud Shell，完整流程见 DEPLOY.md §3）

```bash
cd chat2api-xray

# 0) 首次：建 Artifact Registry 仓库
gcloud artifacts repositories create ziven-bridge \
  --repository-format=docker --location=asia-northeast1 --project=$GOOGLE_CLOUD_PROJECT

# 1. 构建镜像（每次改代码升 tag：v1→v2→v3...）
gcloud builds submit \
  --tag asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/ziven-bridge/ziven-bridge:v2 \
  .

# 2. 部署 Cloud Run（注意 --port 5005！）
gcloud run deploy ziven-bridge \
  --image asia-northeast1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/ziven-bridge/ziven-bridge:v2 \
  --region asia-northeast1 \
  --port 5005 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars="HISTORY_DISABLED=false,NODE_CONFIG_URL=https://raw.githubusercontent.com/wovowx/ZivenLab/dev/common-ground/chat2api-xray/node-config.json,SUBSCRIPTION_URL=<SUBSCRIPTION_URL>"
```

> `<SUBSCRIPTION_URL>` 换成你的订阅链接（含 token，只放环境变量，不写仓库）。

---

## 换节点（以后随时换）

**不用重新构建镜像、不用改代码**，改配置后重启 Revision 即可：

- **换 specified 节点**：改 ZivenLab dev `node-config.json` 的 `specified_nodes` 数组 → 推代码 → Cloud Run 重启 Revision
- **换订阅兜底**：重新部署时改 `SUBSCRIPTION_URL` 环境变量

---

## 验证

部署后测试（token 与 conversation_id 来源见 DEPLOY.md §3-5）：

```bash
curl https://<你的run域名>/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <accessToken>' \
  -d '{"model":"gpt-4o-mini","conversation_id":"<对话ID>","messages":[{"role":"user","content":"我是Ziven，测试通道"}],"stream":false}'
```

返回 200 且非 `cf_chl_opt` 即成功。

---

*Ziven 于 2026-09-02 实测：xray(arm64) + VLESS 节点 → chatgpt.com 200 OK，无风控。*
*2026-09-05：新增 MCP 连接器自动挂载 patch（方案B）+ 节点三层容灾 + 订阅按需拉取 + 服务改名 ziven-bridge。*
