# Threat Hunting

Proactively search for adversary activity.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    HYP[Hypothesis] --> DATA[Query endpoint / SIEM]
    DATA --> PATTERN[Anomaly pattern]
    PATTERN --> IOC[New IOC / detection rule]
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff

```

</div>

### Testing Workflow

<div class="sr-diagram sr-diagram-methodology" markdown="1">

```mermaid
flowchart LR
    P1["1. Preparation & Scoping"]
    P2["2. Discovery & Mapping"]
    P3["3. Validation & Testing"]
    P4["4. Exploitation & Impact Proof"]
    P5["5. Documentation & Reporting"]
    P1 --> P2 --> P3 --> P4 --> P5
```

</div>

## How It Works

Threat hunting is **proactive, hypothesis-driven search** for adversary activity that evades automated detections. Unlike alert-driven SOC work, hunters start with questions:

- "Is an attacker using valid credentials for lateral movement?"
- "Are there signs of Kerberoasting in our domain?"
- "Did any workstation beacon to a newly registered domain?"

The hunting loop:

1. **Hypothesis** — From threat intel, incident trends, or ATT&CK gaps.
2. **Investigation** — Query SIEM, EDR, DNS, and network telemetry.
3. **Pattern discovery** — Identify TTPs, IoCs, or behavioral anomalies.
4. **Enrichment** — Determine true positive vs benign admin activity.
5. **Outcome** — New detection rule, incident escalation, or hypothesis retired.

Hunting requires curated data, skilled analysts, and executive support for time not spent on tickets.

## Exploitation

1. **Select hypothesis** — Example: "APT uses WMI for lateral movement" → hunt Event 4688 with `wmiprvse.exe` parent processes.
2. **Gather data** — Pull 30 days of relevant logs into hunting workspace (Velociraptor, Jupyter + pandas, or SIEM).
3. **Stack counting** — Rare process paths, rare parent-child pairs, rare command-line arguments.
4. **Beaconing analysis** — Periodic HTTPS connections with low jitter to unknown domains.
5. **Credential anomaly** — Logons from new countries, impossible travel, service account interactive logons.
6. **Memory and disk hunts** — YARA scans across endpoints for known implants.
7. **Document hunt** — Hypothesis, queries, findings, and detection gaps filled.
8. **Convert wins to detections** — Successful hunts become Sigma rules with tuned thresholds.

## Defense & Mitigation

- **Dedicate hunting hours** — Weekly rotation for Tier 2+ analysts.
- **Maintain hunt library** — Reusable queries tagged by ATT&CK technique.
- **Invest in endpoint visibility** — EDR with process, network, and file telemetry.
- **Feed hunts from intel** — ISAC reports, CISA advisories, and internal incident lessons learned.
- **Measure outcomes** — Hunts resulting in new detections or confirmed incidents.
- **Purple team integration** — Red validates that hunts would catch simulated TTPs.
- **Avoid alert fatigue** — Hunts explore quietly; only escalate confirmed leads.

## Pro Tips

Practical advice from real engagements — use these to test faster and report better.

!!! tip "Hypothesis driven"
    Start with intel: new CVE, odd DNS, or peer anomaly — not random searches.

!!! tip "Velociraptor scale"
    Deploy hunt across fleet without RDPing to each host.

!!! tip "Baseline normal"
    Know what good looks like before declaring evil.

!!! tip "Hunt to detection"
    Every true positive hunt should become a permanent rule.

!!! tip "Time-box hunts"
    4-hour hunts with clear success criteria beat endless scrolling.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Formulate hypothesis from intel or anomaly

### Phase 2 — Discovery & Mapping

- [ ] Select data source: EDR, SIEM, or Velociraptor
- [ ] Write hunt query for suspicious behavior
- [ ] Establish baseline of normal activity
- [ ] Run hunt across enterprise scope

### Phase 3 — Validation & Testing

- [ ] Investigate positive hits manually
- [ ] Determine true positive vs false positive
- [ ] Develop permanent detection from hunt
- [ ] Share IOCs and TTPs with team

### Phase 4 — Exploitation & Impact Proof

- [ ] Document hunt results and new detections
- [ ] Update threat intel feed
- [ ] Schedule follow-up hunt

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification

## Tools

| Tool | Usage |
|------|-------|
| `velociraptor` | [Endpoint visibility](https://github.com/Velocidex/velociraptor) |
| `sysmon` | [Windows monitoring](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) |
| `yara` | Malware detection rules — [virustotal.github.io/yara](https://virustotal.github.io/yara/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
