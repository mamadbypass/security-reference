# Cryptographic Flaws

Identify weak algorithms, modes, and key management issues.

## Methodology

- [ ] Review cipher suites and protocol versions
- [ ] Check for ECB mode and static IVs
- [ ] Test padding oracle conditions
- [ ] Validate random number generation

## Tools

- `testssl.sh`
- `sslscan`
- `burp`

## Resources

- [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
