# GraphQL Batching Attacks

Abuse query batching to bypass rate limits and brute force.

## How It Works

Many GraphQL servers accept an **array of operations** in a single HTTP POST body, executing them sequentially or in parallel and returning an array of results. Libraries such as Apollo Server enable batching by default in some versions. Similarly, **query aliases** let multiple identical or distinct operations run in one request:

```graphql
mutation {
  a: login(user: "victim@corp.com", pass: "0000") { token }
  b: login(user: "victim@corp.com", pass: "0001") { token }
  # ... dozens more aliases
}
```

Rate limiters and WAFs often count **HTTP requests**, not **GraphQL operations**. An attacker can brute-force passwords, OTP codes, or coupon tokens by packing hundreds of attempts into one request that appears as a single API call in logs.

## Exploitation

1. **Identify batch support** — POST `[{"query":"..."},{"query":"..."}]` and observe whether the response is a JSON array.
2. **Baseline rate limits** — Send single login mutations until throttled; record HTTP 429 thresholds and lockout behavior.
3. **Replay as a batch** — Wrap 50–100 login or `verifyOtp` mutations in one array; compare success rate vs. individual requests.
4. **Use aliases for fan-out** — Brute force without arrays if the server rejects batch arrays but allows aliases on one mutation.
5. **Combine with credential stuffing** — Parallel `login` across many users in one batch to evade per-IP limits.
6. **Measure server-side impact** — Note DB connection pool exhaustion or CPU spikes for DoS reporting.
7. **Capture evidence** — Show one HTTP request attempting N passwords and receiving N responses without throttling.

## Defense & Mitigation

- **Disable query batching** on public endpoints unless there is a clear need.
- **Rate-limit by GraphQL operation count and cost**, not only per HTTP request.
- **Apply stricter limits to auth mutations** (`login`, `register`, `resetPassword`, `verifyOtp`) including per-user and per-IP backoff.
- **Cap aliases per query** and reject documents exceeding complexity budgets.
- **Use CAPTCHA or proof-of-work** after a small number of failed auth attempts, regardless of batching.
- **Log and alert** when a single request contains multiple auth mutations.

## Methodology

- [ ] Send arrays of login or OTP mutations
- [ ] Measure rate limit behavior on batched requests
- [ ] Combine aliases for parallel extraction
- [ ] Report auth bypass impact

## Tools

| Tool | Usage |
|------|-------|
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |
| `custom scripts` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
