# Common Ground：MCP 与 Skill 优化草案

> 状态：讨论草案，尚未定稿
> 参与：柳 / GPT / Ziven
> 目标：减少 Agent 搬运、重复调用、上下文浪费与 token 消耗，让工具真正承担工具应该承担的工作。

## 1. 基本架构原则

目前倾向采用三层思路：

```text
MCP Tools = 原子能力
        ↓
Skills = 能力组合 + 使用策略 + 最佳实践
        ↓
Agent = 根据任务寻找 Skill，并按 Skill 调用工具
```

工具可以很多，不需要为了控制工具数量而牺牲原子能力；真正需要控制的是 Agent 是否需要在大量工具中盲目选择，以及是否需要自己搬运数据。

因此：工具层负责“能做什么”，Skill 层负责“这件事应该怎么做、怎么做更省 token、更少出错”。

## 2. 反苦力原则

判断工具是否需要优化时，优先问：

> 当前这一步是否本应由工具完成，却被迫让 Agent 读取、转换、复制、拼接、重复调用？

如果是，应优先考虑在工具层解决，而不是让 Skill 教 Agent 进行复杂 workaround。

目标不是单纯增加工具数量，而是：

- 减少数据经过模型上下文；
- 减少重复 read / write；
- 减少不必要的工具往返；
- 减少大文件搬运；
- 减少 Agent 自己做编码、复制、拼装等低价值工作；
- 降低 token、延迟和出错概率。

## 3. GitHub：当前最明确的优化区

### 3.1 github_read

现状：一次性读取整个文件，长文件可能导致返回结果截断或 Agent 需要反复读取。

候选改进：

- 支持 start_line / end_line 或 offset / limit；
- 返回 total_lines / returned_lines / has_more；
- 支持按关键词定位，再读取相关范围；
- 必要时支持搜索结果 + 上下文范围，而非整文件返回。

原则：能按需读取，就不要强制 Agent 把整个文件搬进上下文。

### 3.2 github_push

现状：完整文件内容通过 content 或 content_base64 作为 MCP 参数传输。长文件需要 Agent 自己搬运，并可能遇到参数长度问题。

候选改进：

- 小文件继续支持 content；
- 大文件考虑 file_ref / 文件上传接口 / 原始 HTTP body 等方式；
- 不要求 Agent 自己 base64、切片、拼接；
- 能由 Worker 内部完成的数据转换，就不要让 Agent 做。

### 3.3 github_copy

建议新增跨仓库/跨分支文件复制能力。

示意：

```text
ZivenLab/dev/path/to/file
            ↓
       github_copy
            ↓
mcp-memory/main/src/public/file
```

文件内容应在 MCP / GitHub API 内部流转，不经过 Agent 上下文。

这是 Common Ground / 项目协作场景的重要能力。

### 3.4 github_patch

建议新增局部修改能力。

目标：修改大文件的局部内容时，不需要：

```text
read 整文件 → Agent 修改整文件 → push 整文件
```

理想方式：

```text
定位/读取需要修改的范围 → patch → GitHub
```

### 3.5 github_search

建议增加仓库内搜索，帮助 Agent 先定位，再按范围读取。

例如查找 `/chat`、某个函数名、某个配置项时，不需要逐个文件 read。

### 3.6 github_diff

优化代码审查和变更理解，优先返回真正差异，而非重复搬运完整文件。

### 3.7 github_deploy / github_sync

后续可以考虑把已知部署链路抽象成高层动作，例如：

```text
ZivenLab → mcp-memory → Cloudflare
```

但 deploy/sync 涉及覆盖、删除、冲突和环境规则，应在真实工作流稳定后再实现。

## 4. Supabase：优先增强现有工具，而不是盲目增加工具

现有 supabase_db 已支持：query / insert / update / delete / tables / exec，并带 select / filters / limit / offset / order。

这已经是不错的原子能力。

候选优化：

- 对大结果提供明确分页信息；
- 控制默认返回量；
- Skill 规定优先指定 select 字段，不使用无条件 SELECT *；
- 大查询明确 has_more 等状态；
- 将统计/聚合类操作尽量在数据库端完成，而不是把大量行交给 Agent 自己计算。

原则：数据库负责计算和筛选，Agent 尽量只接收最终需要的信息。

## 5. Memory：重点是减少无效上下文

现有 memory 工具已经覆盖 search / list / by_date / by_category / stats / suggest / move 等。

现阶段不急着增加大量工具。

重点观察：

```text
搜索
 ↓
候选记忆
 ↓
相关性筛选
 ↓
必要时读取完整内容
```

而不是：

```text
搜索
 ↓
几十/几百条记忆全部返回
```

后续可以考虑 memory consolidation / 去重合并能力，但应该基于真实使用问题决定。

## 6. query_files

当前工具已经具备 keyword / category / content_type / tags / limit / offset 等筛选能力。

它可以作为“Agent-friendly 查询工具”的参考样例。

未来可考虑增加可选 preview，让 Agent 在不打开完整文件的情况下获得短摘要/前 N 字信息。

## 7. Workflow / Agent 唤醒

这是解放柳的重要方向。

理想链路：

```text
Message
 ↓
Agent Event
 ↓
Workflow / 事件触发
 ↓
对应 Agent
 ↓
Reply
```

MVP 阶段可以接受 2–5 分钟轮询，但长期方向应该减少 Agent 无意义地反复检查“有没有新事件”。

需要继续观察：

- Workflow 是否能稳定承担事件唤醒；
- 是否存在更直接的 webhook / event-driven 方案；
- 如何让 Agent 在没有新任务时不浪费调用和 token。

## 8. Batch / 聚合能力

可以考虑受控的 batch 能力，让多个无依赖的小操作一次完成，减少工具往返。

但不建议做成无边界万能执行器，以免增加安全、调试和错误隔离成本。

先观察真实场景中哪些操作经常成组出现，再决定是否抽象。

## 9. Tool 与 Skill 的职责边界

建议长期遵循：

### Tool

提供可靠、确定、可复用的原子能力。

### Skill

提供场景化流程，例如：

- GitHub 项目协作 Skill
- Common Ground 协作 Skill
- 项目部署 Skill
- Memory 管理 Skill
- Agent Event / Workflow Skill

Skill 应该明确：

- 先做什么；
- 后做什么；
- 哪些工具优先；
- 哪些行为禁止；
- 如何减少 token 和重复搬运；
- 失败时如何判断下一步。

## 10. 一个重要的设计判断

以后发现问题时先区分三类：

### A. Tool 缺能力

例如 GitHub 无法高效复制文件 → 增加 github_copy。

### B. Tool 有能力，但 Skill 没告诉 Agent 正确用法

例如 supabase_db 有 limit/select，却没有规定不要全表查询 → 优化 Skill。

### C. Tool 和 Skill 都存在，但工作流仍然需要大量模型参与搬运

例如大文件读写需要模型复制内容 → 优化底层接口，让数据绕开模型上下文。

## 11. 当前候选优化顺序

第一阶段：

1. GitHub read 分段/查询
2. github_copy
3. github_patch
4. GitHub search / diff
5. Common Ground Agent Event 唤醒

第二阶段：

6. Supabase 大结果保护/数据库端聚合
7. Memory consolidation
8. query_files preview
9. 受控 batch
10. github_deploy / github_sync

具体优先级可以根据 Common Ground 页面实际运行后产生的真实问题调整。

## 12. “小钱包”原则

Common Ground / MCP 后续优化以“完成同一任务需要最少无效 token 和最少无效调用”为重要评价标准之一。

但不能为了省 token 牺牲可靠性、可审计性、安全性或可回滚性。

尤其明确：

**GitHub 不存任何 API Key、Token、密码、Service Role Key 或其他私密凭证。**

—— GPT
2026-09-01（讨论草案）