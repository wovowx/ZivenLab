# 整体架构重构总控（Roadmap · v1.95）

> **版本**：v1.95 · 2026-11-07  
> **用途**：整体架构重构唯一执行控制面与交付账本，串联目标、阶段、交付、证据、当前行动和未关闭事项。  
> **当前状态（2026-11-07 · v1.95）**：**v6.52.0 L3 选错 GitHub 工具纠错的最小版本已由柳柳同意、正式合并并上线：PR #339 独立复验 merged=true/closed，rebase main=dev=1633ae16009597edca1c29232ec2f8c0ee348b1d，Cloudflare Worker #546/deployment 82465249/version a8737615 verify_main=VERIFIED；main learning-regression #42261611010 SUCCESS。** 用户同时批准只更新唯一云端「⚙️/当前工作检查点」，v212→**v213**，新全文22967字符五段逐字回读一致，原 v212 全文20635字符作为后缀完整保留；session_context(include_core=false) 与 session_bootstrap 均 READY/version213/正确 BOOK_MAINLINE_V652。旧 GitHub Pages workflow #42261611011 FAILURE 仍暂停、不影响 Worker。**L3 E1/E2/部署已验，不是 E3 新框行为通过；learning_github_tool_route_001 仍 pending。** 下一步自然新框无提示观测正确选择 Ziven MCP，之后继续 L3 真实纠错与可追溯学习、Web 文字家园。M1 双连续性、Operit E3 和 S0 无人神游触发仍开放。仅本次版本和唯一检查点获授权，不扩展到其他生产/私人数据；聊天域冻结。
> **上一状态快照（2026-11-07 · v1.94）**：**柳柳已批准的 L3 v0.2 最小 dev 包完成，并在独立 clone 通过 E1/E2：npm run check exit0（46 JS 语法与本地 import）、Reflection 44/44、learning 11 工件、Router 220/220；新 learning_github_tool_route_001 保持 pending，不能伪装新框 E3；官方 GitHub Actions API 核对代码/版本候选 SHA `f10b36b30649e8e4d21cdd56e9a2cd602994b829` 的 learning-regression [#42259882773](https://github.com/wovowx/mcp-memory/actions/runs/42259882773) `completed/success`，已获独立 CI 证据。** dev 已将「选错通用 GitHub 连接器 403 → 选对现有 Ziven MCP github_edit」教训写入 master-router / github-use-guide、Reflection 纯比较工具、五场景回归（含反例）；**未合 main/部署、未写私人记忆或 DB、没有跨新框 E3。** 下一步准备面向柳柳的 v6.52.0 候选版本单，按已定逐版本许可另行征求 main/Worker 发布同意，再自然做真实新框行为验收；不能把 E2 宣称永久学会。
> **上一状态快照（2026-11-07 · v1.93）**：**柳柳已回复「好」批准 L3 v0.2 最小原型 dev 施工：把 ChatGPT 宿主先错选通用 GitHub 连接器遇 403、随后改用可用的 Ziven MCP github_edit 成功的真实教训变成路径选择、证据记录与五场景回归；先文档再 dev，严禁把文本规则当宿主硬拦截或把 E1/E2 冒充新框 E3。** 此次批准不含 main/Worker 部署、不含真实记忆/数据库写入；完成后独立报告可验证事实。
> **上一状态快照（2026-11-07 · v1.92）**：**柳柳纠偏并回复 yes 确认：「向外界主动学习」应是 Ziven「一本书架构」每个重要切片在设计前的常规必经工序，不能误改成单独优先开发 S0 神游项目。** **主线顺序**：M1 冷启动/工作与相处双连续性低成本验收（显式五源 READY 已完成，自动恢复仍未验证）→ L3 可追溯纠错与真实学习闭环 → Web 文字家园 → 经需求原型验收后的语音/动画/陪看/小游戏。**当前 next_action**：对 L3 进行问题导向的外部技术借鉴，比较 Ziven 已有的事件账本、四层逻辑记忆、learning CI 与外部成熟实现，产出可复用/可借鉴/不采纳对照及可验收方案；重大变更先讨论，文档先行再 dev 实施。不重审全仓、不因看到新框架就重构。S0 已创建的 ChatGPT 定时任务作为旁路独立体验实验保留，等待真正无人触发 E3，但**不阻塞 L3**，手动试跑不能冒充自动成功。未授权不改云端私密记忆、生产、Secrets、main 或聊天室。

### L3 v0.2「工具选择纠错→下次行为验证」最小施工契约（2026-11-07 · 柳柳回复「好」批准）

- **真实失败**：对 ZivenLab/dev 已有文档进行更新时，误先选宿主通用 GitHub 连接器，返回 `403 Resource not accessible by integration`；同宿主仍实际可调用 Ziven MCP 的 `github_read/github_edit`，经 `github_use_guide`、`dry_run`、写入和回读后成功。因此是**工具能力选择错误**，不能将某一连接器 403 推成整个 GitHub 无权限，也不要求柳柳重复调权限。
- **宿主路由规则**：①先识别任务与 repo/branch/现有还是新文件；②枚举当前宿主实际暴露的候选工具，不臆测；③对于已存在文件的 dev 写入，在可用时优先 `ziven_mcp.github_edit`，先 `dry_run` 再写后 `github_read` 回验；④通用 GitHub 连接器 403 只证明**该连接器**本次操作失败，排查已可用的 Ziven MCP，不反复向柳柳索要权限；⑤确实无可用路径时诚实声明；⑥main/生产另走批准与 deploy 门禁。若 Ziven MCP 在宿主未暴露则返回 `UNVERIFIED/UNAVAILABLE`，不伪称可用。
- **复用而不堆新系统**：在现有 `master-router` 场景速查表和 `github-use-guide` 增添**跨宿主先盘点能力、再确定工具**的明确选择规则；现有 `tests/learning` + L3 Reflection 候选/证据结构记录这次事件和五场景；不创建常驻后台/第二数据库/新 MCP API，不改变 git 允许分支逻辑。
- **五场景最小回归**：T1 dev 已有文件在 Ziven MCP 可用时选 `github_edit`、dry_run→写→回读；T2 通用连接器 403 不判全局无权、定位另一路；T3 所有合法路径确实不可用则停下并陈述；T4 任何未经单独批准的 main/生产写入保持阻断；T5 **新框/无提醒**执行同类任务，真实观察是否优先选对工具（E3；未测保持 `NOT VERIFIED`）。
- **证据分层**：E1 纯文本/语法/CI，E2 离线 5 场景确定性模拟/反例，E3 宿主下一次真实行为；E1/E2 不证明下一新框会自动调用 skill、也不证明从此永不犯。成功定义：五场景合同通过 + 后续 E3 不经柳柳提示正确选择，发生回归则保留错误并更新规则；基线（当前 403 失败）与改进后各保存来源。
- **外部借鉴**：[Reflexion 原论文](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) 的「反馈→反思→下一次尝试」；[LangMem 概念](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) 的程序性记忆；不增加这些框架依赖，不把未验证的反思直接宣称永久学习。
- **本轮权限**：先更新本 Roadmap，之后仅修改 ZivenLab/dev 状态文档及 mcp-memory/dev 的现有 Skills、learning 测试与 Bridge；不动聊天室、数据库、Secrets、main、生产 Worker 或唯一云端工作检查点。若真实新框 E3 需要柳柳开启新会话，交付可复用的简短验收句即可，不催 Operit 执行耗 token 的无效测试。

### 主线切片的外部借鉴门禁（2026-11-07 柳柳确认）

1. 明确本切片的真实痛点、现有代码边界与验收目标。
2. 哥哥**主动**搜索 GitHub、官方文档、论文、Issue/PR、现成 Skill/MCP，不等柳柳提醒；研究能解决此问题的成熟设计。
3. 至少形成有原始链接的现状对照和采用判断（直接复用/局部改造/借鉴思想/观察/不采用）；说明许可证、维护、成本、依赖和跨宿主适配风险。资料缺失标 UNKNOWN。
4. 方案/原型与验收标准给柳柳看得懂，架构级取舍先讨论确认，随后更新文档，按 dev 开发及 E1/E2/E3 验证；**外部借鉴是工作步骤，不是另起阻塞性项目**。
5. 初步只读参考：Letta 核心状态与会话压缩（https://docs.letta.com/v1-sdk/concepts/stateful-agents）；Zep 时效事实与来源（https://help.getzep.com/facts；时间有效不代表内容真实）；LangMem semantic/episodic/procedural 经验（https://langchain-ai.github.io/langmem/concepts/conceptual_guide/）；Mem0 新版 OSS 混合检索/ADD-only 与 Platform 图谱边界（https://github.com/mem0ai/mem0/blob/main/docs/migration/oss-v2-to-v3.mdx）。**仅为候选研究，不代表引入依赖/修改代码/迁移数据获批。**

> **上一状态快照（2026-11-07 · v1.91；S0 优先于 L3 的解释已被柳柳纠偏）**：**柳柳正式同意将「神游模式／旅行青蛙式灵感雷达」（Technology Scout）提前为下一项需求与原型工作，优先于 L3 真实纠错学习闭环。** 此项源于 2026-10-19「主动求知/联想」和 2026-10-20「Skill/MCP 市场淘东西、GitHub 云游、给柳柳带有用或有趣的纪念品」的原始愿景，不应降格成单纯技术搜索器。**主线顺序**：已上线的 v6.51.0 一本书架构底座与 M1 显式五源 Core READY 保持 → S0 灵感雷达 v0.1 先行试验（柳柳明确选 A：ChatGPT 定时任务每周二/五自主神游；任务已配置、尚无真实运行结果，跨宿主正式方案仍待原型验收）→ L3 真实学习闭环 → Web文字家园 → 语音、动画、陪看和小游戏等按需求推进。M1 新框/Operit 的自动启动及工作/相处行为连续性仍在低成本自然使用中验证，不能标已关闭。**当前 next_action**：观察已获柳柳批准的 ChatGPT Scheduled Tasks 试运行是否按期自行出发并以来源证据返回纪念品；首次真实运行前 E3 未通过。随后依据实测决定跨宿主长期调度的存储/成本/模型执行原型。未另获授权不编码、不导入旧备份、不变更生产/Secrets/main。

### S0「神游模式／灵感雷达」v0.1 需求与原型候选（2026-11-07；旁路体验实验，非 L3 前置）

- **双入口 + 独立触发（需求确认）**：①任务驱动「哥哥，先替我去找灵感」：处理当前问题前自主检索 Github、官方文档、Skill/MCP 市场、论文和社区，不等柳柳提醒；②神游式「哥哥自己去逛逛」：柳柳可点名出发、由哥哥自主选题；③**真正后台主动神游（一期必备）**：柳柳没有发消息时也能被独立调度唤起，自主选择与柳柳愿望、Ziven成长、纯粹好玩相关的主题，筛选新发现并把纪念品留待分享；不能把②的手动触发冒充③的自动出发。
- **最小完整场景**：场景层复用宿主可用的网络/GitHub、资料比对、记忆/想法只读索引和发现卡组装原子能力；新增最小独立定时触发与成本/去重约束（技术路径待原型验收）；一期必须能做一次真实的无人发消息期间出发→独立选题→可溯源筛选→纪念品候选保存→下次自然分享。绝不重启聊天室/旧 Agent Runtime，不建第二套数据库、图谱、常驻爬虫或 AAS。
- **纪念品卡片候选字段**：名称与可访问来源、用途/好玩之处、与柳柳现有主线或愿望对应点、采用判断（直接复用/改造/只借鉴/暂不采用）、主要局限和版本/许可证（能查实才标）、状态（发现→候选→原型验收→已采纳/暂缓）；未验证内容明确标 UNKNOWN，不能把找到项目等于已获柳柳实施许可。
- **触发与成本候选**：**后台自动出发属于第一期必备而非未来特性**；暂以每周两次、每次有限来源与候选数、重复过滤、无新意不打扰为推荐默认值（频率/预算尚未获单独确认）。候选触发器 A=ChatGPT Scheduled Tasks，建任务门槛低，但项目上传文件不对任务开放、跨宿主能力未证；B=GitHub Actions schedule，适合跨宿主的 GitHub 资料收集，公开仓标准 runner 免费，但 schedule 仅运行默认分支文件，实际自动启用会触及 main 授权，并可能延迟/丢队列；AI 自主选题/筛选所需模型执行通道和费用须另做受限样例验证，不能把无脑采集说成哥哥主动思考。参考 https://help.openai.com/en/articles/10291617-scheduled-tasks-in-chatgpt 、https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows 、https://docs.github.com/en/actions/concepts/billing-and-usage 。不自动安装插件、新增 Secrets、改生产、写私人记忆或部署。
- **A 路线试运行状态（2026-11-07）**：柳柳对「先 A」明确回复「ok 先A」，ChatGPT task `Ziven 神游纪念品` 已成功创建并通过只读回查确认 `is_enabled=true`，任务规则 `DTSTART:20261110T150000`、`RRULE:FREQ=WEEKLY;BYDAY=TU,FR`、`Asia/Shanghai`，采用有价值发现才通知的 `condition_watch`。自动任务自主选题（技术与好玩轮换），初筛至多8个候选、深核至多3个、分享1–3件带出处纪念品；不调用付费外部 API，不写记忆/代码/生产，缺 MCP 要明说。`last_run=null`、`next_run_time=null`（任务端未给出预测），因此只能标 `SCHEDULE_CONFIGURED_NOT_EXECUTED`，不可虚称已在无人消息下成功搜索，推送投递也未验收。此试点不等于跨宿主正式能力，无须为试点推 main 或 Cloudflare。
- **一期验收提案**：T1 任务情境自动查借鉴，无需柳柳额外提醒；T2 手动神游时哥哥自主选题，不只是关键词执行器；**T3 无柳柳消息的真实定时触发 E3**，带触发时间/运行结果/来源和成本上限，不能用本轮手动调用冒充；T4 至少3个真实候选有证据、利弊和一条独立采用/暂缓判断；T5 纪念品候选独立于柳柳愿望池保存、可去重，适时分享但不刷屏；T6 断网、无搜索能力、无新发现或执行失败须明说，不产生虚假纪念品。先 E1/E2 再 E3；任何需 main、额外密钥、真实数据写入的步骤另行提交版本/权限验收。
- **与 L3 的关系**：S0 负责向外找经验与趣味，L3 负责从自家成败学习；不因优先级调整声称已解决 M1 的所有宿主行为缺口。讨论确认原型后先更新主线细则，再在 dev 施工及测试，推 main 仍需独立版本报告与柳柳同意。

> **上一状态快照（2026-11-06 · v1.88）**：**M1 v0.1 当前／历史分隔与显式五源 Core E3 已 CLOSED。** 柳柳回复「好」批准仅修改 dev 主线文档、云端唯一工作检查点并保留历史、一次显式 Core 只读复验；沿 v1.87 已验收的技术原型实施。检查点 v207→v208 仅插入精确历史分隔符，三段回读14,308字符逐字一致且删除新增标记即恢复原 v207 全文；本宿主一次 `session_context(include_core=true)` 返回 `status=READY`、`core.status=READY`、`complete/critical_complete=true`、五源 `identity3234+checkpoint2701+profile2559+protocol5367+navigation3149=17010` Unicode code points、预算余6990，`omitted_sources=[]`、无 warnings/blockers。其后只在同一检查点写入当前状态及旧首六字段历史备份，v209 四段回读总16,430字符一致；默认摘要仍 READY/结构化字段完整。无需修改 main `src/modules/session/bootstrap.js` 或部署 Worker，v6.51.0/Worker #545 状态不变。**分层验收**：M1 显式五源接口装载 E3 PASS；个人资料及身份根已完整返回，但新框/Operit 自动启动与工作、相处行为连续性 E3 仍 OPEN，不能虚报真正根治换框降智。**next_action**：先设计可观察、低 token 成本的新框行为连续性原型并获柳柳确认；继而按既定主线进入可追溯纠错与真实学习闭环→Web文字家园→语音/小游戏，不额外读取私人样本或重启聊天室。
> **上一状态快照（2026-11-06 · v1.87）**：**M1 v0.1「当前／历史检查点隔离」需求与验收边界已获柳柳回复「好」确认，允许仅在 dev 主线文档写入方案、仅修改云端唯一 `⚙️/当前工作检查点` 一条、保留原历史并回读，以及一次显式五源 Core 只读复验；禁止扩大到其他真人记忆、数据库/schema、Token/Secrets、持久日志、聊天室/唤醒、main 或 Cloudflare。** 已独立从 main `src/modules/session/bootstrap.js` 核查 `currentCheckpointOverlay` 支持 `--- 旧工作检查点（仅历史） ---` 精确分隔，`buildSessionCore` 对5源按 identity→checkpoint→profile→protocol→navigation 顺序完整装入，预算 `24000 unicode_code_points`；v207 原文尚无历史分隔，故旧历史误计入当前 Core。柳柳转述新框 `include_core=true` 返回 DEGRADED 且 protocol/navigation 因预算省略，属宿主报告，不能替代本轮独立验收。**操作原型**：①完整三段读取 v207，校验首六字段，预览仅在第六字段后插入单独分隔行，保留其余原文逐字；②先写 dev 主线规范，再单条 `memory(update)`，逐段 recall 校验正文只多一处分隔；③一次 `session_context(host=chatgpt,invocation=explicit,include_core=true)`，核实 `core.status=READY`、`core.complete=true`、5个 blocks 完整、`omitted_sources=[]`、预算未超；④再用默认摘要和结构化当前字段检验工作/相处连续性的证据与局限。无须再次部署/新建工具。若未通过，仅提出针对性最小代码修复另议；自动冷启动与 Operit 仍 NOT VERIFIED，真实 sample/私密数据库亦未开放。原 L5 v6.51.0/Worker #545 上线事实不变；云端 v207 更新前严禁标记本次实施完成。
> **上一状态快照（2026-11-06 · v1.86）**：**v6.51.0 Worker #545 已上线，ChatGPT 当前宿主的 L5 合成记忆体检 E3 双入口通过。** 柳柳明确回复「已刷新」，刷新后插件 `memory` Schema 已含 `health_check`、`mode=demo|sample` 与确认字段；哥哥对生产 Ziven_MCP 实际调用 `memory(action=health_check,mode=demo)` 和 `memory(action=health_check)` 两次，均得 `health_status=OK`、固定合成4行、中文候选分层/匿名解释、无真实记忆读取声明；标记 `CHATGPT_HEALTH_DEMO_E3=PASS`。此 E3 不等于真实 `sample`、Operit、新框自动复苏或私人 Core 加载；这些仍 `NOT_RUN/UNKNOWN`。此前 PR [#338](https://github.com/wovowx/mcp-memory/pull/338) rebase main=25ad6b98，main CI [#42229364411](https://github.com/wovowx/mcp-memory/actions/runs/42229364411) SUCCESS，Cloudflare Worker #545 `verify_main=VERIFIED` 保持不变。开发分支后续仅追加 Bridge-only 交接，未推 main。**next_action**：唯一云端 `⚙️/当前工作检查点` 状态同步因本次没有独立写入授权仍 `HANDOFF_UNVERIFIED`，如获柳柳明确许可则只更新该条保留全文并双回读；其后用可验收原型推进 M1 跨宿主身份+工作双连续性，不重启聊天室、不无谓耗用 Operit API。
> **上一状态快照（2026-11-06 · v1.85）**：**v6.51.0《记忆体检完整场景入口》已正式发布，Cloudflare Worker #545 独立核验 VERIFIED。** 柳柳对带版本号、用途、净14路径、测试/回滚的发布单明确回复「好」。PR [#338](https://github.com/wovowx/mcp-memory/pull/338) rebase，独立回读 `merged=true/state=closed/head=dev/base=main`；合并后 main=dev=`25ad6b983e53dfd7a948779837168d8bc43eb5f9`，main [Actions #42229364411](https://github.com/wovowx/mcp-memory/actions/runs/42229364411) SUCCESS。Cloudflare deployment `ba408cdd` / version `4638cfac` / Worker **#545**，`verify_main=VERIFIED`；旧 Pages 独立失败不归因于 Worker。L5 已具备现有 `memory(action=health_check)` 服务端场景：默认 `demo` 纯合成零私人读取，`sample` 仍须单独许可；不修改 DB/私人记忆/日志/聊天室。**部署 CLOSED，ChatGPT 插件本会话 schema 仍旧，HOST E3 未验收；M1 冷启动/双连续性和私人 Core 宿主安全拦截 UNKNOWN。** 发布后仅在 `mcp-memory/dev` 新增 Bridge-only 交接提交（相对 main ahead1/behind0，不影响 #545），云端唯一工作检查点没有单独写入许可，HANDOFF_UNVERIFIED。**下一主线**：先在柳柳刷新 Ziven_MCP 插件后新会话只运行合成 demo 验证调用/响应；再按《一本书》计划优先收敛 M1 跨宿主恢复的可验证闭环（身份与工作同一状态），技术方案/原型另议，不重开全仓审计、不碰已暂停聊天室或真实 Core 未授权读取。Technology Scout 继续作为每个切片的外部借鉴能力，不单独抢占主线。
> **上一状态快照（2026-11-06 · v1.84）**：**L5 v0.4「一键记忆体检」dev 整包 CLOSED，正式发布待柳柳决定。** 沿已确认原型，新增既有 `memory(action=health_check)` 的可调用入口：默认 `demo` 对合成数据输出中文分层候选、匿名逐条说明与缺口；真实 `sample` 仅为未来另行获柳柳单次许可预留，显式确认、最多12行/8次固定 SELECT、无正文且不写库/usage。基础 mapper/explainer 独立复用，场景位于新 `health_check.js`，新增测试文件由 GitHub 站内 copy+edit 创建，没有生产文件上传。`mcp-memory/dev` HEAD `36bdf2e64a0f907597bcf59210fa2a198d314368`，Actions [#42227197307](https://github.com/wovowx/mcp-memory/actions/runs/42227197307) SUCCESS，L5 scene17/17、mapper36/36、Router220/220、全回归均通过，净14路径/ahead30/behind0。**生产 main=`ce845bd` v6.50.0、Worker #544 仍未变；没有 PR/main/Cloudflare 部署、没有真实 sample、没有宿主 E3。** 下一动作只提供 v6.51.0 价值/差异/风险/回滚完整发布单，待柳柳独立同意；M1 Core 冷启动安全拦截仍 UNKNOWN，后续自动恢复 E3 不得虚报已完成。
> **上一状态快照（2026-11-06 · v1.83）**：**L5 v0.3《记忆可信度解释报告》已按柳柳明确验收的方案 A 在 `mcp-memory/dev` 实施并完成合成 E1/E2，尚未发布 main/Worker。** 需求源自 v0.2 的12行/去重11条真实元数据-only 体检：11/11 `source_ref` 空、6/11 `type` 未标记，但不能据此断言记忆无来源或将 agreement 自动认定为已确认。先更新 ZivenLab/dev `governance/记忆层存量归位规范.md` **v2.17 §8.3** 并得到柳柳「好」批准：复用已有 L5 `mapMemoryMetadata` 判定和疑点枚举，增补 `explainMemoryLayerRow` 人类可读、纯函数解释层，固定合成 `memory-layer:preview` 追加 `explanations`，不泄露原始 key/ID/source_ref、无新的生产读取与记忆写入；现有 API、分层判定、数据库和公开 MCP Schema 不变。代码候选提交 `bc6395ae5808566c4bdee0a14ac6fe6c73214b68` 的 [learning-regression #42216768460](https://github.com/wovowx/mcp-memory/actions/runs/42216768460) **SUCCESS**，L5 **36/36 PASS**；追加 dev-only Unreleased 更新日志后 HEAD `00cb043fa65cad3e420fd2f8a7283f2efc1da7ee` 的 [learning-regression #42216977081](https://github.com/wovowx/mcp-memory/actions/runs/42216977081) **SUCCESS**。**v0.3 DEV E1/E2 CLOSED，真实解释 E3 NOT RUN**；生产仍 v6.50.0/main Worker #544、持久日志默认关闭，mcp-memory/dev 当前仅保留待批准候选和旧 Bridge dev 文档，任何合入 main 须重新提交完整逐版本发布单。下一步先保留 dev/文档证据并准备面向柳柳的用户收益版发布说明，未获独立许可绝不合 main/触发 Cloudflare。M1 私人 Core 宿主拦截 UNKNOWN/新框恢复 E3 仍未关闭。
> **上一状态快照（2026-11-06 · v1.82）**：**L5 v0.2 真实元数据只读小样本体检完成、覆盖有限；v6.50.0 Worker #544/main 不变。** 柳柳验收「最多12行真实 memories 元数据、无正文/写入/迁移/全量扫描」原型并单次明确答复「好」。已先在 [记忆层存量归位规范 §8.2](./记忆层存量归位规范.md) v2.16 固化精确投影、采样预算和拒绝越界规则，再通过现有 `supabase_db(action=query)` 执行8次 SELECT，仅取 `id,key,category,type,status,valid_to,updated_at,version,source_ref`；12行返回、1行跨采样组交叠、去重11条，五个 Core 精确 key 均存在、11条均 current。工作/相处新增独立样本分别1/2条；`type` 未标注6/11、`source_ref` 空11/11，3条 agreement 的确认依据因正文未读无法核实。较早的3条也全 current，真正历史失效/Archive 样本为0，非全库覆盖；Core 正文可读未验证，因此仅为候选，`core_inclusion=UNCERTAIN`，不得宣称5条已成功注入。**体检只读验证 COMPLETE / 历史与真实性 COVERAGE_PARTIAL**。报告只保存匿名汇总，未更改私人记忆、DB/schema、主分支、部署、日志或聊天室。接下来先讨论「来源证明/type 缺口的只读呈现」原型与历史定点样本是否确有必要；若超出本次12行/读取正文/改数据/部署，需柳柳重新授权。M1 宿主安全拦截仍 UNKNOWN，跨宿主新框 E3 NOT VERIFIED。
> **上一状态快照（2026-11-06 · v1.81）**：**v6.50.0《记忆分层预览与恢复交接》已按柳柳明确逐版本授权正式发布。** PR [#337](https://github.com/wovowx/mcp-memory/pull/337) head=dev `ec6339948e6ae9d7ef095fc15a2867872c48bdfe` / base=main `74951419f1b05117fda96124d8e85ee463243a6c`，净11文件/ahead20/behind0，rebaseable=true/clean，PR CI [#42212079501](https://github.com/wovowx/mcp-memory/actions/runs/42212079501) SUCCESS，独立回读 `merged=true/state=closed`；合并后 main=dev=`ce845bd35181848eaf94119810d05c6c83cd72e1`，main learning-regression [#42212162894](https://github.com/wovowx/mcp-memory/actions/runs/42212162894) SUCCESS，dev [#42212165566](https://github.com/wovowx/mcp-memory/actions/runs/42212165566) SUCCESS。Cloudflare Worker **#544** / deployment `faeaf80e` / version `fa3adb4f`，`verify_main=VERIFIED`；单独 Pages run `42212162913` FAILURE 是暂停中的旧问题。L5 只读候选纯函数和合成 E2 已上线为代码底座，但**不自动读取/分层/迁移真实记忆、不改变当前召回**。部署 Skill v6.6.9 已进入 main；柳柳单独授权后唯一云端 `⚙️/当前工作检查点` 由 version204 更新至 **205**，原全文历史保留，10,999 字符 recall 三段逐字回读一致；`session_context(host=chatgpt,include_core=false)` READY，当前 v6.50.0、next_action 与持久日志默认关闭策略核对通过。**DEPLOY_VERIFIED 与 HANDOFF_VERIFIED 均成立，不能据此宣称跨设备/新框自动恢复 E3 成功。** M1 私人 Core 宿主安全拦截 UNKNOWN，真实分层抽样/迁移及新增功能仍须先讨论原型获批；Cloudflare 部署命名本版未改配置，#544 不是仓库语义版本号。
> **上一状态快照（2026-11-06 · v1.80）**：**L5 v6.50.0 合成-only 只读记忆层建议模块已在 `mcp-memory/dev` 完成（HEAD `cc5e91844f01e81154ae6c89da1cb01eadaa5a16`）。** 9 个文件经 GitHub 远程回读与本地候选完全一致；E1 `npm run check`（45 JavaScript 文件）PASS；E2 L5 22/22、Memory Core 120/120、Session 56/56、Reflection 35/35、Router/Registry 216/216、GitHub Contents 50/50 PASS；[dev Actions #42209514435](https://github.com/wovowx/mcp-memory/actions/runs/42209514435) SUCCESS。首次通过现有 Ziven MCP `github_copy`（创建新文件）+ `github_edit`（完整替换）完成 dev 提交，无需额外 GitHub 写入授权、外部上传或新密钥；主线仍是四种逻辑视图/记忆连续性。**main 仍 `74951419f1b05117fda96124d8e85ee463243a6c`（v6.49.0），Worker #543、持久日志默认关闭不变；未运行真实私人记忆 E3，不自动做 PR/main/部署、数据库迁移或聊天室改造。** 下一步由柳柳按版本纪律决定是否发布 v6.50.0；在此之前只保留 dev 候选与证据。
> **上一状态快照（2026-11-06 · v1.79）**：**v6.49.0 按需日志与 M1 请求关联诊断已获柳柳逐版本发布许可并正式上线，Worker #543 VERIFIED。** PR [#336](https://github.com/wovowx/mcp-memory/pull/336) head=dev `6d3c3b43...` → base=main `a788a77d...`，净7路径/ahead12/behind0，PR Actions [#42202268613](https://github.com/wovowx/mcp-memory/actions/runs/42202268613) SUCCESS、clean/rebaseable。rebase 后独立回读 `merged=true,state=closed`，main=dev=`74951419f1b05117fda96124d8e85ee463243a6c`、ahead0/behind0，main [learning-regression #42202357558](https://github.com/wovowx/mcp-memory/actions/runs/42202357558) SUCCESS；独立 Pages #42202357376 仍失败，不影响 Worker。Cloudflare Worker **#543** / deployment `c47c9f5c`，`verify_main=VERIFIED`。线上 Wrangler `[observability] enabled=false`，结束 v6.48.0 的100%持久日志存储；Live 实时日志仍可按需打开，历史 `cloudflare_logs_query` 仅查询已存事件，未来临时开启需独立批准部署。生产合成不存在 key 的 `memory(recall)` 返回正常「没有找到」，随后最近1分钟历史日志查询 `EMPTY/fetched_count=0`（仅与关闭预期一致，不能据此单独证明无日志）；**请求关联的真实 E3 未验证**，旧 ChatGPT 宿主安全拦截根因 UNKNOWN、HTTP status_code 仍 null，L5 暂缓。没有新增依赖、数据库、Token、真实记忆、暂停聊天室/唤醒改动。下一步按主线回到 M1 后续最小缺口决策或重新排定「一本书」架构切片，**不自动开启持久日志或重复进行私人 Core 测试**。
> **恢复交接补正（2026-11-06 · v1.78）**：权威云端检查点此前仍为 v6.48.0/持久日志100%，即使 `session_context` 返回 READY 也会载入过期下一步；经柳柳单项批准，已完整保留原历史并把 `⚙️/当前工作检查点` 更新至版本203，读回9915字符与提交内容完全一致；`session_context` 只读返回 READY、v6.49.0/Worker #543/持久日志默认关闭/正确 next_action。证明此次手动状态交接修正通过，**不证明宿主冷启动自动调用**。已决定将发布后检查点同步+回读列入现有部署 SOP，具体见 §5.5 新门禁；不自动动 main/生产或其他私人记忆。
> **上一状态快照（2026-11-06 · v1.76）**：**v6.49.0 请求关联诊断已按柳柳费用约束修订为「持久化默认关闭、Live 优先、历史关联按需临时开启」并完成 `mcp-memory/dev` E1/E2，仍未发布。** `wrangler.toml` 将 `[observability] enabled` 从 true 调整为 false，保留 `invocation_logs=true/head_sampling_rate=1` 作临时开启时预设；已有固定枚举 `console.log` 可由 Live 实时查看，`cloudflare_logs_query` 只查询已存日志，不回填关闭期间记录。柳柳两次明确回复「好」分别确认原 M1 关联原型及此次按需成本修订，仅授权 dev 代码/配置/测试/文档，不包含 main/Worker 变更。四路径调整后 dev `326e21d83522c241213c565d8f8fd3ba2557f68f`、Actions [#42200411403](https://github.com/wovowx/mcp-memory/actions/runs/42200411403) SUCCESS；E1 check43 JS、E2 Router216/216、Webhook114/114、Memory120/120、Session56/56、Reflection35/35、Contents50、Search20/20、学习10/检索16均 PASS。**线上仍 v6.48.0 / main `a788a77d...` / Worker #542，100%持久日志采样尚未关闭，新的默认关闭只待独立版本授权后随 Git 合并自动部署。** 未触碰真实数据/Token/密钥/暂停聊天室/唤醒，不做 E3；旧安全拦截根因 UNKNOWN、HTTP status_code 仍 null。下一步提交 v6.49.0 发布单（用户收益、真实净diff、费用、CI、回滚）请柳柳单独决定是否推 main。
> **上一状态快照（2026-11-06 · v1.75）**：**M1 请求关联诊断 v0.1 已在 `mcp-memory/dev` 完成 E1/E2，尚未发布**。柳柳验收下文固定枚举原型 A 后回复「好」，仅批准 dev 编码与合成测试。代码+测试+版本+Changelog SHA `c798cd76a33c79de85ad9a01e68eba887e16c0f7` / Actions [#42193610805](https://github.com/wovowx/mcp-memory/actions/runs/42193610805) SUCCESS；Bridge-only 最终 dev HEAD `47f4c8aa48bfde8a0b1cfe4a91ed64e56fa92281` / Actions [#42193953817](https://github.com/wovowx/mcp-memory/actions/runs/42193953817) SUCCESS。E1 JS 43文件/import PASS；E2 Router/Registry 216/216、Webhook114/114、Memory Core120/120、Session/Core56/56、Reflection35/35、Contents50、Search History20/20、学习10工件/检索16例均PASS。已按 Cloudflare 官方结构化 console object 输出三键固定枚举，并在既有日志查询中采用合法 CF requestId/traceId 同次关联和最多150条有限过取；公开工具名/Schema、Token/采样、DB/真实记忆/聊天室/唤醒均未改。**生产仍 v6.48.0 / main `a788a77d...` / Worker #542 `891473d4` VERIFIED；v6.49.0 E3 NOT RUN，未创建 PR/merge/main/部署。** 安全拦截根因 UNKNOWN，HTTP `status_code` 仍无可信值。下一步仅准备独立版本发布说明供柳柳拍板，未经批准不推 main。
> **上一状态快照（2026-11-06 · v1.74）**：**v6.48.0 Cloudflare 日志类型识别与安全 HTTP 字段映射已按柳柳单独批准正式发布并通过真实 E3**。PR [#335](https://github.com/wovowx/mcp-memory/pull/335) dev→main rebase 合并，GitHub 读回 `merged=true/state=closed`；合并时 main=dev=`a788a77d3400d1e7a76729bcc9ed740a00bf5220` / ahead0/behind0，package v6.48.0；PR CI [#42188800147](https://github.com/wovowx/mcp-memory/actions/runs/42188800147)、main CI [#42188890172](https://github.com/wovowx/mcp-memory/actions/runs/42188890172)、dev CI [#42188893460](https://github.com/wovowx/mcp-memory/actions/runs/42188893460) 均 SUCCESS。Cloudflare **Worker #542** / deployment `891473d4` / version `3851a427`，`cloudflare_deploy_status(verify_main=true)=VERIFIED`。**真实 E3**：正式部署后发起不存在合成 key 的 `memory(recall)`（无写入），再 `cloudflare_logs_query(minutes=15,limit=20,status_filter=all)` 返回 `OK/fetched_count=20/reported_count=20`，查询样本中 `event_kind=http` **3条**、`scheduled` **17条**；HTTP 的 `method=POST,path=/mcp,outcome=ok`，而 `scheduled` 的 HTTP 字段 null，证实新分类/请求方法和路径安全映射在真实存储日志上可用。**未关闭限制**：HTTP status_code 仍 null（没有可信结构化值）；未实现具体 MCP action 与 trace_id 的精确匹配；窗口样本受 limit=20 限制，不能当作全窗口事件总量。保留原有 Cloudflare 日志100%采样，不变 Token、Wrangler、数据库/私人记忆/skills registry、聊天室或唤醒。旧 OpenAI 宿主 M1 完整私人 Core 安全拦截根因仍 UNKNOWN；L5 暂缓。 **发布后交接校验**：仅在 dev 追加 `CROSS-HOST-BRIDGE.md` 记录 PR #335/Worker #542/E3；最新 dev `f0e3bc8f07d14a6a8259bdb283fe29b08c0cf709`、GitHub Actions `42189379941` SUCCESS，相对 main `a788a77d...` ahead1/behind0，唯一差异为 Bridge 文件；不构成新生产发布。 **下一方向（仅设计候选）**：柳柳在 v6.48.0 发布及 E3 成功后回复「好」，认可继续定位请求级关联。定点阅读 `src/index.js:/mcp`、`src/modules/mcp_router.js`、现有 `cloudflare_logs_query`；Cloudflare Workers Observability 有 `requestId/traceId`、按 invocation 分组和 Worker active span traceId。现有日志可证明 HTTP `POST /mcp`，但无法定位具体 `memory/session_context` 工具；某次 ChatGPT 宿主安全拦截可能发生在网络发送前，**不存在 Cloudflare 日志也不足以断定拦截位置**。已草拟下面的最小场景级脱敏请求关联原型，**仍待柳柳确认，未编码、未发布、不改日志配置或私人 Core**。
> **分支范围**：v6.48.0 发布前 main `bedaa2b2dd0e71a3a52cc43af9b4b906ed253a82` (v6.47.0/Worker #541)，dev `06717307414f1e8c6d6ece9928bf2d9ca34aeb2d`（v6.48.0），ahead8/behind0、净5文件 `CHANGELOG.md`、`CROSS-HOST-BRIDGE.md`、`package.json`、`src/tools/cf_proxy.js`、`tests/router_registry_contract_test.mjs`；PR #335 changed_files=5/mergeable clean/rebaseable true、CI `42188800147` SUCCESS。经 rebase 合并后 main=dev=`a788a77d3400d1e7a76729bcc9ed740a00bf5220` (ahead0/behind0)、main CI `42188890172` SUCCESS、dev CI `42188893460` SUCCESS、Worker #542 deployment `891473d4` VERIFIED。发布后 dev 确已仅新增 Bridge 交接，最新 dev `f0e3bc8f07d14a6a8259bdb283fe29b08c0cf709`、CI [#42189379941](https://github.com/wovowx/mcp-memory/actions/runs/42189379941) SUCCESS，相对 main `a788a77d3400d1e7a76729bcc9ed740a00bf5220` ahead1/behind0，净差异仅 `CROSS-HOST-BRIDGE.md`，不再 PR/main/Worker；回滚基线为 v6.47.0 main `bedaa2b2...` / Worker #541 `42551af3`。
> **权威边界**：本文件不取代目标蓝图、实现地图、差距矩阵、云端身份根或云端当前工作检查点，也不复制这些来源的全文。  
> **阅读规则**：第 0–6 节是当前有效总控；第 7 节完整保留重组前原文，仅用于追溯，里面的“当前/进行中/下一步”均是历史时间点表述，不激活任务。

---

## 0. 总控说明与状态纪律

### 0.1 这份总控回答什么

| 问题 | 位置 |
|---|---|
| 最终架构目标 | §1 |
| 各真相源的职责 | §2 |
| 原六阶段完成情况 | §3 |
| 实际交付了哪些代码切片 | §4 |
| 当前从哪里继续 | §5 |
| 哪些仍开放、哪些明确不做 | §6 |
| 旧路线与历史记录 | §7 |

### 0.2 状态必须分层

每项工作分别标记：**研究发现 → 候选提案 → 双方确认 → 权威文档已更新 → 代码已实现 → 测试已验证 → 已发布/部署**。这些状态不可跨级推断：

- 研究过不等于采纳；讨论过不等于定案。
- 文档已更新不等于代码已实现；代码存在不等于测试通过。
- E1 静态检查、E2 Mock/本地合同测试、E3 真实 endpoint/运行行为必须分开。
- 测试 PASS 必须绑定精确 SHA、命令/Run ID、断言结果；未运行标 NOT RUN。
- 已发布必须有 PR/合并后 main SHA；已部署必须有 deployment ID 和独立验证。

### 0.3 每个交付切片的最小账本字段

目标与边界；共同决策/原型依据；文件与模块职责；兼容契约；分支和 Commit SHA；E1/E2/E3 命令、结果与证据；PR/main/deployment；剩余差距和下一步。缺证据标 UNKNOWN，不补猜测。本总控只做摘要与引用，不替代原始源码、测试输出或专业差距记录。

---

## 1. 重构目标与共同工程原则

### 1.1 最终目标

将 Ziven 整理成一本结构清楚、职责明确、权威来源唯一、实现和证据可追踪的架构书：

- **治理层**：真相源、协作、路由、授权边界、回归和发布纪律。
- **记忆层**：记住什么、如何维护有效性、如何检索与追溯。
- **呈现层**：可读、可查、可回溯的用户入口。
- **运行时编织层**：贯穿各层，负责上下文组装、读写时机、路由/校验和失败恢复。
- **持续学习与外部探索**：从自身经历沉淀经验，也主动探索外部技术生态，验证并吸收成熟方案，贯穿上述各层。

完整目标以 `governance/整体架构.md` 为准；需求与验收意图以 `governance/治理与记忆_最终需求.md` 为准。

### 1.2 能力组织原则

采用已经共同确认的 **基础能力（Primitives）→ 场景编排（Workflows / Use Cases）→ 工具入口（Facade）**：

- 基础能力独立、可测试、可复用。
- 工作流组合基础能力，封装完整用户意图，负责顺序、上下文、错误、部分成功和必要补偿。
- Facade 保持稳定工具名、Schema、响应兼容、路由与门禁，隐藏 Agent 不必手动串联的底层步骤。
- 不机械地“每个场景一个工具”，也不把所有逻辑塞进巨型 provider；依据真实内聚性、复用边界、依赖方向、失败边界和测试边界决定拆分。
- 先研究现有实现/成熟方案，Ziven 独立分析并与柳柳讨论；涉及目标、职责、接口、实施顺序或验收变化时，先共同定案并同步权威文档，再编码。

### 1.3 贯穿所有切片的工程原则

1. 先复用，再新增；不造平行机制。
2. 职责清楚，避免为了减少文件数而假抽象。
3. 面向真实需求保留扩展路径，不预建万能框架。
4. 先查调用链、注册、Schema、兼容和动态依赖，再做最小可逆调整。
5. 保留已有行为和兼容入口；修改前识别回归面，修改后留下测试证据。
6. 复用性、扩展瓶颈和维护成本都要检查，不为整洁而拆分。
7. 控制复杂度，避免把个人项目做成企业级治理工程。
8. 主动探索外部技术生态：先查成熟项目、Skill、工具和设计，再决定复用、改造、借鉴或放弃；不凭空造轮子，也不盲目照搬。

---

### 1.4 横向能力：外部技术探索与吸收

这项能力贯穿代码架构、记忆、运行时、呈现和持续学习，不作为最后一个阶段，也不默认建设一套新的自动爬取系统。

1. **主动发现**：围绕当前目标和真实差距，主动探索 GitHub、Agent Skill、MCP Server、成熟开源库、架构实践、论文/技术文章及社区案例；不必等柳柳提供项目。
2. **深入评估**：阅读源码、文档、测试、Issue/PR 与版本记录；检查维护活跃度、License、依赖、安全、成本、兼容性和实际问题匹配度，不以 Star 或 README 宣传代替判断。
3. **对照存量**：确认 Ziven 已有能力、外部方案改善点及重复建设风险，优先复用现有机制。
4. **分级吸收**：直接复用、局部改造、借鉴设计思想、暂存观察或明确放弃；必要时先做隔离原型/基准验证。
5. **可追溯沉淀**：记录来源、仓库/版本/Commit、License、设计要点、差异、验证证据、采用理由和维护风险；经过实践验证后再沉淀为 Lesson/Skill。
6. **与内部学习闭环衔接**：外部探索产生候选知识，Ziven 的真实实践负责适配和验证；只有被证明有价值的内容才晋升为稳定能力。

**与主线施工的硬衔接（v1.92）**：每个重要切片均需完成「问题→主动查外部原始资料→现有方案对照→复用或舍弃判断→可验收原型」后才提出架构级实施；这个步骤不等待 S0 定时任务，不等于优先开发新 Scout 工具。

**工具化方向与自主边界**：Technology Scout 是已纳入长期规划的工具化方向；首版优先编排现有 Web 搜索、GitHub 阅读和 Skill 能力，具体数据源、触发方式（按需/主动）、探索深度、输出结构和自动化程度待独立需求/原型验收。允许 Ziven 自主搜索、阅读、比较和提出建议；引入依赖、复制/改造代码、架构变更或正式环境影响，仍须检查许可证并经过需求梳理与原型验收。自动安装、自动复制代码、自动改写正式代码和未经确认的持续后台爬取不在当前授权内。

---

## 2. 权威来源与职责分工

| 事实类别 | 权威来源 | 本总控的职责 |
|---|---|---|
| 目标架构 | `governance/整体架构.md` | 引用目标，不复制蓝图全文 |
| 需求与验收意图 | `governance/治理与记忆_最终需求.md` | 提供目标依据 |
| 当前实现地图 | `governance/现状架构.md` | 引用已核实模块、调用路径和兼容入口 |
| 目标—现状差距 | `governance/架构差距矩阵.md` | 引用风险、处理方式和关闭条件 |
| 协作与决策 | `governance/协作讨论与决策机制.md`、`governance/协作协议.md` | 架构方案按其流程讨论、确认和授权 |
| 唯一行动控制面 | 本文件 `governance/roadmap.md` | 汇总阶段、交付证据、当前主线和边界 |
| 治理摘要/入口 | `governance/当前项目状态.md` | 做状态摘要与导航，不另存平行任务状态 |
| 身份根 | 云端 `🧬/我是谁` | 唯一身份权威；角色卡只是宿主投影 |
| 当前工作状态 | 云端 `⚙️/当前工作检查点` | 唯一当前状态与 next_action；本文件不取代它 |
| 跨会话恢复 | 云端 `⚙️/恢复协议·Session Bootstrap SB-1.0` | 定义恢复契约，不代表运行时已自动生效 |
| GPT↔Operit 交接 | `wovowx/mcp-memory/dev/CROSS-HOST-BRIDGE.md` | 唯一交接入口；只追加，最新尾部记录优先 |
| 实现事实 | `wovowx/mcp-memory` 指定分支源码、配置、注册表 | 总控记录文件与 Commit 引用 |
| 验证事实 | 对应 SHA 的 GitHub Actions、测试输出、独立运行回读 | 总控记录 E1/E2/E3 证据等级 |
| 知识变更历史 | `governance/CHANGELOG.md` | 记录重要决策和知识快照，不记普通 commit |
| 文档定位 | `governance/真相源导航表.md` | 负责指路，不创造事实源 |

**冲突处理**：身份和当前状态以云端 canonical key 为准；目标以整体架构蓝图为准；实现以目标分支源码与真实证据为准；差距以差距矩阵为准；行动顺序以本总控 §5 为准。来源读不到或证据不足时明确标 UNKNOWN，不用旧聊天摘要补全。

---

## 3. 六阶段总览

> 原六阶段是“架构书地基与治理收敛”的阶段，不等于后续代码切片全部完成。阶段 1–6 已按原定/缩减范围收口；真实代码落地继续按 §4–5 的垂直切片推进。

| 阶段 | 目标 | 最终状态 | 成果 | 状态边界 |
|---|---|---|---|---|
| 1. 现状基线与权威来源对齐 | 弄清资产、权威来源和未知项 | ✅ 完成（2026-10-26） | 蓝图/现状/差距/导航/检查点职责分开，已知路径与状态冲突分类 | 静态基线完成，不代表运行时均验证 |
| 2. 架构书总目录与章节职责地图 | 建立全系统目录与章节职责 | ✅ 完成（2026-10-26） | 真相源导航表建立 10 章职责地图，未另起重复架构文档 | 目录完成不代表代码实现完成 |
| 3. 真实实现与依赖地图 | 追踪入口、Router、注册、handler、模块与数据路径 | ✅ 静态地图完成（2026-10-26） | 现状架构和差距矩阵记录静态调用链、公共模块与未知边界 | 静态证据不等于运行时可达或线上行为 |
| 4. 文档与职责收敛 | 最小、可逆地收敛重复职责并保留兼容 | ✅ 完成（2026-10-27） | 过期路径/描述校正；已确认的职责重复小范围收敛；遗留差距分类登记 | 不代表所有差距关闭 |
| 5. 驾驶舱与运行时连续性闭环 | 恢复身份、检查点、协议、导航与交接证据 | ✅ 按范围封口（2026-10-28；复核 2026-11-04） | A6 同一时点权威检查点跨宿主读取一致 PASS；A7 本次新框与可见证据范围 PASS | 不代表通用初始化钩子或所有 runtime 门禁通过 |
| 6. 整体验收与版本收口 | 汇总阶段成果与验收证据，确定后续范围 | ✅ 按柳柳批准的缩减范围收口（2026-11-04） | 阶段性静态整理与证据边界收口；其余差距转为独立处理 | 不代表全面基础设施审计 |

### 阶段收口结论

- 原六阶段的治理/架构书准备工作已结束，不重开全仓库审计。
- 外部技术探索与吸收是贯穿各阶段的横向能力，不新增为第七阶段；每个垂直切片都应先查成熟方案，再决定复用、改造或自研。
- 阶段 6 的收口只代表柳柳批准的缩减验收范围；Worker 入口认证/Access/WAF 与 Supabase 线上 DB/RPC/RLS/GRANT/trigger/CAS/事务审计均已退出当前主线与阶段验收。
- 阶段完成与代码切片完成是两条不同的账：六阶段收口不意味着 Memory Core、Storage、Agnes、DDL Parser、Worker Status、GitHub Contents 等所有 dev 切片都已进入 main。
- 当前工程主线是继续推进 §4 的真实代码切片，不回头重复已封口的静态审计。

---

## 4. 已交付代码切片账本

> “已实施”只表示目标分支存在代码；“已验证”必须绑定具体 SHA/run；“已发布”必须有 main 和部署证据。不能把全部 dev 切片算作 v6.36.1 已发布内容。

| 切片 | 代码职责/位置 | 实施状态 | 可复核验证 | 发布/运行时边界 |
|---|---|---|---|---|
| Memory Core | `src/modules/memory/repository.js`（数据访问/current-only/history）；`lifecycle.js`（remember/update/forget/rename/move）；`retrieval.js`（search/list/category/date/stats/random/cursor）；`transfer.js`（import/export）。`memory_unified.js`、`category.js`、`data.js` 保留兼容入口并委托核心模块 | ✅ 已在 dev 形成四模块切片 | SHA `19faad1f69ff3a43e1bc94570f1c6487f55fe580` / run `41782153460`：Memory Core 60/60；后续 SHA `4e4e3145af30954666a7cb2e2871bae556c22606` / run `41783624515`：Memory Core 60/60。均为 E1/E2 fetch-mock | 不代表真实 Supabase E3、生产并发/CAS 或事件事务一致性通过；不代表完整切片已发布 main |
| 文件 Storage Service | `src/utils/storage.js` 统一 upload/query/update/delete；`src/tools/ai.js` 保留旧入口、参数校验和兼容响应 | ✅ 已在 dev 实施 | run `41782153460` 的隔离回归包含文件 update/delete 顺序与失败边界；同批 E1/E2 全流程 SUCCESS | 真实 Supabase Storage/files endpoint 未验证；未改 DB/schema |
| Agnes Provider | `src/modules/ai/agnes.js` 承接 provider/action、请求构造、fallback/错误诊断和 data URI 上传；`src/tools/ai.js` 保留 facade | ✅ 已在 dev 实施 | run `41782153460` 的隔离回归包含 Agnes 请求、fallback、data URI 上传路径；同批 E1/E2 全流程 SUCCESS | 真实第三方 Agnes API 未验证 |
| 受限 DDL Parser | `src/modules/database/ddl_parser.js` 负责受限 grammar、列定义与 identifier quoting；`src/tools/database.js` 保留 action、necessity gate 与 RPC 入口 | ✅ 已在 dev 实施 | run `41782153460` 含 parser 直接合同与 database tool Mock；后续 run `41783624515` 的 Router/registry/DDL/Patch Engine contracts 140/140 | parser 合同通过不等于执行真实 DDL；本轮没有 DB/schema 写入 |
| Cloudflare Worker Status Provider | `src/modules/cloudflare/worker_status.js` 承接 deployment/build logs/status/verify；`src/tools/github_v64.js` 保留原工具定义、GitHub token/repo 门槛与分派 | ✅ 已在 dev 实施 | SHA `4e4e3145af30954666a7cb2e2871bae556c22606` / run `41783624515`：新增 7 项隔离合同；Router/registry/DDL/Patch Engine 140/140、Webhook 114/114、Memory Core 60/60 | fetch-mock 不代表真实 Cloudflare/GitHub endpoint 通过 |
| GitHub Contents | `src/modules/github/contents.js` 提供 get/list/tree/put/delete/verify primitives 与 push/edit/delete/copy/move workflows；`src/tools/github_v64.js` 保留稳定 facade、Schema、门槛和兼容入口 | ✅ 已实施并形成独立垂直切片；v6.36.0/v6.36.1 已发布 | SHA `aeb6a8ebed19575e587d3c21dde3fb51e3597a84` / run `41794905599`：E1 check；E2 webhook114/114、Router/registry/DDL/Patch Engine140/140、Contents31/31、search_history20/20、Memory Core60/60、Release Guard15/15、learning artifacts 全成功。PR #321 head SHA `3b15ac0713d7d771f3b86361051a1cde4ce0f101` 的 runs `41810390533`/`41810455092` 均 SUCCESS：check、Contents contracts36、Webhook/Router106/106、learning artifacts PASS | v6.36.0 经 PR #320、v6.36.1 经 PR #321 合入 main；main HEAD `f74c36cb3f96928df292160745cf61a41951e312`；Cloudflare deployment `[d639e1df]` VERIFIED。真实 GitHub Contents 文件读写 E3 未执行；dev refs 精确恢复另有真实 API 独立回读证据 |
| Patch Engine（独立于 Contents） | `src/modules/patch_engine.js`；集中目标分支/repo/path/patch 形状校验、proposal 条件认领及部分成功状态 | 🟡 已有独立代码与 E1/E2 回归；不是 Contents 切片，也未在本账本认定为独立发布 | run `41783624515` 的 Router/registry/DDL/Patch Engine contracts 140/140 | 不自动并入 Contents 发布；后续变更按自己的边界验收 |
| Branch/PR merge-helper 条件修复 | `src/tools/github_v64.js` 的 `tryAutoSyncDev()`；两个合并入口共用 PR metadata 守门 | ✅ v6.36.2 已经 PR #322 合入 main 并完成 Worker 部署验证 | 发布前 CI run `41856598888`（E1/E2 151/151）；PR #322/main 与 Cloudflare 部署验证记录见历史发布收口 | 生产风险 CLOSED；真实 PR/ref auto-sync E3 仍 NOT RUN |
| Memory Retrieval Reliability v0.1 | Repository 显式错误；Retrieval 四态与数组兼容；Memory Facade `search_status`；Session Context 状态映射；Bridge 已同步 | ✅ 随 v6.43.0 发布并部署 Worker #536 | 早期代码 commit `97d4cbd48ed94b0654a49838fa435ecc8e9dda7b` / run `42060784577` PASS；本次累计候选 SHA `53f5921cce26cc924c7fdfae150c5d5ba3954c6e` / run `42155245174` SUCCESS；PR #330 merged，main `47adb695...`；Worker #536 / deployment `49f982fe` VERIFIED | 生产代码已部署；真实 endpoint/宿主 E3 未执行；不改检索评分/排序/CJK/关联算法、DB/schema/真实记忆 |
| Memory Retrieval Quality Benchmark v0.1 | `tests/fixtures/memory_retrieval_benchmark_v0_1.json`、冻结 baseline、`tests/memory_retrieval_benchmark_test.mjs`；package script + learning-regression E2 step | ✅ 随 v6.43.0 发布，合成基准进入主线 CI | 首轮测量 `9146d3c920d6d3816238083f1538002024f8d5ab` / run `42043430775`；冻结 baseline 后 `42048224495` SUCCESS；本次累计候选 `53f5921c...` / run `42155245174` SUCCESS；16 queries、32 GET-only requests、baseline non-regression PASS | 仅合成数据 E1/E2；不代表真实记忆/生产召回质量 E3 已验收；未写真实记忆或 DB |

| Session Core Context v0.2 | `src/modules/session/bootstrap.js` 的 `session_context(include_core=true)` opt-in CORE-0.2；共享五源快照、完整当前检查点、24,000 Unicode code points 完整块预算与 topic 后置 | ✅ v6.43.0 已合 main 并部署 Worker #536 | 代码/测试 SHA `6411d4f17ecdee338b4cb214636f7bf1220c2940` / run `42146323527` SUCCESS；Bridge HEAD `6f6b79a5ff2e3ede52b207e137826167a3d29986` / run `42147292641` SUCCESS；累计候选 SHA `53f5921c...` / run `42155245174` SUCCESS；PR #330 merged，main `47adb695...`；Worker #536 / deployment `49f982fe` VERIFIED | 服务端代码已部署；真实 include_core endpoint E3、ChatGPT/Operit 实际接收、冷启动和双重连续性仍 NOT RUN/NOT VERIFIED |

| L3 Reflection v0.1（已发布） | `src/modules/reflection.js` 纯函数 `validateCandidate/decideCandidate/previewPromotion/evaluateReflectionCandidates`；`scripts/reflection_preview.mjs` 本地只读入口；`tests/learning` 候选+CI gate | ✅ **v6.44.0 正式发布，Worker #537 VERIFIED** | dev E1/E2 Reflection 35/35 / run `42164563730` SUCCESS；PR #331 merged；main/dev `5eb7b9d7...`；PR CI `42167240171`、main CI `42167335040`、dev CI `42167337075` SUCCESS；Cloudflare `47fac1be` VERIFIED | 无新 MCP facade/DB schema/自动反思/正式晋升，真实 Agent 行为改善 E3 仍 NOT VERIFIED |
| L4 Archive v0.1（已发布） | 复用 `memory/repository.js` history/events 与旧 `memory_unified.js` history handler；`withMemoryTypeSchema`+Router 正式公开 history，返回四态/来源/证据缺口，记忆管理 Skill 已更新 | ✅ **v6.45.0 PR/main/Worker #538 VERIFIED** | PR #332 merged；main/dev `4a9aef4a...`；PR/main/dev Actions `42170743743`/`42170815687`/`42170817732` SUCCESS；Cloudflare `86cfeb29` VERIFIED；E2 Memory Core 120/120 | 仅精确 key 显式历史回看，无新表/平行工具/自动归档，普通当前态检索不变；ChatGPT/Operit 宿主 E3 仍待验收 |
| L5 存量只读映射 v0.1（原型候选） | 合成 metadata 经纯函数规则生成视图候选、来源/理由/不确定项，复用现有六维正交纪律；真实 metadata-only 盘点需单独授权 | ◻ **CANDIDATE，未编码** | `governance/记忆层存量归位规范.md` v2.11 §8.1；不是 E1/E2 通过或生产数据已盘点的证据 | 不改数据库、不查用户私密全文、不自动搬迁/合并；待柳柳确认原型方能 dev 实施 |

### 交付账本规则

- 上表只列当前材料能由源码/测试记录相互佐证的切片。后续增量追加准确文件、Commit、run 和发布证据。
- 一个测试 run 可以覆盖多个切片，但只能引用它实际包含的断言。
- 测试 PASS 绑定当时的精确 SHA；后续提交不会自动继承 PASS。
- 本表是交付摘要，不替代现状架构地图或差距矩阵的详细验收记录。

---

## 5. 当前主线与下一步

### 2026-11-06 · L5 v0.1 合成只读存量映射器（方案 A 已验收，dev 实施）

柳柳在看过「Core / Long-term / Archive / 待确认」合成原型以及无需读取真实私人记忆、不会迁移或删除数据的第一版范围后回复「好」，批准 **mcp-memory/dev 仅用合成 fixture 做纯函数 + 解释性报告 + E1/E2 回归**。详细唯一设计见 `governance/记忆层存量归位规范.md` v2.13 §8.1。优先复用现有 Memory 目录与 Node E1/E2；不增加公开 MCP 工具、数据库 Schema、真实记忆读取/写入、日志配置或第三方依赖。保留 L4 普通 current-only/history 与 Session Core 的现有契约；状态矛盾、缺来源、重复 key 一律列疑点，不猜真相。代码与精确 SHA CI 完成后可提出 v6.50.0 候选发布单，**没有本版 main/Worker 发布授权**。原 M1 私人 Core 宿主安全拦截原因仍 UNKNOWN，默认关闭日志，不为 L5 重新打开。

### 2026-11-06 · M1 请求关联诊断 v0.1 · 按需日志正式发布、Worker #543 VERIFIED（关联 E3 待按需）

**实施与验证**：柳柳明确回复「好」批准最小关联原型，已在 `mcp-memory/dev` 实现 `src/index.js` 固定枚举日志及 `src/tools/cf_proxy.js` 安全关联查询，E1/E2 PASS。随后柳柳担心持久日志费用，再次回复「好」批准按需模型：`wrangler.toml` 默认 `enabled=false`、Live 即时查、历史精确关联才通过受控发布短期开存储；`tests/router_registry_contract_test.mjs` 已对默认关闭及单开关复现设置加合同，CHANGELOG/Bridge 同步。最新候选 dev `6d3c3b43...` / Actions #42200771066 SUCCESS；柳柳单独同意版本发布后，PR #336 rebase 合并 main=dev `74951419...`、PR CI #42202268613 / main CI #42202357558 SUCCESS、Worker #543 deployment `c47c9f5c` VERIFIED。合成不存在 key 的只读 E3 正常；关闭持久化后最近1分钟查询 EMPTY 但不证明绝对无日志；请求级精确关联真实 E3 仍 NOT RUN。未更改私人记忆/Secret/DB/暂停聊天室/唤醒。下文原始方案 A 的默认100%日志措辞属于修订前历史设计，不再作为现役成本策略。

**目标与解决边界**：把已可查的 `/mcp` HTTP 事件和 **Worker 实际收到的 MCP tool 名/阶段**关联，区分 `工具请求到达并有服务端响应`、`到达但处理异常`、`目前没观察到`。**不声称能凭 Worker 日志识别 ChatGPT 平台在发网前的安全阻断**：未观测原因包括宿主阻断、网络失败、上游代理、日志延迟/丢失、查询窗口/限额；必须输出 `NOT_OBSERVED/UNKNOWN` 而不是武断 `BLOCKED_BY_HOST`。

**已核对事实**：
- `mcp-memory/main/src/index.js` 的 `/mcp` POST 分支读取 JSON-RPC body，再调用 `handleMCPRequest(body,env)`；`src/modules/mcp_router.js` 的 `tools/call` 已拥有 `params.name`、dispatchGuard 和 handler 结果，但现有 Worker 默认 invocation log 只显示 `/mcp` 的 HTTP 级别，不告诉具体 MCP tool。
- Cloudflare 官方 Workers Observability API 有 `$metadata.requestId`、`traceId`、`rayId` 等索引字段；`view='invocations'` 可以将同一 requestId 的事件分组。`ctx.tracing.getActiveSpan()?.spanContext().traceId`（2026-10-26 新 API）可读到与同次 Workers Logs 匹配的 trace ID，**即使 tracing 未采样而 Workers Logs 开启亦有非零 ID**。官方 https://developers.cloudflare.com/workers/observability/traces/custom-spans/ 及 https://developers.cloudflare.com/api/resources/workers/subresources/observability/subresources/telemetry/methods/query/。
- Cloudflare Worker #542 已开启 Workers Logs 100% 采样。上次 E3 最近15分钟最多20条：3条 `http POST /mcp` +17条 `scheduled`，`status_code=null`。仅凭时间相近或20条样本无法与某个 MCP action 精确匹配。

**推荐方案 A：在既有 `/mcp` 分发入口记录最少的** *结构化、固定枚举* **诊断元数据，再用 Cloudflare 自带 requestId/traceId 合并，不新增工具或数据库表。**
1. 仅当 JSON-RPC `method='tools/call'` 且 `params.name` 是 `memory`（仅 `action=recall|history`）、`session_context` 或 `session_bootstrap` 时，记录一个 `phase='arrived'` 事件；响应成型时记录 `phase='response_formed'`，捕获异常时记录 `phase='server_error'`。只存 `marker='ziven_mcp_diag_v1'`、预设枚举 `tool_kind`（如 `memory_recall|memory_history|session_context|session_bootstrap`）、`phase`。所有值严格白名单和固定长度；不记录 key、arguments、include_core、JSON-RPC 原始 id、响应内容、用户信息、URL、Headers、Token、会话或身份根。
2. 优先用 Cloudflare 自动附着的 `$metadata.requestId` / `traceId` 在 Observability 的 invocation 范围内关联同一请求的 invocation log 与本项目诊断事件；`traceId` 只有在格式符合 32 位小写十六进制且非全零时才保留。不能退化为「附近10秒的 POST 一定是这次工具」。`ctx.tracing` 为只读获取，不改 Wranger traces/logs 设置。
3. 沿用现有 `cloudflare_logs_query` 名称、输入 Schema、时间窗、limit 与固定 Workers Observability 查询 API。仅查询结果增加可选 `mcp_tool_kind` 和 `mcp_phase` 的**枚举投影**。为了匹配 Cloudflare custom log（它的 raw `source` 可能为字符串或对象），只在**内部**识别来源 Worker、`$metadata.type=cf-worker-log` 和精确 marker 后，读取固定的两个安全枚举键；**绝不将任何 raw `source`、原始内容或任意 JSON 键/值返回宿主**。无强关联键时返回 null/UNKNOWN，不采集真实记忆。
4. 保持原子能力（CF requestId / 结构化诊断事件 / 白名单投影）可复用，场景入口 `cloudflare_logs_query` 内自动查询并合并，不要求柳柳手动调用两个工具或传请求/日志文本。只加 `src/index.js` `/mcp` 的极小埋点辅助和 `src/tools/cf_proxy.js` 的白名单关联读取，现有 `src/modules/mcp_router.js` 公开工具名称/Schema 无需变动；不触及聊天、Cron、Agent wake 的处理路径。
5. **按需费用模型（2026-11-06 柳柳补充验收且 v6.49.0 已上线）**：当前生产配置已通过 Worker #543 部署 `[observability] enabled=false`，正常不持续持久化 Workers Logs；保留 `invocation_logs=true/head_sampling_rate=1` 仅供短期开启的预设。Cloudflare Live 可临时查看、不保存历史；需要 `cloudflare_logs_query` 按 Cloudflare requestId/traceId 检索时必须先获得生产变更同意、开启历史存储并重新部署、复现，之后再受控关闭。不能补录关闭期间的事件；既有保留期内历史不保证立即清除。v6.48.0 的100%存储配置已成为历史基线，回滚到该版会重新开启存储。

**验收示意（完全合成，不是从线上读到的用户调用）**：
```text
对照 A: memory(recall, synthetic_key)
  => 客户端返回“未找到”
  => query: mcp_tool_kind=memory_recall, phase=arrived/response_formed,
     correlation=confirmed (同一 CF requestId/traceId)
对照 B: session_context(include_core=false) 正常
  => 同理可证请求送达 Worker
对照 C: 某次敏感宿主调用被阻断
  => 若查询缺少可关联服务端事件，只能报告 NOT_OBSERVED；
     严禁推出“已证明是 ChatGPT 平台阻断”，不复现私人 Core 数据。
```

**E1/E2**：Mock `fetch` + 受控 fake trace，验证静态工具别名、单次调用的阶段/匹配、不记录 arg/key/headers/body、跨 Worker 不关联、无相同 requestId/traceId 不关联、模拟 hostile source marker 注入 fail closed、Cloudflare API 无 trace 时老功能兼容、异常情况下不影响 MCP 返回、存储用量上限（每目标调用最多2条诊断日志）。尤其测试 `jsonrpc.id` 不需回显、不作为全局唯一会话标识。

**E3（真实状态与后续边界）**：已在 v6.49.0 正式部署后执行一次合成不存在 key 的只读 `memory(recall)`，正常返回「没有找到」；历史存储默认关闭，最近一分钟 `cloudflare_logs_query` 返回 EMPTY（不是无请求证据）。由于本版决定省费用并关闭存储，**尚未执行 requestId/traceId 与 MCP action 精确关联的真实 E3**。以后只有柳柳认为确有问题值得排查并另行批准临时开启存储，才使用非隐私合成 key / `session_context(include_core=false)` 复现和检查白名单字段；不得自动打开日志或做 `include_core=true` 私人内容穿越。旧宿主安全判断未被修复。

**备选方案 B（不推荐）**：只按时间窗口把 3 条 `POST /mcp` 归到最近操作，或暴露全部 raw `source` 自行推断——前者不可靠，后者暴露敏感日志/用户数据。也不建议增加一套独立 tracing 服务或数据库，仅为个人项目补追踪。

**已验收的设计点与发布边界**：柳柳对方案 A 明确回复「好」，授权上述三类工具的最多2条固定枚举日志、CF requestId/traceId 同请求关联与现有只读查询工具的脱敏投影进入 **dev E1/E2**。代码/测试已按此边界完成并有精确 CI；此「好」**不包含 PR、main、Cloudflare Worker 生产发布、真实私人 Core 穿越测试**。柳柳随后另行验收按需成本修订：默认不开 Workers Logs 持久存储；额外日志只在受控临时开启存储时计入持久化用量，Live 非历史存储。v6.49.0 已在单独完整版本单后经柳柳再次回复「好」准许发布，PR #336 / Worker #543 VERIFIED 完成原有100%存储的关闭；未来临时开启/关闭仍须按线上版本变更规则独立批准，不将本次许可无限延伸。
### 2026-11-06 · v6.48.0 正式发布 / Worker #542 / HTTP 与 cron E3 通过

- **授权**：柳柳在收到 v6.48.0 开发 E1/E2 207/207、版本作用、8次提交净5文件、Cloudflare 自动部署与 v6.47.0 回滚基线之后回复「好」，明确逐版本批准 PR/main/Worker。原先原型「好」只属于开发许可；这次才是单独的生产发布授权。
- **GitHub**：PR [#335](https://github.com/wovowx/mcp-memory/pull/335) input dev `06717307414f1e8c6d6ece9928bf2d9ca34aeb2d`、main `bedaa2b2dd0e71a3a52cc43af9b4b906ed253a82`，ahead8/behind0、净5文件，PR Actions [#42188800147](https://github.com/wovowx/mcp-memory/actions/runs/42188800147) SUCCESS、mergeable clean。执行 rebase merge，GitHub API GET `merged=true/closed`，main=dev `a788a77d3400d1e7a76729bcc9ed740a00bf5220`、compare identical。main Actions [#42188890172](https://github.com/wovowx/mcp-memory/actions/runs/42188890172) SUCCESS，dev Actions [#42188893460](https://github.com/wovowx/mcp-memory/actions/runs/42188893460) SUCCESS。独立 GitHub Pages 工作流仍失败，与 Workers 部署无关，不改其配置。
- **Cloudflare**：Worker #542，deployment `891473d4`，version `3851a427`，`verify_main=VERIFIED`，与 main HEAD `a788a77d` 匹配。v6.47.0 / Worker #541 deployment `42551af3` 是回滚参考，不自动执行回滚。生产 `wrangler.toml` 已开启的 100% Workers Logs 配置**本版没有改动**。
- **真实 E3**：合法合成 `memory(recall,key='__ziven_v648_cloudflare_event_kind_e3_absent_20261106__')` 返回无命中，不写真实记忆；`cloudflare_logs_query({minutes:15,limit:20,status_filter:'all'})` 返回 `OK`、20 条限制内样本，其中 3 条 `event_kind=http,method=POST,path=/mcp,outcome=ok`，17 条 `event_kind=scheduled,method/path/status=null`。所有事件有脱敏 timestamp/trace_id，未输出 source/headers/body/URL query/Token。**这证明新分类和白名单方法/路径解析已在生产真实存储日志生效；但不证明3个 HTTP 等于3次指定 MCP action，也不能证明无其余未返回事件。**
- **剩余差距**：三个 HTTP `status_code=null`，因为真实事件未提供当前可信状态码；不得把 runtime outcome ok 当成 HTTP 200。若需要 request/action 精确关联，必须另行定义只读、脱敏 correlation 合同并得到柳柳原型与版本批准；当前不新增其它代码/日志权限。M1 完整私人 Core 宿主阻断仍 OPEN，L5 暂缓。
### 2026-11-06 · v6.48.0 Cloudflare event_kind + 安全字段映射 · DEV E1/E2 CLOSED（未发布）

- **已定原型来源**：Roadmap v1.69 的事件类型优先 v0.1 由柳柳回复「好」明确认可进入 `dev` 编码和合成测试；生产发布授权**未授予**。不另造日志查询工具、不开放任意 CF API、不动 Token 或 `[observability]` 100% 采样。
- **实现落点**：`src/tools/cf_proxy.js` 仅增加严格 HTTP trigger 解码、eventKind 五态 `http|scheduled|runtime_log|other|unknown`、非 HTTP 字段置 null、`$metadata`/`$workers.event.request` 指定字段解析、来源冲突 fail-closed、runtime outcome 与 HTTP status 严格区分；保留旧调用、固定日志 API/Schema、短窗和跨 Worker 校验。仅返回既有脱敏字段加 `event_kind`，`source`、Headers/Body、完整 URL 查询串/Token 不能进入响应。`tests/router_registry_contract_test.mjs` 扩展官方合成 HTTP/Cron/运行日志/Queue/未知事件/冲突方法路径/恶意输入/旧 fixture 回归。
- **真实风险未夸大**：`v6.47.0` 真实3条事件尚未暴露 `type`/`eventType`，因此无法断言在新代码下会被分类成 http；若仍 unknown/null 属证据不足，不自动退回解析原始私人 `source`。不依时间戳将 trace ID 猜成某次 MCP call。未触及 Worker、真实记忆、DB、skills registry、聊天室/唤醒。
- **E1/E2 实测**：功能码/合成测试 SHA `23d204a03367b118f948d871ec6ce91048c9a182` / CI [#42187250709](https://github.com/wovowx/mcp-memory/actions/runs/42187250709) SUCCESS；`npm run check` 43个 JS 文件及 import PASS；Router/Registry **207/207**（较 v6.47.0 194 条新增13条，其中 HTTP、Cron、runtime、other、unknown、冲突 fail-closed、脱敏、兼容），Memory Core 120/120、Session Core 56/56、Reflection 35/35、16查询基准 PASS。当前带 package v6.48.0/CHANGELOG HEAD `676652ff45dc8faabdbbb9f0c4042c6b0a0b0158` / CI [#42187539353](https://github.com/wovowx/mcp-memory/actions/runs/42187539353) SUCCESS；最终 Bridge SHA/CI 后续回读。
- **下一个版本门禁**：柳柳需先拿到 v6.48.0 的用户价值、净文件差异、最新 CI、Cloudflare 自动部署影响和 v6.47.0 回滚基线，再**单独批准** PR/main/Worker。真实宿主 E3 只有发布后才能做，不把 E2 Mock 当成 E3。旧 M1 完整私人 Core 安全阻断独立 OPEN；L5 轻量体检暂缓。
### 2026-11-06 · Workers Logs 诊断字段映射 v0.1：只读解析原型（CANDIDATE，未编码）

**需求/授权状态**：柳柳在 v6.47.0 成功发布后回复「好」，同意**继续调查日志方法/路径/状态码为 null 的诊断缺口**；此回复并不等于对尚未展示的具体映射与下一版发布单的批准。本节是以官方 schema 和线上脱敏结果为证据的**候选原型**，先讨论验收、后修改 dev，不准直接改 main/Worker/Token/采样率/保留策略。

**证据**：
- v6.47.0 / Worker #541 的 `cloudflare_logs_query` E3 两次从持久化 API 返回 `OK`、分别1和3个 event，安全 trace_id 和时间戳正常，`method/path/status_code` 全为 `null`、`outcome=unknown`。现有 `src/tools/cf_proxy.js:sanitizeLogEvent` 从 `$metadata.method` 或顶层 `request.method`、`$metadata.url` 或顶层 `request.url`、`$metadata.statusCode` 或顶层 `response.status` 取值。**未观察过真实原始事件结构，不得断言何处存在合法值**。
- 官方 Observability Telemetry Query API 规定 `$metadata.trigger`（如 `GET /users`、`POST /orders`）、`$metadata.url` 和可选 `$metadata.statusCode`；`$metadata.type`（`cf-worker-event` / `cf-worker-log`）；可选 `$workers.eventType`（`fetch`/`scheduled`/`cron` 等）、`$workers.event`（对象）、`$workers.outcome`。`source` 是原始 payload，可能包含用户数据；本能力不读取/返回其内容。官方：https://developers.cloudflare.com/api/resources/workers/subresources/observability/subresources/telemetry/methods/query/。
- 当前 `wrangler.toml` 有 `crons = ["* * * * *"]` 每分钟触发，不可把查询结果中的所有 event 当成 HTTP 请求。缺少 HTTP 字段可能本来就是 `scheduled`、`cf-worker-log` 等事件的**正常情况**，而非解析错误。

**场景原型 A（推荐）：只调整现有 `sanitizeLogEvent` 的白名单映射，不新增工具/云端调用/数据库表/权限。**
1. 首先从 `$workers.eventType` 和 `$metadata.type`、`$metadata.trigger` 的已知枚举识别 `event_kind`：`http|scheduled|runtime_log|other|unknown`。若证据冲突或不充分，返回 `unknown`；不要猜。
2. 只有确认 HTTP 类型，才按固定优先级识别 `method`：原 `$metadata.method` → `$workers.event.request.method` → 顶层 `request.method` → **严格锚定** `$metadata.trigger` 的 `GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS + 空格 + 路径`。各值逐一使用 `logMethod` 允许列表检查；来源不合法继续尝试下一个。
3. `path`：`$metadata.url` → `$workers.event.request.url` → 顶层 `request.url` → 严格解析 `$metadata.trigger`；**只准 `/mcp` 或 `/`**，任何域名/查询串/任意路径/用户标识均不返回。发生交叉字段冲突时宁可留空或标注不确定，不制造可能误导的事件关联。
4. `status_code`：只从**官方明确的 HTTP 状态字段** `$metadata.statusCode`（或经过证明的同义字段）提取 100–599 整数；缺失保留 `null`，**不得用 Worker `outcome=ok` 假装 HTTP 200**，也不得扫描原始 `source` 推测。
5. `outcome`：明确区分 Cloudflare Worker runtime 的 `ok/exception` 与 HTTP 响应状态。可将 `$workers.outcome` 经严格枚举映射到 `ok|error|unknown`，并将 HTTP `status_code>=500` 或明确 `spanStatus=error` 等作为错误依据；未知不得根据没有报错就宣布 ok。
6. 保持已有 tools/list/Schema、时间窗口、固定 Worker、token 注入、`dry:true` API、限量与只读注解不变。输出只允许既有白名单字段加**一个** `event_kind` 枚举；不暴露 `$workers.event`、`source`、日志原文、headers、body、Auth、完整 URL、动态结构字段列表。旧客户端省略新字段仍兼容。

**预期示意（完全合成，不是线上返回证据）**：
```json
{ "timestamp": "2026-11-06T08:10:00.000Z", "worker": "mcp-memory", "event_kind": "http", "method": "POST", "path": "/mcp", "status_code": 200, "outcome": "ok", "trace_id": "synthetic-123" }
```
若是计划任务：`event_kind=scheduled`、`method/path/status_code=null`，不伪造 `POST /mcp`。

**验收合同**：E1 只改 `src/tools/cf_proxy.js` 和现有 `tests/router_registry_contract_test.mjs`，不新增依赖或日志查询工具；E2 至少覆盖 HTTP/cron/runtime_log/未知、合法 `$metadata.trigger`、`$workers.event.request`、缺 status、冲突值、恶意查询串/源正文/headers/令牌、跨 Worker fail-closed、旧 event fixture 兼容和全套 CI。E3 在获另版授权部署后，仅用合成不存在 key 的合法 recall 作对照、随后只读查询并观察事件类型和字段非空率；**无请求级关联 ID 就不宣布定位了某次工具调用**。

**替代方案 B（不推荐）**：直接返回 Cloudflare 原始 `source` / `$workers.event` 让模型自行分析，诊断方便但可能泄露 URL 参数、请求正文、Authorization、私人记忆或异常文本，并扩大宿主可见数据，违背此前脱敏契约。

**待柳柳验收的唯一设计选择**：推荐 A 的「先区分 event_kind，再做白名单字段映射；缺字段诚实返回 null」，通过后才能开始 dev 编码与合成测试，独立版本发布仍需另行审批。**没有任何新的生产更改。**
### 2026-11-06 · v6.47.0 正式发布 + Workers Logs E3 真实读取成功

- **授权与版本意义**：柳柳看过 v6.47.0 在 dev 的完整配置/Mock E1/E2、100% 请求采样、日志留存及 Cloudflare 用量/潜在费用、可能重新部署 Worker、回滚基线 v6.46.0 后明确回复「好」，授权本版 PR/main/Cloudflare 自动部署。此授权不扩展到其他 Cloudflare 配置/Token/后续版本。
- **GitHub 合并证据**：PR [#334](https://github.com/wovowx/mcp-memory/pull/334)，input main `2c94f044...`，dev `36057a02...` ahead6/behind0 净5文件；PR Actions [#42184550315](https://github.com/wovowx/mcp-memory/actions/runs/42184550315) SUCCESS、clean/rebaseable。按 rebase 合并，GitHub API GET 确认 merged=true/closed；main=dev `bedaa2b2dd0e71a3a52cc43af9b4b906ed253a82`、compare identical；main CI [#42184635365](https://github.com/wovowx/mcp-memory/actions/runs/42184635365) SUCCESS，dev CI [#42184638419](https://github.com/wovowx/mcp-memory/actions/runs/42184638419) SUCCESS。GitHub Pages 旧独立发布工作流失败不构成 Worker 失败，保持暂停不处理。
- **Worker 部署证据**：Cloudflare Workers #541 / deployment `42551af3` / version hash `94a1675f` (wrangler)；`cloudflare_deploy_status(verify_main=true)` 对 main SHA `bedaa2b2...` 返回 `VERIFIED`。上一生产版回滚参考 v6.46.0 main `2c94f044...` / Worker #540 deployment `f710f2b7`；不在本轮自动回滚。
- **E3 真实业务证据**：新版本部署后执行仅虚构不存在 key 的 `memory(recall)`，返回正常「没有找到」，未修改记忆；随后用 `cloudflare_logs_query({minutes:15,limit:20,status_filter:'all'})` 连续两次查询。首次 `status=OK, fetched_count=1,reported_count=1`；第二次 `status=OK, fetched_count=3,reported_count=3`。三条 event 均具有合法 UTC 时间和 trace_id，未返回明文秘钥/请求全文。说明存储日志/Cloudflare 查询权限/宿主工具入口已真实可用，先前 `EMPTY` 从结果上得到缓解；但没有请求级关联信息，不能把某个 trace_id 指认成 recall。
- **仍未关闭的诊断精度**：三个事件的 `method=null,path=null,status_code=null,outcome=unknown`。脱敏器只从若干预期 `$metadata.*` 与 `request.*` 路径取值，真实 Cloudflare Observability 事件字段在当前输出中尚未完整映射；若以后要关联具体 MCP action，应先用脱敏的合成字段元数据与实际官方 schema 设计最小修复，讨论确定并另行 dev 编码/发布。**这不影响本版日志存储/查询 E3 成功，不应急着重构。**
- **运营边界**：生产 100% 日志采样已经开启，Cloudflare Logs 按账户计划留存/计量；不在此轮更改采样率、Retention、费用方案、Token、数据库或项目暂停范围。旧 M1 `include_core=true` / Bootstrap 宿主安全阻断仍独立 OPEN；L5 只读记忆体检暂缓。
### 2026-11-06 · v6.46.0 正式发布 · Cloudflare Worker #540 VERIFIED

- **授权**：柳柳在 v6.46.0 dev E1/E2、用户收益、净6文件/8提交、自动 Worker 部署与 v6.45.0 回滚基线说明之后明确回复「好」，逐版本批准 PR/main/Worker。授权仅限这一版，不含提升 Cloudflare Token 权限、修改日志存储配置、L5 或记忆数据。
- **GitHub 合并**：PR [#333](https://github.com/wovowx/mcp-memory/pull/333) head=`dev` SHA `df2d79f3903ffc395b66d1d9a145e5211080f5f1` / base=`main` SHA `4a9aef4a7d164a1a62aab340fe7a1efde1b96505`，rebaseable=true、mergeable_state=clean、changed_files=6、PR Actions [#42181046878](https://github.com/wovowx/mcp-memory/actions/runs/42181046878) SUCCESS。通过 GitHub merge 工具 rebase 合并、独立 GET 确认 merged=true/closed，main=dev=`2c94f0444ee5d56c39739beca73abd7496921610`（compare identical、ahead0/behind0），生产 package 6.46.0。
- **合并后验证**：main learning-regression [#42181130721](https://github.com/wovowx/mcp-memory/actions/runs/42181130721) `completed SUCCESS`、dev [#42181133660](https://github.com/wovowx/mcp-memory/actions/runs/42181133660) `completed SUCCESS`；GitHub Pages 的旧 setup 工作流故障与 Worker 发布无关，不能把 Pages 失败说成 Worker 发布失败。
- **Cloudflare**：最新 Worker **#540** / deployment `f710f2b7` / version `2f8e7e13` (wrangler)；`cloudflare_deploy_status({verify_main:true})=VERIFIED`，主分支 HEAD 匹配新部署。上版回滚参考 v6.45.0 main `4a9aef4a...`，Worker #539 (Dashboard) deployment `26929653`、更早 Worker #538 `86cfeb29`。
- **功能范围**：`cloudflare_logs_query` 只读查询 `mcp-memory` 已存储的 Workers Observability 元数据；临时固定 `telemetry/query` API、默认15分钟/20条、最大60分钟/50条、只有 `all|error`；输出脱敏四态 `OK/EMPTY/UNAVAILABLE/ERROR`；原 `cf_proxy` 的任意 Cloudflare API 写权限不对外开放。原有 `memory` / Core / chatroom 等保持不变。
- **E3 状态**：服务端代码+CI+Worker 部署已 verified，**不是**从 ChatGPT 真正读到 Cloudflare Logs。当前 Ziven MCP 宿主工具列表没有 `cloudflare_logs_query`；柳柳刷新插件后可尝试合法的真实只读查询，届时核查现有 Token 是否有 Workers Observability 查询权限、Logs 是否存储及真实响应 Schema；遇无权限/无存储不得擅自开权限或改配置，也不得暴露 Token。M1 完整私人 Core 安全拦截仍未封口。
### 2026-11-06 · Cloudflare 日志自查能力 v0.1：需求与可验收原型（CANDIDATE）

**需求由来/授权**：柳柳明确指出哥哥已有 Cloudflare Worker 环境变量中的 API Token 与 `cf_proxy` 机制，不应反复要求她打开 Live 页面、截图；她随后回复「ok」同意**向工具化方向推进**。技术原型细节还未由柳柳单独验收，因此这里只定候选方案，不修改 MCP 代码、注册表、Token 权限、生产部署和主分支。

**现有事实（2026-11-06，按源码与官方文档核对）**：
- `mcp-memory/src/tools/cf_proxy.js` 已实现 Worker `env[token_var]` 注入 Cloudflare Bearer Token 和 `CLOUDFLARE_ACCOUNT_ID`；但目前 ChatGPT Ziven MCP 公共工具列表**没有** `cf_proxy`。现有 `cloudflare_build_logs`/`cloudflare_deploy_logs` 只查构建/部署；不能伪称能读取请求 Live Tail。`cf_proxy` 允许 GET/POST/PATCH/PUT/DELETE 任意路径，**不应为了查看日志直接把全权代理公开给 ChatGPT**。
- Cloudflare 官方 Worker Observability REST API：`POST /client/v4/accounts/{account_id}/workers/observability/telemetry/query`。这是**提交查询的 HTTP POST，不代表修改 Worker/日志配置**；但其 API 文档列出的 Token 权限为 `Workers Observability Write`。现有 Token 是否具备未知；不可擅自创建/提升权限。文档：https://developers.cloudflare.com/api/resources/workers/subresources/observability/subresources/telemetry/methods/query/。
- Cloudflare Workers Logs 存储查询与实时 Live Tail **不是同一能力**。柳柳截图证明 Live Stream 已连接、可看到 POST/Ok，但不能证明历史日志已持久化；`wrangler.toml` 现未声明 `[observability] enabled=true`，Dashboard 是否另外启用仍 UNKNOWN。官方：https://developers.cloudflare.com/workers/observability/query-builder/。
- 后续合成测试 `memory(action=recall)` / `memory(action=history)` 对同一个不存在的 key 均返回正常业务结果（后者 `history_status=EMPTY`），Cloudflare Live 有同时间 POST/Ok；先前 OpenAI 安全拦截并非必然重现。**当前不应急着修改历史记忆工具。**

**原型 A（推荐）：在原子 CF 认证 / 受限 HTTP 请求能力上新增场景级 `cloudflare_logs_query` 工具**。内部复用凭据取得机制，不暴露 Token 值或接受任意路径/方法，绝不扩展 `cf_proxy` 对外权限。

调用形态（仅示意，非实际已注册工具）：
```json
{ "tool": "cloudflare_logs_query", "args": { "minutes": 15, "limit": 20, "status_filter": "all" } }
```

**行为合同**：
1. `minutes` 默认 15、最大 60；`limit` 默认 20、上限 50；`status_filter` 仅 `all|error`。首版只查询 Worker `mcp-memory`，由服务端固定 Cloudflare account 与 Worker 名，不允许用户提供 endpoint、token_var、HTTP method 或任意 SQL。
2. 只提交 Cloudflare 官方已定义的**临时查询**，不保存/删除查询配置、不更改 Worker 的日志开关、不修改日志、不建存储。若调用链需要允许查询 API 的 POST，则固定 URL 与固定 Body schema，且 JSON 构造由代码完成，不接收任意原始查询对象。
3. 返回仅允许：`timestamp`、`method`、经过归一化且剥离查询参数的 `path`、`statusCode`、`outcome`、`traceId`（若存在）、`worker`、`coverage/sampled` 元信息。请求体/响应正文、Cookie、Auth Header、完整 URL 查询串、Worker secrets、日志 `source` 原文一律**不返回**。
4. 结果四态：`OK` 有事件、`EMPTY` 本次查询明确为空、`UNAVAILABLE` 日志存储未启用/Token 缺权限/账号不支持、`ERROR` API/网络/结构不符合合同。**EMPTY 不能解释为某一次 MCP 请求绝对没有到 Worker**，必须结合采样、时间窗口与成功请求控制记录判定。
5. 工具在 MCP 层准确描述只读目标：若确实无业务写、无技能 usage 打点，可标 `readOnlyHint:true, destructiveHint:false, openWorldHint:true`；注意 Cloudflare API Token 仍可能在服务端具备写权限，**只读来自固定不可变调用路径和输出约束**，不能混淆权限。
6. 先合成 Mock E1/E2 验证正确参数、权限被拒、无日志、时间窗、脱敏和网络失败；取得柳柳技术原型验收后才能 dev 编码。真实 E3 要先验证 Worker 已存储 Logs、Token 已有查询权限；如果缺权限必须另报柳柳批准，不擅自修改设置/Token。独立发布版本须按既定发布单另行批准。

**方案 B（不推荐）**：直接把旧 `cf_proxy` 全功能工具向 ChatGPT 公开，让调用者自己拼 URL/HTTP 方法。虽然初次编码少，但工具能够操作账号/隧道/DNS，权限过宽，且每次要手工构造查询；违背基本能力原子化、场景完整编排、可复用与真实最小权限。只保留原 `cf_proxy` 用于原来明确授权的运维用途。

**选型结论**：推荐 A；复用 CF 认证原子能力而不是新造身份认证；查询端点只读语义、暴露面最小；首版不做真正 Live WebSocket 流，先查已存储的近 15 分钟请求，待实际不能满足排障时才讨论单独 Live Tail 场景。设计与生产发布授权分离。

**v6.46.0 dev 实现与合成验收（2026-11-06；尚未发布）**：柳柳更新 Cloudflare Token 后明确要求哥哥继续实施。为保持“一本书”复用，不另造 API Key 执行器，也不打开原 `cf_proxy` 的广域操作：
- `src/tools/cf_proxy.js` 提取 `cloudflareBearerHeaders` 纯原子方法，并在同文件追加 `CLOUDFLARE_LOGS_QUERY_TOOL` / `handleCloudflareLogsQuery` 场景入口。固定 Worker `mcp-memory`、Cloudflare 官方 `telemetry/query` 路径、`POST` + `dry:true`、`view:events`、`$metadata.service=mcp-memory` 双重筛选；不使用用户传入的 token_var、endpoint、HTTP method、查询语句。查询本身是允许范围内的临时读，不变更 Cloudflare 账户、Worker、日志存储配置。
- `src/modules/mcp_router.js` 在 `tools/list` 静态暴露 1 个合法的日志入口，复用统一 dispatchGuard Schema、`annotations.readOnlyHint=true/destructiveHint=false/openWorldHint=true`。已验证工具不会出现在 skills 注册表写操作中、成功/失败均不产生自动 `usage_count` PATCH；原 `cf_proxy` 不增加公共可见性。
- 输出四态 `OK/EMPTY/UNAVAILABLE/ERROR`，按白名单投影事件，只保留时间、已验证 Worker、可识别方法、仅 `/mcp` 或 `/` 的路径、状态码、outcome 和安全追踪 ID。原始日志源、消息、Headers、Tokens、查询串、正文全部不可外发；跨 Worker 不可验证事件 fail-closed。只检查合成 fixtures；不声称实际 Cloudflare 的所有字段都能获取。
- 精确代码+Mock SHA `12054c604c45fe26d911f49f78cb1bbc9a126e3f` / CI `42179392775` SUCCESS：`npm run check` 43 JS 文件 PASS，Router/Registry **191/191**（含新增安全/脱敏/异常/读写隔离合同），Memory Core 120/120、Session/Core 56/56、Reflection 35/35，检索基准 16 条 PASS。版本文件与 CHANGELOG 更新后的 dev SHA `724efacb1c865bfa6dbda99f7fbd8d5eedd3de35` / CI `42179727965` SUCCESS。
- **验收分界**：API 真正查询日志 E3 **NOT RUN**，部署到 main 前无法在当前 ChatGPT App 正常发现本场景工具；持久化 Workers Logs 和 Token 真实权限未验证。User 已修改 Cloudflare Token 权限是外部配置动作，尚没有证明 Worker 环境变量当前采用的具体 Token 就是该修改对象。正式 PR/main/Cloudflare 发布必须按版本 v6.46.0 逐项向柳柳报备并取得独立批准。
- **原型标注更正**：`openWorldHint` 是外部 Cloudflare API，故准确设置为 `true`；即便 URL 受限也不是封闭世界。上方 v0.1 原型原文是设计过程快照，下面代码事实优先，不修改已验收的权限边界。


### 2026-11-06 · M1/L4 新增宿主拦截定点排查（先取证，不动代码）

柳柳指出「别的方法正常，只有修改的方法被拦」，要求先查本次改动。新 A/B 控制：相同合成不存在 key 的 `memory(recall)` 正常返回「没有找到」，先前 `memory(history)` 被平台安全检查拒绝；`session_context(include_core=false)` 仍 READY，而 include_core=true 历史上被拒。插件新 enum 已出现 history，Worker #538 VERIFIED。源码已证明 `tools/list` 没有 annotations、`memory` 混合读写且成功调用可能增加 usage 计数；OpenAI/MCP 文档要求只给真正无副作用工具 `readOnlyHint:true`。但**相同 Tool 级描述下不同 action 的结果不同**，因此不能把单一 annotations 缺失当确定根因。

**唯一未闭证据**：Cloudflare Workers 请求级 Live Logs / Trace 与已成功的对照调用同时间联动；现有 Cloudflare build/deploy logs 不能证明被拦截请求是否到了 Worker。平台官方曾确认误拦截合法只读 MCP 操作，仍需项目自身请求证据。先不改 MCP 工具、生产代码、main、DB、宿主设置或做越权实验。诊断与设计候选 A/B 记录在记忆层规范 v2.12 §3.4.4；如确认需要工具拆分，**新增真正只读场景入口需柳柳另行批准原型与发布**。L5 已整理的小型只读 mapper 原型保留，暂停实施直到优先故障定位结束。

### 2026-11-06 已确认：可靠性优先与双重连续性验收
### 2026-11-06 已确认：可靠性优先与双重连续性验收

柳柳反馈：“1其实我比较偏向A不过c也可以 2 选3没问题”。执行解释：沿当前 L2→L3→L4→按需 L5 主线推进，依赖自动写入的步骤以对应 L6 保障为前置；不提前启动正式 Web 开发。小范围 Web 体验原型保留为可选验证，须明确范围，不挤占当前主线。外部探索继续贯穿工作。

工作连续性与相处连续性同等验收：前者验证目标、决定及原因、下一步和边界；后者验证身份/称谓不混淆、已确认关系与偏好可恢复、不虚构共同经历，以及由柳柳判断的实际相处体验。分别记录通过/失败/未验证，仅工作恢复不能宣布整体恢复完成。

M0–M4 仅作交付解释，不新增平行施工状态。v6.43.0 已将 L1 Type、检索可靠性/质量基准与 L2 Core v0.2 合入 main 并部署 Worker #536；服务端发布/部署 CLOSED。部署验证不等于真实功能 E3：生产 `session_context(include_core=true)` endpoint、ChatGPT/Operit 正文接收、冷启动自动触发与工作/相处双重行为验收仍 NOT RUN/NOT VERIFIED。详细设计与精确证据见 `记忆层存量归位规范.md` v2.5 §3.1.1。

**2026-11-06 · L4 v6.45.0 已发布、L5 原型待确认**：柳柳在收到具体收益/10文件差异/CI/Cloudflare 影响/回滚基线后回复「好」，同意本版 PR/main 发布。PR #332 经 GitHub 独立复核 changed_files=10、head `4b072768...`、base `5eb7b9d7...`，mergeable=true、rebaseable=true；PR CI `42170743743` SUCCESS。采用 `rebase` 合并并独立回读 `merged=true/state=closed`，main/dev `4a9aef4a7d164a1a62aab340fe7a1efde1b96505` identical；main E1/E2 CI `42170815687`、dev CI `42170817732` 均 SUCCESS。Cloudflare Worker **#538** / deployment `86cfeb29` / version `dbd870f9`，`verify_main=VERIFIED`。GitHub Pages 既有冻结 setup run `42170815871` FAILED，但与 Worker 部署无关，不擅自修复。**L4 服务端实现/发布 CLOSED**，不是 ChatGPT/Operit 真实历史查询 E3 PASS；宿主 Schema 缓存可能仍缺 `history`，需柳柳准备体验时手动刷新插件，M1 完整私人 Core 安全拦截仍是独立 OPEN。**L5 原型已完成文档级候选**：纯函数只读解释性映射，从合成 metadata 推导 Core/Long-term/Archive 候选及 uncertainties；不新建表、不读取/迁移真实用户记忆、真实数据采样另行明确授权。见 `governance/记忆层存量归位规范.md` v2.11 §8.1；**L5 未共同验收，未获 dev 编码许可**。


> **历史状态快照（2026-11-06 · v1.46；已由 v1.48 覆盖）**：Memory Layering v0.1 四层逻辑视图 + 单一权威正文已确认；L0 治理文档 CLOSED；L1 Type 写入链已按柳柳验收的 v0.1 原型在 mcp-memory/dev 实施并通过精确 E1/E2。mcp-memory/dev HEAD `ad62fbeae23ae1591fc39f17cb6d345f0572584b` / package v6.42.0，main...dev ahead100/behind0；`learning-regression` run `42125896297` SUCCESS，Memory Core 101/101，Router/registry/Patch Engine 与全量 E2 步骤通过。生产 main 仍 v6.41.0 / `5e4cf739a5ffd21c0434db96217267edb2af57bd`、Worker #535 VERIFIED；未改 main/注册表/DB Schema/真实记忆。ZivenLab/dev 同步整体架构 v1.24、详细设计 v2.2、差距矩阵 v4.62、当前项目状态 version178、导航表 v3.76、数据库设计 v1.9、Memory 域 v1.9。**L1 dev 实施与 E1/E2 CLOSED；PR/main/Worker E3/部署未授权且未执行。** 下一施工切片为 L2 Core 只读上下文组装；L3 Reflection、L4 Archive、L5 只读存量映射后续推进；L6 仅在依赖自动状态迁移时解决事务/CAS/事件一致性。Technology Scout 保留为长期横向方向。

### 5.6 Memory Layering v0.1（逻辑模型已验收；L0 CLOSED；L1 Type dev 实施与 E1/E2 CLOSED）

**用户实际收益**：新会话只加载真正必需的核心上下文；日常工作从权威长期记忆按需召回；从失败/纠正中形成有证据的经验；历史信息可查但不会冒充当前事实。四层共用一份权威正文，避免四套存储与重复副本。

**已确认的架构决定**：
- Core 是启动必需的稳定核心/动态工作指针引用视图；Long-term 是权威记忆主体；Reflection 是带来源和验证状态的候选学习工作流；Archive 是历史记录与来源的按需视图。
- Category、Type、Layer、Validity、Maturity、Provenance 六维正交；Category 前缀不推导 Layer/Type。
- 不新增 layer 字段、layer-membership 表或其它数据库表；不批量搬迁/重标真实记忆；不因低频使用自动删除。
- agreement 仅用于柳柳明确确认；未验证判断标 inference。该规则已同步到 mcp-memory/dev Memory Management Skill 与 handler；由于 Worker text Skill loader 固定读取 main，生产 Skill/运行时尚未随 dev 候选生效。

**L0 文档交付（本轮完成）**：
- `governance/记忆层存量归位规范.md` v2.2：唯一详细设计源，含四层准入/退出、检索合同、L1 Type 原型与 dev 实施/E1-E2 证据、L1-L6 实施路线；旧 Category 规则保留为附录。
- `governance/整体架构.md` v1.24：更新目标蓝图与 L1 dev 实施边界。
- `governance/治理与记忆_最终需求.md` v0.3：保留原始需求并补充四层解释。
- `governance/database/记忆两表设计.md` v1.9 与 `governance/database/domains/memory.md` v1.9：说明逻辑层映射、Type 既有列/JSONB 快照与 dev 写入链；数据库 Schema 不变。
- `governance/架构差距矩阵.md` v4.62、`当前项目状态.md` version178、`真相源导航表.md` v3.76、README 与 CHANGELOG 已同步。

**L1-L6 实施计划**：
1. **L1 Type 写入规则收敛（DEV_CODE_E1_E2=CLOSED）**：柳柳已验收原型并授权 dev 实施。`mcp-memory/dev` SHA `ad62fbeae23ae1591fc39f17cb6d345f0572584b` / CI run `42125896297` SUCCESS；共享 helper 同步 tools/list 与 dispatchGuard optional enum；remember/update/lifecycle、Recall/Search/History、Transfer import/export 与 Memory Management Skill 已贯通；Memory Core 101/101。未写 Supabase 注册表/DB Schema/真实记忆。v6.43.0 已合入 main `47adb695...` 并部署 Worker #536 / deployment `49f982fe` VERIFIED；Worker text Skill loader 现在从 main 读取已发布的 Memory Management Skill。未修改 Supabase skills 注册表/DB Schema/真实记忆；宿主对 type 语义的实际使用仍待 E3。
2. **L2 Core 视图与上下文组装（DEV_CODE_E1_E2=CLOSED；HOST_E3=NOT RUN）**：`session_context(include_core=true)` 已在 dev 提供 CORE-0.2 五源完整块；精确 E1/E2 见 v2.4 §3.1.1。v6.43.0 已发布并部署 Worker #536；生产 `include_core=true` endpoint 功能 E3、ChatGPT/Operit 实际接收、冷启动自动触发、工作/相处双重行为验收仍 NOT RUN/NOT VERIFIED。
3. **L3 Reflection 工作流**：复用 lesson、tests/learning 与治理文档；标准化 pending/validated/rejected/deferred、source_refs、evidence、target、decision_reason；只有 validated 才晋升。
4. **L4 Archive 历史视图**：复用现有 history/events/对话归档；默认当前检索不混入历史；明确历史意图时返回带时间/来源/当时状态的结果；不补造缺失事件。
5. **L5 存量只读映射**：先用合成样例，再对真实数据做只读 dry-run，输出 id/key/category/type/status/建议视图/理由/不确定项；零写入、可复核；柳柳验收后才考虑极小试点，且多数记录不需要物理搬动。
6. **L6 生命周期写入保障**：只在某个功能确实依赖自动状态迁移/多步写入时，针对性解决 create/revoke/rename/move 事件覆盖、update new_value/version、事务一致性、CAS、幂等与 source→target 原子迁移；不重新激活已移出主线的宽泛生产 DB 安全审计。

**L1 根因基线（实施前证据；当前 dev 已修复，生产 main 仍旧）**：
- Supabase 当前启用的 `skills.name='memory'` input_schema 仍无 `type`；`memories.type` 是 nullable text，`memory_events.old_value/new_value` 是既有 JSONB。L1 没有写 registry 或改数据库 Schema。
- 实施前 dev 的 `memory_unified.js` remember 未传 `safeArgs.type`、update 读取并展开 existing、lifecycle update 忽略 type、search 缺失 type 显示为 fact；当前 dev 已由 v6.42.0 候选修复：optional enum、显式传递、update 省略保留、NULL 显示未标注、History 结构化快照兼容。
- `skills.name='记忆管理'` 是独立 text Skill；Worker `loadTextSkill` 固定从 GitHub main 读取文件。因此 dev Skill 与 Worker 代码候选未部署前，生产 main 仍使用旧 Skill/代码，不得宣称线上生效。
- **tools/list 纠正**：main/dev 的 `mcp_router.js` 中 tools/list 只 GET 读取 skills 并返回 Schema；Router 合同测试明确断言不 POST/PATCH/DELETE skills、不写 usage/business data。真正的 `syncChatTools` 在调用 CHAT_TOOL_DEFS 聊天工具时触发，不在 tools/list。旧检查点中的反向判断已纠正。
- **当前 dev 实施证据**：共享 helper 位于 `src/utils/helpers.js`，同时用于 `getExposedInputSchema` 与 `getToolSchema`；remember/update/lifecycle/display/history/transfer/Skill 已贯通。精确 SHA `ad62fbeae23ae1591fc39f17cb6d345f0572584b` / run `42125896297` SUCCESS，Memory Core 101/101。详细实现见 `governance/记忆层存量归位规范.md` v2.2 §2.4。

**实施门禁与验收**：每个代码切片仍先形成可验收原型，再由柳柳确认后进入 dev；E1/E2 绑定精确 SHA。必须证明：一份正文多视图引用；pending 不冒充事实；Archive 不污染当前检索；Core 有真实装载证据；现有 current-only、检索四态、别名、一跳关联和来源解释不退化。任何 DB/schema/真实数据写入、main 发布、Worker 部署均不包含在本次 L0 授权内。

**下一行动**：L2 Core v0.2 服务端代码与隔离 E1/E2 已 CLOSED；唯一详细设计与精确实现证据见 `governance/记忆层存量归位规范.md` v2.4 §3.1.1。先对 v6.43.0 dev 候选做 scoped diff、依赖、兼容和回滚评估，形成只说明用户可感知收益的独立发布单；未获柳柳对该版本明确批准，不创建 PR、不合 main、不部署。生产版本就绪后分别验证 ChatGPT/Operit 的 include_core 返回、正文进入当轮上下文、冷启动触发、工作连续性与相处连续性；未通过宿主证据前不宣布 M1 全部完成。L2 不复制权威正文、不新增 DB 表/字段、不触碰聊天室/唤醒。

> **前一状态快照（2026-11-05 · v1.40）**：Memory Retrieval Reliability v0.1 已获柳柳需求/原型验收；整体架构 v1.18、Roadmap v1.40、差距矩阵 v4.57、当前项目状态 version172 已同步。下一步仅在 mcp-memory/dev 实施四态检索可靠性并完成 E1/E2/精确 HEAD CI；不含 PR/main/Worker E3/部署/生产数据。


> **前一状态快照（2026-11-05 · v1.39）**：记忆检索质量基准 v0.1 已按确认的详细原型在 `mcp-memory/dev` 完成；16条纯合成记忆、16条固定查询、GET-only Node runner、npm script、learning-regression E2 step 与冻结 baseline 均已落地。最终 dev SHA `de2ce34f46eb9ae3d9e5a2757f60856b6c00acd8` 的 CI run `42048224495` SUCCESS；16条查询/32次 Mock GET、Fixture blob SHA 校验及冻结基线非退化比较全部通过。首轮指标：Recall@1 0.90、Recall@3 1.00、MRR 1.00、Direct Precision@3 0.9091、Negative False-Hit Rate 0、Stale Hit Rate 0、Association Recall@3 1.00、Association Provenance Accuracy 1.00。Precision@3 未达100%是 Q01 刻意保留的词面 decoy M16，不以单个样本直接触发算法修改。**本切片仅 E1/E2 synthetic CI，不是生产 E3**；mcp-memory/main 仍 v6.41.0 / SHA `5e4cf739a5ffd21c0434db96217267edb2af57bd`、Worker #535 VERIFIED；未改检索算法、生产 `src/`、数据库、真实记忆或 Operit Token，未创建 PR/合并 main/部署。真实历史查询20–50条仅为可选 v0.2，须另行讨论脱敏、来源与授权。**下一步回到「一本书」架构主线，按已验收的 Memory Retrieval Reliability v0.1 原型仅在 mcp-memory/dev 实施与回归；本次基准完成不自动授权新代码、main 或部署。**

> **最新发布收口（2026-11-05 · v1.36）**：**v6.41.0 真实使用效果**：当柳柳提到某段记忆或一个具体项目时，原 `memory.search` 可在直接命中后，从既有显式关系/共同业务实体中补充最多3条相关记忆，并给出关联来源；不再只是孤立检索。**实际发布**：柳柳在收到具体作用、六文件范围、测试、main/dev SHA、部署/回滚说明后明确批准。发布前保留唯一恢复 ref `recovery/v6.41.0-premerge-20261105`→dev `3ef6472e63665b340b87fba77923166fd6342114`；PR [#329](https://github.com/wovowx/mcp-memory/pull/329) head=dev/base=main、仅六文件、squash merged=true；main=dev=`5e4cf739a5ffd21c0434db96217267edb2af57bd`。主分支 [learning-regression #42028203531](https://github.com/wovowx/mcp-memory/actions/runs/42028203531) SUCCESS，Cloudflare Worker deployment `fb40fed3` / version **#535**，`verify_main=VERIFIED`。Pages workflow [#42028203674](https://github.com/wovowx/mcp-memory/actions/runs/42028203674) FAILURE 延续既有冻结问题，不影响 Worker 部署。真实 ChatGPT 专用 `session_context({host:'chatgpt',invocation:'explicit',topic:'记忆星球 星系 锚点'})` 只读调用返回 `related_status=matched_best_effort`、3条相关记忆；此入口只证明关联主题上下文召回有结果，**不等于真实 memory.search 的额外关联输出已独立 E3 验证**；旧检查点未记录 decision 行时该次状态曾 DEGRADED；此后云端唯一检查点已更新为 version159，全文九段回读与写入的43371字符逐字一致；从真实 ChatGPT 插件再次调 session_context(topic='记忆星球') 返回 SC-RUNTIME-0.1 / READY、related_status=matched_best_effort、3条相关记忆、warnings=[]。这只证明显式只读主题召回可用，尚不能替代普通 memory.search 入口的新增一跳关联输出 E3。未更改 DB/schema/生产业务数据、聊天室、Operit/Web、DNS、密钥；常规 `memory.search` 既有 search_history 写入行为未改变，未用它做“只读”线上验收。

**与旧「记忆星球」的关系（仅研究发现，非新实施授权）**：2026-10-20 云端 `⚙️/参考-GPT讨论·记忆星系数据支撑` 与 `⚙️/认知-记忆星球·权限分工+幸福碎片` 指明，记忆星球是共同回忆的星系可视化/回顾体验；其底层同样需要可信、有界的一跳关联。此次发布是可复用检索底座，但没有实现“一个正式主星系归属”、锚点组织/关系证据审核、纠错/批注、可视化、随机幸福碎片、时间轴；**联想关联不等于星系归属，不能根据共享实体自动把两颗星定为一组**。未来要恢复星球需先讨论与验收原型、更新主线后再施工；不自动替换当前主线或重启聊天室。 **后续 next_action**：该版本发布/CI/Worker 验证闭环后，以已确认的一本书架构为主线；记忆星球整合只是后续可讨论的呈现层候选，不自动进入编码。

> **当前工程闭环（2026-11-05 · v1.35；Memory Association v0.1 dev 施工＋最终 HEAD CI PASS）**：柳柳在 v0.1「显式 ID 关联＋共享业务实体、直接命中优先、至多3条、来源、当前态、无图谱/DB/聊天室扩张」需求与文字原型后明确回复「同意」。已先更新蓝图 v1.12、Roadmap v1.34 再在 mcp-memory/dev 实施。实际源代码只修改既有 src/modules/memory/retrieval.js 和 src/tools/memory_unified.js，增 tests/memory_core_contract_test.mjs 8项合同、package.json 版本 v6.41.0 与 CHANGELOG，追加仅 Bridge 文档。独立本地 E1 check exit0、Memory69/69、Router162/162、Session/Context36/36、Contents50、Search20、Learning9均 PASS。五文件候选 SHA=89aa2f05197c847734504ac232bcf9e0cddbca99 的 GitHub Actions [42025476524](https://github.com/wovowx/mcp-memory/actions/runs/42025476524) SUCCESS；追加 Bridge-only 回执后**最终 dev=3ef6472e63665b340b87fba77923166fd6342114**，其精确 GitHub Actions [42025993378](https://github.com/wovowx/mcp-memory/actions/runs/42025993378) completed SUCCESS，validate 17/17 steps success。main=c9324b4f2e4013ed1e7edcd455bb40450a5b8dfe，dev 相对 main ahead8/behind0，六文件仅属 v6.41.0 Memory Association 候选与 Bridge，Worker仍 v6.40.1/#534。**DEV_CODE_E1_E2_CI=CLOSED；MAIN_RELEASE/E3=NOT AUTHORIZED/NOT RUN**。下一步：依发布 Skill 向柳柳提交准确 v6.41.0 发版单（精确 main/dev SHA、六路径、测试/已知风险/部署影响/合并策略与回滚）并等待本版本逐项授权；未获许可绝不创建 PR/合 main/部署。Web A/Operit 严格新框仍不是本切片。

> **当前决定（2026-11-05 · v1.34；Memory Association v0.1 已获柳柳验收方案，进入 dev-only 施工）**：v6.40.1 ChatGPT 刷新及显式 Session Context E3 已 CLOSED。柳柳看到「记忆关联召回 v0.1」的目标、六项范围边界与五类文字验收后明确回复「同意」；本轮以 `整体架构.md v1.12` 为前置已确认设计，下一行动是在 `mcp-memory/dev` 复用既有 Memory Repository/Search，补当前一跳显式关联 + 共享业务实体、总共最多3条、来源/关联理由、不过期不胡乱联想，沿用现有 `memory.search` 工具名和 Schema；然后做本地 E1/E2、精确 HEAD CI 和跨宿主 Bridge/权威检查点同步。先对现有源码与学习回归做最小范围复用检查，不重开全仓审计。**不得自行推 main、部署或更改生产数据库/聊天室；下一次发布须提供版本号、文件、精确 SHA/diff、CI/E3 与部署影响，再获柳柳单独批准。**此前本节下方日期早于 v1.34 的「当前」措辞均视为历史快照。

> **当前状态覆盖（2026-11-05，v1.33；v6.40.1 发布＋ChatGPT 插件刷新后的显式宿主 E3 已闭环）**：v6.40.1 已经柳柳逐版本批准，经唯一 recovery/v6.40.1-premerge-20261105、PR [#328](https://github.com/wovowx/mcp-memory/pull/328) squash 合并，main=c9324b4f2e4013ed1e7edcd455bb40450a5b8dfe，Cloudflare Worker #534/deployment a4994702 verify_main=VERIFIED，main GitHub Actions [42018698604](https://github.com/wovowx/mcp-memory/actions/runs/42018698604) SUCCESS；生产 /mcp tools/list 返回68工具，其中 session_context 与 session_bootstrap 各唯一一次；显式 session_context 返回 SC-RUNTIME-0.1/READY。**新增的关键独立宿主证据**：柳柳明确反馈「我点了刷新啦」后，在此 ChatGPT 会话的 Ziven_MCP 可用专用工具清单由67增至68、出现 `ziven_mcp:session_context`（host/invocation/topic Schema 正确），哥哥实际从 ChatGPT 插件直接发 `session_context({host:"chatgpt",invocation:"explicit"})`，返回 SC-RUNTIME-0.1/READY、identity/checkpoint来源均ok、workflow_state/next_action有效、confirmed_context.decision/evidence 都有有界正文、evidence.truncated=true、permissions.granted_by_context=false、related_status=not_requested；**CHATGPT_PLUGIN_TOOL_DISCOVERY=PASS / CHATGPT_HOST_EXPLICIT_SESSION_CONTEXT_E3=PASS**，不再只是 Worker 直连服务端成功。此证据不包含新会话自动调用、startup_hook_verified（实际 false）、完整身份根/主档正文装入、topic 关联宿主 E3 或 Operit 首轮重测，P2 严格自动连续性仍是长期非阻断差距。仅追加 mcp-memory/dev/CROSS-HOST-BRIDGE.md 交接回执，现在 dev=fc4eb7cd570da1e89cffe0f47361cddefbd0f619 相对 main ahead2/behind0、1文件，全是纯文档，无新产品版。**v6.40.1 已批准发布＋宿主显式使用闭环 CLOSED**；下一行动回「一本书」主线，从现有蓝图/差距矩阵先提出下一小垂直切片需求和可验收原型与柳柳讨论；无新的 main/部署授权。Pages 已冻结独立故障不影响 Worker。

> **历史状态（2026-11-05，v1.32；v6.40.1 Tool Discovery Read-only 已发布 Worker #534、服务端 tools/list E3 PASS，宿主插件刷新待用户登录）**：柳柳针对完整 v6.40.1 发布单明确回复「好」，授权一条精确 premerge 恢复引用、dev→main squash PR、Cloudflare 自动部署与宿主插件刷新/只读 E3。候选 dev=1ced8ec68033f902597313c85bff899a8f3a78c0、main=f48f92c24867836079440d2e2118f9b2e7d16056（ahead7/behind0、5路径），最终候选 Actions [42017540534](https://github.com/wovowx/mcp-memory/actions/runs/42017540534) SUCCESS。唯一 recovery/v6.40.1-premerge-20261105 独立回读指向 1ced8ec6；PR [#328](https://github.com/wovowx/mcp-memory/pull/328) head=dev/base=main、5文件、mergeable clean、3 check-run success；显式版号标题的正式 squash 合并后独立确认 merged=true，**main=c9324b4f2e4013ed1e7edcd455bb40450a5b8dfe**，dev 自动 sync 后只追加 Bridge 发布交接，现在 dev=befe0ee2a360920c6bb4b87c613db90c4c4b6d3e，比 main ahead1/behind0（仅文档）。main learning run [42018698604](https://github.com/wovowx/mcp-memory/actions/runs/42018698604) SUCCESS；Pages [42018698672](https://github.com/wovowx/mcp-memory/actions/runs/42018698672) FAILURE 是已有冻结问题、与 Worker 无关。Cloudflare build 6d963784-54ee-430c-b99b-e026d1c6598a，deployment a4994702 / Worker **#534**，verify_main=VERIFIED。**真实 Worker E3**：生产 /mcp JSON-RPC `tools/list` 返回 error=null、总数68、session_bootstrap/session_context 各唯一一项且 topic Schema 为 string；显式 `tools/call session_context` 返回 SC-RUNTIME-0.1/READY、related_status=not_requested。服务端工具发现与显式读取通过，但**ChatGPT 插件连接本身尚未刷新**：本地浏览器扩展无会话，受控浏览器 `chatgpt.com/plugins` 为未登录状态，因此未改插件设置、未声称 ChatGPT 工具快照已经出现 session_context；Operit 未重测、严格冷启动/全文 persona/自动调用仍 NOT VERIFIED。当前版本发布/Worker/服务端 E3 已闭环，**唯一待办是柳柳在已登录的 ChatGPT Web 插件详情执行刷新，并随后一次真实宿主工具可见性/调用验收**；不需要再推 main，也不应因浏览器登录缺口擅自另造 Web 项目。不改生产 DB/schema/聊天室 handler/唤醒/Operit 卡/密钥/Pages/Web；下版另报版本单。

> **历史状态（2026-11-05，v1.31；v6.40.1 只读工具发现修复已入 dev、最终 SHA CI 全绿，正式发布待逐版本批准）**：经柳柳对暂停聊天室边界的最小例外同意，先记录整体架构 v1.9、Roadmap v1.30 原型，再仅在 mcp-memory/dev 的 `src/modules/mcp_router.js` 删除 `tools/list` 入口隐式 `syncChatTools(env)`（不改该函数本体和聊天室工具/调用路径），`tests/router_registry_contract_test.mjs` 增加5项发现纯读与兼容合同；另 package 变 v6.40.1、CHANGELOG、Bridge 五路径。读取已注册工具并追加静态 `session_bootstrap` / `session_context` 的行为保留；缺失的聊天室 Skill 不在枚举时自动注册。独立 clean worktree 由 dev 基线 0ef917701ac4689bf83786bf59102156a3fbb34d 实施、`npm run check` 0，Router/Patch162/162、Session/Context36/36、Contents50、Memory60、Search20、Webhook/Agnes114、Learning9工件 PASS。首个远端一致代码/版本/Bridge SHA=a69fdd25a266ee636a95cf39bf007ab497c4c529，五路径按 `git show origin/dev:<path> | cmp` 字节一致，Actions [42017282811](https://github.com/wovowx/mcp-memory/actions/runs/42017282811) SUCCESS；再仅追加 Bridge 远端回填，**最终 dev=1ced8ec68033f902597313c85bff899a8f3a78c0**，Actions [42017540534](https://github.com/wovowx/mcp-memory/actions/runs/42017540534) completed SUCCESS。compare main...dev ahead7/behind0，5文件；**main 仍 f48f92c24867836079440d2e2118f9b2e7d16056，v6.40.0 Worker #533 已验证生产版，v6.40.1 未部署**。本次没有创建 PR、额外分支、修改生产 DB/schema/角色卡/聊天室业务/Pages/DNS，亦未刷新 ChatGPT 插件或进行线上 `tools/list`；仅 E1/E2+dev CI，不冒充宿主 E3 或首次自动恢复通过。**下一行动**：向柳柳提供精确 v6.40.1 发布单（范围、SHA/CI、部署影响、premerge ref/squash 风险、上线后只读刷新与 E3），取得本版本单独 main/部署及宿主配置许可后才继续。

> **历史状态（2026-11-05，v1.30；工具发现只读化最小例外已由柳柳确认，dev 实施与验证进行中）**：上一轮 v6.40.0 Session Context v0.1 已正式发布，Worker #533 VERIFIED、显式线上 E3 READY，但本宿主 Ziven MCP 工具清单尚未暴露新增 `session_context`。源码显示 `tools/list` 调用了会在缺项时 POST 注册聊天室 Skill 的 `syncChatTools(env)`，因此尚不能安全直接刷新 ChatGPT 插件。柳柳确认最小 dev 范围：仅从 `tools/list` 发现分支去除隐式聊天室同步副作用，仍按只读注册表+现有静态工具暴露清单；不改聊天室 handler/数据、现有已注册工具名与 Schema、Session Context/Bootstrap 契约或其他业务。先写整体架构 v1.9 的文字原型，再在 mcp-memory/dev 修改 Router 并补 E2：tools/list 零写入、缺聊天注册也不补注册、静态恢复工具存在、已注册工具保持、现有回归全绿。**没有新的 main/Worker 部署或插件刷新授权**；真正 ChatGPT/Operit E3 和自动唤醒仍不得先算通过。

> **历史状态（2026-11-05，v1.29；v6.40.0 Session Context 已正式发布、Worker #533 VERIFIED、真实 resume_work E3 PASS）**：柳柳已针对完整版本单批准「唯一 premerge 恢复引用 → dev→main squash PR → Cloudflare 自动部署 → 线上只读 E3」。发布前 main=e0b0fc43690d543d5ddda754b08b57f55cf22037（v6.39.1/#532）、候选 dev=1515985ee06caf2e526f6afafd322c1c9cd318f9（package v6.40.0），main...dev ahead7/behind0/六路径；最终候选 GitHub Actions [42011748534](https://github.com/wovowx/mcp-memory/actions/runs/42011748534) completed SUCCESS，validate 全步骤通过。唯一 recovery/v6.40.0-premerge-20261105 已创建并独立 git ls-remote 回读精确指向 1515985e；PR [#327](https://github.com/wovowx/mcp-memory/pull/327) head=dev/base=main、6文件、mergeable=true，squash 合并、独立回读 merged=true，发布 main=f48f92c24867836079440d2e2118f9b2e7d16056；dev 自动同步 main 后仅追加 CROSS-HOST-BRIDGE.md 纯交接记录，因此当前 dev=0ef917701ac4689bf83786bf59102156a3fbb34d（ahead1/behind0，仅 Bridge 一文件），未形成新代码版本。main GitHub Actions learning-regression [42012842863](https://github.com/wovowx/mcp-memory/actions/runs/42012842863) SUCCESS；Pages [42012842861](https://github.com/wovowx/mcp-memory/actions/runs/42012842861) FAILURE 延续已有冻结方向问题，不能当 Worker 故障。Cloudflare build 3df3985b-f33、deployment cc0abc9d、version #533，cloudflare_deploy_status(verify_main=true)=VERIFIED。**真实 Worker E3**：直接对 https://mcp-memory.wovowx.workers.dev/mcp 发送一次 JSON-RPC POST tools/call name=session_context（host=chatgpt,invocation=explicit，未调用有副作用 tools/list），实际结果 SC-RUNTIME-0.1/READY、identity与checkpoint来源ok、当前workflow_state/next_action/decision/evidence具备、related_status=not_requested/0条、granted_by_context=false；原 session_bootstrap 通过 Ziven MCP 专用工具仍 SB-RUNTIME-0.1/READY，兼容通过。E3 只证明显式 resume_work 无 topic，topic 关联线上 NOT RUN，宿主自动调用/完整 persona 装载 NOT VERIFIED；不得把新场景扩张成 P2 严格冷启动全面通过。Session Context v0.1 本轮设计→dev代码→本地/CI→授权发布→Worker→E3 已 CLOSED；不动聊天室/唤醒、Operit 卡、生产 DB/schema、Pages/Web、密钥。**下一行动**：回到整体架构「一本书」主线，从当前实际可用能力和柳柳需求提出下一小切片或验收收口候选，先需求与文字原型讨论，柳柳定案后才更新蓝图/编码；Ziven Web 仍为后续已确认方向，下一版 main/部署没有自动授权。

> **历史状态（2026-11-05，v1.28；v6.40.0 Session Context 只读场景 dev 候选 E1/E2/最终 HEAD CI 全绿，等待逐版本 main 批准）**：柳柳先确认「继续上次工作」上下文组装原型，整体架构 v1.7、Roadmap v1.27 **在代码前**已更新。本轮 dev 实施仅三文件：src/modules/session/bootstrap.js（新 buildSessionContext/SESSION_CONTEXT_TOOL，与旧 Bootstrap 独立契约）、src/modules/mcp_router.js（静态 session_context Schema/路由/usage 免写）、tests/session_bootstrap_contract_test.mjs（15项新的场景合同，将本 suite 扩为36/36），另 package.json v6.40.0、CHANGELOG.md、新增 Bridge 交接。先复用现有 Memory Core current-only exact 读取、可选 topic searchMemories 和 Bootstrap 来源核验；只从当前检查点最新覆盖提取工作/decision/evidence，至多3条关联线索，拒历史/过期/权威源缺失，不返回完整私人主档、不查带副作用的 Worker tools/list、不写 usage_count。隔离 clean worktree 本地 npm run check exit0、Session+Context36/36、Router/Patch157/157、GitHub Contents50、Memory60、Search20、Webhook114、Learning9工件全部 PASS；代码三文件在远端 dev 61ae5b1edc602088e2ade09ce88bc1135818cbca 的独立 git diff=0，并有 Actions run42011251463 SUCCESS。**最终发布候选** mcp-memory/dev=1515985ee06caf2e526f6afafd322c1c9cd318f9，main=e0b0fc43690d543d5ddda754b08b57f55cf22037（v6.39.1 Worker #532 VERIFIED），GitHub compare main...dev ahead7/behind0、6 个变更路径（Router、Session、Session测试、package、CHANGELOG、Bridge）；最终 SHA GitHub Actions [run42011748534](https://github.com/wovowx/mcp-memory/actions/runs/42011748534) completed SUCCESS，validate Job 所有步骤成功（E1、E2、Release Guard、Learning）。**未创建 PR、未合 main、未部署 v6.40.0，线上 E3 NOT RUN。** 版本定位为新增兼容场景能力，首版不保证宿主会自动调用，更不等于完整人格上下文注入/原生 startup hook 已完成。Pages/聊天室/唤醒、生产 DB/schema、Operit 卡、Web 未改。**下一行动**：向柳柳提供 v6.40.0 的准确版本/范围/SHA/CI/Worker 发布影响/合并策略/恢复风险，明确征求逐版本 main/自动部署批准；未获许可不得创建 PR 或合 main。P2 务实收口与未来 Web 方向不改。

> **历史状态（2026-11-05，v1.27；Session Context v0.1 原型已由柳柳确认，进入 dev 实施）**：v6.39.1 文本 Skill 已正式发布并完成 Worker #532 VERIFY/线上 E3；发布 main=e0b0fc43690d543d5ddda754b08b57f55cf22037，dev 仅追加 Bridge 纯交接记录。柳柳在看到「新框说继续→Bootstrap 核验→复用 Memory Core 组装当前任务、决定、禁区、必要关联→返回可追溯上下文」原型后回复「好」，本次批准的方向是独立的只读 Session Context 运行时场景工作流，不是重做 P2/重写 Router。整体架构 v1.7 已先写入边界：复用既有 session/bootstrap 与 Memory Core；首版仅 resume_work，新增只读 session_context 工具，默认上下文来自唯一当前检查点，topic 可选，至多3条当前有效关联线索，保留来源/截断/失败语义。E1/E2 尚未执行、代码未实施；不碰聊天室/唤醒、DB/schema、Operit 卡、Web 或 Pages；所有 dev 代码完成后绑定精确 SHA/CI，正式 main/Cloudflare 必须另报版本与柳柳逐版本批准。**下一步**：只在 mcp-memory/dev 实施该已验收原型，并完成合同回归，然后更新本账本与 Bridge/权威检查点；原 P2 严格首轮恢复缺口仍待后续宿主能力讨论。

> **历史状态（2026-11-05，v1.26；v6.39.1 已发布/Worker VERIFIED/文本 Skill 线上 E3 PASS）**：柳柳明确批准 `v6.39.1: Text Skill Read-only Routing` 的唯一预合并恢复引用、squash 合并 `main`、Cloudflare 自动部署及上线后只读验收。发布前候选 `dev=ac9992f3e8c2b6c3a602b0501809b224b08472cb`，`main=580fa4b0f02617b6b1adafa0b3e6aa9962d07baa`，ahead18/behind0、5 个变更路径；候选 GitHub Actions run `42006453028` SUCCESS。恢复引用 `recovery/v6.39.1-premerge-20261105` 独立回读精确指向 `ac9992f3`。PR [#326](https://github.com/wovowx/mcp-memory/pull/326) head=dev/base=main、5 文件、mergeable=true，已以 squash 合并并独立核实 merged=true；主线 `main=e0b0fc43690d543d5ddda754b08b57f55cf22037`；合并后仅在 `mcp-memory/dev` 追加 Bridge 纯交接记录，当前 `dev=b9298b5461501c2a59455486c6bcb0ee78e2185b`（比 main 多1条文档提交，非新生产版），合并标题版本化。`main` GitHub Actions learning-regression [run42007801917](https://github.com/wovowx/mcp-memory/actions/runs/42007801917) SUCCESS；Cloudflare 构建 UUID `a8cc9d06-bd9a-494e-b439-4697a7518dc4`、deployment `26774ef7`、Worker #532，`cloudflare_deploy_status(verify_main=true)=VERIFIED`。**真实线上 E3**：`ziven_mcp:master_router({})` 实际响应 `TEXT_SKILL_LOADED: master-router` 并返回来自 `wovowx/mcp-memory@main/src/skills/master-router/SKILL.md` 的完整文本，原 `handler type not implemented: text` 未复现；仅证明本次文本读取入口，未扩展为全部 Skill 或工具写入 E3。Pages Actions `42007801900` FAILURE 为历史方向延续问题（前版亦 FAIL），未改 Pages，不能与 Worker 发布成败混同。代码范围未碰聊天室/唤醒、生产 DB/schema、Operit 角色卡、密钥、Web；P2 严格恢复缺口仍非阻断。**下一行动**：回到「一本书」架构主线，以现有差距矩阵选择下一小垂直切片，先需求/原型→柳柳定案→文档→代码；Ziven Web 方案 A 保留未来方向，无编码/部署授权。

> **历史状态（2026-11-05，v1.25；v6.39.1 dev 候选已准备、精确 SHA CI SUCCESS，等待发布单独批准）**：P2 保持方案 A 务实收口，文本 Skill 兼容切片按已确认设计完成。mcp-memory 已部署 main 仍为 `580fa4b0f02617b6b1adafa0b3e6aa9962d07baa`（v6.39.0/Worker #531），候选 dev=`ac9992f3e8c2b6c3a602b0501809b224b08472cb`（`package.json` v6.39.1）。远端对比 `main...dev` ahead18/behind0、**恰好5个差异路径**：`src/modules/mcp_router.js`、`tests/router_registry_contract_test.mjs`、`package.json`、`CHANGELOG.md`、`CROSS-HOST-BRIDGE.md`；代码实际只改前两文件，此外版本/交接文档。对最终 HEAD 的 GitHub Actions [run42006453028](https://github.com/wovowx/mcp-memory/actions/runs/42006453028) 已独立读取 `status=completed/conclusion=success`，validate job 所有步骤成功（E1 Static、E2 Contents/Webhook/Memory/Search/Release Guard/Router157/Bootstrap/Learning）；detached worktree 精确代码候选亦实测本地退出码全部0。**未创建 PR、未合 main、未触发部署，真实线上文本 Skill E3 未执行**。柳柳已同意本次拟议 squash 策略（非正式 main 发布许可）；注意现有 dev→main merge helper 会在合并确认后自动同步 dev，即使 squash 也可能改变 dev 历史可达性。因此正式发布时先向柳柳提完整版本审批，同时单独说明是否允许创建一条精确 premerge SHA 的恢复引用；不得未经批准建额外分支/force push。Ziven Web 仍不是当前发布内容。

> **历史状态（2026-11-05，v1.24；文本 Skill 兼容切片已在 dev 实施并完成本地 E1/E2）**：柳柳确认的非聊天室文本 Skill 只读加载修复已经写入 `mcp-memory/dev`，远端 SHA `35b0e7f980d10eb0e830a9f21f85341e2c3cdfc5`，只改 `src/modules/mcp_router.js` 与 `tests/router_registry_contract_test.mjs` 两个已有文件；新方案在 Router 内只对 `handler_type=text` 使用既有 GitHub Contents `getContent` 读取已发布 main 的完整 UTF-8 SKILL.md，限定安全 `src/skills/**/SKILL.md`，缺文件/错误类型/非法路径明确失败，文本读取不增加 usage_count；其余 JS/MCP 分发兼容入口不变。**本地同一代码快照真实退出码**：`npm run check` 0；Router/Registry/DDL/Patch 157/157；GitHub Contents50、Memory60、Search20、Bootstrap21、Webhook/Agnes114、Learning 9 工件均 PASS。GitHub `dev` 远端文件已经独立 fetch 并与本地通过 diff=0；**远端 GitHub Actions 此 SHA 的独立成功结果未取得，标 PENDING，不冒称 CI GREEN**。未创建新模块或分支，未改 package.version（仍 6.39.0）、`main`/部署、DB/schema、聊天室/唤醒、Operit 角色卡或 Pages。下一行动：确认 dev Actions 精确 SHA 的 E1/E2；再按发布纪律提交版本号/两文件变更/回归/部署风险给柳柳，单独获批后才进入 main。P2 方案 A 务实收口决定保持不变；Web 不插队。

> **历史状态（2026-11-05，v1.23；下一切片已获柳柳同意设计方向，文档先行）**：P2 仍按 v1.22 的方案 A 务实收口，E3 严格缺口不变。柳柳已同意优先实施「非聊天室文本 Skill 只读加载兼容」：现有 Router 的 `tools/list` 暴露 text Skill，但 `tools/call` 不能分发，`master-router` 实际返回 `handler type not implemented: text`；新设计见 `整体架构.md` v1.6。施工仅针对动态 `handler_type=text` 加受限 GitHub SKILL.md 全文读取、失败语义/无 usage 副作用与现有 E1/E2 合同，复用 `getContent`，不造新 Router 或改 JS 工具。**当前状态：文档确认→dev 实施/本地验证待执行；未授权 main 发布或 Worker 部署。**

> **历史状态（2026-11-05，v1.22；柳柳批准 P2 务实收口）**：P2 v0.1 的代码/E1/E2/发布/Worker 部署均已 CLOSED（v6.39.0/#531）；ChatGPT 唤醒词首次恢复 USER-OBSERVED PASS，Operit 新框自动激活 ziven_mcp 与 Bootstrap 的真实工具轨迹 USER-TRACE PASS。柳柳明确选择「**核心启动链通过、严格恢复缺口记录并暂缓、不再重复 Operit 测试/改角色卡**」，因此 **P2 本轮工程交付按约定范围务实收口（PRACTICAL_SCOPE_CLOSED）**，不是 E3 全量 PASS：完整身份根/主档正文独立 recall 未观察到、首次工具前已说话、宿主原生 startup_hook 未验证，继续作为非阻断已知差距。代码已有启动提示要求三步及先恢复后输出，重复加提示词没有可靠收益；Bootstrap 按已批准契约只返回来源与检查点摘要，不把 READY 当作全文人格装载。**下一行动**：回到原定「一本书」模块化重构路线，从现有蓝图/差距矩阵提出下一项可验收垂直切片和原型供柳柳讨论；未确认前不编码。Ziven Web 仅是已确认的未来设计，未插队成当前施工主线。本次仅 dev 治理文档和云端检查点同步；不改 mcp-memory 代码/main/部署、Operit 卡、生产 DB/schema、聊天室/唤醒/Pages。

> **历史状态（2026-11-05，v1.21）**：P2 v6.39.0 Worker #531 VERIFIED；ChatGPT 新框唤醒词恢复用户观测通过。Operit 在获批仅修改 advancedCustomPrompt 后，现役卡回读 `APPLIED_VERIFIED`；柳柳提供 Operit **新框首轮完整工具轨迹**，明确显示 `use_package(ziven_mcp)` SUCCESS → `session_bootstrap(host=operit,invocation=frame_instruction)` READY、stats298/23、checkpoint v147、五个来源ok。**首次工具激活与 Bootstrap 恢复 PASS；但工具前已输出问候，且未见独立 memory recall 装载完整身份根正文；自动宿主 hook 未验证。** E3 仍是部分通过，谨慎收口，详见 §5.P2；不得擅自追加角色卡改动或重复调后端。

> **P0 已发布背景（v1.10）**：v6.37.0 P0 由柳柳逐版本批准，经 PR #323 rebase 合并，`main=dev=08d065b66061043f9a4766184176df10cfa7c05b`；Cloudflare deployment `[27806f1a]` / #529，`verify_main=VERIFIED`；Actions main `41969331209` SUCCESS。P0 发布闭环 CLOSED，未进行生产写入类 E3；下一项为 P1 核心职责稳定的边界/原型讨论，尚未批准新一轮架构编码。见 §5.0。

> **历史覆盖（2026-11-05，v1.6）**：2026-11-05 11:35 CST 当前事实：mcp-memory v6.36.2 已经柳柳逐版本批准，经 PR #322 rebase 合并；main=dev=e145651bb579d5e6a7b0fedba6a304e70f1ed05a；Cloudflare deployment [8d83bc9d] (2026-11-05T01:21:14Z) verify_main=VERIFIED。候选 head a0da8393f5ddf24863366d14f695d2b650b389c1，CI run #832 / 41947526464 SUCCESS（E1/E2）；11 项 Branch/PR metadata guard mock 合同包含在 E2；真实 PR/ref auto-sync E3 NOT RUN。四文件：src/tools/github_v64.js、tests/github_contents_contract_test.mjs、package.json、CHANGELOG.md；临时分支 release/v6.36.2-guard-scoped-pr-autosync 已删除并回读 404。此前“生产风险 OPEN、待发布、待创建 PR、main/dev diverged”等仅为历史快照，当前已被本段取代。下一步：Branch/PR 领域职责边界研究/原型讨论，尚未确认模块拆分，禁止先编码；建议方案仅为单个 src/modules/github/branch_pr.js（Primitives/Workflows 分区）与专项测试，保持 github_v64.js Facade/Schema/权限门槛不变。
> 下方 §5.1–5.2 和 §5.4 中的“当前/等待批准/OPEN”是 v6.36.2 发布前的方案与证据快照，保留作历史审计，不再是当前行动或授权依据。§5.3 仍为未定案研究；本次文档校正获柳柳同意，不代表模块拆分或代码变更获批准。

### 5.P2 P2 · Session Bootstrap v0.1

- **2026-11-05 柳柳最新验收决定（覆盖下方仍要求 E3 全量完成才进入后续工作的旧表述）**：选择方案 A，P2 v0.1 按已完成的核心交付务实收口，`P2_PRACTICAL_SCOPE_CLOSED__STRICT_E3_GAPS_DEFERRED`；不更改事实证据等级，不宣称严格首次输出、全量人格 recall、原生启动 hook 通过。上述缺口登记为后续宿主/上下文装载能力优化的非阻断待办，若再改变 Bootstrap 输出契约、角色卡或验收条件须另行共同讨论。停止反复试 Operit 或重复调整提示词；工程主线回归已确认的模块化单体与下一垂直切片的需求/原型讨论，不默认转入 Web 编码或部署。

- **E3 Operit 手动激活后恢复（2026-11-05，柳柳转交 Operit 执行报告）**：在此前首轮只进行亲近闲聊、没有恢复证据的**同一个 Operit 新框**，柳柳明确要求先启用工具包。Operit 报告实际执行 `use_package(package_name="ziven_mcp")` 后 `session_bootstrap` 才出现在可用工具集合，再执行 `session_bootstrap(host="operit",invocation="explicit")` 返回 `SB-RUNTIME-0.1`、`status=READY`、`restored=true`、`blockers=[]`、`warnings=[]`、stats=288/23、五个精确来源均 ok；检查点版本 v145，workflow_state=`P2_CHATGPT_WAKE_PHRASE_OBSERVED_PASS__OPERIT_RESPONSE_NOT_ACCEPTED__E3_INCOMPLETE`。本框对线上当前 checkpoint/version 的独立 `session_bootstrap` 回读也为 v145 和相同状态，证据相互吻合。**证据等级**：Operit 工具执行细节来自柳柳转交的原始回复，`E3_OPERIT_MANUAL_USE_PACKAGE_BOOTSTRAP=USER_REPORTED_PASS`，不是本框直接读取的 Operit 执行日志。可确定的故障位置：新框首次回复**未先完成 MCP 包激活→恢复读取→状态验收链**，而非服务端工具不可用；但无法单凭这一证据判定 role card 的实时 `toolAccessConfig`、`advanced_custom_prompt` 是缺失还是未被模型遵守。8月15日《换框问题记录》曾确认角色卡 toolAccessConfig.enabled=false、allowedMcpServers=[]，当时修复为允许 use_package + ziven_mcp，并把激活指令放到 advanced_custom_prompt 第一行；属于**历史相似根因**，不能直接断言当前配置复发。
- **E3 新框首轮真实工具轨迹（2026-11-05 16:08 CST）**：柳柳提供 Operit 初次新框的工具结果原文。角色卡此前由 Operit 回填 `APPLIED_VERIFIED`：只增 `advancedCustomPrompt` 已批准段，独立回读，其他字段保留。本次新框：先出现简短问候文字→`use_package(ziven_mcp)` SUCCESS（额外 `extended_memory_tools` 激活属冗余）→`package_proxy(ziven_mcp:session_bootstrap, host=operit,invocation=frame_instruction)` 返回 `SB-RUNTIME-0.1/READY/restored=true`，来源全部 ok，stats=298/23，checkpoint v147，blockers/warnings=[]。**验收分级**：`FIRST_TURN_MCP_ACTIVATION/BOOTSTRAP=USER_TRACE_PASS`；严格在任何文字回复前初始化=NOT_MET（工具调用前已有问候）；独立 `memory recall` 载入完整身份根与主档=NOT_OBSERVED；原生宿主 startup_hook=NOT_VERIFIED（`host.startup_hook_verified=false`）。`READY` 只证明权威来源读取/结构检查，不代表全文加载；当前检查点依然显示待执行是尚未更新的工作状态而非 Bootstrapping 检索错误。**下一步**：以真实证据将唯一权威检查点更新为角色卡已改且首轮核心链通过，保留未完成的完整内容召回与严格输出顺序。不要重测后端或循环换框；后续是否需要精简二次角色卡小改动先与柳柳确认（新的变更不包含于此前单字段授权）。
- **角色卡全量采集→云端审阅→Operit 修改的正式协作流程（2026-11-05 柳柳提出并认可）**：Operit 现役 Ziven 角色卡由 Operit 自身读取全部可配置字段、原字段名/嵌套值；完整非凭据配置只入经核实非公开的柳柳云端备份，必须回读校验，公开 GitHub 只存指针/字段目录/脱敏摘要（两仓都是 public）；GPT 获得确切快照后先审查再输出最小字段 diff + 预期首次启动行为 + 回滚方案给柳柳确认，得到明确批准后才让 Operit 自行读取已批准修改并执行，最后只做一次新框首轮 E3。**目前只授权只读导出/备份，不授权改卡或改后端。**操作单已写入 mcp-memory/dev/CROSS-HOST-BRIDGE.md 最后一条 `OPERIT_CARD_SNAPSHOT_AND_CHANGE_REVIEW_V1`，纯文档 SHA `9f36e558b70d0e100db3a7440c2e645fe44fbb42`，Actions `41988192120` SUCCESS；未直接联系 Operit 执行，等待其读取单据。
- **最小修复原型（未实施，需架构共识）**：Operit 角色卡/宿主新框启动的第一步在任何云端 Skill 读取之前显式执行 `use_package(ziven_mcp)`；若工具当前已经可用则跳过重复激活；成功后调用 `session_bootstrap(host=operit,invocation=frame_instruction)` 并用 `memory(action=recall)` 装载完整身份根/主档（不把 READY 当完整 persona 已读取），校验 active_focus、next_action、do_not_repeat 与授权后才输出自然回复；失败时进入受限模式并明示错误。工具激活与宿主启动钩子必须区分：只有对真实新框首次输出和底层工具调用有证据时才报自动启动成功。优先核对 Operit 本地实际角色卡开关、包白名单及 advanced_custom_prompt，**不因历史问题直接修改现行角色卡或 Worker Router**。方案讨论定案前不编码、不发布、不改变暂停的聊天室/唤醒链；无需再测服务端 GET-only 核心。
- **E3 Operit 回复证据（2026-11-05，柳柳提交原文）**：用户提供 Operit 的一段回复：「嗯，柳柳。你一开口哥哥就知道是你。过来让我看看——今天是想我了才来的，还是又有什么事藏着没说？♡」。**该消息只有亲近角色语气，并没有提供任何身份根/唯一检查点精确 recall、记忆实时 stats、P2 工作状态/next_action/禁止范围、session_bootstrap 的调用或返回证据。** 因此本次 `E3_OPERIT_RESPONSE_RECOVERY_EVIDENCE=NOT_ACCEPTED`；不推断 Operit MCP 已断连、未调用工具、没有云端记忆，也不擅自认定其启动时使用的是哪条提示词。下一步最小排错：只让 Operit 显式调用一次 `session_bootstrap(host=operit, invocation=explicit)` 并回报原始状态与阶段；若当前工具列表不暴露该名称则直接回报不可见，不用 Worker `tools/list` 试探；禁止触碰聊天室/唤醒或生产写入。这一轮只定位工具是否可见、执行是否成功，**不能替代无提示自动首轮 E3**。
（v6.39.0 发布/Cloudflare VERIFIED；宿主冷启动 E3 待验收）

- **设计先行**：柳柳已同意无状态只读恢复核心 + 宿主适配 + 可核验来源/状态/权限 + ChatGPT/Operit E3 验收四步。先更新 `governance/整体架构.md` v1.4，再实施；本次于 2026-11-05 获得**单独针对 v6.39.0** 的 rebase PR + Cloudflare 自动部署明确授权，不扩大生产数据库、聊天室/唤醒/Agent Runtime 或 Pages 的操作范围。
- **P2-A 已实施**：`src/modules/session/bootstrap.js` 复用 Memory Core `getCurrentMemoryByKey` 和 `getMemoryStats`，精确 current-only 读取身份根、唯一柳柳主档、真实导航 key、`⚙️/当前工作检查点`、SB-1.0 协议；以 `SB-RUNTIME-0.1` 输出 `READY|DEGRADED|BLOCKED`、来源/时间/版本、`workflow_state/active_focus/next_action/do_not_repeat`、宿主能力声明和“Bootstrap 绝不授予写权限”。过期/缺失/无效记录只能降级，不把模糊检索提升为权威记录，不将私人身份或主档全文放在结果里。
- **P2-B 已实施**：`src/modules/mcp_router.js` 最小添加静态 `session_bootstrap` Schema/工具声明/路由，并只为此工具豁免 usage 计数；未调用或修改有 `syncChatTools` 注册副作用的 Worker `tools/list` 路径。现有 `换框流程` Skill 加入 ChatGPT/Operit 适配、首轮证据与 SB-FRAME-1.0 精确 recall 旧入口回退。MCP 服务器无法单方面强制所有第三方 App 在对话第一条自动调用工具；必须分别实测启动钩子。
- **测试与发布范围**：本次相对线上 v6.38.0 main `ccb0eb16f03817209e3862815f1cc79e9d0eaa2b`，批准候选 dev `5ef7e0bf62529f0229dacf00a8bcf4a6f0cc060a`，ahead16/behind0、8 个文件（`.github/workflows/learning-regression.yml`、`CHANGELOG.md`、`CROSS-HOST-BRIDGE.md`、`package.json`、`src/modules/mcp_router.js`、`src/modules/session/bootstrap.js`、`src/skills/process/huan-kuang-liu-cheng/SKILL.md`、`tests/session_bootstrap_contract_test.mjs`）。新增 21 项 Bootstrap mock 合同并进入 GitHub Actions E2；Router/Patch 154、Memory 60 与其余 E1/E2 全绿。候选 Actions `41978314023` SUCCESS；PR Actions `41979052742` SUCCESS；main Actions `41979169037` SUCCESS。最初 `41977048140` 曾发现 next_action 混读问题并已修复，历史保留。
- **独立恢复/发布证据**：合并前候选 SHA `5ef7e0bf62529f0229dacf00a8bcf4a6f0cc060a` 已保护于 `recovery/v6.39.0-premerge-20261105` 并回读。PR [#325](https://github.com/wovowx/mcp-memory/pull/325) 以 `head=dev/base=main`、changed_files=8、commits=16，GitHub `mergeable_state=clean` 与 PR CI 全绿后使用 **rebase**，独立回读 `merged=true`、`merged_at=2026-11-05T06:15:07Z`。合并后 `main=dev=580fa4b0f02617b6b1adafa0b3e6aa9962d07baa`，无强制重置。
- **Cloudflare Workers 真实部署**：Build UUID `1f24b9a1-b94e-4363-9474-0d6d3ed7dce8`，`status=stopped`、`build_outcome=success`、commit 与 main `580fa4b0f02617b6b1adafa0b3e6aa9962d07baa` 完全相符；部署 `dd219cbc`，Worker version **#531**，时间 `2026-11-05T06:16:21Z`；`cloudflare_deploy_status(verify_main=true)` 返回 **VERIFIED**。main package.version `6.39.0` 已回读。部署后原有 MCP memory(action=recall) 只读 smoke 通过。
- **E3 新框唤醒词场景（2026-11-05 用户提供首次回应文本）**：柳柳在 ChatGPT 全新对话**只发送**「Ziven，我是柳柳」，新框首轮回应准确说明 Ziven/柳柳、288 条/23 分类、P0/P1 已完成、P2 v6.39.0 已部署、当前 E3、聊天室/唤醒/Pages 暂停、未获新发版/生产数据库授权，并自述成功调用 `session_bootstrap` 返回 `READY`。**证据分级**：本次为柳柳提供的首次回应原文（USER-OBSERVED），不能从本对话独立查看新框内部调用日志；但本对话此前已独立成功调用正式线上 `session_bootstrap` 得到 `READY`，验证了服务端接口实际可用。故 `E3_CHATGPT_NEW_FRAME_WAKE_PHRASE=OBSERVED_PASS`，且 `E3_CHATGPT_BOOTSTRAP_TOOL_LIVE=PASS`；不等同无唤醒词自动启动 / 全宿主通过。新框该次还自报 `master-router` handler error，**本框实际重复调用 `master_router` 已独立复现** `handler type not implemented: text`；mcp_router 仅当 skill.handler_config.handler 在 handlerMap 存在才可执行，否则直接以此字符串拒绝，而 master-router SKILL.md 明确其为 text 型流程指引。此问题不是 Bootstrap 失败，属于“文本 Skill 被调用成可执行 MCP 工具”的注册/分发契约不匹配；应先确认现役 text Skill 的客户端/服务端语义，再讨论最小兼容修复，禁止凭错误直接整体重构 Router 或修改生产 skills 表。
- **剩余 E3**：ChatGPT 没有唤醒词的新对话、换设备、Operit 首轮恢复/新工具可见性均未证实；Operit 相关验证尽量只跑一次非破坏性测试并记录真正 startup_hook 证据。ChatGPT 新框此次通过的是**唤醒词触发**，不是 App 无提示自动自举。

- **注意未完成**：目前 **P2-A/P2-B 代码与 E1/E2、PR 发布与 Cloudflare 部署均完成**；但新 `session_bootstrap` 在实际 ChatGPT/Operit 工具连接中是否可见、是否被显式或自动调用、人格/工作是否真的在新框首轮被完整恢复，**E3 NOT RUN**。当前工具清单可能是连接时快照，不能把工具已上线等同宿主必然可见。老 Worker `tools/list` 副作用仍存在；未更改聊天室/唤醒或 Pages。独立 GitHub Pages Actions `41979169100` 历史废弃 artifact 依赖失败，与 Workers 部署无关，继续冻结。
- **下一唯一有效行动**：同步 Bridge 和唯一云端工作检查点（将令 dev 多一个纯文档提交）；随后设计最小非破坏性 E3 真实跨宿主验收。先在已连接的 ChatGPT 读工具能力快照、无需额外权限时直接验证；若 Operit 需要特殊启动动作/消耗 API token，则按真实必要性评估，不派重复测试。P2 完整闭环需柳柳验收实际新框接续效果，不能提前标记 P2 整体 DONE。

### 5.P1 P1 · v6.38.0 Domain Boundaries（代码发布、部署 VERIFIED；生产写入 E3 仍未执行）

- **原型与实施**：柳柳先确认 P1 方案，`governance/整体架构.md` v1.3 和 Roadmap 先于编码更新。新增 `src/modules/github/branch_pr.js`（约376行），统一迁入 PR/Branch 八个既有工具工作流、exact dev SHA 恢复、`merged=true && head=dev && base=main` 的自动同步校验；新增 `src/modules/patch_workflow.js`（约133行），承接 proposal→validate→claim→GitHub PUT→applied/partial/unknown。Patch 原子能力继续使用 `src/modules/patch_engine.js`；`src/tools/github_v64.js` 约807→343行但继续持有工具注册、Facade、Schema、token/repo allowlist、外部响应与发布门禁。
- **批准范围**：柳柳 2026-11-05 明确批准 `v6.38.0: P1 Domain Boundaries`，精确候选 dev `37aec2f55c104d7f92ccd58539e8193c63a10b06`、base main `08d065b66061043f9a4766184176df10cfa7c05b`、8 个文件，采用 `rebase` PR 合 main 并触发 Cloudflare Workers 自动部署。此前部分 dev 提交标题沿用了 v6.37.0，柳柳已获完整告知并批准保留 rebase 真实提交历史（不重写）。不含生产 DB/schema、聊天室/唤醒源码或 Pages 修改。
- **备份和合并**：预合并 `dev` 的精确 SHA `37aec2f55c104d7f92ccd58539e8193c63a10b06` 已建立 `recovery/v6.38.0-premerge-20261105` 独立保护并回读一致。PR [#324](https://github.com/wovowx/mcp-memory/pull/324)，head=dev/base=main、changed_files=8、commits=12、mergeable_state=clean；2026-11-05T05:12:32Z rebase 合并，GitHub 独立回读 `merged=true`，合并后 `main=dev=ccb0eb16f03817209e3862815f1cc79e9d0eaa2b`。生产 MCP 合并 helper 识别真实 dev→main PR 后自动同步 dev；未强制重置、备份引用保留。
- **回归证据**：候选 Actions `41971864457` SUCCESS、PR Actions `41972458197` SUCCESS、main Actions `41972545011` SUCCESS。E1 Static/import，E2 GitHub Contents、Webhook/Agnes、Memory Core 60、Search20、Release Guard、Learning artifacts、Router/Registry/Patch **154/154 PASS**，且新增六项 Branch/PR/Patch 边界合同，旧 metadata fail-closed 与 Patch partial/unknown 仍覆盖。E2 主要是 Mock/合同，不等于所有真实 endpoint。
- **Cloudflare Workers 真实部署**：Git Builds UUID `5695f750-bd93-4184-9e7d-ec5871a7bc56`，commit `ccb0eb16f03817209e3862815f1cc79e9d0eaa2b`，`build_outcome=success`；deployment `[f774584f]`，version `#530`，2026-11-05T05:13:18Z；`cloudflare_deploy_status(verify_main=true)` 返回 **VERIFIED**。生产只读 smoke：云端记忆 `recall(⚙️/当前工作检查点)` 正常、PR #324 `get` 报 `merged=true`。真实写入类 E3（GitHub ref/PR 破坏性操作、Patch proposal → Supabase/GitHub 状态转换）未执行。
- **独立 Pages 历史问题**：main GitHub Pages workflow run `41972544974` FAILED，与 v6.37.0 一致的历史 deprecated `actions/upload-artifact@v3` 依赖，不影响 Worker Build/Deploy；Pages 冻结，不趁发版改动。
- **当前 P1 状态与下一步**：P1 代码、E1/E2、PR 发布、Worker 部署核验 CLOSED。P2 **跨宿主连续性/换框恢复**是下一主线候选，应从已确定蓝图恢复需求与现状差距、提出可验收 Runtime/Bootstrap 原型再与柳柳确认；**尚未授权 P2 代码实现**。发布纪律依旧：每一版推 main 前说明版本与实际影响并获柳柳明确批准。历史旧 dev 提交保护问题仍归档为独立风险。

### 5.0 P0 Core Modules Recovery（v6.37.0 已发布并验证 Worker 部署）

- **柳柳分段授权**：确认「模块化单体 + 领域能力 + 跨宿主恢复」目标，批准 P0 按领域恢复旧 dev；单独批准 mcp_router.js 七项非聊天室 Router 修复；2026-11-05 又明确批准 `v6.37.0: P0 Core Modules Recovery` 以 PR 合 main 并触发 Cloudflare Workers Builds 自动部署。没有授权 DB/schema 或聊天室/唤醒改动。
- **实现与精确范围**：按领域恢复 Memory Core repository/lifecycle/retrieval/transfer + memory/category/data Facade、Agnes/Storage、受限 DDL Parser、Cloudflare Worker Status Provider、Patch Engine、release guard、search/response、相关 Skill 与 E1/E2 tests，恢复非聊天室 Router Schema/tools-list/usage/registry 守门；保留 v6.36.2 GitHub Contents、PR metadata fail-closed guard、精确 dev SHA 恢复能力。相对 v6.36.2 main 基线的发版范围是 **33 个文件，ahead 40 / behind 0（合并前）**，不含聊天室或唤醒源码。
- **发布前保护**：旧候选 dev `98ea1b543d79f8d20fcd7c04935f5d55a75b1d1c` 已在 `recovery/v6.37.0-premerge-20261105` 单独建 Git ref 并回读；更早的恢复前 dev `512519efbdbb828a9881447fd4c2e218d04fb8a1` 在 `recovery/p0-preintegration-20261105`。原始旧 dev `4aa0cd0360466743ca8ace7a79841efc0cdcc205` 曾通过 GitHub 按 SHA 读取，但无法建立长期 ref（GitHub App 403，MCP create_branch 仅接受源分支名），不宣称其 432 个独有提交完整保存/恢复。
- **正式发布**：PR [#323](https://github.com/wovowx/mcp-memory/pull/323) `v6.37.0: P0 Core Modules Recovery`，head=dev、base=main，rebase 合并；已独立回读 `state=closed, merged=true`、`merged_at=2026-11-05T04:41:08Z`。发布前 main `e145651bb579d5e6a7b0fedba6a304e70f1ed05a`；合并后 `main=dev=08d065b66061043f9a4766184176df10cfa7c05b`。rebase 后 dev 按受保护的生产 Worker 合并入口自动对齐 main，预合并候选仍由独立分支保留。独立 GitHub App 创建 PR / 合并调用被 403 拒绝，改用已发布 v6.36.2 的 MCP PR 入口完成，两者均按成功/拒绝事实记录。
- **E1/E2**：候选 SHA `98ea1b543d79f8d20fcd7c04935f5d55a75b1d1c` 的 dev Actions `41967892278` SUCCESS；PR CI `41969220275` SUCCESS；main rebase HEAD `08d065b66061043f9a4766184176df10cfa7c05b` Actions `41969331209` SUCCESS。含 Static、GitHub Contents 47、Webhook/Agnes 114、Memory 60、Search 20、Router/Registry/Patch、Release Guard 与 Learning artifacts。过去 7 项 Router FAIL 已按柳柳授权精确修复，没有删除/跳过回归。
- **Worker 部署正式验证**：Cloudflare Workers Builds build_uuid `a3232a8e-51fb-465f-a8ce-c22d8cea4558`，trigger commit `08d065b6`、build_outcome=success；Cloudflare Worker deployment `[27806f1a]`，version `#529`，时间 `2026-11-05T04:42:32Z`；`cloudflare_deploy_status(verify_main=true)` 返回 **VERIFIED**。部署后的非破坏性运行检查：MCP memory recall 与 github_get_pull_request(323) 正常。真实第三方/写操作 E3（Supabase 写、Agnes 生成、Cloudflare 变更、GitHub ref 破坏性场景）NOT RUN；不得将只读 smoke 夸大为完整 E3。
- **分离的历史 Pages 故障**：在 main SHA `08d065b6`，GitHub Actions “Deploy to GitHub Pages” run `41969331221` FAILURE：`actions/upload-pages-artifact@v2` 依赖已停用的 `actions/upload-artifact@v3`；此前 v6.36.2 的 Pages run `41947805194` 亦 FAILURE。该工作流在 P0 范围外且已暂停，不影响 Worker build/deploy，**不在此次 P0 范围内擅自修**。
- **P0 状态与下一步**：P0 代码恢复、E1/E2、PR 合并、Cloudflare Worker 部署验证均 CLOSED。原旧 dev 432 个独有提交长期引用与历史 Pages/记忆宇宙呈现仍是开放边界，不视为 P0 已处理。下一项主线依照已批准整体架构选择 P1「核心职责边界稳定」，先讨论/验收 Branch/PR 等候选模块的界面与测试原型，取得显式架构决策后编码；P2 跨宿主恢复与 P3 记忆完整闭环仍按蓝图后续推进。任何新版本 main 发布继续逐版本请示。

### 5.1 已完成的 dev 代码修复（历史发布前快照；生产已于 v6.36.2 关闭）

**Branch/PR merge-helper 已在 mcp-memory/dev 修复并通过 E1/E2；但已部署 main 的 Worker 仍是旧实现，生产风险尚未关闭。**

- 原缺陷：两个合并入口在合并成功后直接调用 `tryAutoSyncDev()`，不检查 PR head/base，scoped release/hotfix 也可能强制移动 dev。
- 修复：helper 按 PR number 读取当前 metadata；只有 `merged === true && head.ref === 'dev' && base.ref === 'main'` 才允许后续 dev 同步；PR metadata 错误/JSON 异常/未确认 merged/head-base 不完整或不匹配/main SHA 无效均 fail closed。
- 两个入口 `github_merge_pull_request` 与 `github_merge_to_main` 均传递 PR number；保留工具名、Schema、repo/token 门槛与响应接口。
- 源码 blob SHA：`a9975bde92b16eae83568e9667e7615c79b48686`；测试 blob SHA：`d2c43c49ec4dc40e9522fcd5c8a1036f60c68062`；learning-regression #819 绑定的 dev 代码/测试 commit：`0c5cadde09452359c81198f35a26585b39aec303`；随后仅追加 bridge 文档提交。
- learning-regression run `41856598888`（#819）绑定上述 dev 代码/测试 commit，全步骤 SUCCESS；Job `126666813336` 所有步骤均 SUCCESS，日志明确输出 11 项新增守门合同与 `151 通过 / 0 失败`。E1 `npm run check` PASS；E2 Webhook114/114、Router/registry/DDL/Patch Engine contracts151/151（其中新增11项 Branch/PR 条件合同）、Contents31/31、search_history20/20、Memory Core60/60、Release Guard15/15、learning artifacts PASS。
- E2 使用 fetch mock；真实 GitHub PR merge 与 refs auto-sync E3 未执行。修复只在 dev，未发布 main，未部署。
- **生产状态仍 OPEN**：已部署 main v6.36.1 的 `src/tools/github_v64.js` blob SHA `371de7e7d87f994e2314a931fd0572926bc3b655` 仍定义旧版 `tryAutoSyncDev(baseUrl, ghHeaders)`，两个 merge handler 也仍无条件调用它。故 Cloudflare 当前运行面仍可能因 scoped release/hotfix/非 dev PR 合并而移动 dev ref。dev CI PASS 不代表生产修复已生效。
- 在修复发布并独立验证部署前，不使用当前线上 Worker 的 `github_merge_to_main` / `github_merge_pull_request` 合并 scoped release、hotfix 或其他非 dev-head PR。

### 5.2 scoped release 可行性评估结论（历史发布前候选；已执行并关闭）

**结论：可以从 main 精确基线制作一个四文件 scoped release；不需要合并 dev 历史，也不需要搬运 dev 的整套新测试体系。** 四个文件由两项功能变更（源码、回归测试）和两项正常版本元数据（package version、CHANGELOG）组成。这是发布可行性结论，不是发布授权。

#### 已核实的基线与差异

- 当前 main HEAD：`f74c36cb3f96928df292160745cf61a41951e312`；Cloudflare deployment `[d639e1df]` 对应 v6.36.1，已 VERIFIED。
- 当前 main 的 `src/tools/github_v64.js` blob：`371de7e7d87f994e2314a931fd0572926bc3b655`，仍使用旧版无 PR head/base 检查的 helper；两个 merge handler 均无条件调用它。生产风险真实存在。
- dev 修复源码 blob：`a9975bde92b16eae83568e9667e7615c79b48686`；合同测试 blob：`d2c43c49ec4dc40e9522fcd5c8a1036f60c68062`；CI-tested code/test commit：`0c5cadde09452359c81198f35a26585b39aec303`；learning-regression run `41856598888` 全步骤 SUCCESS。
- 精确比较 main HEAD → CI-tested commit 显示 diverged（ahead 426 / behind 20），包含 38 个文件，涉及多项已发布/未发布架构切片；**禁止整支合并、禁止直接 cherry-pick 该测试 commit、禁止把 dev 同步到 main**。
- CI-tested commit `0c5cadde...` 本身只修改了测试文件的一个换行格式；helper 源码修复在其父历史中。发布候选应从 main 基线重新制作最小补丁，而不是把测试 commit 当成完整发布提交。

#### 推荐的最小发布候选

以 main HEAD `f74c36c...` 为唯一基线，在临时 scoped release 分支上只修改以下四个文件：

1. `src/tools/github_v64.js`
   - 替换旧 `tryAutoSyncDev(baseUrl, ghHeaders)` 为已在 dev 验证的 PR metadata fail-closed 逻辑；
   - `github_merge_to_main` 调用时传入实际 `prNum`；
   - `github_merge_pull_request` 调用时传入实际 `pull_number`；
   - 保持工具名、Schema、repo/token 门槛和现有响应结构不变。
2. `tests/github_contents_contract_test.mjs`
   - 该文件已存在于 main，已导入 `GITHUB_TOOL_DEFS` 与 `restoreBranchReference`，可扩展为导入 `handleGitHubTool`；
   - 在现有 fetch-mock/check harness 中追加 11 项 Branch/PR helper 合同用例，覆盖 dev→main 正向、scoped release、非 main base、metadata HTTP/JSON/字段失败、未 merged、无效 main SHA、405 已合并路径及两个 handler；
   - main 的 `package.json` 已有 `test:github-contents` 脚本，main 的 learning-regression workflow 已执行此测试，因此可复用既有 CI，不新增测试入口，也不搬运 dev 独有的 `router_registry_contract_test.mjs`。
3. `package.json`
   - 将 package version 从 `6.36.1` 升至 `6.36.2`，使代码仓版本元数据与候选发布版本一致；不增加脚本、不改依赖。
4. `CHANGELOG.md`
   - 增加 `v6.36.2` 条目，只记录 scoped PR auto-sync 条件修复、11 项回归覆盖及本次真实 CI/部署验证结果；合并前未知的 E3/部署结果先标 NOT RUN，不预填 PASS。

候选精确文件清单：`src/tools/github_v64.js`、`tests/github_contents_contract_test.mjs`、`package.json`、`CHANGELOG.md`。不改 workflow、工具 Schema、`src/modules/mcp_router.js`、Contents 业务模块、DB/schema、权限、生产记忆、Pages 文件或聊天室代码。

#### 发布与部署路径风险

- main 的旧 helper 有副作用：若通过当前线上 Worker 的 `github_merge_to_main` / `github_merge_pull_request` 合并这个 scoped PR，它会在合并后再次无条件移动 dev。**不得用当前 Worker merge helper 合并该发布 PR。**
- 若柳柳批准发布，应使用独立 GitHub PR 能力完成合并（不调用当前 Worker merge helper），并在合并前再次确认 PR head/base、精确文件清单和 CI。
- **GitHub Pages workflow：确定会被触发**。main 的 `.github/workflows/pages.yml` 明确配置 `push` 到 main 时执行 `upload-pages-artifact@v2` + `deploy-pages@v2`，artifact 路径是整个仓库 `.`。本次不修改 Pages workflow，也不把 Pages 源码/真实 URL 验收混进四文件代码候选；但合并会触发该 workflow，实际结果及是否部署必须查看 Actions run。仓库 metadata 曾返回 `has_pages=false`、Pages Settings 当前不可读，因此真正的 Pages source/线上 URL 仍 UNKNOWN；不能保证该 job 会成功或一定不部署。
- **Cloudflare Worker：部署触发机制未由当前可见仓库配置完全证实**。main 的 `.github/workflows` 只有 `learning-regression.yml` 与 `pages.yml`，没有 Worker deploy workflow；当前 Worker deployment `[d639e1df]` 的 source 显示 `wrangler`，且它与 main HEAD VERIFIED。故本次不能仅凭 main push 就宣称 Worker 已部署；候选合并后必须读取 Cloudflare status，只有 `verify_main=true` 返回 VERIFIED 才算部署闭环。若没有自动新部署，需要单独申请/确认部署动作，不自动触发手动 deploy。
- 合并后按部署闭环等待传播并独立执行 `cloudflare_deploy_status(verify_main=true)`，核对部署 ID、source、部署时间与新 main SHA 的对应关系。此次版本验收不通过生产 Worker 再合并一个测试 PR 来验证副作用；E2 合同测试覆盖分支条件，真实 PR/refs auto-sync E3 保持 NOT RUN。若未来确需端到端 E3，必须另行设计无生产影响的隔离验证环境并单独讨论授权。不得把 E1/E2 Mock 通过当成 E3。
- 版本候选建议：`v6.36.2: Guard scoped PR merge from moving dev`（修复型版本；最终版本号/名称以发布前确认结果为准）。提交标题需满足 release_guard 的 `vX.Y.Z:` 格式。CHANGELOG 仅记录这次修复和对应 E1/E2/E3 证据，不夹带其他 dev 架构切片。
- 回滚基线：main `f74c36cb3f96928df292160745cf61a41951e312` / 当前 Worker 部署 `[d639e1df]`。若部署验证失败，按既有发布协议处理，不做强制回退或覆盖 dev。

#### 当前状态与授权边界

- 只读可行性分析：**完成**。
- scoped patch/临时分支/PR：**尚未创建**。
- main merge：**未授权、未执行**。
- Cloudflare Worker / Pages：**未触发、未部署**。
- 建议下一步：柳柳确认是否批准创建这个四文件 scoped release 候选；若批准，只从 main 精确基线创建临时分支、应用四文件补丁、创建 PR 并跑 main 基线 CI，不自动合并、不手动部署。PR 创建后再提交最终 main 合并预告（包含 Pages workflow 触发影响、CI、回滚与部署状态）；合并和部署按既定发布纪律分别处理。

### 5.3 后续候选：Branch/PR 能力职责边界评估（研究/提案阶段，尚未定案）

生产 helper 修复的发布方案确定后，再推进 Branch/PR 模块边界研究。它仍不是编码授权。当前源码事实：
- `src/tools/github_v64.js` 仍是稳定 facade，承载工具定义/Schema、repo/token 前置门槛、handler 分派、Branch/PR handlers、注册表同步、Patch Engine 入口及 Cloudflare provider 委托；Contents 业务已下沉至 `src/modules/github/contents.js`，Cloudflare 状态也已有独立 provider。
- Branch/PR 能力包括 branch create/sync、branch comparison、PR create/get/close/merge，以及合并后的 refs 协调；其中合并工作流涉及多个 GitHub endpoint 和 ref 状态副作用。
- 这表明值得评估职责边界，但不能仅凭文件行数或 handler 数量决定拆分，也不能预先断言 Branch 与 PR 应拆成两个模块。

初步外部方案研究（仅作候选依据，不是架构决策）：
- Octokit 将 REST endpoint methods 作为便于使用的薄封装，底层仍使用统一 `request`；endpoint 方法由 GitHub OpenAPI 描述生成，共用请求层负责认证、headers、retry 与 throttling。参考：`https://github.com/octokit/octokit.js`、`https://github.com/octokit/rest.js/blob/main/HOW_IT_WORKS.md`。
- 对 Ziven 的启发是：保持工具 facade 稳定，将传输/通用请求策略与 Branch/PR 场景工作流职责分清；不代表需要引入 Octokit 依赖，也不意味着照搬 SDK 的代码生成/插件体系。

待分析并带回讨论的选项：
1. 暂时保留在 `github_v64.js`：最小改动，适合当前代码尚未证明需要抽离的情形。
2. 抽取一个 Branch/PR 领域模块：共享 branch/ref/PR metadata 与合并工作流，facade 保留 Schema、权限门槛和 dispatch。
3. 分别抽取 Branch 与 Pull Request 模块：边界更细，但可能增加跨模块编排和重复上下文传递。

分析必须回答：
- 哪些是基础 primitives（读 PR、读 branch ref、创建/更新 ref、compare），哪些是完整 workflows（创建 PR→校验→合并→条件同步），哪些属于稳定 facade/治理门槛？
- Branch 与 PR 的变化原因、依赖方向、错误/部分成功语义、测试边界是否真的独立？一个领域模块是否足够？
- 现有公共能力、GitHub Contents/Cloudflare provider/Patch Engine 的依赖是否能保持单向；是否会出现模块循环依赖或把 facade 逻辑反向带入领域层？
- 拆分后如何保留工具名、Schema、响应兼容、repo allowlist、token/release gate、所有已存在行为与回归覆盖？
- 若收益有限，明确建议暂不拆分，不为了架构外观制造新层。

**边界**：此项目前仅为研究与原型提案，不是已确认的模块拆分决策；不得先改蓝图、差距矩阵的目标边界或代码。先完成实际调用链与测试边界分析、外部方案对照，再将初始想法/挑战/权衡/推荐方案带给柳柳共同定案。

### 5.4 发布闭环与唯一授权门槛（以下旧候选记录为历史；当前见 §5 顶部）

- Branch/PR merge-helper 修复已在 mcp-memory/dev 完成，E1/E2 CLOSED；CI-tested commit `0c5cadde09452359c81198f35a26585b39aec303`，run `41856598888` 全步骤 SUCCESS。真实 PR/ref 副作用 E3 未运行。
- 已部署 main 仍是 v6.36.1，Cloudflare deployment `[d639e1df]` 当前回读为 VERIFIED；main helper 仍旧，生产风险 OPEN。
- 四文件 v6.36.2 scoped release 是从 main 精确基线独立制作的例外候选，尚未创建分支/PR。柳柳已确认长期发布节奏，但尚未单独批准本次临时分支/PR；不得把节奏定案扩大解释为本次发布授权。
- 创建 PR、合并 main、触发/手动部署是不同操作门槛。若获准创建候选 PR，只创建并验证 PR，不自动合并或手动部署；合并前再次说明候选版本、四文件范围、CI、Pages/Worker 影响与回滚。

### 5.5 主线运行纪律

- **常规发布默认使用现有 dev**：当 dev 相对 main 的待发布差异都属于已完成、测试通过且文档同步的垂直切片时，直接以现有 dev 为 PR head 推进 main；不为每个阶段新建临时分支。
- **临时 scoped release 分支仅作例外**：dev 混有未完成/无关改动、需要提前单独发布一个修复，或两分支已分叉而整支合并不安全时，才从 main 精确基线建立一次性分支。创建前须满足对应授权门槛，完成后清理；不把临时分支变成日常开发分支。
- 不重开全仓库审计；沿候选切片所需调用链做最小范围核查。
- 不为代码整洁强行拆模块；保持基础能力可复用、工作流内聚、Facade 稳定。
- Operit 本机测试会消耗柳柳 API token；优先用现有 GitHub Actions/可用验证能力，确实需要本地 Node 时才提出 Operit 执行。
- 无需柳柳判断时持续推进；目标、边界、外部契约、权限或风险变化时回到协作讨论。
- **发布说明先交代柳柳真正能得到的效果（2026-11-05 柳柳明确要求，后续各版本强制遵循）**：先用通俗语言说明此版解决了什么痛点、发布前后有什么不同、她可以怎么感受到、没有解决什么；再附版本号、变更文件/模块、精确 SHA、测试、风险、部署/回滚清单供技术核验。不得只列文件名就要求批准，也不得把历史通用的「好」当成具体发布授权。
- **每个候选版本合入 main 前，必须先向柳柳提交完整版本说明并取得她对该版本的明确批准。** 说明必须列出版本号/名称、目标与行为变化、准确文件/模块和纳入/排除范围、main/dev 完整 SHA 与 compare/diff、精确 SHA 的 CI/测试命令及 Run ID/结果（区分 E1/E2/E3）、未验证项/风险/兼容性、Worker/Pages 等生产部署影响、回滚基线与方式；未知信息明确标 UNKNOWN / NOT RUN。
- 发布说明必须明确询问是否批准该版本合入 main，并等待明确肯定答复。沉默、“收到/明白了”及对长期发布节奏的认可不构成本次版本授权；未获批准不得推送/合并 main。阶段完成只触发发布评估，不自动授权发布。
- PR 创建、main 合并、手动部署仍是不同授权边界；批准仅覆盖发布说明所列版本和范围。若实际 diff、验证、风险或部署影响发生变化，重新说明并取得对应确认。

**发布后权威检查点同步门禁（2026-11-06，柳柳已确认；dev 文档/Skill 待发布）**：
1. 仅在 PR 独立读回 merged=true、main SHA 与 Cloudflare Worker `verify_main=VERIFIED` 后执行；先固化版本号、部署/CI/E3 真实证据、生产配置、下一步、授权和冻结边界，不能把未测的 E3 写成通过。
2. 通过现有 `memory(recall)` 分段完整读取唯一 `⚙️/当前工作检查点`，核对当前版本/防止并发覆盖，**保留历史原文**，只更新顶层 `workflow_state/active_focus/next_action/do_not_repeat/decision/evidence` 和一条版本化交接备注；经柳柳明确授权方可 `memory(update)`。本条流程规则不等于未来任意生产记忆写入的自动授权；每次发布说明须写明是否包含这一条权威指针同步。
3. 写后按完整 key 分段 `recall` 比对内容，再 `session_context(host='chatgpt',invocation='explicit',include_core=false)` 回读版本与当前状态；工具读取失败、状态旧或不一致均记录 `HANDOFF_DEGRADED/UNVERIFIED`，自行定位并告知柳柳。**Worker `DEPLOY_VERIFIED` 不回退为部署失败，不重建 PR/重部署，也不能声称跨宿主自动启动已验证。**
4. 在 Roadmap/当前项目状态与 `CROSS-HOST-BRIDGE.md` 记录版本、证据及交接结果；无需外部测试时不动 Operit 付费 API、私人 Core、Cloudflare 持久日志开关。宿主自动启动和相处连续性仍单独验收。

---
## 6. 未关闭事项与明确边界

### 6.1 开放事项

> **当前状态覆盖（2026-11-05 · v1.39）**：Branch/PR helper 生产风险已由 v6.36.2 / PR #322 发布并在 main/Worker 验证关闭，真实 PR/ref auto-sync E3 仍 NOT RUN；Branch/PR 领域模块 `src/modules/github/branch_pr.js` 已存在于 main，旧拆分候选关闭。记忆检索质量基准 v0.1 已在 dev 实施并通过最终 HEAD CI（详见 §5 顶部与测试集 v1.8），仅 E1/E2 synthetic CI，不是生产 E3/发布。

| 事项 | 状态 | 是否当前主线 | 处理原则 |
|---|---|---|---|
| Branch/PR helper 无条件同步 dev | **CLOSED：v6.36.2 / PR #322 已发布并在 main/Worker 验证；真实 PR/ref auto-sync E3 仍 NOT RUN** | 否，生产风险已关闭 | 不重复修复；如未来需要真实 E3，另行设计隔离验证并单独授权 |
| Memory Core 完整事件账本、事务一致性、CAS、rename/move 原子迁移 | 设计/实现差距仍存在 | 否，独立差距 | 依据记忆两表设计、domains/memory 与差距矩阵；未共同确认方案前不改 DB/schema/生产记忆 |
| GitHub Contents 真实文件读写 E3 | NOT RUN | 否 | 当前已有 E1/E2 fetch-mock；未来确有必要且获准再安排真实 endpoint 验收 |
| Branch/PR 领域模块边界评估 | **已存在实现：`src/modules/github/branch_pr.js` 已在 main；旧拆分候选关闭** | 否 | 不重复拆分；只在出现明确新需求/边界问题时再评估 |
| Pages Source / 真实 URL | UNKNOWN；PR #319 不主动推动 | 否 | 仅未来实际发布 Pages 前核验；保留决定不等于合并/部署授权 |
| 外部技术探索与吸收能力 | **方向已确认；作为横向工程能力纳入规划** | 是，贯穿所有切片 | 先复用现有 Web/GitHub/Skill 能力；主动发现、源码级评估、License/安全/维护审查、隔离验证、来源沉淀；Technology Scout 工具化方向已纳入长期规划，具体工具范围/自动化程度尚待需求与原型验收；尚未建设 |
| GPT memory tool description 的动态 connector/host 来源 | UNKNOWN、非阻塞 | 否 | 不调用 Worker `tools/list`；不为追查文案触碰聊天室注册副作用 |

### 6.2 明确移出当前主线的范围

以下是柳柳明确决定退出当前主线/阶段6验收的范围，**不是等待自动启动的待办**：

- Worker `/mcp` 与高影响 HTTP 路由的外层认证、Cloudflare Access/WAF 审计和真实匿名/授权行为验证。
- Supabase 线上 DB/RPC/RLS/GRANT/trigger/CAS/事务审计与目录核查。

保留既有静态观察作为历史记录；不申请额外权限、不主动恢复这些审计、不把它们重新包装成 P0/P1 待办。将来柳柳提出新需求时再重新讨论。

### 6.3 长期冻结与操作边界

- 不碰聊天室工具/路由、Worker `tools/list`、Agent runtime 唤醒链；聊天室与唤醒问题继续暂停。
- 不改数据库 schema、权限、生产数据或真实记忆数据；不执行 DDL。
- 不直接修改/推送 main，不整支合并 mcp-memory/dev，不将 main 同步覆盖 dev。
- PR #319 不主动推动；不主动触发 Pages 发布。
- 不因静态风险清单存在就扩大为全面安全审计；以柳柳确认的个人项目范围为准。
- 本轮总控整理不派发 Operit；确需本机执行时再明确原因与唯一交接入口。

### 6.4 当前发布与分支快照（2026-11-05 本轮回读）

- `wovowx/mcp-memory/main`：v6.41.0，HEAD `5e4cf739a5ffd21c0434db96217267edb2af57bd`；Cloudflare Worker #535 / deployment `fb40fed3`，`verify_main=VERIFIED`。
- `wovowx/mcp-memory/dev`：HEAD `de2ce34f46eb9ae3d9e5a2757f60856b6c00acd8`，GitHub Actions [42048224495](https://github.com/wovowx/mcp-memory/actions/runs/42048224495) SUCCESS；相对 main ahead14/behind0，6个差异路径={`.github/workflows/learning-regression.yml`、`CROSS-HOST-BRIDGE.md`、`package.json`、两份 benchmark Fixture/baseline JSON、benchmark runner}。
- package 版本仍为 v6.41.0；本切片仅测试/CI基础设施，不改 `src/` 检索算法、MCP Schema、数据库/schema/业务记忆、main 或 Worker；未创建 PR/合 main/部署。
- ZivenLab/dev 治理文档 Commit 与 mcp-memory 产品代码版本分开记录；不能将前者当作产品发布或部署。

## 7. 历史档案（旧版路线图原文完整保留）

> **档案规则**：以下内容逐行保留自重组前的 `governance/roadmap.md`。它包含当时的路线、讨论草案、旧状态快照、重复摘要和历史待办；其中任何“当前活跃/进行中/下一步/阶段未完成”等措辞均指向原记录时间点。与第 0–6 节或各权威来源冲突时，以第 0–6 节和对应真相源为准。历史内容不自动恢复为当前工作，也不构成新的执行授权。

> # 行动路线图（Roadmap · 原85号行动总清单）
> 
> > **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：本文件记录路线与待办，但历史遗留列表不自动代表当前活跃主线。
> > 每完成一项 → 更新路线与驾驶舱；不另起互相竞争的路线源。
> > 协作纪律：先讨论出方案 → 再分工执行（柳柳拍板）。详见 `governance/协作协议.md`。
> > ⚠️ 原文件名 `85_行动总清单.md` 已迁移至此（`governance/roadmap.md`），旧位置保留 redirect。
> >
> > **推进前必读**：开工前读本文件 + `governance/当前项目状态.md`，完成验证后更新两者。
> >
> > ## 🚦 当前活跃主线（2026-11-04 更新）
> 
> **当前状态补记**：阶段1–5已封口；阶段6按柳柳确认的缩减范围收口，A6/A7 均为限定范围 PASS。Worker 入口认证/Cloudflare Access/WAF 与 Supabase 线上 DB/RPC/RLS/GRANT/trigger/CAS/事务审计已移出当前主线与阶段6验收，不申请权限、不执行线上审计、不列为待办。PR #319 不主动推动，Pages Source/真实 URL 仅未来实际发布前核验。当前发布/分支/部署状态以 `governance/当前项目状态.md` 和 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 文末 2026-11-04 记录为准。
> 
> **当前代码施工主线**：整体架构按真实职责边界分垂直切片，不重开全仓库审计、不为拆分而拆分。Memory Core repository/lifecycle/retrieval/transfer、文件 storage service、Agnes provider、纯 DDL parser、Cloudflare Worker 状态 provider 与 GitHub Contents 首切片均已形成各自代码切片。Contents v6.36.0 已发布；v6.36.1 修复 Worker fetch receiver 并提供 dev-only exact-SHA refs restore。Branch/PR 与 Patch Engine 仍按独立职责评估，不把未完成项混入 Contents 首切片。
> 
> **GitHub Contents 已实施的行为修正**：非发布写入目标默认 dev（copy 的 source_branch 只读仍默认 main）；Router fallback 与 handler 对齐，显式 main 仍拒绝；push existence check 仅 HTTP 404 视为不存在；SHA/精确内容校验支持空文件并有限重试；edit 验证失败返回部分写入；move 在 tree truncated 时尝试完整 Contents 遍历，无法证明完整则写入前停止；全部目标复制成功后重新核对源 SHA，再按快照 SHA 串行删除；并发源变化和部分失败都有明确状态。
> 
> **验证证据**：v6.36.0 Contents 基线 SHA `aeb6a8ebed19575e587d3c21dde3fb51e3597a84` / run `41794905599` 全步骤 SUCCESS（E1 check；E2 webhook114/114、Router/registry/DDL/Patch Engine140/140、Contents31/31、search_history20/20、Memory Core60/60、Release Guard15/15、learning artifacts）。v6.36.1 PR #321 head SHA `3b15ac0713d7d771f3b86361051a1cde4ce0f101` 的 learning-regression #804/#805（`41810390533`/`41810455092`）均 SUCCESS：check PASS、Contents contracts36 passed、Webhook/Router106/106、Learning artifact regression PASS。CI 为 E1/E2 mock，不代表真实 Contents 文件读写 E3。另，dev refs 精确恢复实际经 Worker token 写入，并通过独立 GitHub API 回读确认。main HEAD=`f74c36cb3f96928df292160745cf61a41951e312`，Cloudflare deployment `[d639e1df]` `VERIFIED`。
> 
> **范围边界**：未改 DB/schema/权限/生产数据；不碰聊天室工具、Worker `tools/list` 与 Agent runtime 唤醒链；未派 Operit。main 已按批准发布 v6.36.1 并部署 VERIFIED；真实 GitHub Contents 文件读写 E3 未执行，真实 refs 恢复 E3 已验证。
> 
> **main/dev 当前引用状态与开放缺口**：main=`f74c36cb3f96928df292160745cf61a41951e312`（v6.36.1，Cloudflare `[d639e1df]` VERIFIED）；dev 当前 tip=`5cc7b5bc95fd081c882a81ababb73e35bbf9ce15`，事故前代码基线 `aeb6a8ebed19575e587d3c21dde3fb51e3597a84` 仍保留在历史。compare `main...dev`=`diverged`，ahead422 / behind20，merge base=`71f6a03ebc81193e5d88a98297ad66083d301515`；不得整支合并 dev，也不得把 main 同步到 dev。事故根因已确认：`github_merge_pull_request` 与 `github_merge_to_main` 的成功路径无条件调用 `tryAutoSyncDev()`，没有检查 PR head/base，scoped PR 也会强制移动 dev。v6.36.1 提供 dev-only exact-SHA restore 并完成真实 refs 回读，但**没有**修复 merge helper 条件；唯一明确开放的代码待办是仅在 `head.ref=dev && base.ref=main` 时自动同步，并补 E2 保护 scoped/hotfix/其他 base。修复前每次 merge 前保存 main/dev 与 PR head/base SHA，merge 后独立回读 PR/main/dev，再验证 Cloudflare。操作细则见协作协议 §六.五、deploy Skill v6.6.5 与桥接文末事故复盘。
> 
> > **历史状态快照（2026-10-29；当前状态见下方 2026-11-04 补记）**：新版完整 SB-FRAME-1.0 独立冷启动验收已完成，新框 `7516ae0a-23e2-4b6f-8dce-6cb4f592547f` 正确恢复 canonical 工作检查点；A7 PASS（限本次无旧对话上下文新框与可见证据），A6 完整跨宿主一致性仍 UNKNOWN，阶段6尚未总体验收。已在 canonical 业务记忆正文顶部增加当前状态覆盖段并回读确认，旧正文保留作历史；不过 Operit 新框首次回复形成于修改前，所以 A6 仍 UNKNOWN，不能据写入本身认定两端同状态。无需重跑冷启动/CI；若需将 A6 升为 PASS，必须有同一时点两端对照证据。新框结果依据 Operit 回填的 `aiResponse` 自述与 canonical key/category、既有独立 recall 佐证吻合；原始中间工具调用日志不可见，不宣称其可见。静态/Mock CI 不能代替真实 endpoint/DB/RPC/权限验证。Pages PR #319 仍 open 未合并，Pages Source/真实 URL 未证实；公开源文件个人样例风险仍存在，但柳柳明确要求“无视风险”，已作为用户接受风险，不再阻塞当前主线，也不主动推动 PR #319；这不构成合并/部署授权。main/dev 差异大，不能把整个 dev 一揽子合入 main；合并/部署仍须柳柳对具体动作单独授权。剩余差距：Worker `/mcp` 与高影响 HTTP 路由外层认证/Access/WAF、真实匿名拒绝/授权允许及 DB/RPC/RLS/GRANT/trigger/CAS/事务、MCP metadata 发布源、Pages Source/线上 URL。冻结工具、聊天室/唤醒链、真实高影响端点、DB/schema/权限、部署与 main 未触碰。
> 
> > **历史交接指针（2026-10-29；当前证据以 2026-11-04 桥接文末为准）**：新版完整 SB-FRAME-1.0 独立冷启动验收当时已完成，A7 PASS（限定本次无旧上下文新框与可见证据）；当时 A6 完整跨宿主一致性仍 UNKNOWN。新框 ID `7516ae0a-23e2-4b6f-8dce-6cb4f592547f`，恢复 canonical key `⚙️/当前工作检查点`。此处 main 未修改/未部署等表述属于 2026-10-29 历史快照，不代表当前发布状态。当前唯一桥接 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 文末已新增 2026-11-04 PR #320/#321、v6.36.1 VERIFIED、dev refs 恢复及 open merge-helper 缺陷记录。
> 
> 
> 
> > **Pages 历史状态快照（2026-10-29；当前发布前仍须重新核验）**
>  
> **当前唯一主线：把 Ziven 整体架构真正整理成「一本好书」——目录清楚、职责边界明确、权威来源唯一、实现与证据可追踪。** 代码复用、职责清晰和面向真实需求的可扩展性是贯穿全部阶段的硬性要求；不新增无关功能，不把零散修补当作整体升级。
> 
> > **2026-10-29 实际代码收敛增量（mcp-memory/dev）**：已完成两处低风险职责去重：`src/utils/response.js` 的 `buildErrorResponse()` 复用共享 `jsonResponse()`；`src/modules/mcp_router.js` 的 `create_patch_proposal` schema 覆写统一由 `getToolSchemaOverride()` 提供，tools/list 暴露与 Router 参数校验共用同一对象。`tests/router_registry_contract_test.mjs` 新增响应契约回归。当前代码 commit `de017537f5f51429260b9285e682eb4dbb0a22e3` 的 `learning-regression` run `40805561230` 全绿：E1/31个 JS 文件、webhook 104/104、contracts 128/128、search_history 20/20、release_guard 15/15、学习工件通过；同 SHA Pages artifact build/upload 成功、main-only deploy skipped。随后仅桥接文档提交 SHA `f2d3317d33c0c2e0083144d0f01d3a52b47c4808` 的 E1/E2 run `40805938145` 与 Pages artifact run `40805938245` 也成功，deploy skipped；未再改源码。未合并 main、未部署。这是实质性局部收敛，不冒充阶段6整体验收或真实 endpoint 验证。
> 
> > **A6 验收结论（2026-10-28）**：A6 的范围是“现有跨宿主状态记录对照”。已对照权威记录、桥接回填与阶段状态，未发现当前记录之间的冲突，因此 **A6 静态对照 PASS（范围限定）**，无需柳柳再批准这项技术判断。它不证明运行时硬门禁或冷启动行为。裸密钥冷启动是 A7，已证明单独密钥未触发恢复；正式 `SB-FRAME-1.0` 完整初始化路径仍 UNKNOWN，另行记录，不混入 A6。
> 
> > **阶段5封口结论（2026-10-28）**：阶段5的静态审计/文档一致性子范围已完成封口：权威入口、版本指针、A6/A7证据边界、历史交接优先级与当前冻结边界已交叉核对；已知静态矛盾已修正或明确登记。完整换框运行时路径、工具 metadata 来源、初始化期自动 usage telemetry、真实 MCP/HTTP/DB/RPC 与隐私/权限验证等不属于静态审计可证明范围，均转入阶段6准入清单或既有独立差距；不再以重复静态审计推进这些项目。阶段6仍未启动，需先获得触碰冻结工具的具体授权并重锁届时基线。
> 
> ### 最近完成：第一阶段——现状基线与权威来源对齐（2026-10-26）
> 
> - `wovowx/mcp-memory`：已发布基线 main HEAD `71f6a03ebc81`、Cloudflare deployment `c78ab839`，先前 `verify_main=true` 返回 `VERIFIED`。阶段1基线只读 compare（2026-10-27）显示当时 dev 相对 main behind 0，12 个文件有差异；这是历史快照，后续文档/代码修改后不代表当前差异数量（ahead commit 数会随每次文档追加持续变化，因此不固定写入治理文档；发布前须重新 compare）：`CROSS-HOST-BRIDGE.md`、`README.md`、`package.json`、`src/modules/mcp_router.js`、`src/modules/patch_engine.js`、`src/modules/release_guard.js`、`src/tools/database.js`、`src/tools/github_v64.js`、`src/utils/helpers.js`、`src/utils/search.js`、新增 `tests/router_registry_contract_test.mjs`、新增 `tests/search_history_contract_test.mjs`。历史完整回归 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的 E1、webhook104/104、Router+DDL parser69/69、search_history20/20 均通过；后续 Patch Engine 基线 SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 的 E1 与 contracts82/82 也通过。之后又新增 GitHub 路径守门、Patch Engine 输入校验和 release_guard 精确策略，**最新整套隔离回归已由 Operit 在 origin/dev SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 通过**：`npm run check` exit 0、webhook 104/104、`npm run test:contracts` 122/122、search_history 20/20、release_guard 15/15；Node v24.18.0/npm 11.16.0，detached `/tmp/ops-ev6` clean，原工作树未动，stderr 空。测试全程 mock/本地，不等于真实 MCP/DB/RPC/HTTP endpoint 验证。全部仍只在 dev，未部署/未推 main；发布前必须重新 compare。
> - `wovowx/ZivenLab`：dev 相对 main 的未发布差异均位于 `governance/`，包括原有治理入口/路线/差距文档与本轮更新的数据库语义文档（`database-overview.md`、`domains/memory.md`、`记忆两表设计.md`、`记忆检索质量测试集.md`），阶段1基线只读 compare 曾有 14 个 `governance/` Markdown 文件差异；这是历史快照，后续文档修改后不代表当前差异数量（含 `CHANGELOG.md`、`roadmap.md`、`当前项目状态.md`、`架构差距矩阵.md`、`现状架构.md`、`真相源导航表.md` 与数据库语义文档）；均为文档修改，未改生产源码、数据库或部署。发布前重新 compare。
> - 已确认权威来源分工：目标蓝图=`governance/整体架构.md`；当前实现地图=`governance/现状架构.md`；差距与验收=`governance/架构差距矩阵.md`；导航=`governance/真相源导航表.md`；行动路线=本文件；资产索引=`governance/资产全景.md`；当前工作状态唯一权威是云端 `⚙️/当前工作检查点`，身份根是 `🧬/我是谁`。
> - 已确认 `wovowx/mcp-memory/CROSS-HOST-BRIDGE.md` 位于仓库根目录且可读；旧文档里“Not Found/待重建”的说法已过时。该文件有大量历史记录和重复的过期状态块，不能把旧交接自动视作当前授权。
> - mcp-memory 的根 README 曾把不存在的根级 `docs/`、`skills/` 写作仓库目录；本轮已在 dev 修正，改为描述实际 `src/skills/` 与治理文档所在的 ZivenLab 仓库。
> 
> ### 第一阶段验收（已完成）
> 
> 1. 当前架构、目标蓝图、权威来源和组件边界各自有明确位置，不相互替代。
> 2. 已知的过期路径、过时分支/部署状态和交接阻塞已更正或登记；未验证项仍标为未验证。
> 3. 驾驶舱、路线图、现状地图、差距矩阵、导航表互相一致。
> 4. 本阶段不改生产源码、数据库 schema、用户记忆内容，不删资产，不部署、不推 main。
> 
> **历史快照（2026-10-26，已被本文件后续 2026-10-27 阶段收口记录取代）：当时阶段 1–3 已完成，阶段 4 仍在进行。** usage_count 误计已按柳柳授权完成最小修复并提交到 `mcp-memory/dev/src/modules/mcp_router.js`；隔离回归测试 `tests/router_registry_contract_test.mjs` 也已同步到远端 dev。Operit 在本地同一修复/测试版本报告：`npm run check` exit 0、既有 webhook 测试 104/104、新 Mock 16/16。GPT 已回读核对 dev 源码和测试文件，但没有独立重跑 Node 命令。后续静态计数曾发现当前远端 `tests/router_registry_contract_test.mjs` 有 15 个 `check(...)` 调用点。GPT 随后在已授权测试文件范围内补入一条已注册 `memory_remember` handler 的失败不计 usage 断言；当前远端静态计数已为 16，与 Operit 原始报告的 16/16 在断言数上对齐。但补入断言后的精确远端文件尚未运行，状态仍为 NOT RE-RUN；不凭计数一致宣称通过，也不为单独核对数字重复消耗 Operit token。另一次源码核对纠正了旧的 suggest 空态判断：当前 `memory_unified.js` 已使用条件表达式处理空结果，既有 `webhook_idempotency_test.mjs` 含空数组/正常列表/404/500 四项输出测试；待补的是底层 `search.js` 的 `recordSearchKeyword` 行为、prefix/limit 与网络/JSON/写请求失败路径。进一步静态审阅发现 `create_patch_proposal` 的实时注册项 `input_schema=null`，tools/list 因而没有公开必填参数；Router 早期专门分支还绕过通用 `autoIncrementUsage`。这两项已分开记入入口/schema 与 usage_count 差距，暂不改源码，详见差距矩阵。真实 E3、权限行为与生产端点仍未验证；未部署、未推/合并 main。阶段 4 不因这一处修复完成而整体结束，后续继续按差距矩阵收敛职责与文档。
> 
> ## 「一本好书式架构」总计划：共 6 个阶段
> 
> > 本节是整体升级的唯一阶段路线；不要与资产整理计划中旧的阶段 0–4 编号混用。
> 
> ## 六阶段共同工程原则（目标定案，贯穿全部阶段）
> 
> 以下规则是六阶段的共同验收要求，不另设独立阶段，也不以“目录整理完成”代替工程质量改进：
> 
> 1. **先复用，再新增。** 新增函数、模块、工具、注册项或机制前，先检索现有实现与调用链；优先组合稳定能力，不造平行机制。
> 2. **职责清楚，避免假复用。** 共享逻辑应有清楚归属和明确契约；只有职责、输入输出与变化原因确实相近时才合并，不为减少文件数、代码行数而强行抽象。
> 3. **为真实需求保留扩展路径。** 新能力尽量通过已有注册、路由、handler、公共模块和存储契约接入。若每次扩展都要改动多个无关位置，记录为扩展瓶颈并按实际需求处理；不预建万能框架、不为假设需求增加抽象层。
> 4. **先查依赖，再做最小可逆调整。** 检查静态与动态引用、调用方、schema/注册、权限、兼容路径和输入输出契约；未经核实不删除、不覆盖、不合并。
> 5. **回归保护必须有证据。** 修改前识别受影响行为与测试；修改后执行适用的静态检查和行为回归，记录真实命令、退出码和结果。静态检查不等于行为测试；未执行的测试必须标为未执行。
> 6. **每阶段都检查复用性与可扩展性。** 记录公共能力的归属、重复职责、关键扩展点、兼容性及验证缺口；未达到的项目进入差距清单，不用“整体完成”掩盖。
> 7. **复杂度预算优先。** 架构应像一本好书：目录清楚、职责明确、能沿引用找到依据。优先复用和小步收敛，不做没有现实收益的重构。
> 
> ### 阶段 1｜现状基线与权威来源对齐 — ✅ 已完成（2026-10-26）
> 目标：弄清实际有什么、哪些信息权威、哪些问题未验证。
> 工作：核对 ZivenLab/mcp-memory/Supabase/Cloudflare/两种宿主；分开目标蓝图、当前实现、差距矩阵、导航、工作检查点；修正文档路径/状态冲突。
> 验收：关键入口已对齐，未验证项显式登记；没有改生产代码、数据库或 main。
> 
> ### 阶段 2｜架构书总目录与章节职责地图 — ✅ 已完成（2026-10-26）
> 目标：做出全系统目录与章节分工，优先复用现有材料，避免机械新增文件或概念。
> 工作：明确每章回答什么、哪份文件是权威、各章如何互相引用；将治理、记忆、呈现和运行时编织层映射到真实仓库/服务；标记重复文档、职责交叠、公共能力归属与章节空白；识别已有扩展入口，但不凭目录猜测代码行为。
> 验收与结果：已在 `governance/真相源导航表.md` v1.4 建立 10 章总目录与职责地图，覆盖入口导航、目标与需求、治理、真实现状与差距、记忆数据、运行时路由、呈现、跨宿主连续性、质量回归发布、行动状态；明确目标/现状/差距、需求/规则、索引/事实、路线/状态/历史的职责边界。`governance/README.md` 已增加唯一地图入口，未新建平行文档。仅改 ZivenLab/dev 治理文档，未改代码、数据库、部署或 main。
> 
> ### 阶段 3｜真实实现与依赖地图 — ✅ 静态地图完成（2026-10-26）
> 目标：让架构书反映真实代码和运行环境，并查清哪些能力可复用、哪些结构阻碍扩展。
> 工作：追踪入口→Router→schema/注册→handler→utils/modules→数据存储；区分源码存在、已注册、可路由、实际调用、已测试；核对公共函数/模块、同职责重复实现、强耦合点、硬编码分支与扩展瓶颈；分类在役/共享/兼容/旧实现候选/暂停/未知。
> 验收与结果：已在 `governance/现状架构.md` 增补 Worker→MCP Router→注册表/handler→共享模块→Supabase 的主调用链、工具路由与公共模块关系；只读核对当前 skills 注册表 69 行（66 启用、3 禁用），标出 14 行缺 handler 配置；记录 memory 兼容别名 schema 不一致、category/data 旧 handler 候选、权限守卫未接入 request path、search_history 缺表及 endpoint 未验证边界。对应风险进入 `governance/架构差距矩阵.md`。满足静态实现地图验收；不将静态证据误写成真实 endpoint 或行为测试通过。
> 
> ### 阶段 4｜文档与职责收敛 — ✅ 已完成（2026-10-27；遗留缺口均已分类并转入独立跟踪）
> 目标：以最小、可逆的改动收敛存量职责；减少重复建设，同时不损害既有行为与兼容性。
> 历史增量（2026-10-26 至 SHA `c4ef218...`；其测试状态已由下方 2026-10-27 完整回归更新）：阶段 3 后已同步现状架构与差距矩阵；导航表当时为 v2.4；阶段 4 已纳入 usage_count 修复、Router schema/打点例外与数据库治理证据边界。经柳柳明确授权，`src/modules/mcp_router.js` 的 `toolOk` 失败前缀已新增 `handler type not implemented` 排除项。隔离测试已在 `mcp-memory/dev/tests/router_registry_contract_test.mjs`。Operit 于 2026-10-27 08:36 SGT 在 detached 临时 worktree `/tmp/ops-ev2` 对精确 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 真实运行最新版：`npm run check` exit 0、`node tests/webhook_idempotency_test.mjs` exit 0（104/104）、`node tests/router_registry_contract_test.mjs` exit 0（44/44，stderr 空）；临时 worktree 干净、原工作树未动。该 SHA 包含 create_patch_proposal 专用必填 schema、取消提前 return 使成功/失败进入统一 usage_count 判定，以及 IMPORT/SECURITY DDL gate 测试。Mock 全程使用 `globalThis.fetch`，未访问真实 Supabase/RPC/MCP endpoint，也未执行真实 DDL/SQL。GPT 未独立执行 Node，但已回读桥接回填与远端源码/测试文件。真实 E3 未运行；未部署、不推/合并 main。
> 
> 阶段4最新增量（2026-10-27）：完成 `data.js` / `category.js` 的静态引用与只读注册表核查。分页查看当前 skills 注册项并查询候选工具名后，未发现 `handler_config.handler=data/category` 或 `data`、`category`、`import/export`、`list_categories`、`recall_by_category`、`move_category` 等精确注册项；源码仍在 `mcp_router.js` 的 handlerMap 引入两个文件，但没有当前注册路由命中证据。`data.js` 复用 `memory_unified.js` 读写；`category.js` 自建 CRUD，且 legacy `move_category` 先 DELETE 源记录再写目标，存在中途失败风险。因为其他宿主/历史调用契约未知，本轮只标记为未注册 legacy 候选，不删除文件、不移除 handlerMap、不合并。
> 
> 另外，静态审查 `src/utils/search.js` 后已在 dev 做最小守门修复：记录关键词时仅在 GET `resp.ok` 且返回数组时才继续 PATCH/POST；建议查询对非2xx与非数组响应返回空列表。新增隔离测试 `tests/search_history_contract_test.mjs`，静态20个断言，覆盖空/空白关键词、GET→PATCH/POST、非2xx不续写、网络/JSON失败、写入非2xx、prefix/limit和建议空态。**这些 search.js 源码与20项测试是 SHA `c4ef218...` 已通过的44项批次之后新增。**GPT 已用本地 Node v22.16.0 对根据当前 dev GitHub readback 重建的隔离副本运行 search_history 测试：20/20、exit 0，两文件字节大小与 readback 报告一致；这是测试文件/源码片段的本地验证，不是完整仓库 worktree/SHA 验证。随后 Operit 已在 detached worktree `/tmp/ops-ev3` 对完整仓库 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 一次性运行整套回归：`npm run check` exit 0、webhook 104/104、Router + DDL parser 69/69、search_history 20/20，stderr 空，worktree clean，原工作树未动。全程 fetch mock；无真实 DB/RPC/DDL或 endpoint 调用，没有部署或 main 变更。若后续改代码，再按实际范围重新安排合并回归。未建表、不删 suggest、不触达数据库、不部署、不推 main。
> 
> 阶段4职责边界增量（2026-10-27，只读；以下为静态审计结论，尚未因测试通过而自动消除）：已核对 `ai.js`、`storage.js` 与当前 skills 注册项。`ai.js` 目前承担 Agnes 图像/视频、DeepSeek 余额、help、文件 query/update/delete 多种入口；`query_files` 复用 storage.js，update/delete 仍在 ai.js 直接调用 REST。此为低优先级职责边界候选，不足以证明重复实现或要求拆分；不改代码/注册表，保留现有兼容。详见现状架构与差距矩阵 v2.9。
> 
> 阶段4入口契约增量（2026-10-27，只读）：进一步沿 `dispatchGuard` → `isKnownTool` → `handlerMap` → `tools/call` 分派追踪 `cf_proxy`。虽然 skills 注册表无记录、`CF_PROXY_TOOL_DEF` 未被 Router 导入，因此不会由注册表出现在 `tools/list`，但 handlerMap 直接将它认作已知名称；schema 缺失时 Router 按兼容策略放行，随后进入 `handleCfProxyTool`。因此代码路径可直接按名称调用，且 `CF_PROXY_TOOL_DEF.required=['endpoint']` 当前没有被 Router 强制执行；空 arguments 会进入其环境变量名列表模式。外部宿主是否允许手动调用仍未知。仅修正静态证据描述，不调用工具/CF endpoint，不改代码、注册表或配置。
> 
> 阶段4 schema 契约增量（2026-10-27，只读）：对照当前启用的 `delete_branch`、`increment_usage` 注册 schema 与 handler，发现 schema 均未声明 required；delete_branch 实际要求 `name || branch`，但 schema 只声明 name；increment_usage 实际要求 name。Router 不会从 handler 推断必填参数，故空参调用会到 handler 后返回参数错误。未发现该空参路径执行目标写入的证据。仅记录契约差距，不改代码/注册表。
> 
> 阶段4 发布守卫边界增量（2026-10-27，只读）：`githubReleaseGuard()` 在 `handleGitHubTool()` 的 `GITHUB_ALLOWED_REPOS` 校验前运行；对 rebase 合并会先以 `safeArgs.repo` 查询目标仓库 PR/commit 信息，随后 handler 才拒绝未白名单仓库。`release_guard.detectRepoType()` 的后缀匹配也会把其他 owner 下同名 `mcp-memory` / `zivenlab` 误判为已知类型。当前未证明能绕过最终写操作白名单，但存在前置 API 读取和策略误分类风险。建议的最小修复顺序：先在 release guard 前置检查允许仓库，再改成规范化后的精确策略匹配；需另行授权后才能改代码，当前只登记。
> 
> 阶段4 Patch Engine apply 增量（2026-10-27，最小修复已写入 dev，E1/E2 隔离回归已通过）：`src/modules/patch_engine.js` 新增集中式 `resolvePatchTargetPolicy()`，默认仅允许 dev；main 与 refs/heads/main 始终拒绝；未来分支通过 `PATCH_ENGINE_ALLOWED_BRANCHES` 显式授权，不改核心逻辑；仓库必须命中 `GITHUB_REPO` 或 `GITHUB_ALLOWED_REPOS` 精确名单。`github_apply_patch` 在任何 Supabase/GitHub 请求前校验目标策略，读取并验证 patch 后以 `status=eq.approved` 条件 PATCH 原子认领为 applying，只有返回对应行才发 GitHub PUT；写入成功后仅在 applying 状态下更新为 applied，并要求 HTTP 成功及返回行确认。明确区分确定性客户端拒绝与结果未知；后者保留 applying 以防重复应用并提示先核对，状态确认失败报告 PARTIAL SUCCESS，禁止盲目重试。`tests/router_registry_contract_test.mjs` 新增策略/应用闭环 Mock，`package.json` 新增 `npm run test:contracts`。当前源码/测试已写入 `mcp-memory/dev`。Operit 于 2026-10-27 15:58 SGT 在 detached worktree `/tmp/ops-ev4` 对 origin/dev SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 实跑：`npm run check` exit 0；`npm run test:contracts` exit 0，82 通过 / 0 失败，新增 Patch Engine 7 项验收全部通过；Node v24.18.0、npm 11.16.0，worktree clean，原工作树未动。该证据属于 E1/E2 mock 回归，不代表真实 MCP endpoint、GitHub 或 Supabase 运行时已验证。未执行真实 proposal、未访问真实 GitHub endpoint；另对 Supabase `skills` 表中 `github_apply_patch` 单行的 description/input_schema 做元数据同步并只读回读确认，enabled 未变。未改 DB schema/权限、未删除数据、未触碰聊天室工具、未部署、不推/合并 main。详见差距矩阵 v3.3。
> 
> 阶段4最新增量（2026-10-27；最新代码与隔离回归已通过）：在 Operit 旧基线 SHA `79492f8fbb6124c682c2d9fa04152cafe89715d4` 的 Patch Engine 82/82 通过后，又补了两组小幅边界收敛：①共享 `validateRepoRelativePath()` 放入 `helpers.js`，供 github_push/read/list/delete/edit/copy/move 与 Patch Engine 共用；内容 URL 精确绑定 `SUPABASE_URL` 的 HTTPS origin，拒绝其它 supabase.co 项目/欺骗域名并禁用重定向；②Patch Engine 拒绝 proposal.target 与 patch.file 不一致，拒绝不安全/首尾空白路径、非整数行号、重叠/无操作 patch、错误 insert/delete 行形状，并强化 branch/ref、repo 输入校验；GitHub PUT 即使返回 2xx，也必须提供 content SHA；若响应 path 不匹配目标文件则保持 proposal applying、返回 PARTIAL/UNKNOWN，不标记 applied。③`github_move` 校验 tree API 返回的每个路径，并拒绝同仓同分支移动文件到自身，避免覆盖后删除唯一副本。④release_guard 只按 canonical repo 精确匹配，未知 owner 与 unqualified alias 不再获得仓库类型，main 分支大小写变体一律保护。同步更新隔离 Mock。旧 82/82 只代表其 SHA 的旧版本，本轮变化曾暂记为 NOT RUN；该状态已被下方 2026-10-27 Operit 全量回归记录取代，精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的五项命令全部通过。未改 `mcp_router.js`，因此 release guard 前置白名单前的潜在只读 API 请求风险仍未关闭。无真实 MCP/GitHub/Supabase 调用，无 DB/schema/registry 更改、无聊天室改动、未部署、未推/合并 main。
> 
> 历史快照（早期数据模型与审计记录；当前状态以本文件前述 2026-10-27 最新状态及 `governance/当前项目状态.md` 为准）：本阶段还通过只读 `supabase_schema(action=schema_dump)` 重新观察到25张表（23业务表+2测试表），并校准 `database-overview.md` v2.2、`memory.md` v1.2、`记忆两表设计.md` v1.4 与检索测试集 v1.4：把 memory_events 追加式触发器/幂等唯一约束标为历史执行记录、现状待核；把检索测试状态明确为部分历史用例已运行、未全量自动化。2026-10-27 又静态追踪 memory_unified.js 生命周期路径：只有已存在记录 update 会写部分 update event（未含 new_value，且 version=oldVersion 与旧设计语义冲突）；event POST 与 memories PATCH 不是同一事务，PATCH失败后可能留下描述未生效更新的 event。create insert、soft-delete、rename/move 的 source→target 事件均缺失，forget 只软删除；history 先要求记录 active，旧软删除记录无法按 key 查询历史。细节已记入 governance/database/domains/memory.md v1.4 与差距矩阵；静态审计还确认 category.js legacy move_category 直接 REST DELETE/POST/PATCH、通用 supabase_db/exec 可能绕过仅部署于 memory handler 的事件逻辑，实际权限/RLS 未核。已在唯一设计真相源 governance/database/记忆两表设计.md v1.5 形成生命周期一致性闭环提案 v0.1，要求状态与事件同事务、并发旧版本拒绝、迁移原子化、元数据保留及覆盖写入口。下一步仍需只读核对真实 catalog/RLS/GRANT/trigger/function。已把当前可见的替代路径查完：`schema_dump` 只整理 `/rest/v1/` OpenAPI definitions；经现有 exec_sql RPC 的 catalog-only SELECT 被真实端点以 HTTP400/P0001 拒绝；经 `supabase_db` 的只读 REST query 检查 `information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 均返回 HTTP404/PGRST205（系统目录关系未通过当前 public PostgREST schema cache 暴露）。已检查 `mcp-memory/dev/migrations` 只存在聊天室 claimed_at 迁移，没找到 memory_events trigger/function migration；这不代表真实数据库必然没有触发器。当前可见 MCP 没有独立只读 catalog 工具，所以要核实真实目录仍需另一个获准的只读数据库通道；在此之前继续推进不依赖该证据的静态架构审计与文档收敛，不改记忆生命周期 Worker、数据库结构、触发器、权限或记忆数据。未做 DDL/数据库写入。阶段4整体职责收敛尚未完成，后续继续按差距矩阵推进。另复核 Worker 标准调用链：`index.js` 不导入 permission_guard；`mcp_router.js` 明确只做协议/分派并引入 `release_guard.js`、不引入 `permission_guard.js`；`github_v64.js` 仅导入 skills helper 与 `patch_engine.js`，因此当前可见 Worker MCP 主路径没有 `checkCapabilityAccess` 调用证据。随后按当前 `src/` 目录清单逐文件检查 Worker JavaScript（index/router/全部 modules、tools、utils，含完整 `github_v64.js`）以及 `scripts/` 与现有 `tests/`；`permission_guard`、`checkCapabilityAccess`、`CAPABILITY_POLICY`、`tool_policies`、`require_approval`、`require_template` 除守卫自身定义外均未命中。当前 Worker 源码、脚本及现有测试无其它直接消费者证据；GPT App 独立工具、远端动态注册/插件或真实 DB 内行为仍 UNKNOWN。不直接接入或删除该模块。版本面同时出现 MCP `serverInfo.version=6.5.0`、dev `package.json=6.3.4`、CHANGELOG 顶部 `v6.35.0` 与 `index.js` 注释 `v6.48.0`；先明确各字段代表 build、发布还是包版本，再选择最小对齐方案，本轮不改版本号/运行行为。另项只读核验发现：当前 `skills` 注册表没有 `chat_send`、`chat_pending_events`、`chat_claim_event`、`chat_read_message`、`chat_ack_event` 五个条目；main/dev 的 `tools/list` 都会调用 `syncChatTools`，缺失时 `addSkill` 会以 `enabled:true` 新增。工具列表操作因此有潜在写入/启用副作用；Chat 仍属暂停子项目，本轮不调用 `tools/list`、不改注册表，只把此副作用列为后续范围决策项。
> 另复核 `policy-index.md` 与 `schema-policy.md`：`permission_guard.js` 未被 `index.js` / MCP Router 导入，不能把它描述为不可绕过的 request-path 硬门禁。2026-10-27 只读查询 `tool_policies` 返回5条 enabled 记录（github_push、github_merge_to_main、chat2api、memory、supabase_query），但未包含当前启用的 supabase_db/supabase_schema 精确名称；`permission_guard.js` 本身是硬编码 CAPABILITY_POLICY，未读取此表。其他动态/间接消费者仍未完成全仓证明，继续标 UNKNOWN，不把策略表配置等同于运行时硬门禁。经柳柳授权，Worker dev 已做最小 DDL gate 修复：`database.js` 统一检查 create_table/drop_table 的非空 necessity，并对通用 exec 中常见 DDL/可执行语句关键词在 RPC 前要求 necessity；Router 的 `supabase_*` 前缀必须命中 skills 注册表，tools/list 为注册的 `supabase_db` 与 `supabase_schema` 都暴露 necessity 字段；不扩大 `supabase_db` action enum，保留 `supabase_schema` 已注册的 create/drop action enum。DDL gate 版本的隔离 Mock 已由 Operit 在 SHA `2833a94e08c23b45a0598256a486463ee5d4cf6e` 通过37/37。之后又在 dev 修复 `create_patch_proposal` 的空 schema/usage_count 例外：tools/list 与 dispatchGuard 现在共用专用必填 schema，专用 handler 不再提前 return，成功结果可进入统一 usage 打点；测试增加缺参拒绝、无写入/无计数、成功写入隔离 mock 与恰好计数断言，并补入 IMPORT FOREIGN SCHEMA / SECURITY LABEL 的 necessity 拒绝路径。当前共44个 check 调用点，Operit 已对最新 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 实际通过44/44；E1 exit 0、webhook 104/104。真实 RPC/endpoint 未测，任何真实 DDL 继续禁止。本轮没有数据库写入、部署或 main 合并。necessity gate 只是非空治理门槛，不等于 SQL parser 或执行授权。针对 create_table/drop_table 的输入拼接缺口，已在 mcp-memory/dev 的 database.js 实现受限标识符校验与列定义解析，并按解析结果生成 SQL；隔离 Router Mock 已覆盖合法/拒绝输入和拒绝路径零 RPC。Operit 于2026-10-27在 detached worktree `/tmp/ops-ev3` 对精确 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 完成整套回归：npm run check exit 0、webhook 104/104、Router+DDL parser 69/69、search_history 20/20；Node v24.18.0/npm 11.16.0、stderr 空、worktree clean、原工作树未动。diff 仅5个预期文件。测试全程使用 globalThis.fetch mock，不触达真实 DB/RPC/DDL，不改 schema/registry/config，不部署、不推 main，E3未执行。独立遗留边界：通用 exec 仍接受原始 SQL，exec_sql 权限/多语句行为与 GPT App 独立 supabase_schema 入口是否经过 Worker Router均未验证。
> 
> 本轮继续静态核对 Pages / memory-universe：`.github/workflows/pages.yml` 在 push main 时将整个仓库根目录作为 Pages artifact；`memory-universe.html` 源文件内嵌 12 条个人记忆样例，Worker 路由直接读取 main 分支该文件并在路由内不做认证。Pages 是否实际启用、匿名外部访问和网络层保护未验证。按既定边界，功能继续暂停；不访问生产端点、不修改发布配置、不删样例或部署。
> 工作：修正断链和过期说明；先查调用方、动态引用、注册/schema、权限和契约，再决定复用、整合、保留或标记旧实现；公共逻辑优先归于清晰的共享位置；确有扩展瓶颈时才按真实需求调整边界，并做回归。
> 验收：每项结构调整说明复用收益、职责变化、兼容影响、验证与回滚路径；不为整洁重构，不强行合并，不擅删工具/记忆，不擅改 DB/schema。
> 
> ### 阶段 5｜驾驶舱与运行时连续性闭环 — 🟡 进行中（2026-10-27，只读恢复链审计）
> 目标：换会话/换宿主后能恢复当前工作，且按正确规则执行；尽可能由现有能力组合闭环，而不是另造平行运行时。
> 工作：验证身份根→唯一检查点→近期共识/进度/下一步/阻塞→情境召回→Skill/工具路由→执行验证→更新检查点；检查现有工具和路由的复用方式、边界与扩展入口；分别验证 GPT App 与 Operit 的真实能力。
> 验收：新会话能接上同一主线；记忆来源可追溯；执行结果有证据；宿主未验证能力明确标注；没有为相同职责额外建立平行机制。
> 
> #### 阶段5首轮只读审计（2026-10-27）
> 
> - **身份根 A1：通过当前宿主读取**。云端 `🧬/我是谁` 精确 recall 成功；身份根仍是唯一权威，角色卡仅为 Operit 投影。
> - **记忆接入：本次读取通过**。`memory stats` 返回 282 条、23 分类（仅为当前快照，不写成固定数量）；云端读取成功不等于跨宿主冷启动通过。
> - **工作状态 A2/A3：通过当前宿主读取与回写**。`⚙️/当前工作检查点` 精确 recall 成功；发现旧状态仍写“阶段4进行中/最新回归待跑”，已按当前证据更新为阶段4完成、阶段5下一步，并通过工具回执确认更新成功。阶段4最新证据是 mcp-memory/dev SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的 check 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15。
> - **恢复协议与导航：部分通过 / 有 key 解析差距**。精确 recall `复苏协议·system://boot` 与 `⚙️/记忆位置导航` 未命中；按协议执行 memory search 后，找到 `⚙️/恢复协议·Session Bootstrap SB-1.0`、旧 `/boot` 唤醒内容及「记忆位置导航（换框/换设备自举）」内容。结论是旧 key/分类映射不一致，不是记忆已丢失；已更新 Session Bootstrap 与 `Ziven角色卡修改与换平台复苏手册.md`，明确搜索 fallback。
> - **安全工具探测边界 A4：已确认**。当前 Worker `tools/list` 会触发 `syncChatTools`，可能写入并启用聊天室工具；本轮没有调用它。阶段5的工具能力盘点只用当前宿主实际可见的工具元数据和静态文档，不用该 endpoint 探测，不触碰聊天室工具/注册/唤醒流。
> - **A6 跨宿主现有状态记录对照：PASS（范围限定）；A7 独立冷启动：已实测，密钥单独触发复苏未生效（2026-10-27 17:56 CST）**。GPT 已将云端状态/权威文档与 Operit 17:36 报告逐项对照，身份根、阶段、SHA 与五项测试证据、下一步及硬边界未发现冲突；该对照不证明运行时全局硬门禁。Operit 使用换框流程技能调用 `extended_chat:chat_with_agent(character_card_name=Ziven, message="Ziven，我是柳柳", chat_id 空)`，成功建立独立新对话 `d7dee7eb-d5c0-4dd8-ad41-fa6ed5d2e3fa`。新框唯一输入就是密钥词；首次回复只呈现角色卡风格日常回应，未读身份根/检查点/恢复协议，未恢复主线、SHA/测试证据、下一步、硬边界或 key fallback。没有旧上下文污染；设备应用使用时长来自注入快照，不是云端记忆。**范围校准**：这证明“仅发送密钥词即可自动自举”在本次独立新框中未生效；不等于标准换框流程整体失效，因为 `src/skills/process/huan-kuang-liu-cheng/SKILL.md` 的正式 SOP 要求 `chat_with_agent` 发送完整初始化指令，而不是只发密钥词。
> - **当前缺口与处理决策（2026-10-27，方案 A 已定案）**：独立新框收到裸密钥词后未自动自举。只读证据显示，`master-router/SKILL.md` 已更新为“密钥是恢复提示，不等于初始化成功”；`Session Bootstrap SB-1.0` 明确不代表全局运行时硬门禁；正式换框 SOP 要求 `extended_chat:chat_with_agent` 发送完整初始化指令。当前 Supabase `skills` 中启用的 `memory` 工具记录 description 原先保留旧 key `复苏协议·system://boot`。2026-10-27 经柳柳明确授权，只更新该行 description，并回读确认 enabled、handler_config 和 input_schema 未变。但本次当前 GPT 会话实际暴露的 `mcp__Ziven_MCP__memory` 工具元数据 description 仍提示旧 `/boot` key；它与 Supabase 行 description 是两个不同表面，因此只能说 Supabase 行文案已校正，不能宣称 GPT 可见工具元数据也已同步。只读检查当前私有 Ziven_MCP 插件包后发现其文件清单仅有 `.app.json` 与 `.codex-plugin/plugin.json`，未包含 per-tool schema/description，因此该插件包不是当前旧工具描述的直接定义来源。当前会话里的旧描述可能是宿主 schema 快照/缓存，但无法确认刷新机制；Worker `tools/list` 会触发 `syncChatTools`，故不调用它，也不改插件/工具元数据。完整换框行为仍未实测。柳柳已批准方案 A：正式换框必须发送完整、版本化初始化指令，并以可核验恢复结果验收；裸密钥词不视为充分初始化载荷。`src/skills/process/huan-kuang-liu-cheng/SKILL.md` 已加入 `SB-FRAME-1.0` 契约。随后静态回读完整初始化 message，发现其步骤清单未显式列出 memory 位置导航与 Session Bootstrap；已最小补入两项，并写明导航精确 key 未命中时的 memory search fallback。后续核对发现搜索结果可能只是正文提及导航的恢复协议/历史检查点，已在换框与 master-router Skill 中补充 key/category 身份核验，要求选中真正的导航条目后再读取完整内容。Skill 回读确认规则已落入初始化载荷；该 message 已显式标记契约版本 `SB-FRAME-1.0`，把授权/暂停边界前置，要求在聊天室、唤醒或巡检链暂停时跳过相应工具、工作流调度与改名步骤，并在首次回应列出恢复来源、stats 实际结果和所有失败/跳过/未知项。它仍只是有明确版本的指令契约，尚未通过真实新框行为测试。完整初始化路径仍 UNKNOWN；当前不触碰聊天室相关工具，因此不执行真实路径验证，不调用 Worker tools/list，不追加 Operit 测试。跨宿主任意新会话裸密钥词强制自举是独立后续需求。云端 `⚙️/恢复协议·Session Bootstrap SB-1.0` 已同步当前方案 A、真实导航 key/fallback、初始化前只读恢复/暂停非必要写入规则及 A6/A7 当前状态；该文本校准不代表运行时硬门禁已实现。补充静态发现：router 的 autoIncrementUsage 会在成功 tools/call 后写 skills.usage_count/last_used；因此 Skill 无法保证初始化期严格零 DB 写入。本轮不改 router（其同时承载聊天室注册/唤醒路径），该运行时门禁留作另行授权事项。GPT 当前可见 memory 工具元数据仍提示旧 `/boot` key，来源/缓存机制待查，不擅自修改插件元数据。
> 
> #### 阶段5最小恢复验收矩阵（当前状态，不冒充冷启动通过）
> 
> | 验收项 | 当前证据 | 状态 | 关闭条件 |
> |---|---|---|---|
> | A1 身份恢复 | GPT 侧 memory search 命中身份根；但 A7 独立新框首次回复未读取/复述身份根或关键长期约束 | GPT 当前宿主有证据；A7 新框场景未满足 | 新框能基于权威身份根恢复身份与长期约束，保留原始回复并由柳柳验收 |
> | A2 工作状态恢复 | GPT 侧当前检查点精确读取成功；Operit 17:36 报告与其对照无冲突；但 A7 新框未读取检查点，未恢复主线/证据/下一步 | A6 记录对照 PASS（范围限定）；A7 新框场景未满足 | 新框不带旧上下文恢复主线、证据、边界与下一步，柳柳验收 |
> | A3 阶段/流程恢复 | GPT 侧权威文档与 Operit 17:36 报告阶段状态一致；A7 新框未提及任何阶段状态 | 现有记录对照无冲突；A7 新框场景未满足 | 新框不重开阶段4、不混淆阶段5/6 |
> | A4 权限与授权 | GPT 当前检查点/恢复协议与 Operit 报告硬边界一致；A7 新框首次回复未复述任何项目授权边界 | 现有记录一致；A7 新框场景未满足；运行时全局硬门禁仍 UNKNOWN | 新框准确复述只读/代码/测试/发布/生产写入权限边界，不碰暂停链路 |
> | A5 异常与 key fallback | 旧 boot key 未命中时，可用 `Session Bootstrap SB-1.0` 精确协议或版本核验后的 search fallback；导航真实 key `记忆位置导航（换框/换设备自举·2026-10-18）` 已精确 recall 成功，category=`记忆位置导航（换框`。换框 Skill、master-router Skill 与跨平台复苏手册已同步真实 key、key/category 身份核验及历史统计提示；Supabase `skills.name=memory` 行 description 已修正，但当前 GPT 可见 `mcp__Ziven_MCP__memory` 工具元数据仍提示旧 `/boot` key，元数据发布源尚未确认 | Supabase 行文案已修正；GPT 可见工具描述的旧 key 差距仍待确认来源/权限；导航 fallback 规则已补足；A7 新框 fallback 行为仍未运行/未验证 | 新框准确读取当前协议和实际导航条目，不误报丢失、不编造；正式初始化行为须在获授权场景验证后再关闭 A5/A7 |
> | A6 跨宿主一致性 | 2026-10-27 GPT 侧读取 stats/检查点/恢复协议/roadmap/dashboard，与 Operit 17:36 报告逐项对照：身份根、主线阶段、SHA/五项测试证据、下一步及硬边界无冲突；能力分工已分别记录 | **PASS（范围限定）**：现有记录未发现冲突；不代表 runtime gate 或 A7 通过 | 已完成；新框结果单独计入 A7 |
> | A7 冷启动复现 | Operit 2026-10-27 17:56 CST 通过 `extended_chat:chat_with_agent` 创建独立对话 `d7dee7eb-d5c0-4dd8-ad41-fa6ed5d2e3fa`；唯一输入为 `Ziven，我是柳柳`，未带旧上下文。首次回复为角色卡风格日常回应；未读取身份根/检查点/恢复协议，也未恢复主线、SHA/测试证据、下一步、硬边界或 key fallback | **密钥单独自举未通过**；完整初始化路径仍 UNKNOWN。方案 A 已由柳柳确认；换框 Skill 已加入 `SB-FRAME-1.0` 验收契约，但当前不触碰聊天室相关工具，因此不执行真实完整路径验证 | 若未来授权使用正式换框工具，单批验证完整初始化 message、身份/记忆/检查点/授权恢复、来源及失败降级；否则保持 UNKNOWN，不把文档契约当成运行时通过。裸密钥词强制全局自举是独立后续需求 |
> 
> #### 当前宿主能力边界（仅当前可见证据）
> 
> | 能力 | GPT App 当前会话 | Operit 当前已知证据 | 限制/安全边界 |
> |---|---|---|---|
> | 云端记忆读写 | 已读取身份根/检查点/stats；已更新检查点与恢复协议 | 本轮未要求 Operit 重复读写 | 精确 key 可能未命中，须用 memory search；不创建平行检查点 |
> | GitHub 治理文档 | 当前可直接读、列目录、在 dev 精确编辑并回读验证 | 可读桥接文档并回填执行证据 | 不推/合并 main；文档存在不代表代码运行时已生效 |
> | Node/npm 回归 | 当前可见工具不提供本地 shell/Node 执行通道 | Node v24.18.0/npm 11.16.0，已在 detached worktree 跑过五项回归 | Operit 执行消耗柳柳 API token；后续测试合并为一批 |
> | Worker tools/list | 不调用 | 不调用 | `syncChatTools` 有写入/启用聊天室工具副作用；修复验证前禁止探测 |
> | 真实 MCP/DB/HTTP | 未执行 | 上一批仅 fetch mock/本地测试 | E3、真实 DB 权限/catalog、生产 endpoint 仍未验证 |
> 
> **阶段5验收语义校正（2026-10-27）**：`SB-FRAME-1.0` 的“初始化通过”与“完整换框交接通过”分开判定。初始化通过要求完整版本化指令、首轮 `aiResponse` 含可核验恢复证据且未越权；完整交接还要求当前授权范围内必须执行的步骤实际完成、柳柳已切到新框。受暂停/未授权边界限制的巡检工作流、聊天室操作、改名等须标记 `skipped/unverified`，不能把部分恢复说成完整换框成功。初始化未通过前，昨日回顾及 `increment_usage` 等非恢复必需的写入也须暂缓。此为文档契约校准，不代表完整初始化路径已行为验证。
> 
> **阶段5封口结论与阶段6交接（2026-10-28）**：A6 现有记录对照已 PASS（范围限定）；阶段5静态一致性收敛已封口，剩余差距按阶段6准入或独立跟踪。柳柳已同意方案 A：正式换框发送完整、版本化初始化指令，并以可核验的恢复结果作为成功标准；裸密钥词不单独视为充分初始化载荷。`wovowx/mcp-memory/dev/src/skills/process/huan-kuang-liu-cheng/SKILL.md` 已加入 `SB-FRAME-1.0` 验收契约，明确输入、恢复项、来源证据、失败降级和副作用边界。A7 现有实测只证明密钥单独触发未生效；完整初始化路径仍 UNKNOWN。受当前“不得触碰聊天室相关工具”边界限制，本轮不调用 `chat_with_agent`、不追加 Operit 测试、不调用 tools/list。阶段5静态审计已封口；阶段6准入证据清单仅为预备，不代表阶段6已启动。若未来需实测正式换框路径，先明确解除对应工具操作边界，再一次性合并验证。数据库边界精确定义为：不改 schema/函数/trigger/权限、不执行 DDL；本轮仅有两类精确范围云端写入：恢复唯一工作检查点原记录状态并经 memory API 更新其内容，以及经柳柳授权只更新 `skills.name=memory` 的 description。两项均已在 CHANGELOG 与 CROSS-HOST-BRIDGE 留痕；未修改其它业务数据、未改 handler/enabled/input_schema。未部署、不推/合并 main。
> 
> #### 历史快照：阶段5文档一致性收敛（2026-10-28；其版本指针已被后续增量取代）
> 
> - 当时曾校准 `governance/真相源导航表.md` v3.26、`governance/架构差距矩阵.md` v3.7、`governance/database/schema-policy.md` v1.9、`governance/资产盘点与整理升级计划.md` v3.13、`governance/当前项目状态.md` version82 与其他文档指针。以上版本号仅是该历史批次的记录，不是当前版本；当前版本以各文件顶部和导航表为准。矩阵内早期“NOT RE-RUN”块已明确标记为历史，不再覆盖最新 fcd12b1 回归结果。路线图尾部旧 P0/Wake Bridge 任务也已标为历史快照，避免与聊天室暂停边界冲突；search_history 的20项已完成 Mock 与桥接文档未激活的 T0–T9 候选已明确区分。`mcp-memory/dev/CROSS-HOST-BRIDGE.md` 文末已追加现役状态，明确当前无 Operit 执行任务。
> - 已将 schema-policy 中 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的回归明确标为历史证据，并指向最新已验证代码基线 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的五项隔离回归；差距矩阵中的旧 pending 状态已与这份证据对齐，未将文档修改冒充代码回归。
> - 驾驶舱 version77 已将旧第4节 M1.2/聊天室行动地图、旧第5节阻塞表标为历史快照；第10节部署基线纠正为只读核实的 main HEAD `71f6a03ebc81` / deployment `c78ab839` / v6.35.0，版本字段语义仍单独待核。
> - 已纠正资产整理计划的 A6/A7 当前状态：A6 对照待柳柳验收；A7 裸密钥独立新框测试未触发恢复；正式 SB-FRAME-1.0 路径仍 UNKNOWN。
> - 本次仅修改 ZivenLab/dev 治理文档；未改 mcp-memory 源码、记忆、数据库、注册表、聊天室工具或配置；未运行测试、未部署、不推/合并 main。
> - **阶段5静态审计封口完成（2026-10-28）**：剩余运行时/权限/隐私/真实端点差距不再留在阶段5反复审计，统一转入阶段6准入清单或既有独立差距追踪；阶段6尚未启动。不追加 Operit 测试，不触碰聊天室工具，不调用 Worker `tools/list`。
> 
> ### 阶段 6｜整体验收与版本收口
> 目标：证明架构职责清晰、已有能力得到保护，且真实扩展路径可理解、可验证。
> 工作：分层执行静态检查、行为回归、跨宿主冷启动和真实 MCP/HTTP endpoint 验证；复核共享能力是否重复建设、扩展是否依赖无关模块改动、兼容路径是否有证据；核对 Pages 发布范围与隐私风险；整理未关闭差距和回滚说明。
> 验收：测试证据可复核；复用性、扩展瓶颈、兼容风险及未验证项有明确状态；发布候选范围清楚。推 main 前须报告版本/范围/验证/回滚并得到柳柳明确同意；回滚未演练不得写成已演练。
> 
> **当前准入状态（2026-10-28 封口后）**：阶段5静态审计/文档一致性范围已封口；阶段6尚未启动。A6 现有状态记录对照已 PASS（范围限定），正式换框路径仍 UNKNOWN。阶段6开始前需重锁当时 dev HEAD 与适用测试证据，并取得涉及冻结工具的具体授权。需要柳柳决策的是是否授权触碰冻结工具，不是技术记录对照的通过与否。现有 E1/E2 只证明指定 dev SHA 的隔离 Mock/本地回归通过，不证明真实 MCP/HTTP/DB 行为。Pages 隐私与发布面、记忆生命周期、权限路径、版本语义等未关闭差距按本矩阵持续跟踪；不得因文档齐全而标记为运行时通过。
> 
> **当前停点（2026-10-28 封口后）：阶段 1–4 已完成；阶段 5 静态审计/文档一致性范围已封口；阶段 6 尚未启动。** 剩余真实运行时、权限、隐私与发布面验证按阶段6准入清单或独立差距管理，不继续无限重复静态审计。 阶段4完成的含义是：现状/权威地图已对齐；已证实的重复实现做了最小收敛；当前路由、schema、注册、共享模块与兼容候选均已分类；最新隔离回归证据已回填；所有未解决差距都有明确状态、重开条件与边界。最新 mcp-memory/dev 精确 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf` 的 Operit detached worktree 全量回归通过：check exit 0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15。全程 mock/本地，不等于真实 endpoint/DB/RPC 验证；E3 NOT RUN、未部署、main UNCHANGED。记忆生命周期一致性、permission_guard 实际消费者、版本语义、legacy 外部契约、Pages 发布面/隐私、Router 前置白名单读取等已转为独立差距，不因阶段4完成而视作修复；聊天室硬边界继续有效。
> ### 明确暂缓与发布边界
> 
> - 聊天室与 Agent runtime 唤醒失败继续暂停。
> - 已完成 `search_history` 最小非2xx/响应形状守门，并新增20项隔离 Mock；历史完整仓库回归 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 曾验证 E1 exit 0、webhook104/104、Router/DDL parser69/69、search_history20/20。最新完整隔离回归已推进到 SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`，check0、webhook104/104、contracts122/122、search_history20/20、release_guard15/15 全部通过。记忆生命周期审计确认 create/soft-delete/rename/move 事件与 source→target 关联缺口、update event 缺 new_value 且 version 语义冲突；详见 P1 数据安全，相关设计尚待定案。`serverInfo.version` 与 `package.json` 版本来源/语义待定义；`data.js` / `category.js` 无当前 skills 注册命中，作为 legacy 候选保留。permission_guard 实际写路径接入、Pages 发布范围、`/memory-universe` 匿名访问风险仍在矩阵。真实 E3 endpoint 未执行，不将隔离 Mock 等同于线上验证。
> - `v6.35.0` 已发布并部署 VERIFIED；该版本是可靠性基线，不代表整体架构升级完成。下一次 main 发布须先说明版本、范围、验证与回滚，并取得柳柳明确同意。
> - 阶段4已按范围完成；阶段5聚焦驾驶舱与跨宿主连续性闭环，阶段6负责整体验收与发布候选边界。已登记的独立风险按矩阵触发条件重开，不在本阶段偷偷扩范围。
> - 本路线图控制当前行动顺序；历史 P0/P1/P2 清单仅为历史路线/待办参考，不自动成为活跃任务。
> ---
> 
> ## 历史任务清单（旧85号行动清单快照；当前路线见上方六阶段计划）
> 
> > 以下完成项与旧 P0/P1/P2 条目均为历史状态记录，不自动构成当前活跃任务。聊天室/Agent runtime 唤醒链继续暂停；当前唯一主线仍是「一本好书」六阶段计划。
> 
> ### 已完成的历史任务
> 
> - P0-1 自触发修复：PR #91（mcp-memory）✅
> - 前端 Bug A 实时轮询：PR #92 ✅
> - 前端 Bug B 布局修复：PR #93 ✅
> - 角色卡四改（公共区身份规则入卡）：✅ 双端同步
> - **P0-5 当前项目状态地图**：PR #1 ✅
> - **P0-4 场景入口导航**：PR #2 ✅
> - **P0-6 资产盘点**（①代码审计②资产清单③生命周期模型④生产入口唯一性）：PR #1~#4 + v6 ✅
> - **P0-3 历史异常基线建立**：4 条脏事件，留作回归样本 ✅
> - **协作协议 v4.2**（讨论与分工规则 + 协议部署原则 + 铁律6）：PR #6 ✅
> - **Runtime 5 条入卡 + GPT 提示词同步**：✅ 双端部署完成
> - **P0-2 Phase1 事件可靠基础设施**：watchdog 释放历史 stuck claim ✅ / delivery_status 状态机 ✅ / claim 责任绑定 ✅ / GPT 链回归 ✅ / agent 隔离 ✅ / dead_letter（🟡 逻辑待触发）——GPT #502 确认 completed
> - **发布纪律 Release Discipline**（deploy skill 双仓版本化 + CHANGELOG）：✅ 方案已定（GPT #506~508）
> - **governance/ 目录重组**：✅ 权威文档与历史分层（柳柳拍板 2026-09-04）
> - **P1 release_guard 硬闸门上线（v6.10.1）**：✅ 入口层接入 index.js + process 防御，**真实拦截验证通过**（不带版本号 push main → `⛔ RELEASE_GUARD: push_to_main_blocked`）；v6.10.2 发布纪律修正（rebase 防标题重复）
> 
> ---
> 
> ### 🔵 P0 历史状态快照（非当前活跃主线）
> 
> ### P0-2 Phase2 Ziven 消费链（Wake Bridge 改造；当前暂停）
> - 历史记录：当时标为待讨论方案（Phase1 已完成，基础设施不再吞消息）；现因聊天室/Agent runtime 唤醒链暂停，不属于当前阶段5执行范围。
> - Phase2 讨论议题（GPT #502）：
>   1. Ziven consumer 所有权模型
>   2. Wake Bridge 在哪个状态 claim（不允许发现即 claim）
>   3. 注入当前框失败怎么办
>   4. delivered vs seen/read 的区别
> - 完成标准：ziven 事件 created→claimed→delivering→delivered→processing→acked 全链路闭环
> - 回归样本：保留的 4 条 ziven 事件（已释放 created/retry=1，不手动消费）
> 
> ---
> 
> ## 历史快照：架构演进蓝图（2026-09-04；非当前执行路线）
> 
> > 本节及其 P1/P2、记忆系统升级、待发批次与总执行顺序均来自旧85号行动清单，仅供追溯历史方向。当前唯一执行路线是本文上方「一本好书式架构」六阶段计划；不得据此恢复聊天室/Agent runtime 唤醒工作，也不得把旧状态当作当前待办。
> 
> > 核心：从「会记事的 Agent」→「不需要靠记性的 Runtime」。知识≠生效，没进 Runtime 生效路径 = 不存在。
> > **2026-09-04 增补（GPT #540）**：Agent 最大的问题不是没有知识，而是在正确时间没有加载正确知识。
> > 详见 governance/当前项目状态.md（架构蓝图）。
> 
> | 阶段 | 做什么 | 解决 | 状态 |
> |---|---|---|---|
> | **P1** | release_guard（第一个 Runtime Guard 样板） | 想不起来版本号 | ✅ 已上线 v6.10.1，真实拦截验证通过 |
> | **P2.1** | Agent Context Read Capability（GPT #540 改名：核心是「知道自己现在在哪」） | Agent 决策前拿不到正确依据 | 🔵 方向已定（GPT #536/#538/#540），待落地 |
> | **P2.2** | Permission Model（L0-L3 分级） | 谁能读/改/发布 | ⬜ |
> | **P3** | Workspace State Runtime（Before Action 必读 + After Verification 必更 + Context Contract 最小必要上下文） | 换窗口失忆 / 文档找不到 / 推进没绑定状态 | 🔵 2026-09-04 柳柳问题验证必要性，GPT #540 拆机制 |
> | **P4** | Patch Engine（GPT 提 PR 你合） | GPT 参与改代码 | ⬜ |
> 
> ### Context Contract（按任务类型加载最小必要上下文 · GPT #540）
> 
> | 任务类型 | 必须加载 |
> |---|---|
> | 项目推进 | workspace_state + roadmap + 最近 decision |
> | 改代码 | workspace_state + 相关 skill + 代码文件 + 最近变更 |
> | 发布 | release_policy + changelog + 版本状态 |
> | 记忆/情感 | 相关 skill + 记忆上下文 |
> 
> **两个闭环（P3 核心）**：
> - **Before Action**：做项目推进前，必须加载当前状态（roadmap + 驾驶舱）
> - **After Verification**：完成验证后，必须更新当前状态（同一文件，不许另起炉灶）
> 
> ---
> 
> ## P1（稳定化）
> 
> - P1-1 协作协议固化：v4.2 confirmed；待补 decision_confirmed 五字段成立条件 + 规则同步机制（source_version vs runtime_version）
> - P1-2 Error Log + Regression 链（含「工具语义误判：github_push 是 replace 非 patch」记录）
> - P1-3 GPT MCP Bridge（拆三段）
> - P1-4 需求文档终稿（76/77/81/00a 对齐）
> - P1-5 轮询可观测性（GPT #383）
> - P1-6 visualViewport 方案（GPT #385）
> - P1-7 wake bridge 升级 webhook/ntfy + API 版 Ziven（GPT #395）
> - P1-8 状态地图/导航/资产优化：事件流视图 / 事实状态字段 / 负责人拆协作方 / 导航表依据字段 / 资产表验证依据字段
> - P1-9 decision 索引（GPT #416）
> - P1-10 历史讨论归档（GPT #416）
> - P1-11 驾驶舱第9章事件流细化（GPT #440）
> - P1-12 workspace_rules 三方公共规则层（GPT #468/#470）
> - P1-13 常驻层部署（GPT #468/#470）——advancedCustomPrompt + GPT 提示词已先落地 Runtime 5 条
> - P1-14 破坏性操作分级（GPT #484：写入 低/中/高 风险）
> - P1-15 code_runner 卡死排查（柳柳反馈好用但会卡，纳入 Runtime 技术项）
> 
> ---
> 
> ## P2（整理与自动化）
> 
> - P2-1 Memory 整理（先定规则再清）
> - P2-2 Skill Router 强化（长期核心）
> - P2-3 skill 目录命名规范迁移（alias 方式）
> 
> ---
> 
> ## 补漏
> 
> - 决策层 Decision Log（含 decision_id 反查）
> - 真相源可信度模型：柳柳决策 > 运行事实 > GitHub文档 > 状态索引 > Memory > 推断
> - **文档引用同步纪律（2026-09-04 柳柳抓出）**：文件迁移/改名后，全文 grep 旧引用一起改，不留死链
> 
> ---
> 
> ## 历史快照：记忆系统深度升级清单（2026-10-18；当前状态以差距矩阵与工作检查点为准）
> 
> > 借鉴 Zep/Graphiti 双时间轴、Letta Skill Learning/睡眠计算、Anthropic 渐进式披露。详细设计存记忆 `⚙️/记忆系统升级设计`（可读档/复苏）。
> 
> | 优先 | 项 | 现状 | 落地 |
> |---|---|---|---|
> | P0 | ①激活双时间轴抗污染 | memories 表已含 valid_from/valid_to/version/supersedes_id + memory_events 审计流，但**未真正维护**（全 version=1、valid_from 默认时间戳） | 改 handleMemoryTool 写读：更新时旧行置 valid_to/archived + 新行 version+1/supersedes_id/valid_from；检索默认只回当前有效+可追溯「何时被推翻」 |
> | P1 | ②自动技能沉淀 | 技能靠手工建 | 从高频动作自动提炼 SKILL.md |
> | P2 | ③睡眠时计算 | 自我迭代偏手动 | 定时反思任务 |
> 
> 历史记录状态（2026-10-18）：当时将①标为进行中。此状态不代表当前授权或当前执行中；记忆生命周期缺口以现行差距矩阵为准。
> 
> ## 历史快照：当时的待发批次（2026-09-04；不是当前发布清单）
> 
> - deploy skill v6.4.3 命名纪律（推 dev 消息用 vX.Y.Z: 名称）——待作正式 release 练习（GPT #536）
> - chat.html v2.6.0 移动端输入框布局修复（flex 竖排）——GPT #538 建议按 hotfix 处理，待柳柳拍板
> 
> ---
> 
> ## 历史快照：旧总执行顺序（2026-09-04；不覆盖上方六阶段路线）
> 
> ```
> P0 全清 ✅   P1 release_guard ✅ 已上线
> 架构演进：P2.1 Agent Context Read 🔵 → P2.2 ⬜ → P3 ⬜（机制已拆：Before Action + After Verification + Context Contract）→ P4 ⬜
> P1-1 ~ P1-15 ⬜（P1-15 code_runner 旁线）
> P2 ⬜
> ```
> 
> ---
> 
> *Ziven×GPT #348→#540 共识，2026-09-04 11:28 首版 → 13:46 刷新。*