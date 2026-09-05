#!/usr/bin/env python3
"""
chat2api 消息级挂载 MCP 连接器 patch
======================================
让 chat2api 每次发消息时自动在消息 metadata 里塞入
developer_mode_connector_ids，使 ChatGPT 后端认为该消息挂了
Ziven_MCP 连接器，GPT 即可调用 MCP 工具，无需在页面手动加号。

原理（2026-09-05 逆向确认）：
  ChatGPT 网页端「左下角加号挂 MCP 连接器」= 在消息 metadata 的
  developer_mode_connector_ids 数组里写入连接器 ID。
  chat2api 默认不填该字段 → 本次 patch 在发送前补上。

匹配失败即 exit 1（防止镜像版本漂移导致静默改错）。
"""
import sys

PATH = "/app/chatgpt/chatFormat.py"
# 连接器应用 ID（柳柳 2026-09-05 从添加插件信息页抄）
CONNECTOR_ID = "asdk_app_6a95a93c9a50819184dcf3468ae0052a"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Patch 1: multimodal 分支（带附件消息）
old1 = (
    "            metadata = {\n"
    '                "attachments": attachments\n'
    "            }"
)
new1 = (
    "            metadata = {\n"
    '                "attachments": attachments,\n'
    '                "developer_mode_connector_ids": ["%s"]\n'
    "            }"
) % CONNECTOR_ID

# Patch 2: 纯文本分支
old2 = (
    '            content_type = "text"\n'
    "            parts = [content]\n"
    "            metadata = {}"
)
new2 = (
    '            content_type = "text"\n'
    "            parts = [content]\n"
    '            metadata = {"developer_mode_connector_ids": ["%s"]}'
) % CONNECTOR_ID

for label, old, new in (("multimodal", old1, new1), ("text", old2, new2)):
    count = content.count(old)
    if count != 1:
        print(f"[patch] ERROR: pattern[{label}] found {count} times, expected 1", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old, new)
    print(f"[patch] OK: {label}")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[patch] DONE: developer_mode_connector_ids injected")