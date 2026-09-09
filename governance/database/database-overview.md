# 数据库总览（Database Overview）· 2026-09-09

> **数据源唯一**：所有表都在 Supabase（`shxfosnnaoxzscrhvkat.supabase.co`），承载 mcp-memory Worker。不搞多库、不另起数据源。
>
> **本文件是「过一遍现有表信息」的依据**（Table Change Guard）：要加表/改表前，先看这里现有表能否覆盖，证明必要性才可动。
>
> 表结构机器快照见 `schema/generated-schema.md`（自动生成）；各域语义见 `domains/*.md`。

## 一图流（21 张表 × 5 域）

| 表名 | Domain | Owner | used_by | 一句话用途 |
|---|---|---|---|---|
| chat_threads | chatroom | chatroom | 聊天室/上下文 | 聊天线程（项目/话题） |
| chat_messages | chatroom | chatroom | 聊天室/执行框 | 消息本体（多 Agent 文本+元数据） |
| chat_agent_events | chatroom | chatroom | 聊天室/事件驱动 | Agent 动作事件（claim/状态/投递） |
| thread_members | chatroom | chatroom | 聊天室 | 线程成员 |
| thread_contexts | chatroom | chatroom | 上下文 Worker | 线程上下文快照 |
| agent_chat_state | chatroom | chatroom | 聊天室 | 各 Agent 消费游标 |
| thread_message_counter | chatroom | chatroom | 聊天室 | 线程消息序号计数器 |
| execution | execution | execution | 执行 GPT | 执行会话主表 |
| execution_runs | execution | execution | 执行 GPT | 每次执行 run |
| conversation_bindings | execution | execution | 执行框/路由 | GPT 会话↔线程绑定 |
| conversation_binding_events | execution | execution | 执行框 | 绑定变更审计 |
| memories | memory | memory | 记忆/上下文 | 记忆条目 |
| files | memory | memory | 记忆/媒体 | 上传文件元数据 |
| knowledge | memory | memory | 记忆 | （待确认废弃） |
| decision | collaboration | decision workflow | 主链路 | 决策记录 |
| discussion_evidence | collaboration | collaboration | 讨论治理 | 讨论证据链 |
| actors | platform | platform | 全系统 | Agent 身份注册 |
| skills | platform | platform | 全系统 | MCP 技能注册 |
| tool_policies | platform | permission | 权限系统 | 工具权限策略 |
| system_config | platform | platform | 配置系统 | 系统 KV 配置 |
| chat_webhook_audit | platform | platform | webhook | webhook 投递审计 |

## 待办
- [ ] execution / thread_members 表结构待补（空表，无 DDL 存档）
- [ ] knowledge 疑似废弃，确认后移除
- [ ] 补全字段约束索引（等 dump_schema.js 上线）

## 变更记录
- 2026-09-09：v1 初版（柳柳拍板数据库治理 v1）
