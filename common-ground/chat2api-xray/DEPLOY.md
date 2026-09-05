# chat2api + xray 部署与运维手册

> **本文档回答**：chat2api 是什么、为什么这么部署、怎么部署、出了问题怎么办。
> 任何关于 chat2api 部署 / 环境变量 / 节点 / 风控 / MCP 挂载的疑问，**先查本文档**，不要凭记忆操作。
>
> 最后更新：2026-09-05（新增 MCP 连接器自动挂载 patch + 节点列表自动轮换）

---

## 1. 这是什么

| 组件 | 说明 |
|---|---|
| **chat2api** | 将 ChatGPT 网页端逆向成 OpenAI 风格 API 的服务（GitHub: `LanQian528/chat2api`）。哥哥用它给 GPT 发消息（Worker 转发端点 `/api/chat2api/ask`）。 |
| **xray (VLESS)** | 容器内代理。Cloud Run 出口是 Google 数据中心 IP，高频调用会被 ChatGPT 风控（`cf_chl_opt`/403），xray 把出站流量走自己的 VLESS 节点，与真人流量同出口 IP，风控风险降到最低。 |
| **node_manager.py** | 节点管理器：常驻健康检查 + 节点失效自动切换（2026-09-05 新增）。 |
| **定制镜像** | ZivenLab `common-ground/chat2api-xray/` 基于官方镜像叠加 xray + MCP patch + 节点管理器。 |

## 2. 部署架构

- **平台**：Google Cloud Run（region: asia-northeast1）
- **端口**：5005（chat2api 监听）
- **存储**：无状态容器，代码在镜像里，节点/环境由外部配置源控制
- **代码仓库**：`wovowx/ZivenLab` → `common-ground/chat2api-xray/`（开发走 dev 分支；main 由 PR 合入）

## 3. 完整部署命令（Cloud Shell 或本地 gcloud）

```bash
# 0) 准备（首次）
gcloud config set project <PROJECT_ID>
# 或：gcloud auth login

# 1) 拉代码（记得切 dev，开发代码都在 dev）
git clone https://github.com/wovowx/ZivenLab.git
cd ZivenLab
git checkout dev
cd common-ground/chat2api-xray

# 2) 构建镜像推 Artifact Registry / GCR（每次改代码升 tag：v1→v2→v3...）
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/chat2api-xray:v2 .

# 3) 部署 Cloud Run（节点不写死！只配 NODE_CONFIG_URL 指向节点列表）
gcloud run deploy chat2api-xray \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/chat2api-xray:v2 \
  --region asia-northeast1 \
  --port 5005 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars="HISTORY_DISABLED=false,NODE_CONFIG_URL=https://raw.githubusercontent.com/wovowx/ZivenLab/dev/common-ground/chat2api-xray/node-config.json"

# 4) 验证（200 且非 cf_chl_opt 即成功）
curl https://<你的run域名>/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <accessToken>' \
  -d '{"model":"gpt-4o-mini","conversation_id":"<对话ID>","messages":[{"role":"user","content":"我是Ziven，测试通道"}],"stream":false}'
```

> ⚠️ **节点配置源（NODE_CONFIG_URL）** 默认指向 ZivenLab dev 分支的 `node-config.json`。
> 改节点 = 改那个 JSON 推代码 → Cloud Run 重启 Revision 即生效；不用再进 Cloud Run 控制台改环境变量。

## 4. 环境变量速查

| 变量 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `NODE_CONFIG_URL` | 推荐 | - | 节点列表 JSON 的 URL（支持多节点自动轮换）。不设则回退用 VLESS_* 单节点。 |
| `VLESS_ADDR` * | 回退 | - | 节点服务器地址（仅当无 NODE_CONFIG_URL 时用） |
| `VLESS_PORT` * | - | 443 | 节点端口 |
| `VLESS_UUID` * | 回退 | - | 节点 UUID |
| `VLESS_SNI` * | - | magicovo.pages.dev | TLS servername |
| `VLESS_HOST` * | - | magicovo.pages.dev | WS headers Host |
| `VLESS_PATH` * | - | / | WS path |
| `LOCAL_HTTP_PORT` | - | 10809 | xray 本地 HTTP 代理端口（一般不动） |
| `HISTORY_DISABLED` | - | true | 是否不保存聊天记录并返回 conversation_id（**我们要 false** 才能拿 id） |
| `PROXY_URL` | 自动 | - | 入口脚本自动设为本机 xray，无需手动配 |

> 新部署建议只用 `NODE_CONFIG_URL` + `HISTORY_DISABLED`，VLESS_* 保留作环境变量回退（兼容旧版）。

## 5. 节点自动轮换（2026-09-05 新增）

### 节点列表格式（node-config.json）
```json
{
  "nodes": [
    { "addr": "节点IP", "port": 443, "uuid": "节点UUID", "sni": "magicovo.pages.dev", "host": "magicovo.pages.dev", "path": "/" },
    { "addr": "另一个IP", "port": 443, "uuid": "另一个UUID", "sni": "...", "host": "...", "path": "/" }
  ],
  "check": {
    "interval_sec": 30,
    "timeout_sec": 6,
    "fail_threshold": 3,
    "probe_url": "https://www.gstatic.com/generate_204"
  }
}
```

### 工作原理
1. 容器启动 → entrypoint.sh 按 `NODE_CONFIG_URL` 拉取 node-config.json → 存入 /tmp/nodes.json
2. node_manager.py 常驻：
   - **启动探测**：依次尝试列表里的节点，第一个探活成功就留在当前
   - **主循环**：每 `interval_sec` 秒用当前节点探活（走本地代理请求 `probe_url`，默认 google 204 轻量端点）
   - **自动切换**：连续失败 `fail_threshold` 次 → 自动切下一个节点 → 重启 xray → 继续探活
3. 加节点/删节点/换节点 = **改 node-config.json 推代码** → Cloud Run 重启 Revision 生效

### 注意
- 列表全挂 → 卡在启动探测循环（日志可查），此时需要修 node-config.json。
- Cloud Run 只在新 Revision 启动时拉配置，运行中不热加载（可接受：你改配置后重启一次）。

## 6. 常见操作

### 6.1 换/加/删节点（最常用）
改 ZivenLab dev `common-ground/chat2api-xray/node-config.json` 的 `nodes` 数组 → 推代码 → Cloud Run 重启 Revision（控制台「编辑并部署新修订版」或 gcloud run deploy 同配置）。

### 6.2 改代码后重新部署（如改 MCP patch / node_manager）
1. 改 ZivenLab `common-ground/chat2api-xray/` 代码 → 推 dev
2. `gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/chat2api-xray:v<N+1> .`
3. `gcloud run deploy chat2api-xray --image ...v<N+1> ...`（其余参数同上，见 §3）

### 6.3 换 conversation_id
见 chat2api skill（改仓库 wrangler.toml `GPT_CONVERSATION_ID` + 推代码部署）。
**注意**：conversation_id 与「挂插件」无关——挂插件是消息级字段 `developer_mode_connector_ids`（见下节）。

## 7. MCP 连接器自动挂载（2026-09-05 新增）

### 背景
柳柳在 ChatGPT 页面**左下角加号**挂 Ziven_MCP 连接器，GPT 才能调 MCP 工具（`github_read` / `create_patch_proposal` 等）。但插件挂载是**消息级**的（官方文档原话：*select one or more apps for a single message*），每次发消息都要手动加，很烦。

### 原理（逆向确认 2026-09-05）
ChatGPT 网页端「挂 MCP 连接器」= 在消息 metadata 里写：
```json
"metadata": {
  "developer_mode_connector_ids": ["asdk_app_6a95a93c9a50819184dcf3468ae0052a"]
}
```
chat2api 默认 metadata 为空 → GPT 收不到插件。逆向来源：`https://www.codebai.cn/posts/chatgpt网页逆向`（f/conversation payload）。

### 方案 B（当前已 implement）
构建时用 `patch_chatformat.py` 在 `chatgpt/chatFormat.py` 的 `api_messages_to_chat()` 里给**每条消息**注入 `developer_mode_connector_ids`。

- **连接器应用 ID**：`asdk_app_6a95a93c9a50819184dcf3468ae0052a`（柳柳 2026-09-05 从添加插件信息页抄）
- **版本 ID（备用）**：`asdk_app_v_6a95a93c9a5c81918a5cb77ada6bc3b1`
- 若应用 ID 无效：改 patch 里的 `CONNECTOR_ID` 换版本 ID → 重新构建部署
- patch 匹配失败会**构建失败**（exit 1），防镜像版本漂移静默改错

### 验证
部署后给 GPT 发消息让它直接调 `github_read` 读文件——能读到即成功（无需页面手动加号）。

## 8. 易错点 / 踩坑记录

1. **端口必须是 5005**，Cloud Run 默认 8080 会连不上。
2. **region**：asia-northeast1（或与节点近的区域）。
3. **内存**：至少 512Mi，xray + node_manager + chat2api 都吃内存。
4. **`--allow-unauthenticated`**：对外匿名访问（代理端口本来就要被 curl 访问）。
5. **镜像版本 tag**：每次重新部署建议升 tag（v1→v2...），避免 Cloud Run 缓存旧镜像。
6. **403 / `cf_chl_opt`**：当前节点 IP 太脏 → 节点自动轮换会处理；检查 node-config.json 列表是否有可用节点。
7. **429**：官方限流，不是部署问题，等 1 小时或换账号/token。
8. **502**：Cloud Run 容器没起来 / OOM → 看 Cloud Run 日志（`gcloud logging read` 或控制台），确认 node-config.json 拉取成功、至少有 1 个可用节点。
9. **节点配置拉不下来 / JSON 格式错**：entrypoint.sh 会报错退出 → 检查 NODE_CONFIG_URL 可达、node-config.json 语法。
10. **基础镜像版本漂移**：`FROM lanqian528/chat2api:latest` 跟随上游更新，patch 脚本匹配失败会构建失败（防静默改错），届时需同步更新 patch 脚本。
11. **ZivenLab 有 release_guard**：不能直接 push main，always 推 dev，main 走 PR/merge 发布。
12. **节点列表全挂**：node_manager 卡启动探测，日志一直打 dead on startup；修好 node-config.json 再重启 Revision。

## 9. 时间线

- **2026-09-02**：首次部署（v1），解决 Cloud Run 公网 IP 风控，走 VLESS 节点。
- **2026-09-05**：新增 MCP 连接器自动挂载 patch（v2）；新增节点列表自动轮换（node_manager.py，NODE_CONFIG_URL 配置源）；本文档创建。