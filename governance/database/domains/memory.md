# Memory 域数据模型 · 2026-09-09

> 记忆系统：Agent 的长期记忆 + 文件存储。
> 语义：记忆是 key-value + 分类的语义条目，文件是媒体/文档的元数据表。

## 表清单

| 表 | 角色 |
|---|---|
| memories | 记忆条目（含版本/状态/追溯字段） |
| memory_events | 记忆变更账本（追加式，禁改删） |
| files | 文件元数据 |

## memories（记忆）
**用途**：所有 Agent（Ziven/GPT）的长期记忆。key + value + 分类。2026-10-17 升级加 version/status/supersedes_id/source_ref/valid_from/valid_to/type（无损，旧数据保留）。

当前有效判定：`status='active' AND valid_to IS NULL`。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| key | text | 记忆键（语义） |
| value | text/timestamptz | 内容（或时间） |
| category | text | 分类 |
| title | text | 标题 |
| created_at / updated_at | timestamptz | |

**坑**：不同来源的记忆 key 格式不同（事件/实体/日常…）；分类用于归档。

## memory_events（事件账本）
**目标语义**：记录 memories 的 create/update/revoke/restore 等生命周期事件，作为追溯与审计依据。文档历史记录称 `memory_events` 禁止 UPDATE/DELETE（触发器，2026-10-17 实装）；当前触发器/RLS 规则仍应以实时数据库证据复核。**实现覆盖不能由表设计推定**：2026-10-23 对 `mcp-memory/dev/src/tools/memory_unified.js` 的静态检查只看到 `putMemory` 在 update 路径显式 POST `memory_events`，且未检查该请求的 HTTP 状态；create、soft-delete、rename、move 未见完整的显式生命周期事件链。当前 rename/move 先软删源、再写目标，相关写请求不检查 HTTP 状态，也无事务/补偿/核验。因此暂不能声称所有变更均可审计或可靠回滚；此处是源码静态发现，不代表已证实发生数据丢失。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| memory_id | uuid | 关联记忆 |
| event_type | text | create/update/revoke/restore |
| actor | text | user/agent/system |
| idempotency_key | text 唯一 | 防重复入账 |
| version | int | 对应变更后记忆版本 |
| old_value / new_value | jsonb | 变更前后 |
| reason | text | 变更原因 |
| source_ref | text | 来源引用 |
| created_at | timestamptz | |

## memory_aliases（检索别名索引）
**用途**：一条记忆补多个检索入口（项目名/简称/技术名），解决「想不起 key 也能找到」。2026-10-18 建。检索流程：先关键词 search 查 content/key → 再匹配 alias → 合并 → 过滤 status='active'。

| 列 | 类型 | 含义 |
|---|---|---|
| alias | text 唯一 | 别名/关键词/旧称 |
| memory_id | uuid | 关联记忆 |
| created_at | timestamptz | |

## files（文件）
**用途**：上传文件的元数据（实际内容在 Supabase Storage）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| file_path | text | 存储路径 |
| file_name | text | 展示名 |
| file_size | int | 字节 |
| file_type / content_type | text | MIME |
| category | text | 分类 |
| tags | jsonb | 标签 |
| description | text | |
| storage_url | text | 完整 URL |
| created_at / updated_at | timestamptz | |

## knowledge
✅ 已确认不存在（2026-10-17 实测，schema cache 404）。已从总表移除。

## 变更记录
- 2026-10-17：v2 新增 memory_events 语义；memories 升级加版本/状态/追溯字段；knowledge 确认已移除
- 2026-09-09：v1（2026-09-09 实测）
