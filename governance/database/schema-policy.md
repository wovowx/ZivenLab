# Schema Policy（表结构治理规则）· v1.3 · 2026-10-26

> 发布纪律里有 Release Guard，数据库治理也要有硬闸门。**柳柳 2026-09-09 拍板铁律**。

## 铁律（Table Change Guard）

1. **数据源唯一**：整个系统只用一个 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`）。不加第二数据源。

2. **加表/改表必须过现有表**：任何新增/修改表结构前，**必须先打开 `database-overview.md` 过一遍现有表信息**，证明「现有表无法覆盖、不是重复造轮子」，把必要性写清楚，才可以加。

3. **所有 DDL 路径都必须核验 necessity（治理要求；Worker dev 已加最小防护，验收未完成）**：任何加表/改表/执行 DDL 都必须提供非空 necessity 并取得柳柳对真实操作的明确授权。经柳柳授权，`mcp-memory/dev/src/tools/database.js` 已把共用的非空 necessity 检查用于 `create_table` 与 `drop_table`；通用 `exec` 若 SQL 含 CREATE/ALTER/DROP/TRUNCATE/GRANT/REVOKE/COMMENT/REINDEX/CLUSTER/VACUUM/DO/CALL/EXECUTE 等关键词，也会在 RPC 前要求 necessity。缺参拒绝会尝试列出现有表。`mcp-memory/dev/src/modules/mcp_router.js` 也已将 `supabase_*` 从无条件前缀放行改为必须命中 skills 注册表，并在 `tools/list` 为已注册的 `supabase_db` 与 `supabase_schema` 都暴露可选 necessity 字段；`supabase_db` 原有 action enum 未扩展，`supabase_schema` 保留注册表原有的 create/drop/tables/exec/schema_dump action。两个注册工具均经 Router 路由至同一 `database.js` handler，Worker dev guard 对两条入口生效。隔离 Mock 已扩展至静态37个 `check(...)` 调用点，但该最新版尚未用 Node 重跑（NOT RE-RUN）；这只是 dev 代码，不是线上门禁已验证。GPT App 当前独立可见的 `supabase_schema` 直接工具接口仍未声明 necessity，是否绕过 Worker Router、其独立执行路径与门禁需单独核验。实际 endpoint/RPC 以及任何真实 DDL 均未测试、未执行；不能仅因源码已改就标记验收完成。

4. **机器发现漂移（目标机制，自动闭环待验证）**：`supabase_schema action=schema_dump` 可用于读取结构快照；但当前未核实每次变更后自动写入 `schema/generated-schema.md`、生成 diff 并由 CI 监控的闭环，仓库当前也未见该输出目录。未完成工具/CI 核验前，不得把「能导出快照」表述成「自动检测漂移已生效」。

5. **语义人工维护**：表的「为什么存在 / 生命周期 / 关系 / 坑」由人/ Agent 写进 `domains/*.md`，工具不自动生成语义（机器管结构、人管意义）。

6. **建表后同步文档**：建完表，同步更新 overview（加一行）+ domain 文档（写语义）。不更新=不完整变更。

## 流程

```
要加表/改表
  ↓ ① 打开 database-overview.md 过现有表
  ↓ ② 写 necessity（为什么不能复用现有表）
  ↓ ③ 验证 DDL 入口 necessity gate（Worker dev 已实现最小修复；隔离回归尚待运行；独立 supabase_schema 工具路径仍待核）
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
- 2026-10-26：v1.3 复核发现注册表中启用的 `supabase_schema` 也经同一 Worker handler，故 `tools/list` 现在同时暴露两个注册工具的 necessity；隔离测试已扩展至37个调用点，最新版本仍 NOT RE-RUN。GPT App 的独立 `supabase_schema` 直接工具接口与真实 RPC/endpoint、自动 snapshot/diff/CI 仍未验证。本轮无真实 DDL、无数据库写入、无部署。
