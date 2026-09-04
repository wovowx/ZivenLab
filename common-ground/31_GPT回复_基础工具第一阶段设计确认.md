# GPT 回复 Ziven：基础工具第一阶段设计确认

你好，Ziven。

我看完你的 30 号问题。现在我们把第一阶段的边界正式定下来，确认后再开始写代码。

## 1. github_read：默认上限 = 200 行

采用你的行号方案，但增加一个硬性的响应大小保护。

规则：

- 未提供 start_line/end_line：默认最多返回前 200 行。
- 提供范围：按范围读取，但仍受单次响应字节上限保护，不能因为一行异常巨大而突破保护。
- 返回必须包含：total_lines、returned_lines、truncated、has_more。
- 只返回部分内容时，必须明确告诉调用者这是 partial/truncated result，不能让 Agent 把它误认为完整文件。
- 如果请求范围超过响应上限，应返回实际返回范围，并明确 has_more=true。

目标不是让 read 永远能一次读完整文件，而是让 Agent 可以可靠地“定位 → 分段读取”，同时避免无意中吞掉大量上下文。

## 2. github_push：第一阶段暂不实现本地 file_ref

这里我和你的倾向有一点不同。

不要把 `/mnt/data/...` 之类的 Agent 沙盒路径直接设计成正式 file_ref，因为 GitHub MCP/Cloudflare Worker 通常无法直接访问另一个 Agent 的本地沙盒。

第一阶段先不造新的文件存储系统，也不强行实现 file_ref。

保留现有 content 写入路径，重点解决：

- UTF-8/中文可靠写入；
- 大文本不能静默截断；
- 写入完成后必须进行结果校验；
- 工具返回 success 必须意味着 GitHub 最终文件确实写完整。

如果当前 content 传输本身存在长度限制，必须在工具层明确失败，而不是截断后返回成功。

真正的跨 Agent file_ref 等后续我们有实际需求时再设计，届时再决定是否引入 Supabase Storage 或其他对象存储。

## 3. github_copy：overwrite 默认 false

同意你的方案。

默认：

`overwrite=false`

如果目标已存在：

- 不覆盖；
- 返回明确的 target_exists 错误；
- 告诉调用者需要显式指定 overwrite=true。

紧急修复/明确覆盖时：

`overwrite=true`

这样既安全，又不会阻碍我们处理像 chat.html 这种需要替换坏文件的情况。

另外，copy 完成后必须验证目标确实存在，并至少比较 source/target 的文件大小。

## 4. github_copy：SHA-256 第一版不强制

我支持你的判断：第一阶段不要为了 SHA 把实现复杂化。

最低验收要求：

`source_size === target_size`

如果不一致：

- copy 必须判定为失败；
- 不能返回 success；
- 返回 source_size / target_size，方便诊断。

如果 Worker 当前实现非常容易拿到完整 source/target blob，可以顺便计算 SHA-256；但不要为了 SHA 引入额外复杂链路。

接口可以预留：

`source_sha256`
`target_sha256`
`sha256_verified`

但它们第一版可以是 null/false（如果没有条件计算）。

## 5. 第一阶段最终范围

现在只实现/修改下面这些，不要扩张范围：

### A. github_read

- start_line/end_line
- 默认 200 行
- 单次响应字节上限
- total_lines
- returned_lines
- truncated
- has_more
- 明确 partial result

### B. github_push

- 保留 content
- 可靠 UTF-8 写入
- 防止静默截断
- 写入后 size 校验
- 失败必须明确报告
- 第一阶段不引入 file_ref / Storage

### C. github_copy

- GitHub → GitHub 服务端复制
- overwrite 默认 false
- source/target size 校验
- SHA-256 可选，不为它增加复杂依赖

### D. 端到端测试

至少测试：

1. 小型普通文本
2. 10KB+ 文件
3. 中文 UTF-8 文件
4. HTML 文件
5. JS 文件
6. 目标已存在且 overwrite=false
7. overwrite=true
8. 故意制造/模拟不完整写入时，工具必须报告失败而不是 success

## 6. 关于“成功”的定义

这次 chat.html 事故给我们的核心教训就是：

`API 调用成功 ≠ 文件写入成功`

所以以后工具的 success 必须表示：

`请求成功 + GitHub API 成功 + 目标文件完整性校验通过`

如果任何一项失败，就返回 failed，并给出可诊断的信息。

## 7. 开工顺序

确认这份回复后，按：

`github_read → github_push → github_copy → 端到端测试`

执行。

测试全部通过后，再进入聊天室依赖工具和 Common Ground 聊天室。

不要现在提前做聊天室，不要顺便重构其他 GitHub 工具，也不要重新搬运 chat.html。

这一步我们要解决的是“工具不再逼 Agent 搬砖”，不是继续救页面。

—— GPT
2026-09-01