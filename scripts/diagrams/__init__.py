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


STYLES = """
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff
"""


def get_diagram(path: str) -> str | None:
    """Return Mermaid source for a docs path like 'web/sqli/index.md'."""
    key = path.replace("/index.md", "").replace(".md", "")
    diagram = DIAGRAMS.get(key)
    if not diagram:
        return None
    diagram = diagram.strip()
    if "classDef" not in diagram:
        diagram += STYLES
    return diagram


def render_diagram_block(path: str) -> str:
    """Render markdown section with attack-flow and methodology overview diagrams."""
    diagram = get_diagram(path)
    if not diagram:
        return ""
    from methodologies import methodology_diagram

    parts = [
        "## Overview Diagram",
        "",
        "Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.",
        "",
        "### Attack / Data Flow",
        "",
        '<div class="sr-diagram" markdown="1">',
        "",
        "```mermaid",
        diagram,
        "```",
        "",
        "</div>",
        "",
    ]
    phase_diagram = methodology_diagram(path)
    if phase_diagram:
        parts += [
            "### Testing Workflow",
            "",
            '<div class="sr-diagram sr-diagram-methodology" markdown="1">',
            "",
            "```mermaid",
            phase_diagram,
            "```",
            "",
            "</div>",
            "",
        ]
    return "\n".join(parts)
