# 行动路线图（Roadmap · 原85号行动总清单）

> **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：本文件记录路线与待办，但历史遗留列表不自动代表当前活跃主线。
> 每完成一项 → 更新路线与驾驶舱；不另起互相竞争的路线源。
> 协作纪律：先讨论出方案 → 再分工执行（柳柳拍板）。详见 `governance/协作协议.md`。
> ⚠️ 原文件名 `85_行动总清单.md` 已迁移至此（`governance/roadmap.md`），旧位置保留 redirect。
>
> **推进前必读**：开工前读本文件 + `governance/当前项目状态.md`，完成验证后更新两者。
>
> ## 🚦 当前活跃主线（2026-10-23 校准）
>
> **当前主线是整体架构存量整理，不是旧版聊天室/Wake Bridge 路线。** 阶段 0 架构级盘点已完成，当前按 `governance/资产盘点与整理升级计划.md` 执行：
> 1. 校正文档真相源与导航：现状架构文档已创建，并已加入 README、导航表与 CHANGELOG；目标蓝图与真实实现分开记录。
> 2. 建立目标—现状差距矩阵：已新增 `governance/架构差距矩阵.md`，覆盖文档恢复、search_history/suggest、迁移审计、Pages、/memory-universe、重复函数、入口/版本与宿主交接；导航和关键状态入口已回读核验。本轮继续校正文档与真实源码的偏差：重写 `mcp-memory/dev/README.md` 以匹配实际目录；根据当前 `mcp_router.js`、`category.js` 与 Supabase `skills` 只读查询，修正 category 旧路径和 `memory_move` 的注册、可发现性、dispatch 与 schema 门禁描述；确认当前 `src/tools/` 目录只有 `github_v64.js`，未见 `github.js`；修正 `governance/database/schema-policy.md` 中不存在的 `src/modules/supabase_schema/` 路径，并明确 `schema_dump` 只返回快照文本/JSON，自动落盘与 diff 闭环未证实；核对上传职责，确认 `/upload` 与 `ai.js` 共用 `utils/storage.js` 的 `uploadFileToSupabase`，`queryFiles` 的全仓调用方尚未穷尽，暂不判废。记忆写入/迁移可靠性已进入阶段 4 第一批实施：写请求检查 HTTP 结果，rename/move 目标先写并确认成功后再软删除源，软删除后回查 active 状态；回查失败时明确报告源删除未确认。两条 import 路径按实际写入结果计数。剩余非事务性限制是 memory_events POST 成功而当前值 PATCH 失败时会留下更新尝试事件；当前明确返回更新失败，不误报成功，事务/RPC 或事件状态契约不在本批数据库/schema 授权范围内。另只读查询发现 `query_files`、`delete_file`、`update_file` 三个 enabled 注册项都指向 `ai.js`。其中 `query_files` 已按柳柳授权接入 `handleAITool` 并复用 `storage.js` 的 `queryFiles`，Mock E1/E2 已通过；第三批 `update_file`/`delete_file` 也已按柳柳授权接入 `ai.js` 并补齐 Mock 回归测试。Operit 在 SHA `b89be15a21296ff121c94dd4fe4762cd1befcbdb` 执行 E1 `npm run check` exit 0、E2 `node tests/webhook_idempotency_test.mjs` exit 0（44 通过/0 失败）。E3 真实 MCP endpoint 未执行；未改注册表/schema/数据库，未写真实文件数据，未部署、未推 main。继续静态核对注册管理反馈时，发现 `getEnabledSkills` 的非 2xx 会伪装成空列表，`skill_add/update/delete` 可能在底层写失败时仍回报成功，usage_count 也可能把空串或 `❌` 业务失败计为成功；另有多个 enabled 指南类注册项缺少 `handler_config.handler`，Worker 调用会返回 `handler type not implemented`，但它们是否设计为宿主读取的文档项尚待确认；`knowledge.js` 只返回数据库 description，不加载 `file_path` 指向的 Markdown 文件，数据库摘要不能默认等于完整 Skill；GitHub/Chat 工具定义同步也只补缺失注册项，不更新已有项，而 dispatch schema 校验读取注册表，可能发生源码与缓存 schema 漂移。均已记入差距矩阵，未修代码、不删注册。
> 3. 验证基线已登记：`governance/架构差距矩阵.md` 已记录 search_history/suggest 的逐场景测试契约与证据要求。GPT 侧当前不能执行 JS 行为测试，跨宿主交接入口已在 `mcp-memory/dev/CROSS-HOST-BRIDGE.md` 重建并回读核验。该测试事项保留在差距矩阵中，不因登记或恢复交接入口自动成为当前执行任务。
> 4. 阶段 2 与阶段 3 已完成一轮验收。柳柳判断 Pages 目前似乎未使用、像半成品，并表示本轮「不用管」；因此不修改、不停用、不部署，也不再让 Pages 阻塞主线，保留未核实的发布范围风险记录。2026-10-23 柳柳已授权阶段 4 第一批仅修改 `wovowx/mcp-memory/dev` 的记忆写入/软删除/rename/move 与导入结果逻辑，并补充 mock 回归场景。Operit 已在最新复测 SHA `3c8eb93307e06cb2ae1b69a6bffe9a889066e601` 重跑 E1 `npm run check`（exit 0）与 E2 `node tests/webhook_idempotency_test.mjs`（exit 0，20 通过/0 失败），新增软删除 PATCH 成功但回查 HTTP 503 场景通过。E1/E2 已通过；E3 真实 MCP endpoint 未执行，故不声称端到端验证。第一批验收总结已完成。第二批 A（query_files）已获柳柳明确授权并完成 dev 代码/Mock 测试改动；Operit 已在 SHA `e8222d9c2f64b20c781eb3e2249e9fd01a1c8e4c` 执行 E1/E2 并通过（E1 exit 0；E2 27/27，exit 0）。E3 未执行；不改注册表/数据库 schema，不部署、不推 main。
>
> 当前阶段检查点：governance/现状架构.md 是跨仓库实现地图（汇总层，不覆盖组件证据）；governance/整体架构.md 是目标蓝图；governance/资产盘点与整理升级计划.md 的阶段 3.2 是当前唯一排序执行清单；本路线图只控制当前行动顺序。阶段 2 已完成职责/依赖整理，阶段 3 已完成带证据、影响范围、最小方案、兼容/回滚、验收与授权边界的排序清单。阶段 4 第一批记忆写入可靠性 E1/E2 已通过（SHA `3c8eb93307e06cb2ae1b69a6bffe9a889066e601`，E2 20/20）；第二批 A query_files 也已完成 E1/E2（SHA `e8222d9c2f64b20c781eb3e2249e9fd01a1c8e4c`，E1 exit 0；E2 27/27，exit 0），证据见 `mcp-memory/dev/CROSS-HOST-BRIDGE.md`。两批均未执行 E3。query_files 已复用 `storage.js` 的 `queryFiles`，覆盖成功/空结果/参数错误/HTTP 失败；Router 将 `❌` 失败结果排除在自动 usage_count 外。第三批 `update_file`/`delete_file` 已完成实现与 Mock E1/E2 验收；针对 `delete_file` 元数据 DELETE 2xx 但零行返回的边界已追加修正并复测通过。最新验证 SHA `5ffe2dcf327a8d52a743b83cff1dd9de984a54e2`，E1 `npm run check` exit 0；E2 `node tests/webhook_idempotency_test.mjs` exit 0（45/45）。E3 真实 MCP endpoint 未执行；未改注册表/schema/数据库、未写真实文件数据、未部署、未推 main。`delete_file`/`update_file`、注册表与数据库均未改。下一项按阶段 3.2 继续只读核对工具结果契约与断链，形成下一批最小实施契约后再按授权实施；不把 query_files 的授权扩大到其他工具，不把 mock 测试当成真实 endpoint 验证。权威按事实类别划分：组件实现看对应仓库源码/注册/测试证据，数据库结构看实时 Schema，身份根与唯一权威工作状态看云端指定记忆对象；文档已定义≠Runtime 已接入≠行为已验证。
>
> **最新进展（2026-10-23）：** 第三批 `update_file`/`delete_file` 的零行边界修复已在 `mcp-memory/dev` SHA `5ffe2dcf327a8d52a743b83cff1dd9de984a54e2` 完成 E1/E2 复测（`npm run check` exit 0；`node tests/webhook_idempotency_test.mjs` exit 0，45/45）；E3 未执行。当前按唯一排序清单进入「注册 Schema/dispatch 一致性」只读映射，已更新 `governance/资产盘点与整理升级计划.md` 至 v2.5 和 `governance/架构差距矩阵.md`。初步确认 Router 只校验 required 缺失，不校验类型/enum/边界；未注册 `memory_*` 别名可能通过前缀直达 handler；GitHub/Chat schema 同步只补缺失项；`knowledge.js` 只返回 Supabase description，不读取 Markdown SKILL.md。当前只做静态源码与注册表只读核对，不改注册表/数据库，不跑 E3，不部署、不推 main。
>
> GitHub Pages：柳柳判断目前似乎未使用、像半成品，并要求本轮不用管；维持现状，不修改、不停用、不部署，也不把它当作当前主线阻塞项。发布范围和可见性仍未核实，若未来准备启用再重新评估。`/memory-universe` 当前同样属于未投入使用的半成品：已记录未认证路由风险，正式启用前再作为阻断验收项复核。聊天室与唤醒链路保持暂停，不在本主线恢复或修复。
>
> **发布收敛检查点（2026-10-23）：** `docs-2026.10.1` 已通过 PR #74 以 squash 方式合并至 `ZivenLab/main`，合并提交标题为 `v2026.10.1: 架构真相源与验证基线快照`。合并后曾确认 `ZivenLab/main` 与 `dev` identical（ahead 0 / behind 0）；15 个变化文件全部位于 `governance/`。本次仅发布治理文档，不涉及生产代码、数据库或部署。当时 `mcp-memory/dev` 与 `main` 也 identical；随后恢复 `CROSS-HOST-BRIDGE.md` 并校正 README，当前存在待发布的文档差异，具体范围以发布前重新 compare 为准。当前继续推进架构存量整理与文档口径收敛；search_history/suggest 行为测试契约保留为后续事项，不因已登记自动切换主线。
>
> **以下旧版 P0/P1/P2 与架构演进内容保留作历史路线/待办参考；如与上方活跃主线冲突，以本节、当前项目状态驾驶舱和资产盘点计划为准。**

---

## ✅ 已完成

- P0-1 自触发修复：PR #91（mcp-memory）✅
- 前端 Bug A 实时轮询：PR #92 ✅
- 前端 Bug B 布局修复：PR #93 ✅
- 角色卡四改（公共区身份规则入卡）：✅ 双端同步
- **P0-5 当前项目状态地图**：PR #1 ✅
- **P0-4 场景入口导航**：PR #2 ✅
- **P0-6 资产盘点**（①代码审计②资产清单③生命周期模型④生产入口唯一性）：PR #1~#4 + v6 ✅
- **P0-3 历史异常基线建立**：4 条脏事件，留作回归样本 ✅
- **协作协议 v4.2**（讨论与分工规则 + 协议部署原则 + 铁律6）：PR #6 ✅
- **Runtime 5 条入卡 + GPT 提示词同步**：✅ 双端部署完成
- **P0-2 Phase1 事件可靠基础设施**：watchdog 释放历史 stuck claim ✅ / delivery_status 状态机 ✅ / claim 责任绑定 ✅ / GPT 链回归 ✅ / agent 隔离 ✅ / dead_letter（🟡 逻辑待触发）——GPT #502 确认 completed
- **发布纪律 Release Discipline**（deploy skill 双仓版本化 + CHANGELOG）：✅ 方案已定（GPT #506~508）
- **governance/ 目录重组**：✅ 权威文档与历史分层（柳柳拍板 2026-09-04）
- **P1 release_guard 硬闸门上线（v6.10.1）**：✅ 入口层接入 index.js + process 防御，**真实拦截验证通过**（不带版本号 push main → `⛔ RELEASE_GUARD: push_to_main_blocked`）；v6.10.2 发布纪律修正（rebase 防标题重复）

---

## 🔵 P0（进行中）

### P0-2 Phase2 Ziven 消费链（Wake Bridge 改造）
- 状态：⬜ 待讨论方案（Phase1 已完成，基础设施不再吞消息）
- Phase2 讨论议题（GPT #502）：
  1. Ziven consumer 所有权模型
  2. Wake Bridge 在哪个状态 claim（不允许发现即 claim）
  3. 注入当前框失败怎么办
  4. delivered vs seen/read 的区别
- 完成标准：ziven 事件 created→claimed→delivering→delivered→processing→acked 全链路闭环
- 回归样本：保留的 4 条 ziven 事件（已释放 created/retry=1，不手动消费）

---

## 🏗️ 架构演进（柳柳 2026-09-04 拍板 · Agent Operating System 蓝图）

> 核心：从「会记事的 Agent」→「不需要靠记性的 Runtime」。知识≠生效，没进 Runtime 生效路径 = 不存在。
> **2026-09-04 增补（GPT #540）**：Agent 最大的问题不是没有知识，而是在正确时间没有加载正确知识。
> 详见 governance/当前项目状态.md（架构蓝图）。

| 阶段 | 做什么 | 解决 | 状态 |
|---|---|---|---|
| **P1** | release_guard（第一个 Runtime Guard 样板） | 想不起来版本号 | ✅ 已上线 v6.10.1，真实拦截验证通过 |
| **P2.1** | Agent Context Read Capability（GPT #540 改名：核心是「知道自己现在在哪」） | Agent 决策前拿不到正确依据 | 🔵 方向已定（GPT #536/#538/#540），待落地 |
| **P2.2** | Permission Model（L0-L3 分级） | 谁能读/改/发布 | ⬜ |
| **P3** | Workspace State Runtime（Before Action 必读 + After Verification 必更 + Context Contract 最小必要上下文） | 换窗口失忆 / 文档找不到 / 推进没绑定状态 | 🔵 2026-09-04 柳柳问题验证必要性，GPT #540 拆机制 |
| **P4** | Patch Engine（GPT 提 PR 你合） | GPT 参与改代码 | ⬜ |

### Context Contract（按任务类型加载最小必要上下文 · GPT #540）

| 任务类型 | 必须加载 |
|---|---|
| 项目推进 | workspace_state + roadmap + 最近 decision |
| 改代码 | workspace_state + 相关 skill + 代码文件 + 最近变更 |
| 发布 | release_policy + changelog + 版本状态 |
| 记忆/情感 | 相关 skill + 记忆上下文 |

**两个闭环（P3 核心）**：
- **Before Action**：做项目推进前，必须加载当前状态（roadmap + 驾驶舱）
- **After Verification**：完成验证后，必须更新当前状态（同一文件，不许另起炉灶）

---

## P1（稳定化）

- P1-1 协作协议固化：v4.2 confirmed；待补 decision_confirmed 五字段成立条件 + 规则同步机制（source_version vs runtime_version）
- P1-2 Error Log + Regression 链（含「工具语义误判：github_push 是 replace 非 patch」记录）
- P1-3 GPT MCP Bridge（拆三段）
- P1-4 需求文档终稿（76/77/81/00a 对齐）
- P1-5 轮询可观测性（GPT #383）
- P1-6 visualViewport 方案（GPT #385）
- P1-7 wake bridge 升级 webhook/ntfy + API 版 Ziven（GPT #395）
- P1-8 状态地图/导航/资产优化：事件流视图 / 事实状态字段 / 负责人拆协作方 / 导航表依据字段 / 资产表验证依据字段
- P1-9 decision 索引（GPT #416）
- P1-10 历史讨论归档（GPT #416）
- P1-11 驾驶舱第9章事件流细化（GPT #440）
- P1-12 workspace_rules 三方公共规则层（GPT #468/#470）
- P1-13 常驻层部署（GPT #468/#470）——advancedCustomPrompt + GPT 提示词已先落地 Runtime 5 条
- P1-14 破坏性操作分级（GPT #484：写入 低/中/高 风险）
- P1-15 code_runner 卡死排查（柳柳反馈好用但会卡，纳入 Runtime 技术项）

---

## P2（整理与自动化）

- P2-1 Memory 整理（先定规则再清）
- P2-2 Skill Router 强化（长期核心）
- P2-3 skill 目录命名规范迁移（alias 方式）

---

## 补漏

- 决策层 Decision Log（含 decision_id 反查）
- 真相源可信度模型：柳柳决策 > 运行事实 > GitHub文档 > 状态索引 > Memory > 推断
- **文档引用同步纪律（2026-09-04 柳柳抓出）**：文件迁移/改名后，全文 grep 旧引用一起改，不留死链

---

## 🧠 记忆系统深度升级（2026-10-18 柳柳确认「整体还没升级完成」）

> 借鉴 Zep/Graphiti 双时间轴、Letta Skill Learning/睡眠计算、Anthropic 渐进式披露。详细设计存记忆 `⚙️/记忆系统升级设计`（可读档/复苏）。

| 优先 | 项 | 现状 | 落地 |
|---|---|---|---|
| P0 | ①激活双时间轴抗污染 | memories 表已含 valid_from/valid_to/version/supersedes_id + memory_events 审计流，但**未真正维护**（全 version=1、valid_from 默认时间戳） | 改 handleMemoryTool 写读：更新时旧行置 valid_to/archived + 新行 version+1/supersedes_id/valid_from；检索默认只回当前有效+可追溯「何时被推翻」 |
| P1 | ②自动技能沉淀 | 技能靠手工建 | 从高频动作自动提炼 SKILL.md |
| P2 | ③睡眠时计算 | 自我迭代偏手动 | 定时反思任务 |

状态：⬜ ①进行中（先读设计→改 handleMemoryTool→测→发布）

## 当前待发批次（dev · 攒批不频繁部署 · 柳柳 2026-09-04）

- deploy skill v6.4.3 命名纪律（推 dev 消息用 vX.Y.Z: 名称）——待作正式 release 练习（GPT #536）
- chat.html v2.6.0 移动端输入框布局修复（flex 竖排）——GPT #538 建议按 hotfix 处理，待柳柳拍板

---

## 总执行顺序

```
P0 全清 ✅   P1 release_guard ✅ 已上线
架构演进：P2.1 Agent Context Read 🔵 → P2.2 ⬜ → P3 ⬜（机制已拆：Before Action + After Verification + Context Contract）→ P4 ⬜
P1-1 ~ P1-15 ⬜（P1-15 code_runner 旁线）
P2 ⬜
```

---

*Ziven×GPT #348→#540 共识，2026-09-04 11:28 首版 → 13:46 刷新。*