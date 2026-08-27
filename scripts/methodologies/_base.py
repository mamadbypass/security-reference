"""Helper to build 5-phase methodology structures."""

from __future__ import annotations


def phases(
    p1: list[str],
    p2: list[str],
    p3: list[str],
    p4: list[str],
    p5: list[str],
) -> list[dict]:
    names = [
        "Phase 1 — Preparation & Scoping",
        "Phase 2 — Discovery & Mapping",
        "Phase 3 — Validation & Testing",
        "Phase 4 — Exploitation & Impact Proof",
        "Phase 5 — Documentation & Reporting",
    ]
    return [
        {"phase": names[0], "steps": p1},
        {"phase": names[1], "steps": p2},
        {"phase": names[2], "steps": p3},
        {"phase": names[3], "steps": p4},
        {"phase": names[4], "steps": p5},
    ]


SCOPE = [
    "Confirm target is in program scope and ROE allows this test type",
    "Set up isolated lab or proxy (Burp/ZAP) with scope filters",
    "Document baseline application behavior and account roles",
    "Identify test accounts for each privilege level",
]
REPORT = [
    "Write step-by-step reproduction with HTTP requests/responses",
    "Capture screenshots or video showing impact (redact sensitive data)",
    "Rate severity using program CVSS or impact matrix",
    "Provide concrete remediation guidance for developers",
    "Retest after fix if program allows verification",
]
