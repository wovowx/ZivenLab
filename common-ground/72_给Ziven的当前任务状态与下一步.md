# 给 Ziven 的当前任务状态与下一步

> 更新时间：2026-09-02
> 用途：Ziven 如果从上下文中断/忘记当前任务，优先读取本文件，再继续工作。

## 0. 先记住：我们现在在做什么

目标不是继续堆 Common Ground 功能，而是把 **GPT 从“只能在 ChatGPT App 里被动回复”逐步变成一个可后台运行、能自主调用工具干活的 Agent Runtime**。

当前采用“小实验逐层验证”，不允许把未实测的兼容性当成 PASS。

---

## 1. 已经 PASS 的东西

### Common Ground 通信层

- Agent 间 `chat_send → event → pending → read → ack` 已经跑通。
- Phase 1 atomic claim 已 PASS。
- Test A：Ziven 自动发现 GPT 事件、claim、read、reply、ack 已 PASS。

### 真实触发链 PoC

**已正式 PASS，且不是 dry-run：**

```text
GPT chat_send
  → chat_agent_events INSERT
  → Supabase Database Webhook
  → Cloudflare Worker
  → webhook audit
```

本次真实验证：

- GPT 消息：`b2b038e7`，内容「真实触发测试」
- Supabase event：`615575cb`
- Webhook：真实 delivered
- INSERT → Webhook delivered：不到 1 秒
- 审计表 `chat_webhook_audit` 有真实记录

所以：**INSERT → Webhook → Worker 这一层现在不用再反复证明。**

详细记录见：
`common-ground/70_触发链PoC_PASS_INSERT事件到Webhook到Worker.md`

---

## 2. 当前真正的下一步

### 第一优先级：模型链 PoC

验证：

```text
Agent Runtime
  → Chat2API
  → 模型
  → 返回结果
```

需要实际验证，而不是根据“OpenAI-compatible”字样推断：

1. 最小 `/v1/chat/completions` 调用是否成功
2. session / 上下文是否能正常工作
3. 认证与 token refresh 是否可靠
4. timeout / error 时 Runtime 如何处理
5. **最重要：自定义 tools / function calling 是否真的兼容**

如果使用 `lanqian528/chat2api`，不要忘记之前已经确认：它本身不是 Cloudflare Worker 原生运行时应用；如果走 Cloudflare，需要单独确认 Containers 等实际部署方式，不要把“Cloudflare 能跑 Docker”直接等同于“这个项目已经验证可部署”。

### 第二优先级：tool-call round-trip PoC

模型链通过后，先不要接全部 MCP。

只选一个**无副作用**工具验证：

```text
模型决定调用 tool
  → Runtime 解析 tool call
  → Tool Executor 执行 MCP
  → 工具结果回传模型
  → 模型继续判断
  → 最终回复
```

这个实验如果 PASS，才能说“后台 GPT Agent 已经具备最基本的自主工具调用能力”。

### 第三优先级：接入 Common Ground

最后再组合成：

```text
Common Ground
  → Agent Runtime
  → Chat2API / Model
       ↕
  Tool Executor / MCP
  → Common Ground
```

目标是最终形成：

```text
收到事件
→ claim
→ read
→ 模型判断
→ 必要时调用 MCP 工具
→ 得到工具结果
→ 模型继续判断
→ chat_send
→ ack
```

并且全过程不需要柳柳拿手机手动转发。

---

## 3. 重要架构判断

不要把下面三个东西混成一个概念：

- **Chat2API：** 模型接口/模型适配层
- **Agent Runtime：** 后台运行的 Agent 身体，负责循环、状态、tool call、错误处理
- **MCP：** 工具执行层，是 Agent 的“手脚”

ChatGPT App 里 GPT 能调用的 MCP，**不会因为 Chat2API 接上 GPT 模型就自动继承到后台 Runtime**。

Runtime 必须自己拥有/获取工具 schema，并实现 tool-call → MCP execution → tool result → model continuation 的闭环。

---

## 4. 现在不要做的事

1. 不要因为 Webhook PASS 就直接宣布整个 Agent Runtime PASS。
2. 不要一次接几十个 MCP 工具。
3. 不要先做复杂 Queue / Durable Object；先看最小 PoC 是否真的需要。
4. 不要凭记忆判断 Chat2API、Cloudflare Containers、Supabase tier 等兼容性；涉及部署/费用/平台能力必须实测或查官方资料。
5. 不要为了“看起来完整”先写大量文档，而不做最小实验。
6. 不要擅自修改生产/主分支。按现有 GitHub 运维规则走 `dev → review → main`。

---

## 5. 关于今天的治理问题

`common-ground/71_治理问题清单_2026-09-02.md` 记录了另外一条治理线：

- P0：版本号 + CHANGELOG 的 main 部署硬校验
- P1：help/skill 目前属于软约束
- P2：新工具失败后容易绕回老路
- P3：A/B/C 三种治理方案待讨论

**这条治理线不要抢在当前 Agent Runtime PoC 前面自行开工。**
除非 GPT / 柳柳明确决定，否则先保持暂停。

---

## 6. 我们现在的验收顺序

```text
[已 PASS]
Common Ground 基础通信
        ↓
[已 PASS]
Atomic Claim
        ↓
[已 PASS]
Test A：Ziven 自动发现闭环
        ↓
[已 PASS]
真实 INSERT → Webhook → Worker
        ↓
[现在做]
Chat2API 模型链 PoC
        ↓
[下一步]
tool-call round-trip PoC
        ↓
[最终组合]
Common Ground → Runtime → Model ↔ MCP → Common Ground
        ↓
Full Test B
```

**当前任务只有一句话：先把模型链实测出来。**

如果模型链还没 PASS，就不要跳到 Full Test B。

---

## 7. 给 Ziven 的协作要求

你如果重新进入这个项目、发现自己忘了上下文：

1. 先读本文件；
2. 再读 70 号验证记录；
3. 再读 71 号治理清单；
4. 在 Common Ground @gpt 报告你准备验证的最小实验；
5. GPT 审议后再动手；
6. 实测结果与理论判断分开写；
7. PASS 必须有真实证据，不用“应该可以”。

**不要让柳柳再次充当我们两个 Agent 之间的人工消息中转站。Common Ground 就是我们的协作通道。**
