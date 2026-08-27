# Security Reference

[![Deploy](https://github.com/mamadbypass/security-reference/actions/workflows/deploy.yml/badge.svg)](https://github.com/mamadbypass/security-reference/actions/workflows/deploy.yml)
[![Site](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://mamadbypass.github.io/security-reference/)

A comprehensive, searchable knowledge base for **bug bounty hunting**, **penetration testing**, and **defensive security** — built with MkDocs Material and deployed to GitHub Pages.

**Live site:** https://mamadbypass.github.io/security-reference/

## What's Inside

- **95+ topic pages** across 22 security domains
- **[Master Checklist](docs/MASTER_CHECKLIST.md)** — 100+ engagement checklist items
- **[Tools Index](docs/TOOLS_INDEX.md)** — 40+ tools organized by category
- Links to [PortSwigger](https://portswigger.net/web-security), [OWASP](https://cheatsheetseries.owasp.org/), [HackTricks](https://book.hacktricks.xyz/), [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings), and [MITRE ATT&CK](https://attack.mitre.org/)

### Sections

| Category | Topics |
|----------|--------|
| Bug Bounty | Recon, subdomain enum, port scanning, DNS, tech detection |
| Web Security | SQLi, XSS, SSRF, smuggling, cache poisoning, business logic |
| API | GraphQL, versioning, shadow APIs, gRPC |
| Authentication | JWT, SSO/SAML, password reset, WebAuthn |
| Mobile | APK analysis, Frida, SSL pinning, deep links |
| Network | Active Directory, BloodHound, privesc, lateral movement |
| Blue Team | Detection engineering, SIEM, threat hunting, IR |
| Cloud | AWS, Azure, GCP, Kubernetes |
| + more | Crypto, containers, DevSecOps, binary, OSINT, IoT, Web3, forensics |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Serve locally
mkdocs serve

# Build static site
mkdocs build --strict
```

Open http://127.0.0.1:8000 to browse the site locally.

See [SETUP.md](SETUP.md) for detailed setup and deployment instructions.

## Deployment

The site auto-deploys to GitHub Pages on every push to `main` via GitHub Actions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add or improve content in `docs/`
4. Run `mkdocs build --strict` to verify
5. Submit a pull request

## License

Content is provided for educational and authorized security testing purposes only. Always obtain proper authorization before testing any system.

## Disclaimer

This project is for educational purposes. The authors are not responsible for misuse. Follow all applicable laws and program rules of engagement.
