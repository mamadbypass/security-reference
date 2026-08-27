# Clickjacking

Frame sensitive actions to trick users into unintended clicks.

## Methodology

- [ ] Check X-Frame-Options and CSP frame-ancestors
- [ ] Build proof-of-concept iframe overlays
- [ ] Target high-impact actions (password change, payment)
- [ ] Test mobile WebView contexts

## Tools

- `burp`
- `custom html poc`

## Resources

- [PortSwigger Clickjacking](https://portswigger.net/web-security/clickjacking)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
