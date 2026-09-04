# 77 | GPT 补漏审议结果（对 76 号的最终架构检查）

> 2026-09-02 21:50 GPT 真身对补漏清单的完整审议
> 状态：补漏完成，MVP 架构基本稳定，下一步进入 schema 固化

---

## GPT 总体结论

> 现在不要追求做一个 Discord/Slack。优先保证 Agent 协作所需的四件事：**身份 → 消息 → 事件 → 上下文。**

Common Ground 不再是聊天数据库，而是：
- 多 Agent 协作协议层
- 共享项目记忆层
- 事件驱动 Runtime 层

设计优先级围绕：Agent 能不能可靠理解、发现、继续工作。聊天体验反而是第二层。

---

## 8 个补漏点逐条审议

| # | 项 | 判断 | 落点 |
|---|---|---|---|
| 1 | 消息编辑/撤回/删除 | ✅ 预留字段，不做复杂逻辑 | chat_messages 加 `edited_at / deleted_at / version`；编辑=新版本，删除=soft delete |
| 2 | 搜索 | ✅ 值得现在做基础版 | 关键词/thread_id/actor_id/时间范围；先用 PostgreSQL full text search，不上 embedding |
| 3a | 未读提醒 | ✅ 必须做（Agent 自动发现依赖） | 新表 `thread_reads`(thread_id, actor_id, last_read_message_id, updated_at) |
| 3b | 置顶 | ✅ 预留即可 | chat_threads 加 `is_pinned` |
| 3c | 收藏 | ⏳ 超 MVP | UI 使用习惯，不影响协议 |
| 4 | 权限控制 | ✅ 必须预埋，不做复杂 RBAC | 新表 `thread_members`(thread_id, actor_id, role)；role: owner/member/viewer |
| 5 | 通知机制（@） | 🔥 核心功能，必须设计 | @ 是协议不是文字：message metadata 加 `mentions:[actor_id...]`；链路 message→mention resolver→chat_agent_events→runtime |
| 6 | 导出/归档 | ✅ 预留即可 | chat_threads 加 `status`(active/archived/deleted) |
| 7 | 消息类型 | ✅ 必须预留 | chat_messages 加 `message_type`：text/system/command/event；未来 task/vote/approval/decision |
| 8 | AI 状态显示 | ✅ 协议预留，MVP 不做 UI | Runtime 状态用 queued/processing/completed/failed（复用 event 状态）；不要把“正在思考”存成业务数据 |

---

## 最终优先级

### ⭐⭐⭐⭐⭐ 现在必须加入架构
1. **Actor Identity**（谁说的）→ 新表 `actors`
2. **Mention/Event**（谁需要行动）→ metadata.mentions
3. **Thread Context**（我们之前做到哪）
4. **Thread Member**（谁能参与）→ 新表 `thread_members`
5. **Read State**（谁已经处理）→ 新表 `thread_reads`

### ⭐⭐⭐⭐ 现在只预留
- edit/delete 字段、message_type、archive status、metadata、attachment interface

### ⭐⭐ 超 MVP（砍）
- 收藏、投票系统、完整权限、AI 状态 UI、导出界面

---

## 关键闭环

```
Actor → Message → Event → Context → Artifact
```

- actors（谁）
- thread_members（谁参与）
- thread_reads（谁看到）

---

## 下一步（GPT 建议）

> 这轮补漏完后，MVP 架构基本稳定。下一步进入 **schema 固化 + migration**，而不是继续无限扩需求。

*本条由 Ziven 整理（2026-09-02），GPT 原话审议。*