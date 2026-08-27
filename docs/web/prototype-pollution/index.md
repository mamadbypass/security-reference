# Prototype Pollution

Pollute JavaScript object prototypes for XSS and RCE.

## Methodology

- [ ] Identify merge/extend utilities in client code
- [ ] Test __proto__ and constructor.prototype keys
- [ ] Look for gadget chains leading to XSS
- [ ] Check server-side Node.js pollution

## Tools

- `burp`
- `ppmap`
- `dom clobbering scanners`

## Resources

- [PortSwigger Prototype Pollution](https://portswigger.net/web-security/prototype-pollution)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
