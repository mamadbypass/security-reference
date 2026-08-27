# Open Redirect

Abuse redirect parameters for phishing and OAuth token theft.

## Methodology

- [ ] Find redirect, next, url, return parameters
- [ ] Test external domain acceptance
- [ ] Chain with OAuth and SSO flows
- [ ] Validate bypasses using //evil.com and encoded URLs

## Tools

- `burp`
- `openredirex`

## Resources

- [PayloadsAllTheThings Open Redirect](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Open%20Redirect)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
