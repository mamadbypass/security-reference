# SQL Injection

Classic SQL injection across query types and database engines.

## Methodology

- [ ] Identify injectable parameters with error and boolean tests
- [ ] Determine query type (UNION, blind, stacked)
- [ ] Extract schema and sensitive records
- [ ] Document minimal proof for reporting

## Tools

- `sqlmap`
- `burp`
- `ghauri`

## Resources

- [PortSwigger SQLi](https://portswigger.net/web-security/sql-injection)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
