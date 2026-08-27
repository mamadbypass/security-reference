# GraphQL Security

Test GraphQL APIs for introspection, batching, and authorization flaws.

## Methodology

- [ ] Enable and review schema introspection
- [ ] Test batch queries for brute force and rate limit bypass
- [ ] Check field-level authorization
- [ ] Look for debug endpoints and IDE exposure

## Tools

- `clairvoyance`
- `graphql-voyager`
- `burp`
- `inql`

## Resources

- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
