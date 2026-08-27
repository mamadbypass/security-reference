# AWS Security Testing

Assess Amazon Web Services misconfigurations and IAM issues.

## Methodology

- [ ] Review IAM policies and privilege escalation paths
- [ ] Check S3 bucket public access
- [ ] Audit security groups and exposed services
- [ ] Test SSRF to metadata service where applicable

## Tools

- `pacu`
- `prowler`
- `scout suite`
- `cloudfox`

## Resources

- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
