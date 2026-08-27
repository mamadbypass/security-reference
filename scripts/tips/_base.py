"""Tip helpers."""

from __future__ import annotations


def t(title: str, body: str, kind: str = "tip") -> dict[str, str]:
    return {"title": title, "body": body, "type": kind}
