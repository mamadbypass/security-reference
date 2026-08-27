# Infrastructure as Code Security

Scan Terraform, CloudFormation, and Kubernetes manifests.

## Methodology

- [ ] Run static analysis on IaC templates
- [ ] Check for public resources and open security groups
- [ ] Enforce policy as code in PRs
- [ ] Review state file access controls

## Tools

- `checkov`
- `tfsec`
- `kics`

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
