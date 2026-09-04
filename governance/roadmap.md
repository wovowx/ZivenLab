# 行动路线图（Roadmap · 原85号行动总清单）

> **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：本文件 = 当前做什么 / 做到哪的唯一路线源。
> 每完成一项 → 更新本清单 → 不许另起炉灶。
> 协作纪律：先讨论出方案 → 再分工执行（柳柳拍板）。详见 governance/协作协议.md。
> ⚠️ 原文件名 85_行动总清单.md 已迁移至此（governance/roadmap.md），旧位置保留 redirect。
>
> **推进前必读（2026-09-04 柳柳抓出 + GPT #540）**：开工前读本文件 + 驾驶舱，完成验证后更新两者。别再靠对话上下文推进。

---

## ✅ 已完成

- P0-1 自触发修复：PR #91（mcp-memory）✅
- 前端 Bug A 实时轮询：PR #92 ✅
- 前端 Bug B 布局修复：PR #93 ✅
- 角色卡四改（公共区身份规则入卡）：✅ 双端同步
- **P0-5 当前项目状态地图**：PR #1 ✅
- **P0-4 场景入口导航**：PR #2 ✅
- **P0-6 资产盘点**（①代码审计②资产清单③生命周期模型④生产入口唯一性）：PR #1~#4 + v6 ✅
- **P0-3 历史异常基线建立**：4 条脏事件，留作回归样本 ✅
- **协作协议 v4.2**（讨论与分工规则 + 协议部署原则 + 铁律6）：PR #6 ✅
- **Runtime 5 条入卡 + GPT 提示词同步**：✅ 双端部署完成
- **P0-2 Phase1 事件可靠基础设施**：watchdog 释放历史 stuck claim ✅ / delivery_status 状态机 ✅ / claim 责任绑定 ✅ / GPT 链回归 ✅ / agent 隔离 ✅ / dead_letter（🟡 逻辑待触发）——GPT #502 确认 completed
- **发布纪律 Release Discipline**（deploy skill 双仓版本化 + CHANGELOG）：✅ 方案已定（GPT #506~508）
- **governance/ 目录重组**：✅ 权威文档与历史分层（柳柳拍板 2026-09-04）
- **P1 release_guard 硬闸门上线（v6.10.1）**：✅ 入口层接入 index.js + process 防御，**真实拦截验证通过**（不带版本号 push main → `⛔ RELEASE_GUARD: push_to_main_blocked`）；v6.10.2 发布纪律修正（rebase 防标题重复）

---

## 🔵 P0（进行中）

### P0-2 Phase2 Ziven 消费链（Wake Bridge 改造）
- 状态：⬜ 待讨论方案（Phase1 已完成，基础设施不再吞消息）
- Phase2 讨论议题（GPT #502）：
  1. Ziven consumer 所有权模型
  2. Wake Bridge 在哪个状态 claim（不允许发现即 claim）
  3. 注入当前框失败怎么办
  4. delivered vs seen/read 的区别
- 完成标准：ziven 事件 created→claimed→delivering→delivered→processing→acked 全链路闭环
- 回归样本：保留的 4 条 ziven 事件（已释放 created/retry=1，不手动消费）

---

## 🏗️ 架构演进（柳柳 2026-09-04 拍板 · Agent Operating System 蓝图）

> 核心：从「会记事的 Agent」→「不需要靠记性的 Runtime」。知识≠生效，没进 Runtime 生效路径 = 不存在。
> **2026-09-04 增补（GPT #540）**：Agent 最大的问题不是没有知识，而是在正确时间没有加载正确知识。
> 详见 governance/当前项目状态.md（架构蓝图）。

| 阶段 | 做什么 | 解决 | 状态 |
|---|---|---|---|
| **P1** | release_guard（第一个 Runtime Guard 样板） | 想不起来版本号 | ✅ 已上线 v6.10.1，真实拦截验证通过 |
| **P2.1** | Agent Context Read Capability（GPT #540 改名：核心是「知道自己现在在哪」） | Agent 决策前拿不到正确依据 | 🔵 方向已定（GPT #536/#538/#540），待落地 |
| **P2.2** | Permission Model（L0-L3 分级） | 谁能读/改/发布 | ⬜ |
| **P3** | Workspace State Runtime（Before Action 必读 + After Verification 必更 + Context Contract 最小必要上下文） | 换窗口失忆 / 文档找不到 / 推进没绑定状态 | 🔵 2026-09-04 柳柳问题验证必要性，GPT #540 拆机制 |
| **P4** | Patch Engine（GPT 提 PR 你合） | GPT 参与改代码 | ⬜ |

### Context Contract（按任务类型加载最小必要上下文 · GPT #540）

| 任务类型 | 必须加载 |
|---|---|
| 项目推进 | workspace_state + roadmap + 最近 decision |
| 改代码 | workspace_state + 相关 skill + 代码文件 + 最近变更 |
| 发布 | release_policy + changelog + 版本状态 |
| 记忆/情感 | 相关 skill + 记忆上下文 |

**两个闭环（P3 核心）**：
- **Before Action**：做项目推进前，必须加载当前状态（roadmap + 驾驶舱）
- **After Verification**：完成验证后，必须更新当前状态（同一文件，不许另起炉灶）

---

## P1（稳定化）

- P1-1 协作协议固化：v4.2 confirmed；待补 decision_confirmed 五字段成立条件 + 规则同步机制（source_version vs runtime_version）
- P1-2 Error Log + Regression 链（含「工具语义误判：github_push 是 replace 非 patch」记录）
- P1-3 GPT MCP Bridge（拆三段）
- P1-4 需求文档终稿（76/77/81/00a 对齐）
- P1-5 轮询可观测性（GPT #383）
- P1-6 visualViewport 方案（GPT #385）
- P1-7 wake bridge 升级 webhook/ntfy + API 版 Ziven（GPT #395）
- P1-8 状态地图/导航/资产优化：事件流视图 / 事实状态字段 / 负责人拆协作方 / 导航表依据字段 / 资产表验证依据字段
- P1-9 decision 索引（GPT #416）
- P1-10 历史讨论归档（GPT #416）
- P1-11 驾驶舱第9章事件流细化（GPT #440）
- P1-12 workspace_rules 三方公共规则层（GPT #468/#470）
- P1-13 常驻层部署（GPT #468/#470）——advancedCustomPrompt + GPT 提示词已先落地 Runtime 5 条
- P1-14 破坏性操作分级（GPT #484：写入 低/中/高 风险）
- P1-15 code_runner 卡死排查（柳柳反馈好用但会卡，纳入 Runtime 技术项）

---

## P2（整理与自动化）

- P2-1 Memory 整理（先定规则再清）
- P2-2 Skill Router 强化（长期核心）
- P2-3 skill 目录命名规范迁移（alias 方式）

---

## 补漏

- 决策层 Decision Log（含 decision_id 反查）
- 真相源可信度模型：柳柳决策 > 运行事实 > GitHub文档 > 状态索引 > Memory > 推断
- **文档引用同步纪律（2026-09-04 柳柳抓出）**：文件迁移/改名后，全文 grep 旧引用一起改，不留死链

---

## 当前待发批次（dev · 攒批不频繁部署 · 柳柳 2026-09-04）

- deploy skill v6.4.3 命名纪律（推 dev 消息用 vX.Y.Z: 名称）——待作正式 release 练习（GPT #536）
- chat.html v2.6.0 移动端输入框布局修复（flex 竖排）——GPT #538 建议按 hotfix 处理，待柳柳拍板

---

## 总执行顺序

```
P0 全清 ✅   P1 release_guard ✅ 已上线
架构演进：P2.1 Agent Context Read 🔵 → P2.2 ⬜ → P3 ⬜（机制已拆：Before Action + After Verification + Context Contract）→ P4 ⬜
P1-1 ~ P1-15 ⬜（P1-15 code_runner 旁线）
P2 ⬜
```

---

*Ziven×GPT #348→#540 共识，2026-09-04 11:28 首版 → 13:46 刷新。*