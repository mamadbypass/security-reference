# GraphQL Batching Attacks

Abuse query batching to bypass rate limits and brute force.

## Methodology

- [ ] Send arrays of login or OTP mutations
- [ ] Measure rate limit behavior on batched requests
- [ ] Combine aliases for parallel extraction
- [ ] Report auth bypass impact

## Tools

- `burp`
- `custom scripts`

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
