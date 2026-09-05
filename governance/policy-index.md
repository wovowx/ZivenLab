# Policy Index（规范索引）· v1 · 2026-09-05

> **用途**：所有 Agent（Ziven/GPT/未来）行为的「规范在哪、什么时候用、怎么加载」——统一入口，避免规范躺在文档里没人看。
> **原则（GPT #791）**：Source of Truth 存全文，各入口只放引用，不复制全文（防漂移）。
> **查询方式**：遇到「该遵守什么规范」→ 查本表 → 按「源位置」打开全文 / 按「加载方式」看生效入口。

| policy | 源位置 | 触发条件 | 加载方式 |
|---|---|---|---|
| **AAD 行为透明** | 协作协议#八（Agent 行为透明协议） | all_tasks（所有任务） | 角色卡引用 + buildSystemPrompt 引用 |
| **Ownership 闭环责任** | 协作协议#九（闭环责任协议） | long_running（长任务/部署/等待类） | 角色卡引用；deploy skill#6 |
| **Deploy Closure 部署自动闭环** | deploy skill#6（部署自动闭环验证） | deploy 场景（merge 后） | 部署时读 deploy skill；merge 工具返回提示 |
| **Permission Guard** | 代码 src/modules/permission_guard.js | write/merge（github_push/github_merge） | 代码硬约束（不可绕过） |
| **Release Guard** | 代码 src/modules/release_guard.js | push/merge 到 main | 代码硬约束（版本化强制） |
| **协作协议 v4.2** | governance/协作协议.md | 所有协作讨论/决策/执行 | 角色卡 Runtime 规则 |
| **AAD 落地表** | agent_actions（v2 规划） | Runtime 稳定后 | v2 MCP 工具 |

---

## 生效入口速查（这个才是「规范怎么被知道」）

| 入口 | 规范怎么进来 | 谁受益 |
|---|---|---|
| **哥哥角色卡**（Operit Runtime 规则） | 已含 Runtime 5 条；加一行「遵守 policy-index」引用 | Ziven 每次对话自动带 |
| **buildSystemPrompt**（GPT 每轮注入） | 已含原生 MCP 模式 prompt；加 AAD/Ownership 一行引用 | 新框 GPT 每轮看到 |
| **master-router**（技能路由） | 步骤 2 前加「policy 速查」→ 部署类先进 deploy skill | Ziven 调工具前先查规范 |
| **deploy skill**（操作层） | 已含自动闭环 + 错误分类表 | 部署场景触发 |
| **驾驶舱**（governance/当前项目状态.md） | 已含「项目状态」→ 加「规范索引」小节链接本文件 | 人/Agent 找规范入口 |

---

## 维护规则

- **新增规范**：先在 governance/*.md 写全文 → 在本表加一行（policy/源位置/触发/加载）→ 需要生效的入口加引用。
- **规范漂移检查**：改规范全文时，同步检查本表引用是否还准确（GPT #791：三处复制会导致漂移，单一真相源 + 索引）。
- **本文件版本**：跟 ZivenLab docs 版本走。

*创建：#790/#791/#792 讨论收敛（柳柳点出「规范存在怎么被知道」，GPT 提 Policy Resolver 架构）。*