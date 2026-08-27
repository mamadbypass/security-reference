# LDAP / XPath Injection

Manipulate directory and XML query syntax.

## Methodology

- [ ] Identify search and login filters using LDAP/XPath
- [ ] Test wildcard and boolean injection
- [ ] Extract attributes via blind inference
- [ ] Validate input encoding bypasses

## Tools

- `burp`
- `manual payloads`

## Resources

- [OWASP LDAP Injection](https://owasp.org/www-community/attacks/LDAP_Injection)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
