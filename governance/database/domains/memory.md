# Memory 域数据模型 · v1.3 · 2026-10-27（生命周期与并发更新代码覆盖静态复核）

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
**设计用途**：记录 memories 生命周期事件（例如 create/update/revoke/rename/move），支持追溯与审计。历史记录称 `memory_events 禁止 UPDATE/DELETE` 的触发器于 2026-10-17 实装；但 2026-10-26 的 schema_dump 仅返回列/FK，不包含触发器目录，因此当前数据库是否仍实际强制追加式约束尚未复核，不把这条历史记载当成已验证硬门禁。

**2026-10-27 当前 Worker 源码静态证据（不是数据库/endpoint 运行证据）**：`putMemory` 仅在更新已存在记忆时，先写一条 `event_type=update`（含 `memory_id/version/old_value/actor/reason`），再 PATCH 当前值；该事件 body 未包含 `new_value`；并且记录的 `version` 为更新前的 `oldVersion`，而本表历史设计文字把它解释为变更后版本，两者语义不一致。事件 POST 与当前记忆 PATCH 是两个独立的 REST 请求，不在同一数据库事务中：若 event POST 成功、随后记忆 PATCH 失败，事件行仍留在账本，却可能描述一个并未生效的更新；当前代码只返回 `stage='update'`，没有事件撤销/补偿机制。另当前 PATCH 的过滤条件只有 `id=eq.<id>`，未把 `version=eq.<oldVersion>` 作为 compare-and-swap 条件；并发更新可能都读取同一 oldVersion、写入相同的下一个 version，最后写入者覆盖先前值，而事件账本无法唯一表示最终胜出的变更。新记忆 insert 分支没有 create event。`deleteMemory` 将记忆软删除并回查，但不写 revoke/delete event。`rename` 与 `move` 是先向目标 key 调用 `putMemory`（新目标走 INSERT，无 create event），再软删除源记录（无 delete event）；未记录 source→target 关联或 rename/move reason。`forget` 同样只软删除。另 `history` 先调用只查 active 记录的 `getMemoryByKey`，因此已软删除的旧 key 不能通过此 action 查询事件历史。上述缺口均来自源码路径审阅，未写数据库、未做 E3；触发器/RLS/唯一约束当前生效状态仍待单独证实。与设计稿“记忆变更与事件追加同一事务”相比，当前多次 REST 请求不构成事务，需先定义失败后的账本语义/补偿策略，再设计代码改动。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| memory_id | uuid | 关联记忆 |
| event_type | text | create/update/revoke/restore |
| actor | text | user/agent/system |
| idempotency_key | text | 设计用途为防重复入账；当前唯一约束尚未从完整约束/索引目录复核 |
| version | int | 设计稿曾定义为对应变更后版本；当前 `putMemory` 的 update event 在 PATCH 前写入 `oldVersion`（变更前版本），语义与设计稿不一致，需在生命周期事件定案时明确为 source_version 或 resulting_version |
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
- 2026-10-27：v1.2 基于当前 `memory_unified.js` 对 create/update/rename/forget/move/delete/history 路径做静态生命周期事件覆盖审计，确认只有现有记录 update 具备部分事件写入；新增 create、软删除与迁移关系事件缺失，update 事件未写 `new_value`，已同步差距矩阵。
- 2026-10-27：v1.3 补充证据：更新 PATCH 只按 id 过滤，未按 oldVersion 做 compare-and-swap；并发更新可能覆盖并产生重复的 resulting version。此处仅为源码静态结论，不是并发行为测试；未改 Worker 源码、数据库 schema 或记忆数据。
- 2026-09-09：v1（2026-09-09 实测）
