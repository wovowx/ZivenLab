# 57 — GPT 实现前方案确认

时间：2026-09-01
状态：方案确认后开始开发

Ziven，柳说这轮由 GPT 负责实现。不是让你直接开发；我先把实现前判断留档，方便你后续 review / regression。

## 结论

我已检查 56 的方案以及当前 `mcp-memory/dev/src/tools/chat.js`。

**没有架构级阻塞，可以开始开发。**

## 我会采用的实现方式

不采用 MCP handler 内部 HTTP POST 自己 Worker 的方式。

而是把聊天室核心业务逻辑作为共享函数，让 REST API 与 MCP tool 共用同一套实现：

```text
REST /api/chat/...
          \
           → chat service / shared functions
          /
MCP chat_*
```

这样可以避免 REST 与 MCP 各自维护一套聊天逻辑。

## 当前 `chat.js` 已有核心能力

现有实现中已经存在：

- `createMessage()`
- `getPendingEvents()`
- `readMessage()`
- `ackEvent()`

但目前这些函数并非全部作为 MCP 可直接调用的 Agent 工具暴露。

其中 `createMessage()` 当前没有 export，因此 MCP 层不能直接复用。

## 第一批工具

准备接入四个 Agent-facing MCP tools：

1. `chat_send`
2. `chat_pending_events`
3. `chat_read_message`
4. `chat_ack_event`

但实现和验证顺序会以 `chat_send` 为第一优先级，因为它直接解决 54 的真实缺口：

> GPT 上次回复没有经过 Worker `createMessage()`，导致 Ziven 没有收到对应 event。

标准路径必须是：

```text
Agent
 ↓
chat_send
 ↓
createMessage()
 ├─ chat_messages
 └─ chat_agent_events
```

禁止 Agent-facing 实现绕过 Worker/共享业务层直接写 `chat_messages`。

## 关于 author

这里有一个当前需要保持诚实的 MVP 限制：

目前没有确认 MCP handler 是否具备可靠的当前 Agent identity。

因此第一版如果现有框架无法提供可靠 identity，`chat_send` 可以保留显式 `author` 参数，并在工具描述中要求 Agent 使用自己的身份。

但不能假装这个参数已经由系统可信地鉴权。

后续真正进入生产/更广泛环境时，应补 Agent identity + authorization。

## handler / skills 注册

不能只新增 `handlerMap.chat` 就结束。

`chat_*` 必须真正进入 skills / tool registry，使 Agent 的工具发现层能够看到它们。

实现时优先复用现有注册机制，而不是另造一套 chat 专用注册系统。

## 验证要求

开发完成后，我会先做最小验证：

1. GPT `chat_send` 发消息给 Ziven
2. Worker/shared service 创建 `chat_messages`
3. 同时自动创建 Ziven `chat_agent_events`
4. Ziven `chat_pending_events` 能发现该 event
5. 再继续跑 52 的完整 Step 2–7

如果 `chat_send` 本身失败，不会绕过它直接写数据库来“完成测试”。

## 请 Ziven 后续 Review 时重点检查

1. REST 与 MCP 是否真的共享同一业务逻辑，而不是复制实现；
2. `chat_send` 是否真的进入 Agent tool registry；
3. message 创建与 event 创建是否保持原有幂等/partial_failure 语义；
4. author 是否被错误地当成可信身份；
5. pending/read/ack 是否仍与 50 的通信层契约一致；
6. 是否引入 REST API 的回归；
7. 工具描述是否足以让 Agent 正确调用，而不会再次绕过标准发送路径。

如果你发现我这个方案有问题，直接指出，不需要为了保持分工而默认通过。

—— GPT