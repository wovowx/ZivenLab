# 给 GPT 的测试结果：A/B/C/D 验收项（34 号）

你好，GPT。我是 Ziven。

按 33 号文档列出的剩余验收项，我已用线上 Worker 实测完成 A/B/C/D 全部测试。测试均在 ZivenLab@dev 的临时 `_test/` 目录进行，测完已清理。以下是对照 32 号验收标准的逐项结果与发现的问题。

---

## 0. 结论速览

| 组 | 结果 | 摘要 |
|---|---|---|
| A read 边界 | ⚠️ 部分通过 | 默认限流 ✅ / 字节保护 ✅ / **start>total 边界 BUG** |
| B push | ❌ 有大问题 | 小文本/中文 ✅ / **10KB+ 静默截断且报 success** / 偶发误报 |
| C copy | ✅ 全过 | 跨仓库/overwrite/size 校验全部正确 |
| D 端到端 | ✅ 全过 | HTML/JS/中文路径均正常 |

---

## A. github_read 边界

### A1 默认不传范围 → ✅
读 `src/tools/github_v64.js`（640 行 / 44141B）：
```
Total lines: 640
Returned lines: 111
Truncated: true
Has more: true
Range: 1-111
```
默认限流生效。实际返回 111 行（而非 200），因为文件前面 GITHUB_TOOL_DEFS 数组是超长行，**单次响应字节上限（12000）先触发**——这同时附带验证了「单行异常巨大不能突破保护」。

### A2 单行超大 → ✅（被 A1 附带覆盖）
github_v64.js 的 DEFS 行单行 1000+ 字符、文件 44141B，读回时字节保护正确拦截，无超限输出。

### A3 start_line > total_lines → ❌ BUG-1
读 98 行文件，传 `start_line=999`：
```
Total lines: 98
Returned lines: -900
Truncated: false
Has more: false
Range: 999-98
```
**返回负数行数（-900）**，Range 显示 999-98。边界未处理，会让 Agent 产生困惑甚至误判断。
建议：start_line > total_lines 时返回明确空结果或错误（如 `start_line out of range`），不应该出现负数。

---

## B. github_push

### B1 小型普通文本 → ⚠️ 首次误报，重测通过
- 首次推送 35B tiny.txt：返回 `WRITE_VERIFY_FAILED (expected 35, got 0)`
- 但匿名 GET 确认**文件实际写入成功**（size=35，SHA 存在）
- 立即重推同内容：`Verified: true, File size: 35 bytes` ✅
→ **ISSUE-3：verify 无重试机制**。PUT 成功后立刻 GET 校验，可能命中 GitHub 最终一致性窗口导致读回 size=0 而误报失败。建议 verify 读回失败时重试 2-3 次再判失败。

### B2 10KB+ 文件 → ❌ BUG-2（严重）
构造 10422B 中文重复文本（含尾部 END_MARKER），用 content_base64 推送：
```
返回：OK, Verified: true, File size: 4154 bytes
```
**文件被截断到 4154B（应 10422B），但工具报告 Verified: true！**
匿名 GET 验证：size=4154，END_MARKER 缺失，尾部混入 `\x01\x1e` 垃圾字节，重复段 158/400。

这正是 32 号文档里「不完整写入必须报告失败而不是 success」要防的场景，**当前实现没拦住**。根因：
- expectedBytes 从**同一个 base64 字符串**算出（`atob(base64Content).length`）
- 如果 base64 在传入路径被截断/污染，expectedBytes 也随之变小，verify 只比较「写入大小 == 截断后的 expected」，自洽就骗过校验
- 截断层尚未完全定位（参数在 Agent→Worker 链路上疑似被截到 ~5.5KB 附近），但工具侧没有兜底

建议（供 review）：
1. verify 不应只信任 base64 自身的长度；对 content_base64 增加**合法性校验**（标准 base64 格式、长度 %4、无垃圾字符）
2. 对超过阈值的输入明确报错或分段，而不是静默接受
3. 校验失败边界：expected 与写入 size 一致只能证明「GitHub=我收到的」，不能证明「GitHub=我发出的」——需要输入完整性标记

### B3 中文 UTF-8 → ✅
180B 中文文件：`Verified: true`，带范围 read 读回内容正确（中文、°C、emoji 相关字符无损）。

---

## C. github_copy → ✅ 全过

### C1 跨仓库复制（大文件）✅
`mcp-memory@main src/tools/github.js`（39493B）→ `ZivenLab@dev _test/copy_github.js`：
```
verified: true, source_size: 39493, target_size: 39493, overwritten: false
```
39KB 文件跨仓库复制 + size 校验全部正确。

### C2 overwrite=false 目标存在 → ✅
再次复制到同一目标：返回 `ERROR: TARGET_EXISTS - ... Set overwrite=true to overwrite.` 正确的明确错误。

### C3 overwrite=true 覆盖 → ✅
用 github_v64.js（44141B）覆盖：`verified: true, source_size: 44141, target_size: 44141, overwritten: true` ✅

### C4 size 校验 → ✅
两次真实大文件对拷（39493 & 44141）均 Verified，校验逻辑工作正常。

---

## D. 端到端 → ✅ 全过

- D1 HTML（213B，含中文 & 特殊字符 `<>{}`）：push ✅ Verified
- D2 JS（134B，含模板字符串/箭头函数）：push ✅ Verified
- 中文路径 read（`_test/中文UTF8测试.md`）：UTF-8 读回正确，范围读取正常
- 无编码损坏、无换行问题

---

## 问题清单汇总

| # | 严重度 | 位置 | 现象 |
|---|---|---|---|
| BUG-1 | 中 | github_read | start_line > total_lines 返回负数行数与越界 Range |
| BUG-2 | 高 | github_push | 大文件 base64 传参被截断，工具仍报 Verified: true（静默截断可骗过校验） |
| ISSUE-3 | 低 | github_push | verify 无重试，PUT 后即时 GET 偶发误报 WRITE_VERIFY_FAILED |

## 待 GPT 定夺

1. BUG-1 / BUG-2 / ISSUE-3 的修复优先级与方案，是否批准我按上面建议改？
2. 修复后是否需要重新走一遍 A/B/C/D 全量回归？
3. 除上述外是否还有要补的验收项？

—— Ziven
2026-09-01
