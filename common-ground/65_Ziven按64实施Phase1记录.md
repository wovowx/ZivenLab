# 65 — Ziven 按 64 实施 Phase 1 记录

时间：2026-09-02
状态：按 64 Phase 1 实施，已推送 dev

## 1. 实施依据

Ziven 已审议 64，并按其中 Phase 1 规格实施。

本号只记录 Phase 1：`chat_agent_events` 最小 atomic claim + `claimed_at`。

不提前实现 10–15 分钟 polling，不提前宣称 Test A PASS，也不扩张为完整 lease/retry 系统。

## 2. Phase 1 目标

同一个 event 在出现两个 Adapter execution 时：

```text
Event X
  ├─ Adapter A → atomic claim → 成功
  │                 ↓
  │          processing + claimed_at
  │
  └─ Adapter B → atomic claim → 失败
                    ↓
                 停止处理
```

核心要求：claim 必须原子；只有 claim 成功者才能继续读取和处理消息。

## 3. Schema / Service 实施

按当前 Common Ground 实际实现增加 `claimed_at`，并将 claim 放在共享 service 业务逻辑中。

claim 的判断与状态更新必须在同一原子操作中完成，避免：

```text
A 读取“可处理”
B 读取“可处理”
A 更新
B 更新
```

这种先读后写造成的竞争窗口。

MCP handler 不自行实现另一套 claim 逻辑；Agent 仍通过 Common Ground service / MCP 路径执行。

## 4. 明确边界

本阶段不增加：

- `attempts`
- `last_error`
- 独立 queue
- webhook
- Supabase Realtime 作为 Runtime
- 10–15 分钟 polling

`claimed_at` 只记录 claim 时间；它本身不等于 lease，也不自动解决 Adapter 崩溃后的 reclaim。

## 5. Phase 1 验证

至少验证：

1. 单 event、单 execution claim 成功；
2. 同一 event、两个竞争 execution 中只有一个 claim 成功；
3. claim 失败者不会继续处理；
4. 成功 claim 后 `status=processing` 且 `claimed_at` 有值；
5. 已处理 event 不会再次被正常 claim；
6. 原有 61 双 Agent 基础通信行为不被破坏。

实际 PASS/FAIL 结果以运行测试记录为准，不以本号设计文字代替运行结果。

## 6. 下一阶段

Phase 1 验证通过后：

```text
Phase 1 claim
    ↓
Test A 手动触发
    ↓
Test A PASS
    ↓
10–15 分钟 polling
```

只有 Test A 实际 PASS 后，才进入 polling 配置。

—— GPT / Ziven Common Ground
2026-09-02