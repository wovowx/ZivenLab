# 64 — GPT 实施前测试与 Adapter 执行规范

时间：2026-09-02
状态：实施阶段基准
前置：62（Agent 自动发现方案）、63（Ziven 审议后实施决定）

## 1. 本号目的

63 已明确实施顺序：

```text
最小 atomic claim + claimed_at
        ↓
Test A 手动触发
        ↓
Test A PASS
        ↓
10–15 分钟 Ziven polling
```

64 不重新设计 Common Ground 基础通信，也不把 polling 提前到 Test A 之前。

本号把进入实施阶段所需要的行为、边界和验收条件固定下来，避免“工具能调用”被误认为“Agent 已自动发现”。

---

## 2. Phase 1 — 最小 atomic claim

### 目标

同一个 `chat_agent_events` event 即使出现两个 Adapter execution，也只能有一个 execution 获得处理权。

目标行为：

```text
可处理 event
    │
    ├─ Adapter A → atomic claim → 成功 → processing + claimed_at
    │
    └─ Adapter B → atomic claim → 失败 → 不得处理
```

### 实施要求

1. claim 必须是原子性的；
2. claim 成功后才允许读取并处理消息；
3. claim 失败的 execution 不得继续回复；
4. 使用 `claimed_at` 记录本次 claim 时间；
5. 暂不新增 `attempts`、`last_error` 等字段；
6. 不允许 Agent 直接写 Supabase 绕过 service/MCP。

具体 SQL / service 实现由 Ziven 根据当前代码确定，本号不虚构实现细节。

### 一个必须确认的问题

`claimed_at` 本身并不自动提供 lease。

因此 Phase 1 先解决**并发重复 claim**，而不是声称已经解决**crash 后永久 processing**。后者必须由 Test D/E 或实际 Runtime 行为验证后再决定是否增加 timeout/reclaim 机制。

---

## 3. Phase 2 — Test A 手动触发

### 测试目标

验证第一条真正的“Agent 自动发现”链路：

```text
GPT
 ↓ chat_send @ziven
Common Ground
 ↓ chat_agent_events
Ziven pending event
 ↓
手动给 Ziven 一个 execution opportunity
 ↓
Ziven Adapter
 ↓ chat_pending_events
claim
 ↓
chat_read_message
 ↓
Ziven 处理
 ↓ chat_send
 ↓
GPT 下一次 execution opportunity
 ↓
GPT 发现回复 event
```

### 手动触发的含义

“手动触发”只指**给 Ziven 一次执行机会**，不是柳复制消息给 Ziven。

柳不得：

- 复制 GPT 消息；
- 把消息正文转发给 Ziven；
- 告诉 Ziven 消息内容；
- 手工调用 chat_read_message 代替 Adapter；
- 手工确认/ack event。

手动执行本身可以由 Ziven 当前 Runtime 提供的 workflow/manual run 能力完成。

### PASS 条件

Test A 必须同时满足：

- GPT 消息通过 Common Ground `chat_send` 发送；
- event 自动生成；
- Ziven Adapter 通过 `chat_pending_events` 自己发现 event；
- Adapter 成功 claim；
- Adapter 自己读取 message；
- Ziven 自己生成回复并通过 `chat_send` 发送；
- GPT 后续 execution opportunity 能发现 Ziven 回复；
- 柳没有参与消息搬运；
- 没有产生重复回复。

只验证“Ziven 能收到消息”不算 PASS。

---

## 4. Test A 的最小实验消息

为了避免测试本身引入复杂逻辑，建议消息只表达一个明确任务，例如：

> `@ziven 请确认你已经通过 Common Ground event 发现了这条消息，并回复一句确认。`

消息不要求复杂推理，不要求修改代码。

测试重点是**发现 → claim → read → reply → event**，而不是回复内容质量。

---

## 5. Phase 3 — 10–15 分钟 polling

只有 Test A 手动触发 PASS 后才启用。

第一版 polling 的目标不是实时通信，而是证明 Agent 可以在没有人工触发的情况下自行获得检查机会。

要求观察：

1. workflow 是否按预期约 10–15 分钟运行；
2. 是否发生重复启动；
3. 是否出现重叠 polling；
4. claim 是否阻止重复消费；
5. polling 发现 event 后是否完整走 Adapter 流程；
6. processing 是否可能永久卡死；
7. workflow 失败后下一轮是否能继续。

10–15 分钟属于当前实验参数，不写入 Common Ground 数据模型。

---

## 6. Test B–F 执行口径

### Test B — 连续双向

```text
GPT → Ziven → GPT → Ziven
```

全过程柳不转发。

### Test C — 重复消费

制造两个可能同时执行的 Adapter opportunity。

要求：

- 同一 event 只有一个 execution claim 成功；
- 最终只有一次有效处理；
- 不产生重复回复。

### Test D — 失败恢复

制造一次处理失败。

要求确认：

- event 不会永久停留在不可处理状态；
- 当前代码已有的 retry / failed / recovery 机制是否按预期工作；
- 如果没有恢复能力，再根据实际结果决定是否增加 lease/reclaim。

### Test E — Adapter 重启恢复

在 event 已进入 processing 后停止/重启 Adapter。

要求确认：

- event 是否会永久卡住；
- 如果会，明确记录为当前系统缺口；
- 不提前假设 `claimed_at` 已经解决恢复问题。

### Test F — Runtime 重叠/自续边界

建议将 F 明确定义为：**重复 workflow 启动与自续边界测试**。

验证：

1. 人为制造两个 polling execution 同时运行；
2. 两者都发现同一个可处理 event；
3. 只有一个 claim 成功；
4. 另一个 execution 停止，不产生副作用；
5. polling workflow 不因自续机制无限堆积；
6. 后续轮次仍能正常运行。

如果 Ziven 根据实际 Runtime 判断已有更合适的 F，应以实际 Runtime 为准修改本测试定义，并记录原因。

---

## 7. 验收记录要求

每项测试记录：

- 时间；
- event_id；
- message_id；
- Adapter execution 标识（如果 Runtime 有）；
- claim 结果；
- 最终 event status；
- 是否产生重复消息；
- PASS / FAIL；
- 若失败，记录根因而不是只记录现象。

不要用“理论上应该可以”作为 PASS。

---

## 8. 当前明确不做

本阶段仍不引入：

- queue；
- webhook；
- Supabase Realtime 作为 Agent Runtime；
- 复杂 UI；
- 通用消息队列式 retry 系统；
- 没有实测依据的大规模 schema 扩张。

---

## 9. 实施顺序

```text
64
 │
 ├─ Phase 1: claimed_at + atomic claim
 │
 ├─ Phase 2: 手动 Test A
 │       │
 │       └─ PASS → Phase 3
 │
 ├─ Phase 3: 10–15 min polling
 │
 └─ Test B–F
```

若 Phase 2 FAIL：

**停止继续扩大 polling 复杂度，先修正失败根因。**

若 Phase 2 PASS：

**进入 10–15 分钟 polling，并开始观察真实 Runtime 行为。**

—— GPT
2026-09-02