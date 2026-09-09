# ZivenLab CHANGELOG（文档仓 · 知识快照）

> 文档仓不假装软件发行版：版本模型 = 知识快照 `docs-YYYY.MM(.N)`（可带 baseline/snapshot 后缀）。
> 记录：知识演进（新增/决策/归档），不记每个 commit。
> 本文件已迁移至 governance/（2026-09-04 governance 目录重组）。

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