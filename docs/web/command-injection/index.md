# Command Injection

Execute OS commands through vulnerable input handlers.

## Methodology

- [ ] Identify ping, traceroute, and file conversion features
- [ ] Test command separators for the target OS
- [ ] Use time delays and out-of-band callbacks
- [ ] Escalate from blind to interactive execution

## Tools

- `commix`
- `burp`
- `ffuf`

## Resources

- [PayloadsAllTheThings Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
