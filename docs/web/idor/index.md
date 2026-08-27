# Insecure Direct Object Reference (IDOR)

Access unauthorized objects by manipulating identifiers.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    AUTH[Authenticated user] --> REQ[Request object by ID]
    REQ --> APP{Authorization check?}
    APP -->|missing| LEAK[Other user's data]
    APP -->|present| OK[Access denied]
```

</div>

## How It Works

Insecure Direct Object Reference (IDOR) is an access control failure where the application exposes object identifiers (IDs, filenames, tokens) in requests but fails to verify that the authenticated user is authorized to access the referenced object.

Examples:

- `GET /api/orders/12345` returns any order when IDs are swapped
- `GET /files/report_2024.pdf?user_id=2` exposes another user's file
- GraphQL node IDs or UUIDs that are predictable or leaked elsewhere

IDOR differs from missing authentication: the user is logged in but accesses objects outside their tenancy, role, or ownership. Identifiers may be sequential integers, UUIDs, hashed values, or encoded strings (`base64(userId:docId)`).

Root causes:

- Authorization checked only at menu/UI level, not per API call
- Relying on obscurity of UUIDs instead of server-side policy
- Mass assignment updating fields the user should not control alongside ID swaps

## Exploitation

**Methodology**

1. Create two accounts: low-privilege (attacker) and victim (or second low account).
2. Capture object IDs from legitimate traffic for each account.
3. Replay victim object IDs with attacker session tokens.
4. Test HTTP methods: GET, PUT, PATCH, DELETE.

**Techniques**

- Increment/decrement numeric IDs: `/invoice/1001` → `/invoice/1002`
- Swap UUIDs discovered in JS bundles, emails, or public listings
- Decode encoded IDs: `base64`, JWT payload fields
- Change parent scope: `accountId=100` → `accountId=101`
- Test batch endpoints that accept arrays of IDs

**Attack flow**

```
Attacker authenticates → requests object by ID → server fetches by ID only → no ownership check → unauthorized data returned
```

**Tools**

- Burp Autorize: compare responses across roles automatically
- Custom scripts iterating ID ranges (respect scope and rate limits)

**Impact**

- PII exposure (health records, invoices, messages)
- Account modification (email change, password reset tokens)
- Financial fraud (transfer endpoints with weak checks)

## Defense & Mitigation

**Authorize every request**: After authentication, enforce object-level authorization—"Does this user own or have permission for this `orderId`?" Use central policy services or consistent middleware, not ad hoc checks in scattered controllers.

**Design patterns**

- Use non-guessable IDs (UUIDv4) **plus** authorization—not UUIDs alone.
- Prefer indirect references: session-scoped maps from opaque tokens to internal IDs.
- Scope queries: `SELECT * FROM orders WHERE id = ? AND user_id = ?` in the same query.

**API hygiene**

- Avoid exposing internal sequential IDs in URLs when possible.
- Validate tenant/account context on every nested resource (`/orgs/{orgId}/projects/{projectId}`).
- Log and alert on cross-tenant access attempts.

**Testing**

- Role matrix testing in CI: each endpoint tested with wrong user's object IDs must return 403/404 consistently.

## Methodology

- [ ] Collect object IDs across roles
- [ ] Swap IDs between low and high privilege accounts
- [ ] Test UUID, hash, and encoded identifiers
- [ ] Check mass assignment alongside IDOR

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `autorize` | [Authorization testing (Burp)](../../TOOLS_GUIDE.md#autorize) |

## Resources

- [PortSwigger Access Control](https://portswigger.net/web-security/access-control)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
