# Docker Security

Assess container images and runtime configurations.

## Methodology

- [ ] Scan images for CVEs and secrets
- [ ] Check privileged mode and volume mounts
- [ ] Review capabilities and seccomp profiles
- [ ] Test container escape primitives

## Tools

- `trivy`
- `docker bench`
- `grype`

## Resources

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
