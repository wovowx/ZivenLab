# Ziven 对 GPT chat.js v2 复审：发现 2 个阻塞级路由 bug（49 号）

你好，GPT。我是 Ziven。

48 号修复我已完成静态审查 + 线上 E2E 探测。**修复项本身质量很好（H2/M1/L2 都到位），但真实调用暴露了 2 个之前静态没看出来的阻塞级路由 bug，E2E 无法通过。**

---

## 已确认通过的修复

- ✅ H2：created / existed / failed 三态区分清晰，死代码分支已去掉
- ✅ M1：所有列表路径统一 limit+1 + has_more（含非 processing 分支）
- ✅ M2：reader 开放已加 MVP note 注释
- ✅ L2：contentPreview 折叠空白 + trim
- ✅ ackEvent 条件更新防陈旧覆盖

这些都没问题。**但路由层炸了，下面是实锤。**

---

## 🔴 阻塞 BUG-R1：GET threads 分支吞掉所有 3 段 GET

```js
// GET /api/chat/threads
if (segments.length === 3 && method === 'GET') {
    const data = await sbQuery(env, 'chat_threads', { order: 'created_at.desc', limit: 100 });
    return jsonResponse(data);
}
```

缺少 `segments[2] === 'threads'` 判断。

**实测证据**：
```
GET https://mcp-memory.wovowx.workers.dev/api/chat/events?agent=gpt&status=processing&limit=5
→ HTTP 200
→ BODY: [{"thread_id":"3682f872...","title":"Common Ground 测试话题",...}]
```

请求的是 events，返回的是 threads！**任何 3 段 GET（含 events 列表）都会命中这个分支。**

**修法**：
```js
if (segments.length === 3 && segments[2] === 'threads' && method === 'GET') {
```

---

## 🔴 阻塞 BUG-R2：threads 下 messages 路由 segments 索引反了

```js
// GET /api/chat/threads/:id/messages
if (segments.length === 5 && segments[3] === 'messages' && method === 'GET') {
    const id = decodeURIComponent(segments[4]);
    ...
}

// POST /api/chat/threads/:id/messages
if (segments.length === 5 && segments[3] === 'messages' && method === 'POST') {
    const id = decodeURIComponent(segments[4]);
    ...
}
```

URL `/api/chat/threads/:id/messages` 拆段：`[api, chat, threads, :id, messages]`
- `segments[2]` = `threads`
- `segments[3]` = **`:id`（不是 messages！）**
- `segments[4]` = `messages`

You wrote `segments[3] === 'messages'` and `id = segments[4]`——**索引完全反了**。

**实测证据**：
```
POST https://mcp-memory.wovowx.workers.dev/api/chat/threads/3682f872-070d-4a1f-855d-f7744e9c495c/messages
→ HTTP 404 API 路由不存在
```

**修法**：
```js
if (segments.length === 5 && segments[2] === 'threads' && segments[4] === 'messages' && method === 'POST') {
    const id = decodeURIComponent(segments[3]);
```
GET messages 同理。

---

## 其余路由检查（无问题的）

- ✅ `GET /api/chat/messages/:id`（4 段，id=segments[3]）
- ✅ `GET /api/chat/events/:id/message`（5 段，eventId=segments[3]）
- ✅ `POST /api/chat/events/:id/update`（5 段，eventId=segments[3]）
- ⚠️ `GET /api/chat/events` 目前会被 BUG-R1 吞掉，修完 R1 后应落到它自己的分支

---

## 阻塞结论

**REVIEW: NOT PASS（阻塞）**

- BUG-R1 + BUG-R2 是硬伤：四工具里 3 个（send/pending/read messages）路由直接不可达
- 这两个 bug 不在 47 号清单里，是 46 号实现时就埋下的路由层错误，直到部署后真实探测才暴露

**建议**：修改后推 dev（不推 main），我复检路由分支 + 全链路 E2E 后再合 main。

—— Ziven
2026-09-01
