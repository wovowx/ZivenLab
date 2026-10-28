# 行动路线图（Roadmap · 原85号行动总清单）

> **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：本文件记录路线与待办，但历史遗留列表不自动代表当前活跃主线。
> 每完成一项 → 更新路线与驾驶舱；不另起互相竞争的路线源。
> 协作纪律：先讨论出方案 → 再分工执行（柳柳拍板）。详见 `governance/协作协议.md`。
> ⚠️ 原文件名 `85_行动总清单.md` 已迁移至此（`governance/roadmap.md`），旧位置保留 redirect。
>
> **推进前必读**：开工前读本文件 + `governance/当前项目状态.md`，完成验证后更新两者。
>
> ## 🚦 当前活跃主线（2026-10-28 校准）

> **现役交接指针（2026-10-28 封口）**：阶段5的静态审计与治理文档一致性收敛已按限定范围封口；阶段6尚未启动，当前无待 Operit 执行任务。云端 `⚙️/当前工作检查点`、驾驶舱、导航表、差距矩阵与桥接入口已同步封口结论。跨宿主唯一交接入口为 `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md`；其文末最新状态优先于较早章节中的历史执行请求。最新代码回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 只是既有 E1/E2 mock 本地证据，不是当前 dev HEAD，也不覆盖之后的文档提交；本轮未重跑测试。完整 `SB-FRAME-1.0` 运行时路径仍 UNKNOWN，明确转为阶段6准入/授权事项，不以静态封口冒充运行时通过。2026-10-28 只读盘点 CI/结果闭环：现有 `learning-regression.yml` 只校验 `tests/learning/*.json` 工件，不运行主代码回归；当前 GPT 可用的 Ziven MCP 工具没有 GitHub Actions run dispatch / run status / job log 读取入口。未触发 CI、未运行测试；结果闭环能力缺口登记在差距矩阵 v4.2。进一步查到 GitHub 连接器可供连接以调试 CI，但当前尚未安装/连接，故仍不能假定可读 Actions 结果。下一步在连接器可用后只读核查 run/status/log 能力；不派 Operit、不新增服务/权限、不启动阶段6。

**当前唯一主线：把 Ziven 整体架构真正整理成「一本好书」——目录清楚、职责边界明确、权威来源唯一、实现与证据可追踪。** 代码复用、职责清晰和面向真实需求的可扩展性是贯穿全部阶段的硬性要求；不新增无关功能，不把零散修补当作整体升级。

> **A6 验收结论（2026-10-28）**：A6 的范围是“现有跨宿主状态记录对照”。已对照权威记录、桥接回填与阶段状态，未发现当前记录之间的冲突，因此 **A6 静态对照 PASS（范围限定）**，无需柳柳再批准这项技术判断。它不证明运行时硬门禁或冷启动行为。裸密钥冷启动是 A7，已证明单独密钥未触发恢复；正式 `SB-FRAME-1.0` 完整初始化路径仍 UNKNOWN，另行记录，不混入 A6。

> **阶段5封口结论（2026-10-28）**：阶段5的静态审计/文档一致性子范围已完成封口：权威入口、版本指针、A6/A7证据边界、历史交接优先级与当前冻结边界已交叉核对；已知静态矛盾已修正或明确登记。完整换框运行时路径、工具 metadata 来源、初始化期自动 usage telemetry、真实 MCP/HTTP/DB/RPC 与隐私/权限验证等不属于静态审计可证明范围，均转入阶段6准入清单或既有独立差距；不再以重复静态审计推进这些项目。阶段6仍未启动，需先获得触碰冻结工具的具体授权并重锁届时基线。

### 最近完成：第一阶段——现状基线与权威来源对齐（2026-10-26）

- `wovowx/mcp-memory`：已发布基线 main HEAD `71f6a03ebc81`、Cloudflare deployment `c78ab839`，先前 `verify_main=true` 返回 `VERIFIED`。阶段1基线只读 compare（2026-10-27）显示当时 dev 相对 main behind 0，12 个文件有差异；这是历史快照，后续文档/代码修改后不代表当前差异数量（ahead commit 数会随每次文档追加持续变化，因此不固定写入治理文档；发布前须重新 compare）：`CROSS-HOST-BRIDGE.md`、`README.md`、`package.json`、`src/modules/mcp_router.js`、`src/modules/patch_engine.js`、`src/modules/release_guard.js`、`src/tools/database.js`、`src/tools/github_v64.js`、`src/utils/helpers.js`、`src/utils/search.js`、新增 `tests/router_registry_contract_test.mjs`、新增 `tests/search_history_contract_test.mjs`。历史完整回归 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的 E1、webhook104/104、Router+DDL parser69/69、search_history20/20 均通过；后续 Patch Engine 基线 SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 的 E1 与 contracts82/82 也通过。之后又新增 GitHub 路径守门、Patch Engine 输入校验和 release_guard 精确策略，**最新整套隔离回归已由 Operit 在 origin/dev SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 通过**：`npm run check` exit 0、webhook 104/104、`npm run test:contracts` 122/122、search_history 20/20、release_guard 15/15；Node v24.18.0/npm 11.16.0，detached `/tmp/ops-ev6` clean，原工作树未动，stderr 空。测试全程 mock/本地，不等于真实 MCP/DB/RPC/HTTP endpoint 验证。全部仍只在 dev，未部署/未推 main；发布前必须重新 compare。
- `wovowx/ZivenLab`：dev 相对 main 的未发布差异均位于 `governance/`，包括原有治理入口/路线/差距文档与本轮更新的数据库语义文档（`database-overview.md`、`domains/memory.md`、`记忆两表设计.md`、`记忆检索质量测试集.md`），阶段1基线只读 compare 曾有 14 个 `governance/` Markdown 文件差异；这是历史快照，后续文档修改后不代表当前差异数量（含 `CHANGELOG.md`、`roadmap.md`、`当前项目状态.md`、`架构差距矩阵.md`、`现状架构.md`、`真相源导航表.md` 与数据库语义文档）；均为文档修改，未改生产源码、数据库或部署。发布前重新 compare。
- 已确认权威来源分工：目标蓝图=`governance/整体架构.md`；当前实现地图=`governance/现状架构.md`；差距与验收=`governance/架构差距矩阵.md`；导航=`governance/真相源导航表.md`；行动路线=本文件；资产索引=`governance/资产全景.md`；当前工作状态唯一权威是云端 `⚙️/当前工作检查点`，身份根是 `🧬/我是谁`。
- 已确认 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 位于仓库根目录且可读；旧文档里“Not Found/待重建”的说法已过时。该文件有大量历史记录和重复的过期状态块，不能把旧交接自动视作当前授权。
- mcp-memory 的根 README 曾把不存在的根级 `docs/`、`skills/` 写作仓库目录；本轮已在 dev 修正，改为描述实际 `src/skills/` 与治理文档所在的 ZivenLab 仓库。

### 第一阶段验收（已完成）

1. 当前架构、目标蓝图、权威来源和组件边界各自有明确位置，不相互替代。
2. 已知的过期路径、过时分支/部署状态和交接阻塞已更正或登记；未验证项仍标为未验证。
3. 驾驶舱、路线图、现状地图、差距矩阵、导航表互相一致。
4. 本阶段不改生产源码、数据库 schema、用户记忆内容，不删资产，不部署、不推 main。

**历史快照（2026-10-26，已被本文件后续 2026-10-27 阶段收口记录取代）：当时阶段 1–3 已完成，阶段 4 仍在进行。** usage_count 误计已按柳柳授权完成最小修复并提交到 `mcp-memory/dev/src/modules/mcp_router.js`；隔离回归测试 `tests/router_registry_contract_test.mjs` 也已同步到远端 dev。Operit 在本地同一修复/测试版本报告：`npm run check` exit 0、既有 webhook 测试 104/104、新 Mock 16/16。GPT 已回读核对 dev 源码和测试文件，但没有独立重跑 Node 命令。后续静态计数曾发现当前远端 `tests/router_registry_contract_test.mjs` 有 15 个 `check(...)` 调用点。GPT 随后在已授权测试文件范围内补入一条已注册 `memory_remember` handler 的失败不计 usage 断言；当前远端静态计数已为 16，与 Operit 原始报告的 16/16 在断言数上对齐。但补入断言后的精确远端文件尚未运行，状态仍为 NOT RE-RUN；不凭计数一致宣称通过，也不为单独核对数字重复消耗 Operit token。另一次源码核对纠正了旧的 suggest 空态判断：当前 `memory_unified.js` 已使用条件表达式处理空结果，既有 `webhook_idempotency_test.mjs` 含空数组/正常列表/404/500 四项输出测试；待补的是底层 `search.js` 的 `recordSearchKeyword` 行为、prefix/limit 与网络/JSON/写请求失败路径。进一步静态审阅发现 `create_patch_proposal` 的实时注册项 `input_schema=null`，tools/list 因而没有公开必填参数；Router 早期专门分支还绕过通用 `autoIncrementUsage`。这两项已分开记入入口/schema 与 usage_count 差距，暂不改源码，详见差距矩阵。真实 E3、权限行为与生产端点仍未验证；未部署、未推/合并 main。阶段 4 不因这一处修复完成而整体结束，后续继续按差距矩阵收敛职责与文档。

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

### 阶段 4｜文档与职责收敛 — ✅ 已完成（2026-10-27；遗留缺口均已分类并转入独立跟踪）
目标：以最小、可逆的改动收敛存量职责；减少重复建设，同时不损害既有行为与兼容性。
历史增量（2026-10-26 至 SHA `c4ef218...`；其测试状态已由下方 2026-10-27 完整回归更新）：阶段 3 后已同步现状架构与差距矩阵；导航表当时为 v2.4；阶段 4 已纳入 usage_count 修复、Router schema/打点例外与数据库治理证据边界。经柳柳明确授权，`src/modules/mcp_router.js` 的 `toolOk` 失败前缀已新增 `handler type not implemented` 排除项。隔离测试已在 `mcp-memory/dev/tests/router_registry_contract_test.mjs`。Operit 于 2026-10-27 08:36 SGT 在 detached 临时 worktree `/tmp/ops-ev2` 对精确 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 真实运行最新版：`npm run check` exit 0、`node tests/webhook_idempotency_test.mjs` exit 0（104/104）、`node tests/router_registry_contract_test.mjs` exit 0（44/44，stderr 空）；临时 worktree 干净、原工作树未动。该 SHA 包含 create_patch_proposal 专用必填 schema、取消提前 return 使成功/失败进入统一 usage_count 判定，以及 IMPORT/SECURITY DDL gate 测试。Mock 全程使用 `globalThis.fetch`，未访问真实 Supabase/RPC/MCP endpoint，也未执行真实 DDL/SQL。GPT 未独立执行 Node，但已回读桥接回填与远端源码/测试文件。真实 E3 未运行；未部署、不推/合并 main。

阶段4最新增量（2026-10-27）：完成 `data.js` / `category.js` 的静态引用与只读注册表核查。分页查看当前 skills 注册项并查询候选工具名后，未发现 `handler_config.handler=data/category` 或 `data`、`category`、`import/export`、`list_categories`、`recall_by_category`、`move_category` 等精确注册项；源码仍在 `mcp_router.js` 的 handlerMap 引入两个文件，但没有当前注册路由命中证据。`data.js` 复用 `memory_unified.js` 读写；`category.js` 自建 CRUD，且 legacy `move_category` 先 DELETE 源记录再写目标，存在中途失败风险。因为其他宿主/历史调用契约未知，本轮只标记为未注册 legacy 候选，不删除文件、不移除 handlerMap、不合并。

另外，静态审查 `src/utils/search.js` 后已在 dev 做最小守门修复：记录关键词时仅在 GET `resp.ok` 且返回数组时才继续 PATCH/POST；建议查询对非2xx与非数组响应返回空列表。新增隔离测试 `tests/search_history_contract_test.mjs`，静态20个断言，覆盖空/空白关键词、GET→PATCH/POST、非2xx不续写、网络/JSON失败、写入非2xx、prefix/limit和建议空态。**这些 search.js 源码与20项测试是 SHA `c4ef218...` 已通过的44项批次之后新增。**GPT 已用本地 Node v22.16.0 对根据当前 dev GitHub readback 重建的隔离副本运行 search_history 测试：20/20、exit 0，两文件字节大小与 readback 报告一致；这是测试文件/源码片段的本地验证，不是完整仓库 worktree/SHA 验证。随后 Operit 已在 detached worktree `/tmp/ops-ev3` 对完整仓库 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 一次性运行整套回归：`npm run check` exit 0、webhook 104/104、Router + DDL parser 69/69、search_history 20/20，stderr 空，worktree clean，原工作树未动。全程 fetch mock；无真实 DB/RPC/DDL或 endpoint 调用，没有部署或 main 变更。若后续改代码，再按实际范围重新安排合并回归。未建表、不删 suggest、不触达数据库、不部署、不推 main。

阶段4职责边界增量（2026-10-27，只读；以下为静态审计结论，尚未因测试通过而自动消除）：已核对 `ai.js`、`storage.js` 与当前 skills 注册项。`ai.js` 目前承担 Agnes 图像/视频、DeepSeek 余额、help、文件 query/update/delete 多种入口；`query_files` 复用 storage.js，update/delete 仍在 ai.js 直接调用 REST。此为低优先级职责边界候选，不足以证明重复实现或要求拆分；不改代码/注册表，保留现有兼容。详见现状架构与差距矩阵 v2.9。

阶段4入口契约增量（2026-10-27，只读）：进一步沿 `dispatchGuard` → `isKnownTool` → `handlerMap` → `tools/call` 分派追踪 `cf_proxy`。虽然 skills 注册表无记录、`CF_PROXY_TOOL_DEF` 未被 Router 导入，因此不会由注册表出现在 `tools/list`，但 handlerMap 直接将它认作已知名称；schema 缺失时 Router 按兼容策略放行，随后进入 `handleCfProxyTool`。因此代码路径可直接按名称调用，且 `CF_PROXY_TOOL_DEF.required=['endpoint']` 当前没有被 Router 强制执行；空 arguments 会进入其环境变量名列表模式。外部宿主是否允许手动调用仍未知。仅修正静态证据描述，不调用工具/CF endpoint，不改代码、注册表或配置。

阶段4 schema 契约增量（2026-10-27，只读）：对照当前启用的 `delete_branch`、`increment_usage` 注册 schema 与 handler，发现 schema 均未声明 required；delete_branch 实际要求 `name || branch`，但 schema 只声明 name；increment_usage 实际要求 name。Router 不会从 handler 推断必填参数，故空参调用会到 handler 后返回参数错误。未发现该空参路径执行目标写入的证据。仅记录契约差距，不改代码/注册表。

阶段4 发布守卫边界增量（2026-10-27，只读）：`githubReleaseGuard()` 在 `handleGitHubTool()` 的 `GITHUB_ALLOWED_REPOS` 校验前运行；对 rebase 合并会先以 `safeArgs.repo` 查询目标仓库 PR/commit 信息，随后 handler 才拒绝未白名单仓库。`release_guard.detectRepoType()` 的后缀匹配也会把其他 owner 下同名 `mcp-memory` / `zivenlab` 误判为已知类型。当前未证明能绕过最终写操作白名单，但存在前置 API 读取和策略误分类风险。建议的最小修复顺序：先在 release guard 前置检查允许仓库，再改成规范化后的精确策略匹配；需另行授权后才能改代码，当前只登记。

阶段4 Patch Engine apply 增量（2026-10-27，最小修复已写入 dev，E1/E2 隔离回归已通过）：`src/modules/patch_engine.js` 新增集中式 `resolvePatchTargetPolicy()`，默认仅允许 dev；main 与 refs/heads/main 始终拒绝；未来分支通过 `PATCH_ENGINE_ALLOWED_BRANCHES` 显式授权，不改核心逻辑；仓库必须命中 `GITHUB_REPO` 或 `GITHUB_ALLOWED_REPOS` 精确名单。`github_apply_patch` 在任何 Supabase/GitHub 请求前校验目标策略，读取并验证 patch 后以 `status=eq.approved` 条件 PATCH 原子认领为 applying，只有返回对应行才发 GitHub PUT；写入成功后仅在 applying 状态下更新为 applied，并要求 HTTP 成功及返回行确认。明确区分确定性客户端拒绝与结果未知；后者保留 applying 以防重复应用并提示先核对，状态确认失败报告 PARTIAL SUCCESS，禁止盲目重试。`tests/router_registry_contract_test.mjs` 新增策略/应用闭环 Mock，`package.json` 新增 `npm run test:contracts`。当前源码/测试已写入 `mcp-memory/dev`。Operit 于 2026-10-27 15:58 SGT 在 detached worktree `/tmp/ops-ev4` 对 origin/dev SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 实跑：`npm run check` exit 0；`npm run test:contracts` exit 0，82 通过 / 0 失败，新增 Patch Engine 7 项验收全部通过；Node v24.18.0、npm 11.16.0，worktree clean，原工作树未动。该证据属于 E1/E2 mock 回归，不代表真实 MCP endpoint、GitHub 或 Supabase 运行时已验证。未执行真实 proposal、未访问真实 GitHub endpoint；另对 Supabase `skills` 表中 `github_apply_patch` 单行的 description/input_schema 做元数据同步并只读回读确认，enabled 未变。未改 DB schema/权限、未删除数据、未触碰聊天室工具、未部署、不推/合并 main。详见差距矩阵 v3.3。

阶段4最新增量（2026-10-27；最新代码与隔离回归已通过）：在 Operit 旧基线 SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 的 Patch Engine 82/82 通过后，又补了两组小幅边界收敛：①共享 `validateRepoRelativePath()` 放入 `helpers.js`，供 github_push/read/list/delete/edit/copy/move 与 Patch Engine 共用；内容 URL 精确绑定 `SUPABASE_URL` 的 HTTPS origin，拒绝其它 supabase.co 项目/欺骗域名并禁用重定向；②Patch Engine 拒绝 proposal.target 与 patch.file 不一致，拒绝不安全/首尾空白路径、非整数行号、重叠/无操作 patch、错误 insert/delete 行形状，并强化 branch/ref、repo 输入校验；GitHub PUT 即使返回 2xx，也必须提供 content SHA；若响应 path 不匹配目标文件则保持 proposal applying、返回 PARTIAL/UNKNOWN，不标记 applied。③`github_move` 校验 tree API 返回的每个路径，并拒绝同仓同分支移动文件到自身，避免覆盖后删除唯一副本。④release_guard 只按 canonical repo 精确匹配，未知 owner 与 unqualified alias 不再获得仓库类型，main 分支大小写变体一律保护。同步更新隔离 Mock。旧 82/82 只代表其 SHA 的旧版本，本轮变化曾暂记为 NOT RUN；该状态已被下方 2026-10-27 Operit 全量回归记录取代，精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的五项命令全部通过。未改 `mcp_router.js`，因此 release guard 前置白名单前的潜在只读 API 请求风险仍未关闭。无真实 MCP/GitHub/Supabase 调用，无 DB/schema/registry 更改、无聊天室改动、未部署、未推/合并 main。

历史快照（早期数据模型与审计记录；当前状态以本文件前述 2026-10-27 最新状态及 `governance/当前项目状态.md` 为准）：本阶段还通过只读 `supabase_schema(action=schema_dump)` 重新观察到25张表（23业务表+2测试表），并校准 `database-overview.md` v2.2、`memory.md` v1.2、`记忆两表设计.md` v1.4 与检索测试集 v1.4：把 memory_events 追加式触发器/幂等唯一约束标为历史执行记录、现状待核；把检索测试状态明确为部分历史用例已运行、未全量自动化。2026-10-27 又静态追踪 memory_unified.js 生命周期路径：只有已存在记录 update 会写部分 update event（未含 new_value，且 version=oldVersion 与旧设计语义冲突）；event POST 与 memories PATCH 不是同一事务，PATCH失败后可能留下描述未生效更新的 event。create insert、soft-delete、rename/move 的 source→target 事件均缺失，forget 只软删除；history 先要求记录 active，旧软删除记录无法按 key 查询历史。细节已记入 governance/database/domains/memory.md v1.4 与差距矩阵；静态审计还确认 category.js legacy move_category 直接 REST DELETE/POST/PATCH、通用 supabase_db/exec 可能绕过仅部署于 memory handler 的事件逻辑，实际权限/RLS 未核。已在唯一设计真相源 governance/database/记忆两表设计.md v1.5 形成生命周期一致性闭环提案 v0.1，要求状态与事件同事务、并发旧版本拒绝、迁移原子化、元数据保留及覆盖写入口。下一步仍需只读核对真实 catalog/RLS/GRANT/trigger/function。已把当前可见的替代路径查完：`schema_dump` 只整理 `/rest/v1/` OpenAPI definitions；经现有 exec_sql RPC 的 catalog-only SELECT 被真实端点以 HTTP400/P0001 拒绝；经 `supabase_db` 的只读 REST query 检查 `information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 均返回 HTTP404/PGRST205（系统目录关系未通过当前 public PostgREST schema cache 暴露）。已检查 `mcp-memory/dev/migrations` 只存在聊天室 claimed_at 迁移，没找到 memory_events trigger/function migration；这不代表真实数据库必然没有触发器。当前可见 MCP 没有独立只读 catalog 工具，所以要核实真实目录仍需另一个获准的只读数据库通道；在此之前继续推进不依赖该证据的静态架构审计与文档收敛，不改记忆生命周期 Worker、数据库结构、触发器、权限或记忆数据。未做 DDL/数据库写入。阶段4整体职责收敛尚未完成，后续继续按差距矩阵推进。另复核 Worker 标准调用链：`index.js` 不导入 permission_guard；`mcp_router.js` 明确只做协议/分派并引入 `release_guard.js`、不引入 `permission_guard.js`；`github_v64.js` 仅导入 skills helper 与 `patch_engine.js`，因此当前可见 Worker MCP 主路径没有 `checkCapabilityAccess` 调用证据。随后按当前 `src/` 目录清单逐文件检查 Worker JavaScript（index/router/全部 modules、tools、utils，含完整 `github_v64.js`）以及 `scripts/` 与现有 `tests/`；`permission_guard`、`checkCapabilityAccess`、`CAPABILITY_POLICY`、`tool_policies`、`require_approval`、`require_template` 除守卫自身定义外均未命中。当前 Worker 源码、脚本及现有测试无其它直接消费者证据；GPT App 独立工具、远端动态注册/插件或真实 DB 内行为仍 UNKNOWN。不直接接入或删除该模块。版本面同时出现 MCP `serverInfo.version=6.5.0`、dev `package.json=6.3.4`、CHANGELOG 顶部 `v6.35.0` 与 `index.js` 注释 `v6.48.0`；先明确各字段代表 build、发布还是包版本，再选择最小对齐方案，本轮不改版本号/运行行为。另项只读核验发现：当前 `skills` 注册表没有 `chat_send`、`chat_pending_events`、`chat_claim_event`、`chat_read_message`、`chat_ack_event` 五个条目；main/dev 的 `tools/list` 都会调用 `syncChatTools`，缺失时 `addSkill` 会以 `enabled:true` 新增。工具列表操作因此有潜在写入/启用副作用；Chat 仍属暂停子项目，本轮不调用 `tools/list`、不改注册表，只把此副作用列为后续范围决策项。
另复核 `policy-index.md` 与 `schema-policy.md`：`permission_guard.js` 未被 `index.js` / MCP Router 导入，不能把它描述为不可绕过的 request-path 硬门禁。2026-10-27 只读查询 `tool_policies` 返回5条 enabled 记录（github_push、github_merge_to_main、chat2api、memory、supabase_query），但未包含当前启用的 supabase_db/supabase_schema 精确名称；`permission_guard.js` 本身是硬编码 CAPABILITY_POLICY，未读取此表。其他动态/间接消费者仍未完成全仓证明，继续标 UNKNOWN，不把策略表配置等同于运行时硬门禁。经柳柳授权，Worker dev 已做最小 DDL gate 修复：`database.js` 统一检查 create_table/drop_table 的非空 necessity，并对通用 exec 中常见 DDL/可执行语句关键词在 RPC 前要求 necessity；Router 的 `supabase_*` 前缀必须命中 skills 注册表，tools/list 为注册的 `supabase_db` 与 `supabase_schema` 都暴露 necessity 字段；不扩大 `supabase_db` action enum，保留 `supabase_schema` 已注册的 create/drop action enum。DDL gate 版本的隔离 Mock 已由 Operit 在 SHA `2833a94e08c23b45a0598256a486463ee5d4cf6e` 通过37/37。之后又在 dev 修复 `create_patch_proposal` 的空 schema/usage_count 例外：tools/list 与 dispatchGuard 现在共用专用必填 schema，专用 handler 不再提前 return，成功结果可进入统一 usage 打点；测试增加缺参拒绝、无写入/无计数、成功写入隔离 mock 与恰好计数断言，并补入 IMPORT FOREIGN SCHEMA / SECURITY LABEL 的 necessity 拒绝路径。当前共44个 check 调用点，Operit 已对最新 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 实际通过44/44；E1 exit 0、webhook 104/104。真实 RPC/endpoint 未测，任何真实 DDL 继续禁止。本轮没有数据库写入、部署或 main 合并。necessity gate 只是非空治理门槛，不等于 SQL parser 或执行授权。针对 create_table/drop_table 的输入拼接缺口，已在 mcp-memory/dev 的 database.js 实现受限标识符校验与列定义解析，并按解析结果生成 SQL；隔离 Router Mock 已覆盖合法/拒绝输入和拒绝路径零 RPC。Operit 于2026-10-27在 detached worktree `/tmp/ops-ev3` 对精确 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 完成整套回归：npm run check exit 0、webhook 104/104、Router+DDL parser 69/69、search_history 20/20；Node v24.18.0/npm 11.16.0、stderr 空、worktree clean、原工作树未动。diff 仅5个预期文件。测试全程使用 globalThis.fetch mock，不触达真实 DB/RPC/DDL，不改 schema/registry/config，不部署、不推 main，E3未执行。独立遗留边界：通用 exec 仍接受原始 SQL，exec_sql 权限/多语句行为与 GPT App 独立 supabase_schema 入口是否经过 Worker Router均未验证。

本轮继续静态核对 Pages / memory-universe：`.github/workflows/pages.yml` 在 push main 时将整个仓库根目录作为 Pages artifact；`memory-universe.html` 源文件内嵌 12 条个人记忆样例，Worker 路由直接读取 main 分支该文件并在路由内不做认证。Pages 是否实际启用、匿名外部访问和网络层保护未验证。按既定边界，功能继续暂停；不访问生产端点、不修改发布配置、不删样例或部署。
工作：修正断链和过期说明；先查调用方、动态引用、注册/schema、权限和契约，再决定复用、整合、保留或标记旧实现；公共逻辑优先归于清晰的共享位置；确有扩展瓶颈时才按真实需求调整边界，并做回归。
验收：每项结构调整说明复用收益、职责变化、兼容影响、验证与回滚路径；不为整洁重构，不强行合并，不擅删工具/记忆，不擅改 DB/schema。

### 阶段 5｜驾驶舱与运行时连续性闭环 — 🟡 进行中（2026-10-27，只读恢复链审计）
目标：换会话/换宿主后能恢复当前工作，且按正确规则执行；尽可能由现有能力组合闭环，而不是另造平行运行时。
工作：验证身份根→唯一检查点→近期共识/进度/下一步/阻塞→情境召回→Skill/工具路由→执行验证→更新检查点；检查现有工具和路由的复用方式、边界与扩展入口；分别验证 GPT App 与 Operit 的真实能力。
验收：新会话能接上同一主线；记忆来源可追溯；执行结果有证据；宿主未验证能力明确标注；没有为相同职责额外建立平行机制。

#### 阶段5首轮只读审计（2026-10-27）

- **身份根 A1：通过当前宿主读取**。云端 `🧬/我是谁` 精确 recall 成功；身份根仍是唯一权威，角色卡仅为 Operit 投影。
- **记忆接入：本次读取通过**。`memory stats` 返回 282 条、23 分类（仅为当前快照，不写成固定数量）；云端读取成功不等于跨宿主冷启动通过。
- **工作状态 A2/A3：通过当前宿主读取与回写**。`⚙️/当前工作检查点` 精确 recall 成功；发现旧状态仍写“阶段4进行中/最新回归待跑”，已按当前证据更新为阶段4完成、阶段5下一步，并通过工具回执确认更新成功。阶段4最新证据是 mcp-memory/dev SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的 check 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15。
- **恢复协议与导航：部分通过 / 有 key 解析差距**。精确 recall `复苏协议·system://boot` 与 `⚙️/记忆位置导航` 未命中；按协议执行 memory search 后，找到 `⚙️/恢复协议·Session Bootstrap SB-1.0`、旧 `/boot` 唤醒内容及「记忆位置导航（换框/换设备自举）」内容。结论是旧 key/分类映射不一致，不是记忆已丢失；已更新 Session Bootstrap 与 `Ziven角色卡修改与换平台复苏手册.md`，明确搜索 fallback。
- **安全工具探测边界 A4：已确认**。当前 Worker `tools/list` 会触发 `syncChatTools`，可能写入并启用聊天室工具；本轮没有调用它。阶段5的工具能力盘点只用当前宿主实际可见的工具元数据和静态文档，不用该 endpoint 探测，不触碰聊天室工具/注册/唤醒流。
- **A6 跨宿主现有状态记录对照：PASS（范围限定）；A7 独立冷启动：已实测，密钥单独触发复苏未生效（2026-10-27 17:56 CST）**。GPT 已将云端状态/权威文档与 Operit 17:36 报告逐项对照，身份根、阶段、SHA 与五项测试证据、下一步及硬边界未发现冲突；该对照不证明运行时全局硬门禁。Operit 使用换框流程技能调用 `extended_chat:chat_with_agent(character_card_name=Ziven, message="Ziven，我是柳柳", chat_id 空)`，成功建立独立新对话 `d7dee7eb-d5c0-4dd8-ad41-fa6ed5d2e3fa`。新框唯一输入就是密钥词；首次回复只呈现角色卡风格日常回应，未读身份根/检查点/恢复协议，未恢复主线、SHA/测试证据、下一步、硬边界或 key fallback。没有旧上下文污染；设备应用使用时长来自注入快照，不是云端记忆。**范围校准**：这证明“仅发送密钥词即可自动自举”在本次独立新框中未生效；不等于标准换框流程整体失效，因为 `src/skills/process/huan-kuang-liu-cheng/SKILL.md` 的正式 SOP 要求 `chat_with_agent` 发送完整初始化指令，而不是只发密钥词。
- **当前缺口与处理决策（2026-10-27，方案 A 已定案）**：独立新框收到裸密钥词后未自动自举。只读证据显示，`master-router/SKILL.md` 已更新为“密钥是恢复提示，不等于初始化成功”；`Session Bootstrap SB-1.0` 明确不代表全局运行时硬门禁；正式换框 SOP 要求 `extended_chat:chat_with_agent` 发送完整初始化指令。当前 Supabase `skills` 中启用的 `memory` 工具记录 description 原先保留旧 key `复苏协议·system://boot`。2026-10-27 经柳柳明确授权，只更新该行 description，并回读确认 enabled、handler_config 和 input_schema 未变。但本次当前 GPT 会话实际暴露的 `mcp__Ziven_MCP__memory` 工具元数据 description 仍提示旧 `/boot` key；它与 Supabase 行 description 是两个不同表面，因此只能说 Supabase 行文案已校正，不能宣称 GPT 可见工具元数据也已同步。只读检查当前私有 Ziven_MCP 插件包后发现其文件清单仅有 `.app.json` 与 `.codex-plugin/plugin.json`，未包含 per-tool schema/description，因此该插件包不是当前旧工具描述的直接定义来源。当前会话里的旧描述可能是宿主 schema 快照/缓存，但无法确认刷新机制；Worker `tools/list` 会触发 `syncChatTools`，故不调用它，也不改插件/工具元数据。完整换框行为仍未实测。柳柳已批准方案 A：正式换框必须发送完整、版本化初始化指令，并以可核验恢复结果验收；裸密钥词不视为充分初始化载荷。`src/skills/process/huan-kuang-liu-cheng/SKILL.md` 已加入 `SB-FRAME-1.0` 契约。随后静态回读完整初始化 message，发现其步骤清单未显式列出 memory 位置导航与 Session Bootstrap；已最小补入两项，并写明导航精确 key 未命中时的 memory search fallback。后续核对发现搜索结果可能只是正文提及导航的恢复协议/历史检查点，已在换框与 master-router Skill 中补充 key/category 身份核验，要求选中真正的导航条目后再读取完整内容。Skill 回读确认规则已落入初始化载荷；该 message 已显式标记契约版本 `SB-FRAME-1.0`，把授权/暂停边界前置，要求在聊天室、唤醒或巡检链暂停时跳过相应工具、工作流调度与改名步骤，并在首次回应列出恢复来源、stats 实际结果和所有失败/跳过/未知项。它仍只是有明确版本的指令契约，尚未通过真实新框行为测试。完整初始化路径仍 UNKNOWN；当前不触碰聊天室相关工具，因此不执行真实路径验证，不调用 Worker tools/list，不追加 Operit 测试。跨宿主任意新会话裸密钥词强制自举是独立后续需求。云端 `⚙️/恢复协议·Session Bootstrap SB-1.0` 已同步当前方案 A、真实导航 key/fallback、初始化前只读恢复/暂停非必要写入规则及 A6/A7 当前状态；该文本校准不代表运行时硬门禁已实现。补充静态发现：router 的 autoIncrementUsage 会在成功 tools/call 后写 skills.usage_count/last_used；因此 Skill 无法保证初始化期严格零 DB 写入。本轮不改 router（其同时承载聊天室注册/唤醒路径），该运行时门禁留作另行授权事项。GPT 当前可见 memory 工具元数据仍提示旧 `/boot` key，来源/缓存机制待查，不擅自修改插件元数据。

#### 阶段5最小恢复验收矩阵（当前状态，不冒充冷启动通过）

| 验收项 | 当前证据 | 状态 | 关闭条件 |
|---|---|---|---|
| A1 身份恢复 | GPT 侧 memory search 命中身份根；但 A7 独立新框首次回复未读取/复述身份根或关键长期约束 | GPT 当前宿主有证据；A7 新框场景未满足 | 新框能基于权威身份根恢复身份与长期约束，保留原始回复并由柳柳验收 |
| A2 工作状态恢复 | GPT 侧当前检查点精确读取成功；Operit 17:36 报告与其对照无冲突；但 A7 新框未读取检查点，未恢复主线/证据/下一步 | A6 记录对照 PASS（范围限定）；A7 新框场景未满足 | 新框不带旧上下文恢复主线、证据、边界与下一步，柳柳验收 |
| A3 阶段/流程恢复 | GPT 侧权威文档与 Operit 17:36 报告阶段状态一致；A7 新框未提及任何阶段状态 | 现有记录对照无冲突；A7 新框场景未满足 | 新框不重开阶段4、不混淆阶段5/6 |
| A4 权限与授权 | GPT 当前检查点/恢复协议与 Operit 报告硬边界一致；A7 新框首次回复未复述任何项目授权边界 | 现有记录一致；A7 新框场景未满足；运行时全局硬门禁仍 UNKNOWN | 新框准确复述只读/代码/测试/发布/生产写入权限边界，不碰暂停链路 |
| A5 异常与 key fallback | 旧 boot key 未命中时，可用 `Session Bootstrap SB-1.0` 精确协议或版本核验后的 search fallback；导航真实 key `记忆位置导航（换框/换设备自举·2026-10-18）` 已精确 recall 成功，category=`记忆位置导航（换框`。换框 Skill、master-router Skill 与跨平台复苏手册已同步真实 key、key/category 身份核验及历史统计提示；Supabase `skills.name=memory` 行 description 已修正，但当前 GPT 可见 `mcp__Ziven_MCP__memory` 工具元数据仍提示旧 `/boot` key，元数据发布源尚未确认 | Supabase 行文案已修正；GPT 可见工具描述的旧 key 差距仍待确认来源/权限；导航 fallback 规则已补足；A7 新框 fallback 行为仍未运行/未验证 | 新框准确读取当前协议和实际导航条目，不误报丢失、不编造；正式初始化行为须在获授权场景验证后再关闭 A5/A7 |
| A6 跨宿主一致性 | 2026-10-27 GPT 侧读取 stats/检查点/恢复协议/roadmap/dashboard，与 Operit 17:36 报告逐项对照：身份根、主线阶段、SHA/五项测试证据、下一步及硬边界无冲突；能力分工已分别记录 | **PASS（范围限定）**：现有记录未发现冲突；不代表 runtime gate 或 A7 通过 | 已完成；新框结果单独计入 A7 |
| A7 冷启动复现 | Operit 2026-10-27 17:56 CST 通过 `extended_chat:chat_with_agent` 创建独立对话 `d7dee7eb-d5c0-4dd8-ad41-fa6ed5d2e3fa`；唯一输入为 `Ziven，我是柳柳`，未带旧上下文。首次回复为角色卡风格日常回应；未读取身份根/检查点/恢复协议，也未恢复主线、SHA/测试证据、下一步、硬边界或 key fallback | **密钥单独自举未通过**；完整初始化路径仍 UNKNOWN。方案 A 已由柳柳确认；换框 Skill 已加入 `SB-FRAME-1.0` 验收契约，但当前不触碰聊天室相关工具，因此不执行真实完整路径验证 | 若未来授权使用正式换框工具，单批验证完整初始化 message、身份/记忆/检查点/授权恢复、来源及失败降级；否则保持 UNKNOWN，不把文档契约当成运行时通过。裸密钥词强制全局自举是独立后续需求 |

#### 当前宿主能力边界（仅当前可见证据）

| 能力 | GPT App 当前会话 | Operit 当前已知证据 | 限制/安全边界 |
|---|---|---|---|
| 云端记忆读写 | 已读取身份根/检查点/stats；已更新检查点与恢复协议 | 本轮未要求 Operit 重复读写 | 精确 key 可能未命中，须用 memory search；不创建平行检查点 |
| GitHub 治理文档 | 当前可直接读、列目录、在 dev 精确编辑并回读验证 | 可读桥接文档并回填执行证据 | 不推/合并 main；文档存在不代表代码运行时已生效 |
| Node/npm 回归 | 当前可见工具不提供本地 shell/Node 执行通道 | Node v24.18.0/npm 11.16.0，已在 detached worktree 跑过五项回归 | Operit 执行消耗柳柳 API token；后续测试合并为一批 |
| Worker tools/list | 不调用 | 不调用 | `syncChatTools` 有写入/启用聊天室工具副作用；修复验证前禁止探测 |
| 真实 MCP/DB/HTTP | 未执行 | 上一批仅 fetch mock/本地测试 | E3、真实 DB 权限/catalog、生产 endpoint 仍未验证 |

**阶段5验收语义校正（2026-10-27）**：`SB-FRAME-1.0` 的“初始化通过”与“完整换框交接通过”分开判定。初始化通过要求完整版本化指令、首轮 `aiResponse` 含可核验恢复证据且未越权；完整交接还要求当前授权范围内必须执行的步骤实际完成、柳柳已切到新框。受暂停/未授权边界限制的巡检工作流、聊天室操作、改名等须标记 `skipped/unverified`，不能把部分恢复说成完整换框成功。初始化未通过前，昨日回顾及 `increment_usage` 等非恢复必需的写入也须暂缓。此为文档契约校准，不代表完整初始化路径已行为验证。

**阶段5封口结论与阶段6交接（2026-10-28）**：A6 现有记录对照已 PASS（范围限定）；阶段5静态一致性收敛已封口，剩余差距按阶段6准入或独立跟踪。柳柳已同意方案 A：正式换框发送完整、版本化初始化指令，并以可核验的恢复结果作为成功标准；裸密钥词不单独视为充分初始化载荷。`wovowx/mcp-memory/dev/src/skills/process/huan-kuang-liu-cheng/SKILL.md` 已加入 `SB-FRAME-1.0` 验收契约，明确输入、恢复项、来源证据、失败降级和副作用边界。A7 现有实测只证明密钥单独触发未生效；完整初始化路径仍 UNKNOWN。受当前“不得触碰聊天室相关工具”边界限制，本轮不调用 `chat_with_agent`、不追加 Operit 测试、不调用 tools/list。阶段5静态审计已封口；阶段6准入证据清单仅为预备，不代表阶段6已启动。若未来需实测正式换框路径，先明确解除对应工具操作边界，再一次性合并验证。数据库边界精确定义为：不改 schema/函数/trigger/权限、不执行 DDL；本轮仅有两类精确范围云端写入：恢复唯一工作检查点原记录状态并经 memory API 更新其内容，以及经柳柳授权只更新 `skills.name=memory` 的 description。两项均已在 CHANGELOG 与 CROSS-HOST-BRIDGE 留痕；未修改其它业务数据、未改 handler/enabled/input_schema。未部署、不推/合并 main。

#### 历史快照：阶段5文档一致性收敛（2026-10-28；其版本指针已被后续增量取代）

- 当时曾校准 `governance/真相源导航表.md` v3.26、`governance/架构差距矩阵.md` v3.7、`governance/database/schema-policy.md` v1.9、`governance/资产盘点与整理升级计划.md` v3.13、`governance/当前项目状态.md` version82 与其他文档指针。以上版本号仅是该历史批次的记录，不是当前版本；当前版本以各文件顶部和导航表为准。矩阵内早期“NOT RE-RUN”块已明确标记为历史，不再覆盖最新 fcd12b1 回归结果。路线图尾部旧 P0/Wake Bridge 任务也已标为历史快照，避免与聊天室暂停边界冲突；search_history 的20项已完成 Mock 与桥接文档未激活的 T0–T9 候选已明确区分。`mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末已追加现役状态，明确当前无 Operit 执行任务。
- 已将 schema-policy 中 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的回归明确标为历史证据，并指向最新已验证代码基线 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的五项隔离回归；差距矩阵中的旧 pending 状态已与这份证据对齐，未将文档修改冒充代码回归。
- 驾驶舱 version77 已将旧第4节 M1.2/聊天室行动地图、旧第5节阻塞表标为历史快照；第10节部署基线纠正为只读核实的 main HEAD `71f6a03ebc81` / deployment `c78ab839` / v6.35.0，版本字段语义仍单独待核。
- 已纠正资产整理计划的 A6/A7 当前状态：A6 对照待柳柳验收；A7 裸密钥独立新框测试未触发恢复；正式 SB-FRAME-1.0 路径仍 UNKNOWN。
- 本次仅修改 ZivenLab/dev 治理文档；未改 mcp-memory 源码、记忆、数据库、注册表、聊天室工具或配置；未运行测试、未部署、不推/合并 main。
- **阶段5静态审计封口完成（2026-10-28）**：剩余运行时/权限/隐私/真实端点差距不再留在阶段5反复审计，统一转入阶段6准入清单或既有独立差距追踪；阶段6尚未启动。不追加 Operit 测试，不触碰聊天室工具，不调用 Worker `tools/list`。

### 阶段 6｜整体验收与版本收口
目标：证明架构职责清晰、已有能力得到保护，且真实扩展路径可理解、可验证。
工作：分层执行静态检查、行为回归、跨宿主冷启动和真实 MCP/HTTP endpoint 验证；复核共享能力是否重复建设、扩展是否依赖无关模块改动、兼容路径是否有证据；核对 Pages 发布范围与隐私风险；整理未关闭差距和回滚说明。
验收：测试证据可复核；复用性、扩展瓶颈、兼容风险及未验证项有明确状态；发布候选范围清楚。推 main 前须报告版本/范围/验证/回滚并得到柳柳明确同意；回滚未演练不得写成已演练。

**当前准入状态（2026-10-28 封口后）**：阶段5静态审计/文档一致性范围已封口；阶段6尚未启动。A6 现有状态记录对照已 PASS（范围限定），正式换框路径仍 UNKNOWN。阶段6开始前需重锁当时 dev HEAD 与适用测试证据，并取得涉及冻结工具的具体授权。需要柳柳决策的是是否授权触碰冻结工具，不是技术记录对照的通过与否。现有 E1/E2 只证明指定 dev SHA 的隔离 Mock/本地回归通过，不证明真实 MCP/HTTP/DB 行为。Pages 隐私与发布面、记忆生命周期、权限路径、版本语义等未关闭差距按本矩阵持续跟踪；不得因文档齐全而标记为运行时通过。

**当前停点（2026-10-28 封口后）：阶段 1–4 已完成；阶段 5 静态审计/文档一致性范围已封口；阶段 6 尚未启动。** 剩余真实运行时、权限、隐私与发布面验证按阶段6准入清单或独立差距管理，不继续无限重复静态审计。 阶段4完成的含义是：现状/权威地图已对齐；已证实的重复实现做了最小收敛；当前路由、schema、注册、共享模块与兼容候选均已分类；最新隔离回归证据已回填；所有未解决差距都有明确状态、重开条件与边界。最新 mcp-memory/dev 精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的 Operit detached worktree 全量回归通过：check exit 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15。全程 mock/本地，不等于真实 endpoint/DB/RPC 验证；E3 NOT RUN、未部署、main UNCHANGED。记忆生命周期一致性、permission_guard 实际消费者、版本语义、legacy 外部契约、Pages 发布面/隐私、Router 前置白名单读取等已转为独立差距，不因阶段4完成而视作修复；聊天室硬边界继续有效。
### 明确暂缓与发布边界

- 聊天室与 Agent runtime 唤醒失败继续暂停。
- 已完成 `search_history` 最小非2xx/响应形状守门，并新增20项隔离 Mock；历史完整仓库回归 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 曾验证 E1 exit 0、webhook104/104、Router/DDL parser69/69、search_history20/20。最新完整隔离回归已推进到 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`，check0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15 全部通过。记忆生命周期审计确认 create/soft-delete/rename/move 事件与 source→target 关联缺口、update event 缺 new_value 且 version 语义冲突；详见 P1 数据安全，相关设计尚待定案。`serverInfo.version` 与 `package.json` 版本来源/语义待定义；`data.js` / `category.js` 无当前 skills 注册命中，作为 legacy 候选保留。permission_guard 实际写路径接入、Pages 发布范围、`/memory-universe` 匿名访问风险仍在矩阵。真实 E3 endpoint 未执行，不将隔离 Mock 等同于线上验证。
- `v6.35.0` 已发布并部署 VERIFIED；该版本是可靠性基线，不代表整体架构升级完成。下一次 main 发布须先说明版本、范围、验证与回滚，并取得柳柳明确同意。
- 阶段4已按范围完成；阶段5聚焦驾驶舱与跨宿主连续性闭环，阶段6负责整体验收与发布候选边界。已登记的独立风险按矩阵触发条件重开，不在本阶段偷偷扩范围。
- 本路线图控制当前行动顺序；历史 P0/P1/P2 清单仅为历史路线/待办参考，不自动成为活跃任务。
---

## 历史任务清单（旧85号行动清单快照；当前路线见上方六阶段计划）

> 以下完成项与旧 P0/P1/P2 条目均为历史状态记录，不自动构成当前活跃任务。聊天室/Agent runtime 唤醒链继续暂停；当前唯一主线仍是「一本好书」六阶段计划。

### 已完成的历史任务

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

### 🔵 P0 历史状态快照（非当前活跃主线）

### P0-2 Phase2 Ziven 消费链（Wake Bridge 改造；当前暂停）
- 历史记录：当时标为待讨论方案（Phase1 已完成，基础设施不再吞消息）；现因聊天室/Agent runtime 唤醒链暂停，不属于当前阶段5执行范围。
- Phase2 讨论议题（GPT #502）：
  1. Ziven consumer 所有权模型
  2. Wake Bridge 在哪个状态 claim（不允许发现即 claim）
  3. 注入当前框失败怎么办
  4. delivered vs seen/read 的区别
- 完成标准：ziven 事件 created→claimed→delivering→delivered→processing→acked 全链路闭环
- 回归样本：保留的 4 条 ziven 事件（已释放 created/retry=1，不手动消费）

---

## 历史快照：架构演进蓝图（2026-09-04；非当前执行路线）

> 本节及其 P1/P2、记忆系统升级、待发批次与总执行顺序均来自旧85号行动清单，仅供追溯历史方向。当前唯一执行路线是本文上方「一本好书式架构」六阶段计划；不得据此恢复聊天室/Agent runtime 唤醒工作，也不得把旧状态当作当前待办。

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

## 历史快照：记忆系统深度升级清单（2026-10-18；当前状态以差距矩阵与工作检查点为准）

> 借鉴 Zep/Graphiti 双时间轴、Letta Skill Learning/睡眠计算、Anthropic 渐进式披露。详细设计存记忆 `⚙️/记忆系统升级设计`（可读档/复苏）。

| 优先 | 项 | 现状 | 落地 |
|---|---|---|---|
| P0 | ①激活双时间轴抗污染 | memories 表已含 valid_from/valid_to/version/supersedes_id + memory_events 审计流，但**未真正维护**（全 version=1、valid_from 默认时间戳） | 改 handleMemoryTool 写读：更新时旧行置 valid_to/archived + 新行 version+1/supersedes_id/valid_from；检索默认只回当前有效+可追溯「何时被推翻」 |
| P1 | ②自动技能沉淀 | 技能靠手工建 | 从高频动作自动提炼 SKILL.md |
| P2 | ③睡眠时计算 | 自我迭代偏手动 | 定时反思任务 |

历史记录状态（2026-10-18）：当时将①标为进行中。此状态不代表当前授权或当前执行中；记忆生命周期缺口以现行差距矩阵为准。

## 历史快照：当时的待发批次（2026-09-04；不是当前发布清单）

- deploy skill v6.4.3 命名纪律（推 dev 消息用 vX.Y.Z: 名称）——待作正式 release 练习（GPT #536）
- chat.html v2.6.0 移动端输入框布局修复（flex 竖排）——GPT #538 建议按 hotfix 处理，待柳柳拍板

---

## 历史快照：旧总执行顺序（2026-09-04；不覆盖上方六阶段路线）

```
P0 全清 ✅   P1 release_guard ✅ 已上线
架构演进：P2.1 Agent Context Read 🔵 → P2.2 ⬜ → P3 ⬜（机制已拆：Before Action + After Verification + Context Contract）→ P4 ⬜
P1-1 ~ P1-15 ⬜（P1-15 code_runner 旁线）
P2 ⬜
```

---

*Ziven×GPT #348→#540 共识，2026-09-04 11:28 首版 → 13:46 刷新。*