"""Pro tips for security reference topic pages."""

from __future__ import annotations

from tips.bug_bounty import BUG_BOUNTY_TIPS
from tips.web import WEB_TIPS
from tips.api_auth import API_AUTH_TIPS
from tips.infrastructure import INFRA_TIPS
from tips.specialized import SPECIALIZED_TIPS

# Each entry: list of {"title": str, "body": str, "type": "tip"|"warning"|"info"}
TIPS: dict[str, list[dict[str, str]]] = {}
TIPS.update(BUG_BOUNTY_TIPS)
TIPS.update(WEB_TIPS)
TIPS.update(API_AUTH_TIPS)
TIPS.update(INFRA_TIPS)
TIPS.update(SPECIALIZED_TIPS)


def get_tips(path: str) -> list[dict[str, str]] | None:
    key = path.replace("/index.md", "").replace(".md", "")
    return TIPS.get(key)


def render_tips_block(path: str) -> str:
    tips = get_tips(path)
    if not tips:
        return ""
    lines = [
        "## Pro Tips",
        "",
        "Practical advice from real engagements — use these to test faster and report better.",
        "",
    ]
    for item in tips:
        admon_type = item.get("type", "tip")
        title = item["title"]
        body = item["body"].strip()
        lines.append(f'!!! {admon_type} "{title}"')
        for body_line in body.split("\n"):
            lines.append(f"    {body_line}")
        lines.append("")
    return "\n".join(lines)
