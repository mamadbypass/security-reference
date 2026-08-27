# JWT Attacks

Exploit weak JSON Web Token implementations.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    JWT[JWT token] --> ALG{alg=none / HS confusion?}
    ALG -->|weak| FORGE[Forged token]
    FORGE --> ACCESS[Privileged access]
    JWT --> EXP[Expired? / missing aud]
```

</div>

## How It Works

JSON Web Tokens (JWTs) are compact, signed (or MAC'd) claims objects, typically `header.payload.signature` in Base64url. The header declares `alg` (HS256, RS256, etc.); the payload holds claims like `sub`, `role`, and `exp`. Servers verify integrity using a shared secret (HMAC) or public key (RSA/ECDSA).

Common flaws:
- **`alg: none`** — libraries that accept unsigned tokens.
- **Algorithm confusion** — RS256 public key used as HMAC secret (`alg: HS256`).
- **Weak HMAC secrets** — brute-forced `secret`, `password`, `changeme`.
- **`jku` / `x5u` / `kid` abuse** — server fetches attacker-controlled keys.
- **Missing `exp` / `nbf` validation** and accepting tokens after logout.
- **Sensitive data in payload** — JWTs are base64, not encrypted, unless JWE is used.

## Exploitation

1. **Decode the token** — Inspect header and payload in Burp or `jwt.io` (use only for public tokens, not production secrets).
2. **Test `alg: none`** — Change algorithm to `none` and strip the signature; try variants `None`, `NONE`.
3. **Key confusion** — If RS256, embed the public key in an HS256 token and sign with it (`jwt_tool -X k`).
4. **Brute-force HMAC** — `hashcat -a 0 -m 16500 jwt.txt wordlist.txt` or `jwt_tool -C -d wordlist.txt`.
5. **Tamper claims** — Change `role` to `admin`, `sub` to another user ID after forging a valid signature.
6. **`jku` injection** — Point `jku` to attacker-hosted JWK set; host matching public key.
7. **`kid` manipulation** — SQL injection or path traversal in `kid` lookup (`../../../../dev/null` for empty HMAC secret).
8. **Replay expired tokens** — Remove `exp` if verification is lax; test tokens after password change.
9. **Cross-service replay** — Use tokens intended for API A against API B if audience is not checked.

## Defense & Mitigation

- **Allowlist algorithms** server-side; never trust the header's `alg` blindly.
- **Reject `none`** and enforce asymmetric verification with pinned public keys.
- **Use strong secrets** (≥256-bit random) for HMAC; prefer RS256/ES256 for multi-service setups.
- **Validate all standard claims**: `exp`, `nbf`, `iss`, `aud`; use short TTLs and refresh tokens.
- **Disable `jku`/`x5u` fetching** or pin keys; sanitize `kid` resolution (no filesystem/SQL lookups on attacker input).
- **Store revocation state** for logout and compromise; do not put secrets or PII in payloads.
- **Rotate keys** with `kid` versioning; monitor for signature failures and algorithm anomalies.
- Reference [PortSwigger JWT attacks](https://portswigger.net/web-security/jwt) for test cases to block.

## Methodology

- [ ] Test alg:none and key confusion
- [ ] Brute force weak HMAC secrets
- [ ] Modify claims for privilege escalation
- [ ] Check jku and kid header injection

## Tools

| Tool | Usage |
|------|-------|
| `jwt_tool` | [JWT analysis & attacks](../../TOOLS_GUIDE.md#jwt_tool) |
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |

## Resources

- [PortSwigger JWT](https://portswigger.net/web-security/jwt)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
