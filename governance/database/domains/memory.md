# Memory 域数据模型 · v1.6 · 2026-10-27（生命周期、并发、写入口与 catalog 可观测性复核）

> 记忆系统：Agent 的长期记忆 + 文件存储。
> 语义：记忆是 key-value + 分类的语义条目，文件是媒体/文档的元数据表。
>
> **现状边界（2026-10-27）**：本文件包含历史数据模型设计，不替代实时 schema 与活跃 Worker 调用链。当前公开 OpenAPI 列快照已在 2026-10-27 重新读取并写入 `governance/database/database-overview.md` v2.4：memories 当前列集中包含 version/status/valid_to/type/trigger_intents/entities/related_memory_ids；memory_events 有 jsonb old_value/new_value 列及 memory_id 外键。此快照不提供触发器、RLS、GRANT、外键 ON DELETE 行为、唯一约束和函数权限。进一步尝试经 `supabase_db` REST query 读取 `information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 均返回 HTTP404/PGRST205（未在当前 public PostgREST schema cache 暴露）；经 `exec_sql` 做 catalog-only SELECT 也被 P0001 拒绝。已检查的 `mcp-memory/dev/migrations` 当前只有聊天室 `claimed_at` 迁移，未发现 memory_events trigger/function migration；这仅说明当前检查范围缺少这类源码/迁移证据，不能据此断言真实数据库里不存在触发器。当前可见 MCP 没有独立只读 catalog 查询工具。下文“追加式账本/触发器/事件类型”若没有当前数据库目录和源码覆盖证据，只表示设计约束或历史记录，不自动视为已验证生效。

## 2026-11-04 Worker Memory Core 代码分层与兼容入口收敛（仅 mcp-memory/dev）

本节记录当前代码归属与验证基线，不改变下方数据库模型、设计约束或历史生命周期结论：

- src/modules/memory/repository.js：memories、memory_events、memory_aliases 的数据访问层。
- src/modules/memory/lifecycle.js：putMemory、软删除、rename、move 的协调层；仍沿用分离的 REST 请求，rename/move 仍是目标写入后源软删除的两步流程。
- src/modules/memory/retrieval.js：记忆搜索、当前有效过滤、匹配评分、受约束中文 bigram 回退、一跳关联，以及列表/分类/日期/统计/随机读取。
- src/modules/memory/transfer.js：共享导入与导出用例；导入通过 lifecycle.putMemory 写入并按真实写入结果计数，导出统一过滤 active 且 valid_to IS NULL 的记录。
- src/tools/memory_unified.js：保留 MCP memory 工具与 action 兼容入口；原 getMemoryByKey/getAllMemories/findAuthoritativeKey/putMemory 兼容导出继续存在，搜索输出增加 match_reason，import/export 委托 transfer。
- src/tools/category.js：保留 list_categories/recall_by_category/move_category 旧入口，但读取与迁类已改为复用 repository/retrieval/lifecycle，不再自行执行 memories REST CRUD 或物理 DELETE。
- src/tools/data.js：保留 data import/export 兼容入口，与 memory action 共用 transfer；为保留旧接口差异，非法行在 data facade 中继续跳过，在 memory facade 中计为 failed。
- src/utils/search.js：仍只负责 search_history/suggest，不是记忆正文检索实现。

当前实现代码相关提交链：Memory Core 实现/兼容收敛 commit 5d20095f352ba45dd4104daa22e2d8f00e0c5a8b；transfer 模块 commit 6a9f49358161a933e4a3d3fa7840eb365e45947a；后续 facade/test 补齐持续提交至当前 mcp-memory/dev HEAD 5949f333f7081f65840b1024f54e2db108fc4ab5。失败边界测试基线 c3853215854a951da6ce00df9c51b18069c2ac62；transfer contract/facade parity 最新测试 SHA 5949f333f7081f65840b1024f54e2db108fc4ab5。GitHub Actions learning-regression run 41768648532 全步骤 SUCCESS；Memory Core contracts **47 passed / 0 failed**。上述为 E1 与 fetch-mock 行为证据，不证明真实 Supabase endpoint、生产数据库或真实 GPT/Operit 检索行为。此次没有修改 DB schema、表、函数、trigger、权限或数据。

生命周期语义差距仍然存在：create/revoke/rename/move 事件覆盖、update event new_value、事件与当前记录的事务一致性、CAS 并发保护以及 source→target 的原子迁移均未实现。rename/move 虽已统一入口并保留 type/source_ref/trigger_intents/entities/related_memory_ids 等语义元数据，但若源软删除失败仍会留下部分迁移并返回警告。category.js 旧的直接 REST DELETE/POST/PATCH 路径已于 2026-11-04 移除；data.js 与 memory_unified 的重复导入/导出用例已合并至 transfer.js。通用 supabase_db 仍是另一个可执行 CRUD/SQL 的潜在绕行入口，其实际 DB 权限不在本轮范围。下方静态生命周期差距仍有效，但旧的“category.js 当前直接物理 DELETE”仅作历史源码记录，不代表当前 dev 实现。
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

**2026-10-27 当前 Worker 源码静态证据（不是数据库/endpoint 运行证据）**：`lifecycle.putMemory` 仅在更新已存在记忆时，先写一条 `event_type=update`（含 `memory_id/version/old_value/actor/reason`），再 PATCH 当前值；该事件 body 未包含 `new_value`；并且记录的 `version` 为更新前的 `oldVersion`，而本表历史设计文字把它解释为变更后版本，两者语义不一致。事件 POST 与当前记忆 PATCH 是两个独立的 REST 请求，不在同一数据库事务中：若 event POST 成功、随后记忆 PATCH 失败，事件行仍留在账本，却可能描述一个并未生效的更新；当前代码只返回 `stage='update'`，没有事件撤销/补偿机制。另当前 PATCH 的过滤条件只有 `id=eq.<id>`，未把 `version=eq.<oldVersion>` 作为 compare-and-swap 条件；并发更新可能都读取同一 oldVersion、写入相同的下一个 version，最后写入者覆盖先前值，而事件账本无法唯一表示最终胜出的变更。新记忆 insert 分支没有 create event。`lifecycle.deleteMemory` 将记忆软删除并回查，但不写 revoke/delete event。`lifecycle.renameMemory` 与 `moveMemory` 仍是先向目标 key 调用 `putMemory`（新目标走 INSERT，无 create event），再软删除源记录（无 delete event）；未记录 source→target 关联或 rename/move reason。2026-11-04 起 `category.js` 的 `move_category` 已委托该 lifecycle 流程，不再直接对 memories 物理 DELETE；这只消除了该 Worker 工具入口的旁路，不构成事务原子化。`forget` 同样只软删除。另 `history` 先调用只查 active 记录的 `getMemoryByKey`，因此已软删除的旧 key 不能通过此 action 查询事件历史。上述缺口均来自源码路径审阅，未写数据库、未做 E3；触发器/RLS/唯一约束当前生效状态仍待单独证实。继续核对写入口发现：data.js 的 import 复用 memory_unified 兼容导出的 putMemory；category.js 旧 move_category 直接 CRUD 的实现已在 2026-11-04 移除，当前改为委托 lifecycle.moveMemory。已注册的通用 supabase_db 可执行任意表 CRUD，exec 会调用原始 exec_sql；若仅在 Worker memory handler 增补事件逻辑，这些路径仍可能绕过。因此，硬性事务/事件不变量必须落实在数据库写入边界，且先核对真实 RLS/GRANT/trigger/function 才能决定最小实现。与设计稿“记忆变更与事件追加同一事务”相比，当前多次 REST 请求不构成事务，需先定义失败后的账本语义/补偿策略，再设计代码改动。

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
- 2026-10-27：v1.3 补充证据：更新 PATCH 只按 id 过滤，未按 oldVersion 做 compare-and-swap；并发更新可能覆盖并产生重复的 resulting version。此处仅为源码静态结论，不是并发行为测试。
- 2026-10-27：v1.4 补全写入口审计：data.js import 复用 putMemory；category.js legacy move_category 与通用 supabase_db/exec 可能绕开 memory_unified 事件写入；当前 registry/实际 DB 权限决定其真实可达性仍需核实。已在记忆表设计 v1.5 形成事务一致性规格提案；无 Worker/DB/schema 写入。
- 2026-10-27：v1.5 重新读取公开 OpenAPI schema_dump 并补充 database-overview v2.3：确认当前 memories 与 memory_events 列类型/FK片段，未确认 trigger/RLS/GRANT/唯一约束/删除行为；没有执行数据库写入或真实 SQL/DDL。
- 2026-10-27：v1.6 排查现有只读查询通路：exec_sql 拒绝 catalog-only SELECT；PostgREST query 对 information_schema.triggers、pg_catalog.pg_trigger、pg_indexes 均返回 PGRST205；已检查的 migration 目录没有 memory_events trigger/function migration。没有数据库写入、DDL 或代码改动；需要另一个获准的只读数据库通道，才能证实真实 trigger/RLS/GRANT/约束状态。
- 2026-09-09：v1（2026-09-09 实测）
