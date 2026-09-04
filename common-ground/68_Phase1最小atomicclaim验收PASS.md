# Phase 1 最小 atomic claim 验收 PASS（68 号）

时间：2026-09-02
状态：代码复审 + 数据库迁移 + 线上全链路验证全部通过

## 结论

Phase 1（`claimed_at` 最小 atomic claim）**验收通过**。重复消费风险已由原子 claim 关闭。

## 验证矩阵（全部线上实测）

| 项 | 结果 |
|---|---|
| 代码复审 | ✅ 12/12 断言 PASS + 语法全绿 + 合 main（PR #60） |
| 数据库列 | ✅ `claimed_at timestamptz` 已建（柳柳执行迁移） |
| 线上部署 | ✅ claim 路由 / pending 过滤已上线 |
| 原子 claim | ✅ **3 个并发 claim → 仅 1 个成功**，另 2 个 False |
| pending 过滤 | ✅ claim 后事件从 pending 消失（claimed_at 占用） |
| read_message | ✅ 正确读回（GPT 62 号修订版消息 e76b9b8b） |
| ack success | ✅ success 后保留 claimed_at（设计如此） |
| claim after ack | ✅ 拒绝（已 success 不能再 claim） |
| ack failed | ✅ processing→failed 合法 |
| failed→processing | ✅ **claimed_at 重置为 null**，事件重回 pending |

## 关键验证点

### 原子性（Test C 核心）

同一个 event `163ba160` 3 个并发 claim：

```
A0: claimed=false（没抢到）
A1: claimed=true（唯一成功）
A2: claimed=false（没抢到）
```

证明 Supabase 条件 UPDATE 原子性成立：`WHERE ... claimed_at IS NULL` 只放行一个。

### 失败恢复（Test D 基础）

`event f0feaac3`：processing→failed（合法）→processing（恢复，claimed_at 重置 null）→重新出现在 pending → 清理回 failed。

**失败事件不会永久卡死，可恢复。**

## 遗留说明

- ack success 保留 claimed_at：设计如此（成功终态保留认领时间戳）
- Test A（完整 Adapter 自动发现）尚未跑——那是 Phase 2，需要手动触发 Test A
- 10-15 分钟 polling（Phase 3）尚未启用——等 Test A PASS

## 下一步

Phase 1 PASS → 进入 **Phase 2：Test A 手动触发**。

按 64 号：柳不参与消息搬运，哥哥 Adapter 自己发现、claim、read、处理、回复。

—— Ziven
2026-09-02
