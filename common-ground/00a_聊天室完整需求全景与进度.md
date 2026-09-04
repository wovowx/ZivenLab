# 聊天室 · 完整需求全景与进度（v2 定稿）

> 整理：Ziven + GPT 对齐（2026-09-04 00:18）· 柳柳确认后执行
> **本文件是需求唯一真相源**：00-83 号散档已合并于此；任何新增需求/进度先更新本文件，再补详细分档
> 对齐过程：Ziven 整理 00a v1 → GPT 审查（#329）→ Ziven 回应保留意见（#331）→ GPT 接受折中并补充设计原则（#332）→ 定稿

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

> 需求 1-9 原始出处：76 需求全景 + 77 GPT 补漏；10-11 为 00a v2 对齐新增

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

### 🚧 进行中 / 待办
见「五、优先级定稿」P0-P3；MCP Bridge 方案已三方对齐待柳柳拍板开工。

---

## 七、GPT 通道与节点（chat2api 速查）

- **Worker 转发**：POST `https://mcp-memory.wovowx.workers.dev/api/chat2api/ask`（Body `{"message":"..."}`，token 在 Worker 环境变量）
- **Cloud Run**：`chat2api-1029559493109.asia-northeast1.run.app`（端口 5005，镜像 chat2api-xray:v1）
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