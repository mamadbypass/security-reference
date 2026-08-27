# Information Disclosure

Find sensitive data exposed through errors, backups, and misconfigurations.

## How It Works

Information disclosure exposes sensitive data through errors, misconfiguration, excessive API responses, and forgotten assets—not always a CVE-class bug but often high impact for attackers doing recon and chaining findings.

Common sources:

- **Verbose errors**: stack traces, SQL errors, internal paths
- **Misconfigured storage**: public S3 buckets, directory listing enabled
- **Source/repo leaks**: `.git/`, `.env`, backup files (`backup.zip`, `.sql`)
- **Metadata**: `X-Powered-By`, internal IPs in headers, comments with credentials
- **API over-fetching**: returning full user objects including PII fields
- **Client bundles**: API keys, internal URLs, feature flags in minified JS

Attackers combine small disclosures (employee names, schema hints) into larger exploits (password reset, SQLi, social engineering).

## Exploitation

**Recon pipeline**

```bash
# Historical URLs and backups
gau target.com | grep -E '\.(sql|zip|env|bak|config)$'
ffuf -u https://target.com/FUZZ -w sensitive-files.txt

# Secrets in repos and JS
trufflehog git https://github.com/org/repo
linkfinder -i bundle.js -o api-endpoints.txt
```

**Error triggering**

- Invalid IDs, type confusion (`id=abc`), missing headers—capture stack traces.
- Compare error verbosity across environments (staging more leaky).

**Attack flow**

```
Disclosure source → attacker collects credentials/schema/paths → enables targeted exploit or direct credential use
```

**Cloud checks**

- Enumerate bucket names `target-backup`, `target-dev`
- Search certificate transparency for hidden subdomains leaking internal names

**API review**

- Diff responses for `GET /users/me` vs admin; note fields like `ssn`, `internalNotes`.

## Defense & Mitigation

**Error handling**

- Generic client messages; detailed logs server-side only.
- Disable debug mode in production (`DEBUG=False`).

**Configuration**

- Block web access to `.git`, `.env`, IDE folders at server/CDN.
- Disable directory listing; audit cloud bucket ACLs continuously.

**Data minimization**

- API field allow-lists per role; GraphQL max depth and field auth.
- Remove secrets from client bundles; use backend proxies for third-party APIs.

**Headers**

- Strip `X-Powered-By`, server version headers at proxy.

**Monitoring**

- DAST for sensitive paths; GitHub secret scanning; cloud CSPM (Prowler, ScoutSuite).

**Process**

- Rotate any credential ever committed; treat disclosure as incident.

## Methodology

- [ ] Trigger verbose error messages
- [ ] Check /.git, /.env, backup files
- [ ] Review API responses for excessive data
- [ ] Search JS bundles for secrets and endpoints

## Tools

| Tool | Usage |
|------|-------|
| `trufflehog` | [Secret scanner](../../TOOLS_GUIDE.md#trufflehog) |
| `gitleaks` | [Git secret scanner](../../TOOLS_GUIDE.md#gitleaks) |
| `nuclei` | [Template-based vuln scanner](../../TOOLS_GUIDE.md#nuclei) |
| `linkfinder` | [JS endpoint discovery](../../TOOLS_GUIDE.md#linkfinder) |

## Resources

- [OWASP Information Exposure](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/05-Testing_for_Information_Disclosure)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
