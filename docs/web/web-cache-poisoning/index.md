# Web Cache Poisoning

Poison shared caches to serve malicious content.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    A[Attacker] -->|unkeyed header/param| CACHE[CDN cache]
    CACHE --> STORE[Stores poisoned response]
    STORE --> VICTIM[All users get XSS/redirect]
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff

```

</div>

### Testing Workflow

<div class="sr-diagram sr-diagram-methodology" markdown="1">

```mermaid
flowchart LR
    P1["1. Preparation & Scoping"]
    P2["2. Discovery & Mapping"]
    P3["3. Validation & Testing"]
    P4["4. Exploitation & Impact Proof"]
    P5["5. Documentation & Reporting"]
    P1 --> P2 --> P3 --> P4 --> P5
```

</div>

## How It Works

Web cache poisoning stores a malicious response in a shared cache (CDN, reverse proxy) so subsequent users receive attacker-controlled content from the cache key the poisoner triggered.

Caches key responses on URL path, host, and selected headers—but often **ignore** unkeyed inputs:

- `X-Forwarded-Host`, `X-Original-URL`, `X-Rewrite-URL`
- `Accept-Language`, `Accept-Encoding` (fat GET)
- Query parameters stripped by cache but processed by app

If the application reflects an unkeyed header in HTML (e.g., in `<link href="...">` built from `X-Forwarded-Host`), attacker poisons cache entry for a popular URL with XSS or malicious script include.

**Cache deception** (related): trick cache into storing private responses under public URLs using path confusion (`/static/app.js/..%2fprofile`).

## Exploitation

**Find unkeyed inputs**

- Param Miner (Burp) identifies headers/parameters not in cache key but affecting response.
- Compare responses with varied `X-Forwarded-Host` values.

**Poisoning POC**

```http
GET /popular-page HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com
```

If response body includes `https://evil.com/...` and `Cache-Control` allows caching, verify with cache buster then clean request from another IP:

```http
GET /popular-page HTTP/1.1
Host: target.com
```

Victim receives poisoned body from edge cache.

**Attack flow**

```
Attacker sends crafted request → origin reflects unkeyed input → cache stores malicious response → victims load poisoned page from CDN
```

**Impact**

- Mass XSS without per-victim targeting
- Phishing content on legitimate domain
- SEO spam injection

**Tools**

- Web Cache Vulnerability Scanner, Burp Param Miner

## Defense & Mitigation

**Cache design**

- Key on all inputs that affect response body and `Vary` headers appropriately.
- Do not reflect host/header values without validation; use configured canonical hostnames.

**Caching policy**

- `Cache-Control: private` or `no-store` on dynamic and authenticated pages.
- Separate cache partitions for authenticated vs anonymous content.

**Header hygiene**

- Strip or overwrite `X-Forwarded-*` at trusted edge only; ignore client-supplied values on origin.
- Normalize URLs at single tier.

**Testing**

- Regular cache poisoning assessments on CDN config + app behavior.
- Monitor cache HIT responses for unexpected external domains in HTML.

**WAF/CDN features**

- Some providers offer cache poisoning protection rules—enable and tune.

## Pro Tips

Practical advice from real engagements — use these to test faster and report better.

!!! tip "Param Miner extension"
    Burp Param Miner finds unkeyed headers automatically.

!!! tip "Fat GET requests"
    Some caches key on URL only — poison via unkeyed header on GET.

!!! tip "X-Forwarded-Host"
    Classic cache poison header — reflect into HTML links.

!!! tip "Verify with cache buster"
    Confirm poison without `cb=` param affects other users.

!!! warning "Purge after test"
    Clear CDN cache or wait TTL after PoC to avoid harming users.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Identify CDN/cache in front of dynamic content

### Phase 2 — Discovery & Mapping

- [ ] Find unkeyed headers and parameters with Param Miner
- [ ] Test `X-Forwarded-Host`, `X-Original-URL`, custom headers
- [ ] Map cacheable responses containing user input reflection
- [ ] Review cache key configuration if accessible

### Phase 3 — Validation & Testing

- [ ] Inject reflected XSS or redirect via unkeyed input
- [ ] Confirm poisoned response served to other users
- [ ] Test fat GET, parameter cloaking, and key normalization
- [ ] Validate with cache buster param for victim simulation

### Phase 4 — Exploitation & Impact Proof

- [ ] Demonstrate stored poison affecting multiple clients
- [ ] Show XSS or open redirect served from cache
- [ ] Document cache TTL and purge behavior
- [ ] Purge poison after test if possible

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification
- [ ] Include unkeyed inputs in cache key or disable caching on dynamic routes

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `param-miner` | [Hidden parameter discovery](../../TOOLS_GUIDE.md#param-miner) |
| `web-cache-vulnerability-scanner` | [Cache poisoning scanner](../../TOOLS_GUIDE.md#web-cache-vulnerability-scanner) |

## Resources

- [PortSwigger Web Cache Poisoning](https://portswigger.net/web-security/web-cache-poisoning)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
