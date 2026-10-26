# Schema Policy（表结构治理规则）· v1.1 · 2026-10-26

> 发布纪律里有 Release Guard，数据库治理也要有硬闸门。**柳柳 2026-09-09 拍板铁律**。

## 铁律（Table Change Guard）

1. **数据源唯一**：整个系统只用一个 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`）。不加第二数据源。

2. **加表/改表必须过现有表**：任何新增/修改表结构前，**必须先打开 `database-overview.md` 过一遍现有表信息**，证明「现有表无法覆盖、不是重复造轮子」，把必要性写清楚，才可以加。

3. **建表工具强制 necessity（治理要求；运行时门禁待验证）**：任何加表/改表提议都必须说明 necessity（必要性说明），这是本项目的治理要求。但截至 2026-10-26，当前可见 `supabase_schema` 工具接口没有暴露 `necessity` 参数，且没有拒绝缺少说明的运行时回归证据；因此不能宣称工具已经实现“不传拒建”或自动列出现有相关表。真正修改 schema 前，仍须逐案确认必要性并取得柳柳明确授权；在硬门禁证据补齐前不得把文档规则当作工具执行拦截。

4. **机器发现漂移（目标机制，自动闭环待验证）**：`supabase_schema action=schema_dump` 可用于读取结构快照；但当前未核实每次变更后自动写入 `schema/generated-schema.md`、生成 diff 并由 CI 监控的闭环，仓库当前也未见该输出目录。未完成工具/CI 核验前，不得把「能导出快照」表述成「自动检测漂移已生效」。

5. **语义人工维护**：表的「为什么存在 / 生命周期 / 关系 / 坑」由人/ Agent 写进 `domains/*.md`，工具不自动生成语义（机器管结构、人管意义）。

6. **建表后同步文档**：建完表，同步更新 overview（加一行）+ domain 文档（写语义）。不更新=不完整变更。

## 流程

```
要加表/改表
  ↓ ① 打开 database-overview.md 过现有表
  ↓ ② 写 necessity（为什么不能复用现有表）
  ↓ ③ 目标工具门禁：校验 necessity 非空 + 列出相关表（当前运行时未证实）
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
- 2026-10-26：v1.1 区分数据结构治理要求与实际工具门禁；确认当前可见工具 schema 无 necessity 参数，自动 snapshot/diff/CI 闭环仍待验证。本次只改文档，未执行 DDL。
