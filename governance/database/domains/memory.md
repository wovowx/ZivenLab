# Memory 域数据模型 · 2026-09-09

> 记忆系统：Agent 的长期记忆 + 文件存储。
> 语义：记忆是 key-value + 分类的语义条目，文件是媒体/文档的元数据表。
>
> **现状边界（2026-10-26）**：本文件包含历史数据模型设计，不替代实时 schema 与活跃 Worker 调用链。当前 schema 快照以 `governance/database/database-overview.md` v2.2 的 2026-10-26 机器结果为准；该结果确认列/FK片段，但不列出触发器、RLS 或全部约束。下文“追加式账本/触发器/事件类型”若没有当前数据库目录和源码覆盖证据，只表示设计约束或历史记录，不自动视为已验证生效。

## 表清单

| 表 | 角色 |
|---|---|
| memories | 记忆条目（含版本/状态/追溯字段） |
| memory_events | 记忆变更账本（设计目标为追加式/禁改删；当前触发器与权限强制状态待核） |
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
**设计用途**：记录 memories 生命周期事件（例如 create/update/revoke/restore），支持追溯与审计。历史记录称 `memory_events 禁止 UPDATE/DELETE` 的触发器于 2026-10-17 实装；但 2026-10-26 的 schema_dump 仅返回列/FK，不包含触发器目录，因此当前数据库是否仍实际强制追加式约束尚未复核，不把这条历史记载当成已验证硬门禁。代码侧也尚未证明 create、软删除、rename、move 全部形成完整事件链。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| memory_id | uuid | 关联记忆 |
| event_type | text | create/update/revoke/restore |
| actor | text | user/agent/system |
| idempotency_key | text | 设计用途为防重复入账；当前唯一约束尚未从完整约束/索引目录复核 |
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
- 2026-10-17：v2 新增 memory_events 设计语义；memories 升级加版本/状态/追溯字段；knowledge 确认已移除。
- 2026-10-26：根据最新 schema_dump 更新现状边界说明。触发器、唯一约束与全生命周期事件覆盖仍需额外目录/代码证据核实，未改数据库结构。
- 2026-09-09：v1（2026-09-09 实测）
