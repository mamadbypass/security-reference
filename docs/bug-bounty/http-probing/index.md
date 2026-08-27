# HTTP Probing

Identify live web services, technologies, and response behaviors.

## How It Works

HTTP probing determines which discovered hosts serve **live web applications** and collects metadata for prioritization: HTTP status codes, page titles, redirect chains, TLS certificates, response sizes, and technology fingerprints.

A host may resolve in DNS but return no web service; probing filters the asset list to actionable targets. Probers send HTTP/HTTPS requests (often HEAD or GET) and parse responses in parallel across thousands of hosts.

Key signals:

- **Status codes** — 200 (live app), 401/403 (auth required—interesting), 302 (redirect chains reveal internal hostnames).
- **Titles** — `Login`, `Dashboard`, `phpMyAdmin`, `Index of /` indicate high-value targets.
- **TLS cert SANs** — Certificate subject alternative names reveal additional hostnames for recursive enumeration.
- **CDN/WAF presence** — Cloudflare, Akamai, and AWS CloudFront headers affect which tests will succeed.

Tools like `httpx` integrate probing with tech detection, screenshotting, and favicon hashing for efficient pipeline stages.

## Exploitation

1. **Probe all resolved hosts** — `httpx -l hosts.txt -title -status-code -tech-detect -follow-redirects -threads 50 -o live.txt`.
2. **Test both HTTP and HTTPS** — Some apps only respond on one scheme; use `-ports 80,443,8080,8443`.
3. **Capture redirect chains** — `-follow-redirects` reveals `staging.internal` hostnames in Location headers.
4. **Hash favicons** — `httpx -favicon` matches default admin panel icons (Shodan favicon hash database).
5. **Screenshot for triage** — `gowitness` or `aquatone` visualizes hundreds of hosts for quick manual review.
6. **Filter by status** — Prioritize 200/401/403; investigate 502/503 for backend misconfigurations.
7. **Extract TLS SANs** — `httpx -tls-probe -json` feeds new subdomains back into enumeration.
8. **Build target tiers** — Tier 1: login pages and APIs; Tier 2: static sites; Tier 3: error pages worth content discovery.

## Defense & Mitigation

- **Remove or protect unused virtual hosts** — Default nginx/Apache pages on forgotten vhosts are common low-hanging fruit.
- **Normalize redirects** — Avoid leaking internal hostnames in Location headers.
- **Require authentication** on staging and admin interfaces; do not rely on obscurity.
- **Deploy WAF/CDN** consistently across all public vhosts, not only the main site.
- **Monitor for new live hosts** — Alert when httpx-equivalent scans would find new 200 responses on your IP space.
- **Use consistent TLS certificates** — Minimize SAN sprawl that expands attacker subdomain lists.
- **Return generic error pages** — Avoid verbose server banners and stack traces on probed endpoints.

## Methodology

- [ ] Probe HTTP/HTTPS on discovered hosts
- [ ] Capture status codes, titles, and redirects
- [ ] Detect WAF and CDN behavior
- [ ] Build a prioritized target list

## Tools

| Tool | Usage |
|------|-------|
| `httpx` | See [Tools Guide](/TOOLS_GUIDE/) |
| `httprobe` | See [Tools Guide](/TOOLS_GUIDE/) |
| `aquatone` | See [Tools Guide](/TOOLS_GUIDE/) |
| `gowitness` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [ProjectDiscovery httpx](https://github.com/projectdiscovery/httpx)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
