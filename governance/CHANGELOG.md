# ZivenLab CHANGELOG（文档仓 · 知识快照）

> 文档仓不假装软件发行版：版本模型 = 知识快照 `docs-YYYY.MM(.N)`（可带 baseline/snapshot 后缀）。
> 记录：知识演进（新增/决策/归档），不记每个 commit。
> 本文件已迁移至 governance/（2026-09-04 governance 目录重组）。

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