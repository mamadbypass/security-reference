# Insecure Direct Object Reference (IDOR)

Access unauthorized objects by manipulating identifiers.

## Methodology

- [ ] Collect object IDs across roles
- [ ] Swap IDs between low and high privilege accounts
- [ ] Test UUID, hash, and encoded identifiers
- [ ] Check mass assignment alongside IDOR

## Tools

- `burp`
- `autorize`

## Resources

- [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
