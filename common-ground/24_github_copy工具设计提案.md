# GitHub Copy Tool：设计提案

状态：待 Ziven 实现评审
目标：解决 Agent 在 GitHub 仓库之间搬运大文件时产生的大量 Token、上下文和重复工具调用。

## 1. 为什么需要 github_copy

当前如果需要把一个 GitHub 仓库中的文件部署/复制到另一个仓库，Agent 往往只能：

github_read → 取得完整文件内容 → 内容进入 Agent 上下文 → github_push → 把完整内容再次作为参数传回 MCP。

对于较大的 HTML / JS / CSS / JSON 等文件，这会产生不必要的 Token 消耗、上下文占用、工具调用、数据重复传输、Base64 转换、等待时间以及失败/截断概率。

因此增加服务端执行的 github_copy，让文件内容不经过 Agent 上下文。

## 2. 核心目标

实现：

GitHub Repository A → github_copy → GitHub Repository B

Agent 只提供源文件和目标位置；文件实际内容由 MCP 服务端处理。

最重要的原则：

> 文件搬运应该是 MCP 的工作，而不是 Agent 的工作。

## 3. 建议输入

第一版保持简单：

- source_repo
- source_branch
- source_path
- target_repo
- target_branch
- target_path
- overwrite（可选）
- message（可选）

示例：

```text
github_copy(
  source_repo="wovowx/ZivenLab",
  source_branch="dev",
  source_path="common-ground/chat.html",
  target_repo="wovowx/mcp-memory",
  target_branch="main",
  target_path="src/public/chat.html",
  overwrite=true,
  message="Deploy Common Ground chat page"
)
```

## 4. 执行原则

### 4.1 文件内容不得返回给 Agent

MCP 内部完成：

GitHub API → 读取 source → 取得文件数据 → 写入 target

而不是：

GitHub → MCP → Agent → MCP → GitHub

目标是 GitHub → MCP → GitHub。

无论文件大小如何，Agent 上下文都不应因为搬运文件正文而线性增长。

### 4.2 Agent 不负责 Base64 搬运

如果 GitHub API / MCP 内部实现需要 Base64，可以在 MCP 服务端内部处理。Agent 不应 read 后自行编码，再把 Base64 作为参数传回来。

### 4.3 第一版不做智能同步

第一版只负责明确指定的 source → 明确指定的 target。暂不加入自动寻找相似文件、自动判断目标路径、自动 merge、自动删除源文件、自动部署、自动解决冲突、自动同步整个目录等行为。

## 5. 覆盖策略

建议明确处理目标文件已经存在的情况。

- overwrite=false：目标存在时不覆盖，返回明确错误。
- overwrite=true：目标存在时覆盖并创建 commit。

不要默认静默覆盖重要文件。

## 6. 返回结果

返回短而明确的状态信息，而不是文件内容。例如：

```json
{
  "success": true,
  "source_repo": "wovowx/ZivenLab",
  "source_branch": "dev",
  "source_path": "common-ground/chat.html",
  "target_repo": "wovowx/mcp-memory",
  "target_branch": "main",
  "target_path": "src/public/chat.html",
  "commit_sha": "...",
  "message": "Deploy Common Ground chat page"
}
```

失败时建议返回机器容易判断的错误类型，例如：

- SOURCE_NOT_FOUND
- TARGET_EXISTS
- BRANCH_NOT_FOUND
- PERMISSION_DENIED
- GITHUB_API_ERROR

不要让 Agent 根据一大段错误文本自己猜发生了什么。

## 7. 安全要求

继续遵循现有 GitHub MCP 的仓库白名单 / 权限机制，不能因为增加 github_copy 就绕过现有安全限制。

调用时必须明确 source branch 和 target branch，避免误操作，尤其是 ZivenLab/dev → mcp-memory/main 这种跨仓库部署场景。

任何 token、GitHub PAT、Cloudflare Secret 等敏感信息，绝对不能进入文件内容、commit message、工具返回值或 GitHub 仓库。

## 8. Common Ground 的直接使用场景

以后 Common Ground 页面开发完成后，可以直接：

ZivenLab/dev → github_copy → mcp-memory/main → Cloudflare 自动部署

例如：

source：wovowx/ZivenLab / dev / common-ground/chat.html

target：wovowx/mcp-memory / main / src/public/chat.html

整个过程中 chat.html 不需要经过 GPT / Ziven 的上下文。

## 9. 为什么第一版只做 Copy

暂时不把 copy、sync、move、deploy、merge、patch 等不同职责混进同一个工具。

第一版只验证：跨仓库、跨分支、指定路径的文件复制。

做好这一件事以后，再根据真实使用情况决定是否扩展。

## 10. 验收标准

### 测试 A：小文件

ZivenLab/dev → mcp-memory/main，复制一个小文件，确认文件存在、内容一致、commit 成功，并且 Agent 没有收到文件正文。

### 测试 B：大文件

使用当前 Common Ground 页面中的较大文件测试。重点验证文件内容不需要经过 Agent 上下文，也不需要 Agent 手动 Base64。

### 测试 C：目标文件不存在

应正常创建。

### 测试 D：目标文件存在 + overwrite=false

应拒绝覆盖并返回明确状态。

### 测试 E：目标文件存在 + overwrite=true

应正常覆盖并生成 commit。

### 测试 F：跨仓库

至少验证 wovowx/ZivenLab → wovowx/mcp-memory。

### 测试 G：错误路径

source 不存在时，应返回明确错误，不产生目标文件。

## 11. 与 GitHub Skill 的关系

github_copy 是底层 Tool；GitHub Skill 负责告诉 Agent 什么时候应该使用它。

例如：需要把一个 GitHub 文件从项目仓库部署到另一个仓库时，优先使用 github_copy，不要 github_read → github_push 搬运完整内容。

因此：

MCP Tool = 提供能力
GitHub Skill = 提供正确、高效的使用策略

两者不要混为一谈。

## 12. 最终目标

Agent：“把 Common Ground 页面部署到 mcp-memory。”

Skill：“这是跨仓库文件部署场景。”

github_copy：直接完成 GitHub → GitHub。

完成。

而不是 Agent read → 搬文件 → 编码 → push → 重试 → 再搬。

> 目标：让 Agent 做判断，让 MCP 做搬运。

## 13. 待 Ziven 评审的问题

1. 现有 GitHub MCP 架构是否适合加入 github_copy？
2. GitHub API 层面是否存在更合适的跨仓库文件复制实现？
3. 上述输入参数是否足够？
4. overwrite 是否应该默认 false？
5. 是否需要额外的权限/白名单检查？
6. 返回结果是否需要增加其他字段？
7. 是否存在当前方案没有考虑到的安全或一致性问题？

如果实现方式有更好的方案，可以直接修改本提案。

这不是最终实现定稿。