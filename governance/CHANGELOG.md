# ZivenLab CHANGELOG（文档仓 · 知识快照）

## [docs-2026.10.49] - 2026-10-29（dev 草稿，未发布）

### 阶段6证据收敛状态与风险决策对齐
- 最新唯一运行时证据为 `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末 2026-10-29 16:47 CST：新版 `SB-FRAME-1.0` 独立新框 `7516ae0a-23e2-4b6f-8dce-6cb4f592547f` 恢复 canonical 检查点，A7 PASS（限定本次新框与可见证据）；原始中间工具调用日志不可见，不声称拥有该日志。
- A6 完整跨宿主一致性仍 UNKNOWN：新框恢复的检查点正文存在陈旧阶段指针，且当前会话/桥接的最新状态与记忆正文未完全同步。不能只凭两边读到同一 canonical key 就判一致，也不擅自改写业务记忆。
- 阶段1–5静态整理已封口；阶段6尚未总体验收。剩余外部/运行时证据包括 Worker `/mcp` 与高影响 HTTP 路由实际认证及外层 Access/WAF、真实 DB/RPC/RLS/GRANT/trigger/CAS/事务、MCP metadata 发布源、Pages Source/真实 URL。缺少权限或证据的项目保持 UNKNOWN，不以静态/Mock 代替。
- 柳柳已明确决定“无视风险”：公开 main 源文件中的旧个人样例仍作为已知事实记录，但不作为当前主线阻塞项，不主动推动 PR #319。此决定不授权合并、部署、改写历史或更改业务记忆。
- 未改 main、未合并/部署、未改 DB/schema/权限、未写业务记忆、未调用冻结工具或生产高影响端点；不重复已通过 CI 或冷启动测试。

## [docs-2026.10.48] - 2026-10-29（dev 草稿，未发布）

### 新版 SB-FRAME-1.0 独立冷启动验收完成
- Operit 已按授权执行唯一一次完整新版初始化，新框 `7516ae0a-23e2-4b6f-8dce-6cb4f592547f`，无旧对话上下文；载荷逐字取自 `mcp-memory/dev/src/skills/process/huan-kuang-liu-cheng/SKILL.md` 完整 SB-FRAME-1.0 指令。
- 新框恢复身份根、canonical 检查点 `⚙️/当前工作检查点`（精确 recall 命中、category=⚙️）、SB-1.0、导航、巡检规则、日常归档与实时 stats（285条/23分类）；跳过冻结范围，未写业务记忆/DB、未调用冻结工具、未部署/推 main。A7 升为 PASS，限定于本次无旧对话上下文新框和可见证据；A6 完整跨宿主一致性仍 UNKNOWN，阶段6未总体验收。
- 证据限制：Operit 回填的是 `read_messages` 返回的 aiResponse 自述，原始中间工具调用日志不可见；恢复结果与 canonical key/category 及既有独立 recall 佐证一致。故不宣称拥有原始工具调用日志或完整 A6 证据。详细记录见唯一桥接文末 2026-10-29 16:47 CST 条目。
- 公开 `mcp-memory/main/src/public/memory-universe.html` 仍含旧个人样例，PR #319 脱敏候选未合并；Pages Source/真实 URL、真实 Worker/DB 权限、MCP metadata 来源仍 UNKNOWN。main 未改、未部署。

## [docs-2026.10.47] - 2026-10-29（dev 草稿，未发布）

### 确认 main 上的公开源文件仍有个人样例
- 最新只读回读 `wovowx/mcp-memory/main/src/public/memory-universe.html`，blob SHA `78473d60c0536fced45ba76b62b8785c0dcadd72`；检查确认仍包含旧个人记忆样例。mcp-memory 为 public 仓库，因此可从 GitHub 源文件直接访问；不需要 Pages 实际启用就存在源代码可见风险。
- PR #319 的候选页已将样例替换为合成演示记录，静态检查通过，但 PR 仍 open 未合并。它是仅 3 个文件的 Pages 候选；main/dev compare 仍为 260 commits ahead、21 文件差异，不能把整条 dev 一揽子合入 main。必须由柳柳单独明确批准合并该候选并核对版本/范围/CI/回滚；当前未改 main、未部署。
- 已同步驾驶舱 version113、架构差距矩阵 v4.23、导航表 v3.54、资产整理计划 v3.37。
## [docs-2026.10.46] - 2026-10-29（dev 草稿，未发布）

### 锁定一次性验收、最新回归与发布边界
- 新版 `SB-FRAME-1.0` 只读/初始化行为验收已写入唯一 `CROSS-HOST-BRIDGE.md` 文末，当前 AUTHORIZED / NOT RUN；需要 Operit 按该任务创建唯一一个新框并回填真实调用日志。GPT 当前宿主没有 `chat_with_agent`/Operit 对话创建工具，因此不能冒称已代跑。
- 当前 mcp-memory/dev HEAD `fc13b9455712cfb302aab8f16872b028cbed6677` 的 learning-regression run `40838550949` SUCCESS：check PASS、webhook104/104、contracts128/128、search_history20/20、release_guard15/15、学习工件9项 PASS；Pages artifact run `40838550970` build/upload SUCCESS、main-only deploy skipped。以上不是实时端点/DB/权限验收。
- 当前 main HEAD `71f6a03ebc81193e5d88a98297ad66083d301515`、dev HEAD `fc13b9455712cfb302aab8f16872b028cbed6677`；compare main...dev 为 ahead 260、behind 0、21 files。不能把整个 dev 一揽子合入 main。Pages PR #319 仅 3 文件、open、无 review threads，候选构建已成功但部署 skipped；Pages Source 仍需有权限者确认，合并/部署须柳柳另行明确授权。
- main 的可见 branch 保护摘要为 protected=true，但 `required_status_checks.enforcement_level="off"`、contexts/checks 为空；细项保护接口仍 403。保留这一证据边界，不把它解释为不存在其他治理政策。
- 阶段6仍未总体验收：真实 Worker 认证与外层 Access/WAF、DB/RPC/RLS/GRANT/trigger/CAS/事务、MCP metadata 发布源、Pages Source/URL 保持 UNKNOWN。没有改业务记忆、DB/schema/权限、main 或部署；没有调用冻结工具。
- 本次状态同步版本：驾驶舱 version112、架构差距矩阵 v4.22、真相源导航表 v3.53、资产整理计划 v3.36、roadmap 当前状态指针已校准。
## [docs-2026.10.45] - 2026-10-29（dev 草稿，未发布）

### 新版换框初始化一次性运行时验收获授权
- 柳柳最新指令“一次性搞定全部的”被落实为一项明确、有限的执行授权：仅再执行一次新版 `SB-FRAME-1.0` 独立冷启动验收，确认初始化是否实际调用 `ziven_mcp:memory(action=recall,key="⚙️/当前工作检查点")` 并正确恢复当前主线。
- 唯一执行契约已追加至 `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末。当前状态为 AUTHORIZED / NOT RUN，等待 Operit 按该文档执行并追加真实证据；不重建第二个框、不重跑整套 CI。
- 此授权不包括 main 合并/推送、部署、数据库/schema/权限修改、生产高影响端点、Worker `tools/list` 或聊天室/唤醒链。Pages 发布仍需要有权限者确认 Source=GitHub Actions，并由柳柳另行明确授权。
- 最新 mcp-memory/dev HEAD `fc13b9455712cfb302aab8f16872b028cbed6677` 的 learning-regression run `40838550949` SUCCESS：check PASS、webhook104/104、Router/contracts128/128、search_history20/20、release_guard15/15、学习工件9项 PASS；Pages artifact run `40838550970` build/upload SUCCESS、main-only deploy skipped。上述不等于真实 runtime/DB/RPC/auth 验收。
- 发布门禁只读补充：`GET /repos/wovowx/mcp-memory/branches/main` 的可见摘要返回 `protected=true`/`protection.enabled=true`，但 `required_status_checks.enforcement_level="off"`、`contexts=[]`、`checks=[]`；dev 为 `protected=false`。细项 `/protection` 仍不可读取（403），所以只记录“当前可见摘要未显示强制 CI contexts”，不推断其他仓库治理规则。
- 当前发布范围核对：`mcp-memory main...dev` compare 为 ahead 260、behind 0、总计 21 个文件有差异；main HEAD `71f6a03ebc81193e5d88a98297ad66083d301515`，dev HEAD `fc13b9455712cfb302aab8f16872b028cbed6677`。不得把整个 dev 一揽子合入 main；Pages 候选 PR #319 仅 3 文件，仍须先确认 Pages Source=GitHub Actions，再由柳柳另行明确授权合并/部署。- 已同步驾驶舱 version111、差距矩阵 v4.21、导航表 v3.52、资产计划 v3.35。
## [docs-2026.10.44] - 2026-10-29（dev 草稿，未发布）

### 一次性架构状态收敛
- 复核 `mcp-memory` PR #319 的文件清单与 review threads：仅 workflow、README、memory-universe 页面 3 个文件；当前无 review threads。只读审查不替代 Pages Source/真实 URL 验证，PR 仍 open、未合并。
- 将当前阶段事实统一到驾驶舱 version110、架构差距矩阵 v4.20、导航表 v3.51、资产整理计划 v3.34：精确 recall 通路 PASS；初始化自动调用仍 UNKNOWN；A7 部分 PASS、A6 UNKNOWN；阶段6未总体验收。
- 将未关闭项明确分组：① Pages Source/线上 URL 与发布授权；② Worker `/mcp`/高影响路由认证和外层 Access/WAF；③真实 DB/RPC、RLS/GRANT/trigger/CAS/事务；④ MCP metadata 发布源；⑤新框初始化自动调用行为。无权限/证据的事项保留 UNKNOWN，不以静态/Mock 代替运行时通过。
- 未修改业务记忆、生产代码、数据库/schema/权限；未调用冻结工具、聊天室/唤醒链或高影响端点；未部署、未合并、未推 main。后续历史快照不自动构成授权。

## [docs-2026.10.43] - 2026-10-29（dev 草稿，未发布）

### 一次针对性检查点精确读取验收完成
- 柳柳明确授权后，Operit 执行一次最小只读调用：`ziven_mcp:memory(action=recall,key="⚙️/当前工作检查点")`；真实响应命中 canonical 完整 key，并返回 category `⚙️`。判定：精确 recall 通路 PASS。
- 结论边界：这次独立 recall 证明工具/完整 key 在 Operit 当前宿主可用，不证明 SB-FRAME-1.0 新框初始化会自动发起该调用。A7 仍部分 PASS，A6 完整跨宿主一致性仍 UNKNOWN；不重复冷启动、CI 或相同 recall。
- 已同步驾驶舱 version109、架构差距矩阵 v4.19、导航表 v3.50、资产整理计划 v3.33。未改业务记忆、数据库/schema、生产代码；未部署、未推/合并 main。
- 对 Pages 候选 PR #319 做了只读 diff/readback：仅 3 个文件（workflow、README、memory-universe 页面）；workflow 构建 `_site` 白名单且断言只含 2 个文件，部署 job 仅在 main 运行；页面使用合成演示记录并标注 `noindex,nofollow`。本次回读的 12 条记录均为通用示例，已检查的旧个人样例/健康关键词无命中。此项只是静态内容审查，不等于访问控制或线上匿名访问验证；Pages Source/真实 URL 仍 UNKNOWN，PR 仍未合并。
- 校正 roadmap 中残留的过期授权状态：明确记录精确 recall 通路已 PASS，但初始化自动调用仍未证实；移除“尚待授权进行同一次精确 recall”的旧措辞。仅文档改动，未触碰代码/业务记忆/数据库、未部署、未推/合并 main。

## [docs-2026.10.42] - 2026-10-29（dev 草稿，未发布）

### Operit 检查点读取契约调查关闭与下一步授权门槛
- Operit 侧只读 metadata 确认 `get_memory_by_title` 属于宿主顶层默认 memory-space 工具集，必填 `title` 且按精确标题查找，不按记忆 key；可选 `chunk_index`、`chunk_range`、`query`、`limit`。因此将 `⚙️/当前工作检查点` 作为 title 传入不会命中标题为“当前工作检查点”的记录。MCP 工具 `ziven_mcp:memory(action=recall,key="⚙️/当前工作检查点")` 则按 canonical key 精确读取。
- 该证据在契约层解释了 A7 读取差异；宿主工具的内部索引/实现仍 UNKNOWN。静态 metadata 调查关闭，不再重复派发；现有三份 Skill 已要求完整 key exact recall，search 仅作候选定位且不能独立验收。
- 尚无证据证明修订后的 SB-FRAME-1.0 初始化在真实新框中确实发起精确 recall。A7 仍部分 PASS，A6 完整跨宿主一致性 UNKNOWN，阶段6未总体验收。若要验证，仅做一次针对性运行时调用验收，必须另获柳柳明确授权；授权前不调用宿主工具、不创建新框、不重跑 CI，不查/写 DB，不调用 Worker `tools/list`，不写业务记忆、不部署、不推/合并 main。
- 治理指针同步：驾驶舱 version108、架构差距矩阵 v4.18、导航表 v3.49、资产计划 v3.32。未改生产代码或业务数据。

> 文档仓不假装软件发行版：版本模型 = 知识快照 `docs-YYYY.MM(.N)`（可带 baseline/snapshot 后缀）。
> 记录：知识演进（新增/决策/归档），不记每个 commit。
> 本文件已迁移至 governance/（2026-09-04 governance 目录重组）。

## [docs-2026.10.41] - 2026-10-29（dev 草稿，未发布）

### Operit 检查点读取工具契约核实（只读，不代表运行时复验）
- Operit 侧只读 metadata 核验完成：`get_memory_by_title` 位于宿主顶层默认 memory-space 工具集，与 `query_memory` 同一工具面，不是 ziven_mcp MCP server 工具；输入必填 `title`，按精确 title 查找，可选 `chunk_index`、`chunk_range`、`query`、`limit`。带分类前缀的 `⚙️/当前工作检查点` 是 key 形态，不是 title；把它作为 `title` 传入不会命中记录标题“当前工作检查点”。
- 该证据解释了 A7 新框中两种读取面的差异：`get_memory_by_title(title="⚙️/当前工作检查点")` 未命中，而 `ziven_mcp:memory(action=recall,key="⚙️/当前工作检查点")` 可按 canonical key 精确读取。宿主底层实现/索引仍不可见；本次只确认可见契约，不声称已证实全部内部过滤实现。
- 换框流程、master-router、memory-retrieval-hybrid 三份 Skill 已规定以 `ziven_mcp:memory` + `action=recall` + 完整 key 读取 canonical 检查点，失败后 search 只用于定位、不可独立验收。尚未确认初始化指令在真实新框中是否实际发起该精确调用，故 A7 仍部分 PASS、A6 完整跨宿主一致性仍 UNKNOWN。
- 静态工具契约调查已关闭，无需再次派发同项调查或重跑 CI。若要确认新框实际调用契约，必须另获针对性运行时授权；授权前不调用宿主工具、不创建新框、不查/写 DB、不调用 Worker `tools/list`，不写/改业务记忆、不部署、不推/合并 main。治理同步：roadmap、驾驶舱 version107、差距矩阵 v4.17、资产计划 v3.31；导航表更新尝试受连接器权限阻止，暂留 v3.48，后续仅在可用写入权限时更新。

## [docs-2026.10.40] - 2026-10-29（dev 草稿，未发布）

### 工作检查点读取契约最小修正与 CI 证据核对
- A7 只读调查确认：云端 canonical key `⚙️/当前工作检查点` 存在且可由完整 key 的 MCP recall 读取；Operit 新框的系统 `get_memory_by_title` 读取面未命中。该系统工具实现仍不在当前 GPT 可见工具目录或两个仓库代码索引中，根因尚不能认定。
- 不扩大查找范围、不调用 Worker `tools/list`、不再跑 A7；优先修正现有入口说明。在 `mcp-memory/dev` 的换框流程、master-router、memory-retrieval-hybrid 三份 Skill 中明确：先用 `ziven_mcp:memory` + `action=recall` + 完整 key `⚙️/当前工作检查点`；只有精确读取失败时才用 `action=search, keyword="⚙️/当前工作检查点"` 定位线索。静态源码与只读实测证实 search 格式化输出不含原始完整 key/status，故 search 结果不能独立验收；必须重试完整 key 的精确 recall，仍失败就进入受限模式。标题读取面、裸 key 与过渡副本不能代替权威记录。三文件均写入并回读验证。
- 最新 `mcp-memory/dev` HEAD `fb34371dd00f7a3339648d7a6a8fae355996ecb7` 的 `learning-regression` run `40813963598` SUCCESS：E1 `npm run check` PASS、webhook 104/104、Router/contracts 128/128、search_history 20/20、release_guard 15/15、学习工件 9 项 PASS。相同 SHA 的 Pages run `40813963599` build/upload SUCCESS，main-only deploy 在 dev 上按设计 skipped。该次仅新增桥接文档，不改生产代码；Mock/静态回归不等于真实新框验证。以上仅是静态/Mock 回归，不等于真实新框通过。
- 新增 Operit 侧静态核验任务：只读检查其现有工具注册表/工具说明/metadata 中的 `get_memory_by_title` 定义、输入 schema、title/key 语义、完整 key/分类前缀支持及实现来源；不要调用该工具，不发起真实记忆查询或新框/A7，不调用额外 API、Worker `tools/list` 或聊天室工具。若本地 metadata 无定义，报告已检查位置并停止。A7 仍部分 PASS，A6 完整跨宿主一致性仍 UNKNOWN。未写入/修改业务记忆、未改 DB/schema/生产代码、未部署或推/合并 main。已同步治理路线图、驾驶舱 version106、差距矩阵 v4.16、导航表 v3.48 与资产计划 v3.30；唯一跨宿主执行说明仍以 `mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末为准。

## [docs-2026.10.39] - 2026-10-29（dev 草稿，未发布）

### 跨宿主工作检查点读取差异核验
- 在唯一交接文档 `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末追加 GPT 侧只读调查，并修正了起初基于截断输出提出、后经 DB 行数据推翻的 valid_to 假设。
- 实时 memory stats 为 285 条/23 分类。Supabase memories 的只读查询确认 canonical key `⚙️/当前工作检查点` 只有一条匹配活动行：status=active、valid_to=null、updated_at=2026-10-29T01:37:39.013+00:00（新加坡时间 09:37:39）。同 title 另有一条旧裸 key `当前工作检查点`，category=默认、status=deleted、valid_to 已设置；精确裸 key recall 未命中与该软删除状态一致。
- GPT 侧按完整 canonical key 的 MCP recall 成功；Operit 新框（有角色卡、无旧对话上下文）报告系统 get_memory_by_title 未命中 canonical 行并回退找到过渡检查点副本。没有证据表明 canonical 云端记忆丢失；系统读取面的实现/索引/过滤契约仍 UNKNOWN。GPT 可见工具目录无该工具名，wovowx/mcp-memory 与 wovowx/ZivenLab 的代码索引搜索 get_memory_by_title、memory_by_title 均无命中，故实现来源当前对 GPT 侧不可见，暂记宿主/连接器层外部可见性阻塞。canonical 检查点正文停在 09:37，尚未包含 10:55/11:00 的新框测试结论。
- A7 更新为部分 PASS，A6 完整跨宿主一致性 UNKNOWN。同步更新路线图、驾驶舱 version104、差距矩阵 v4.14、导航表 v3.46、资产整理计划 v3.28；不重跑 A7、不委派 Operit、不写/重命名/删除业务记忆、不改 DB/schema/权限/生产代码，不部署或推/合并 main。

## [docs-2026.10.38] - 2026-10-29（dev 草稿，未发布）

### 阶段6只读准入与证据收敛（尚未总体验收）
- 复核 `mcp-memory/dev` 的 CI：源码/测试 run `40805561230`、桥接提交 run `40805938145` 与最新阶段6桥接 commit `5fac03c5950e6afc8cc5e98d3d0eab68d259a647` 的 run `40807824353` 均 SUCCESS；同 SHA Pages artifact run `40807824328` build/upload SUCCESS、main-only deploy skipped。测试覆盖 E1、webhook 104/104、Router/contracts 128/128、search_history 20/20、release_guard 15/15 与学习工件。均为静态/隔离 Mock，不证明真实 endpoint/DB/权限或完整换框路径。
- 只读核验 Cloudflare `verify_main=true` 返回 `VERIFIED`：main HEAD `71f6a03ebc81` 与最新部署 `c78ab839` 匹配。Pages PR #319 状态仍为 open、mergeable clean、未合并；候选 artifact CI 成功不等于 Pages Source 已确认或真实部署成功。
- 阶段6已开始做非破坏性核验，但不能总体验收通过：完整 SB-FRAME-1.0 冷启动需要冻结链具体授权；`/mcp` 与高影响 HTTP 路由外层认证/匿名拒绝与授权允许路径未验证；DB RLS/GRANT/trigger/CAS/事务和真实 RPC 行为未验证；Pages Source/真实 URL 未验证。没有调用高影响生产端点、Worker `tools/list` 或聊天室工具；没有 DB/schema/权限写入、部署、合并或推 main；未重复运行已通过的 Operit 测试，避免额外消耗 token。
- 文档状态同步到驾驶舱 version103、架构差距矩阵 v4.13、导航表 v3.45、资产计划 v3.27、现状架构与路线图。此记录不把静态/Mock 证据升格为真实运行时 PASS。

## [docs-2026.10.37] - 2026-10-29（dev 草稿，未发布）

### Worker HTTP 高影响路由授权边界静态审计
- 只读审查 `wovowx/mcp-memory/main/src/index.js` 及 `src/modules/mcp_router.js` 发现 `/mcp` POST 直接进入未见 caller identity auth 的 `handleMCPRequest`（Router 的 dispatch guard 只是工具/注册/schema 门禁）；另有 Northflank restart、execution session init/rotate/task、debug agent-context/deploy-status 等高影响路由在对应处理块前未见统一认证/能力授权守卫；`/upload` 亦未见入口级认证检查。
- 风险影响包括可能被未经授权触发的服务重启/执行会话或任务操作，以及上下文/部署元数据读取；但 Worker 实际部署 SHA、Cloudflare Access/WAF 与公网可达性未知，不将静态代码证据写成已证实的外部可利用事实。
- 处置：先由具备权限者核实当前部署版本与外层保护；若保护不充分，再另行授权实施 Worker 内认证与最小权限，并补拒绝/允许回归。同步更新 `governance/现状架构.md`、差距矩阵 v4.12、路线图、驾驶舱 version101、导航表 v3.44 与资产整理计划 v3.26；保留 Pages 隐私门槛独立条目。仅治理文档更改；未调用生产端点，未改 Worker/权限/DB，不触碰冻结聊天室/执行链、未推/合并 main、未部署。

## [docs-2026.10.36] - 2026-10-29（dev 草稿，未发布）

### Pages 保留决策落入差距矩阵
- 柳柳已确认保留 Pages；差距矩阵升至 v4.11，区分 dev/候选 PR 的白名单 artifact 构建成功与 main 尚未修改、未部署的状态。
- 明确剩余门槛：有权限者核验 Pages Source=GitHub Actions；之后仍需柳柳独立授权合并/部署。Worker `/memory-universe` 路由的未认证读取风险独立保留，未擅自修改。
- 同步路线图、驾驶舱 version100、导航表 v3.43 与资产整理计划 v3.25。仅治理文档调整；未推/合并 main，未部署。

## [docs-2026.10.35] - 2026-10-29（dev 草稿，未发布）

### Pages 候选与当前 dev 回归证据刷新
- 柳柳已明确决定保留 GitHub Pages；该决定不授权合并/部署。
- mcp-memory/dev 桥接提交 SHA `e444c9e7c041b1ebf4e0eeabd2550c7652cf150a` 的完整 E1/E2 run `40801256052` SUCCESS；同 SHA Pages artifact run `40801256038` SUCCESS，artifact build/upload 成功，main-only deploy job 按设计 skipped。
- 发布候选 `release/pages-retain-2026-10` SHA `fd4cf7b6e735d186869cf89dd12459e6350b5fb4` 的 Pages run `40799872572` SUCCESS；PR #319 open、未合并，仅涉及 workflow、合成演示 HTML 与 README。
- 发布 artifact 仅含 `_site/index.html` 与 `_site/memory-universe.html`；已知个人样例关键词扫描无命中。Pages source 与线上 URL 仍 UNKNOWN，须由有权限的人确认 Source=GitHub Actions，且合并/部署另需柳柳明确授权。main 未改、未部署。

## [docs-2026.10.34] - 2026-10-29（dev 草稿，未发布）

### GPT memory tool 元数据来源差距记录
- 只读检查当前账号私有插件 `Ziven_MCP`（plugin ID `plugin_asdk_app_6ad85722a6808191b55587a39c60941e`，current release `PluginRelease_d2c4b06819cc8191a05828b0258e9c7c`）的 manifest/file list：包内只有 `.app.json` 与 `.codex-plugin/plugin.json`，没有 MCP memory tool schema 或 description。
- 因此，插件包本身不是目前已证实的旧 key `复苏协议·system://boot` 文案来源。Supabase `skills.name=memory` description 与 GPT 当前可见的工具元数据是不同表面；真正来源/缓存更新路径仍 UNKNOWN。
- 为避免聊天室注册副作用，不调用 Worker `tools/list`；不盲改插件包、不改数据库或生产配置。来源差距已加入架构差距矩阵 v4.10、驾驶舱 version98、roadmap 与导航表 v3.41。

## [docs-2026.10.33] - 2026-10-29（dev 草稿，未发布）

### Pages 发布候选门槛与回滚原则
- 当前 mcp-memory/dev HEAD `37d4cd1f88a945f5fee0cf33ddf5affef54848ed` 的 E1/E2 run `40800449492` SUCCESS，Pages artifact run `40800449494` SUCCESS；构建/上传白名单 artifact 成功，main-only deploy job 按设计 skipped。
- 发布候选 PR #319 当前 SHA `fd4cf7b6e735d186869cf89dd12459e6350b5fb4` 的 Pages run `40799872572` SUCCESS。PR 仍 open、未合并；main 仍为 `71f6a03ebc81193e5d88a98297ad66083d301515`，未改、未部署。
- 桥接文档已加入明确发布顺序：先让有权限的人确认 Pages source 为 GitHub Actions，再核对 PR/CI/脱敏 artifact，向柳柳报告版本、范围、风险、验证和回滚并取得明确合并授权；合并后再验证 main deploy run 与真实 URL。
- 回滚必须保留脱敏 HTML 与白名单 artifact；不得直接恢复旧 `path: .` 全仓库发布或原个人记忆样例。Pages Settings/真实 URL 仍 UNKNOWN；保留 Pages 不构成部署授权。
- 治理指针已更新至驾驶舱 version97、差距矩阵 v4.9、导航表 v3.40、资产整理计划 v3.23。没有触碰数据库/业务记忆/聊天室工具、没有部署或推/合并 main。

## [docs-2026.10.32] - 2026-10-29（dev 草稿，未发布）

### Pages 保留候选与 CI 状态收敛
- 柳柳已明确决定保留 GitHub Pages；本决定不授权合并/推 main 或部署。
- mcp-memory/dev SHA `c25f71d1e41be36b7dc9a888c1fb60d591fc7e2f` 的完整 E1/E2 run `40799853469` SUCCESS；同 SHA 的 Pages artifact build run `40799853457` SUCCESS，deploy job 按设计 skipped。
- release candidate `release/pages-retain-2026-10` SHA `fd4cf7b6e735d186869cf89dd12459e6350b5fb4` 的 Pages run `40799872572` SUCCESS；build/上传白名单 artifact 成功，main-only deploy job skipped。workflow 使用 checkout@v7、configure-pages@v6、upload-pages-artifact@v5、deploy-pages@v5，只将首页与记忆宇宙示例页放入 `_site/`。
- PR #319 仍 open、未合并，3 个文件涉及 Pages workflow、示例 HTML 脱敏和公开仓库 README 纠正。Pages settings/source 与真实 URL 仍 UNKNOWN；main 未改、未部署。合并前须核实 GitHub Pages source 为 GitHub Actions，合并/部署仍需柳柳单独明确同意。
- 仅同步治理文档与 PR 发布候选说明；没有改云端/数据库业务记忆、聊天室工具、DB/schema/权限，没有部署或推/合并 main。

## [docs-2026.10.31] - 2026-10-28（dev 草稿，未发布）

### Pages artifact 在 dev 上构建验收通过（不部署）
- `.github/workflows/pages.yml` 现在在 push 到 `dev` 或 `main` 时都构建并上传最小 `_site/` artifact；只有 `main` 分支会执行 deploy job。这样可在不部署的前提下，提前验证 Pages 页面构建和隐私断言。
- bridge HEAD `7eabe99ee5c043cc837e3606769c60fadc02008d` 的 `learning-regression` run `40660621011` SUCCESS；同 SHA 的 Pages workflow run `40660621137` SUCCESS，`Build and validate Pages artifact` 完成，`Deploy Pages (main only)` 因 dev 分支按设计 skipped。
- 构建合同检查 artifact 只含 `index.html` 与 `memory-universe.html`，且后者含合成示例标记、不含已知个人样例标记。该验证不证明 GitHub Pages 设置已启用或真实 URL 可访问。
- 柳柳已确认保留 Pages；main 未改、未部署。正式发布前仍须先报告版本/范围/验证/风险/回滚并取得明确同意。

## [docs-2026.10.30] - 2026-10-28（dev 草稿，未发布）

### Pages 保留决策与最小发布范围准备
- 柳柳已明确决定保留 GitHub Pages。
- `mcp-memory/dev/.github/workflows/pages.yml` 已准备为 main push 触发、最小权限、并发取消、`configure-pages@v5` 与 `upload-pages-artifact@v5` / `deploy-pages@v5`；runner 仅生成 `_site/index.html` 与 `_site/memory-universe.html` 并上传白名单目录，避免发布整个仓库。
- `src/public/memory-universe.html` 中原硬编码个人记忆样例已换成合成演示数据并加 `noindex,nofollow`；没有改动任何真实云端/数据库记忆。
- mcp-memory/dev 最新 HEAD `8306a42c10a0d686bfd79371367f203044fc1958` 的完整自动 E1/E2 run `40659261645` SUCCESS；Pages workflow 修改对应 run `40659233295` 也 SUCCESS。该 CI 仅验证主代码静态/Mock 回归，不代表 Pages 部署成功。
- Pages settings 当前不可读，repo metadata `has_pages=false`，main 仍保留旧 workflow，未改 main、未部署。下一步是完成 dev 证据与发布/回滚清单；发布到 main 前须先向柳柳说明版本、范围、验证、风险与回滚并取得明确同意。

## [docs-2026.10.29] - 2026-10-28（dev 草稿，未发布）

### CI 自动回归闭环已修复并验证
- 修改 `wovowx/mcp-memory/dev/.github/workflows/learning-regression.yml`：去掉 `paths` 过滤，让每次 push/PR 都运行回归；保留 workflow/job 名称 `learning-regression`/`validate`；使用 `actions/checkout@v7`、`setup-node@v7`（Node 24）、`setup-python@v7`（Python 3.12），权限仅 `contents: read`。
- CI 批次包括：`npm run check`、webhook 幂等/记忆写入 Mock、Router/registry/DDL/Patch Engine contracts、search_history Mock、release_guard、学习工件 runner。
- 精确 HEAD `d962718b20f91c365ca87939e12fb62ddbdbe88b` 的 run `40655855146` SUCCESS；原始 job log：check PASS，webhook 104/104，contracts 122/122，search_history 20/20，release_guard 15/15，学习工件 9 项 PASS。环境 Node 24.21.0、Python 3.12.15。测试均为静态/本地 Mock，不代表真实 MCP/HTTP/DB/RPC 行为。
- `rulesets` GET 返回空数组，dev/main branch protection 读取均 403 `Resource not accessible by integration`，required-check 状态仍无法证实；不把未读取到当作未配置。
- 同步驾驶舱 version93、差距矩阵 v4.5、导航表 v3.36、资产整理计划 v3.19、roadmap 与唯一桥接入口。没有推/合并 main，没有部署，没有触碰聊天室/唤醒链或数据库 schema/权限。

## [docs-2026.10.28] - 2026-10-28（dev 草稿，未发布）

### Pages workflow 持续故障范围扩大（只读审计）
- 对 main 上最近两页 Actions runs 分页结果核对：最近连续 289 条 `Deploy to GitHub Pages` workflow run（2026-08-27 至 2026-10-26）全部 failure。抽查 2026-08-27 的 run `33092479438`、2026-09-10 的 run `34448495645` 以及 2026-10-25/26 的 runs `40163294520`、`40276421501`，均在 setup 阶段因依赖链使用已弃用的 `actions/upload-artifact@v3` 被自动终止，未进入部署步骤。
- GitHub 官方迁移说明要求使用 `actions/upload-pages-artifact@v3` 与 `actions/deploy-pages@v4`：https://github.blog/changelog/2024-12-05-deprecation-notice-github-pages-actions-to-require-artifacts-actions-v4-on-github-com/ 。当前未改 workflow、未 rerun、未部署。
- CI required-check 配置只读核查：`GET /repos/wovowx/mcp-memory/rulesets` 返回空数组；dev/main branch protection 查询均返回 403 `Resource not accessible by integration`。因此当前不能确认 GitHub 是否配置了 required status checks，记录为连接器权限可见性限制，不把“未读取到”误写成“未配置”。
- 重要前置风险：现有 `pages.yml` 使用 `path: .`，会将整个仓库根目录打包；`src/public/memory-universe.html` 内含硬编码个人记忆样例。只读 GitHub repo metadata 返回 `private=false`、`has_pages=false`、`homepage=null`；main 根目录无 `CNAME`/`index.html`，Pages settings 专用 endpoint 当前连接器无法读取。证据指向 Pages 当前未启用或 workflow 已过时，但旧 URL 可访问性仍未证实。`mcp-memory/dev/README.md` 原“私有仓库”表述已更正，因为仓库当前是 public；公开仓库中已提交的记忆样例本身就能从源码读取。修复前需先确认 Pages 是否仍需要、明确最小发布目录并完成隐私审查，不能只升级 action 后直接恢复全仓库发布。
- 同步驾驶舱 version92、差距矩阵 v4.4、导航表 v3.35、资产整理计划 v3.18、roadmap 与唯一桥接入口。只读核查和治理文档更新；未改源码/DB/schema/注册表/聊天室链路，不触发 workflow、不派 Operit、不部署、不推/合并 main。

## [docs-2026.10.27] - 2026-10-28（dev 草稿，未发布）

### GitHub Actions 现有结果只读核查
- GitHub 连接器现已可读取 Actions runs/jobs/steps/logs；只读检查未 dispatch/rerun workflow。`mcp-memory/dev` 在本次只读核查时的 HEAD 快照=`985c2ef4725ea04b55569a98155fde2e5d7fbccb`（之后本轮文档提交会移动 dev HEAD，未对这些文档提交重跑代码回归）；最近一次 `learning-regression` 成功 run `39922942691` 运行于旧 SHA `2c6a00ffc1f94a4a368ac4d91c7d1ef494ec5f2b`，真实 job log 显示 `npm run check` 通过、学习工件 9 项 PASS，但不能覆盖当前 HEAD。
- 当前 dev workflow 的路径过滤仅对 `tests/learning/**` 或 workflow 文件变更触发；当前 workflow 只运行学习工件 JSON 校验，不是每次提交的主代码回归。因此当前 HEAD 尚无此 workflow 提供的主代码回归结果，需登记为覆盖缺口，不将历史 PASS 当作现状。
- main 上 Pages workflow runs `40163294520`（2026-10-25）与 `40276421501`（2026-10-26）均在 setup 阶段因 action 依赖链使用已弃用 `actions/upload-artifact@v3` 而失败，未进入部署步骤。此为发布流水线基础设施阻塞，不等于主代码测试失败，也不能单独推断当前线上部署状态；Pages settings/当前部署与可见性仍待独立核实。
- 同步：驾驶舱 version91、路线图现役交接指针、差距矩阵 v4.3、桥接入口。仅更新治理/交接文档与检查点；未运行测试/触发 workflow、不改源码/DB/schema/注册表/聊天室链路、不部署、不推/合并 main。

## [docs-2026.10.26] - 2026-10-28（dev 草稿，未发布）

### CI 执行与结果读取能力盘点
- 只读核对 `mcp-memory/dev/.github/workflows/learning-regression.yml` 与 `tests/learning/run_learning_tests.py`：现有 workflow 只在学习工件或 workflow 文件变更时触发，校验 `tests/learning/*.json` 的字段、ID 唯一性与状态格式，不运行 `npm run check` 或 Router/HTTP/DB 回归。
- 当前 GPT 可用的 Ziven MCP 工具暴露 GitHub 文件、分支/PR及 Cloudflare 部署/构建日志操作，但未暴露 GitHub Actions workflow dispatch、run status/list 或 job log 读取能力。Cloudflare build logs 不是 GitHub Actions 测试结果。此次未触发 workflow、未运行测试，因此不宣称 CI 通过或失败。
- 当前结果：代码测试执行与结果读取闭环在 GPT 宿主侧未证实。已找到可用于 CI 调试的 GitHub 连接器，但尚未安装/连接；下一步连接器可用后只读核查 Actions run/status/log 能力。在连接前不假定权限/能力，不新增外部服务/权限、不派 Operit、不启动阶段6。
- 同步指针：驾驶舱 version90、导航表 v3.34、差距矩阵 v4.2、资产整理计划 v3.17。未改源码、DB/schema、注册表或聊天室链路；未部署、不推/合并 main。

## [docs-2026.10.25] - 2026-10-28（dev 草稿，未发布）

### 阶段5静态审计封口
- 按预先约定的结束条件完成封口审计：权威入口、版本指针、A6/A7证据边界、历史交接优先级与冻结边界已交叉核对；已知静态状态冲突修复或明确登记。阶段5的静态审计/治理文档一致性范围封口，不等于完整换框运行时路径通过。
- 当前指针：驾驶舱 version88、导航表 v3.32、差距矩阵 v4.0、资产整理计划 v3.15、policy-index v2.6；云端唯一检查点同步阶段5封口状态，桥接文档文末同步阶段6准入边界。
- 剩余完整 `SB-FRAME-1.0` 路径、memory 工具 metadata 来源、初始化期自动 usage telemetry、真实 MCP/HTTP/DB/RPC、权限与 Pages 隐私/发布面等，转入阶段6准入或既有独立差距，不再重复阶段5静态审计。阶段6尚未启动，当前无待 Operit 执行任务。
- 本轮只改治理/交接文档与云端检查点；未改源码、DB/schema/注册表/聊天室链路，未运行测试、未部署、不推/合并 main。既有代码回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 不覆盖本轮文档提交。

## [docs-2026.10.24] - 2026-10-28（dev 草稿，未发布）

### 阶段5现役状态指针与工作检查点收敛
- 云端唯一检查点 `⚙️/当前工作检查点` 已经 memory API 更新并回读确认：A6 统一为静态记录对照 PASS（范围限定），当前文档版本指针同步为驾驶舱 version87、导航表 v3.31、差距矩阵 v3.9、policy-index v2.6、资产整理计划 v3.14；完整 `SB-FRAME-1.0` 路径仍 UNKNOWN。
- `governance/roadmap.md` 增加现役交接指针；驾驶舱更新到 version87；导航表更新到 v3.31。阶段5仍只做静态文档一致性与差距收敛，阶段6未启动。
- `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末增加更晚的权威状态指针，明确当前无待 Operit 执行任务；较早章节中的 2026-10-23 E1/E2 请求与命令为历史记录，不构成当前任务或授权。旧正文保留供追溯，文末最新状态优先。
- 最新已验证代码回归仍绑定 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`；后续文档提交未重跑测试，该 SHA 不代表当前 dev HEAD，也不证明真实 MCP/HTTP/DB/RPC 行为。本轮未分派 Operit、不追加测试、不改源码/数据库/schema/注册表/聊天室工具、不部署、不推/合并 main。

## [docs-2026.10.23] - 2026-10-28（dev 草稿，未发布）

### 阶段6准入证据清单预备（阶段6未启动）
- `governance/架构差距矩阵.md` 升至 v3.9，新增阶段6准入清单：权威状态一致性、正式启动前重新锁定代码基线、A6/A7与 SB-FRAME-1.0 状态、冻结工具授权门槛、一批式验证、未关闭差距、发布候选与回滚证据。
- A6 结论：现有跨宿主状态记录对照未发现冲突，故静态对照 PASS（范围限定）；该结果不覆盖运行时硬门禁、冷启动或真实 MCP endpoint。A7 裸密钥自举未触发，完整 SB-FRAME-1.0 路径仍 UNKNOWN。
- `governance/真相源导航表.md` 升至 v3.30，指针同步差距矩阵 v3.9；驾驶舱 version86。
- 静态复核又发现 `现状架构.md` 仍把 A6 写成待柳柳验收、`policy-index.md` 的 Database Guard 仍将 SHA `d41d6cdf...` 称为最新回归；已分别校正为 A6 静态记录对照 PASS（范围限定）与最新完整隔离回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`。`policy-index.md` 升至 v2.6；真实 RPC/endpoint/DB 权限仍未验证。
- 本轮仅改治理文档与 mcp-memory/dev 跨宿主桥接文档，不启动阶段6；未运行测试、未改源码/数据库/业务记忆/聊天室工具，不部署、不推/合并 main。

## [docs-2026.10.22] - 2026-10-28（dev 草稿，未发布）

### 阶段5/6边界与子计划指针最终同步
- `governance/资产盘点与整理升级计划.md` 升至 v3.14：明确阶段5当前仅进行不触碰聊天室/运行时写路径的静态文档一致性验收，阶段6尚未启动；预整理准入证据不代表阶段6开始。
- `governance/真相源导航表.md` 升至 v3.28，资产整理计划版本指针同步为 v3.14；驾驶舱升至 version84。
- 仅治理文档调整；未运行测试、未改代码/数据库/记忆/聊天室工具，不部署、不推/合并 main。

## [docs-2026.10.21] - 2026-10-28（dev 草稿，未发布）

### 阶段5静态审计：旧路线隔离与回归指针修正
- `governance/roadmap.md` 的旧85号行动清单虽已有历史父标题，但尾部架构演进蓝图、记忆系统升级“进行中”状态、待发批次与总执行顺序仍可能被单独摘读成现役任务；现已逐项明确标为历史快照，当前唯一执行路线仍是上方六阶段计划。未删除历史材料，也未恢复聊天室/Agent runtime 唤醒链。
- `governance/真相源导航表.md` 升至 v3.27，修正 `search_history` 行仍指向历史 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的问题，统一指向最新完整隔离回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`，同时保留“Mock不代表真实表/endpoint验收”的边界。
- 驾驶舱升至 version83；仅文档静态一致性校正，未运行测试、未修改源码/数据库/记忆/聊天室工具，不部署、不推/合并 main。

## [docs-2026.10.20] - 2026-10-28（dev 草稿，未发布）

### 阶段5文档一致性校准（只读证据对齐，不新增运行时结论）
- 校正 `governance/真相源导航表.md` 至 v3.26：同步驾驶舱 version82、架构差距矩阵 v3.7、现状架构 2026-10-28 状态，并更新 Schema Policy v1.9、资产整理计划 v3.13 的当前版本指针。驾驶舱旧 M1.2/聊天室行动地图已明确标为历史快照，避免与当前 roadmap 主线冲突。
- `governance/database/schema-policy.md` 升至 v1.9：将 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的最新完整隔离回归与较早 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的历史回归分开表述；真实 RPC/endpoint/DB 权限/DDL 仍未验收。
- `governance/资产盘点与整理升级计划.md` 升至 v3.13：修正 A6/A7 状态，A6 现有记录对照待柳柳验收；A7 裸密钥独立新框实测未触发恢复，完整 SB-FRAME-1.0 路径仍 UNKNOWN。
- `governance/架构差距矩阵.md` 升至 v3.6：将 GitHub 路径、release_guard、Patch Engine 先前的 E1/E2 pending 状态校准至最新完整回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`；旧 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 与 `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 保留为历史证据。真实 endpoint/DB/RPC 仍未验收；阶段1–3和阶段4早期的 NOT RE-RUN 块已标作历史状态快照。
- `governance/roadmap.md` 尾部原 P0（进行中）/P0-2 Wake Bridge 改造被明确改为旧85号行动清单历史快照。聊天室/Agent runtime 唤醒链继续暂停，该旧任务不再显示为当前阶段5活动任务；没有删历史任务，也没有恢复其执行。
- `governance/架构差距矩阵.md` 升至 v3.7：将 search_history/suggest 节由旧的“下一步才需补测试”改为已完成的 Mock 验收契约说明，引用最新完整回归 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的20/20结果；同时明确桥接文档 T0–T9 是另一个未激活候选，不能因为本节已有20项 Mock 测试就自动启动或冒充已完成真实 endpoint 验收。
- `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末追加 2026-10-28 现役状态：当前无待 Operit 执行任务，历史交接块不自动构成授权。聊天室/唤醒链与 Worker `tools/list` 继续冻结。
- 驾驶舱 version77 将旧第4节 M1.2/聊天室行动路线、第5节旧阻塞表标为历史快照，并把第10节错误的 v6.57.2 “当前基线”修正为已只读核验的 v6.35.0 部署基线（main HEAD `71f6a03ebc81`、deployment `c78ab839`、verify_main=VERIFIED）；版本字段语义仍列作未关闭差距。
- `governance/现状架构.md` 核对日期改为 2026-10-28；将当前阶段统一为阶段1–4完成、阶段5进行中、阶段6未启动；旧 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 回归明确改为历史批次，最新隔离回归基线指向 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`；对 memory alias、data/category 等留存项明确为未关闭兼容差距，不把阶段4完成误写成这些风险已经消除。
- 统一阶段边界措辞：当前仍处阶段5静态审计/文档一致性，阶段6仅可整理准入证据清单、尚未启动；已同步 `governance/roadmap.md` 与 `mcp-memory/dev/CROSS-HOST-BRIDGE.md`，驾驶舱更新至 version82，导航表更新至 v3.26。
- 本次仅修改 ZivenLab/dev 治理文档与 mcp-memory/dev 跨宿主交接文档；未改 Worker 源码、记忆内容、数据库、注册表、聊天室工具或配置；未运行测试、未部署、不推/合并 main。

## [docs-2026.10.19] - 2026-10-27（dev 草稿，未发布）

### 阶段4收尾、阶段5方案A定案与阶段6准入边界
- 新增验收语义区分：`初始化通过` 按 SB-FRAME-1.0 判断完整版本化指令与首轮可核验恢复证据；`完整换框交接通过` 另要求授权范围内必须执行的交接步骤完成、柳柳已切到新框。master-router 自举序列同步区分只读恢复与按授权执行的巡检接管，并在 SB-FRAME-1.0 初始化成功前暂停昨日回顾及其记忆/Skill/日期主动写入，不手动调用 increment_usage；但当前 router 的 autoIncrementUsage 仍会在成功 tools/call 后更新 skills.usage_count/last_used，Skill 不能保证严格零 DB 写入。该运行时缺口本轮不修，因为 router 同时承载聊天室注册/唤醒路径。跨平台复苏手册现为 v1.4：裸密钥仅是恢复提示；完整初始化须报告身份根、检查点、授权边界、stats、来源与失败/跳过/未知项；核心恢复不完整则进入受限模式；并揭示 `src/modules/mcp_router.js:autoIncrementUsage` 的成功调用后自动 usage telemetry，故 Skill 指令不能保证严格零 DB 写入。补充待查项：当前 GPT 会话暴露的 memory 工具 description 仍指向旧 `复苏协议·system://boot`，而此前获授权修改仅覆盖 Supabase `skills.name=memory` 行；元数据发布源/更新权限待确认，本轮不改插件元数据。云端 `⚙️/恢复协议·Session Bootstrap SB-1.0` 已按方案 A 补齐真实导航 key/fallback、初始化前只读恢复与非必要写入暂停、A6/A7 当前状态及该工具元数据差距；该记忆更新已回读确认，不代表运行时硬门禁通过。受暂停/未授权边界限制的巡检、聊天室、改名步骤标记 `skipped/unverified`，部分恢复不得表述为完整交接成功。该修正仅为 Skill/治理文档澄清，不是行为测试结果。
- 最新换框初始化 message 已显式标记 `SB-FRAME-1.0`，将授权/暂停边界放在副作用步骤前；暂停聊天室/唤醒/巡检链时跳过相关工具、工作流清理/调度与改名，不宣称完整换框已通过，并要求首轮回应列出身份/主线/下一步、实时 stats 与来源、失败/跳过/未知项。该契约已静态回读确认，仍无真实新框行为测试。
- 阶段4按其范围完成：当前实现/注册/输入契约/兼容候选均已分类，公共重复函数做了最小收敛，遗留运行时、数据库、权限、Pages 隐私风险仍保留为独立差距，不宣称已修复。
- mcp-memory/dev 精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的隔离回归已由 Operit 全绿：check exit 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15；Node v24.18.0/npm 11.16.0，stderr 空。全程 mock/本地；E3 NOT RUN、未部署、main 未变。
- 阶段5只读审计确认 memory stats/身份根/当前检查点可读；旧 boot/navigation 精确 key 未命中但 memory search 找到内容，已在 Session Bootstrap 与换平台手册中补 search fallback。Worker `tools/list` 会触发 `syncChatTools`，可能写入并启用聊天室工具，本轮未调用。
- 阶段5后续证据已更新本条早期快照：A6 现有状态/权威文档/Operit 报告对照已完成初核，待柳柳验收；A7 已于 2026-10-27 17:56 CST 在独立新框实测，裸密钥词未触发云端恢复。柳柳批准方案 A：正式换框必须发送完整、版本化初始化指令，并以可核验恢复结果验收；换框 Skill 已加入 SB-FRAME-1.0 契约。随后回读完整 message，补入此前清单遗漏的 memory 位置导航、Session Bootstrap 和导航 key 的 search fallback；并在 master-router Skill 中把裸密钥明确为恢复提示而非初始化成功证明，更新恢复协议 key 与 fallback。随后依据实际 memory search 结果，再补充导航 fallback 的身份核验：必须确认 key/category 指向真正的导航条目，不能把仅在正文提及导航的协议或历史检查点误当导航；恢复协议 fallback 则先搜索 `Session Bootstrap SB-1.0` 并核对标题/版本。通过只读查询和精确 recall 确认导航真实 key 为 `记忆位置导航（换框/换设备自举·2026-10-18）`，category=`记忆位置导航（换框`；导航正文中的 182条/17分类是创建日的历史快照，当前统计必须以实时 memory stats 为准。只做静态 Skill 修正，未执行真实换框路径。（早期快照，已被本节后续授权更新记录取代）运行时 `skills` 表的 memory 工具 description 当时仍保留旧 `/boot` key 指示；随后已按柳柳授权更新并回读确认其余字段不变。完整初始化路径仍 UNKNOWN，因为当前不得触碰聊天室相关工具，本轮未执行真实路径验证。阶段6验收准入状态已补到 roadmap：尚未启动，须保留真实 endpoint/DB 与隐私/权限等未验证差距，不以 Mock 或文档替代运行时证据。
- 工作检查点键冲突已恢复：只读查询确认 `⚙️/当前工作检查点` 原 ID `5b0048ab-0e0e-424e-adb5-958375cd375e` 被标记 deleted 且仍占用唯一 key；已按 ID 与 deleted 状态精确恢复为 active，随后通过 memory 工具更新内容并验证标准 key 可 recall、`valid_to=null`。完整旧值另存于 `⚙️/历史检查点·2026-10-27方案A定案前`；临时默认键副本改名归档为 `⚙️/过渡检查点副本·2026-10-27键冲突修复`，没有硬删除记忆。由于状态恢复使用条件更新而非记忆 API，该次 status 恢复动作本身未单独写入 memory_events；后续内容更新仍经 memory 工具正常进入其版本链。
- 经柳柳明确授权，仅更新 Supabase `skills` 表 `name=memory` 这一行的 `description`，对齐 `⚙️/恢复协议·Session Bootstrap SB-1.0`、记忆导航 search fallback 与 `SB-FRAME-1.0`；回读确认 `enabled=true`、`handler_config` 与 `input_schema` 均未变。只更新描述文本，不代表全局运行时硬门禁已实现，也没有执行完整换框行为测试。
- 当前边界：不调用 chat_with_agent / tools/list、不改聊天室工具/注册/唤醒链，不改 DB schema/函数/trigger/权限，不部署、不推/合并 main。

## [docs-2026.10.17] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：写入响应确认与文件移动保护
- Patch Engine 在 GitHub PUT 返回 2xx 后仍要求可验证的 `content.sha`；若响应没有 SHA，或返回的 `content.path` 与已批准目标不一致，保留 proposal `applying` 并返回 `PARTIAL/UNKNOWN`，不误标为 `applied`，避免无法核对写入身份时继续自动推进状态。
- `github_move` 除了校验 source/target 路径和 tree API 返回的每个条目外，还拒绝同仓库、同分支、同路径的移动，避免目标覆盖唯一源文件后又把源删除。
- `validateRepoRelativePath()` 拒绝首尾空白与空白路径段；隔离 Mock 覆盖新增边界。**该历史状态已由 docs-2026.10.18 记录的最新精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 全量回归结果取代**：check exit 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15。仅 dev；无真实 endpoint、proposal、DB/RPC/DDL；未改 schema/registry/聊天室，不部署、不推或合并 main。

## [docs-2026.10.16] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：GitHub 路径与 Patch Engine 输入边界收敛
- 在 `src/utils/helpers.js` 增加共享 `validateRepoRelativePath()`，统一验证并按 path segment 编码 GitHub 内容路径；github_push/read/list/delete/edit/copy/move 与 Patch Engine 共用此契约。
- `github_push` 的 `content_url` 现在必须来自当前 `SUPABASE_URL` 对应的 HTTPS origin，必须位于 public-files 路径，禁止 URL credentials 并拒绝重定向，避免从其它 Supabase project 或重定向目标读取内容。
- Patch Engine now rejects proposal.target 与 patch.file 的路径不一致、危险路径、非整数行号、重叠范围、无操作 patch、多行 insert entries 与不匹配的 delete_content；分支策略拒绝 main 大小写变体和嵌套 refs/heads aliases。
- `release_guard.js` 改为只识别 canonical repository policy，移除 suffix fallback 与无 owner alias；main 大小写变体一致拒绝。受聊天室暂停范围约束，未改 `mcp_router.js`，前置白名单前的潜在只读 API 请求风险继续留存。
- **验证状态：最新代码/测试 E1/E2 NOT RUN，等待 Operit 对最新 `origin/dev` detached worktree 一次性执行；此前 Patch Engine 82/82 只对应旧 SHA，不覆盖本条新增改动。** 所有改动仅在 dev；未操作真实 GitHub/Supabase endpoint 或 proposal，未改 DB/schema/权限/注册表、未删除数据、未触碰聊天室、未部署、不推/合并 main。

## [docs-2026.10.15] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：Patch Engine apply 闭环最小实现
- `src/modules/patch_engine.js` 新增集中式目标策略：默认只允许 `dev`，`main` / `refs/heads/main` 永久拒绝，其他分支通过 `PATCH_ENGINE_ALLOWED_BRANCHES` 显式授权；目标仓库必须精确命中 `GITHUB_REPO` 或 `GITHUB_ALLOWED_REPOS`。
- `github_apply_patch` 现在先做目标策略校验；读取并验证 patch 后用 `status=eq.approved` 条件 PATCH 原子认领为 `applying`，只有返回匹配行才继续写 GitHub；成功写入后要求 `applying→applied` 的状态 PATCH 同时满足 HTTP 成功与返回行确认。
- GitHub 写入结果或状态更新结果不确定时不谎报成功；状态确认失败返回 `PARTIAL SUCCESS` 并要求先核对，避免直接重复应用。新增 Patch Engine 隔离 Mock 场景，并提供 `npm run test:contracts`。
- 当前源码/测试/治理文档写入 `dev`；另将 Supabase `skills` 表中 `github_apply_patch` 单行的 description/input_schema 元数据同步到新契约，并只读回读确认，enabled 保持 true。E1 `npm run check` 与 E2 `npm run test:contracts` 尚待 Operit 在 detached worktree 对最新 SHA 实跑。未执行真实 proposal、未访问真实 GitHub endpoint、未改数据库 schema/权限、未删除数据或触碰聊天室工具、未部署、不推/合并 main。

## [docs-2026.10.14] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：Patch Engine 分支授权策略收敛
- 为避免把 `dev` 永久硬编码成唯一目标分支，明确采用集中式分支授权策略：默认仅允许 `dev`；`main` 由独立发布审批规则保护，Patch Engine 不直接写入；其他分支默认拒绝，需经明确授权加入允许列表后才可使用。
- 新增分支应通过策略配置扩展，而不是修改 Patch Engine 核心逻辑；执行前还需校验仓库白名单、分支授权、proposal 状态及重复/并发应用条件。
- 本次只更新治理设计与验收标准，未改 Worker 源码、数据库、聊天室工具、部署或 `main`。Patch Engine 实施仍待授权；具体策略存放位置与并发原子认领方案需在改码前结合现有实现确认。

## [docs-2026.10.13] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：Patch Engine apply 闭环静态审计
- `github_apply_patch` 的公开描述/schema 声称目标分支必须为 dev，但实现仅拒绝精确 `main`，没有强制只写 dev。
- GitHub 文件 PUT 成功后，代码 PATCH `patch_proposals.status='applied'`，但未检查状态 PATCH 的 HTTP 结果或返回行数，之后仍报告完整成功。若状态更新失败，proposal 可能仍为 approved，重复调用可能再次应用 patch。
- `patch_engine.js` 的 `selfTest()` 只有3项且不在 `npm run check` 中运行；当前 tests 目录没有独立 Patch Engine 回归。此项只读登记，未调用 GitHub/Supabase endpoint、未应用 proposal、未改源码/数据库。最小修复与测试建议已记入差距矩阵 v3.0，正式改码须另行授权。

## [docs-2026.10.12] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：release_guard 仓库边界静态审计
- `mcp_router.js` 的 `githubReleaseGuard()` 在 `handleGitHubTool()` 执行 `GITHUB_ALLOWED_REPOS` 白名单校验前调用；rebase 合并路径会先根据 `safeArgs.repo` 查询 GitHub PR/commit 信息。未获允许的目标仓库可能因此先触发只读 API 请求，再由 handler 拒绝后续操作。
- `release_guard.js` 的 `detectRepoType()` 在精确匹配失败后使用后缀匹配，会把 `other-owner/mcp-memory` / `other-owner/zivenlab` 误分类为已知仓库类型。当前未证明可以绕过 handler 的最终写操作白名单，故按防御纵深风险登记，不夸大为已发生发布绕过。
- 最小修复建议：在发布守卫进行任何 API 查询前校验仓库白名单；release policy 仅匹配规范化后的明确仓库名/显式别名；补充 unknown-owner 后缀误分类与拒绝路径零 fetch 测试。当前未执行 API/运行时测试、未改源码或配置。

## [docs-2026.10.11] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：工具 schema 与 handler 必填契约静态审计
- 已确认 `cf_proxy` 无 skills 注册项且不由 `tools/list` 公布，但 Router 的 handlerMap/直接分派路径将它认作已知名称，缺 schema 时兼容放行；其 `CF_PROXY_TOOL_DEF.required=['endpoint']` 未接入 Router，空 arguments 可进入环境变量名列表模式。只读登记，不调用工具或 CF endpoint。
- 对照已启用的 `delete_branch` 与 `increment_usage`：注册 schema 均未声明 required；delete_branch 实际要求 `name || branch`，但 schema 仅声明 name；increment_usage 实际要求 name。Router 不会从 handler 推断必填参数，缺参调用会进入 handler 后返回错误；当前静态证据未显示该缺参路径执行目标写入。
- 仅同步文档，不改 Worker 源码、注册表、数据库、聊天室工具、部署或 main。

## [docs-2026.10.10] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：cf_proxy 路由与 schema 静态证据校正
- 沿 `dispatchGuard` → `isKnownTool` → `handlerMap` → `tools/call` 追踪后确认：skills 注册表无 `cf_proxy` 记录，Router 未导入 `CF_PROXY_TOOL_DEF`，因此注册表不会将它放入 `tools/list`；但 handlerMap 将其作为已知 handler，tools/call 具有直接分派分支，schema 缺失时 dispatchGuard 按兼容策略放行。代码路径因此可由已知名称直接调用，外部宿主 UI 是否允许手动调用仍未知。
- `CF_PROXY_TOOL_DEF` 声明 required endpoint，但该定义未接入 Router，故不参与参数校验；空 arguments 会进入 handler 的环境变量名列表模式。仅修正静态证据，不调用 cf_proxy 或 Cloudflare endpoint，不改代理能力、注册表、数据库、聊天室、部署或 main。

## [docs-2026.10.9] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：AI handler 职责边界只读审计
- 只读核对 `src/tools/ai.js`、`src/utils/storage.js` 与 Supabase `skills` 精确记录：当前启用的 `agnes`、`ds_quota`、`help`、`query_files`、`update_file`、`delete_file` 均使用 handler=ai；ai.js 同时分派 Agnes 媒体任务、DeepSeek 余额、通用 help 与文件 query/update/delete。`query_files` 复用 `storage.js` 的 `queryFiles`；update/delete 在 ai.js 直接调用 REST，storage.js 当前没有同名更新/删除函数。旧 `describe_image`、`generate_image`、`generate_video` 注册项 disabled；`describe_video` 没有独立注册项，但 agnes action 支持 describe_video。
- 该结果只说明当前 handler 的职责聚合与调用边界，不证明重复实现或线上故障。按“复用优先、不过度设计”原则，只登记为低优先级候选；不拆 ai.js、不改注册表、不执行 endpoint 测试。未改 Worker、聊天室、数据库、部署或 main。

## [docs-2026.10.8] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：现状证据与文档一致性收敛
- 再次校正治理导航的版本漂移：差距矩阵 v2.5、database-overview v2.4、schema-policy v1.8、domains/memory.md v1.6、资产整理计划 v3.4 与各自实际文档头部一致；将 roadmap 与资产计划中的早期生命周期盘点及旧测试批次明确标为历史快照，按当前 memory_unified.js 回读纠正 rename/move 控制流描述，避免旧版本/旧测试状态覆盖最新 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的完整回归证据。所有改动仅限 ZivenLab/dev 文档，未改 mcp-memory 代码、聊天室工具、数据库或 main。
- 非聊天室工具契约审计：`cf_proxy` 有 handlerMap/直接分派路径，但当前 skills 精确注册查询为空，Router 未导入 `CF_PROXY_TOOL_DEF`；实际宿主可见性与缺 schema 时参数校验仍未知。只登记，不修改代理能力或注册表。
- 只读比较 `wovowx/mcp-memory` main...dev，当前差异为7个文件（README、CROSS-HOST-BRIDGE、mcp_router、database、search、两份测试）；最新完整隔离回归精确 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的 `npm run check` exit 0、webhook104/104、Router+DDL parser69/69、search_history20/20，stderr空、detached worktree clean。测试全程 fetch mock，不代表真实 DB/RPC/DDL 或 MCP endpoint 验收。未部署、未推/合并 main。
- 将 `supabase_schema.schema_dump` 的实现限制核实为读取 PostgREST OpenAPI `definitions`；系统目录关系 `information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 经 query 不在公开 schema cache（PGRST205）；exec_sql 拒绝 catalog-only SELECT（P0001）。当前可见 MCP 没有独立只读 catalog 入口；不能据此断言真实 DB 无触发器。
- 按当前 Worker `src/` JavaScript、`scripts/`、现有 `tests/` 做直接符号扫描，除 `permission_guard.js` 自身定义之外，未发现 `checkCapabilityAccess` / `tool_policies` 等引用。当前 Worker MCP 主调用链未见通用 permission guard 接入；GPT App 独立工具、宿主插件/远端动态配置与 DB 内机制仍 UNKNOWN，未修改权限运行行为。
- 记录版本面并不一致：MCP `serverInfo.version=6.5.0`、`package.json=6.3.4`、CHANGELOG 最新 release 标记 `v6.35.0`、源码注释还出现 `v6.48.0`。先定义各字段的 build/package/release 语义，不为数字相同而改代码。
- 同步导航表 v2.4、policy-index v2.5、架构差距矩阵 v2.5、现状架构、roadmap 与驾驶舱 version45；修正旧的 create_patch_proposal / search_history “测试尚未执行”状态。记忆生命周期设计仍是 proposal，不实施 DB/schema/function/trigger/permission 写入；继续保留真实 trigger/RLS/GRANT/约束为 UNKNOWN。
- 新增一项只读调用链发现：当前 `skills` 查询中5个 Common Ground 工具名均缺失；`main` 与 `dev` 的 `tools/list` 都调用 `syncChatTools`，缺失时经 `addSkill` 新建且默认 `enabled:true`。因此列表读取可能副作用式地重新注册并启用聊天室工具。聊天室子项目保持暂停，本轮未调用 `tools/list`、未改 registry/DB，仅登记待处理边界。

## [docs-2026.10.7] - 2026-10-27（dev 草稿，未发布）

### 阶段 4：MCP serverInfo 版本契约差异（只读登记）
- 静态读取当前 `mcp-memory/dev`：`src/modules/mcp_router.js` 的 MCP `initialize` 响应硬编码 `serverInfo.version='6.5.0'`，同分支 `package.json` 为 `6.3.4`。该字段究竟代表 MCP server build、Worker release 还是 package version 没有明确契约。未为凑一致而改版本号；已登记到架构差距矩阵，后续先定义权威语义再决定单一来源。本轮未调用 initialize endpoint、未改 Worker 源码、未部署。

### 阶段 4：search_history 辅助路径防退化（dev，本地隔离测试20/20；完整仓库回归暂缓）
- 静态核查 `src/utils/search.js` 发现：`recordSearchKeyword` 未检查 GET 的 HTTP 状态，GET 404/500 后可能被当作空历史继续 POST；`getSearchSuggestions` 未检查非 2xx，可能把错误状态下的数组当作建议。此前已知 `search_history` 表未出现在 schema 快照，因此不建表、不改数据库。
- 已在 dev 做最小修复：`recordSearchKeyword` 只在 GET `resp.ok` 且 JSON 是数组时继续 PATCH/POST；`getSearchSuggestions` 在非 2xx 或非数组 JSON 时返回空列表，网络/JSON异常仍被隔离。空值/非字符串关键词也直接忽略。
- 新增 `tests/search_history_contract_test.mjs`，静态共20个 `check(...)` 调用点，全部使用 `globalThis.fetch` mock。覆盖空白/空值关键词、规范化与 GET→PATCH/POST、404/500不续写、网络/JSON失败、写请求非2xx、建议 prefix/limit/错误响应。该测试和源码修复是最后一次 44/44 验证之后新增。GPT 随后在本地 Node v22.16.0 对基于当前 dev GitHub readback 重建的隔离副本运行：20/20、exit 0；source/test 两文件字节大小分别与 GitHub readback 的 2672/6518 bytes 相符。这不是完整 Git worktree/SHA 运行，仅作逻辑初步验证。
- `npm run check`、webhook 104项与 Router 44项的最后一次全仓真实通过证据属于 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c`，早于 search.js 修改。GPT 已在本地 Node v22.16.0 对基于当前 dev readback 重建的 search.js/测试文件运行新测试并通过20/20；因为这不是完整 repo worktree/SHA 测试，保留该限制，但为节省柳柳的 Operit API token，暂不单独委派。若后续还有更多代码改动需要全仓回归，再合并成一次批次。未建 `search_history` 表、未调用 DDL、未写数据库；未部署、未推/合并 main。

### 阶段 4：记忆生命周期事件覆盖静态审计（只读，无代码/DB变更）
- 静态追踪 `src/tools/memory_unified.js` 的 create/update/rename/forget/move/delete/history 后确认：只有已存在记录的 update 分支写部分 `memory_events`（event_type=update、memory_id、version、old_value、actor、reason），并且先写 event 再 PATCH 当前记忆；该事件 body 未包含 `new_value`，写入的 version 是旧版本，与历史设计说明矛盾。两步为独立 REST 请求而非同一事务，若 event POST 成功但 memories PATCH 失败，会留下对应未生效更新的事件；当前没有补偿/失败事件机制。
- 新记忆 INSERT 不写 create event；软删除与回查不写 revoke/delete event；rename/move 目标新建走 INSERT，源记录软删除，均没有 rename/move/delete 事件或 source→target 关系；forget 同样只软删除。history action 先经仅查 active 记录的 `getMemoryByKey`，因此软删除记录无法按 key 查询历史事件。
- 已把结论写入 `governance/database/domains/memory.md` v1.2 与 `governance/架构差距矩阵.md` P1 数据安全：下一步需要先定义事件语义、version/source-target关联、失败态，再写隔离测试；本轮没有修改 Worker、触发器、schema、记忆或生产数据。

### 阶段 4 补充：create_patch_proposal schema / usage_count 收敛（dev，隔离回归已通过）
- 静态审计确认 `create_patch_proposal` 注册项仍为 `input_schema=null`，且 Router 专用分支原先提前 return，绕过通用 `toolOk/autoIncrementUsage`。已在 `mcp_router.js` 定义共享 schema（required: `target_file`、`change_summary`、`reason`），同时用于 tools/list 与 dispatchGuard；专用 handler 改为执行后进入统一成功判定与 usage 打点。
- `tests/router_registry_contract_test.mjs` 增加隔离覆盖：公开必填 schema、缺参在 Router 层拒绝、缺参不写 proposal/不计 usage、成功只写 fake REST、成功恰好计一次 usage；随后补入 `IMPORT FOREIGN SCHEMA` 与 `SECURITY LABEL` 缺 necessity 的拒绝测试。静态 `check(...)` 调用点现为44。Operit 于2026-10-27 08:36 SGT 在 detached 临时 worktree `/tmp/ops-ev2` 对精确 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 真实运行：`npm run check` exit 0、`node tests/webhook_idempotency_test.mjs` exit 0（104/104）、`node tests/router_registry_contract_test.mjs` exit 0（44/44，stderr 空）。worktree clean，原工作树 `/tmp/mcpmem-check` 未动。

### 阶段 4：DDL necessity gate 最小修复（柳柳已授权）
- `mcp-memory/dev/src/tools/database.js` 现在用共享的非空 `necessity` 检查保护 `create_table`、`drop_table`；`exec` 中识别常见 DDL/可执行语句关键词，在调用 `exec_sql` RPC 前拒绝缺少 necessity 的请求，并尝试列出现有表。
- `src/modules/mcp_router.js` 中 `supabase_*` 前缀不再无条件视为已知工具，而是必须命中 skills 注册表；`tools/list` 为已注册 `supabase_db` 与 `supabase_schema` 都暴露可选 `necessity` 参数；`supabase_db` action enum 未扩大，`supabase_schema` 保留原有 action enum。
- `tests/router_registry_contract_test.mjs` 新增隔离 Mock：未注册 `supabase_*` 前缀被拦；exec 中 ALTER/DROP/CREATE 等 DDL 缺 necessity 不到 RPC；经 Router 的 `supabase_schema` create/drop 缺参时不触 RPC；create/drop handler 缺或空 necessity 拒绝；只读 `SELECT 1` 保持兼容；提供 necessity 的写入路径只命中 fake `exec_sql` mock；`tools/list` 同时验证 `supabase_db` 与 `supabase_schema` 的 necessity 提示，且不开放 `supabase_db.drop_table` action。所有网络由 `globalThis.fetch` mock 接管；静态计数现为 37 个 `check(...)` 调用点。Operit 于2026-10-26 21:12 SGT 在 detached 临时 worktree 对精确 SHA `2833a94e08c23b45a0598256a486463ee5d4cf6e` 真实运行并通过37/37。
- **前一轮 DDL gate 验证**：Node v24.18.0 / npm 11.16.0；detached worktree `/tmp/ops-ev`，HEAD `2833a94e08c23b45a0598256a486463ee5d4cf6e`，`npm run check` exit 0，webhook 104/104，Router Mock 37/37。该记录保留为历史基线；当前验收以本条 44/44 的后续版本为准。
- `policy-index.md` 当前版本为 v2.2；`database/schema-policy.md` 为 v1.3。Worker dev 的隔离回归已通过，但真实 endpoint/RPC 和 GPT App 独立工具入口仍未验证。GPT App 独立直连 `supabase_schema` 工具的外层 schema 仍未声明 necessity，其是否经过 Worker Router待核。
- **剩余安全边界**：本批 necessity gate 是非空理由与常见 DDL 关键词门槛，不是 SQL parser 或批准状态的运行时验证。`create_table` 的 table/columns 和 `drop_table` 的 table 仍拼入 SQL 字符串，参数注入/多语句防护尚未审查。本轮仅把该项登记到差距矩阵与 schema-policy，未扩展源码修改；是否另立最小修复批次须先界定安全范围，且不得用真实数据库进行测试。
- 未触达真实 Supabase RPC、未执行实际 DDL/数据库写入、未修改 DB/schema/skills 注册表或生产配置；未部署、未推/合并 main。真实 RPC 权限、Pages 实际发布状态仍未验证。

---

## [docs-2026.10.3] - 2026-10-26（dev 草稿，未发布）

### 阶段 4 补充：数据库证据边界与运行契约校准
- 只读调用 `supabase_schema(action=schema_dump)` 于 2026-10-26 返回 25 张表（23 业务表 + 2 测试表），输出包含列和部分外键，但不包含触发器、RLS 或全部约束目录；没有执行数据库写入或 schema 变更。
- `database-overview.md` 更新为 v2.2；`domains/memory.md` 更新为 v1.1；`记忆两表设计.md` 更新为 v1.4；`记忆检索质量测试集.md` 更新为 v1.4。将 `memory_events` 追加式触发器、`idempotency_key` 唯一约束的 2026-10-17 历史执行/验证记录与当前 enforcement 分开陈述；检索质量测试集状态改为历史用例部分执行，未声称已全量测试。
- Router 静态复核补充发现：实时 `create_patch_proposal` 注册项 `input_schema=null`、metadata handler 为 `database`，但 Router 通过早期专门分支处理并直接 return；公开 tools/list schema 因此为 `{}`，且该路径绕过通用 usage_count 计数。差距已登记于现状架构和差距矩阵，未修改运行时代码或数据库。
- 隔离 Mock 测试当前远端静态有 16 个 `check(...)` 调用点；最后一条 registered-handler failure 断言尚未重跑，因此精确版本仍为 NOT RE-RUN。Operit 原始 16/16 报告保留但不替代对最新版文件的实际执行证据。
- 真相源导航表更新至 v1.8，资产盘点计划更新至 v2.9，`policy-index.md` 更新至 v2.1，`schema-policy.md` 更新至 v1.1；治理驾驶舱继续作为摘要，云端 `⚙️/当前工作检查点` 仍是唯一当前工作状态源。
- **运行时生效边界校正**：`policy-index.md` 不再声称 Permission Guard 已是不可绕过的硬门禁，因为当前 `src/index.js` 与 `mcp_router.js` 未导入该模块。数据库 DDL 闸门经更细的 Router/handler 静态审查发现为部分实现：`database.js` 的 `create_table` 分支要求 `necessity`，但 `drop_table` 与通用 `exec` 分支不检查；Router 对任意 `supabase_*` 前缀视为已知，schema 缺失又兼容放行，存在未注册前缀绕过专属 schema 的可能路径。外露 `supabase_schema` 签名没有 `necessity` 参数。实际 Supabase RPC 是否执行成功仍未测试；本轮未调用任何 DDL。`schema-policy.md` 已将这一状况标记为 P1，并保留“先授权再改 Worker”的硬停点。
- **Pages / memory-universe 证据补全**：静态读取 `.github/workflows/pages.yml` 确认其在 push `main` 时触发并上传整个仓库根目录（`path: .`）为 Pages artifact；`src/public/memory-universe.html` 内嵌 12 条个人记忆样例，`src/index.js` 的 `/memory-universe` 路由直接读取 main 分支页面且路由内无认证。实际 Pages 是否启用、网络层保护及匿名外部可达性仍未验证；该功能按柳柳既定暂停边界保留，本轮没有改发布配置或访问生产端点。
- 所有修改仅在 dev；无数据库写入/schema 改动、无部署、未推/合并 main；E3 与回滚演练未运行。

---

## [docs-2026.10.2] - 2026-10-26（dev 草稿，未发布）

### 阶段 4：usage_count 最小修复与 Mock 回归资产同步（2026-10-26）
- 经柳柳明确授权，在 `mcp-memory/dev/src/modules/mcp_router.js` 的 `toolOk` 失败判定中新增 `handler type not implemented` 前缀排除，修复没有可执行 handler 的 Skill 调用被误计为成功的问题。
- Operit 在本地修复版本报告：`npm run check` exit 0；`node tests/webhook_idempotency_test.mjs` exit 0（104/104）；`node tests/router_registry_contract_test.mjs` exit 0（16/16）。GPT 已回读核对远端 dev 源码和测试脚本，但未独立重跑 Node 命令。
- `tests/router_registry_contract_test.mjs` 已由 GPT 通过 GitHub 工具同步至 `mcp-memory/dev` 并回读核验；全部网络请求采用 `globalThis.fetch` mock，不访问真实 Supabase 或 MCP endpoint。
- **后续证据校正**：Operit 原始回报称新 Mock 16/16；GPT 对当前远端测试文件静态计数最初发现 15 个 `check(...)` 调用点；随后在已授权范围内补入一条已注册 `memory_remember` handler 的失败不计 usage 断言，当前远端文件静态计数为 16，与 Operit 原始 16/16 回报在数量上对齐。但补入断言后的精确远端文件尚未重新运行，仍为 NOT RE-RUN；GPT 当前不能执行该仓库的 Node 脚本。为遵守 Operit API token 成本约束，不因单一计数差异立即要求重跑；若之后确需本地运行，则与其他必要验证合并成一次任务。
- **静态事实校正**：旧盘点曾把 `memory_unified.js` 的 suggest 空态判断记为字符串拼接与 `||` 优先级缺陷；当前 dev 源码已使用条件表达式处理空结果，且既有 `tests/webhook_idempotency_test.mjs` 包含空数组、正常列表、404 JSON 错误对象、500 JSON 错误对象四项输出断言。因此该旧静态缺陷不再作为当前问题；剩余测试缺口集中在底层 `search.js` 的 `recordSearchKeyword`、prefix/limit 及网络/JSON/写请求失败行为。
- **真相源边界校正**：治理入口和导航表进一步区分 `governance/当前项目状态.md`（项目治理驾驶舱摘要）与云端 `⚙️/当前工作检查点`（唯一权威当前工作状态和下一步），避免多处维护平行“当前状态”。 README 负责指路，roadmap 负责行动顺序，现状架构/差距矩阵分别记录实现地图与未完成事项。
- **Router 注册/分派契约补充**：阶段 4 静态复核发现，`create_patch_proposal` 虽在当前 `skills` 注册记录中声明 `handler_config.handler=database`，但 `mcp_router.js` 有提前执行的专门分支，实际调用 `handleCreatePatchProposal`，不会走通用 handlerMap。该注册项同时为 `input_schema=null`，所以 `tools/list` 公开的 `inputSchema` 是 `{}`，调用时只靠专门 handler 校验三个必填字段；专门分支直接 return，还绕过通用 `autoIncrementUsage`。这些作为两项独立的公开 schema/用量统计差距登记，暂不改源码。连同 `supabase_db` 等前缀特例，说明注册 metadata 与命名分派规则必须整体审阅；这只是已确认的源码/注册差异，不据此推断线上调用失败。
- `main` 未改、Worker 未部署，E3 真实 endpoint 未运行，回滚演练未执行。该事项不代表阶段 4 整体完成；其余职责/兼容差距继续按矩阵追踪。

### 整体架构目标定案（2026-10-26，目标与阶段进度早期快照）
- 定案：六阶段整体架构升级以「像一本好书」为目标，代码复用、职责清晰、面向真实需求的可扩展性与回归保护是贯穿全程的硬性原则，不新增第七阶段。
- 明确五类工程检查：先复用再新增；职责相近才合并；沿现有清晰边界扩展且不预建万能框架；先核依赖再做最小可逆调整；以真实检查和回归证据保护既有行为。
- 阶段 2 于 2026-10-26 完成：复用 `真相源导航表.md` v1.4 建立 10 章总目录，由 `governance/README.md` 提供唯一入口。阶段 3 于 2026-10-26 完成静态实现地图：核对 `index.js`、MCP Router、共享工具模块、技能注册表与 Supabase 表清单；发现并登记 69 行 skills 注册记录（66 enabled、3 disabled）、14 行缺 handler_config.handler、memory_* 未注册别名与 schema/路由口径不一致、category/data 旧 handler 候选、permission_guard 未接入 request path 等差距。真实 MCP endpoint、权限行为与运行回归未在这个早期快照中测试。当时阶段 4 刚进入文档口径同步与隔离 Mock 验证准备；Operit 的 E1/E2 与新测试尚未执行。其后测试、usage_count 最小修复和测试资产同步均见本节上方最新阶段 4 条目。只更新 dev 治理文档，未改生产代码、数据库 schema、部署或 main。

### 阶段 4 文档口径与 Mock 验证进展（2026-10-26，较早快照；当前状态以本节上方最新条目为准）
- Operit 回填隔离 Mock 13/13、E1 `npm run check` exit 0、现有 E2 104/104，基线 SHA `096c6383079930cf1a01752c49b1653d0b08bfcb`。
- 发现无 handler 的 text Skill 返回 `handler type not implemented: text` 后仍触发 `usage_count` PATCH；仅记录缺陷，未修改源码。真实 E3 未运行；新增测试文件仍为 Operit 本地未跟踪文件，未进入远端 dev。
- 下一步需柳柳决定是否授权在 dev 对 usage_count 成功判定做最小修复。
- 将 `governance/真相源导航表.md` 升至 v1.5，同步阶段 3 的 Router/注册表快照与旧 handler 候选；进一步明确 `memory_*` 缺少注册 schema 时由当前兼容策略放行，因此是“列表不可见但可能可调用且无专属参数校验”，实际 endpoint 行为仍待测。
- 更新 `现状架构.md` 和 `架构差距矩阵.md`，标出旧 historical cockpit 对 schema 缺失拒绝行为的推断已被当前源码更正；不删除历史，仅添加明确更正。
- 阶段 4 当前只完成文档/口径同步；真实调用、权限行为与 E1/E2 尚未执行。已安排 Operit 仅新增隔离 Mock 测试并执行检查，不授权改 `src/**`、注册表、数据库/schema、部署或 main。当前仍只在 dev。

### 第一阶段：现状基线与权威来源对齐
- 更新 `现状架构.md`、`架构差距矩阵.md`、`真相源导航表.md`、`roadmap.md`、`当前项目状态.md` 与 `资产盘点与整理升级计划.md`，统一当前主线为「一本好书式架构」的第一阶段基线校正。
- 根据实际仓库读取，确认 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 位于仓库根目录且可读取，纠正历史文档中已过期的 Not Found/待重建说法；记录桥接文档内旧状态重复与当前任务口径漂移，不删除历史内容。
- 根据实际目录校正 mcp-memory 根 README 的目录与入口说明；该 README 修订仅在 `mcp-memory/dev`，尚未合并到 main。
- 将 `buildErrorResponse` 重复导出从待处理候选改为已完成事项：其删除已包含在 mcp-memory `v6.35.0`，既有 E1/E2 证据分别记录，不把本次文档整理冒充为新测试。
- `mcp-memory v6.35.0` main HEAD `71f6a03ebc81` 对应 Cloudflare deployment `c78ab839`，`verify_main=true` 返回 `VERIFIED`；本条文档草稿不推 main、不改生产代码、数据库或部署。
- 阶段 1 完成后，阶段 2 已通过复用现有导航表完成；阶段 3 继续以静态源码、路由与实时注册表证据完成主链路地图。下一阶段是阶段 4：校准文档与职责口径；动态引用/行为测试未验证项继续留在差距矩阵。

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