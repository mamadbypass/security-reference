# XXE

XML External Entity injection testing.

## Methodology

- [ ] Identify XML input endpoints
- [ ] Test file read via external entities
- [ ] Attempt SSRF through XXE
- [ ] Check blind XXE with out-of-band callbacks

## Tools

- `burp`
- `xxeinjector`
- `oxmlxxe`

## Resources

- [PortSwigger XXE](https://portswigger.net/web-security/xxe)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
