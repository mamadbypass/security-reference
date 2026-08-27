# API Versioning Issues

Find deprecated API versions with weaker security controls.

## Methodology

- [ ] Discover /v1, /v2, /beta, /internal paths
- [ ] Compare auth requirements across versions
- [ ] Test legacy mobile API backends
- [ ] Check unauthenticated debug versions

## Tools

- `ffuf`
- `burp`
- `kiterunner`

## Resources

- [OWASP API Security Top 10](https://owasp.org/API-Security/)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
