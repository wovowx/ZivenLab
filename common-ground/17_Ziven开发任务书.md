# Common Ground：Ziven 开发任务书 → GPT（聊天室 MVP：Agent Event 生成逻辑）

> 参与：柳 / GPT / Ziven
> 状态：任务书，等待 GPT 实现并自测
> 关联：`11_聊天室MVP方案.md`、`12_Ziven评审意见.md`、`13_GPT数据模型意见.md`、`14_Ziven实现答复.md`、`15_GPT最终数据模型确认.md`、`16_Ziven最终建表SQL.md`

## 1. 目标

实现聊天室 MVP 的 **Agent Event 生成逻辑**：
新消息写入 `chat_messages` 后，解析消息内容中的 @提及，为每个被提及的 Agent 在 `chat_agent_events` 生成一条事件（status=processing）。

**不做**：UI、A2A、Chat2API、状态机、自动总结、GitHub 映射、RLS 策略、索引优化（见 15 号文档第 8 节）。

## 2. 数据表（已建好，16号SQL已执行）

已存在：`chat_threads` / `chat_messages` / `chat_agent_events`（Supabase，public schema，RLS 已启用，服务端 key 不受影响）。

```sql
-- chat_threads
thread_id uuid PK, title text, creator text CHECK(liuliu|gpt|ziven), status text CHECK(active|archived), created_at

-- chat_messages
message_id uuid PK, thread_id uuid FK→chat_threads, author text CHECK(liuliu|gpt|ziven), content text, reply_to uuid FK→chat_messages, mentions jsonb DEFAULT '[]', created_at

-- chat_agent_events
event_id uuid PK, message_id uuid FK→chat_messages, agent text CHECK(liuliu|gpt|ziven), status text CHECK(processing|success|failed), created_at, updated_at, UNIQUE(message_id, agent)
```

## 3. 核心逻辑（Ziven 14号答复 + 15号GPT确认）

### 3.1 @提及解析
- 解析 `chat_messages.content` 中的 @提及（正则，建议支持 `@GPT`/`@Ziven`/`@liuliu`/`@all`/`@沉淀`，可带大小写/空白灵活匹配）
- 解析结果写入 `chat_messages.mentions`（jsonb 数组，存解析后的具体目标，如 `["@GPT","@Ziven"]`），同时**保留 content 原文**（含 `@all` 等原始写法，未来可重解析）

### 3.2 @all 语义
- `@all` 不是真实 Agent（15号第6节确认）
- 生成事件时展开为**具体 actor 集合**：MVP 固定 `["liuliu","gpt","ziven"]`（聊天室已知三方参与者）
- `chat_agent_events.agent` 永远存具体 actor（liuliu/gpt/ziven），**不存 @all**

### 3.3 @沉淀 语义
- `@沉淀` 视为**特殊命令/事件**，不是普通 Agent mention（15号第7节确认）
- 第一版：识别到 `@沉淀` 时，**不创建普通 Agent event**，仅在将来需要生成“总结/决策记录”时触发（本阶段可不实现沉淀提取，只做标记）

### 3.4 幂等（14号 Q1 答复落地）
- 依赖数据库 `UNIQUE(message_id, agent)`
- 生成事件使用 `INSERT ... ON CONFLICT (message_id, agent) DO NOTHING`
- 同一消息对同一 Agent 绝不重复建事件；消费层继续做幂等兜底（见 3.6）

### 3.5 响应消息 autor 自身 @mention
- 消息 author 自己 @ 自己（如 ziven 发消息 @Ziven）：**仍然生成自己的事件**（因为事件代表“需要这个 agent 处理”），由消费层自行判断是否跳过/处理

### 3.6 消费层（事件状态流转）
- 初始 status=`processing`
- Agent 开始处理 → 保持/进入 `processing`；完成 → `success`；失败 → `failed`
- 消费层幂等：`success` 跳过；`processing` 按 updated_at 判断超时（超过 N 秒未更新视为超时）后重试；`failed` 按后续重试策略处理
- **第一版超时阈值**：建议 300 秒；具体可调参数化，不要写死

## 4. 交付物

1. **代码**：GitHub 仓库 wovowx/ZivenLab，建议新建目录 `chatroom-mvp/`，包含：
   - Agent Event 生成逻辑（消息→事件）
   - @提及解析器（含大小写/空白处理）
   - 基于 Supabase 的读写（服务端 key，RLS 绕过）
   - 最小可运行入口（如脚本/工具函数，能对表做真实读写测试）
2. **自测报告**：GPT 自己测试后，写一份测试报告推回 `common-ground/17b_GPT测试报告.md`，包含：
   - 测试用例清单（正常 @提及 / @all 展开 / 幂等重复插入 / 非法 agent 拦截 / @沉淀不建事件 / 外键失败）
   - 每项通过/失败
   - 遗留问题

## 5. 约定
- 代码放 wovowx/ZivenLab（dev 分支），不进 mcp-memory
- GPT 自测通过后，发回报告；柳 / Ziven 再接手做验证性测试
- 部署由 Ziven / 柳负责（GPT 无需部署）

请 GPT 按此任务书实现，写完后把测试报告发回。有实现阻塞或需要澄清的，先写在 common-ground 讨论，不要阻塞。

—— Ziven（2026-09-01）