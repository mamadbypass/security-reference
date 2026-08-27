"""Detailed vulnerability content: how it works, exploitation, defense."""

from vuln_content.web import WEB_CONTENT
from vuln_content.api_auth import API_AUTH_CONTENT
from vuln_content.infrastructure import INFRA_CONTENT
from vuln_content.specialized import SPECIALIZED_CONTENT

VULN_CONTENT: dict[str, dict[str, str]] = {}
VULN_CONTENT.update(WEB_CONTENT)
VULN_CONTENT.update(API_AUTH_CONTENT)
VULN_CONTENT.update(INFRA_CONTENT)
VULN_CONTENT.update(SPECIALIZED_CONTENT)


def enrich_meta(path: str, meta: dict) -> dict:
    """Merge detailed content into page metadata by docs path key."""
    key = path.replace("/index.md", "").replace(".md", "")
    if key in VULN_CONTENT:
        meta = {**meta, **VULN_CONTENT[key]}
    elif not meta.get("how_it_works"):
        title = meta.get("title", "This topic")
        meta["how_it_works"] = (
            f"**{title}** is a security concern that attackers may abuse when "
            f"applications or infrastructure are misconfigured or lack proper controls. "
            f"{meta.get('description', '')}"
        )
        meta["exploitation"] = (
            "Follow the methodology checklist below. Use the recommended tools to "
            "identify weak points, validate impact with a minimal proof-of-concept, "
            "and document exact reproduction steps."
        )
        meta["defense"] = (
            "Apply defense-in-depth: least privilege, secure defaults, input validation, "
            "logging/monitoring, and regular configuration reviews. Map findings to "
            "relevant OWASP, CIS, or MITRE ATT&CK guidance."
        )
    return meta
