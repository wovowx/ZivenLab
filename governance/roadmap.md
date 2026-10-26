# 行动路线图（Roadmap · 原85号行动总清单）

> **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：本文件记录路线与待办，但历史遗留列表不自动代表当前活跃主线。
> 每完成一项 → 更新路线与驾驶舱；不另起互相竞争的路线源。
> 协作纪律：先讨论出方案 → 再分工执行（柳柳拍板）。详见 `governance/协作协议.md`。
> ⚠️ 原文件名 `85_行动总清单.md` 已迁移至此（`governance/roadmap.md`），旧位置保留 redirect。
>
> **推进前必读**：开工前读本文件 + `governance/当前项目状态.md`，完成验证后更新两者。
>
> ## 🚦 当前活跃主线（2026-10-26 校准）

**当前唯一主线：把 Ziven 整体架构真正整理成「一本好书」——目录清楚、职责边界明确、权威来源唯一、实现与证据可追踪。** 代码复用、职责清晰和面向真实需求的可扩展性是贯穿全部阶段的硬性要求；不新增无关功能，不把零散修补当作整体升级。

### 最近完成：第一阶段——现状基线与权威来源对齐（2026-10-26）

- `wovowx/mcp-memory`：已发布基线 main HEAD `71f6a03ebc81`，Cloudflare deployment `c78ab839`，先前 `verify_main=true` 返回 `VERIFIED`。第一阶段基线校准时，dev 相对 main 仅有 `README.md` 与 `CROSS-HOST-BRIDGE.md` 文档差异；阶段 4 获授权后，当前 dev 又新增 `src/modules/mcp_router.js` 的 usage_count 最小修复和 `tests/router_registry_contract_test.mjs` 隔离回归资产。当前未发布差异为 4 个文件（上述两份文档、源码修复、测试文件），仅在 dev，未部署/未合并 main。发布前必须重新 compare，不以本路线图中的提交数代替即时检查。
- `wovowx/ZivenLab`：dev 相对 main 的未发布差异均位于 `governance/`，包括 `README.md`、CHANGELOG、roadmap、当前项目状态、架构差距矩阵、现状架构、真相源导航表和资产整理计划，共 8 个文档文件；均为文档修改，未改生产源码、数据库或部署。提交数会随每次文档提交变化，发布前重新 compare。
- 已确认权威来源分工：目标蓝图=`governance/整体架构.md`；当前实现地图=`governance/现状架构.md`；差距与验收=`governance/架构差距矩阵.md`；导航=`governance/真相源导航表.md`；行动路线=本文件；资产索引=`governance/资产全景.md`；当前工作状态唯一权威是云端 `⚙️/当前工作检查点`，身份根是 `🧬/我是谁`。
- 已确认 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 位于仓库根目录且可读；旧文档里“Not Found/待重建”的说法已过时。该文件有大量历史记录和重复的过期状态块，不能把旧交接自动视作当前授权。
- mcp-memory 的根 README 曾把不存在的根级 `docs/`、`skills/` 写作仓库目录；本轮已在 dev 修正，改为描述实际 `src/skills/` 与治理文档所在的 ZivenLab 仓库。

### 第一阶段验收（已完成）

1. 当前架构、目标蓝图、权威来源和组件边界各自有明确位置，不相互替代。
2. 已知的过期路径、过时分支/部署状态和交接阻塞已更正或登记；未验证项仍标为未验证。
3. 驾驶舱、路线图、现状地图、差距矩阵、导航表互相一致。
4. 本阶段不改生产源码、数据库 schema、用户记忆内容，不删资产，不部署、不推 main。

**当前停点：阶段 1–3 已完成；阶段 4「文档与职责收敛」继续进行（2026-10-26）。** usage_count 误计已按柳柳授权完成最小修复并提交到 `mcp-memory/dev/src/modules/mcp_router.js`；隔离回归测试 `tests/router_registry_contract_test.mjs` 也已同步到远端 dev。Operit 在本地同一修复/测试版本报告：`npm run check` exit 0、既有 webhook 测试 104/104、新 Mock 16/16。GPT 已回读核对 dev 源码和测试文件，但没有独立重跑 Node 命令。后续静态计数曾发现当前远端 `tests/router_registry_contract_test.mjs` 有 15 个 `check(...)` 调用点。GPT 随后在已授权测试文件范围内补入一条已注册 `memory_remember` handler 的失败不计 usage 断言；当前远端静态计数已为 16，与 Operit 原始报告的 16/16 在断言数上对齐。但补入断言后的精确远端文件尚未运行，状态仍为 NOT RE-RUN；不凭计数一致宣称通过，也不为单独核对数字重复消耗 Operit token。另一次源码核对纠正了旧的 suggest 空态判断：当前 `memory_unified.js` 已使用条件表达式处理空结果，既有 `webhook_idempotency_test.mjs` 含空数组/正常列表/404/500 四项输出测试；待补的是底层 `search.js` 的 `recordSearchKeyword` 行为、prefix/limit 与网络/JSON/写请求失败路径。进一步静态审阅发现 `create_patch_proposal` 的实时注册项 `input_schema=null`，tools/list 因而没有公开必填参数；Router 早期专门分支还绕过通用 `autoIncrementUsage`。这两项已分开记入入口/schema 与 usage_count 差距，暂不改源码，详见差距矩阵。真实 E3、权限行为与生产端点仍未验证；未部署、未推/合并 main。阶段 4 不因这一处修复完成而整体结束，后续继续按差距矩阵收敛职责与文档。

## 「一本好书式架构」总计划：共 6 个阶段

> 本节是整体升级的唯一阶段路线；不要与资产整理计划中旧的阶段 0–4 编号混用。

## 六阶段共同工程原则（目标定案，贯穿全部阶段）

以下规则是六阶段的共同验收要求，不另设独立阶段，也不以“目录整理完成”代替工程质量改进：

1. **先复用，再新增。** 新增函数、模块、工具、注册项或机制前，先检索现有实现与调用链；优先组合稳定能力，不造平行机制。
2. **职责清楚，避免假复用。** 共享逻辑应有清楚归属和明确契约；只有职责、输入输出与变化原因确实相近时才合并，不为减少文件数、代码行数而强行抽象。
3. **为真实需求保留扩展路径。** 新能力尽量通过已有注册、路由、handler、公共模块和存储契约接入。若每次扩展都要改动多个无关位置，记录为扩展瓶颈并按实际需求处理；不预建万能框架、不为假设需求增加抽象层。
4. **先查依赖，再做最小可逆调整。** 检查静态与动态引用、调用方、schema/注册、权限、兼容路径和输入输出契约；未经核实不删除、不覆盖、不合并。
5. **回归保护必须有证据。** 修改前识别受影响行为与测试；修改后执行适用的静态检查和行为回归，记录真实命令、退出码和结果。静态检查不等于行为测试；未执行的测试必须标为未执行。
6. **每阶段都检查复用性与可扩展性。** 记录公共能力的归属、重复职责、关键扩展点、兼容性及验证缺口；未达到的项目进入差距清单，不用“整体完成”掩盖。
7. **复杂度预算优先。** 架构应像一本好书：目录清楚、职责明确、能沿引用找到依据。优先复用和小步收敛，不做没有现实收益的重构。

### 阶段 1｜现状基线与权威来源对齐 — ✅ 已完成（2026-10-26）
目标：弄清实际有什么、哪些信息权威、哪些问题未验证。
工作：核对 ZivenLab/mcp-memory/Supabase/Cloudflare/两种宿主；分开目标蓝图、当前实现、差距矩阵、导航、工作检查点；修正文档路径/状态冲突。
验收：关键入口已对齐，未验证项显式登记；没有改生产代码、数据库或 main。

### 阶段 2｜架构书总目录与章节职责地图 — ✅ 已完成（2026-10-26）
目标：做出全系统目录与章节分工，优先复用现有材料，避免机械新增文件或概念。
工作：明确每章回答什么、哪份文件是权威、各章如何互相引用；将治理、记忆、呈现和运行时编织层映射到真实仓库/服务；标记重复文档、职责交叠、公共能力归属与章节空白；识别已有扩展入口，但不凭目录猜测代码行为。
验收与结果：已在 `governance/真相源导航表.md` v1.4 建立 10 章总目录与职责地图，覆盖入口导航、目标与需求、治理、真实现状与差距、记忆数据、运行时路由、呈现、跨宿主连续性、质量回归发布、行动状态；明确目标/现状/差距、需求/规则、索引/事实、路线/状态/历史的职责边界。`governance/README.md` 已增加唯一地图入口，未新建平行文档。仅改 ZivenLab/dev 治理文档，未改代码、数据库、部署或 main。

### 阶段 3｜真实实现与依赖地图 — ✅ 静态地图完成（2026-10-26）
目标：让架构书反映真实代码和运行环境，并查清哪些能力可复用、哪些结构阻碍扩展。
工作：追踪入口→Router→schema/注册→handler→utils/modules→数据存储；区分源码存在、已注册、可路由、实际调用、已测试；核对公共函数/模块、同职责重复实现、强耦合点、硬编码分支与扩展瓶颈；分类在役/共享/兼容/旧实现候选/暂停/未知。
验收与结果：已在 `governance/现状架构.md` 增补 Worker→MCP Router→注册表/handler→共享模块→Supabase 的主调用链、工具路由与公共模块关系；只读核对当前 skills 注册表 69 行（66 启用、3 禁用），标出 14 行缺 handler 配置；记录 memory 兼容别名 schema 不一致、category/data 旧 handler 候选、权限守卫未接入 request path、search_history 缺表及 endpoint 未验证边界。对应风险进入 `governance/架构差距矩阵.md`。满足静态实现地图验收；不将静态证据误写成真实 endpoint 或行为测试通过。

### 阶段 4｜文档与职责收敛 — 🟡 进行中（usage_count 最小缺陷已修复；其余收敛继续）
目标：以最小、可逆的改动收敛存量职责；减少重复建设，同时不损害既有行为与兼容性。
进展（2026-10-26）：阶段 3 后已同步现状架构与差距矩阵；导航表已更新至 v1.7，并纳入阶段 4 usage_count 最小修复、Router schema/打点例外、数据库证据边界。经柳柳明确授权，`src/modules/mcp_router.js` 的 `toolOk` 失败前缀已新增 `handler type not implemented` 排除项。隔离测试已在 `mcp-memory/dev/tests/router_registry_contract_test.mjs`；Operit 原始报告为 E1 `npm run check` exit 0、E2 webhook 104/104、新 Mock 16/16。GPT 后续补入一条 registered-handler failure 断言，当前远端静态有16个 `check(...)` 调用点，但该精确版本尚未重跑（NOT RE-RUN）；GPT 未独立执行 Node 命令。真实 E3 未运行；未部署、不推/合并 main。

本阶段还通过只读 `supabase_schema(action=schema_dump)` 重新观察到25张表（23业务表+2测试表），并校准 `database-overview.md` v2.2、`memory.md` v1.1、`记忆两表设计.md` v1.4 与检索测试集 v1.4：把 memory_events 追加式触发器/幂等唯一约束标为历史执行记录、现状待核；把检索测试状态明确为部分历史用例已运行、未全量自动化。本轮没有写数据库、改 schema 或触发器。阶段4整体职责收敛尚未完成，后续继续按差距矩阵推进。
工作：修正断链和过期说明；先查调用方、动态引用、注册/schema、权限和契约，再决定复用、整合、保留或标记旧实现；公共逻辑优先归于清晰的共享位置；确有扩展瓶颈时才按真实需求调整边界，并做回归。
验收：每项结构调整说明复用收益、职责变化、兼容影响、验证与回滚路径；不为整洁重构，不强行合并，不擅删工具/记忆，不擅改 DB/schema。

### 阶段 5｜驾驶舱与运行时连续性闭环
目标：换会话/换宿主后能恢复当前工作，且按正确规则执行；尽可能由现有能力组合闭环，而不是另造平行运行时。
工作：验证身份根→唯一检查点→近期共识/进度/下一步/阻塞→情境召回→Skill/工具路由→执行验证→更新检查点；检查现有工具和路由的复用方式、边界与扩展入口；分别验证 GPT App 与 Operit 的真实能力。
验收：新会话能接上同一主线；记忆来源可追溯；执行结果有证据；宿主未验证能力明确标注；没有为相同职责额外建立平行机制。

### 阶段 6｜整体验收与版本收口
目标：证明架构职责清晰、已有能力得到保护，且真实扩展路径可理解、可验证。
工作：分层执行静态检查、行为回归、跨宿主冷启动和真实 MCP/HTTP endpoint 验证；复核共享能力是否重复建设、扩展是否依赖无关模块改动、兼容路径是否有证据；核对 Pages 发布范围与隐私风险；整理未关闭差距和回滚说明。
验收：测试证据可复核；复用性、扩展瓶颈、兼容风险及未验证项有明确状态；发布候选范围清楚。推 main 前须报告版本/范围/验证/回滚并得到柳柳明确同意；回滚未演练不得写成已演练。

**当前停点：阶段 1–3 已完成；阶段 4 仍进行中。** usage_count 误计的最小修复已在 `mcp-memory/dev`，隔离 Mock 测试文件也已同步到远端 dev。Operit 报告本地 E1 exit 0、既有 E2 104/104、新 Mock 16/16；GPT 后来在授权范围内补入直接的 registered-handler failure 断言，当前远端文件已有 16 个 `check(...)` 调用点，与 Operit 原始报告的16/16在计数上对齐；但补入断言后的精确文件尚未重跑，仍标 NOT RE-RUN。保留 Operit 原始报告，不把它包装成当前远端文件已复现通过；真实 E3 endpoint 与线上行为未验证。当前未部署、未推/合并 main；接下来按矩阵继续文档/职责收敛与验证。
### 明确暂缓与发布边界

- 聊天室与 Agent runtime 唤醒失败继续暂停。
- `search_history` 底层记录/建议查询失败路径（`recordSearchKeyword`、prefix/limit、网络/JSON/写请求失败）、记忆迁移事件审计、工具注册/schema/handler 一致性（含 `create_patch_proposal` 的 schema 缺失与专门路由分支）、usage_count 计数覆盖、权限守卫接入、Pages 发布范围、`/memory-universe` 匿名访问风险仍保留在差距矩阵。现有 suggest 输出断言已经覆盖空数组、正常列表、404/500 JSON 错误对象；不再把旧的 suggest 空态静态问题当作当前缺陷。usage_count 误计已在 dev 修复，隔离 Mock 文件已进入 dev；Operit 报告 16/16，随后已补入一条 registered-handler failure 断言，当前远端脚本静态计数为16；与 Operit原始16/16回报数字相符，但新版本尚未重跑，状态仍为NOT RE-RUN。真实 E3 endpoint 未执行，不将 Mock 报告等同于线上验证。
- `v6.35.0` 已发布并部署 VERIFIED；该版本是可靠性基线，不代表整体架构升级完成。下一次 main 发布须先说明版本、范围和证据，并取得柳柳明确同意。
- 本路线图控制当前行动顺序；历史 P0/P1/P2 清单仅为历史路线/待办参考，不自动成为活跃任务。
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