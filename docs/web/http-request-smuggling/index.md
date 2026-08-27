# HTTP Request Smuggling

Desynchronize front-end and back-end HTTP parsers.

## Methodology

- [ ] Identify CL.TE and TE.CL behavior
- [ ] Use timing-based detection
- [ ] Exploit for cache poisoning or request hijacking
- [ ] Test HTTP/2 downgrade scenarios

## Tools

- `burp`
- `smuggler`
- `h2csmuggler`

## Resources

- [PortSwigger Request Smuggling](https://portswigger.net/web-security/request-smuggling)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
