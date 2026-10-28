# Schema Policy（表结构治理规则）· v1.9 · 2026-10-28

> 发布纪律里有 Release Guard，数据库治理也要有硬闸门。**柳柳 2026-09-09 拍板铁律**。

## 铁律（Table Change Guard）

1. **数据源唯一**：整个系统只用一个 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`）。不加第二数据源。

2. **加表/改表必须过现有表**：任何新增/修改表结构前，**必须先打开 `database-overview.md` 过一遍现有表信息**，证明「现有表无法覆盖、不是重复造轮子」，把必要性写清楚，才可以加。

3. **所有 DDL 路径都必须核验 necessity（治理要求；Worker dev 已加最小防护，完整隔离回归已通过；真实 RPC/endpoint 权限未验收）**：任何加表/改表/执行 DDL 都必须提供非空 necessity 并取得柳柳对真实操作的明确授权。经柳柳授权，`mcp-memory/dev/src/tools/database.js` 已把共用的非空 necessity 检查用于 `create_table` 与 `drop_table`；通用 `exec` 若 SQL 含 CREATE/ALTER/DROP/TRUNCATE/GRANT/REVOKE/COMMENT/REINDEX/CLUSTER/VACUUM/DO/CALL/EXECUTE/IMPORT/SECURITY 等关键词，也会在 RPC 前要求 necessity。中间版本的隔离 Mock 曾扩展至44个 check 调用点，并在 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 通过44/44（历史证据）；SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 的69项 Router/DDL parser 与20项 search_history 是历史完整回归证据；当前最新完整回归绑定 mcp-memory/dev SHA `fcd12b1e55f6a7119addb27647e6d2692773a8cf`，`npm run check` exit 0、webhook104/104、`npm run test:contracts` 122/122、search_history20/20、release_guard15/15。最新回归仍全程使用 mock/本地，不代表真实 RPC/endpoint/DB 权限或 DDL 已验收。缺参拒绝会尝试列出现有表。`mcp-memory/dev/src/modules/mcp_router.js` 也已将 `supabase_*` 从无条件前缀放行改为必须命中 skills 注册表，并在 `tools/list` 为已注册的 `supabase_db` 与 `supabase_schema` 都暴露可选 necessity 字段；`supabase_db` 原有 action enum 未扩展，`supabase_schema` 保留注册表原有的 create/drop/tables/exec/schema_dump action。两个注册工具均经 Router 路由至同一 `database.js` handler，Worker dev guard 对两条入口生效。隔离 Mock 的44项版本与 `/tmp/ops-ev2`、SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 的44/44结果属于中间历史证据；当前完整回归已在后续 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 通过。这只是 dev 代码和隔离 Mock 证据，不代表线上门禁或真实 RPC 权限已验证。该 necessity 机制仍只是非空门槛，不是执行授权。2026-10-27 静态审计确认 create_table/drop_table 曾将未经语法校验的 table/columns 拼入 SQL；当前已按兼容优先的受限语法方案，在 mcp-memory/dev 的 database.js 增加标识符校验与列定义解析，并从解析结构重新生成 SQL，不再把原始 columns 片段拼入 CREATE TABLE。现有工具参数形状保持不变；列定义首期支持白名单类型、有限约束与安全默认值，未支持语法明确拒绝。tests/router_registry_contract_test.mjs 已增加隔离 Mock 用例，覆盖合法类型/默认值/RLS、非法表名、注释/分号/未闭合语法/未支持语法/重复列名与拒绝路径零 RPC。**当前完整隔离回归已由 Operit 于2026-10-27在 detached worktree `/tmp/ops-ev3` 对精确 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 实际运行通过：`npm run check` exit 0、webhook 104/104、Router registry + DDL parser 69/69、search_history 20/20；Node v24.18.0/npm 11.16.0，stderr 空、worktree clean、原工作树未动。GPT 另外在隔离 V8 + fetch mock 对回读的 database.js 做了28/28定向 smoke。两类证据均不代表真实数据库/RPC/DDL验收。全部测试仅使用 mock，无真实 Supabase/MCP endpoint、真实 SQL/DDL、数据库写入或 schema/registry/config 变化；未部署、E3 NOT RUN、main UNCHANGED。** 通用 exec 仍把原始 SQL 交给 exec_sql，语句数量/执行权限尚未核验；当前仓库静态范围未找到 exec_sql RPC 定义/授权目录。2026-10-27 曾向该 RPC 发送一条只读 catalog SELECT，真实端点返回 HTTP 400/P0001 `Only DDL allowed (exec_sql is restricted)`；因此经此 RPC 的只读目录核查被拒，且没有得到函数定义或权限数据。此结果不证明该 RPC 对所有 DDL 的安全策略，也不能代替实际函数源码和授权目录；真实 DDL 多语句行为与 exploitability 仍未知。GPT App 的独立 supabase_schema 入口是否经过 Worker Router 也仍未知。解析器实现与隔离回归批次只改 dev 源码/测试，全程 mock 且未触达真实 RPC/DDL。随后为生命周期设计做了一次独立的只读 catalog SELECT 尝试，真实 exec_sql 返回 HTTP400/P0001「Only DDL allowed」，未获得 catalog 数据；未提交 DDL、未写数据库/注册表/配置。没有部署或合并 main。详见 架构差距矩阵.md。GPT App 当前独立可见的 `supabase_schema` 直接工具接口仍未声明 necessity，是否绕过 Worker Router、其独立执行路径与门禁需单独核验。后续只读排查发现：`supabase_db` 的 REST query 对 `information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 均返回 HTTP 404/PGRST205（未通过当前 public PostgREST schema cache 暴露）；源码中 `schema_dump` 只解析 `/rest/v1/` 的 OpenAPI `definitions`。已检查 `wovowx/mcp-memory/dev/migrations` 目前只有 `20260902_add_chat_agent_events_claimed_at.sql`，未找到 memory_events trigger/function migration；这不等于证明真实 DB 无触发器。当前可见 MCP 没有独立只读 catalog 工具，因此触发器/RLS/GRANT/唯一约束/ON DELETE/function ACL 仍需获准的外部只读数据库通道核验。实际 endpoint/RPC 权限与任何真实 DDL 均未验证/执行；不能仅因代码已改就标记验收完成。

4. **机器发现漂移（目标机制，自动闭环待验证）**：`supabase_schema action=schema_dump` 可用于读取结构快照；但当前未核实每次变更后自动写入 `schema/generated-schema.md`、生成 diff 并由 CI 监控的闭环，仓库当前也未见该输出目录。未完成工具/CI 核验前，不得把「能导出快照」表述成「自动检测漂移已生效」。

5. **语义人工维护**：表的「为什么存在 / 生命周期 / 关系 / 坑」由人/ Agent 写进 `domains/*.md`，工具不自动生成语义（机器管结构、人管意义）。

6. **建表后同步文档**：建完表，同步更新 overview（加一行）+ domain 文档（写语义）。不更新=不完整变更。

## 流程

```
要加表/改表
  ↓ ① 打开 database-overview.md 过现有表
  ↓ ② 写 necessity（为什么不能复用现有表）
  ↓ ③ 验证 DDL 入口 necessity gate（Worker dev 当前完整隔离回归 Router+DDL parser 69/69；独立 GPT App supabase_schema 工具路径、真实 endpoint/RPC 权限仍待核）
  ↓ ④ 经明确授权后建表/改表
  ↓ ⑤ 目标自动化：生成 schema snapshot + diff（当前闭环未验证）
  ↓ ⑥ 更新 overview + domain 文档
  ↓ ⑦ 完成
```

## 分工（双仓）

| 层 | 位置 | 内容 | 谁维护 |
|---|---|---|---|
| 文档 | ZivenLab/governance/database/ | overview + domains/ + schema-policy | 人/Agent 人工 |
| 脚本 | mcp-memory/src/modules/supabase_schema/ | dump/diff/validate | 代码仓工具 |
| 事实 | Supabase | 真实表结构 | 数据库本身 |

## 变更记录
- 2026-09-09：v1 初版（柳柳拍板 Table Change Guard）。
- 2026-10-26：v1.1 区分治理要求与实际工具门禁，记录 create_table 局部检查和 drop_table/exec/前缀路由缺口。
- 2026-10-26：v1.2 记录柳柳授权后的 Worker dev 最小修复（create/drop/exec DDL necessity gate、Supabase 前缀注册校验、公开 necessity 参数），当时隔离 Mock 尚未运行。
- 2026-10-26：v1.3 复核发现注册表中启用的 `supabase_schema` 也经同一 Worker handler，故 `tools/list` 同时暴露两个注册工具的 necessity。
- 2026-10-27：v1.4 记录 create_patch_proposal schema/usage_count 与 IMPORT/SECURITY DDL 关键词测试随同更新后的隔离回归已由 Operit 在 SHA `c4ef21814fb6c0a5c9b06fed9295cac9d5bc975c` 通过44/44；E1 exit 0、webhook 104/104。GPT App 的独立 `supabase_schema` 直接工具接口与真实 RPC/endpoint、自动 snapshot/diff/CI 仍未验证。本轮无真实 DDL、无数据库写入、无部署。
- 2026-10-27：v1.5 完成 table/columns/原始 exec 的静态输入边界审计，确认缺少语法/标识符/语句数量校验；真实可利用性和 exec_sql RPC 权限、多语句行为未验证。
- 2026-10-27：v1.6 按受限语法方案，在 mcp-memory/dev 为 create_table/drop_table 实现标识符校验与列定义解析，并扩展隔离 Router Mock；保持 exec 原始 SQL 通路为独立未解决风险。
- 2026-10-27：v1.7 记录通过现有 exec_sql 请求执行 catalog-only SELECT 被真实端点以 HTTP400/P0001「Only DDL allowed (exec_sql is restricted)」拒绝；未执行 DDL或数据库写入。Operit 已在 detached worktree `/tmp/ops-ev3` 对 SHA `d41d6cdfa8d4ef1e70e59c047f0a33c7f010ca8a` 实跑完整回归：npm run check exit 0、webhook 104/104、Router/DDL 69/69、search_history 20/20；stderr 空、worktree clean，原工作树未动。全程 mock，不触达真实 RPC/DDL/DB，无 schema/registry/config 变更；未部署、E3 NOT RUN、main UNCHANGED。
- 2026-10-27：v1.8 追加现有只读 REST query 能力核查：`information_schema.triggers`、`pg_catalog.pg_trigger`、`pg_indexes` 均以 PGRST205 返回“未在当前 schema cache 找到”；`schema_dump` 源码只读取 PostgREST OpenAPI definitions；当前已检查 migrations 目录未见 memory lifecycle trigger/function migration。结论仅为当前暴露工具与仓库证据不足，不将其扩大为“真实 DB 不存在触发器”；需要独立获准的只读数据库通道才能完成实况核验。未做 DB 写入/DDL、未部署、未合并 main。
