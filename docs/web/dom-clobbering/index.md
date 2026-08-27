# DOM Clobbering

Overwrite DOM properties using named HTML elements.

## Methodology

- [ ] Review client-side sinks relying on window or form properties
- [ ] Inject elements with id and name attributes
- [ ] Chain with prototype pollution or XSS
- [ ] Test sanitizer bypass via clobbered globals

## Tools

- `burp`
- `dompurify bypass research`

## Resources

- [PortSwigger DOM Clobbering](https://portswigger.net/web-security/dom-based/dom-clobbering)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
