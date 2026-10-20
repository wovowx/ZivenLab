# 数据库变更日志（Change Log）· 起于 2026-10-20

> **历史层索引**：只记「有业务意义」的结构变更，链接现有治理记录（需求/决策/执行/PR/部署），**不复制第二份事实**。
> **触发**：本日志随 P0 落地随手起；P1 判据（见 database-overview.md）任一满足即进入「日志完整化 + Supabase CLI 版本化迁移」。
> **约定**：每次新增/修改/废弃有业务意义的表或字段，在这里加一条索引（含 提出/决策/实施/验证 状态）。时间轴区分「提出/决策/提交/部署」时间，不知道的标 unknown，不拿一个字段冒充。

---

## 2026-10-20 — 数据库管理规范化（overview v2 + P1 判据）【非结构变更·文档/治理】
- 项目/模块：数据库治理
- 事件：校准 database-overview 到实测 23 表 + 每表字典（purpose/owner/used_by/lifecycle/relationships/source_status）+ 定义 P1 触发判据 + 确认 dump_schema 可用
- 提出：柳柳「想要专门数据库文档 + 规范化 + 网上 idea」→ 与 GPT 有来有回收敛 → 柳柳拍板 P0
- 决策：`governance/database/database-overview.md` v2（ZivenLab PR #66，main fefeffa0）
- 实施：dump_schema 由 `supabase_schema action=schema_dump` 提供（database.js v3，早已实现），实测 23 表快照可用
- 状态：已上线（overview v2 / change-log 起头）

（后续每次表/字段变更在这里追加索引）
