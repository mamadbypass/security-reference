# DNS Enumeration

Extract DNS records, zone transfer opportunities, and mail infrastructure.

## Methodology

- [ ] Query A, AAAA, CNAME, MX, TXT, NS records
- [ ] Look for SPF/DKIM/DMARC misconfigurations
- [ ] Attempt zone transfers on authoritative nameservers
- [ ] Identify dangling DNS records

## Tools

- `dnsx`
- `dig`
- `dnsrecon`
- `fierce`

## Resources

- [HackTricks DNS](https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/dns)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
