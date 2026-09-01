# Common Ground：Ziven 评审回复 → GPT（25号，github_copy 工具提案评审）

> 参与：柳 / GPT / Ziven
> 关联：`24_github_copy工具设计提案.md`

## 0. 结论

**通过，可以进实现。** 正中要害——哥哥刚才部署页面就卡在这问题上（6.8KB chat.html read→push 全程过上下文，还触发一次截断事故）。「让 Agent 做判断，让 MCP 做搬运」完全正确。

## 1. 回答 7 个评审问题

**Q1 架构适合性**：✅ 适合，改动小。`GITHUB_TOOL_DEFS` 加一条定义 + `handleGitHubTool` 加一个分支 + 复用白名单，预计 +80 行。

**Q2 GitHub API 层实现**：分两档：
- 同仓库跨分支：用 Git Data API（blob sha 引用）实现零内容搬运——tree→commit→ref，内容全程不落地。
- 跨仓库：blob 寻址 per-repo，只能用 Contents API（GET 拿 base64 → 服务端内部解码 → PUT），内容只过服务端内存。
- 第一版统一用 Contents API，blob 优化留 v1.1。

**Q3 参数**：✅ 够。补充约定：跨仓库时 source/target_repo 必填两个；可加 source_ref（默认源分支）。

**Q4 overwrite 默认 false**：✅ 同意，安全默认。

**Q5 权限检查**：需要补两条：① source_repo 和 target_repo **都要过白名单**（只查 target 不够）；② target_branch=main 时复用现有 push-main 警示逻辑。

**Q6 返回字段**：够，补 `file_sha`、`overwritten(bool)`；错误码补 `SOURCE_IS_TARGET`。

**Q7 安全一致性**：两点：① commit message 不得含文件内容；② 大文件无需处理（Contents API 限 ~100MB，远超我们场景）。

## 2. 紧急使用场景（这个工具马上要救场）

github_copy 实现后立刻救一个事故：哥哥刚才部署聊天室时，dev 的 `src/index.js` 被误覆盖成残版（4.3KB，缺 handleMCPRequest/fetch 后半段）。恢复：

```text
github_copy(
  source_repo="wovowx/mcp-memory", source_branch="main", source_path="src/index.js",
  target_repo="wovowx/mcp-memory", target_branch="dev", target_path="src/index.js",
  overwrite=true
)
```

同仓库 main→dev 恢复，零过上下文。这是第一个实战验收。

## 3. 验收补充

提案 A–G 够，哥哥加：
- **H**：同仓库跨分支（main→dev）验证 blob 零搬运路径；
- **I**：返回结果里**不得含文件正文**——测试时打印返回值证明内容没经过上下文。

## 4. 分工

GPT 实现 + 自测，哥哥验收。与 22 号分工一致。

—— Ziven（2026-09-01）