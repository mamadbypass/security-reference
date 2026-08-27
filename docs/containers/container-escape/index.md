# Container Escape

Break out of container isolation to the host.

## Methodology

- [ ] Identify privileged containers
- [ ] Abuse mounted docker.sock
- [ ] Exploit kernel vulnerabilities when in scope
- [ ] Test cgroup release_agent techniques

## Tools

- `deepce`
- `cdk`

## Resources

- [HackTricks Docker Escape](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
