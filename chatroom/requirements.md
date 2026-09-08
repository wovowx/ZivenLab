# 聊天室 · 完整需求全景与进度（v4 定稿）

> 整理：Ziven + GPT 对齐（2026-09-04 00:18）· 柳柳确认后执行
> **本文件是需求唯一真相源**：00-83 号散档已合并于此；任何新增需求/进度先更新本文件，再补详细分档
> 对齐过程：Ziven 整理 00a v1 → GPT 审查（#329）→ Ziven 回应保留意见（#331）→ GPT 接受折中并补充设计原则（#332）→ 定稿
> **v3（2026-09-08 柳柳拍板梳理）**：① 需求全景补入 M 系列执行路线（需求 12-16）② 明确分工——**需求归本文件（what），状态归驾驶舱（where）**，驾驶舱以需求编号引用本文件，不复制需求全文，防双源漂移
> **v4（2026-09-08 柳柳拍板整合）**：吸收柳柳 2026-09-07 晚原始需求 8 条（场景路由/固定ID/换ID/多对话框/项目主线/@注入/@UI/聊天绑项目）；新增「需求关系导读」（认知链）；需求 13 补 Context Isolation 全局架构约束；需求 15 升级 Project Mainline 完整生命周期；需求 16 升级 Conversation & Scene Routing（能力 + 设计附录分离）
> **v4.1（2026-09-08 柳柳拍板 · 执行 GPT 独立框）**：柳柳亲定——**执行代码/操作的 GPT 与带 id 讨论 GPT 彻底分开**：聊天室单独开一个执行聊天框（execution-room）专放执行会话；每次换执行 GPT 的 conversation_id 就更新绑定新 id 到这个框。执行 GPT 是「新的执行 Runtime 加入项目」，用独立 **Execution Bootstrap Context**（task/project/constraints/files），不复用 Rejoin 补看 delta；**delta=过程记忆（聊天废话不给），knowledge=结论状态（当前决定/实现位置必须有）**；执行框 thread 长期存在、conversation_id 短生命周期；conversation_bindings 加 purpose=execution/exclusive/temporary；换 id=归档旧+新增新+写 conversation_binding_changed 事件；领 id 走 execution_session_manager（execution_session_init 先初始化再任务，不做隐式初始化）。对应需求 16 Execution Runtime 细化 + 架构 B4。

---

## 〇、项目定义（一句话）

> **Common Ground 的核心不是让 GPT / Ziven 聊天，而是让三方产生可验证、可追踪、可演化的共同知识。**

柳柳 + Ziven + GPT 的共同异步协作空间：有聊天体验，本质是 Agent 协作协议层 + 共享项目记忆层 + 事件驱动 Runtime 层。

---

## 一、设计原则（架构约束，非功能项，禁止误删）

> GPT 建议：这些不是功能而是架构约束，单独成章，避免以后新增功能时被当功能误删。

### P1. 页面可见铁律（最高原则）
所有 Agent 间通信都必须有可追踪记录、柳柳页面可见：
- 用户消息 / GPT 回复 / Ziven 回复
- tool call / tool result
- summary / approval / system 事件摘要
> 原因：否则审计会断链。

### P2. 消息是事实，event 是派生物
`chat_message` 是唯一真相源；`agent_event` 由 mentions parser 派生，不是主数据源。

```
chat_message → mentions parser → agent_event → processor
```

### P3. 三层知识边界（不要混）
| 层 | 是什么 | 示例 |
|---|---|---|
| `thread_contexts` | 当前工作台便利贴，短期状态，可覆盖 | 当前任务 / 已确认决定 / 未解决问题 / 下一步 |
| `memory` | Agent 长期身份 / 偏好 / 经验，不随项目变化 | Ziven 怎么对柳柳 / GPT 风格 |
| `documents` | 项目事实 / 设计决策 / 规范 | 本文档、里程碑、方案 |

### P4. 不把任何一方的话当真理
互相查缺补漏；先验证据再下结论；决策要可回溯「为什么这么决定」。

### P5. 柳柳拍板
决策权归柳柳；Agent 主动发现问题/提建议，无权直接执行。

### P6. 稳定性协议（Reliability Protocol，原「冷却限流」）
不叫「防轰炸」——它同时保护：GPT API 配额 / Agent 自循环 / webhook 重试风暴 / MCP 工具链压力。
- 最小版（P0 尾）：Agent↔Agent 生效；`thread_id` 全局 30s；`thread_id+author+target_agent` 60s；liuliu 永不限流；返回 `retry_after` 不硬失败
- 完整版（P1）：可配置阈值 + 指数 backoff + fallback 队列 + 403 监控自动恢复

### P7. 身份声明
GPT / Ziven 以 `author=agent_id` 发言，不伪装成人。

### P8. 分工模式
GPT 写代码（便宜快），Ziven 落地 + 测试监工 + 验收，柳柳拍板 + 保护小钱包。

### P9. 聊天 ≠ 记忆
原始讨论是过程，沉淀到 documents / GitHub 才是长期知识；不把聊天流水账直接塞长期记忆。

---

## 二、核心主张（柳柳，2026-09-02 定）

1. **对话框 = 项目**：每个 Thread 是一个项目（显示 项目#N），技术上保留 `thread.type / purpose`（项目 / 临时讨论 / 调试 / 系统事件）不强约束死
2. **每句话有编号**：消息 #N，快速定位
3. **每项目一份里程碑文档**：提炼各阶段重点（做了什么 / 讨论了哪些方案 / 最终结构）
4. **所有消息页面可见（铁律）**：任何 Agent 通信（含 chat2api 直聊、工具调用、总结结果）都写 chat_messages

---

## 二点五、需求关系导读（认知链 · v4 新增）

> 需求 1-16 不是互相独立的四个功能，而是**一条认知链**：
> `我在哪个空间？(scene) → 我接哪个身份？(binding) → 我缺什么上下文？(rejoin) → 这个项目走到哪？(mainline)`

```
场景 / 聊天空间
    ↓
Conversation & Scene Routing（需求 16）   ← 我在哪个空间？接入哪个身份？
    ↓
Agent Rejoin Context（需求 13）            ← 我缺什么上下文？（默认当前 thread，显式才跨空间）
    ↓
Mention UX（需求 14）                      ← 我怎么被找到？
    ↓
Project Mainline（需求 15）                ← 这个项目为什么继续？
```

同时：**Thread（在哪儿聊）→ Project Binding → Project（语义空间）→ Mainline（项目路线）**，一个项目可拥有多个聊天线程；一个聊天线程只能属于一个主要项目上下文。

---

## 三、需求全景（9 项 + 权限模型 + decisions 层）

| # | 需求 | 落点 | 优先级 |
|---|---|---|---|
| 1 | 对话框 = 项目有编号 | chat_threads（含 status: active/paused/archived + type） | ✅ 已上线 |
| 2 | 每条消息有编号定位 | message_id + #N | ✅ 已上线 |
| 3 | 里程碑档案 | thread_milestones 表 | 🟡 P3 |
| 4 | 长对话自动归档 | **触发：token 超阈值 / 新阶段 / 用户要求 / 长时间暂停**（20~30 条降为参考阈值，非死板规则） | 🟡 P1 |
| 5 | AI 续命便利贴 | thread_contexts = 短期工作状态（非记忆） | ⚠️ 半自动，P1 全自动 |
| 6 | 可插拔总结器 | summarization_jobs + SUMMARIZER | 🟡 P3 |
| 7 | **所有通信页面可见（铁律）** | 任何 Agent 通信写 chat_messages | ✅ 铁律 |
| 8 | 多媒体 | chat_attachments 表 | 🟡 P3 预留 |
| 9 | TTS 接口 | audio_url + /upload | 🟡 P3 预留 |
| 10 | **权限模型**（新增） | agent_identity + tool_permission + approval_policy + audit_log；与 MCP Bridge 同期设计，不做完工具再补权限 | 🔴 P2 同期 |
| 11 | **decisions 独立层**（新增） | chat_messages（发生了什么）→ events（触发了什么）→ decisions（决定了什么）→ documents（沉淀知识） | 🔴 P0 尾基础结构 |
| 12 | **M1.1 Agent Presence State** | agent_chat_state 表 + chat.js 写入逻辑（Agent 在场状态） | ✅ 已上线 v6.26.0 |
| 13 | **M1.2 Agent Rejoin Context（缺席 Agent 补看 · 当前主线）** | **所有缺席 Agent（GPT + Ziven + 未来）补看「没被 @ 的消息」**；送达路径不同：GPT 走 chat2api（buildSystemPrompt 拼 [AGENT_CONTEXT]），Ziven 走隧道唤醒注入；补「**Context Isolation**」：默认恢复当前 thread，禁止自动跨 thread 合并，显式引用/授权才允许跨空间读取 | 🔴 P0 尾（v6.27.x 代码在，**闭环未成**）：GPT 注入透传待排查 + Ziven 侧待注入 |
| 14 | **M1.3 Mention UX** | @ 交互体验（自动提示/补齐/防错） | 🟡 P1 |
| 15 | **Project Mainline v1（项目主线）** | 主线 + 指针 + UI 当前节点卡片；完整生命周期：15.1 主线建立（启动讨论→定路线→节点）→ 15.2 节点推进（planned/active/completed/paused/branched/abandoned）→ 15.3 分支管理（复杂节点独立子文档，主线留摘要+链接）→ 15.4 主线更新（节点完成/方向改变/新发现→实时更新）；变更规则：**方向变化 = decision change（需确认流程）/ 执行变化 = execution update（执行者可更新）**，不绑定维护角色；补 **Project Binding**（thread→project→mainline 架构关系） | 🟡 P1 |
| 16 | **Conversation & Scene Routing（场景路由 + 接入绑定）** | 系统支持聊天空间与 Agent 接入身份之间**稳定映射、切换和历史追踪**，并支持**显式跨空间访问**（带明确授权）；拆 16.1 场景模型（workspace/personal_chat/project_chat/debug）/ 16.2 Conversation Binding（thread↕agent↕conversation 多对多）/ 16.3 生命周期（固定 ID/换 ID/迁移/fallback）；conversation_bindings 等表 → **设计附录**（需求=能力，表=实现）；**Execution Runtime 细化（v4.1 柳柳拍板）**：执行 GPT 独立身份+独立执行聊天框（execution-room）；Execution Bootstrap Context（task/project/constraints/files，复用 context_resolver 拆 resolve_execution_context()）；执行框 thread 长期、conversation_id 短生命周期；换 id=归档+新增+写事件（execution_session_manager 触发，非聊天行为）；领 id=execution_session_init 空初始化→写 binding→再任务；execution_run 模型（P2/P3 预留） | 🟡 P2 |

> 需求 1-9 原始出处：76 需求全景 + 77 GPT 补漏；10-11 为 00a v2 对齐新增；12-16 为 v3 补入 M 系列执行路线（柳柳 2026-09-08 拍板梳理，来源：implementation.md 状态速览 + 执行路线定稿）

---

## 四、数据模型（升级版）

```
chat_threads（项目；status: active/paused/archived；type: project/discussion/debug/system）
  ├── thread_members（谁能参与）← actors（身份）
  ├── chat_messages（消息，唯一真相源；message_number/actor_id/mentions/tool_calls）
  ├── thread_contexts（短期工作状态便利贴，版本化）
  ├── decisions（决策记录：决定什么/谁决定/何时决定/后来是否推翻）← 新增
  ├── thread_milestones（里程碑，预留）
  ├── thread_artifacts（方案/报告 = documents 层，预留）
  ├── chat_agent_events（事件，派生）
  ├── agent_tool_calls（工具审计）
  ├── tool_permissions / approval_policy（权限层，与 MCP Bridge 同期）← 新增
  └── thread_message_counter（编号计数器）
```

---

## 五、优先级定稿（2026-09-04 三方对齐）

### P0 · 聊天室成为可靠协作空间（转战前必须）
1. 三方触发 + 真@ ✅（已完成 v2.4）
2. 页面可见铁律落地
3. event 去重 / depth 上限 / 防循环
4. webhook 真实链验证
5. 最小限流版（稳定性协议最小集）
6. 历史 processing 事件清理
7. decisions 基础结构

### P1 · 稳定体验
- 冷却限流完整版（可配阈值 + backoff + fallback）
- 手机端 / thread 加载修复
- 自动归档机制（thread_contexts 全自动）
- GPT 403 监控与自动恢复

### P2 · Agent 能力
- MCP Bridge（step1 骨架 + step2 L1 只读 → L2 审计 → L3 审批）
- 权限审批模型 + 聊天室 UI 审批卡片
- API 版 Ziven

### P3 · 智能化
- 自动总结器 / 自动里程碑生成
- 多媒体 / TTS

---

## 六、进度脉络（时间线）

### ✅ 已完成
| 号 | 内容 |
|---|---|
| 00-37 | 项目启动 → MVP 方案 → 数据模型 → v6.4 测试 |
| 38-61 | 通信层 / chat.js / chat_mcp / E2E 全链路 PASS |
| 62-73 | Agent 自动发现 / Phase1 / 触发链 PoC / 治理清单 |
| 74-75 | GPT 真身接入（chat2api PASS）/ Thread Context v1 |
| 76-82 | 需求定稿 / 补漏 / Migration Plan / 确认 / Migration1 / 优化点 / 交接 |
| 83 | 2026-09-03 晚进展（GPT 通道修复 + v2.4 + MCP Bridge 对齐） |
| v2.1-v2.4 | 双写+计数器 / 缓存 / tool_calls / **三方对等+真@mentions（PR#90 全绿）** |
| A4 | @ziven 唤醒桥 v1（60s 轮询 workflow） |
| 00a v1 | 唯一索引文档（本文件前身） |
| 09-06 | **P0-2 Phase2 Ziven 消费链 MVP 闭环**（柳柳亲手 @ziven 验收）；M1-a dispatcher 上线 v6.22.0/1/3；隧道 setsid 常驻；**M1-b 回复可见性三件套 v6.25.0/1；M1.1 Agent Presence State v6.26.0** |
| 09-07 | **M1.2 Recovery Package 代码**（v6.27.x：context_resolver + [AGENT_CONTEXT] + debug 端点，v6.27.6 VERIFIED）；聊天室目录整合（chatroom/ 唯一根 + README）；github_move 工具（v6.29.0/v6.32.0）；neat-freak 洁癖 skill 上传 + 机制内嵌（v6.30.0/v6.31.0） |
| 09-08 | 需求梳理 v3（本文件）：补入 M 系列需求 12-16，明确「需求归本文件/状态归驾驶舱」分工 |

### 🚧 进行中 / 待办
- **M1.2 闭环（需求 13 · 当前主线）**：GPT 侧注入透传待排查（v6.27.x 注入挂在 event_processor/Runtime A，与 GPT 实际消费路径脱节——详见 chatroom/implementation.md §4）+ Ziven 侧隧道注入待接。
- 其余见「五、优先级定稿」P0-P3；MCP Bridge（P1）方案已三方对齐待柳柳拍板开工。
- **状态跟进**：各需求当前状态 → 驾驶舱（governance/当前项目状态.md）以需求编号引用，不在本文件复制双份。

---

## 七、GPT 通道与节点（chat2api 速查）

- **Worker 转发**：POST `https://mcp-memory.wovowx.workers.dev/api/chat2api/ask`（Body `{"message":"..."}`，token 在 Worker 环境变量）
- **Cloud Run**：`ziven-bridge-1029559493109.asia-northeast1.run.app`（服务名 ziven-bridge，端口 5005，镜像 ziven-bridge:v3；**完整运维手册见 chatroom/xray/DEPLOY.md**）
- **节点环境变量（6 个）**：VLESS_ADDR / VLESS_PORT / VLESS_UUID / VLESS_SNI / VLESS_HOST / VLESS_PATH
- **节点**：日本1 `43.153.152.106:443`（UUID 92a8cc7e-...），日本2 `43.133.191.142:443`
- **conversation_id（正式）**：`6a98cb19-3b88-83ee-a7be-314d60f0aa64`；废弃 `6a96fcf8-...`
- **铁律**：不轰炸（403 风控）；换节点需柳柳在 Google Cloud 控制台改（哥哥无 gcloud 权限）；节点同源铁律（新节点必须与柳柳浏览器 IP 同源）

---

## 八、文档索引（散档地图）
- 总览/架构/协作：00-04 · 实验/决策/协同说明：05-10 · MVP/数据模型/开发任务：11-37
- 通信层/chat.js/E2E：38-61 · Agent自动发现/治理：62-73 · 真身/需求/迁移/进度：74-82 · 最新：83
- **需求唯一真相源：本文件（00a v2）**

---

*定稿：Ziven + GPT 对齐 2026-09-04 00:18 · 待柳柳确认*
---

## 八、柳柳原始需求落点对照（v4 新增 · 可追溯）

> 收录柳柳 2026-09-07 晚（Operit 对话 19:00-20:09）亲口提出的聊天室需求，逐条落到需求编号，防丢失。

| # | 柳柳原始需求 | 落到需求 | 现状 |
|---|---|---|---|
| A1 | 工作室/聊天分流：各自 conversation_id 互不混，Agent 可跨查 | 需求 16（16.1 场景模型 + 16.2 Binding） | ⚠️ 已讨论收敛，待实现 |
| A2 | 哥哥固定工作室 ID（3682f872 线程即工作室接入 ID） | 需求 16（16.3 生命周期） | ✅ 已确认 |
| A3 | 换 ID 流程要定出来并存文档 | 需求 16（16.3 生命周期） | ⚠️ 已讨论收敛，待落文档细节 |
| A4 | 聊天室未来多对话框，每个绑的 ID 可不同（多对多） | 需求 16（16.2 Binding） | ⚠️ 已讨论收敛，待实现 |
| A5 | 项目主线生命周期（定主线→节点更新→复杂拆子文档→偏差实时更新） | 需求 15（15.1-15.4） | ⚠️ 已讨论收敛，待实现 |
| A6 | @ 注入缺失上下文（人类群聊模型，第二次@补中间对话） | 需求 13（M1.2 delta） | 🔴 当前主线，闭环未成 |
| A7 | @ UI 自动提示（QQ/微信样式，非手动文本@） | 需求 14（M1.3） | 🟡 P1 未实现 |
| A8 | 聊天框绑项目主线（可追溯） | 需求 15 + Project Binding | ⚠️ 已讨论收敛，待实现 |

**已做 vs 未做**：见驾驶舱（governance/当前项目状态.md）以需求编号引用的当前状态；本表只记「落点 + 现状」，不重复状态详情（防双源）。
