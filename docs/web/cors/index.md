# CORS Misconfiguration

Exploit overly permissive cross-origin resource sharing.

## Methodology

- [ ] Check Access-Control-Allow-Origin on sensitive endpoints
- [ ] Test null origin and subdomain reflection
- [ ] Verify credentials with ACAO + ACAC
- [ ] Demonstrate data exfiltration impact

## Tools

- `burp`
- `corsy`
- `CORScanner`

## Resources

- [PortSwigger CORS](https://portswigger.net/web-security/cors)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
