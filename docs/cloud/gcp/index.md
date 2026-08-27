# GCP Security Testing

Assess Google Cloud Platform IAM and storage security.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    SCAN[gcp_scanner] --> IAM[GCP IAM bindings]
    SCAN --> BUCKET[Open GCS buckets]
    IAM & BUCKET --> PERSIST[Project takeover]
```

</div>

## How It Works

Google Cloud Platform (GCP) organizes resources in a hierarchy: **Organization → Folders → Projects**. IAM bindings attach roles to principals at any level with inheritance.

Critical services and risks:

- **Compute Engine** — Firewall rules tagged `0.0.0.0/0`; metadata server at `169.254.169.254` (similar SSRF risk to AWS).
- **Cloud Storage (GCS)** — `allUsers` or `allAuthenticatedUsers` IAM bindings.
- **Service accounts** — JSON key leaks; keys do not expire by default.
- **GKE (Kubernetes)** — Cluster admin bindings, workload identity misconfigs.
- **Cloud Functions** — Overprivileged runtime service accounts.

GCP's **Organization Policy Service** can enforce constraints (no public IPs, require OS Login) but is often not fully deployed.

## Exploitation

1. **Authenticate** — `gcloud auth activate-service-account` with leaked JSON key or metadata token from compromised VM.
2. **Enumerate IAM** — `gcloud projects get-iam-policy <project>`; hunt `roles/owner` and `roles/editor`.
3. **Scan storage** — `gsutil ls -p <project>`; check `allUsers:objectViewer`.
4. **Test SSRF to metadata** — Request metadata with `Metadata-Flavor: Google` header.
5. **Service account impersonation** — `roles/iam.serviceAccountTokenCreator` allows token minting.
6. **Firewall audit** — `gcloud compute firewall-rules list` for open SSH/RDP.
7. **GKE access** — `kubectl` with exposed endpoints or stolen kubeconfig.
8. **Privilege escalation** — `iam.serviceAccounts.setIamPolicy` to grant self access to powerful SAs.

## Defense & Mitigation

- **Disable service account key creation** org policy; use Workload Identity.
- **No `allUsers` on buckets** — Use uniform bucket-level access and IAM Conditions.
- **VPC Service Controls** — Perimeter around sensitive projects.
- **OS Login** for SSH instead of metadata-propagated SSH keys.
- **Enable Security Command Center** and audit logs to BigQuery/SIEM.
- **Least-privilege IAM** — Custom roles; avoid primitive Owner/Editor.
- **Regular Forseti/Scout Suite** assessments.

## Methodology

- [ ] Review service account keys and permissions
- [ ] Check GCS bucket IAM bindings
- [ ] Audit firewall rules and VPC design
- [ ] Test metadata server access from workloads

## Tools

| Tool | Usage |
|------|-------|
| `gcp_scanner` | [GCP misconfiguration scan](https://github.com/google/gcp_scanner) |
| `scout suite` | [Multi-cloud audit](../../TOOLS_GUIDE.md#scout-suite) |

## Resources

- [HackTricks GCP](https://book.hacktricks.xyz/cloud-security/gcp-security)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
