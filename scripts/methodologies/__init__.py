"""Phased testing methodology for security reference topic pages."""

from __future__ import annotations

from methodologies.bug_bounty import BUG_BOUNTY_METHODOLOGIES
from methodologies.web import WEB_METHODOLOGIES
from methodologies.api_auth import API_AUTH_METHODOLOGIES
from methodologies.infrastructure import INFRA_METHODOLOGIES
from methodologies.specialized import SPECIALIZED_METHODOLOGIES

# Each entry: list of {"phase": str, "steps": list[str]}
METHODOLOGIES: dict[str, list[dict[str, list[str] | str]]] = {}
METHODOLOGIES.update(BUG_BOUNTY_METHODOLOGIES)
METHODOLOGIES.update(WEB_METHODOLOGIES)
METHODOLOGIES.update(API_AUTH_METHODOLOGIES)
METHODOLOGIES.update(INFRA_METHODOLOGIES)
METHODOLOGIES.update(SPECIALIZED_METHODOLOGIES)

PHASE_NAMES = [
    "Phase 1 — Preparation & Scoping",
    "Phase 2 — Discovery & Mapping",
    "Phase 3 — Validation & Testing",
    "Phase 4 — Exploitation & Impact Proof",
    "Phase 5 — Documentation & Reporting",
]


def get_methodology(path: str) -> list[dict[str, list[str] | str]] | None:
    key = path.replace("/index.md", "").replace(".md", "")
    return METHODOLOGIES.get(key)


def methodology_diagram(path: str) -> str:
    """Return Mermaid flowchart for the 5-phase methodology workflow."""
    key = path.replace("/index.md", "").replace(".md", "")
    phases = get_methodology(key)
    if not phases:
        return ""
    nodes = []
    for i, phase in enumerate(phases, 1):
        label = str(phase["phase"]).split("—")[-1].strip()[:28]
        nodes.append(f'    P{i}["{i}. {label}"]')
    chain = " --> ".join(f"P{i}" for i in range(1, len(phases) + 1))
    return f"flowchart LR\n" + "\n".join(nodes) + f"\n    {chain}"


def render_methodology_block(path: str) -> str:
    phases = get_methodology(path)
    if not phases:
        return ""
    lines = ["## Testing Methodology", ""]
    lines.append(
        "Work through each phase in order. Every step has a checkbox — complete them all "
        "for thorough, reproducible coverage."
    )
    lines.append("")
    # Phase workflow diagram is shown in Overview Diagram section
    for phase in phases:
        lines.append(f"### {phase['phase']}")
        lines.append("")
        for step in phase["steps"]:
            lines.append(f"- [ ] {step}")
        lines.append("")
    return "\n".join(lines)
