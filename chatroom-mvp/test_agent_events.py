"""Small dependency-free parser tests for Common Ground MVP."""

from agent_events import agent_targets, parse_mentions


def check(content, mentions, targets, digest=False):
    parsed = parse_mentions(content)
    assert parsed["mentions"] == mentions, (content, parsed)
    assert agent_targets(parsed) == targets, (content, parsed)
    assert parsed["needs_digest"] is digest


# Normal mentions
check("@GPT 请看看", ["@GPT"], ["gpt"])
check("@GPT @Ziven 请分别看看", ["@GPT", "@Ziven"], ["gpt", "ziven"])

# Case/whitespace normalization
check("@ gPt   @ ZIVEN", ["@GPT", "@Ziven"], ["gpt", "ziven"])

# @all expands to the Agent set only (human liuliu is not an Agent)
check("@all 大家看看", ["@GPT", "@Ziven"], ["gpt", "ziven"])

# Duplicate mentions are de-duplicated
check("@GPT @GPT @Ziven @GPT", ["@GPT", "@Ziven"], ["gpt", "ziven"])

# Human mention is retained as semantic mention but creates no Agent Event
check("@liuliu 你看看", ["@liuliu"], [])

# Self-mention still targets the concrete Agent
check("@Ziven 你再看看", ["@Ziven"], ["ziven"])

# @沉淀 is a special marker, not an Agent Event
check("@沉淀 请整理一下", [], [], digest=True)

# Unknown @names are ignored by the MVP parser
check("@Nobody 请看看", [], [])

print("PASS: all parser tests")
