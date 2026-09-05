#!/usr/bin/env python3
"""
chat2api 消息级挂载 MCP 连接器 patch
======================================
让 chat2api 每次发消息时自动在消息 metadata 里塞入完整的
connector 挂载结构，使 ChatGPT 后端认为该消息挂了
Ziven_MCP 连接器，GPT 即可调用 MCP 工具，无需在页面手动加号。

原理（2026-09-05 逆向确认）：
  ChatGPT 网页端「左下角加号挂 MCP 连接器」= 在消息 metadata 的
  developer_mode_connector_ids 数组里写入连接器 ID，
  同时伴随完整的辅助字段（selected_sources / serialization_metadata 等）。
  chat2api 默认不填该字段 → 本次 patch 在发送前补上完整结构。

匹配失败即 exit 1（防止镜像版本漂移导致静默改错）。

v6（2026-09-05）：metadata 从「只塞 connector_ids」改为「完整结构」。
背景：v3/v4/v5 只塞 developer_mode_connector_ids 单字段，实测 GPT
「能发现工具但执行被禁用」（The Ziven_MCP tool has been disabled.）。
codebai.cn ChatGPT 网页逆向（2026-06-05）显示真实浏览器 metadata 为：
  {
    "developer_mode_connector_ids": [...],
    "selected_sources": [],
    "selected_github_repos": [],
    "selected_all_github_repos": false,
    "serialization_metadata": {"custom_symbol_offsets": []}
  }
缺失辅助字段可能导致后端判定连接器未正确启用 → 工具被 disabled。
v6 补齐全部字段，尽量与真实浏览器一致。
v5（2026-09-05）：CONNECTOR_ID 改为运行时读环境变量 MCP_CONNECTOR_ID。
"""
import sys

PATH = "/app/chatgpt/chatFormat.py"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Patch 0: 文件顶部补 import os（chatFormat.py 默认没有 import os）
if "import os\n" not in content:
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("import "):
            lines.insert(i, "import os")
            break
    content = "\n".join(lines)
    print("[patch] OK: import-os inserted")
else:
    print("[patch] SKIP: import os already present")

# 完整 metadata 结构（与真实浏览器一致）
# 注意：%s 会被替换成 os.environ.get("MCP_CONNECTOR_ID", "")
METADATA_MULTIMODAL = (
    "            metadata = {\n"
    '                "attachments": attachments,\n'
    '                "developer_mode_connector_ids": [os.environ.get("MCP_CONNECTOR_ID", "")],\n'
    '                "selected_sources": [],\n'
    '                "selected_github_repos": [],\n'
    '                "selected_all_github_repos": False,\n'
    '                "serialization_metadata": {"custom_symbol_offsets": []}\n'
    "            }"
)
METADATA_TEXT = (
    '            content_type = "text"\n'
    "            parts = [content]\n"
    '            metadata = {\n'
    '                "developer_mode_connector_ids": [os.environ.get("MCP_CONNECTOR_ID", "")],\n'
    '                "selected_sources": [],\n'
    '                "selected_github_repos": [],\n'
    '                "selected_all_github_repos": False,\n'
    '                "serialization_metadata": {"custom_symbol_offsets": []}\n'
    "            }"
)

# Patch 1: multimodal 分支（带附件消息）
old1 = (
    "            metadata = {\n"
    '                "attachments": attachments\n'
    "            }"
)
# Patch 2: 纯文本分支
old2 = (
    '            content_type = "text"\n'
    "            parts = [content]\n"
    "            metadata = {}"
)

for label, old, new in (("multimodal", old1, METADATA_MULTIMODAL), ("text", old2, METADATA_TEXT)):
    count = content.count(old)
    if count != 1:
        print(f"[patch] ERROR: pattern[{label}] found {count} times, expected 1", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old, new)
    print(f"[patch] OK: {label}")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[patch] DONE: full connector metadata injected (v6)")