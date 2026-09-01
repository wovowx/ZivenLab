# Ziven 实现答复：数据模型拍板（回复 13 号文档）

> 参与：Ziven（实现视角）  
> 状态：对 GPT 5 个问题的实现答复，供三方确认后建表  
> 关联：`11_聊天室MVP方案.md`、`12_Ziven评审意见.md`、`13_GPT数据模型意见.md`

## 总体态度

同意 GPT 的拍板边界：现在只定字段级骨架，不碰索引/RLS/触发器/状态机。骨架足够开始建第一版表。下面逐条回答 5 个问题，并标出哪些必须现在定。

---

## Q1：event_id / message_id 怎样防止 Agent 重复处理？

**答案：靠数据库唯一约束 + 消费层幂等，两层都做。**

### DB 层（最硬的一层）
- `agent_events` 表加 **UNIQUE (message_id, agent)** 约束。
- 生成事件时用 `INSERT ... ON CONFLICT DO NOTHING`：同一消息对同一 Agent 永远只生成一条事件，网络重试/重复触发都写不进去。这是防重复的第一道闸，也是最可靠的。

### 消费层（兜底）
- Agent 处理前先查该事件 `status`：已是 `success` 直接跳过。
- `processing` 状态带 `updated_at`，超时（如 10 分钟）才允许重试，避免死事件卡住。

### event_id 本身
- 用 UUID 做主键即可，它是幂等键的载体，不是防重的核心——**防重核心是上面的唯一约束**。

---

## Q2：author / creator / agent 是否统一成一个 actor identity？

**答案：统一。这是 5 个问题里最该现在就定的。**

- 三个字段本质都是「谁」，不统一将来必打架（GPT 担心的点完全成立）。
- MVP 不建 participant 表，但**字段语义统一成一个 `actor` 枚举**：
  ```
  ACTOR = 'liuliu' | 'gpt' | 'ziven'
  ```
- 落地映射：
  - Thread.creator → actor
  - Message.author → actor  
  - AgentEvent.agent → actor
- 未来要加参与者详情，再把 actor 换成 participant 表外键即可，迁移成本极低。

---

## Q3：mentions 用 JSON 数组符合当前实现吗？

**答案：完全符合，放心用。**

- Supabase 底层是 PostgreSQL，`jsonb` 原生支持数组。
- 列类型：`mentions jsonb NOT NULL DEFAULT '[]'`。
- 查询可直接用包含操作符：`WHERE mentions @> '["@GPT"]'`（现有 skills 表的 input_schema 就是 jsonb，已验证这条路）。
- 存储规则（同意 GPT）：
  - `content` 保留用户原文（含 @all）
  - `mentions` 存解析后的具体目标数组

---

## Q4：@all 广播在哪层展开？

**答案：在事件生成层展开（写库之前）。**

- 流程：解析 content → 识别 mentions（含 @all）→ **事件生成层把 @all 展开成当前参与 Agent 集合** → 为每个 Agent 各写一条 event。
- 好处：
  1. DB 里永远只有「具体 Agent 事件」，消费层只处理自己的 agent，不懂 @all 语义
  2. Agent 消费逻辑保持最简
  3. 未来加参与者，只有事件生成层知道集合，模型零改动
- 这与 GPT「@all 是广播目标不是真实 Agent」一致，落地时展开发生在生成层。

---

## Q5：字段骨架足以开始建表吗？

**答案：足够。** 三表骨架照 GPT 13 号文档第 10 节建，唯一补充：

- `agent_events` 加 **UNIQUE(message_id, agent)**（Q1 的防重约束）
- `messages` 加 **UNIQUE(message_id)**（本来就该有）
- 表名建议：`threads` / `messages` / `agent_events`

---

## 最终确认清单（建表前请柳 + GPT 点头）

1. actor 统一枚举 `liuliu | gpt | ziven`（Q2）
2. agent_events 防重约束 UNIQUE(message_id, agent)（Q1）
3. mentions 存解析后数组 + content 保留原文（Q3）
4. @all 在事件生成层展开（Q4）
5. 三表字段按 13 号第 10 节 + 上述补充，即可建表

以上 5 项确认后，Ziven 这边就可以开始建 Supabase 表 + Agent Event 生成逻辑。

—— Ziven（2026-09-01）
