# Server-Side Request Forgery (SSRF)

Force server-side requests to internal and cloud metadata endpoints.

## How It Works

Server-Side Request Forgery (SSRF) abuses server-side functionality that fetches or connects to URLs supplied by users. The attacker's goal is to make the **server** request resources the attacker cannot reach directly—internal services, cloud metadata endpoints, or restricted admin interfaces.

Typical features at risk:

- Image/document import from URL
- Webhook URL configuration
- PDF generators fetching HTML
- Link preview/unfurl
- SSO or OIDC discovery URL fetch
- Server-side crawlers and health checks

Cloud metadata is a classic target:

- AWS: `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
- GCP/Azure: similar link-local metadata services

The server often sits inside a trust boundary with access to internal APIs (`http://127.0.0.1:8080/admin`), Redis, Elasticsearch, or Kubernetes API—none of which should be exposed to the internet.

## Exploitation

**Discovery**

1. Find parameters accepting URLs: `url`, `src`, `redirect`, `callback`, `feed`, `path`.
2. Submit `http://your-collaborator.burpcollaborator.net` and observe DNS/HTTP callbacks.
3. Probe internal hosts: `http://127.0.0.1`, `http://10.0.0.1`, `http://192.168.1.1`.

**Bypass filters**

- Alternative IP representations: `2130706433` (decimal), `0x7f000001`, `127.1`
- DNS rebinding: domain resolves to public IP first, then internal
- Redirect chains: attacker URL redirects to `http://169.254.169.254/`
- URL schemes: `file:///etc/passwd`, `gopher://`, `dict://` (when supported)

**Attack flow**

```
Attacker supplies URL → server fetches it → internal/metadata response returned or used server-side → credential theft / port scan / RCE via internal admin
```

**Cloud credential theft**

```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
```

**Escalation**

- Scan internal ports via response timing or error messages
- Hit Redis `http://127.0.0.1:6379` with crafted paths (protocol smuggling contexts)
- Chain with XXE or deserialization on internal services only reachable from the app server

## Defense & Mitigation

**Network controls**

- Deny egress from application servers to link-local and internal ranges except explicitly required destinations.
- Use metadata service v2 (IMDSv2 on AWS) requiring session tokens and hop limits.

**Application controls**

- Allow-list destinations (specific partner domains) instead of block-lists.
- Resolve hostnames and validate resolved IP is not private/link-local before connecting.
- Disable redirects or re-validate each hop in a redirect chain.
- Strip or ignore dangerous URL schemes; use `https` only where possible.

**Architecture**

- Separate fetch workers in isolated network segments with no cloud metadata access.
- Do not return raw internal responses to users; summarize or proxy through strict parsers.

**Monitoring**

- Alert on requests to metadata IPs, `localhost`, and RFC1918 ranges from app tiers.

## Methodology

- [ ] Find URL import, webhook, and preview features
- [ ] Probe localhost and cloud metadata IPs
- [ ] Use DNS rebinding and redirect chains
- [ ] Escalate to internal service access

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `ssrfmap` | [SSRF exploitation](../../TOOLS_GUIDE.md#ssrfmap) |
| `interactsh` | [Out-of-band interaction server](../../TOOLS_GUIDE.md#interactsh) |

## Resources

- [PortSwigger SSRF](https://portswigger.net/web-security/ssrf)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
