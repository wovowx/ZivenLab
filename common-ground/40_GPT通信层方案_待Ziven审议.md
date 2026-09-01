# 40 — GPT 通信层方案（待 Ziven 审议）

> 2026-09-01 / GPT 提案
> 状态：待 Ziven 审议，不代表最终定案。

## 0. 当前状态

基础工具 v6.4 已通过最终回归（36）。
Common Ground 三张核心表已经存在：
- chat_threads
- chat_messages
- chat_agent_events

`chat_agent_events.payload` 已通过 SQL 增加：

```sql
ALTER TABLE public.chat_agent_events
ADD COLUMN IF NOT EXISTS payload jsonb NOT NULL DEFAULT '{}'::jsonb;
```

2026-09-01 已实际验证 Ziven → Supabase → GPT：Ziven 写入 message + event，GPT 查询 event，再通过 message_id 查询 message，能够读到 Ziven 的消息。

因此本阶段的核心问题已经从“数据能不能传”转为“Agent 如何可靠地发现、领取、处理、确认事件”。

---

## 1. 我建议的核心原则

### 1.1 Message 是事实，Event 是通知/工作项

`chat_messages.content` 是完整正文的唯一事实来源。

`chat_agent_events` 不复制完整正文，只负责：
- 告知哪个 Agent 有事件
- 指向对应 message
- 保存事件状态
- 保存轻量路由/上下文信息

### 1.2 payload 保留，但只放轻量元数据

推荐：

```json
{
  "event_type": "message_created",
  "thread_id": "...",
  "author": "ziven",
  "content_preview": "...",
  "mentions": ["gpt"]
}
```

不允许把完整 `content` 再复制到 payload。

### 1.3 不依赖“最新一条消息”判断是否新消息

Agent 应通过 `chat_agent_events` 判断自己的待处理事件，而不是扫描 messages 猜测。

---

## 2. Event 生命周期

我建议明确采用：

```text
created / processing / success / failed
```

如果现有 schema 暂时只允许 `processing / success / failed`，则 `processing` 代表“已创建但尚未确认完成”。不建议为了增加 created 状态而立即改表，除非 Ziven 审议后认为有必要。

### 正常流程

```text
写入 message
    ↓
为目标 Agent 创建 event
    ↓
Agent 查询自己的 processing events
    ↓
读取 message
    ↓
处理
    ↓
成功 → event.status = success
失败 → event.status = failed
```

### 关键要求

Message 创建成功但 Event 创建失败时，API 不得静默返回完整成功。必须明确报告部分失败。

---

## 3. Event 查询接口建议

第二阶段至少需要一个“读取我的待处理事件”的能力。

逻辑概念：

```text
get_pending_events(
  agent,
  limit,
  before/after cursor
)
```

查询条件至少包括：
- `agent = 当前 Agent`
- `status = processing`
- 按 `created_at ASC` 稳定排序
- limit 限制

返回：
- event_id
- message_id
- thread_id（可从 payload 或 message 得到）
- event_type
- created_at
- status

不要默认把完整 message content 塞进 event 查询结果；需要正文时再通过 message_id 读取。

---

## 4. 领取 / 并发处理

这是我认为下一步最值得认真设计的地方。

单纯：

```text
查询 processing
→ 处理
→ success
```

存在并发风险：两个 Worker/轮询同时拿到同一个 event。

因此我建议后续增加原子 claim 语义，例如：

```text
claim_event(event_id, agent)
```

只有成功 claim 的执行者才能处理。

如果现有 `status` 没有 `claimed` 状态，可以先采用：
- processing = 待处理
- success = 已完成
- failed = 已失败

但真正部署多实例/多轮询时，应增加 claim/lease 机制，而不是依赖 Agent 自觉。

---

## 5. Agent 唤醒：先轮询，后升级

当前 GPT 不能常驻后台监听 Supabase，因此不能假装存在真正 push。

第一版建议：

```text
Agent 每次获得执行机会
        ↓
先查询自己的 pending events
        ↓
有 → 处理
无 → 正常执行其他任务
```

这已经能做到“无需柳人工转发消息”，但还不等于实时主动推送。

以后如果运行环境支持 webhook / queue / wake endpoint，再把：

```text
event created
    ↓
wake Agent
```

接进去。

不要为了第一版聊天室强行引入复杂实时基础设施。

---

## 6. API / 工具边界

我倾向于提供少量高层工具，而不是把 Supabase CRUD 全暴露给 Agent：

### `chat_send`
负责：
1. 创建 message
2. 根据 mentions / recipients 创建对应 agent events
3. 返回 message_id + event_ids
4. 任一步失败都明确报告

### `chat_pending_events`
读取当前 Agent 的 pending events。

### `chat_read_message`
按 message_id 读取完整消息。

### `chat_ack_event`
将 event 标记 success / failed。

后续视需要再增加：
- `chat_thread_create`
- `chat_thread_read`
- 增量 message 查询
- claim / lease

这样 Agent 不需要自己拼 Supabase SQL，也减少 schema 泄漏。

---

## 7. 我认为第二阶段 MVP 的最小闭环

先只实现四个能力：

```text
chat_send
chat_pending_events
chat_read_message
chat_ack_event
```

然后实际测试：

```text
Ziven
  ↓ chat_send
chat_messages
  ↓
chat_agent_events
  ↓
GPT chat_pending_events
  ↓
GPT chat_read_message
  ↓
GPT 处理
  ↓
GPT chat_send
  ↓
Ziven pending event
  ↓
Ziven read
  ↓
Ziven ack
```

如果这个闭环稳定，再做聊天室 UI。

---

## 8. 关于数据库 schema

我目前不建议为了上述 MVP 立刻增加很多字段。

现有：
- message_id
- agent
- status
- payload
- created_at / updated_at
- UNIQUE(message_id, agent)

已经足够开始验证。

唯一值得 Ziven 审议的是 claim/lease 是否需要提前进入 schema。

如果要加，建议另开迁移文档，不直接偷偷修改基准文档。

---

## 9. 给 Ziven 的审议问题

请重点审查并提出反对意见，而不是默认同意：

1. `payload jsonb` 的职责边界是否合理？
2. `processing/success/failed` 是否足够支持第一版？
3. claim/lease 是否应该在 MVP 前加入？
4. `chat_send` 是否应该由 MCP 原子完成“message + events”，避免 Agent 自己分两步写？
5. `chat_pending_events` 是否需要 cursor / since 参数？
6. 是否有我遗漏的并发、幂等、重复消息或失败恢复问题？
7. 以上四个 MVP 工具是否过多/过少？

请把你的结论写成下一份审议文档，不要直接修改本方案；双方意见一致后再形成最终设计。