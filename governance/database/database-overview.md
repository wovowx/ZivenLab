# 数据库总览（Database Overview）· v2 · 2026-10-20

> **数据源唯一**：所有表都在 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`），承载 mcp-memory Worker。不搞多库、不另起数据源。
>
> **维护闭环（2026-10-20 与 GPT 讨论收敛，柳柳拍板 P0 落地）**：分三层建立持续可核验的闭环，而不是一次写厚文档——
> - **现状层**：`dump_schema` 可生成 md/json 结构快照；本文记录的 23 表是 2026-10-20 历史快照。2026-10-23 通过表清单工具观察到 25 张表，其中包含 `sb1_0_test_memories` 与 `sb1_0_test_memory_events` 两张测试表；这不是同一统计口径下的已重跑 schema dump，后续应重新生成机器快照再逐项对齐。
> - **解释层**：本文件即为每张表的业务字典（purpose/owner/used_by/lifecycle/relationships/source_status），未知项明确标 `unknown`，不编造。
> - **历史层**：`change-log.md`（待 P0 后随手起）+ 复用现有治理记录（需求/决策/执行/PR），只做索引链接，不复制第二份事实。
>
> **表数统计以最新机器快照为准，不手写总数**。本文表字典沿用 2026-10-20 的 23 表业务口径；2026-10-23 另一次表清单观察到 25 张（含两张 `sb1_0_test_*` 测试表）。在重新生成 `schema_dump` 并逐表核对前，不把两种结果直接判定为数据库漂移或误建表。

## 表字典（2026-10-20 历史业务表字典；当前 25 张表清单待逐表重核）

> 字段说明：`used_by` = 实际使用该表的 Worker 工具/路由/模块（**source_status=verified 表示已由代码检索核实；guess/unknown 表示待核**）；`owner` = 负责维护该表的模块/负责人（不是「谁最近碰过」）；`lifecycle` = active / paused / deprecated / pending-confirmation。

### memory 域（记忆体系 · active）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| memories | memory | 记忆管理 skill / memory 工具 | 记忆条目主表（2026-10-17 升级 type/status/version/supersedes_id/source_ref/valid_from-to，当前有效判定） | supersedes_id 自关联；alias→memory_aliases | verified |
| memory_events | memory | 记忆/审计 | 记忆变更账本（追加式，禁 UPDATE/DELETE，可追溯每次记忆演化） | →memories | verified |
| memory_aliases | memory | memory search 检索 | 检索别名索引（多钥匙：一条记忆多入口） | →memories | verified |

### chatroom 域（聊天室 · 方向暂停，paused 保留）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| chat_threads | chatroom | 聊天室/上下文 | 聊天线程（项目/话题） | ←chat_messages | verified |
| chat_messages | chatroom | 聊天室/执行框 | 消息本体（多 Agent 文本+元数据） | →chat_threads | verified |
| chat_agent_events | chatroom | 聊天室/事件驱动 | Agent 动作事件（claim/状态/投递） | →chat_messages | verified |
| thread_members | chatroom | 聊天室 | 线程成员（**空表**，无 DDL 存档待补） | →chat_threads | guess |
| thread_contexts | chatroom | 上下文 Worker | 线程上下文快照 | →chat_threads | verified |
| agent_chat_state | chatroom | 聊天室 | 各 Agent 消费游标 | | verified |
| thread_message_counter | chatroom | 聊天室 | 线程消息序号计数器 | →chat_threads | verified |

### execution 域（执行会话 · active）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| execution | execution | 执行 GPT | 执行会话主表 | ←execution_runs | verified |
| execution_runs | execution | 执行 GPT | 每次执行 run | →execution | verified |
| conversation_bindings | execution | 执行框/路由 | GPT 会话↔线程绑定 | | verified |
| conversation_binding_events | execution | 执行框 | 绑定变更审计 | →conversation_bindings | guess |

### collaboration 域（治理/讨论 · active）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| decision | collaboration | 决策 workflow | 决策记录 | | verified |
| discussion_evidence | collaboration | 讨论治理 | 讨论证据链（含硬 guard 设计讨论的 1 条关键记录，有历史价值不删） | | verified |
| patch_proposals | collaboration | Patch Engine/权限 | Patch Proposal（proposed→reviewed→approved→applied） | | verified |

### platform 域（平台/权限 · active）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| actors | platform | 全系统 | Agent 身份注册（system/ziven/gpt/liuliu…） | | verified |
| skills | platform | 全系统 | MCP 技能注册（68 个） | | verified |
| tool_policies | platform | permission | 工具权限策略（github_push/merge 等审批） | | verified |
| system_config | platform | 配置系统 | 系统 KV 配置（如 operit_tunnel_url/bearer_token） | | verified |
| chat_webhook_audit | chatroom | webhook | webhook 投递审计（聊天室暂停范围） | →chat_agent_events | verified |

### files 域（上传文件 · active，具体使用状态待核）

| 表名 | owner | used_by | purpose | relationships | source_status |
|---|---|---|---|---|---|
| files | files/storage | `/upload` 与 `src/utils/storage.js` | 上传文件元数据；对象存储写入与元数据写入需一起验证 | 与 Supabase Storage 对象对应 | verified |

> 备注：`knowledge` 不在当前实际表清单中，不再当作现存表描述；代码/文档是否仍有引用需单独核对。2026-10-23 表清单另外观察到 `sb1_0_test_memories`、`sb1_0_test_memory_events` 两张测试表，尚未核清创建来源与用途；本字典没有将其混入 2026-10-20 的 23 张业务表历史快照。

## P1 触发判据（什么时候进入 P1：change-log 完整化 + Supabase CLI 版本化迁移）

> P0（本文件校准 + dump_schema）落地后，P1 不在固定时间点，而是**满足任一判据即触发**；触发即进入「先补 change-log 完整化 → 建 Supabase CLI 初始迁移基线 → 之后 DDL 全走版本化 SQL」。

| 判据 | 说明 |
|---|---|
| **① 结构漂移发生** | `dump_schema` 检测到「数据库实际结构与已核对基线不一致、且无法用手工说明对齐」——说明需要版本化迁移来锁定事实 |
| **② 变更频率上升** | 一个月内 ≥3 次有业务意义的表/字段变更，且开始靠记忆记不牢 |
| **③ 规模/协作扩大** | 表数 >30，或出现「多项目/多 Agent 依赖同一库、需要复现结构」 |
| **④ 时间轴自动化需求** | 柳柳/哥哥要的「项目时间轴回顾」从查 main 记录升级到「需自动查某表历次变更」，change-log 满足不了 |

> 记录说明：本项目（数据库管理规范化 / P0+P1）的相关信息记于：本文件（现状+解释）、`change-log.md`（历史索引，P0 后随手起）、驾驶舱 `当前项目状态.md`（进度）、记忆 `⚙️/柳柳愿景·项目时间轴星系回顾`（柳柳的原始诉求）。P1 判据满足时在驾驶舱 + change-log 同步标记触发。

## 变更记录
- 2026-09-09：v1 初版（柳柳拍板数据库治理 v1）。
- 2026-10-20：v2 校准到实测 23 表 + 每表字典（purpose/owner/used_by/lifecycle/relationships/source_status）+ 定义 P1 触发判据 + 明确维护闭环三层。来源：柳柳提「数据库管理规范化」→ 与 GPT 有来有回收敛 → 柳柳拍板 P0。

*创建 v1 2026-09-09；v2 校准 2026-10-20（Ziven 落，GPT 讨论，柳柳拍板）。*