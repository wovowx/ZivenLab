#!/usr/bin/env python3
"""
chat2api 消息级挂载 MCP 连接器 patch（v7）
==========================================
让 chat2api 每次发消息时，完全照抄真实浏览器「挂载 Ziven_MCP 连接器」的
payload 结构，使 GPT 原生可调用 MCP 工具，无需页面手动加号。

v7（2026-09-05，柳柳 F12 抓包铁证版）：
┌─────────────────────────────────────────────────────┐
│ 真实浏览器挂插件发的 f/conversation payload：          │
│ content.parts = ["@Ziven_MCP "]                      │
│ metadata = {                                        │
│   "system_hints": ["plugin:asdk_app_..."],           │
│   "serialization_metadata": {"custom_symbol_offsets":│
│     [{"id":"plugin:asdk_app_...","symbol":           │
│       "ecosystemMention","startIndex":0,"endIndex":10}]},
│   "submission_mode": "manual_send"                   │
│ }                                                   │
│ 顶层也有 system_hints: ["plugin:asdk_app_..."]      │
│ ★ 根本没有 developer_mode_connector_ids 字段！       │
└─────────────────────────────────────────────────────┘
v3-v6 一直注入 developer_mode_connector_ids（错误字段）→ GPT 看到
「工具可发现但执行 disabled」。v7 完全照抄真实 payload。

ID：柳柳页面 + 抓包双证实 = 应用 ID asdk_app_6a95a93c9a50819184dcf3468ae0052a
（v5/v6 曾误用版本 ID asdk_app_v_...，已废弃）

匹配失败即 exit 1（防镜像版本漂移静默改错）。
"""

import os
import sys

# 连接器 ID（可用环境变量 MCP_CONNECTOR_ID 覆盖）
CONNECTOR_ID = os.environ.get("MCP_CONNECTOR_ID", "asdk_app_6a95a93c9a50819184dcf3468ae0052a")

def patch_chatformat():
    """patch /app/chatgpt/chatFormat.py：消息级 metadata + @提及"""
    PATH = "/app/chatgpt/chatFormat.py"
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Patch 0: 补 import os
    if "import os\n" not in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("import "):
                lines.insert(i, "import os")
                break
        content = "\n".join(lines)
        print("[chatFormat] OK: import-os inserted")
    else:
        print("[chatFormat] SKIP: import os already present")

    # Patch 1: multimodal 分支（带附件消息）→ 注入 system_hints 结构
    old1 = (
        "            metadata = {\n"
        '                "attachments": attachments\n'
        "            }"
    )
    new1 = (
        "            metadata = {\n"
        '                "attachments": attachments,\n'
        '                "system_hints": ["plugin:%s"],\n'
        '                "serialization_metadata": {"custom_symbol_offsets": [{"id": "plugin:%s", "symbol": "ecosystemMention", "startIndex": 0, "endIndex": 10}]},\n'
        '                "submission_mode": "manual_send"\n'
        "            }"
    ) % (CONNECTOR_ID, CONNECTOR_ID)

    # Patch 2: 纯文本分支 → @提及 + system_hints 结构
    old2 = (
        '            content_type = "text"\n'
        "            parts = [content]\n"
        "            metadata = {}"
    )
    new2 = (
        '            content_type = "text"\n'
        '            if role == "user":\n'
        '                parts = ["@Ziven_MCP " + content]\n'
        '                metadata = {\n'
        '                    "system_hints": ["plugin:%s"],\n'
        '                    "serialization_metadata": {"custom_symbol_offsets": [{"id": "plugin:%s", "symbol": "ecosystemMention", "startIndex": 0, "endIndex": 10}]},\n'
        '                    "submission_mode": "manual_send"\n'
        "                }\n"
        "            else:\n"
        "                parts = [content]\n"
        "                metadata = {}"
    ) % (CONNECTOR_ID, CONNECTOR_ID)

    for label, old, new in (("multimodal", old1, new1), ("text", old2, new2)):
        count = content.count(old)
        if count != 1:
            print(f"[chatFormat] ERROR: pattern[{label}] found {count} times, expected 1", file=sys.stderr)
            sys.exit(1)
        content = content.replace(old, new)
        print(f"[chatFormat] OK: {label}")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[chatFormat] DONE")
    return content


def patch_chatservice():
    """patch /app/chatgpt/ChatService.py：顶层 system_hints"""
    PATH = "/app/chatgpt/ChatService.py"
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Patch 0: 补 import os
    if "import os\n" not in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("import "):
                lines.insert(i, "import os")
                break
        content = "\n".join(lines)
        print("[ChatService] OK: import-os inserted")
    else:
        print("[ChatService] SKIP: import os already present")

    # Patch 1: 顶层 system_hints 注入插件
    old = '            "system_hints": [],'
    new = '            "system_hints": ["plugin:%s"],'
    count = content.count(old)
    if count != 1:
        print(f"[ChatService] ERROR: pattern[system_hints] found {count} times, expected 1", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old, new % CONNECTOR_ID)
    print("[ChatService] OK: system_hints injected")

    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[ChatService] DONE")
    return content


if __name__ == "__main__":
    cf = patch_chatformat()
    cs = patch_chatservice()
    print("\n=== VERIFY ===")
    print("[chatFormat] '@Ziven_MCP' count:", cf.count("@Ziven_MCP"))
    print("[chatFormat] system_hints count:", cf.count("system_hints"))
    print("[chatFormat] ecosystemMention count:", cf.count("ecosystemMention"))
    print("[chatFormat] developer_mode_connector_ids count:", cf.count("developer_mode_connector_ids"))
    print("[ChatService] system_hints count:", cs.count("system_hints"))
    print("[ChatService] plugin count:", cs.count(f"plugin:{CONNECTOR_ID}"))
    print(f"[ALL] CONNECTOR_ID={CONNECTOR_ID}")