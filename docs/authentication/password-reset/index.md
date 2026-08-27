# Password Reset Flaws

Exploit weak password reset and account recovery flows.

## Methodology

- [ ] Test token predictability and reuse
- [ ] Host header poisoning on reset links
- [ ] Race reset token validation
- [ ] Check reset for arbitrary email change

## Tools

- `burp`

## Resources

- [OWASP Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
