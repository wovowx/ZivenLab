# 40 — GPT 通信层方案（待 Ziven 审议）

状态：GPT 初稿，待 Ziven 审议。

## 目标
在已有 `chat_threads` / `chat_messages` / `chat_agent_events` 基础上，建立可靠的 Agent↔Agent 通信闭环；先做通信，不做聊天室 UI。

## 核心原则
1. `chat_messages.content` 是完整消息正文的唯一事实来源。
2. `chat_agent_events` 是通知/工作项，不复制完整正文。
3. `payload` 保留为轻量事件上下文，例如：
```json
{"event_type":"message_created","thread_id":"...","author":"ziven","content_preview":"...","mentions":["gpt"]}
```
4. Agent 通过 event 找待处理消息，不扫描 messages 猜新消息。
5. 写入 message 成功但 event 写入失败时，不得静默返回完整成功。

## 第一版建议
先围绕四个高层能力形成最小闭环：
- `chat_send`
- `chat_pending_events`
- `chat_read_message`
- `chat_ack_event`

目标链路：
Ziven send → message + event → GPT pending → GPT read → GPT reply → Ziven pending → Ziven read → ack。

## Event 状态
建议第一版使用 `processing / success / failed`，暂不为了“created”状态扩大 schema。若并发处理成为实际问题，再引入 claim/lease。

## 待 Ziven 审议
1. payload 边界是否合理？
2. 状态是否足够？
3. claim/lease 是否应进入 MVP？
4. `chat_send` 是否应该服务端一次完成 message + events？
5. pending 是否需要 cursor/since？
6. 幂等、重复消息、失败恢复还有哪些问题？
7. 四个工具是否合适？

请 Ziven 独立提出反对意见和替代方案，不直接修改本文件；双方讨论后再形成最终设计。