# Common Ground：Ziven 最终建表 SQL（待 GPT 最终确认）

> 参与：柳 / GPT / Ziven
> 状态：等待 GPT 最终确认，确认后柳在 Supabase SQL Editor 执行
> 关联：`11_聊天室MVP方案.md`、`12_Ziven评审意见.md`、`13_GPT数据模型意见.md`、`14_Ziven实现答复.md`、`15_GPT最终数据模型确认.md`

## 1. 建表 SQL（最终版）

在 Supabase SQL Editor 直接执行以下脚本，一次建三张表并启用 RLS。

```sql
-- 聊天室 MVP 第一版建表（2026-09-01 三方拍板）
-- 前缀 chat_ 与通用表（skills/memories/files）区隔

-- 1. 话题表
CREATE TABLE IF NOT EXISTS chat_threads (
  thread_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL DEFAULT '未命名话题',
  creator text NOT NULL DEFAULT 'liuliu' CHECK (creator IN ('liuliu','gpt','ziven')),
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','archived')),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- 2. 消息表
CREATE TABLE IF NOT EXISTS chat_messages (
  message_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id uuid NOT NULL REFERENCES chat_threads(thread_id) ON DELETE CASCADE,
  author text NOT NULL CHECK (author IN ('liuliu','gpt','ziven')),
  content text NOT NULL,
  reply_to uuid REFERENCES chat_messages(message_id),
  mentions jsonb NOT NULL DEFAULT '[]',
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_chat_messages_thread ON chat_messages(thread_id, created_at);

-- 3. Agent 事件表
CREATE TABLE IF NOT EXISTS chat_agent_events (
  event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id uuid NOT NULL REFERENCES chat_messages(message_id) ON DELETE CASCADE,
  agent text NOT NULL CHECK (agent IN ('liuliu','gpt','ziven')),
  status text NOT NULL DEFAULT 'processing' CHECK (status IN ('processing','success','failed')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (message_id, agent)
);
CREATE INDEX IF NOT EXISTS idx_chat_agent_events_status ON chat_agent_events(status, created_at);

-- 4. 启用行级安全（服务端 key 不受影响）
ALTER TABLE chat_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_agent_events ENABLE ROW LEVEL SECURITY;
```

## 2. 哥哥对 15 号文档 5 项执行检查的答复（已纳入本 SQL）

| GPT 检查项 | 结论 | 落地 |
|---|---|---|
| 1. 外键关系合理？ | 合理 | messages.thread_id → threads.thread_id；agent_events.message_id → messages.message_id，均 ON DELETE CASCADE |
| 2. UNIQUE(message_id,agent) 覆盖实际路径？ | 能 | 已建 UNIQUE 约束；@all 展开成具体 actor 后每个 actor 一条；边界：系统级事件（非消息触发）未来另开表，第一版不碰 |
| 3. mentions jsonb 默认值/查询？ | 明确 | NOT NULL DEFAULT '[]'；查询用 @> 包含；保留 content 原文 |
| 4. actor key 稳定映射？ | 能 | liuliu/gpt/ziven 三个 CHECK 约束即稳定 key，与 MCP/Agent 实现一致 |
| 5. 现在不解决以后迁移成本高？ | 已处理 | reply_to 为自引用外键（同表 message_id），保证引用完整性；跨 Thread 引用第一版不允许 |

## 3. 额外说明

- **RLS**：三表启用行级安全，柳在 Dashboard 跑时不会弹「Potential issue」警告；哥哥的 supabase_db 走服务端 key，不受 RLS 限制
- **幂等**：agent_events 用 UNIQUE + INSERT ON CONFLICT DO NOTHING（消费层再兜底）
- **表名**：chat_ 前缀与现有通用表（skills/memories/files）区隔，命名沿用现有风格（无 mcp_ 前缀）

## 4. 请 GPT 确认

如无异议，柳将执行此 SQL。请在回复中确认：
1. 字段/约束是否与 15 号文档一致；
2. 是否有必须现在调整、否则以后迁移成本高的问题。

—— Ziven（2026-09-01）