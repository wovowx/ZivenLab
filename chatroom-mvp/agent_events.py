"""Common Ground MVP: mention parsing and Agent Event generation.

This module intentionally keeps the first implementation small:
- parse @GPT / @Ziven / @liuliu / @all / @沉淀
- store concrete agent targets in messages.mentions
- expand @all to the participating agents (gpt, ziven; liuliu is not an Agent)
- create events idempotently via the database UNIQUE(message_id, agent) constraint
"""

from __future__ import annotations

import os
import re
from typing import Any

from supabase import create_client, Client

AGENTS = ("gpt", "ziven")
ACTORS = ("liuliu", "gpt", "ziven")
ALIASES = {
    "gpt": "gpt",
    "ziven": "ziven",
    "liuliu": "liuliu",
}

# @name matching is deliberately conservative: an @ followed by optional
# whitespace and one of the known names. Case-insensitive for Latin names.
MENTION_RE = re.compile(r"@\s*(gpt|ziven|liuliu|all|沉淀)\b?", re.IGNORECASE)


def parse_mentions(content: str) -> dict[str, Any]:
    """Return normalized mentions plus the special @沉淀 marker.

    mentions contains concrete targets only. @all is expanded to GPT/Ziven.
    @liuliu is retained in mentions for semantic fidelity but does not create
    an Agent Event because liuliu is the human participant, not an Agent.
    """
    found: list[str] = []
    persist: list[str] = []
    persist_seen: set[str] = set()
    needs_digest = False

    for match in MENTION_RE.finditer(content):
        token = match.group(1).lower()
        if token == "沉淀":
            needs_digest = True
            continue
        if token == "all":
            targets = ["@GPT", "@Ziven"]
        else:
            target = "@" + ALIASES[token]
            targets = [target]
        for target in targets:
            if target not in persist_seen:
                persist.append(target)
                persist_seen.add(target)

    return {"mentions": persist, "needs_digest": needs_digest}


def agent_targets(parsed: dict[str, Any]) -> list[str]:
    """Convert persisted mention targets to concrete Agent keys."""
    result: list[str] = []
    for mention in parsed.get("mentions", []):
        agent = mention.lstrip("@").lower()
        if agent in AGENTS and agent not in result:
            result.append(agent)
    return result


def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def process_message(message_id: str, content: str, db: Client | None = None) -> dict[str, Any]:
    """Parse a message, persist mentions, and create Agent Events.

    The operation is intentionally idempotent. Re-running it for the same
    message updates the normalized mentions and attempts event inserts; the
    database UNIQUE(message_id, agent) constraint prevents duplicates.
    """
    client = db or get_supabase()
    parsed = parse_mentions(content)

    client.table("chat_messages").update({"mentions": parsed["mentions"]}).eq(
        "message_id", message_id
    ).execute()

    targets = agent_targets(parsed)
    created: list[str] = []
    for agent in targets:
        response = (
            client.table("chat_agent_events")
            .upsert(
                {
                    "message_id": message_id,
                    "agent": agent,
                    "status": "processing",
                },
                on_conflict="message_id,agent",
                ignore_duplicates=True,
            )
            .execute()
        if response.data:
            created.append(agent)

    return {
        "message_id": message_id,
        "mentions": parsed["mentions"],
        "agent_targets": targets,
        "created_events": created,
        "needs_digest": parsed["needs_digest"],
    }


if __name__ == "__main__":
    raise SystemExit("Import process_message() from an application/worker; no automatic DB mutation is performed.")
