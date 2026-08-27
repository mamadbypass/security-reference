# SSO & SAML

Test single sign-on and SAML assertion handling.

## Methodology

- [ ] Review SAML response signature validation
- [ ] Test XML signature wrapping
- [ ] Check redirect URI in OAuth/OIDC flows
- [ ] Attempt token replay and mix-up attacks

## Tools

- `burp`
- `saml raider`

## Resources

- [OWASP SAML Security](https://owasp.org/www-community/vulnerabilities/SAML_Security_Cheat_Sheet)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
