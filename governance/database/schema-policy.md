# Schema Policy（表结构治理规则）· v1.1 · 2026-10-26

> 发布纪律里有 Release Guard，数据库治理也要有硬闸门。**柳柳 2026-09-09 拍板铁律**。

## 铁律（Table Change Guard）

1. **数据源唯一**：整个系统只用一个 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`）。不加第二数据源。

2. **加表/改表必须过现有表**：任何新增/修改表结构前，**必须先打开 `database-overview.md` 过一遍现有表信息**，证明「现有表无法覆盖、不是重复造轮子」，把必要性写清楚，才可以加。

3. **所有 DDL 路径都必须核验 necessity（治理要求；当前只部分实现）**：任何加表/改表/执行 DDL 都必须说明 necessity 并取得柳柳明确授权。静态源码确认 `src/tools/database.js` 的 `create_table` 分支会检查 `safeArgs.necessity`，缺失时返回 `TABLE_CHANGE_GUARD_REQUIRED` 并尝试列出现有表；但 `drop_table` 与通用 `exec` 分支未在 handler 内检查 necessity。实时 `supabase_db` 注册 schema 仅暴露 `query/insert/update/delete/tables/exec` action，未暴露 `create_table/drop_table/schema_dump`；Router 对 `supabase_*` 前缀直接视为已知且 schema 缺失兼容放行，所以未注册的 `supabase_*` 名称可能到达 handler 而不受专属 schema 约束。当前外露 `supabase_schema` 工具签名也没有 `necessity` 参数。由于没有执行真实 endpoint/RPC 行为测试，实际 DDL 是否最终会被 Supabase RPC 权限拒绝仍未知；不能把 create_table 的局部检查表述为全通路硬门禁。任何 DDL 都先停下，待差距矩阵 P1 闸门完成隔离回归和最小修复，并获明确授权后再执行。

4. **机器发现漂移（目标机制，自动闭环待验证）**：`supabase_schema action=schema_dump` 可用于读取结构快照；但当前未核实每次变更后自动写入 `schema/generated-schema.md`、生成 diff 并由 CI 监控的闭环，仓库当前也未见该输出目录。未完成工具/CI 核验前，不得把「能导出快照」表述成「自动检测漂移已生效」。

5. **语义人工维护**：表的「为什么存在 / 生命周期 / 关系 / 坑」由人/ Agent 写进 `domains/*.md`，工具不自动生成语义（机器管结构、人管意义）。

6. **建表后同步文档**：建完表，同步更新 overview（加一行）+ domain 文档（写语义）。不更新=不完整变更。

## 流程

```
要加表/改表
  ↓ ① 打开 database-overview.md 过现有表
  ↓ ② 写 necessity（为什么不能复用现有表）
  ↓ ③ 验证所有 DDL 入口均检查 necessity（当前仅 create_table 分支有源码检查，完整链路未验证）
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
- 2026-10-26：v1.1 区分数据结构治理要求与实际工具门禁；静态复核确认 create_table 有局部 necessity 检查，但 drop_table/exec 分支与 `supabase_*` 前缀+缺 schema 兼容路由存在潜在绕行；外露工具签名无 necessity 参数，真实 RPC/endpoint 行为未验证。自动 snapshot/diff/CI 闭环仍待验证。本次只改文档，未执行 DDL。
