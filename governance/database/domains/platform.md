# Platform 域数据模型 · 2026-09-09

> 平台配置：系统运行需要什么（身份、技能、权限、配置、审计）。
> 区别于业务域——platform 是「系统能力配置」，不是业务数据。

## 表清单

| 表 | 角色 |
|---|---|
| actors | Agent 身份 |
| skills | MCP 技能注册 |
| tool_policies | 工具权限 |
| system_config | KV 配置 |
| chat_webhook_audit | webhook 审计 |

## actors（身份）
**用途**：Agent 身份注册（ziven/gpt/gpt-exec/…）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | 特殊 id（如 0000…0002=gpt） |
| actor_type | text | system/agent/… |
| name | text | 名称 |
| metadata | jsonb | |
| created_at / updated_at | timestamptz | |

## skills（技能）
**用途**：MCP 技能注册表（供 LLM 选择工具）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| name | text | 技能名 |
| description | text | 描述 |
| input_schema | jsonb | 参数 schema |
| handler_type / handler_config | 文本/json | 处理器 |
| category / tags | 文本/json | 分类/标签 |
| enabled | bool | 启用 |
| created_by / file_path | 文本 | 来源 |
| usage_count / last_used | int/timestamptz | 使用统计 |
| created_at / updated_at | timestamptz | |

## tool_policies（权限策略）
**用途**：工具权限策略（risk_level/是否需审批/是否执行会话）。

| 列 | 类型 | 含义 |
|---|---|---|
| tool_name | text | 工具 |
| risk_level | text | low/high |
| require_session_purpose | bool | 需执行会话 |
| require_approval | bool | 需审批 |
| require_template | bool | 需模板 |
| enabled | bool | |
| description | text | |
| created_at | timestamptz | |

## system_config（KV 配置）
| 列 | 类型 | 含义 |
|---|---|---|
| key | text PK | 配置键 |
| value | text | 配置值 |
| updated_at | timestamptz | |

## chat_webhook_audit（webhook 审计）
**用途**：webhook 投递审计（谁投递/什么决定/理由）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | int PK | |
| event_id | text | |
| agent | text | |
| decision | text | delivered/… |
| reason | text | |
| received_at / created_at | timestamptz | |

## 变更记录
- 2026-09-09：v1（2026-09-09 实测）
