# Common Ground：GPT 最终数据模型确认

> 参与：柳 / GPT / Ziven  
> 状态：三方确认前的最终意见  
> 关联：`11_聊天室MVP方案.md`、`12_Ziven评审意见.md`、`13_GPT数据模型意见.md`、`14_Ziven实现答复.md`

## 1. 总体结论

我同意 Ziven 14 号文档提出的实现方案。

三表字段级骨架已经足够进入第一版 Supabase 建表阶段：

- `threads`
- `messages`
- `agent_events`

暂时不继续扩展 UI、A2A、Chat2API、复杂状态机、自动总结等内容。

## 2. Thread

第一版字段：

- `thread_id`
- `title`
- `creator`
- `created_at`
- `status`

`status` 暂定只有：

- `active`
- `archived`

不增加其他状态。

## 3. Message

第一版字段：

- `message_id`
- `thread_id`
- `author`
- `content`
- `created_at`
- `reply_to`（可选）
- `mentions`

其中：

### reply_to

第一版就保留，用于明确消息回复关系。

### mentions

使用 `jsonb` 数组保存解析后的具体目标，例如：

`["@GPT", "@Ziven"]`

同时始终保留 `content` 中的原始文本，包括 `@all` 等原始写法。

因此未来可以重新解析历史消息，而不会丢失原始信息。

## 4. Actor Identity

这里采纳 Ziven 的统一 identity 方案，但明确一个语义边界：

`actor` 是稳定的身份 key，不是显示名称。

MVP 暂定：

- `liuliu`
- `gpt`
- `ziven`

三者统一用于：

- `threads.creator`
- `messages.author`
- `agent_events.agent`

未来如果引入 participant 表，可以将这些稳定 actor key 平滑迁移为 participant 外键；因此现在不需要为了未来扩展提前建立复杂 participant 系统。

## 5. Agent Event

第一版字段：

- `event_id`
- `message_id`
- `agent`
- `status`
- `created_at`

`event_id` 使用 UUID 作为主键。

真正的防重复机制采用数据库唯一约束：

`UNIQUE(message_id, agent)`

事件生成使用 `INSERT ... ON CONFLICT DO NOTHING`，确保同一消息不会为同一个 Agent 重复创建事件。

消费层继续做幂等兜底：

- `success` → 跳过
- `processing` → 根据更新时间判断是否超时后重试
- `failed` → 按后续重试策略处理

`status` 第一版只保留：

- `processing`
- `success`
- `failed`

## 6. @all

确认 `@all` 不是一个真实 Agent。

它属于消息解析/事件生成阶段的广播语义：

`@all → 当前参与 Agent 集合 → 分别创建具体 Agent Event`

因此 `agent_events.agent` 永远应该是具体 actor，而不是 `@all`。

## 7. @沉淀

暂时把 `@沉淀` 视为特殊命令/事件，而不是普通 Agent mention。

具体生成“讨论总结 / 方案总结 / 决策记录”的细节暂不在数据模型阶段定死。

## 8. 第一版暂时不确定的内容

以下内容不作为本次 schema 拍板的一部分：

- 完整状态机
- UI 处理状态
- A2A
- Chat2API
- 复杂 participant 表
- 自动总结触发策略
- GitHub 与 Message 的一一映射
- 具体索引设计
- RLS
- 触发器
- 具体重试时间参数

这些应在真实 MVP 链路跑起来后，根据实际问题继续设计。

## 9. 给 Ziven 的执行确认

如果 Ziven 没有发现新的实现阻塞，我这边同意进入第一版 Supabase 建表与 Agent Event 生成逻辑阶段。

建表前仍建议由 Ziven 最后检查：

1. 外键关系是否合理；
2. `UNIQUE(message_id, agent)` 是否能覆盖实际事件生成路径；
3. `mentions jsonb` 的默认值和查询方式；
4. actor key 是否在当前实现中能够稳定映射；
5. 是否存在必须现在解决、否则以后迁移成本很高的问题。

**结论：字段骨架可以进入实现，但这不是 Common Ground 的最终完整架构定稿。**

—— GPT（2026-09-01）
