# Chatroom 🌐

柳柳 + Ziven（哥哥）+ GPT 三个角色异步协作的共享空间（Common Ground）。

> **聊天室是 ZivenLab 下的一个项目**。本目录 = 聊天室唯一根。
> 新会话 / 新接手者从本 README 读起。

## 这是什么

聊天室不是「让 AI 闲聊」，而是**三方协作协议层 + 共享项目记忆层 + 事件驱动 Runtime 层**：
- 聊天体验做外壳，本质是「柳柳 @ 谁 → 谁被唤醒 → 读上下文 → 回复 → 事件闭环」的 Agent 协作系统
- 属 ZivenLab 的项目之一（与记忆星球 memory-planet/ 平级）

## 现在做到哪（2026-09-07）

| 里程碑 | 状态 |
|---|---|
| M1.1 Agent Presence State（Agent 消费位置状态） | ✅ 完成上线 |
| M1.2 Agent Rejoin Context（缺席 Agent 补看没被@的消息） | 🟡 代码完成、**链路未闭环**（GPT 走 chat2api / Ziven 走隧道唤醒，皆未注入，见 implementation.md） |
| M1.3 Mention UX（@ 选择 UI） | ⬜ 未开始 |

## 先读哪几份（新框框 5 分钟站稳）

| 顺序 | 文档 | 回答 |
|---|---|---|
| 1 | `README.md`（本文件） | 项目是什么、做到哪 |
| 2 | `architecture.md` | 整个系统为什么这样设计（四层架构） |
| 3 | `implementation.md` | 具体怎么实现的（全链路参考） |
| 4 | `requirements.md` | 完整需求全景与进度 |
| 5 | `overview.md` | 协作原则与参与者 |
| — | `../governance/协作协议.md` | 怎么一起协作/讨论/决策（跨项目治理） |
| — | `../governance/当前项目状态.md` | 系统驾驶舱（推进唯一依据） |
| — | `../governance/roadmap.md` | 行动路线（做什么、做到哪） |

## 目录

```
chatroom/
├── architecture.md    ← 四层架构（为什么这么设计）
├── implementation.md  ← 实现文档（怎么实现、全链路）
├── requirements.md    ← 需求全景
├── overview.md        ← 项目总览（协作原则）
├── mvp/               ← 聊天室 MVP 原型（chat.html + python）
├── xray/              ← chat2api xray（GPT 真身通道工具）
├── skills/            ← 聊天室相关 skill
└── backups/           ← 数据备份/历史快照
```

> 历史讨论记录（01~85 号编号文档）留在 `../common-ground/`（git 已完整保留，为历史归档区，不占现役）。

## 协作铁律（精简）

- **柳柳拍板**：决策权归柳柳；Agent 主动发现问题，无权直接执行
- **讨论带痕迹**：方案要能被别的参与者真正影响（见协作协议）
- **事实与推断分离**：先验证据再下结论；不把推断当事实写进文档
- **代码 = 唯一实时真相**：文档是懒人参考，改代码后顺手更新文档