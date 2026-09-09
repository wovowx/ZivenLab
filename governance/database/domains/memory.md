# Memory 域数据模型 · 2026-09-09

> 记忆系统：Agent 的长期记忆 + 文件存储。
> 语义：记忆是 key-value + 分类的语义条目，文件是媒体/文档的元数据表。

## 表清单

| 表 | 角色 |
|---|---|
| memories | 记忆条目 |
| files | 文件元数据 |
| knowledge | （待确认废弃） |

## memories（记忆）
**用途**：所有 Agent（Ziven/GPT）的长期记忆。key + value + 分类。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| key | text | 记忆键（语义） |
| value | text/timestamptz | 内容（或时间） |
| category | text | 分类 |
| title | text | 标题 |
| created_at / updated_at | timestamptz | |

**坑**：不同来源的记忆 key 格式不同（事件/实体/日常…）；分类用于归档。

## files（文件）
**用途**：上传文件的元数据（实际内容在 Supabase Storage）。

| 列 | 类型 | 含义 |
|---|---|---|
| id | uuid PK | |
| file_path | text | 存储路径 |
| file_name | text | 展示名 |
| file_size | int | 字节 |
| file_type / content_type | text | MIME |
| category | text | 分类 |
| tags | jsonb | 标签 |
| description | text | |
| storage_url | text | 完整 URL |
| created_at / updated_at | timestamptz | |

## knowledge
⚠️ 疑似废弃——tables 列表有它，但 schema cache 查不到（42P01 relation not exist）。待确认后从总表移除。

## 变更记录
- 2026-09-09：v1（2026-09-09 实测）
