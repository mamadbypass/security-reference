# Cloud Forensics

Investigate incidents in cloud environments.

## How It Works

**Cloud forensics** investigates incidents in AWS, Azure, and GCP where attackers lack physical access but abuse IAM, APIs, and misconfigurations. Evidence lives in **audit logs** (CloudTrail, Azure Activity Log, GCP Audit Logs), flow logs, snapshot APIs, and SaaS integrations.

Multi-region deployments, ephemeral instances, and shared responsibility models complicate acquisition. Logs may be disabled, encrypted, or in attacker-controlled accounts.

## Exploitation

1. **Preserve logs**: export CloudTrail to immutable S3; enable organization trail.
2. **Snapshot volumes**: EBS/Azure disk snapshots for offline disk forensics.
3. **Memory**: SSM Run Command or vendor-specific memory capture where supported.
4. **IAM trace**: session issuer, `AssumeRole` chains, access key creation events.
5. **Network**: VPC Flow Logs, GuardDuty findings, WAF logs.
6. **Cross-account**: identify role trust policies abused for pivot.

Use dedicated forensics account with read-only roles; avoid modifying evidence in-place.

## Defense & Mitigation

- **Organization-wide audit logging** with log file validation and MFA delete on buckets.
- Central SIEM ingestion for all cloud audit and flow logs.
- Restrict IAM ability to disable logging or delete trails (SCPs).
- Automated snapshots and **Velociraptor/osquery** on cloud workloads.
- Incident response runbooks specific to cloud API abuse.
- Regular purple-team exercises simulating credential theft in cloud consoles.

## Methodology

- [ ] Collect CloudTrail and audit logs
- [ ] Snapshot volumes and memory where supported
- [ ] Trace IAM session activity
- [ ] Preserve evidence across regions

## Tools

| Tool | Usage |
|------|-------|
| `aws cli` | [Cloud forensics with `aws cloudtrail lookup-events`](../../TOOLS_GUIDE.md) |
| `azure monitor` | [Azure log analytics & Sentinel queries](../../TOOLS_GUIDE.md) |
| `gcp logging` | [Cloud Logging & Chronicle investigation](../../TOOLS_GUIDE.md) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
