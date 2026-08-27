# CRLF Injection

Inject carriage return and line feed to manipulate HTTP responses.

## Methodology

- [ ] Test redirect and header-reflecting parameters
- [ ] Attempt response splitting
- [ ] Inject Set-Cookie or Location headers
- [ ] Chain with XSS via injected headers

## Tools

- `burp`
- `crlfuzz`

## Resources

- [PayloadsAllTheThings CRLF](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CRLF%20Injection)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
