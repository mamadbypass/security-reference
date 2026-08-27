# HTTP Request Smuggling

Desynchronize front-end and back-end HTTP parsers.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    FE[Front-end server] --> BE[Back-end server]
    A[Smuggled request] --> FE
    FE -->|desync| BE
    BE --> HIJACK[Poison next user's request]
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

HTTP request smuggling exploits disagreements between front-end (CDN, load balancer, WAF) and back-end (app server) on message boundaries. Attackers craft ambiguous requests so each parser splits headers/body differently—desynchronizing the connection queue.

Classic variants:

- **CL.TE**: Front-end uses `Content-Length`, back-end uses `Transfer-Encoding: chunked`
- **TE.CL**: Opposite priority
- **TE.TE**: Obfuscated `Transfer-Encoding` headers confuse one parser

When desync occurs, leftover bytes prefix the **next** user's request on a reused connection—hijacking victims' requests or poisoning caches.

HTTP/2 downgrades and HTTP/2-specific smuggling (H2.CL, H2.TE) extend the class to modern stacks when H2 is translated to H1 behind the edge.

## Exploitation

**Detection (timing)**

Send ambiguous CL/TE requests; observe delays or error patterns vs baseline. Burp HTTP Request Smuggler automates probe templates.

**CL.TE smuggle skeleton**

```
POST / HTTP/1.1
Host: target.com
Content-Length: 6
Transfer-Encoding: chunked

0

GPOST /admin HTTP/1.1
Host: target.com
...
```

Front-end forwards one request; back-end reads smuggled prefix as next request start.

**Attack flow**

```
Smuggled bytes on keep-alive connection → prepended to victim request → cache poison / credential hijack / bypass front-end ACL
```

**Impact chains**

- Force victims to hit attacker-controlled URLs (cache or redirect poisoning)
- Access internal admin paths only front-end should block
- Reflect victim headers to attacker via smuggled log endpoints

**Tools**

- Burp Smuggler, `smuggler.py`, `h2csmuggler` for H2 contexts

**Requirements**

- HTTP/1.1 keep-alive between tiers
- Parser differential confirmed—not theoretical on target architecture

## Defense & Mitigation

**Normalize HTTP at edge**

- Re-encode requests at CDN/WAF; terminate ambiguous `Transfer-Encoding`.
- Disable HTTP/2 downgrade unless strictly validated.
- Prefer HTTP/2 end-to-end with strict RFC compliance.

**Back-end hardening**

- Reject requests with both CL and TE.
- Close connections after anomalous parsing instead of recovering.
- Use distinct connection pools; limit keep-alive for untrusted paths.

**Architecture**

- Isolate admin interfaces on separate hostnames without shared front-end connection reuse with public traffic.

**Detection**

- Monitor for malformed TE headers, duplicate Content-Length, abnormal chunk sequences.
- Vendor patches: keep proxies (nginx, Apache, IIS, HAProxy, Cloudflare) updated—many smuggling variants are version-specific.

## Pro Tips

Practical advice from real engagements — use these to test faster and report better.

!!! tip "HTTP/1.1 desync"
    CL.TE vs TE.CL — run Burp smuggler or `python3 smuggler.py`.

!!! tip "HTTP/2 downgrade"
    h2c smuggling when front speaks H2 and back speaks H1.

!!! tip "Poison admin cache"
    Smuggled request can poison next user's response — high impact.

!!! tip "Confirm with timing"
    Desync often shows as delayed or swapped responses — use multiple requests.

!!! tip "Document server pair"
    Report exact CDN + origin versions — smuggling is stack-specific.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Confirm front-end/back-end server pair (CDN + origin, load balancer)

### Phase 2 — Discovery & Mapping

- [ ] Identify CL.TE and TE.CL desync opportunities with Burp smuggler
- [ ] Test HTTP/2 downgrading to H1 smuggling vectors
- [ ] Map timeout and buffer differences between servers
- [ ] Review reverse proxy documentation for known issues

### Phase 3 — Validation & Testing

- [ ] Send ambiguous `Content-Length` vs `Transfer-Encoding` requests
- [ ] Observe desync via response queue poisoning indicators
- [ ] Validate with timing and response-order anomalies
- [ ] Test h2c smuggling if HTTP/2 front-end present

### Phase 4 — Exploitation & Impact Proof

- [ ] Demonstrate request hijacking or cache poisoning via smuggle
- [ ] Capture second request affecting other users (in lab)
- [ ] Document exact server versions and header combinations
- [ ] Avoid sustained poisoning on production

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification
- [ ] Recommend single consistent HTTP parser and disable TE upgrades

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `smuggler` | [HTTP request smuggling](../../TOOLS_GUIDE.md#smuggler) |
| `h2csmuggler` | [H2C smuggling detection](../../TOOLS_GUIDE.md#h2csmuggler) |

## Resources

- [PortSwigger Request Smuggling](https://portswigger.net/web-security/request-smuggling)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
