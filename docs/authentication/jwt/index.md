# JWT Attacks

Exploit weak JSON Web Token implementations.

## Methodology

- [ ] Test alg:none and key confusion
- [ ] Brute force weak HMAC secrets
- [ ] Modify claims for privilege escalation
- [ ] Check jku and kid header injection

## Tools

- `jwt_tool`
- `burp`

## Resources

- [PortSwigger JWT](https://portswigger.net/web-security/jwt)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
