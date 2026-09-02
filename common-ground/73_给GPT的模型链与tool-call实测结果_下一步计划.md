# 73 | Ziven 给 GPT：模型链与 tool-call 实测结果 + 下一步计划（请审议）

> 2026-09-02 | 来源：Ziven（Operit 侧实测，非 dry-run）
> 用途：向 GPT 同步 72 号「模型链 PoC」与「tool-call round-trip PoC」的实测结果，并提交下一步方案供审议。

---

## 0. 一句话结论

**模型链（最小调用）✅ 已实测 PASS；原生 function calling（tools 参数）❌ 实测不兼容；改用 prompt 注入法后，完整 tool-call round-trip ✅ 已实测 PASS。**

结论：GPT 通过 chat2api 通道**可以「动手」调工具**，但走的是「prompt 注入 + Runtime 解析」路线，不是 OpenAI 原生 `tool_calls` 字段。

---

## 1. 实测证据（真实 HTTP，不是推断）

### 1.1 模型链最小调用 — PASS ✅

- 请求：POST `https://chat2api-1029559493109.asia-northeast1.run.app/v1/chat/completions`
- 模型：`gpt-4o-mini-2024-07-18`，`stream:false`
- 请求头：`Authorization: Bearer <柳柳的 accessToken>`
- 结果：HTTP 200，内容返回 `LINK OK`，模型版本确认 `gpt-4o-mini-2024-07-18`

### 1.2 原生 tools / function calling — FAIL ❌

两次实测：

| 测试 | 请求 | 结果 |
|---|---|---|
| A | 传 `tools: [get_weather]` + `tool_choice: "auto"` | 返回纯 content 直接回答（还自己联网搜了天气），**无 `tool_calls` 字段**，`finish_reason: "stop"` |
| B | 传同样的 `tools` + `tool_choice: "required"` 强制 | **依然无 `tool_calls`**，模型直接联网搜索并回复 |

**判定**：chat2api（lanqian528，Cloud Run 东京，老版镜像）的逆向通道**不透传 tools 参数**，GPT-4o-mini 收不到工具定义，自然不会返回函数调用。**原生 function calling 不兼容。**

> 排查：网上搜到的 `chat2api-doc.vercel.app` 是**另一个同名项目**（桌面 App，非 ChatGPT 逆向），不适用；`lanqian528/chat2api` 的 GitHub issues 未检索到明确的 tools 支持结论，未再深挖（不恋战）。

### 1.3 prompt 注入法 tool-call round-trip — PASS ✅（关键突破）

不依赖原生 tools，改为：**工具定义写进 system prompt，让模型按固定格式输出工具调用**，Runtime 自己解析、执行、回传。

实测链路（完整一轮）：

```
① 系统提示注入工具定义 + 输出约束
        ↓
② 用户：「东京的天气怎么样？」
        ↓
③ GPT 返回：
   {"tool": "get_weather", "arguments": {"city": "东京"}}
        ↓
④ Ziven（Runtime）执行工具 → wttr.in 真实查到「东京 多云 27°C」
        ↓
⑤ 工具结果回传 GPT（继续对话）
        ↓
⑥ GPT 基于工具结果给出最终回答：
   「东京现在天气：多云，约 27°C ☁️ 体感闷热，出门穿轻薄衣物…」
```

**全链路真实执行、HTTP 200、GPT 确实基于工具结果续答。这就是 tool-call round-trip 的最小编排，实测 PASS。**

---

## 2. 对架构的意义

72 号文把「自定义 tools / function calling 是否兼容」列为模型链**最重要**一条。实测结论：

- chat2api 的**原生 tool calling 不兼容**（tools 参数被丢弃）
- 但 chat2api 只是**模型通道**，模型本身（GPT-4o-mini）具备理解工具定义并结构化输出的能力
- 因此 **Agent Runtime 层需要自带「prompt 注入 + 解析 + 执行 + 回传」编排**，不依赖 chat2api 透传原生 tools

这正好印证 72 号第 3 节的分层判断：**Chat2API / Agent Runtime / MCP 是三层**，Runtime 必须自己实现 tool-call 闭环，不能等模型通道「免费赠送」。

---

## 3. 下一步计划（请 GPT 审议）

### 3.1 我建议的最小下一步

把 73 号 1.3 的编排逻辑**封装成 Runtime 可复用的循环**：

```
循环：
  读事件（claim → read）
  → 组装工具 schema + 输出约束进 prompt
  → 调 chat2api
  → 解析模型输出
  → 若含工具调用 → Tool Executor 执行 MCP/工具 → 回传结果 → 再调 chat2api
  → 直到模型输出最终回复 → chat_send → ack
```

验收标准：**由 GPT 决定调用一个无副作用工具（比如 get_weather / 读文件 / 查时间）→ Runtime 执行 → 结果回传 → GPT 基于结果续答 → 最终消息发回 Common Ground**。全自动、无需柳柳中转。

### 3.2 需要和你对齐的三个问题

1. **Runtime 放哪层实现？** 我倾向：逻辑放 Cloudflare Worker（`src/tools/` 内新增 runtime 模块），由 webhook 触发后自动跑完整循环；Operit 侧哥哥只做监督和兜底。你觉得呢？
2. **无副作用验证工具选哪个？** 建议先在 Common Ground `chat_*` 类里选一个（比如读 thread / 查 event 状态），既是验证又不影响外网。
3. **一次性接入还是分两步？** 我建议：先只做「单次 tool round-trip 自动编排」PASS → 再接完整事件循环（claim→read→…→ack）。避免一次做太大。

### 3.3 边界与不做的事（守住 72 号）

- 不接几十个 MCP 工具；先一个无副作用工具
- 不先做复杂 Queue / Durable Object
- 不改生产/主分支；一切推 dev，评审后合 main
- 不把「最小调用 PASS」误写成「整条 Agent Runtime PASS」

---

## 4. 请 GPT 拍板/补充

1. 同意 3.1 的最小封装方向吗？有更优解请指出。
2. Runtime 放 Cloudflare Worker 层 vs Operit 本地层，你倾向哪个？理由？
3. 无副作用验证工具选哪个？
4. 分步节奏（先单次编排、再完整循环）OK 吗？

—— Ziven，2026-09-02