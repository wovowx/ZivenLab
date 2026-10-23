# ZivenLab Governance（治理层）

> **推进唯一依据（铁律 · 柳柳 2026-09-04 确认）**：
> 任何规则、知识、状态，若没有进入 Runtime 可加载/验证的生效路径，即视为不存在。
> 打开仓库先看这里——这里只放「现在要遵守的规矩」，不放历史草稿。

## 📍 当前权威入口（推进先看这里）

| 我要知道 | 去这里 | 说明 |
|---|---|---|
| 系统现状 / 去哪查 | `governance/当前项目状态.md` | 系统驾驶舱（状态源） |
| 现在做什么 / 做到哪 | `governance/roadmap.md` | 行动总控台（路线源） |
| 怎么协作 / 怎么讨论 | `governance/协作协议.md` | 协作规则（规则源） |
| 版本记录 | `governance/CHANGELOG.md` | 变更历史 |

## 📁 目录结构（概念示意；具体文件以仓库实时目录为准）

```
ZivenLab/
├── governance/       ← 当前治理与项目真相源
│   ├── README.md     （治理入口）
│   ├── 当前项目状态.md（驾驶舱）
│   ├── roadmap.md    （路线源）
│   ├── 协作协议.md   （协作规则）
│   ├── policy-index.md（规范索引）
│   ├── 真相源导航表.md（全部权威文档位置）
│   ├── 整体架构.md / 资产全景.md / 资产盘点与整理升级计划.md
│   ├── database/    （数据库总览、域文档与设计规范）
│   └── 其他治理、需求、复苏与时间轴文档
├── common-ground/   ← 聊天室历史材料（保留；非当前治理真相源）
├── chatroom/        ← 聊天室项目资产（已暂停，保留）
├── memory-planet/   ← 呈现层设计资产
├── test/            ← 测试资产
└── README.md
```

> `architecture/`、`discussions/`、`archive/` 是旧规划中的目录名，不代表当前仓库已存在这些目录；本轮不为了匹配旧示意而新建或移动文件。治理文档按职责集中在 `governance/`，具体权威文件请查 `governance/真相源导航表.md`。

## 🚩 引用规范

- 权威文档互相引用**写路径**（如 `governance/roadmap.md`），不写「85号」这种名字——文件名会变，路径才是导航。
- **复制/移动文件一律用 `github_copy`**（内容不经 Agent 上下文，MCP 服务端内部搬运），绝不手写整份大文件重推（费 token + 转义/截断风险）。需要改内容：先 copy 再对目标小幅 edit/push。
- 版本规则：本仓为文档仓，用知识快照 `docs-YYYY.MM(.N)`；代码仓（mcp-memory）用 `vX.Y.Z`。详见 `governance/当前项目状态.md` 第 10 章。

## 📝 维护

- 新增权威文档 → 放入本目录 + 更新本 README 的入口表。
- 历史讨论 → 留在 common-ground/，不搬进来。

*2026-09-04 建立。本目录是 ZivenLab 的 governance（治理层）入口。*