# TLS / SSL Testing

Assess transport layer security configuration.

## How It Works

**TLS** negotiates cipher suites, certificates, and key exchange between client and server. Misconfigurations expose **deprecated protocols** (SSLv3, TLS 1.0/1.1), **weak ciphers** (RC4, 3DES, NULL), **certificate problems** (expired, wrong hostname, weak RSA keys), and **missing features** (HSTS, OCSP stapling).

Termination at load balancers, CDNs, and Kubernetes ingress adds layers where settings may differ from origin servers. Mixed content and TLS downgrades remain relevant on legacy applications.

## Exploitation

1. **Scan**: `testssl.sh target.com` or `sslyze --regular target:443`.
2. **Protocol downgrade**: test SSLv3/TLS1.0 support and POODLE/BEAST relevance.
3. **Cipher audit**: identify NULL, EXPORT, or anonymous suites.
4. **Certificate review**: weak key length, SHA-1 signatures, missing SANs.
5. **HSTS**: check for absent or short `max-age`; test subdomain inclusion.
6. **Renegotiation and compression**: CRIME/BREACH on HTTPS compression.
7. **Internal TLS**: scan management interfaces (Kubernetes API, Elasticsearch).

Document findings per endpoint; CDN-fronted sites may show different configs than origin.

## Defense & Mitigation

- Enforce **TLS 1.2+** (prefer TLS 1.3); disable SSLv2/v3 and TLS 1.0/1.1.
- Use strong cipher suites; prefer ECDHE with AES-GCM or ChaCha20.
- Deploy **HSTS** with `max-age` ≥ one year and `includeSubDomains` where appropriate.
- Automate certificate renewal (Let's Encrypt, ACME) and monitor expiry.
- Enable OCSP stapling; use CA/Browser Forum baseline requirements.
- Align CDN, load balancer, and origin TLS policies; scan continuously with sslyze or Mozilla SSL Config Generator.

## Methodology

- [ ] Scan for weak protocols and ciphers
- [ ] Check certificate validity and chain
- [ ] Test HSTS and certificate pinning
- [ ] Review TLS termination at load balancers

## Tools

| Tool | Usage |
|------|-------|
| `testssl.sh` | [TLS configuration testing](../../TOOLS_GUIDE.md#testsslsh) |
| `sslyze` | [TLS configuration analysis](https://github.com/nabla-c0d3/sslyze) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
