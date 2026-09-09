# Chatroom 域数据模型 · 2026-09-09

> 聊天室运行时：多 Agent 协作的「对话空间」——线程、消息、事件、上下文。
> 这是 Common Ground（聊天室）+ 上下文 Worker 的核心数据域。

## 表清单

| 表 | 角色 | 关系 |
|---|---|---|
| chat_threads | 线程主表（项目/话题） | 1→N messages |
| chat_messages | 消息本体 | N→1 thread |
| chat_agent_events | Agent 动作事件 | 1 message → N events |
| thread_members | 线程成员 | N→N thread↔actor |
| thread_contexts | 线程上下文快照 | 1 thread → N versions |
| agent_chat_state | Agent 消费游标 | 1 (agent,thread) 一条 |
| thread_message_counter | 消息序号 | 1 thread 一条 |

## chat_threads（线程）
**用途**：Common Ground 的「项目/话题」容器。每条消息归属于一个线程。

| 列 | 类型 | 含义 |
|---|---|---|
| thread_id | uuid PK | 线程 id |
| title | text | 标题 |
| creator / created_by | text | 创建者 |
| status | text | active/archived… |
| thread_type | text | project/… |
| thread_number | int | 展示序号 |
| metadata | jsonb | 扩展 |
| is_pinned | bool | 置顶 |
| created_at / updated_at | timestamptz | 时间戳 |

**坑**：thread_number 是全局递增（非每线程），靠 counter 表保障。

## chat_messages（消息）
**用途**：多 Agent 文本消息 + 元数据（提及、工具调用、版本）。事实层。

| 列 | 类型 | 含义 |
|---|---|---|
| message_id | uuid PK | |
| thread_id | uuid FK | 所属线程 |
| author | text | ziven/gpt/… |
| content | text | 正文 |
| reply_to | uuid | 回复目标 |
| mentions | jsonb | @提及数组 |
| message_number | int | 线程内序号 |
| actor_id | uuid FK | 作者身份 |
| message_type | text | text/… |
| metadata | jsonb | |
| version | int | 编辑版本 |
| edited_at / deleted_at | timestamptz | 软删 |
| tool_calls | jsonb | 工具调用记录 |

**坑**：content 可能很长；tool_calls 是 JSON 数组不是列。

## chat_agent_events（事件）
**用途**：Agent 对消息的「动作事件」（claim/已读/投递/状态），事件驱动核心。

| 列 | 类型 | 含义 |
|---|---|---|
| event_id | uuid PK | |
| message_id | uuid FK | 关联消息 |
| agent | text | 目标 agent |
| status | text | success/… |
| payload | jsonb | event_type/content_preview… |
| claimed_at | timestamptz | 被认领 |
| delivery_status | text | created/claimed/… |
| retry_count | int | 重试 |
| dead_letter | bool | 死信 |
| claimed_by | text | |
| z_probe | jsonb | 预留 |
| created_at / updated_at | timestamptz | |

## thread_contexts（上下文快照）
**用途**：Context Worker 生成的线程上下文（摘要/稳定事实/决策），版本化不覆盖。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| thread_id | uuid FK | |
| version | int | 版本 |
| summary | text | 摘要 |
| stable_facts | jsonb | 稳定事实 |
| decisions | jsonb | 决策 |
| open_questions | jsonb | 未决 |
| next_actions | jsonb | 下一步 |
| recent_context | jsonb | 近期上下文 |
| generated_by | text | 生成者 |
| created_at | timestamptz | |

## agent_chat_state（消费游标）
**用途**：每个 Agent 在每个线程的「读到哪里」——防重复消费。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| agent_id | text | |
| thread_id | uuid FK | |
| last_consumed_message_id | uuid | 已消费 |
| last_trigger_event_id | uuid | 触发 |
| last_seen_at / updated_at | timestamptz | |

## thread_message_counter（序号）
| 列 | 类型 | 含义 |
|---|---|---|
| thread_id | uuid PK | |
| last_number | int | 当前最大序号 |

## thread_members
⚠️ 空表，结构待补（无 DDL 存档）。

## 典型流程
1. Agent 发消息 → INSERT chat_messages（message_number = counter+1）
2. 事件驱动 → INSERT chat_agent_events（对目标 agent）
3. Agent 收到 → claim event → 读消息 → 处理 → 更新 agent_chat_state
4. Context Worker → 定期生成 thread_contexts（版本化）

## 变更记录
- 2026-09-09：v1（基于 2026-09-09 实测结构）
