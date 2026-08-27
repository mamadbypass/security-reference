# Subdomain Enumeration

Discover subdomains and expand the attack surface.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    A[Root Domain] --> P[Passive Enum]
    A --> B[Brute Force]
    P --> CT[crt.sh / CT logs]
    P --> API[DNS APIs]
    B --> WL[Wordlists]
    CT & API & WL --> R[Resolve with dnsx]
    R --> V[Validate live subs]
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

Subdomain enumeration discovers hostnames under a root domain (`*.target.com`) that expand the attack surface beyond the primary website. Hostnames are found through multiple channels:

- **Certificate Transparency (CT) logs** — Every publicly trusted TLS certificate is logged; services like crt.sh reveal `api`, `staging`, `jenkins`, and regional variants.
- **Passive DNS and search engines** — Historical resolutions and indexed pages expose hosts no longer in active use but still routable.
- **Brute force and permutation** — Tools combine wordlists (`subdomains-top1million`) with the root domain and resolve via high-speed resolvers (`massdns`, `puredns`).
- **Zone transfers and DNS records** — Misconfigured NS servers may AXFR entire zones.

**Wildcard DNS** (`*.target.com → single IP`) complicates enumeration: brute-force hits return false positives unless tools detect wildcard responses and filter them. Each discovered subdomain may host a distinct application, API, admin panel, or cloud service with different security posture.

## Exploitation

1. **Passive sweep** — `subfinder -d target.com -all -o passive.txt` and `amass enum -passive -d target.com` before sending any direct DNS traffic.
2. **CT log mining** — Query crt.sh for `%.target.com` and deduplicate SAN entries.
3. **Brute force with wildcard handling** — `puredns bruteforce wordlist.txt target.com -r resolvers.txt -w resolved.txt` filters wildcard noise.
4. **Permutation scanning** — `gotator` or `alterx` generate `dev-api`, `api-dev`, `api-staging` variants from known subdomains.
5. **Resolve and validate** — `dnsx -l candidates.txt -a -aaaa -cname -resp` confirms live records and follows CNAME chains to cloud providers.
6. **Check for takeovers** — CNAMEs pointing to deprovisioned S3, Azure, GitHub Pages, or Heroku instances are high-severity findings.
7. **Probe each live host** — Pass results to httpx and nuclei; staging subdomains often lack WAF and auth.
8. **Respect scope** — Wildcard `*.target.com` includes all subdomains unless explicitly excluded in program rules.

## Defense & Mitigation

- **Audit all DNS records quarterly**; remove dangling CNAMEs and unused subdomains.
- **Disable zone transfers** (AXFR) on authoritative nameservers except to designated secondaries.
- **Avoid wildcard DNS** where possible; if required, return NXDOMAIN for unprovisioned hosts instead of a catch-all virtual host.
- **Use CAA records** and monitor CT logs to detect unauthorized certificate issuance for your domains.
- **Claim or delete** cloud resources referenced by DNS before decommissioning services (S3, Azure Web Apps, Fastly).
- **Segment environments** — Do not point `staging.target.com` at production data; use separate accounts and credentials.
- **Alert on new subdomains** via automated CT monitoring (e.g., Facebook ct-monitor, Certstream, commercial EASM).

## Pro Tips

Practical advice from real engagements — use these to test faster and report better.

!!! tip "Combine passive sources"
    subfinder + amass + assetfinder + crt.sh — union beats any single tool.

!!! tip "Wildcard handling"
    Use puredns or shuffledns to filter wildcard DNS before httpx.

!!! tip "Permutation attacks"
    altdns or gotator on discovered subs finds `dev-api-v2.target.com`.

!!! tip "Monitor CT logs"
    crt.sh RSS + Slack alert for new certs on in-scope domains.

!!! tip "Validate ownership"
    Never test a subdomain until confirmed in program scope.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Confirm wildcard scope rules and out-of-scope patterns

### Phase 2 — Discovery & Mapping

- [ ] Passive: CT logs, DNS APIs, search engines
- [ ] Active: brute force with curated wordlists
- [ ] Permutation: alter discovered names (dev-, api-, staging-)
- [ ] Resolve and deduplicate results

### Phase 3 — Validation & Testing

- [ ] Validate ownership against scope
- [ ] Check for dangling DNS / takeover candidates
- [ ] Probe HTTP/HTTPS on all discovered subs
- [ ] Flag high-risk names (jenkins, gitlab, vpn)

### Phase 4 — Exploitation & Impact Proof

- [ ] Test subdomain takeover on NXDOMAIN CNAMEs
- [ ] Document new in-scope assets
- [ ] Report out-of-scope discoveries without testing

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification

## Tools

| Tool | Usage |
|------|-------|
| `subfinder` | [Passive subdomain discovery](../../TOOLS_GUIDE.md#subfinder) |
| `amass` | [OSINT & subdomain enum](../../TOOLS_GUIDE.md#amass) |
| `puredns` | [DNS resolver & wildcard filter](https://github.com/d3mondev/puredns) |
| `massdns` | [High-performance DNS stub](https://github.com/blechschmidt/massdns) |
| `dnsx` | [DNS toolkit](../../TOOLS_GUIDE.md#dnsx) |
| `shuffledns` | [Subdomain brute force](https://github.com/projectdiscovery/shuffledns) |

## Resources

- [Certificate Transparency](https://crt.sh/)
- [HackTricks Subdomain Enumeration](https://book.hacktricks.xyz/generic-methodologies-and-resources/external-recon-methodology#subdomain-enumeration)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
