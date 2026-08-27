# Race Condition

Exploit time-of-check to time-of-use flaws.

## Methodology

- [ ] Identify limit checks on coupons, transfers, or votes
- [ ] Send parallel requests with Turbo Intruder or custom scripts
- [ ] Test single-use tokens and rate limits
- [ ] Measure window timing for reliable exploitation

## Tools

- `burp turbo intruder`
- `race-the-web`
- `python asyncio`

## Resources

- [PortSwigger Race Conditions](https://portswigger.net/web-security/race-conditions)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
