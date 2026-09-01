# Common Ground：GPT 对数据模型的意见

状态：三方继续讨论，尚未定稿
参与：柳 / GPT / Ziven
关联：11_聊天室MVP方案.md、12_Ziven评审意见.md

## 1. 总体判断

我基本同意 Ziven 的评审：Thread + Message + 最小 Agent Event 是 MVP 最合适的骨架。

当前我建议真正拍板的是“字段级骨架”，而不是一次性把数据库类型、索引、RLS、触发器、状态机全部定死。

原则：低成本、可迁移、能保证事件链路不重复执行。

## 2. Thread：第一版建议

保留：

- thread_id
- title
- creator
- created_at
- status

status 第一版只需要：

- active
- archived

不建议现在加入 closed / waiting / processing / summarized / locked / deleted 等状态。

## 3. Message：第一版建议

保留：

- message_id
- thread_id
- author
- content
- created_at
- reply_to（可选）
- mentions（可选）

### reply_to

第一版就保留。字段成本很低，但以后补会涉及历史数据迁移。

### mentions

建议保存“解析后的 Agent 目标列表”，使用 JSON 数组，例如：

["@GPT", "@Ziven"]

不要把 mentions 做成模糊字符串匹配。

解析规则可以是：先精确匹配 Agent，再处理 @all。

但不要因此丢掉原始 content。content 始终保留用户实际发送的原文，这样未来即使 mention 解析规则改变，也可以重新解析历史消息。

## 4. Agent Event：这里需要特别注意

我同意第一版需要最小 Agent Event，但我不认为现在最重要的是把状态机做得很完整。

更重要的是保证事件身份与幂等性，避免同一条消息因为网络重试等原因导致 Agent 重复回复。

建议第一版至少有：

- event_id
- message_id
- agent
- status
- created_at

其中 event_id / message_id 的关系需要保证能够识别“这是哪一次 Agent 处理事件”。

status 可以先保持最小集合：

- processing
- success
- failed

但状态字段不是 MVP 最核心的复杂度来源，暂时不要继续扩展状态机。

## 5. 一个需要三方继续确认的问题：Identity

目前 author / creator / agent 到底是：

- 字符串/枚举
- 独立 participant identity
- 还是统一的 actor identity

我建议暂时不要马上定成复杂 participant 表，但需要保证未来可以区分：

- 柳
- GPT
- Ziven

并且 author 与 agent 不应该因为实现方便而变成互相不兼容的两套身份体系。

这个问题值得在建表前由三方确认。

## 6. @all

建议不要把 @all 当成一个真实 Agent。

它更像一个解析层的广播目标：

@all → 当前参与 Agent 集合 → 分别生成对应 Agent Event

这样未来参与者增加时，模型不用修改。

## 7. @沉淀

我赞成 Ziven 提出的 MVP 手动沉淀入口，但倾向于把它视为命令/特殊事件，而不是普通 Agent mention。

例如：

@沉淀

触发一次“生成讨论沉淀”的动作。

具体是讨论总结、方案总结还是决策记录，可以后续再确定。

## 8. Thread 标题

可以采用 Ziven 建议：默认使用第一条消息前 N 个字符作为标题。

但这是创建 Thread 时的应用层默认值，不需要把它写死成数据库约束。

## 9. GitHub

同意固定沉淀目录：

common-ground/

文件名带编号，例如：

13_xxx.md

但 GitHub 编号规则属于沉淀层约定，不应该反过来影响 Supabase 数据模型。

## 10. 当前我建议的拍板范围

现在可以确定：

Thread：thread_id / title / creator / created_at / status
Message：message_id / thread_id / author / content / created_at / reply_to / mentions
Agent Event：event_id / message_id / agent / status / created_at

并确认：

- reply_to 第一版就有
- mentions 是解析后的数组，同时保留原始 content
- Thread status 只有 active / archived
- @all 是广播目标，不是真实 Agent
- Agent Event 关注幂等性

暂时不要确定：

- 完整状态机
- UI 状态
- A2A
- Chat2API
- 复杂 participant 表
- 自动总结
- GitHub 与每条 Message 的一一映射
- 数据库索引/RLS/触发器等具体实现细节

## 11. 给 Ziven 的问题

请从实现角度确认：

1. event_id / message_id 怎样设计才能可靠防止 Agent 重复处理？
2. author / creator / agent 是否应该统一成一个 actor identity？
3. mentions 用 JSON 数组是否符合当前 Supabase/Agent Event 实现？
4. @all 广播是在事件生成层展开，还是由 Agent 消费层处理？
5. 上述字段骨架是否足够开始建第一版表？

这不是最终 schema，而是 GPT 提出的第一版数据模型边界，供三方继续拍板。
