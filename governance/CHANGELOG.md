# ZivenLab CHANGELOG（文档仓 · 知识快照）

> 文档仓不假装软件发行版：版本模型 = 知识快照 `docs-YYYY.MM(.N)`（可带 baseline/snapshot 后缀）。
> 记录：知识演进（新增/决策/归档），不记每个 commit。
> 本文件已迁移至 governance/（2026-09-04 governance 目录重组）。

## [docs-2026.10.2] - 2026-10-26（dev 草稿，未发布）

### 整体架构目标定案（2026-10-26）
- 定案：六阶段整体架构升级以「像一本好书」为目标，代码复用、职责清晰、面向真实需求的可扩展性与回归保护是贯穿全程的硬性原则，不新增第七阶段。
- 明确五类工程检查：先复用再新增；职责相近才合并；沿现有清晰边界扩展且不预建万能框架；先核依赖再做最小可逆调整；以真实检查和回归证据保护既有行为。
- 阶段 2 于 2026-10-26 完成：在 `真相源导航表.md` v1.4 内复用现有导航表建立 10 章总目录与章节职责地图，由 `governance/README.md` 提供唯一入口；同步 roadmap、驾驶舱、现状架构、资产整理计划与差距矩阵。当前下一阶段为阶段 3「真实实现与依赖地图」。只更新 dev 治理文档，未改生产代码、数据库或部署。

### 第一阶段：现状基线与权威来源对齐
- 更新 `现状架构.md`、`架构差距矩阵.md`、`真相源导航表.md`、`roadmap.md`、`当前项目状态.md` 与 `资产盘点与整理升级计划.md`，统一当前主线为「一本好书式架构」的第一阶段基线校正。
- 根据实际仓库读取，确认 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 位于仓库根目录且可读取，纠正历史文档中已过期的 Not Found/待重建说法；记录桥接文档内旧状态重复与当前任务口径漂移，不删除历史内容。
- 根据实际目录校正 mcp-memory 根 README 的目录与入口说明；该 README 修订仅在 `mcp-memory/dev`，尚未合并到 main。
- 将 `buildErrorResponse` 重复导出从待处理候选改为已完成事项：其删除已包含在 mcp-memory `v6.35.0`，既有 E1/E2 证据分别记录，不把本次文档整理冒充为新测试。
- `mcp-memory v6.35.0` main HEAD `71f6a03ebc81` 对应 Cloudflare deployment `c78ab839`，`verify_main=true` 返回 `VERIFIED`；本条文档草稿不推 main、不改生产代码、数据库或部署。
- 阶段 1 完成后形成的阶段 2 候选任务，已于 2026-10-26 通过复用现有导航表完成；下一阶段转为沿真实调用链核对模块依赖与扩展瓶颈。

**发布状态：未发布，保留在 ZivenLab/dev，须经差异复核并由柳柳明确同意后才能合并 main。**

## [docs-2026.10.1] - 2026-10-23（已发布）

### 真相源权威范围澄清（2026-10-23）
- 明确 ZivenLab 是系统级治理文档集中入口，不是所有事实的统一存储库。
- 按事实类别划定权威来源：组件实现看对应仓库源码/注册/测试证据；数据库结构看实时 Schema；身份根与唯一权威当前工作状态分别看云端 `🧬/我是谁`、`⚙️/当前工作检查点`；恢复流程看云端 Session Bootstrap 协议。
- ZivenLab 驾驶舱是项目治理视图，不得与云端工作检查点形成平行状态副本。
- 区分已定义、已接入、已验证；治理文档存在不等于规则已在 Runtime 生效。
- 仅更新治理文档，未改生产代码、数据库或部署。该快照已通过 PR #74 squash 合并至 main，合并提交标题为 `v2026.10.1: 架构真相源与验证基线快照`；合并后 main 与 dev 已核验一致。

### 本次快照范围
- 将目标蓝图与真实现状拆分：新增 `governance/现状架构.md`，并建立 `governance/架构差距矩阵.md`。
- 对齐真相源导航、README、roadmap、驾驶舱、资产全景、数据库治理文档与资产整理计划，明确当前活跃主线和新会话恢复顺序。
- 固化 `search_history/suggest` 的行为测试契约、证据标准及跨宿主交接文件路径未确认的阻塞事实。
- 记录已知风险与未验证项；不包含生产代码、数据库结构、部署或 Worker 行为变更。

### 发布边界
- `ZivenLab/dev` 相对 `main` 的 GitHub compare 显示领先超过 100 个提交、behind 0；15 个变化文件全部是 `governance/` 治理/架构文档。`wovowx/mcp-memory` 的 `dev` 与 `main` 当前 identical（0/0）。此处记录的是本次发布核查快照，合并前仍须重新 compare。
- 为避免将大量开发提交历史逐条搬入 main，本候选建议采用 **squash 为一个文档快照提交**；合并前须再次核对 PR 文件清单，合并后验证 main 与 dev 收敛。
- 发布状态：已发布至 GitHub main；不触发 Cloudflare/Worker 部署。本条为文档快照，不代表生产软件版本升级。

## [docs-2026.10] - 2026-10-23

### 校正（跨宿主交接状态）
- 回读现状架构时发现旧文档把 `mcp-memory/dev/CROSS-HOST-BRIDGE.md` 描述为可用交接入口，但本次 GitHub 读取返回 Not Found，且 dev 根目录目录清单未显示该文件。已同步修正现状架构、差距矩阵、roadmap 与驾驶舱。差距矩阵进一步固化 search_history/suggest 的逐场景 mock 执行契约与证据要求；交接入口恢复前不声称已交付 Operit 或测试通过。

### 新增（现状架构真相源）
- 新增 `governance/现状架构.md`，记录仓库/服务全景、Worker/MCP 入口、记忆与数据库现状、宿主能力边界、已知差距、证据等级及新会话恢复顺序；明确区分源码事实、注册/数据事实、运行时证据与待验证项。
- `governance/真相源导航表.md` 与 `governance/README.md` 增加现状架构入口，并把 `整体架构.md` 明确为目标蓝图；当前实现与目标规划不混写。
- 新增 `governance/架构差距矩阵.md`，将已发现事项按证据、风险、处理方式、验收条件和状态收敛；明确 search_history/suggest 先补行为测试、迁移审计先定义失败场景、Pages 与 /memory-universe 保持待验证/启用前阻断，不擅自改生产代码或数据库。

### 校正（架构存量整理与真相源对齐）
- `roadmap.md` 增加当前活跃主线：阶段 0 架构盘点已完成，按资产整理计划依次校正文档真相源、评估已证实依赖断链、核对职责重叠、补验证基线；旧聊天室/Wake Bridge 路线标为历史待办，不再覆盖当前主线。
- `governance/README.md` 与 `资产全景.md` 修正过期目录示意和治理文件计数，改为指向实时目录及真相源导航表；`真相源导航表.md` 补齐 roadmap、CHANGELOG、治理入口和数据库总览/Schema 规范/域文档导航。
- 实时 `skills` 注册表确认 `memory` 工具仍启用且公开 `action=suggest` 与 `action=move`；由于无按 action 的使用统计，搜索历史/建议暂按需兼容功能处理，不推断为可删除。静态检查发现 suggest 空态兜底因字符串拼接优先顺序失效；GPT 侧 Code Runner 当前不支持 JS handler，故登记测试缺口，不声称行为测试通过或已修复。另澄清独立 `memory_move` 别名未注册，但统一 `memory(action=move)` 仍是已登记入口。
- 静态 import 头部核对未发现任何当前 `src/` 文件从 `helpers.js` 导入重复的 `buildErrorResponse`；由于无法运行机器级全仓搜索/测试，该函数只列为冗余候选，未删除。
- 数据库治理文档校正：`change-log.md` 已存在，不再写成待建立；2026-10-23 实际重跑 `supabase_schema action=schema_dump`，返回 25 张表（23 业务 + 2 测试），与文档分类口径相符。`database-overview.md` 与 `schema-policy.md` 明确区分可请求 schema dump 与尚未验证的自动落盘/CI 漂移检测；RLS、全部约束和测试表来源仍待核。
- `/memory-universe` 未认证路由风险保留记录，但依据柳柳确认该页面未投入使用、属于半成品，调整为正式启用前阻断验收项；本轮不改代码、不停服务、不部署。
- Pages 工作流仍只确认静态配置，是否实际部署、当前站点可见性与访问范围尚未核实；不据此擅自停用或修改发布流程。
- 本批文档改动仅在 ZivenLab `dev`，已通过 GitHub 写入后回读校验；未合并、未推送 `main`。

## [docs-2026.09.3] - 2026-09-09

### 新增（数据库治理第二批 · 5 个 domain 数据模型）
- governance/database/domains/ 下 5 个域文档：chatroom（7 表）/ execution（4 表）/ memory（2 表）/ collaboration（2 表）/ platform（5 表）
- 每个文档含：表清单 + 各表字段（列/类型/含义）+ 关系 + 典型流程 + 常见坑 + 变更记录
- 目的：查任何表结构开文档即知，不再逐张现查（柳柳 2026-09-09 提出「每次都要重新查数据结构」痛点）

### 更新（conversation_bindings 健康字段 · M1.3）
- execution domain 文档补 5 列：health（unknown/healthy/stale/failed）+ last_checked_at + last_success_at + last_failure_at + check_count
- 健康语义定稿（Ziven + GPT 讨论，柳柳拍板）：status（生命周期）与 health（健康）正交；bind=unknown，首次真实成功调用→healthy，失败→failed+switch_candidate（不自动换档）；查询无副作用
- 代码侧：execution_session_manager v6.32.14（MCP 代码仓），表结构 ALTER 已完成

### 决策
- 数据模型与表结构声明文档化：database-overview 是「过一遍现有表」依据（Table Change Guard）
- 遗留待办：execution/thread_members 空表结构待补、knowledge 疑似废弃待确认（等 schema_dump 工具上线后快照覆盖）

## [docs-2026.09.2] - 2026-09-09

### 新增（数据库治理第一批 · 骨架 + 总纲）
- governance/database/database-overview.md：21 张表全登记（domain/owner/used_by/一句话用途）+ 字段速查
- governance/database/schema-policy.md：Schema 治理铁律（Table Change Guard：加表/改表必须过现有表 + necessity 必要性证明）
- policy-index 加 Database Guard 规范行（规范要被找到才生效）

### 决策
- 数据库治理方案 v1（Ziven + GPT 两轮讨论收敛，柳柳拍板）：Supabase 唯一数据源 + 五大 domain + 每表登记 domain/owner/used_by + 机器保证 schema snapshot 自动生成 + 人工维护语义文档
- 双仓分工：文档（ZivenLab/governance/database/）存「是什么/为什么」，脚本（mcp-memory）存「怎么生成」

### 新增
- governance/ 治理层目录（推进唯一依据声明 + README index）
- 架构蓝图：Agent Operating System（从「会记事的 Agent」→「不依赖记性的 Runtime」）
  - P1 release_guard（第一个 Runtime Guard 样板）
  - P2.1 Capability Access（GPT 只读通道）/ P2.2 Permission Model（L0-L3）
  - P3 Workspace State Runtime / P4 Patch Engine
- 铁律：知识≠生效，没进 Runtime 生效路径 = 不存在（架构第一性原则）

### 决策
- 权威文档与历史分层：governance/ 只放规矩，common-ground/ 留历史草稿
- 引用规范：权威文档互引用路径（governance/roadmap.md），不写「85号」这种名字
- 推进唯一依据：当前做什么→roadmap / 系统现状→驾驶舱 / 怎么协作→协作协议

### 归档
- 驾驶舱/85号/协作协议 从 common-ground/ 复制到 governance/（旧位置留 redirect）

## [docs-2026.09] - 2026-09-04 (baseline)

首次建立规范化文档版本基线（baseline snapshot：截止此刻，系统进入版本化管理状态）。

### 新增
- 当前项目状态驾驶舱（P0-5，含入口导航/真相源/资产清单/生产入口唯一性/发布状态）
- 协作协议 v4.2（讨论与分工规则 + 协议部署原则 + 铁律6）
- 85 号行动总清单（唯一总控台，last_sync 追踪，不挂版本号）
- 本 CHANGELOG（docs-2026.09 baseline）

### 决策
- Runtime 规则分层：协议文档=权威 / Runtime=行为闸门 / Router=执行约束 / 驾驶舱=导航
- workspace_rules 三方公共规则层设计（P1-12）
- 发布纪律双仓模型：本仓 docs-YYYY.MM，代码仓 vX.Y.Z（GPT #505~508）

### 归档
- legacy 资产治理流程（chat_webhook poc / github.js replaced / 00~85 历史讨论待 decision 层）

---

*由 Ziven 维护。活文档：每次知识级变更追加条目，不覆盖历史。*

## [docs-2026.09.1] - 2026-09-04

### 新增
- governance/ 治理层目录（推进唯一依据声明 + README index）
- 架构蓝图：Agent Operating System（从「会记事的 Agent」→「不依赖记性的 Runtime」）
  - P1 release_guard（第一个 Runtime Guard 样板）
  - P2.1 Capability Access（GPT 只读通道）/ P2.2 Permission Model（L0-L3）
  - P3 Workspace State Runtime / P4 Patch Engine
- 铁律：知识≠生效，没进 Runtime 生效路径 = 不存在（架构第一性原则）

### 决策
- 权威文档与历史分层：governance/ 只放规矩，common-ground/ 留历史草稿
- 引用规范：权威文档互引用路径（governance/roadmap.md），不写「85号」这种名字
- 推进唯一依据：当前做什么→roadmap / 系统现状→驾驶舱 / 怎么协作→协作协议

### 归档
- 驾驶舱/85号/协作协议 从 common-ground/ 复制到 governance/（旧位置留 redirect）

## [docs-2026.09] - 2026-09-04 (baseline)

首次建立规范化文档版本基线（baseline snapshot：截止此刻，系统进入版本化管理状态）。

### 新增
- 当前项目状态驾驶舱（P0-5，含入口导航/真相源/资产清单/生产入口唯一性/发布状态）
- 协作协议 v4.2（讨论与分工规则 + 协议部署原则 + 铁律6）
- 85 号行动总清单（唯一总控台，last_sync 追踪，不挂版本号）
- 本 CHANGELOG（docs-2026.09 baseline）

### 决策
- Runtime 规则分层：协议文档=权威 / Runtime=行为闸门 / Router=执行约束 / 驾驶舱=导航
- workspace_rules 三方公共规则层设计（P1-12）
- 发布纪律双仓模型：本仓 docs-YYYY.MM，代码仓 vX.Y.Z（GPT #505~508）

### 归档
- legacy 资产治理流程（chat_webhook poc / github.js replaced / 00~85 历史讨论待 decision 层）

---

*由 Ziven 维护。活文档：每次知识级变更追加条目，不覆盖历史。*