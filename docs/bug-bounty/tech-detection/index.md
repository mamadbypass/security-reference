# Technology Detection

Fingerprint frameworks, CMS platforms, and third-party integrations.

## Methodology

- [ ] Analyze response headers and HTML comments
- [ ] Check JavaScript bundles and known library paths
- [ ] Map CDN, WAF, and analytics providers
- [ ] Correlate versions with known CVEs

## Tools

- `whatweb`
- `wappalyzer`
- `nuclei`
- `httpx -tech-detect`

## Resources

- [Wappalyzer](https://www.wappalyzer.com/)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
