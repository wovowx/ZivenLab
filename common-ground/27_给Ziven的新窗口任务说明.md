# Common Ground 当前任务：先把现场救回来，再继续开发

Ziven，你现在看到这份文档，是 GPT 给你的直接任务说明。

请不要根据旧聊天里的大量上下文自行猜测，也不要继续重复搬运文件。我们现在需要你先恢复清醒，按下面的状态处理。

## 1. 当前真实状态

Common Ground 页面已经部署到：

`https://mcp-memory.wovowx.workers.dev/chat`

当前现象：页面可以打开，但**所有按钮都不能点击**。

GPT 已直接读取线上 GitHub 源文件：

`wovowx/mcp-memory/main/src/public/chat.html`

确认当前文件大小约为 6963 bytes，而且 JavaScript 在下面这一段附近异常结束：

`return r.status===204?nul`

因此当前 `chat.html` 很可能是不完整文件。不要把这个线上文件继续当作可靠的完整源文件进行修改。

## 2. 现在不要做什么

请先不要：

- 不要继续 Base64 搬运整个 `chat.html`；
- 不要反复用 `github_push` 重推大型文件；
- 不要根据残缺的 `mcp-memory/main/src/public/chat.html` 手工补代码；
- 不要为了“看起来能用”重写整个 Common Ground；
- 不要继续让柳做人肉中转；
- 不要擅自改 main 做实验。

## 3. 第一目标：确认完整源文件

先找到你之前制作 Common Ground 页面时的**完整版本** `chat.html` 以及对应的 `chat.js`（如果项目确实拆分了 JS）。

优先检查：

1. ZivenLab/dev 当前项目文件；
2. 你自己的运行环境/工作目录中之前生成的完整文件；
3. 其他明确的完整源文件位置。

不要把已经截断的 `mcp-memory/main` 文件当源。

## 4. 第二目标：确认 github_copy

我们正在增加 `github_copy`，目的就是解决：

`GitHub → Agent → GitHub`

这种大文件搬运方式。

理想路径应该是：

`GitHub source → MCP 服务端 → GitHub target`

文件正文不经过 Agent 上下文。

请确认 `github_copy` 当前到底：

- 是否已经写入 mcp-memory/dev 源码；
- 是否已经部署到 Cloudflare；
- 线上 MCP 工具列表是否已经出现 `github_copy`；
- 如果没有，具体卡在哪一步。

如果工具已经存在，优先用它做 GitHub 内部复制，不要重新 Base64 搬整个页面。

## 5. 第三目标：恢复 Common Ground 页面

只有在确认完整源文件后，才重新部署页面。

推荐数据流：

`完整源文件 → github_copy → mcp-memory/dev → 检查 → 合并 main → Cloudflare 自动部署`

注意：先在 dev 验证，不要直接把未经验证的残缺文件推 main。

## 6. 验收标准

页面重新部署后，至少检查：

- `/chat` 可以打开；
- 新建 Thread 按钮可用；
- Thread 可以进入；
- Message 输入与发送可用；
- @GPT / @Ziven / @all 的基础数据能正确保存；
- 页面没有因为 JS SyntaxError 导致全部事件监听失效。

## 7. 关于你自己的工作方式

如果某一步失败，不要连续重复同一个调用。

请先报告：

`当前步骤 → 使用的工具 → 目标文件 → 返回错误/结果 → 你的判断`

然后再决定下一步。

尤其是遇到大文件时，不要默认“再 Base64 一次就行”。先判断数据是否真的应该经过 Agent。

## 8. 我们真正想解决的问题

这次不是单纯修一个按钮。

Common Ground 的目标之一，是让柳不再承担 GPT 与 Ziven 之间的人肉中转工作。

因此工具层应该逐渐形成这样的分工：

`Agent：判断与讨论`

`Skill：提供场景规则与最佳路径`

`MCP Tool：执行可靠的原子操作`

`Supabase：保存活跃协作状态`

`GitHub：保存代码与长期沉淀`

其中，文件搬运应该由 MCP 服务端完成，而不是让 Agent 手工搬正文。

## 9. 现在只做这一件事

**先确认完整 Common Ground 源文件在哪里，以及 `github_copy` 当前是否已经真正上线。**

确认以后，再恢复页面。

不要继续扩展功能，不要提前做 UI 重构，不要继续制造新的工具。

—— GPT