# 79 | Common Ground Schema + Runtime 落地最终确认版（Ziven × GPT 双方对齐）

> 2026-09-02 22:05 Ziven 提出6条修正 → GPT 逐条审议 → 全部同意 → 定稿
> 状态：✅ 双方确认，进入实现阶段

---

## GPT 总判断

> 76 号是「理想化新系统设计」，79 号是「现实迁移方案」。
> Ziven 的六个修正方向全部同意——不是退让，是重新按当前真实约束（Cloudflare Worker 单体、已有 author、已有 @解析、已有 chat MCP）评估后，Ziven 的方案更符合正在运行系统的渐进演化路径。

---

## 最终阶段路线

```
Phase 0   数据保护（备份）
Phase 1   Schema 增量迁移（actors/thread_members/thread_contexts/milestones/artifacts）
Phase 1.5 @GPT 最小闭环（chat2api + event + chat_send）🔥 柳柳看到「不用转发」的第一次成功
Phase 2   完整 Agent Runtime（Context 读取/状态机/retry）
Phase 3   Context Worker 能力增强（自动摘要/里程碑生成）
Phase 4   体验层（搜索/UI/多媒体/导出）
```

---

## 六条对齐结论（全部 ✅）

| # | 议题 | 结论 |
|---|---|---|
| 1 | actors 表 vs author 字段 | ✅ 渐进迁移：actors 先建，保留 author 兼容过渡（双写 actor_id + author），读取优先 actor_id、失败回退 author，全部迁移后再删 author。**补：旧数据建 legacy_import actor，不设 system/imported** |
| 2 | mentions 结构化时机 | ✅ 字段第一批加（mentions jsonb 允许空），解析逻辑升级放 Phase 2 Runtime 一起改。文本 @ 只是展示，协议 @ 才是驱动 |
| 3 | Context Worker 部署 | ✅ 逻辑独立 ≠ 物理独立：MVP 在现有 Worker 内做 context module（src/modules/chat+event+context+milestone+artifact），以后拆 worker 只迁 module |
| 4 | message_number 迁移 | ✅ 用 thread_message_counter 表（thread_id, last_number）事务锁计数，避免 count(*) 和删除跳号；旧消息 created_at ASC 回填 1..N，counter=N 继续 |
| 5 | @GPT 最小闭环 | ✅ 强烈同意：Phase 1.5 先做 chat2api 直通+event+chat_send，验证「柳柳看到不需要转发的第一次成功」；完整 Runtime 后置 |
| 6 | Phase 0 数据保护 | ✅ 补三个动作：0.1 Schema snapshot、0.2 Data export（chat_threads/messages/events 三表 JSON）、0.3 Migration rehearsal（先 dev 后 production） |

---

## 唯一补充（GPT 提出，必须收进 79）

### 双写期间数据一致性规则

author + actor_id 同时存在期间：
- **actor_id 是真源，author 是兼容镜像**
- 禁止只修改 author
- 否则迁移永远结束不了

---

## 代码结构建议（Context Worker 单体化）

```
src/
 └── modules/
      ├── chat/
      ├── event/
      ├── context/
      ├── milestone/
      └── artifact/
```

## 双写迁移路线

- Phase 1：chat_messages 保留 author + 新增 actor_id；写入 {author, actor_id} 双写；读取优先 actor_id
- Phase N：所有消费者迁移后删除 author

---

## @GPT MVP 最小链路（Phase 1.5）

```
柳柳/GPT消息 → chat_messages → @GPT → chat_agent_events → chat2api → GPT回复 → chat_send → 页面显示
```

这个成功后再加：context 读取、状态机、retry、lease。

---

*本条由 Ziven 整理（2026-09-02），GPT 逐条审议同意。79号 = 双方确认版，可以开工。*