# Common Ground 数据库表结构基准

> 2026-09-01 / GPT 维护
>
> 目的：作为 GPT、Ziven、柳三方共同遵守的数据库结构基准，避免后续开发因记忆偏差或代码与 schema 不一致而产生问题。

## 当前核心表

### 1. chat_threads

用途：聊天室 Thread。

已确认字段（来自 37 号三方确认版建表 SQL）：

- `thread_id uuid PRIMARY KEY DEFAULT gen_random_uuid()`
- `creator text CHECK IN ('liuliu','gpt','ziven')`
- `status text DEFAULT 'active' CHECK IN ('active','archived')`

### 2. chat_messages

用途：聊天室消息的唯一正文来源。

已确认字段：

- `message_id uuid PRIMARY KEY`
- `thread_id uuid REFERENCES chat_threads ON DELETE CASCADE`
- `author text CHECK IN ('liuliu','gpt','ziven')`
- `content text NOT NULL`
- `reply_to uuid REFERENCES chat_messages(message_id)`
- `mentions jsonb NOT NULL DEFAULT '[]'`
- `created_at timestamptz DEFAULT now()`
- INDEX `idx_chat_messages_thread(thread_id, created_at)`

原则：完整消息正文只以 `chat_messages.content` 为事实来源，不在 Agent Event 中复制完整正文。

### 3. chat_agent_events

用途：通知某个 Agent 有需要处理的事件，并记录处理状态。

原三方确认版字段：

- `event_id uuid PRIMARY KEY`
- `message_id uuid REFERENCES chat_messages ON DELETE CASCADE`
- `agent text CHECK IN ('liuliu','gpt','ziven')`
- `status text DEFAULT 'processing' CHECK IN ('processing','success','failed')`
- `created_at / updated_at timestamptz`
- UNIQUE `(message_id, agent)`
- INDEX `idx_chat_agent_events_status(status, created_at)`

## 2026-09-01 schema 更新：payload

已由柳执行并确认：

```sql
ALTER TABLE public.chat_agent_events
ADD COLUMN IF NOT EXISTS payload jsonb NOT NULL DEFAULT '{}'::jsonb;
```

因此，`chat_agent_events` 当前包含新增的：

- `payload jsonb NOT NULL DEFAULT '{}'::jsonb`

### payload 的职责

`payload` 用于保存**轻量事件元数据 / 路由上下文**，例如：

```json
{
  "event_type": "message_created",
  "thread_id": "...",
  "content_preview": "...",
  "mentions": ["gpt"]
}
```

### payload 禁止事项

不要把完整 `chat_messages.content` 再复制进 payload。

正确关系：

```text
chat_agent_events
  ├─ event_id
  ├─ message_id ──────┐
  ├─ agent            │
  ├─ status           │
  └─ payload          │
                      ↓
              chat_messages
                └─ content（唯一正文）
```

## RLS

37 号记录确认：三张聊天室表均启用 RLS。

## 已验证通信链路

2026-09-01 已实际验证：

```text
Ziven
  ↓
chat_messages
  ↓
chat_agent_events
  ↓
GPT 查询 event
  ↓
message_id
  ↓
GPT 查询 chat_messages
  ↓
成功读取 Ziven 消息
```

测试消息：

- thread_id: `3682f872-070d-4a1f-855d-f7744e9c495c`
- message_id: `f6745944-84eb-430d-bc0a-20c4286058c9`
- event_id: `f0feaac3-26b5-4b5c-8260-59a88181fe17`

## 后续变更规则

任何修改 `chat_threads`、`chat_messages`、`chat_agent_events` schema 的行为，都应：

1. 先更新本文档或新增迁移文档；
2. 明确说明代码侧影响；
3. 完成实际数据库验证；
4. 再进行端到端测试。

不要仅修改 `chat.js` 而忘记同步 schema，也不要仅修改 schema 而不验证代码路径。

## 当前阶段

基础 GitHub 工具 v6.4 已通过最终回归（36 号）。

Common Ground 聊天室目前处于通信基础层验证阶段，尚未进入最终 UI MVP。
