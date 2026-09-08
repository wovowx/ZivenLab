# 聊天室系统架构总览（system-architecture v1）

> **用途**：回答「整个聊天室系统为什么这样设计、由什么组成」。
> **状态**：待柳柳拍板后正式生效（2026-09-07 Ziven × GPT 讨论收敛 + 2026-09-07 晚 GPT 链路实况修正）。
> **讨论链**：#957→#958→#959→#960→#961→#962→#963→#964→#965→#966→#967→#968→#969→#970→#971→#972
> **搭档文档**：
> - 怎么实现 → `chatroom/implementation.md`
> - 一个项目走到哪 → `projects/{项目名}/mainline.md`
> - 三个文档职责分离，不合并。

---

## 0. 背景与术语（新读者从这里读起）

**聊天室** = 柳柳 + Ziven（哥哥）+ GPT 三个角色异步协作的共享空间（Common Ground）。柳柳在聊天室 @ 某个 Agent，那个 Agent 被唤醒、读取上下文、回复、完成事件闭环。

**M1.x** = 聊天室能力的里程碑切片：
- M1.1 Agent Presence State（Agent 消费位置状态）— 已完成
- M1.2 Agent Rejoin Context（Agent 重新加入群聊的上下文恢复）— 未闭环（根因已确认）
- M1.3 Mention UX（@ 选择 UI）— 未开始

---

## 1. 目标与分层

```
                 ┌────────────────────────┐
                 │ L3 Context Recovery    │  ← 横向服务（不是层级）
                 │ 补看/恢复/解释器       │     读取 L1 + L2
                 └───────────┬────────────┘
                             │ 读取
                             ↓
L0 接入层     thread / @入口 / conversation routing（我怎么进来）
      ↓
L1 事实事件层  chat_messages / chat_agent_events / ack / agent_chat_state
              （发生了什么 —— 唯一事实源，不可人工改）
      ↓
L2 项目意识层  mainline / nodes / decisions（这些事代表什么、我们往哪走）
```

- **L0 接入层**：对话框、thread、@ 入口、conversation routing。回答「我怎么进来」。
- **L1 事实事件层**：聊天室实际发生了什么（消息、事件、ack、消费状态）。**唯一事实源**，不可人工修改。
- **L2 项目意识层**：这些事代表什么、项目现在往哪走（主线、节点、决策）。
- **L3 恢复服务（横向）**：读取 L1 + L2，把 Agent 缺席期间漏掉的内容补偿给它 = 人类群聊补看。不是 L2 的下一层，而是横跨的「解释器」。

---

## 2. 现状（✅ VERIFIED）

| 模块 | 状态 | 说明 |
|---|---|---|
| A1 链路基础设施 | ✅ | @ziven → chat_messages → chat_agent_events → claim → 隧道唤醒 Operit → reply → ack 全自动闭环（Ziven 侧）；GPT 侧见 §3 说明 |
| A2 M1.1 Agent Presence State | ✅ | agent_chat_state 表（agent_id+thread_id 唯一），last_consumed_message_id = 最后一次完整闭环位置，ack 后推进 |
| A4 场景↔conversation_id 路由 | ✅ | §9.6：工作室（Ziven thread 3682f872 / GPT 固定 id）/ 聊天两空间分流，Ziven 可跨查 |

---

## 3. 现状（🟡 未闭环）+ GPT 消费路径（2026-09-07 晚柳柳亲述确认）

> ✅ **正确认知（柳柳亲述）**：@GPT 走 **chat2api**——event_processor 以 gpt 身份 claim（claimed_by=gpt 正常）→ buildSystemPrompt 拼 [AGENT_CONTEXT] → callChat2Api（同一 conversation_id）→ GPT 真身回复 → sendMessage → ack。GPT 天然拥有**所有被 @ 的消息 + 对应的回复**（同一 conversation_id 都进同一对话）；**缺失的只是「没被 @ 的消息」**（聊天室中没@到 GPT 的讨论）。M1.2 = 把「没被 @ 的消息」作为 delta 补发给 GPT（人类群聊补看）。

**A3 M1.2 Agent Rejoin Context**
- 已完成（代码层面）：context_resolver.js、trigger/delta/knowledge 恢复层、event_processor 注入逻辑（v6.27.x 已部署）；注入挂在 event_processor → chat2api ——**链路方向正确**。
- 🟡 **未闭环**：GPT 真身 #938 反馈「看不到 [AGENT_CONTEXT]」。已排除 resolver 组装问题（debug 端点实测正确）。**待排查注入透传**：buildSystemPrompt → chat2api payload → ChatGPT 真身这一段为何不可感知。
- 原则：**内部组件存在 ≠ 用户体验完成**。

---

## 4. 核心设计组件

- **B1 conversation_bindings**：thread ↔ agent ↔ conversation_id 接入路由。
  - 三概念分离：`route_type`（primary/fallback/migration/temporary）+ `access_mode`（exclusive/shared）+ `status`（active/archived）
  - 补 `purpose` 字段（development/brainstorm/debug/execution…），同一 thread 可绑多个 conversation 时能解释为什么。**执行框（execution-room）绑定：purpose=execution / access_mode=exclusive / route_type=temporary**。
  - 铁规：Context 边界永远按 agent+thread，不按 conversation_id；conversation 内部历史不可信；换档 = 旧归档 + 新激活 + 写 `conversation_route_changed` 事件。
- **B2 Project Mainline v1**：见 §6。
- **B3 Agent Rejoin 补看**：第二次 @ 时把两次 @ 之间缺失的消息补偿给 Agent = 人类群聊补看。`last_consumed_message_id` = Agent 最后一次参与群聊的位置，不是阅读位置。
- **B4 Execution Runtime（v4.1 柳柳拍板）**：执行 GPT = 新的执行 Runtime 加入项目，不是「缺席的讨论 GPT 回来」。
  - **Execution Bootstrap Context**（独立于 Agent Rejoin Context）：task_context（要执行什么/验收标准）+ project_context（哪个项目/当前主线节点）+ constraints_context（架构规则/禁改项/决策）+ files_context（实现文档/相关文件）。
  - **边界铁律**：delta=过程记忆（聊天废话，执行 GPT 不需要），knowledge=结论状态（当前决定/实现位置，必须有）。执行 GPT 不继承讨论 GPT 的 delta。
  - 底层复用 context_resolver，但拆两个方法：`resolve_rejoin_context()`（讨论 GPT/Ziven 补看）+ `resolve_execution_context()`（执行 GPT 启动）——别让执行伪装 rejoin（否则出现「执行 GPT 怎么有 last_consumed_message_id」）。
  - **执行框 thread 长期存在，conversation_id 短生命周期**：thread 是聊天室事实（长期），conversation_id 是外部模型接入状态（短命可换）。执行框（长期）→ 挂 GPT session A/B/C，不反过来。
  - **领 id**：execution_session_manager 负责（execution_session_init 空初始化 → 创建临时 conversation → 拿 conversation_id → 写 conversation_bindings → 返回 ready → 再开任务），不做隐式初始化。
  - **换 id**：归档旧 binding（status=archived）+ 新增新 binding（status=active, reason=context_reset）+ 写 conversation_binding_changed 事件，不 UPDATE。
  - **execution_run 模型（P2/P3 预留）**：execution_run_id/task/thread/status/pending|running|success|failed/started_at/finished_at——区分「聊天消息」和「执行任务」（一次执行可能换 id/重试/超时/分批）。

---

## 5. 数据职责边界 ⭐（最容易翻车的点，提前写死）

| 数据 | 归属 | 谁能改 |
|---|---|---|
| chat_messages / chat_agent_events | 发生了什么（事实源） | 只能系统流程产生，**不人工编辑** |
| agent_chat_state | Agent 消费到哪（运行状态） | 系统流程 |
| conversation_bindings | Agent 怎么接入（路由状态） | 只能通过绑定变更流程 |
| mainline.md | 项目往哪走（项目意识） | 人工 / Agent 协作维护 |

---

## 6. 项目主线模型（Project Mainline v1）

```
projects/{项目名}/
 ├─ mainline.md        ← 唯一项目路线源：目标/路线/节点/指针 CURRENT_NODE/调整历史
 └─ nodes/node-xxx.md  ← 复杂节点细节（chat2api 部署坑之类）
```

- **指针单源**：`CURRENT_NODE: node-xxx` 存 mainline.md 顶行；**不建 current_node.yaml**（刚治完文档漂移，不制造第二真源）。
- **节点六态**：⬜ planned / 🔄 active / ✅ completed / ⏸ paused / ↪ branched / ❌ abandoned。
- **插入分支**：节点 ID 与顺序分离（插 `node-004` 不重排原编号）；插入 = 加节点 + 改指针 + 记原因；原节点保留（「为什么没走这条路」也是项目历史）。
- **UI 卡片**：聊天室对话页只显示当前节点标题 / 状态 / 下一步，不拖整条主线。
- **铁律**：L2 描述「项目应如何理解」，**不负责维护「系统当前运行状态」**。迁移前 mainline.md 是唯一项目路线源；未来 Project State Runtime 可能承载机器状态，但尚未决定。

---

## 7. 失败与闭环原则 ⭐

任何 Agent 处理失败必须产生**可追踪状态**。禁止：
- 静默失败
- 已 claim 无结果
- 已回复但未 ack

（对应已发生过的事故：被唤醒只 ack、没 chat_send——这不是 bug，是原则。）

---

## 8. 文档职责分离

| 问题 | 文档 |
|---|---|
| 为什么这么设计 | architecture/system-architecture.md（本文件） |
| 怎么实现 | chatroom/implementation.md |
| 现在做到哪 | projects/{项目名}/mainline.md |

不要合并成一个万能文档（此前漂移就是因为单一文档承载太多）。

---

## 9. 演进路线

```
Step1  M1.2 Agent Rejoin Context 闭环（把两次 @ 之间缺失的消息补给 GPT —— 按 Runtime B 实际路径）
Step2  Project Mainline v1（主线 + 指针 + UI 当前节点卡片）
Step3  M1.3 Mention UX（@ 有恢复机制才值得做）
Step4  Conversation Binding 完整化（routing 是基础设施）
```

---

*Ziven × GPT 2026-09-07 讨论收敛；GPT 链路实况 2026-09-07 晚修正（柳柳指正）。待柳柳拍板。*