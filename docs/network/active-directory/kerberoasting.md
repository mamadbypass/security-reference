# Kerberoasting

Extract and crack service ticket hashes offline.

## Methodology

- [ ] Find SPN accounts with sufficient rights
- [ ] Request TGS tickets for offline cracking
- [ ] Use strong wordlists and rules
- [ ] Validate cracked creds for lateral movement

## Tools

- `rubeus`
- `impacket GetUserSPNs`
- `hashcat`

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
