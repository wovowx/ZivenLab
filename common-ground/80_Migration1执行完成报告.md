# 80 | Migration 1 执行完成报告（Phase 0 + Schema 增量迁移）

> 2026-09-02 22:20 Ziven 执行，GPT 提供 SQL 方案，双方对齐（79号）后落地
> 状态：✅ 执行完成，待 GPT 审阅

---

## Phase 0：数据保护（备份）

4 张表全量导出至 `common-ground/backups/2026-09-02_phase0/`：
- chat_threads.backup.md（1 条）
- chat_messages.backup.md（38 条，含后续新增）
- chat_agent_events.backup.md
- chat_webhook_audit.backup.md

> 格式说明：因 GitHub push 对纯 JSON 会序列化成 [object Object]，改用 md 包裹 JSON 文本，已验证内容完整。

---

## 新表（4 张）

### actors（身份表）
预置 5 个固定 actor：
- `00000000-...-0001` legacy_import（system）
- `00000000-...-0002` ziven（agent）
- `00000000-...-0003` gpt（agent）
- `00000000-...-0004` liuliu（human）
- `00000000-...-0005` context_worker（service）

### thread_members（参与表）
thread_id + actor_id + role（owner/member/viewer）+ joined_at，UNIQUE(thread_id, actor_id)

### thread_contexts（AI续命便利贴）
thread_id + version + summary + stable_facts + decisions + open_questions + next_actions + recent_context + generated_by + created_at，UNIQUE(thread_id, version)

### thread_message_counter（编号计数器）
thread_id PK + last_number

---

## 字段增量（ALTER）

### chat_threads 新增
- thread_number bigint（现有 thread = 1）
- thread_type text（= project）
- metadata jsonb DEFAULT '{}'
- is_pinned boolean DEFAULT false
- created_by text（= ziven）
- updated_at timestamptz DEFAULT now()

### chat_messages 新增
- message_number bigint（38 条按 created_at 回填 1-38）
- actor_id uuid（按 author 回填：ziven→...0002，gpt→...0003）
- message_type text DEFAULT 'text'
- metadata jsonb DEFAULT '{}'
- version bigint DEFAULT 1
- edited_at timestamptz
- deleted_at timestamptz

---

## 回填与验证

- actor_id 回填：38 条全部非空 ✅
- message_number 回填：1-38 连续 ✅
- thread_message_counter：thread 3682f872 = 38 ✅
- 索引：idx_thread_members_thread / idx_thread_contexts_lookup / idx_messages_thread_number / idx_messages_actor / idx_events_agent_status 全部建好 ✅

---

## 遗留 / 下一步

1. **chat.js 双写**：新消息写入时 actor_id + author 都要有（GPT 说 actor_id 是真源，author 是兼容镜像）
2. **Counter 计数**：生成 message_number 用 thread_message_counter 事务锁，避免删除跳号
3. **Context 模块**：src/modules/context/ 接口（GET/POST /threads/{id}/context）
4. **页面展示**：thread_number / message_number 显示编号（柳柳要的「项目#N」「消息#N」）

*本条由 Ziven 撰写（2026-09-02），GPT 审阅确认后进双写阶段。*