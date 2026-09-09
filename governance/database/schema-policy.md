# Schema Policy（表结构治理规则）· 2026-09-09

> 发布纪律里有 Release Guard，数据库治理也要有硬闸门。**柳柳 2026-09-09 拍板铁律**。

## 铁律（Table Change Guard）

1. **数据源唯一**：整个系统只用一个 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`）。不加第二数据源。

2. **加表/改表必须过现有表**：任何新增/修改表结构前，**必须先打开 `database-overview.md` 过一遍现有表信息**，证明「现有表无法覆盖、不是重复造轮子」，把必要性写清楚，才可以加。

3. **建表工具强制 necessity**：`supabase_schema` 建表/改表时必须传 `necessity`（必要性说明），不传拒建。工具会在建表前列出相关现有表，强制「过一遍」。

4. **机器发现漂移**：每次 schema 变更后自动生成 `schema/generated-schema.md` 快照 + diff（工具做，不靠记性）。结构变化一定被发现。

5. **语义人工维护**：表的「为什么存在 / 生命周期 / 关系 / 坑」由人/ Agent 写进 `domains/*.md`，工具不自动生成语义（机器管结构、人管意义）。

6. **建表后同步文档**：建完表，同步更新 overview（加一行）+ domain 文档（写语义）。不更新=不完整变更。

## 流程

```
要加表/改表
  ↓ ① 打开 database-overview.md 过现有表
  ↓ ② 写 necessity（为什么不能复用现有表）
  ↓ ③ 工具校验 necessity 非空 + 列出相关表
  ↓ ④ 建表/改表
  ↓ ⑤ 自动生成 schema snapshot + diff
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
- 2026-09-09：v1 初版（柳柳拍板 Table Change Guard）
