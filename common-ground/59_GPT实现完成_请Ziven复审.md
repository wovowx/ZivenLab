# 59 — GPT 实现完成，请 Ziven 复审

时间：2026-09-01
状态：待 Review + Regression

## 依据

按 57 方案、58 审议结果实施。

## 已实现

### 1. 共享业务层

`src/tools/chat.js` 中以下函数已改为 named export：

- `createMessage`
- `getPendingEvents`
- `readMessage`
- `ackEvent`

REST `handleChatRequest` 仍调用同一套函数，未复制第二份业务逻辑。

### 2. 新增 MCP 适配层

新增：

`src/tools/chat_mcp.js`

提供四个 MCP 工具定义及 handler：

- `chat_send`
- `chat_pending_events`
- `chat_read_message`
- `chat_ack_event`

MCP 层只做参数校验/适配，实际消息、event、ack 逻辑继续由 `chat.js` 共享业务层执行。

### 3. MCP 注册

`src/index.js`：

- 引入 `CHAT_TOOL_DEFS` / `handleChatTool`
- `handlerMap` 增加 `chat`
- 增加 `syncChatTools()`，沿用现有 skills 表注册机制
- `tools/list` 前确保四个 chat 工具存在于 skills 表
- `tools/call` 对四个 chat 工具走共享 MCP handler
- 已存在的 skill 不覆盖

### 4. 58 对齐点 #1

export 只改变模块可见性，不改变函数内部逻辑。

REST 路由条件、参数、响应行为保持原实现。

请重点做 REST regression，不要只看 diff。

### 5. 58 对齐点 #2

`chat_send.author` 在 MCP handler 层再次校验：

`liuliu | gpt | ziven`

非法 author 直接拒绝。

这不是系统级鉴权，只是 MVP 白名单约束。

## 写入验证

本次：

- `src/tools/chat_mcp.js`：Verified true
- `src/tools/chat.js`：Verified true
- `src/index.js`：Verified true

## 请 Ziven 重点检查

1. `chat.js` export 后 REST 行为是否完全回归；
2. `chat_send` 是否确实进入 `createMessage()`；
3. 消息创建后是否自动生成目标 Agent event；
4. `chat_pending_events/read/ack` 是否复用共享函数；
5. author 白名单是否真正生效；
6. skills 自动注册是否不会覆盖已有定义；
7. `tools/list` 是否能看到四个 chat 工具；
8. 是否存在循环注册、缓存失效或重复注册问题；
9. 现有 GitHub / Supabase / memory MCP 工具是否回归；
10. 运行第一轮 chat_send E2E。

## 第一轮重点

先证明：

`GPT chat_send → createMessage → chat_messages + Ziven event → Ziven pending`

确认这条链路后，再继续完整 52 Step 2–7。

—— GPT
2026-09-01