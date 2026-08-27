# API Versioning Issues

Find deprecated API versions with weaker security controls.

## How It Works

APIs evolve through versioned paths (`/v1/`, `/v2/`), headers (`Accept-Version`, `X-Api-Version`), query parameters, or separate hostnames (`api-old.example.com`). Teams frequently ship stricter auth, input validation, and rate limiting on new versions while **legacy versions remain online** for mobile apps, partners, or internal tools.

This creates a **version skew** vulnerability class (related to OWASP API #9 Improper Inventory Management): attackers target deprecated endpoints that still accept weak API keys, lack MFA checks, expose verbose errors, or skip object-level authorization added only in newer code paths.

## Exploitation

1. **Enumerate versions** — Fuzz `/v1`, `/v2`, `/v3`, `/beta`, `/internal`, `/mobile`, `/legacy`, and date-stamped paths (`/2023-01/`).
2. **Compare OpenAPI/Swagger** — Diff `/swagger/v1/swagger.json` vs `/v2/` for removed auth requirements or extra endpoints.
3. **Replay attacks across versions** — Take a blocked IDOR or auth bypass payload from `/v2/users/123` and retry on `/v1/users/123`.
4. **Inspect mobile apps** — Hardcoded base URLs often point at older API versions with weaker controls.
5. **Check version headers** — Send `X-Api-Version: 1` on routes that default to v2 behavior.
6. **Hunt debug builds** — `/v1/debug`, `/v2/test`, and feature-flagged routes may exist only in specific versions.
7. **Document differential behavior** — Show the same token or none at all succeeding only on the legacy path.

## Defense & Mitigation

- **Maintain an authoritative API inventory** with owner, auth model, and sunset date for every version.
- **Deprecate aggressively**: return `Sunset` headers, monitor traffic, then decommission old versions on a fixed timeline.
- **Backport critical security fixes** to all supported versions or force client upgrades.
- **Apply consistent authorization middleware** shared across versions, not copy-pasted per router.
- **Block internet access** to internal/beta versions; require VPN or mTLS.
- **Automate contract tests** so new security controls cannot ship only in the latest route tree.

## Methodology

- [ ] Discover /v1, /v2, /beta, /internal paths
- [ ] Compare auth requirements across versions
- [ ] Test legacy mobile API backends
- [ ] Check unauthenticated debug versions

## Tools

| Tool | Usage |
|------|-------|
| `ffuf` | See [Tools Guide](/TOOLS_GUIDE/) |
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |
| `kiterunner` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [OWASP API Security Top 10](https://owasp.org/API-Security/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
