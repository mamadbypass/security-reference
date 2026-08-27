# Server-Side Request Forgery (SSRF)

Force server-side requests to internal and cloud metadata endpoints.

## Methodology

- [ ] Find URL import, webhook, and preview features
- [ ] Probe localhost and cloud metadata IPs
- [ ] Use DNS rebinding and redirect chains
- [ ] Escalate to internal service access

## Tools

- `burp`
- `ssrfmap`
- `interactsh`

## Resources

- [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
