# Collaboration 域数据模型 · 2026-09-09

> 协作治理：决策链 + 讨论证据。这是「系统为什么这样走」的事实层。
> 与 release_guard 同思想：让「讨论必须有痕迹、改变必须带决策」成为硬约束。

## 表清单

| 表 | 角色 |
|---|---|
| decision | 决策记录 |
| discussion_evidence | 讨论证据链 |

## decision（决策）
**用途**：一个「改变系统未来行为的执行」必须带 confirmed 决策才能放行。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| decision_id | uuid | 决策业务 id |
| discussion_id | uuid | 关联讨论 |
| approved_by | text | 批准人（柳柳/…） |
| status | text | confirmed/… |
| created_at | timestamptz | |

**坑**：guard 只查 status==confirmed，不判质量。

## discussion_evidence（讨论证据）
**用途**：记录一场讨论的完整证据链（初始立场/挑战/变更/收敛）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| discussion_id | uuid | |
| related_action | text | 关联动作 |
| source_thread_id | text | 来源线程 |
| participants | text | 参与者 |
| proposal_summary | text | 提案摘要 |
| initial_position | text | 初始立场 |
| challenge_points | text | 挑战点 |
| changes_made | text | 变更过程 |
| final_proposal | text | 收敛提案 |
| created_at | timestamptz | |

## 典型流程
1. 讨论 → 在 thread 里发生 → 记录 discussion_evidence（六要素）
2. 收敛 → 柳柳拍板 → INSERT decision（status=confirmed）
3. 执行 guard → 查 decision.status==confirmed → 放行

## 变更记录
- 2026-09-09：v1（2026-09-09 实测）
