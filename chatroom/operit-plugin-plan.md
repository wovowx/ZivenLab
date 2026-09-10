# 聊天室 Operit 插件化 · 方案决策记录（Discussion Plan）

> 创建：2026-09-10 16:50 · Ziven
> 状态：**待柳柳拍板**（未开工）
> 用途：把聊天室从「浏览器网页」搬进 Operit 成为原生入口 + 修复哥哥唤醒慢/断的问题。**本文件是唯一真相源**——开工前、换框后、做到一半质疑方向时，回这里看。
> 讨论链：#1001→（柳柳提出）→ Ziven × GPT 两轮架构讨论（2026-09-10 16:21-16:44）

---

## 0. 决策摘要（柳柳拍板前先看这里）

| 问题 | 结论 |
|---|---|
| 聊天室要搬进 Operit 吗？ | ✅ 要。柳柳提出，哥哥 + GPT 都认同 |
| 搬的意义是什么？ | 打开 Operit 就是聊天室（不用开浏览器）；哥哥唤醒链路收进 Operit 生命周期（重启自愈，不再聋） |
| 搬了会变快吗？ | 会。真正的提速点是「唤醒链路少一层转发 + 轮询 5s→1s」，不是 WebView 本身 |
| 云端要改吗？ | 不改。聊天室数据（Supabase）+ 后端（Worker）不变，Operit 只是新入口 |
| 分几步？ | Phase 1 先做入口+唤醒收编；Phase 2 再优化推送（Realtime）；Phase 3 多端平等 |

---

## 1. 现状（已查证 · 2026-09-10）

### 1.1 聊天室现在的实现
- **前端**：`chat.html`（Cloudflare Worker `/chat` 路由从 GitHub raw 实时拉取），浏览器打开 `https://mcp-memory.wovowx.workers.dev/chat` 使用
- **后端**：Worker `/api/chat/...` 路由（`src/tools/chat.js`），读写 Supabase
- **数据**：`chat_threads`（话题）、`chat_messages`（消息+mentions）、`chat_agent_events`（@事件队列）、`agent_chat_state`（消费位置）
- **@触发**：`parseMentions` 扫描 `@ziven`/`@gpt`/`@all` → 给对应 Agent 建 `processing` 事件 → 各 Agent 自己消费
- **角色**：`liuliu`（柳柳）、`ziven`（哥哥）、`gpt`——v2.4 起三方对等

### 1.2 哥哥现在的唤醒链路（慢/断的根因）
```
柳柳 @哥哥
  → Supabase chat_agent_events 产生 processing 事件
  → /root/chat_wake.py（Operit 外孤儿进程，每5秒轮询）
  → 发现事件 → POST 本地 8094 /api/external-chat（async_callback + callback_url）
  → 哥哥 AI 被唤醒 → 处理 → chat_send 回复 + chat_ack_event
```
**痛点**：
1. chat_wake 是 **Operit 外的孤儿进程**——Operit 一重启它就死（柳柳今天实测撞了 3 次）
2. 自动拉起（hook v5）偶发不触发 → 哥哥聋
3. 转发链路长（轮询→HTTP 唤醒→处理→回复），回复慢（GPT 走 chat2api 直连所以快）
4. 现在哥哥回复哥哥要手动 nohup 拉起（PID 22121，绕过 boot_all.sh 存活）

### 1.3 Operit 插件能力（已查证）
- ✅ **ToolPkg 插件格式**：manifest.json + dist/main.js，放在 `/sdcard/Android/data/com.ai.assistance.operit/files/packages/`
- ✅ **侧边栏入口**：`ToolPkg.registerNavigationEntry({surface:"main_sidebar_plugins"})`
- ✅ **WebView 内嵌网页**：`UI.WebView({url: ...})`（哥哥的 deepseek-harness 插件已用，一模一样）
- ✅ **后台进程**：插件可启动后台 python（微信桥接 ws_receiver 先例）
- ✅ **生命周期 hook**：`registerAppLifecycleHook({event:application_on_create})`（唤醒链路 v4 已用）
- ⚠️ **启动期沙盒回收**：hook 直起进程约 60s 内会被回收（真实约束，v3 踩过）
- ⚠️ **进程不保证永活**：插件后台进程 ≠ 系统 daemon，Operit 被强杀/省电回收可能没了（GPT 提醒）

### 1.4 GPT 真身两轮讨论结论（2026-09-10 16:21-16:44）
> 通道：chat2api（conversation 6a9c3dbc，Worker 转发端点）。哥哥 + GPT 语义一致。

| # | 结论 |
|---|---|
| 1 | 聊天室插件化 **值得做**——核心价值不是「变快」，是「Operit 成为聊天室的宿主」 |
| 2 | **WebView 不是加速点**——真正加速的是「event delivery」（把唤醒收进 Operit 生命周期 + pull→push） |
| 3 | chat_wake 搬进插件后台 **可以作为 Phase 1**（跟随 Operit 生命周期，重启自动恢复） |
| 4 | ⚠️ **不要把 chat_wake 业务逻辑原样搬**——插件只做「本地接入」，业务判断留在云端 Worker |
| 5 | ⚠️ **必须保留 claim_event 去重**——多端开着时同一事件只允许一个实例处理（否则柳柳发一句哥哥回三次） |
| 6 | Supabase Realtime（push）留 **Phase 2**（websocket 生命周期/断线重连/Android后台限制，时机不成熟） |
| 7 | 后台进程不保证永活——目标写成「**生命周期内的事件接收能力 + 重启自动恢复**」，不是「永不死」 |

---

## 2. 目标架构（Phase 1 后）

```
Operit（柳柳的手机）
 ├─ ChatRoom Plugin（新 ToolPkg）
 │    ├─ WebView UI ← 内嵌聊天室 URL（https://mcp-memory.wovowx.workers.dev/chat）
 │    └─ Event Receiver（插件生命周期内）
 │         ├─ 轮询云端 pending events（1s 轻轮询，替代 chat_wake.py 5s）
 │         ├─ claim event（保留去重）
 │         └─ POST 本地 8094 /api/external-chat 唤醒哥哥
 │
 └─ Operit AI 哥哥（被唤醒 → chat_send 回复 + ack）
```

**不变**：Supabase 仍是唯一事实源；Worker 业务逻辑不动；聊天室 API 不动。

**消失**：/root/chat_wake.py 孤儿进程、boot_all.sh、wake_stabilizer.sh、ziven.chat_wake_boot hook（全部可由插件生命周期接管）。

---

## 3. Phase 计划

### Phase 1 · 聊天室入口 + 唤醒收编（✅ 现在能做）
| # | 任务 | 验收标准 |
|---|---|---|
| P1.1 | 写 ChatRoom ToolPkg 插件（WebView 内嵌聊天室 URL + 侧边栏入口） | 打开 Operit 侧边栏能看到聊天室，能发消息 |
| P1.2 | 插件启动时拉起 Event Receiver（后台 python 轮询 1s + claim + 8094 唤醒） | Operit 开着时 @哥哥 5s 内被唤醒 |
| P1.3 | Operit 重启后自动恢复（插件生命周期接管） | 重启 Operit → 聊天室入口自动回来 + Event Receiver 自动拉起 |
| P1.4 | 保留 claim 去重 | 同一事件不被多个实例重复处理 |
| P1.5 | 移除旧链路（chat_wake.py / boot_all.sh / 稳定器 / 旧 hook 包） | 无孤儿进程，自启全靠插件 |

**P1.2 与 GPT 的分歧点**：GPT 建议「业务逻辑留在云端，插件只做本地接入」。哥哥倾向 Phase 1 先用「轮询+唤醒」的简单搬移（快、稳），把 claim 去重守住；云端业务层的重构（如果要做）放 Phase 2。**此分歧已记录，开工时如果柳柳有倾向再定。**

### Phase 2 · 事件推送优化（⏸ 后续）
- Supabase Realtime（websocket push）替换轻轮询
- 多设备在线策略（手机 Operit / 桌面 / 浏览器三端平等）
- 云端业务逻辑边界重构（如果 Phase 1 后发现需要）

### Phase 3 · Runtime 统一（远期）
- Agent Runtime Manager（Ziven runtime / GPT runtime / execution runtime 统一事件入口）
- 与 conversation_bindings 结合：明确「哪个 Operit 实例承载哪个 Agent Runtime」

---

## 4. 关键参数 / 凭证（沿用现状，不新造）

| 项 | 值 | 说明 |
|---|---|---|
| 聊天室 URL | https://mcp-memory.wovowx.workers.dev/chat | WebView 内嵌目标 |
| 聊天室线程 ID | 3682f872-070d-4a1f-855d-f7744e9c495c | Common Ground 聊天室 |
| 8094 Bearer | d0c18673c328440eb260901de89f3e1d | Operit 本地 external-chat token |
| 角色卡 ID | 8cafce11-b7b6-43d3-bd95-9c1859dfc2e3 | Ziven |
| 本地聊天 ID | f4dd5a0a-7200-4823-a183-8b015b6df1cc | 唤醒消息绑定的聊天 |
| MCP Worker | https://mcp-memory.wovowx.workers.dev/mcp | 云端 |
| MCP 认证 | CF-Access-Client-Id + Secret（见唤醒链路决策记录） | chat_wake.py 在用 |
| 插件目录 | /sdcard/Android/data/com.ai.assistance.operit/files/packages/ | ToolPkg 部署位置 |

---

## 5. 风险 / 注意

| 风险 | 等级 | 对策 |
|---|---|---|
| 后台进程被 Android 回收 | 中 | Operit 重启自动恢复 + 哥哥兜底技能（聊天室说句话） |
| 多端同时监听 → 重复处理 | 高 | claim_event 必须保留（Chat 事件模型已支持原子 claim） |
| WebView 内嵌后登录/状态丢失 | 中 | 聊天室无登录（公开读），状态在 Cloudflare 侧；如果 localStorage 有状态，WebView 需确认持久化 |
| 插件依赖 Operit 生命周期 | 中 | 设计目标 = 生命周期内工作 + 重启自愈，不追求永远存活 |
| GPT 回复是否也要进聊天室 | 待定 | 当前 GPT 靠 chat2api 被 @ 唤醒；聊天室插件化后续再议 |

---

## 6. 状态记录

| 时间 | 事件 |
|---|---|
| 2026-09-10 16:21 | 柳柳提出「把聊天室从浏览器搬进 Operit 插件，GPT 接进来」 |
| 2026-09-10 16:24 | 哥哥查证聊天室实现 + Operit 插件能力（WebView 可用） |
| 2026-09-10 16:34 | 柳柳要求：搞清楚架构、做好计划、跟 GPT 商量后再动手 |
| 2026-09-10 16:44 | Ziven × GPT 两轮讨论收敛（结论见 §1.4） |
| 2026-09-10 16:50 | 本文档创建，**待柳柳拍板 Phase 1** |

---

## 7. 待柳柳拍板

- [ ] Phase 1 开工？（聊天室 WebView 插件 + Event Receiver 收编）
- [ ] P1.2 分歧点：插件直接轮询+唤醒（哥哥倾向）vs 云端业务层先行重构（GPT 建议）？