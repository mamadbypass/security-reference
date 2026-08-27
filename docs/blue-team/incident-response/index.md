# Incident Response

Contain, eradicate, and recover from security incidents.

## How It Works

Incident response (IR) is the structured process of **detecting, containing, eradicating, and recovering** from security incidents while preserving evidence. NIST SP 800-61 phases:

1. **Preparation** — Playbooks, contacts, tooling, and tabletop exercises.
2. **Detection & Analysis** — Triage alerts, determine scope and severity.
3. **Containment** — Short-term (isolate host) and long-term (block IoCs, disable accounts).
4. **Eradication** — Remove malware, close vulnerabilities, reset credentials.
5. **Recovery** — Restore systems from clean backups; monitor for re-entry.
6. **Post-incident** — Root cause analysis, lessons learned, control improvements.

IR teams balance **speed** (stop bleeding) with **forensic integrity** (chain of custody for potential legal action).

## Exploitation

1. **Activate playbook** — Declare severity (P1–P4); assign incident commander, scribe, and comms lead.
2. **Preserve evidence** — Snapshot VMs, collect EDR triage packages, export relevant SIEM logs before containment alters state.
3. **Scope the incident** — Identify compromised accounts, hosts, and data accessed; build timeline.
4. **Contain** — Network isolate endpoints, disable AD accounts, revoke tokens and API keys.
5. **Eradicate** — Reimage workstations, patch exploited vulnerability, remove persistence (scheduled tasks, registry, golden ticket requires krbtgt reset).
6. **Recover** — Restore from known-good backups; validate integrity before reconnecting to network.
7. **Communicate** — Stakeholder updates per cadence; legal/regulatory notification if PII/PHI affected.
8. **Post-mortem** — Blameless review; track remediation items with owners and deadlines.

## Defense & Mitigation

- **Maintain IR playbooks** for ransomware, BEC, insider threat, and cloud compromise.
- **Tabletop exercises** quarterly with executives and IT.
- **Pre-position tooling** — EDR, forensic workstations, immutable backups, out-of-band comms.
- **Define escalation matrix** — When to involve legal, PR, and law enforcement.
- **Backup and restore testing** — Ransomware recovery depends on clean backups.
- **Retainer with IR firm** — For surge capacity on P1 incidents.
- **Track MTTR metrics** — Containment time, recovery time, repeat incident rate.
- Follow [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final).

## Methodology

- [ ] Activate IR playbook and assign roles
- [ ] Preserve forensic evidence
- [ ] Contain affected systems
- [ ] Perform root cause analysis and lessons learned

## Tools

| Tool | Usage |
|------|-------|
| `thehive` | See [Tools Guide](/TOOLS_GUIDE/) |
| `velociraptor` | See [Tools Guide](/TOOLS_GUIDE/) |
| `ftk imager` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [NIST SP 800-61](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
