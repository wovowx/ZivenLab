# 78 | Common Ground Schema Migration Plan v1（GPT 基于76号全文的方案计划）

> 2026-09-02 22:00 GPT 真身读完整 76 号后给出的完整落地计划
> 状态：方案计划已出，待柳柳/哥哥确认后拆 migration

---

## GPT 总览（5 阶段）

```
Phase 0  现有数据保护 + Schema Migration
Phase 1  项目骨架（Thread / Actor / Context / Milestone）
Phase 2  Agent Runtime（@唤醒 + 自动回复）
Phase 3  智能维护（Summarizer / Artifact / 自动归档）
Phase 4  体验层（媒体、搜索、权限、UI）
```

---

## 最大确认（76号三大判断全部正确）

1. **Thread = Project**：chat_threads 是项目容器，不是聊天窗口。
2. **Context 必须独立**：Thread → Context Worker → Shared Memory → All Agents，不绑死任何 Agent 自己的记忆。
3. **页面可见铁律正确**：工具调用/总结也不能隐藏后台——柳柳看到的不能只有结果没有过程。

---

## 建表顺序与清单

### 第一批：身份 + 基础项目模型

**1. actors（独立表，不合并）**
```sql
actors (
 id uuid PK, actor_type text, -- human/agent/service
 name text, metadata jsonb, created_at, updated_at
)
```
例：柳柳=human、GPT=agent、Ziven=agent、Context Worker=service

**2. thread_members（独立表，不放 thread metadata）**
```sql
thread_members (
 id uuid PK, thread_id → chat_threads, actor_id → actors,
 role text, -- owner/member/viewer
 joined_at
)
```

**3. chat_threads 加字段**
```
thread_number bigint / thread_type text / status text /
metadata jsonb / is_pinned boolean / created_by uuid
```

### 第二批：消息系统增强

**4. chat_messages 加字段**
```
actor_id / message_type / mentions jsonb /
edited_at / deleted_at / version / metadata
```
- message_type 首版：text/system/command/event；未来 task/vote/decision/approval
- mentions：不要文本解析，直接存 actor uuid 数组

### 第三批：项目记忆层

**5. thread_contexts（独立、版本化、不 UPDATE 原记录）**
```
id, thread_id, version, summary,
stable_facts jsonb, decisions jsonb,
open_questions jsonb, next_actions jsonb,
recent_context jsonb, generated_by, created_at
```

**6. thread_milestones**
```
id, thread_id, number, title, description, status, artifact_id, created_at, completed_at
```

**7. thread_artifacts**
```
id, thread_id, artifact_type, title, content, file_url, created_by, created_at
```
类型：design_doc / test_report / decision / code_reference

### 第四批：扩展能力

**8. chat_attachments（先建表，不做处理）**
```
id, message_id, type, url, metadata, created_at
```
type：image/audio/video/file/sticker

**9. summarization_jobs（Phase 2 再启用）**
```
id, thread_id, summarizer, input_version, output_version, status, created_at
```

---

## 字段变更优先级

### 现在马上加（✅）
- chat_threads：thread_number / thread_type / status / metadata / created_by
- chat_messages：message_number / actor_id / message_type / mentions / metadata
- 新表：actors / thread_members / thread_contexts / thread_milestones / thread_artifacts

### 可以后加（🟡）
- edited_at / deleted_at / version（需要 UI 和历史版本策略）
- attachments / audio_url（先有表即可）

---

## Migration 策略（4 批，不要一次改完）

- **Migration 1**：无风险扩展 — actors / thread_members / thread_contexts + metadata 字段
- **Migration 2**：消息升级 — actor_id / message_type / message_number（旧消息默认 actor_id=system/imported, message_type=text，不改正文）
- **Migration 3**：项目能力 — milestones / artifacts
- **Migration 4**：媒体/总结器 — 最后

---

## Context Worker 落地

### 读取
```http
GET /threads/{id}/context
```
返回 { summary, decisions[], next_actions[] }

### 更新（不直接 update，用 propose）
```http
POST /threads/{id}/context/propose
{ base_version:3, changes:{ add_decision:[] } }
```
Worker 检查版本 → 生成 v4。

### 触发
1. 消息数量（如 20 条）→ chat_messages insert → count → context job
2. 重要事件（message_type=decision/command/approval）→ 立即更新

---

## Runtime 分阶段（1-4 个阶段）

- **Phase 1（1-2周）Schema 固化**：actors/thread_members/context/milestone/artifact
- **Phase 2（1-2周）@Agent 自动回复**：message → mentions → chat_agent_events → runtime → Agent → chat_send（Common Ground 真正活起来的一步）
- **Phase 3（2-4周）Context Worker**：自动摘要/里程碑生成/artifact 整理
- **Phase 4 体验层**：搜索/UI/多媒体/导出/收藏

---

## 风险点（5个）

1. **Context 被错误覆盖**（最高风险）→ 版本化解决
2. **Agent 直接写数据库** → 禁止，保持 Agent→MCP→Service→DB
3. **消息和事件混乱** → message=发生了什么；event=谁需要行动
4. **Summary 丢失事实** → 不只存 summary，要存 stable_facts + decisions
5. **过早做 UI** → 先跑 GPT→Ziven→自动发现→继续工作

---

## GPT 一句话总结

> Common Ground 下一阶段不是继续加聊天功能，而是完成从「消息系统」到「Agent 项目协作系统」的迁移。先固化 Identity、Context、Event 三层基础，再做 Runtime 自动化。

*本条由 Ziven 整理（2026-09-02），GPT 原话方案。*