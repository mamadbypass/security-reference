# Getting Started

This guide walks you through setting up your security testing lab, installing essential tools, and using this reference effectively.

## Who Is This For?

| Role | Start With |
|------|------------|
| Bug bounty beginner | [Workflows → Bug Bounty Day 1](WORKFLOWS.md#bug-bounty-day-1) |
| Web app pentester | [Web Security](web/sqli/index.md) + [Tools Guide](TOOLS_GUIDE.md) |
| API tester | [API Security](api/graphql/index.md) |
| Mobile researcher | [Mobile Security](mobile/apk-ipa-analysis/index.md) |
| AD / internal pentest | [Network & AD](network/active-directory/index.md) |
| Blue team analyst | [Blue Team](blue-team/detection-engineering/index.md) |

---

## Lab Setup

### Recommended Environment

=== "Linux (Kali / Parrot)"

    ```bash
    # Update system
    sudo apt update && sudo apt upgrade -y

    # Essential packages
    sudo apt install -y git curl wget jq python3-pip golang-go

    # Go tools path
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
    source ~/.bashrc
    ```

=== "macOS"

    ```bash
    # Install Homebrew if needed
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    brew install go python3 jq git
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.zshrc
  ```

=== "Windows (WSL2)"

    ```powershell
    # Install WSL2 + Ubuntu from Microsoft Store, then inside WSL:
    sudo apt update && sudo apt install -y git curl python3-pip golang-go
    ```

### Install ProjectDiscovery Toolkit

Most recon tools come from [ProjectDiscovery](https://projectdiscovery.io/). Install via Go:

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# Update nuclei templates
nuclei -update-templates
```

### Install Core Web Testing Tools

```bash
# Python tools
pip install sqlmap commix

# ffuf (fuzzer)
go install github.com/ffuf/ffuf/v2@latest

# Secret scanning
pip install trufflehog
# or: brew install gitleaks
```

### Burp Suite Setup

1. Download [Burp Suite Community](https://portswigger.net/burp/communitydownload)
2. Configure browser proxy → `127.0.0.1:8080`
3. Install Burp CA certificate in your browser
4. Enable extensions: **Autorize**, **JWT Editor**, **Param Miner**, **Turbo Intruder**

!!! tip "Pro Tip"
    Create a dedicated browser profile for testing with the Burp proxy configured. Never use your personal browser profile.

---

## How to Use This Reference

### 1. Search First

Use the **search bar** (top of page) to find techniques, tools, or payloads instantly.

```
Examples: "kerberoasting", "graphql introspection", "ssrf metadata"
```

### 2. Follow a Workflow

For structured testing, start with [Workflows](WORKFLOWS.md):

- **Bug Bounty Day 1** — full recon pipeline
- **Web App Assessment** — OWASP Top 10 testing flow
- **API Testing** — REST and GraphQL methodology
- **Active Directory** — internal network attack path

### 3. Use the Tools Guide

Each tool in [Tools Guide](TOOLS_GUIDE.md) includes:

- Installation command
- Basic usage with real examples
- Common flags and options
- Output interpretation tips
- When to use it in a workflow

### 4. Topic Pages

Every vulnerability page follows this structure:

| Section | Purpose |
|---------|---------|
| **Methodology** | Step-by-step testing approach |
| **Tools** | Recommended tools for this vuln |
| **Commands** | Copy-paste ready examples |
| **Resources** | External learning links |
| **Checklist** | Final verification before reporting |

### 5. Master Checklist

Before submitting a report, run through the [Master Checklist](MASTER_CHECKLIST.md) to ensure nothing was missed.

---

## Essential Tool Categories

| Category | Primary Tools | Guide Section |
|----------|--------------|---------------|
| Recon | subfinder, httpx, nuclei | [Recon Tools](TOOLS_GUIDE.md#reconnaissance) |
| Web proxy | Burp Suite, OWASP ZAP | [Web Tools](TOOLS_GUIDE.md#web-application) |
| Fuzzing | ffuf, wfuzz | [Web Tools](TOOLS_GUIDE.md#ffuf) |
| SQLi | sqlmap, ghauri | [Web Tools](TOOLS_GUIDE.md#sqlmap) |
| Secrets | trufflehog, gitleaks | [Secrets Tools](TOOLS_GUIDE.md) |
| AD | BloodHound, Impacket | [Network Tools](TOOLS_GUIDE.md) |
| Cloud | Prowler, Pacu | [Cloud Tools](TOOLS_GUIDE.md#cloud) |
| Mobile | jadx, Frida, objection | [Mobile Tools](TOOLS_GUIDE.md#mobile) |

---

## File Organization Tips

Keep your engagement organized:

```
engagement/
├── scope.txt          # In-scope domains/IPs
├── subdomains.txt     # Discovered subdomains
├── live-hosts.txt     # HTTP 200/301/302 hosts
├── urls.txt           # Crawled URLs
├── findings/          # One folder per vulnerability
│   ├── sqli-login/
│   │   ├── poc.py
│   │   ├── screenshot.png
│   │   └── notes.md
└── reports/           # Final writeups
```

---

## Reporting Basics

When you find a vulnerability:

1. **Title** — Clear, specific (e.g., "SQL Injection in `/api/search?q=` parameter")
2. **Severity** — Use CVSS or program matrix
3. **Steps** — Numbered reproduction steps
4. **Impact** — What an attacker can achieve
5. **PoC** — Minimal proof (screenshot, curl command, HTTP request)
6. **Remediation** — Specific fix recommendation

See [Vulnerability Reporting](reporting/vulnerability-reports/index.md) for the full template.

---

## Next Steps

<div class="sr-grid">

<a class="sr-card" href="TOOLS_GUIDE/">
<span class="sr-card-icon" aria-hidden="true">🛠</span>
<span class="sr-card-title">Install &amp; Learn Tools</span>
<span class="sr-card-text">Step-by-step commands for every major security tool.</span>
</a>

<a class="sr-card" href="WORKFLOWS/">
<span class="sr-card-icon" aria-hidden="true">⚡</span>
<span class="sr-card-title">Run Your First Workflow</span>
<span class="sr-card-text">Complete recon-to-report pipelines ready to copy.</span>
</a>

<a class="sr-card" href="bug-bounty/recon/">
<span class="sr-card-icon" aria-hidden="true">🔍</span>
<span class="sr-card-title">Start Recon</span>
<span class="sr-card-text">Begin with subdomain enumeration and asset discovery.</span>
</a>

</div>
