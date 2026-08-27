# HTTP Parameter Pollution

Abuse duplicate parameters handled differently by proxies and backends.

## Methodology

- [ ] Send duplicate GET/POST parameters
- [ ] Test WAF bypass via parameter splitting
- [ ] Check auth bypass on access control checks
- [ ] Compare framework-specific parsing behavior

## Tools

- `burp`
- `manual fuzzing`

## Resources

- [OWASP HPP](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
