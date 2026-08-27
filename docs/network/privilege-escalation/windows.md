# Windows Privilege Escalation

Escalate privileges on Windows hosts.

## Methodology

- [ ] Run winPEAS or manual enumeration
- [ ] Check unquoted service paths and weak permissions
- [ ] Review token impersonation opportunities
- [ ] Exploit missing patches when in scope

## Tools

- `winpeas`
- `powerup`
- `watson`

## Resources

- [HackTricks Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
