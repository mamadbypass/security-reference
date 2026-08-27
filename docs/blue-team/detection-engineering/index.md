# Detection Engineering

Build detections mapped to MITRE ATT&CK techniques.

## How It Works

Detection engineering is the discipline of building **reliable, actionable security detections** mapped to adversary behaviors (MITRE ATT&CK). The lifecycle:

1. **Threat prioritization** — Select techniques relevant to your industry and threat intel (ransomware, APT, insider threat).
2. **Data source identification** — Determine which logs are required (Sysmon, EDR, Windows Security, DNS, proxy, cloud audit).
3. **Detection authoring** — Write Sigma rules, Splunk SPL, KQL, or Elastic EQL queries with clear logic.
4. **Validation** — Execute atomic red team tests or purple team exercises to confirm true positives.
5. **Tuning** — Reduce false positives without blinding to true attacks.
6. **Maintenance** — Update rules when log formats, tools, or TTPs change.

Good detections specify **analytic story**: data source, logic, false positive guidance, and response playbook link.

## Exploitation

1. **Map coverage gaps** — Compare current detections to ATT&CK matrix; prioritize uncovered techniques with high threat relevance.
2. **Author Sigma rules** — Start from [SigmaHQ](https://github.com/SigmaHQ/sigma); customize for your environment.
3. **Convert to SIEM** — Use sigma-cli or Uncoder to generate Splunk/Elastic/Sentinel queries.
4. **Validate with Atomic Red Team** — `Invoke-AtomicTest T1003.001` and confirm alert fires within SLA.
5. **Define severity and MITRE tags** — Every rule links to technique ID and recommended response.
6. **Build detection-as-code** — Store rules in Git; PR review for logic changes.
7. **Measure MTTD** — Track time from attack simulation to alert in SOC dashboard.
8. **Iterate on false positives** — Add exclusions for known-good admin tools with change control.

## Defense & Mitigation

- **Establish detection engineering as a dedicated function** — Not ad-hoc analyst queries.
- **Maintain ATT&CK coverage dashboard** — Executive visibility into gaps.
- **Require validation before production** — No rule goes live without atomic test evidence.
- **Version-control all detections** — Git repo with CI conversion to SIEM formats.
- **Quarterly purple team** — Red executes; blue validates and improves detections.
- **Document runbooks** — Each high-severity detection links to IR playbook.
- **Retire noisy rules** — Failed detections erode SOC trust; fix or remove.

## Methodology

- [ ] Select high-risk techniques for coverage
- [ ] Author Sigma rules and SIEM queries
- [ ] Validate detections with atomic tests
- [ ] Tune to reduce false positives

## Tools

| Tool | Usage |
|------|-------|
| `sigma` | [Detection rule format](https://github.com/SigmaHQ/sigma) |
| `splunk` | [SIEM search & correlation](../../TOOLS_GUIDE.md) |
| `elastic` | [Elastic Security SIEM & detection](../../TOOLS_GUIDE.md) |
| `atomic red team` | [Detection validation](https://github.com/redcanaryco/atomic-red-team) |

## Resources

- [MITRE ATT&CK](https://attack.mitre.org/)
- [Sigma Rules](https://github.com/SigmaHQ/sigma)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
