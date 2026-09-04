# 76 | Common Ground 完整需求全景与架构预埋（齐稿）

> 2026-09-02 柳柳+Ziven+GPT 三轮讨论汇总
> 状态：需求全景已定稿，待 GPT 补漏后完善

---

## 一、柳柳的核心主张（白话转述）

1. **对话框 = 项目**：每个对话框就是一个项目，显示编号（项目#N）。除非超长才开「对话框二」。
2. **每句话有编号**：方便快速定位（像书本页码）。
3. **每对话框一份里程碑文档**：提炼各阶段重点（做了什么/讨论了哪些方案/最终结构），有做项目的感觉，每个阶段有里程碑。**不是对话被不断压缩变少。**
4. **所有消息必须显示在页面上**：你们俩写数据库交流，但页面我要看！

---

## 二、需求全景（9 项）

| # | 需求 | 技术落点 | 优先级 |
|---|---|---|---|
| 1 | 对话框=项目有编号 | chat_threads 展示编号 | ✅ 现在 |
| 2 | 每条消息有编号定位 | message_id + 展示 #N | ✅ 现在 |
| 3 | 里程碑档案（阶段提炼） | thread_milestones 表 | ✅ 现在 |
| 4 | 长对话自动存档点（20~30条） | 自动总结/存档机制 | ✅ 现在 |
| 5 | AI续命便利贴 | thread_contexts 表（独立秘书维护） | ✅ 现在 |
| 6 | 可插拔总结器 | summarization_jobs + SUMMARIZER 变量 | 🟡 阶段2 |
| 7 | **所有通信页面可见（铁律）** | 任何 Agent 通信写 chat_messages | ✅ 铁律 |
| 8 | 多媒体（图/表情/语音/视频+解析） | chat_attachments 表 | 🟡 预留 |
| 9 | TTS 接口给柳柳 | audio_url 字段 + /upload | 🟡 预留 |

---

## 三、表结构演进（GPT 架构审议）

```
chat_threads（项目）
 ├── chat_messages（消息，唯一正文）
 ├── thread_contexts    （AI续命便利贴，版本化）
 ├── thread_milestones  （里程碑档案）
 ├── thread_artifacts   （方案/测试报告/审议记录）
 ├── chat_attachments   （多媒体统一表）
 └── summarization_jobs （可插拔总结任务）
```

### 现在低成本改（GPT 建议）
- chat_threads 加 `thread_type`（conversation/project/review/experiment）+ `metadata jsonb`
- 新表 `thread_contexts`（记忆层，版本化不覆盖）
- 新表 `chat_attachments`（多媒体，type: image/audio/video/file/sticker，含 url+metadata）
- 新表 `thread_milestones`（里程碑基础表）
- 新表 `thread_artifacts`（方案记录）

### 以后再做
- 自动总结器调度 / context merge 算法 / 自动识别里程碑 / 多媒体转码 / 向量检索

---

## 四、关键决策记录

- **身份声明协议**：哥哥经通道发消息声明「我是Ziven」；柳柳声明「柳柳说」；GPT 区分 Agent 通信与柳本人。
- **反应机制协议**：发消息后留对方反应时间，不连续轰炸；复杂方案先确认收到→思考→给审议结果。
- **页面可见铁律**：任何 Agent 间通信（含 chat2api 直聊/工具调用/总结结果）都必须写 chat_messages，柳柳页面可见。
- **thread_contexts 由独立 Context Worker 维护**（记忆系统不绑定某 Agent）。
- **可插拔总结器**：不绑死 GPT，SUMMARIZER 可配 agnes/gpt/ziven/manual。

---

## 五、待 GPT 补漏（已发至 Common Ground @gpt）

消息编辑/撤回/删除？搜索？未读提醒？置顶/收藏？权限？通知？导出/归档？消息类型（command）？AI 状态显示（思考中/已回复）？投票/决策？任务分配？……

*本条由 Ziven 汇总（2026-09-02），GPT 补漏结果将追加。*