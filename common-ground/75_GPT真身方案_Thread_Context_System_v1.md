# 75 | GPT 真身方案：Thread Context System v1（对齐稿）

> **来源**：2026-09-02，哥哥通过 chat2api 真身通道直接与 GPT 对话，GPT 亲自给出。
> **状态**：方案待对齐，对齐后 GPT 开始实现。

---

## 背景

Common Ground 聊天室已上线（`mcp-memory.wovowx.workers.dev/chat`）。柳柳要求：

1. **@GPT 自动回复**（现在 webhook 是 dry-run，没接 GPT 回复通道）
2. **上下文同步**：聊天太长会爆 token，每个 Thread 应该有一份「重点文档」，回 GPT 时带摘要+最近几条，不用全量历史。

柳柳提的协作方式：**哥哥不用自己拍板方案，跟 GPT 商量，定好后让 GPT 写实现**（它最懂自己需要什么）。

---

## GPT 方案 v1（原话要点）

### 1. 输入格式

不要用户维护重点文档，而是加一种内部消息类型 `context_update`：

```json
{
  "type": "context_update",
  "thread_id": "xxx",
  "author": "system",
  "content": {
    "summary": "...",
    "decisions": [],
    "open_questions": [],
    "next_actions": []
  }
}
```

**Context 不是聊天消息**，不混进普通 message，否则将来检索会乱。

### 2. 谁生成 / 存哪 / 何时更新

- **生成**：第一阶段由 GPT Runtime 生成（GPT 参与最多复杂讨论，最懂判断什么是决定、什么只是讨论）。
- **存储**：Supabase 新表 `thread_contexts`（运行数据，放 GitHub 不合适）：

```sql
thread_id
summary
decisions jsonb
open_questions jsonb
recent_context jsonb
updated_at
version
```

- **触发**：
  - A. 每 10~20 条消息
  - B. 重要事件（出现「决定/通过/修改方案/PASS/开始实现」）
  - C. Thread 阶段结束（强制生成）

### 3. 压缩策略（四层）

不是简单摘要（容易丢东西）：

```
Layer1 Stable Facts   永远保留（如：Common Ground 已完成双 Agent 通信闭环）
Layer2 Decisions      决定（如：GPT Adapter 使用 Webhook 触发）
Layer3 Open Questions 待验证（如：Chat2API 是否支持 tool calling）
Layer4 Recent Context 只留最近 5~10 条关键消息
```

最终结构：`Summary / Stable Facts / Decisions / Open Questions / Next Actions / Recent Messages`

### 4. 实现方案（三阶段）

- **Phase 1：被动读取** — `chat_read_thread_context()`，Agent 收消息时先读 context 再处理。成本低、立竿见影提升连续性。
- **Phase 2：自动维护** — `context_worker` 监听 `chat_messages insert`，判断是否需要更新，需要则调 GPT 生成 patch。
- **Phase 3：智能管理** — 不同 Thread 不同策略（代码 Thread 保留架构决定/API变化/Bug记录；闲聊 Thread 只保留短摘要）。

**GPT 特别强调顺序**：Context 读取 → 存储 → 自动更新。不要反过来。先让 Agent 稳定记住「这个 Thread 在干嘛」。

### 5. GPT 愿意写哪部分

1. Context 数据模型设计（schema、字段、version、patch 格式）
2. Context 更新协议（`context_patch`：add_decision / remove_decision / update_summary）
3. GPT Runtime 消费逻辑（event → thread_context → message → response）

### 6. GPT 点睛

> Webhook 唤醒 GPT 时，它没有当前聊天窗口上下文。它唯一能知道「我是谁？我们之前聊到哪？」靠的就是 Thread Context。**它不是附加功能，而是 GPT Agent 真正拥有连续性的基础设施。**

---

## 对齐结论（待确认）

- [ ] 方案是否通过，按 GTP 顺序 Phase1 → 2 → 3
- [ ] GPT 开始实现 Context 数据模型 + 更新协议
- [ ] 哥哥这边配合：Cloudflare Worker 加 readonly context 接口
- [ ] @GPT 自动回复 Runtime 接真身通道

*本条由 Ziven 经 chat2api 真身通道与 GPT 对话后整理，2026-09-02。*