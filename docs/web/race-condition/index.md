# Race Condition

Exploit time-of-check to time-of-use flaws.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
sequenceDiagram
    participant A as Attacker
    participant S as Server
    participant DB as Database
    par Parallel requests
        A->>S: Transfer $100
        A->>S: Transfer $100
    end
    S->>DB: Check balance once
    DB-->>S: OK
    S->>DB: Double spend
```

</div>

## How It Works

Race conditions in web applications exploit the gap between **checking** a condition and **using** the result (time-of-check to time-of-use, TOCTOU). Parallel requests can pass a limit check simultaneously before any request completes the state update.

Classic web examples:

- Double-spend: two parallel transfers when balance covers only one
- Coupon reuse: same discount code applied concurrently
- Vote or like limits bypassed
- Account creation with single-use invitation tokens
- File upload race: swap file after path check

Single-threaded request handling does not eliminate races when multiple app instances, async workers, or database transactions with weak isolation interact.

Microsecond-level windows matter: attackers send dozens of simultaneous HTTP/2 or TCP connections with Burp Turbo Intruder or custom asyncio scripts.

## Exploitation

**Identify targets**

1. Operations with limits: balance, inventory, rate limits, one-time tokens.
2. Multi-step flows where step 2 assumes step 1 state unchanged.
3. File operations: upload then execute, move then read.

**Parallel request technique**

Send 20–100 identical POSTs in the same millisecond:

```python
import asyncio, aiohttp

async def post(session):
    await session.post("https://target.com/apply-coupon", data={"code": "SAVE50"})

async def main():
    async with aiohttp.ClientSession() as s:
        await asyncio.gather(*[post(s) for _ in range(50)])

asyncio.run(main())
```

**Attack flow**

```
Request A and B read balance=100 → both pass check for 100 debit → both commit → balance=-100 or double payout
```

**Last-byte synchronization**

- Align requests with `Connection: close` bursts
- HTTP/2 single-connection multiplexing for tighter timing
- Turbo Intruder `race` mode with gate release

**Indicators**

- Inconsistent final state vs expected single-operation outcome
- Multiple success responses where only one should succeed

## Defense & Mitigation

**Atomic operations**

- Use database constraints: `CHECK (balance >= 0)`, unique indexes on coupon usage per user.
- Single atomic SQL: `UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100`.

**Transactions and locking**

- `SELECT ... FOR UPDATE` in transactions for financial operations.
- Distributed locks (Redis Redlock) for cross-instance critical sections—use carefully with fencing tokens.

**Idempotency**

- Idempotency keys on payment APIs; server stores processed key set.
- One-time tokens consumed atomically with compare-and-swap.

**Design**

- Avoid check-then-act in application memory; push rules to DB or transactional message queues.

**Testing**

- Load tests with deliberate parallelism in staging.
- Property-based tests asserting invariant (balance never negative).

## Methodology

- [ ] Identify limit checks on coupons, transfers, or votes
- [ ] Send parallel requests with Turbo Intruder or custom scripts
- [ ] Test single-use tokens and rate limits
- [ ] Measure window timing for reliable exploitation

## Tools

| Tool | Usage |
|------|-------|
| `burp turbo intruder` | [Race condition & burst attacks](../../TOOLS_GUIDE.md#burp-suite) |
| `race-the-web` | [Race condition testing](../../TOOLS_GUIDE.md#race-the-web) |
| `python asyncio` | [Async HTTP for race condition PoCs](../../TOOLS_GUIDE.md) |

## Resources

- [PortSwigger Race Conditions](https://portswigger.net/web-security/race-conditions)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
