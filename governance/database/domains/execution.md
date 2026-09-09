# Execution 域数据模型 · 2026-09-09

> 执行 GPT 流水线：会话、run、绑定、绑定事件。
> 核心：把「GPT 独立框」变成可管理、可审计、可复用的执行资源。
> 2026-09-09 更新：conversation_bindings 增加健康字段（M1.3，柳柳+GPT 讨论定稿）

## 表清单

| 表 | 角色 |
|---|---|
| execution | 执行会话主表 |
| execution_runs | 每次执行 run |
| conversation_bindings | GPT 会话↔线程绑定 |
| conversation_binding_events | 绑定变更审计 |

## execution（会话主表）
⚠️ 空表，结构待补（无 DDL 存档，execution_session_manager.js 里没有 CREATE TABLE）。

**语义**（从代码推断）：
- 一行 = 一个「执行会话」（GPT 独立框实例）
- 生命周期：init → rotate（释放旧会话）→ status → task
- 与 execution_runs 1→N
- 与 conversation_bindings 绑定（一个执行会话对应一个 GPT conversation）

## execution_runs（执行 run）
**用途**：一次具体任务的派发与结果。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| execution_session_id | uuid FK | 所属会话 |
| agent_id | text | 执行 agent（gpt-exec） |
| thread_id | text | 执行线程 |
| task_type | text | verify/… |
| status | text | completed/… |
| task_desc | text | 任务描述 |
| created_at / started_at / finished_at | timestamptz | 生命周期 |
| result | jsonb | 任务结果 |

## conversation_bindings（绑定）
**用途**：把 GPT conversation_id 绑到线程，实现「执行框即线程」的路由。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| conversation_id | uuid | GPT 会话 |
| agent_id | text | 绑定 agent |
| thread_id | text | 绑定线程 |
| purpose | text | execution/… |
| access_mode | text | exclusive/… |
| route_type | text | temporary/… |
| status | text | active/archived/…（生命周期） |
| health | text | unknown/healthy/stale/failed（健康，正交于 status） |
| last_checked_at | timestamptz | 最近检查时间 |
| last_success_at | timestamptz | 最近真实成功调用 |
| last_failure_at | timestamptz | 最近失败时间 |
| check_count | integer | 累计检查次数 |
| source | text | 创建来源 |
| metadata | jsonb | reason/created_by/switch_candidate/switch_reason… |
| created_at / archived_at / updated_at | timestamptz | |

**坑**：status=archived 表示已释放；access_mode=exclusive 表示专用。
**健康语义（M1.3 · 2026-09-09 柳柳+GPT 定稿）**：
- status（生命周期）与 health（健康）**正交**：active+failed = 当前绑定但已失效等待替换；archived+healthy = 历史绑定曾正常
- bind 时 health=unknown（绑定≠可用）；第一次真实成功调用 → healthy
- 失败（401/403/429）→ failed + metadata.switch_candidate=true + switch_reason（下次换档，不在 error path 自动换）
- 查询无副作用：健康只由 runtime 真实调用（init/rotate/dispatch）更新，getActive 纯读取

## conversation_binding_events（绑定审计）
**用途**：记录绑定变更（轮换/释放）的完整历史。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| agent_id | text | |
| thread_id | text | |
| old_conversation_id | uuid | 旧 |
| new_conversation_id | uuid | 新 |
| reason | text | 变更原因（生命周期: created/switched/archived/migration；健康: health_success/health_failed/health_stale） |
| created_at | timestamptz | |

## 典型流程
1. init：建执行会话 → 创建 execution → 绑定 conversation（conversation_bindings）
2. 派发任务：INSERT execution_runs（task_type/desc/status=running）
3. 完成：更新 status=completed + result
4. 轮换：archive 旧绑定 → 建新绑定 → 记 conversation_binding_events

## 变更记录
- 2026-09-09 v2：conversation_bindings 加 5 健康字段（health/last_checked_at/last_success_at/last_failure_at/check_count）+ execution_session_manager v6.32.14 健康观测
- 2026-09-09：v1（execution 空表结构待补，其余 2026-09-09 实测）
