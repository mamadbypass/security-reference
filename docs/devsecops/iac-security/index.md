# Infrastructure as Code Security

Scan Terraform, CloudFormation, and Kubernetes manifests.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    TF[Terraform / K8s YAML] --> SCAN[checkov / tfsec]
    SCAN --> MIS[Public SG / open S3]
    MIS --> FIX[Block merge / remediate]
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

**Infrastructure as Code** (Terraform, CloudFormation, Pulumi, Kubernetes YAML) defines cloud resources declaratively. Misconfigurations—public S3 buckets, open security groups, overly permissive IAM, unencrypted databases—are committed to git and deployed at scale.

State files (Terraform `.tfstate`) often contain secrets in plaintext. PR-based IaC changes bypass traditional change boards if policy checks are not enforced in CI.

## Exploitation

1. **Static scan**: `checkov -d .`, `tfsec`, `kics` on all IaC directories.
2. **Manual review**: `0.0.0.0/0` ingress, `Principal: *`, missing encryption flags.
3. **State file access**: if `.tfstate` is in S3 without encryption/IAM, extract secrets.
4. **Drift detection**: compare deployed resources vs templates for shadow admin accounts.
5. **Module supply chain**: third-party Terraform modules pulling unexpected providers.
6. **Kubernetes manifests**: privileged pods, hostNetwork, wildcard RBAC in git.

Integrate IaC scanning in PR checks; block merge on critical findings.

## Defense & Mitigation

- Run **policy-as-code** (OPA, Sentinel, Kyverno) on every IaC PR.
- Encrypt and restrict access to **Terraform state**; use remote backends with locking.
- Prohibit public access defaults; use SCPs at org level as guardrails.
- Peer review all infrastructure changes; separate prod apply roles.
- Scan for secrets in IaC with git-secrets and trufflehog.
- Maintain golden modules with secure defaults; deprecate risky patterns.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Collect Terraform, CloudFormation, K8s manifests

### Phase 2 — Discovery & Mapping

- [ ] Run checkov, tfsec, and kics scans
- [ ] Review public security group rules
- [ ] Check IAM wildcards and admin policies
- [ ] Validate encryption flags on storage

### Phase 3 — Validation & Testing

- [ ] Exploit misconfiguration in test account
- [ ] Demonstrate open S3 or SG 0.0.0.0/0 impact
- [ ] Prioritize findings by exploitability
- [ ] Integrate scans into PR checks

### Phase 4 — Exploitation & Impact Proof

- [ ] Report with line numbers and fix snippets
- [ ] Recommend policy-as-code guardrails

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification

## Tools

| Tool | Usage |
|------|-------|
| `checkov` | [IaC security scanner](../../TOOLS_GUIDE.md#checkov) |
| `tfsec` | [Terraform security scanner](https://github.com/aquasecurity/tfsec) |
| `kics` | [IaC security (multi-cloud)](https://github.com/Checkmarx/kics) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
