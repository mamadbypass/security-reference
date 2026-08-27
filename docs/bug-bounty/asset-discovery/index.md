# Asset Discovery

Map all in-scope assets including APIs, mobile backends, and cloud resources.

## How It Works

Asset discovery goes beyond subdomain lists to build a **complete map of in-scope resources**: web applications, APIs, mobile backends, cloud storage, IP ranges, ASN allocations, and third-party integrations.

Modern organizations expose assets across:

- **Corporate DNS** — Primary domains and acquired company brands.
- **Cloud providers** — S3 buckets, Azure blobs, GCP storage named after the company (`target-backups`, `target-dev`).
- **IP/ASN space** — Netblocks registered to the organization may host services not linked from public DNS.
- **Mobile and desktop apps** — Hardcoded API endpoints, analytics SDKs, and certificate pinning configs reveal hidden backends.
- **Code and artifact leaks** — GitHub, GitLab, npm packages, and Docker Hub images expose internal hostnames and API keys.

Attackers correlate these sources to find **forgotten properties**—acquired startups, deprecated products, and employee side projects still on corporate infrastructure.

## Exploitation

1. **Map ASN and IP ranges** — `asnmap -d target.com` and `mapcidr` to find netblocks; scan for web services not in DNS.
2. **Hunt cloud storage** — Probe `target-dev.s3.amazonaws.com`, permutations with `cloud_enum`, `s3scanner`, or nuclei S3 templates.
3. **Search code repositories** — GitHub dorks: `org:target password`, `target.com api_key`, `.env target`.
4. **Analyze mobile apps** — Decompile APK/IPA with `jadx`; extract API base URLs, staging hosts, and embedded secrets.
5. **Review acquisitions** — Enumerate domains owned by subsidiaries listed in annual reports or press releases.
6. **Crawl for assets** — `katana -u https://target.com -d 5` discovers linked domains, CDN origins, and third-party widgets.
7. **Cross-reference Shodan/Censys** — Search `ssl.cert.subject.cn:target.com` and `org:"Target Corp"` for unlisted services.
8. **Validate ownership** — Confirm each asset is in program scope before testing; document provenance for reports.

## Defense & Mitigation

- **Maintain a living asset register** tied to business owners, environment type, and decommission dates.
- **Integrate M&A due diligence** — Transfer or retire DNS, certs, and cloud accounts when acquiring companies.
- **Block public listing** of dev/staging buckets and storage; use private ACLs and IAM policies by default.
- **Scan code repositories** for secrets and internal hostnames; use `gitleaks` in CI and GitHub Advanced Security.
- **Inventory mobile app endpoints** and ensure they route through the same WAF and auth controls as web.
- **Deploy EASM** that correlates DNS, IPs, cloud APIs, and code leaks into one dashboard.
- **Run quarterly "forgotten asset" reviews** with security and infrastructure teams.

## Methodology

- [ ] Correlate subdomains with ASN and IP ranges
- [ ] Identify staging, dev, and legacy environments
- [ ] Check acquisition domains and forgotten properties
- [ ] Validate ownership against program scope

## Tools

| Tool | Usage |
|------|-------|
| `asnmap` | See [Tools Guide](/TOOLS_GUIDE/) |
| `mapcidr` | See [Tools Guide](/TOOLS_GUIDE/) |
| `naabu` | See [Tools Guide](/TOOLS_GUIDE/) |
| `httpx` | See [Tools Guide](/TOOLS_GUIDE/) |
| `katana` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [ProjectDiscovery Tools](https://projectdiscovery.io/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
