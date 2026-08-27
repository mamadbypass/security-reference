# Web Cache Poisoning

Poison shared caches to serve malicious content.

## Methodology

- [ ] Identify unkeyed headers and parameters
- [ ] Test cacheable responses
- [ ] Confirm poisoning with unique cache keys
- [ ] Assess victim impact on CDN edges

## Tools

- `burp`
- `param-miner`
- `web-cache-vulnerability-scanner`

## Resources

- [PortSwigger Web Cache Poisoning](https://portswigger.net/web-security/web-cache-poisoning)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
