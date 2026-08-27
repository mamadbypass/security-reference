"""Mermaid diagram definitions for security reference topic pages."""

from __future__ import annotations

from diagrams.bug_bounty import BUG_BOUNTY_DIAGRAMS
from diagrams.web import WEB_DIAGRAMS
from diagrams.api_auth import API_AUTH_DIAGRAMS
from diagrams.infrastructure import INFRA_DIAGRAMS
from diagrams.specialized import SPECIALIZED_DIAGRAMS

DIAGRAMS: dict[str, str] = {}
DIAGRAMS.update(BUG_BOUNTY_DIAGRAMS)
DIAGRAMS.update(WEB_DIAGRAMS)
DIAGRAMS.update(API_AUTH_DIAGRAMS)
DIAGRAMS.update(INFRA_DIAGRAMS)
DIAGRAMS.update(SPECIALIZED_DIAGRAMS)


def get_diagram(path: str) -> str | None:
    """Return Mermaid source for a docs path like 'web/sqli/index.md'."""
    key = path.replace("/index.md", "").replace(".md", "")
    return DIAGRAMS.get(key)


def render_diagram_block(path: str) -> str:
    """Render markdown section with mermaid fence, or empty string."""
    diagram = get_diagram(path)
    if not diagram:
        return ""
    return "\n".join([
        "## Overview Diagram",
        "",
        '<div class="sr-diagram" markdown="1">',
        "",
        "```mermaid",
        diagram.strip(),
        "```",
        "",
        "</div>",
        "",
    ])
