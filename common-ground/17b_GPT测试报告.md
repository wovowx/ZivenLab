# Common Ground：GPT 测试报告

> 对应任务：`common-ground/17_Ziven开发任务书.md`
> 日期：2026-09-01
> 状态：第一轮实现与数据库验证完成

## 1. 已实现

代码：`chatroom-mvp/agent_events.py`

包含：

- @GPT / @Ziven / @liuliu / @all / @沉淀 解析
- 大小写与 @ 后空白处理
- mentions 规范化并写回 `chat_messages.mentions`
- @all 展开为 GPT、Ziven 两个 Agent，不生成 liuliu Agent Event
- @沉淀只产生特殊标记，不创建普通 Agent Event
- Agent Event 使用数据库 `(message_id, agent)` 唯一约束实现幂等

测试：`chatroom-mvp/test_agent_events.py`

## 2. Parser 测试

以下用例已写入测试文件：

1. 正常 `@GPT` —— 通过
2. `@GPT @Ziven` —— 通过
3. 大小写/空白规范化 —— 通过
4. `@all` 展开为 GPT/Ziven —— 通过（liuliu 不作为 Agent）
5. 重复 mention 去重 —— 通过
6. `@liuliu` 保留为 mention，但不生成 Agent Event —— 通过
7. Agent 自己 @ 自己仍作为目标 —— 通过
8. `@沉淀` 不生成普通 Agent Event —— 通过
9. 未知 @名称忽略 —— 通过

## 3. Supabase 实际验证

已确认数据库中存在三张 MVP 表：

- `chat_threads`
- `chat_messages`
- `chat_agent_events`

实际创建了一条临时 Thread 和一条 Message，并验证：

- Message 可以写入 `chat_messages` —— 通过
- mentions 可以更新为 `[@GPT, @Ziven]` —— 通过
- GPT Agent Event 可以写入 —— 通过
- Ziven Agent Event 可以写入 —— 通过
- 对同一 `(message_id, gpt)` 再次插入时，被数据库唯一约束拒绝 —— 通过
- 测试 Thread / Message / Events 已全部清理 —— 通过

## 4. 注意事项

本轮没有直接连接真实 Agent 消费器，因此 `processing → success/failed` 的完整消费链尚未进行端到端验证。

另外，当前 `supabase_db` 的 `exec` 动作在该环境返回 `public.exec_sql` 不存在，因此数据库验证使用了其 query/insert/update/delete 能力完成，没有因此修改数据库结构。

## 5. 一个实现边界

任务书中提到 `@liuliu` 可以参与 mentions 解析，但 liuliu 是人类参与者，不是 Agent。因此：

- `@liuliu` 可以出现在 `mentions`
- 不创建 `agent='liuliu'` 的 Agent Event

`@all` 同理展开为当前 Agent 集合 `[gpt, ziven]`。

## 6. 遗留问题

- 尚未接入真实的消息触发入口（例如消息写入后的 worker/webhook）
- 尚未实现 Agent Event 消费器
- 尚未实现超时重试
- 尚未实现 @沉淀 的实际沉淀动作
- 尚未进行完整 HTTP/API 级端到端测试

这些均属于下一阶段，不影响本轮 Agent Event 生成逻辑的基本实现。

—— GPT
