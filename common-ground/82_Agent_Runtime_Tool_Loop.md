# 82 号 · Agent Runtime Tool Loop 设计

> 2026-09-03 · Ziven + GPT 对齐 · 柳柳拍板
> 状态：✅ 已批准，分 Phase T1-T4 落地

## 目标

让 GPT 不只当监督员，而是通过 **工具循环** 真正参与写代码/查数据/改代码。柳柳全程可见（不花冤枉token）。

## 核心架构

```
              Common Ground

                  Runtime Gate
                       |
        +--------------+--------------+
        |              |              |
       GPT           Ziven          Tools
        |              |              |
        +--------------+--------------+
                       |
              agent_tool_calls
                       |
                 柳柳可见审计
```

**关键决策（GPT 审议结论）**：
- 不依赖 chat2api 原生 function calling（网关透传不稳）
- 工具循环放 Worker（Runtime Loop），由 event_processor 升级而来
- 人类消息才算触发源，Agent 回复不触发（防自循环，已落地 v2.2）

## 工具循环（Runtime Loop）

```
event
 ↓
Agent Runtime Loop

while(max 5):

 GPT生成
    |
    ├── 普通回复
    │       ↓
    │    chat_send
    │
    └── 工具请求
            ↓
        execute MCP
            ↓
        保存 tool_call
            ↓
        结果回GPT
```

- `MAX_TOOL_ROUNDS = 5`（防死循环）

## 第一批工具（T3 落地）

| 工具 | 作用 | 安全级别 |
|---|---|---|
| context_read | 读 Thread 上下文（治失忆） | 只读 |
| github_read | 看真实代码（不凭感觉写） | 只读 |
| github_patch | 生成修改方案/补丁 | 需审核 |
| supabase_query | 查真实数据 | 只读（白名单） |

**暂缓**：github_push / 文件删除 / 部署权限（T4 再议）

## 数据模型：agent_tool_calls（✅ 已建表）

```sql
id uuid pk default gen_random_uuid()
event_id uuidagent text not null
tool_name text not null
arguments jsonb default '{}'
result jsonb
status text not null default 'pending'  -- pending/running/success/failed
started_at timestamptz
finished_at timestamptz
error text
created_at timestamptz default now()
```

状态机：pending → running → success/failed

链路：
```
chat_agent_event → agent_runtime → agent_tool_calls → tool execute → GPT继续回复
```

## 前端展示（T1 后半）

不做私有思考链，展示**可折叠工具卡片**：

```
GPT

🔧 github_read
   ▼ 展开查看参数

✅ 返回 xxx 文件

回复：我发现问题在...
```

展示内容：工具调用、操作理由摘要、执行结果、决策日志（判断→动作→结果三段）。
参考 Operit 样式：消息内 tool 调用卡片，可展开折叠。

## 落地顺序

| Phase | 内容 | 状态 |
|---|---|---|
| T1 | 建 agent_tool_calls 表 + 前端工具卡片 UI（先用假数据验证） | 🚧 进行中 |
| T2 | Runtime Loop 跑通 + echo 工具验证（GPT→tool→result→GPT） | 待做 |
| T3 | 接真实工具：context_read → github_read → supabase_query → github_patch | 待做 |
| T4 | github_push / 自动部署 / 更高权限 | 待做（需复核） |

## 安全边界

- 工具只读优先，patch/push 需要审核
- MAX_TOOL_ROUNDS=5 防死循环
- 所有工具调用入库可审计（agent_tool_calls）
- Agent 回复不触发事件（防自循环）
