#!/usr/bin/env python3
# chat2api conversation_id 透出 patch (v8 2026-09-08)
# 让新建对话的 conversation_id 返回给客户端（OpenAI 兼容响应加字段）。
# 匹配失败即 exit 1（防镜像版本漂移静默改错）。
import sys


def patch_chatformat():
    PATH = "/app/chatgpt/chatFormat.py"
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()
    old_a = '                conversation_id = chunk_old_data.get("conversation_id")'
    new_a = ('                conversation_id = chunk_old_data.get("conversation_id")\n'
             '                if conversation_id and not service.conversation_id:\n'
             '                    service.conversation_id = conversation_id')
    count = content.count(old_a)
    if count != 1:
        print(f"[conv_id] ERROR: pattern[chatFormat] found {count} times, expected 1", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old_a, new_a)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[conv_id] OK: chatFormat stores conversation_id")


def patch_api():
    PATH = "/app/api/chat2api.py"
    with open(PATH, "r", encoding="utf-8") as f:
        content = f.read()
    old_b = '            return JSONResponse(res, media_type="application/json", background=background)'
    new_b = ('            if isinstance(res, dict) and getattr(chat_service, "conversation_id", None):\n'
             '                res["conversation_id"] = chat_service.conversation_id\n'
             '            return JSONResponse(res, media_type="application/json", background=background)')
    count = content.count(old_b)
    if count != 1:
        print(f"[conv_id] ERROR: pattern[api] found {count} times, expected 1", file=sys.stderr)
        sys.exit(1)
    content = content.replace(old_b, new_b)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[conv_id] OK: api response includes conversation_id")


if __name__ == "__main__":
    patch_chatformat()
    patch_api()
    print("[conv_id] DONE")
