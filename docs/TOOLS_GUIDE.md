# Tools Guide

Complete install, usage, and pro tips for every major security tool. Copy commands directly into your terminal.

!!! info "Quick Navigation"
    Use the table of contents on the right, or search for a tool name with `Ctrl+K`.

---

## Reconnaissance

### subfinder

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Passive Recon</span><span class="tool-tag">Subdomains</span></div>

**Install**

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Basic Usage**

```bash
# Single domain
subfinder -d target.com

# All sources, save to file
subfinder -d target.com -all -o subs.txt

# Multiple domains
subfinder -dL domains.txt -o all_subs.txt
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `-all` | Use all sources (slower, more results) |
| `-recursive` | Recursive subdomain discovery |
| `-silent` | Show only subdomains in output |
| `-config` | Path to provider config (API keys) |

**Pro Tips**

- Add API keys in `~/.config/subfinder/provider-config.yaml` for more sources (Shodan, Censys, VirusTotal)
- Pipe to `httpx` for instant live host check: `subfinder -d target.com -silent | httpx`

</div>

### httpx

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">HTTP Probe</span><span class="tool-tag">Tech Detection</span></div>

**Install**

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

**Basic Usage**

```bash
# Probe a list of hosts
httpx -l subs.txt -title -status-code -tech-detect

# Single URL with full info
httpx -u https://target.com -title -status-code -content-length -tech-detect -follow-redirects

# Save live hosts only
httpx -l subs.txt -mc 200,301,302,403 -o live.txt
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `-title` | Extract page title |
| `-status-code` | Show HTTP status code |
| `-tech-detect` | Detect technologies (Wappalyzer) |
| `-follow-redirects` | Follow HTTP redirects |
| `-mc 200` | Match status code filter |
| `-screenshot` | Take screenshots (requires headless browser) |
| `-json` | JSON output for parsing |

**Pro Tips**

```bash
# Full recon one-liner
subfinder -d target.com -silent | httpx -title -status-code -tech-detect -o live.txt
```

</div>

### nuclei

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Vulnerability Scanner</span><span class="tool-tag">Templates</span></div>

**Install**

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates   # Always run after install
```

**Basic Usage**

```bash
# Scan single URL
nuclei -u https://target.com

# Scan list of hosts
nuclei -l live_hosts.txt -o results.txt

# Specific template categories
nuclei -l hosts.txt -t cves/ -t exposures/ -t misconfiguration/

# Scan with severity filter
nuclei -l hosts.txt -severity critical,high -o critical.txt
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `-t` | Template path or tag |
| `-tags` | Run templates with specific tags |
| `-severity` | Filter by severity |
| `-rate-limit` | Requests per second (default 150) |
| `-H` | Custom header (e.g., `-H "Authorization: Bearer TOKEN"`) |
| `-jsonl` | JSON lines output |

**Pro Tips**

```bash
# Update templates weekly
nuclei -update-templates

# Custom template
nuclei -u https://target.com -t ./my-templates/

# With auth header for authenticated scan
nuclei -l hosts.txt -H "Cookie: session=abc123" -t exposures/
```

</div>

### naabu

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Port Scanner</span><span class="tool-tag">Fast</span></div>

**Install**

```bash
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

**Basic Usage**

```bash
# Top 1000 ports on a host
naabu -host target.com -top-ports 1000

# Scan IP range
naabu -host 10.10.10.0/24 -p 22,80,443,3389,8080

# From subdomain list
naabu -list subs.txt -top-ports 100 -o ports.txt
```

</div>

### gau

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">URL Archive</span><span class="tool-tag">Passive</span></div>

**Install**

```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

**Basic Usage**

```bash
# Get all archived URLs for a domain
gau target.com | sort -u > urls.txt

# Include subdomains
gau --subs target.com > urls.txt

# Filter by extension
gau target.com | grep -E '\.(js|json|xml)$' > interesting.txt
```

</div>

### katana

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Web Crawler</span><span class="tool-tag">JS Parsing</span></div>

**Install**

```bash
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

**Basic Usage**

```bash
# Crawl a site (depth 3)
katana -u https://target.com -d 3 -o crawl.txt

# Parse JavaScript files for endpoints
katana -u https://target.com -d 3 -jc -kf

# Crawl from URL list
katana -list live_hosts.txt -d 2 -o all_urls.txt
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `-jc` | Parse JavaScript files |
| `-kf` | Keep form URLs |
| `-d` | Crawl depth |
| `-H` | Custom headers for auth |

</div>

---

## Web Application

### Burp Suite

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Proxy</span><span class="tool-tag">Essential</span></div>

**Setup**

1. Download from [portswigger.net](https://portswigger.net/burp/communitydownload)
2. Proxy → Options → `127.0.0.1:8080`
3. Browser proxy → Burp
4. Visit `http://burp` → Download CA certificate

**Key Features**

| Feature | Use Case |
|---------|----------|
| **Repeater** | Modify and resend individual requests |
| **Intruder** | Fuzz parameters, brute force |
| **Scanner** | Automated vulnerability detection (Pro) |
| **Turbo Intruder** | Race conditions, high-speed attacks |
| **Comparer** | Diff two responses |
| **Decoder** | Encode/decode Base64, URL, HTML |

**Essential Extensions**

```
Autorize      — IDOR / auth bypass testing
JWT Editor    — JWT manipulation
Param Miner   — Hidden parameter discovery
Logger++      — Advanced logging
Turbo Intruder — Race conditions
```

**Pro Tips**

```bash
# Export requests from command line tools to Burp
# In Burp: Project options → Misc → "Allow external tools to launch Burp"
```

</div>

### ffuf

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Fuzzer</span><span class="tool-tag">Directory Brute</span></div>

**Install**

```bash
go install github.com/ffuf/ffuf/v2@latest
```

**Basic Usage**

```bash
# Directory fuzzing
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302,403

# Parameter fuzzing
ffuf -u https://target.com/search?FUZZ=test -w params.txt -mc 200

# Subdomain fuzzing
ffuf -u https://FUZZ.target.com -w subdomains.txt -mc 200

# POST data fuzzing
ffuf -u https://target.com/login -X POST -d "username=admin&password=FUZZ" -w passwords.txt
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `-mc` | Match HTTP status codes |
| `-fc` | Filter status codes |
| `-fs` | Filter by response size |
| `-fr` | Filter by regex |
| `-t` | Threads (default 40) |
| `-rate` | Requests per second |

**Pro Tips**

```bash
# Filter out common false positives by size
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200 -fs 1234

# Recursive directory fuzzing
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 2
```

</div>

### sqlmap

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">SQL Injection</span><span class="tool-tag">Automated</span></div>

**Install**

```bash
pip install sqlmap
# or: git clone https://github.com/sqlmapproject/sqlmap.git
```

**Basic Usage**

```bash
# Test URL parameter
sqlmap -u "https://target.com/product?id=1" --batch

# From Burp request file
sqlmap -r request.txt --batch

# Enumerate databases
sqlmap -u "https://target.com?id=1" --dbs --batch

# Dump specific table
sqlmap -u "https://target.com?id=1" -D dbname -T users --dump --batch

# POST request
sqlmap -u "https://target.com/login" --data="user=admin&pass=test" --batch
```

**Useful Flags**

| Flag | Description |
|------|-------------|
| `--batch` | Never ask for user input |
| `--level=3` | Test level 1-5 (higher = more tests) |
| `--risk=2` | Risk level 1-3 |
| `--tamper=space2comment` | Use tamper scripts for WAF bypass |
| `--cookie="session=abc"` | Authenticated testing |
| `--proxy=http://127.0.0.1:8080` | Route through Burp |

**Pro Tips**

```bash
# WAF bypass with tamper scripts
sqlmap -u "URL" --tamper=space2comment,between --random-agent --batch

# Test all parameters
sqlmap -u "URL" --level=5 --risk=3 --batch
```

</div>

### dalfox

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">XSS Scanner</span><span class="tool-tag">Fast</span></div>

**Install**

```bash
go install github.com/hahwul/dalfox/v2@latest
```

**Basic Usage**

```bash
# Single URL
dalfox url "https://target.com/search?q=test"

# From URL list
dalfox file urls.txt -o xss_results.txt

# With custom payload
dalfox url "https://target.com/search?q=test" --custom-payload payloads.txt

# Pipe from other tools
cat urls.txt | dalfox pipe
```

</div>

### jwt_tool

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">JWT</span><span class="tool-tag">Auth Bypass</span></div>

**Install**

```bash
pip install jwt_tool
# or: git clone https://github.com/ticarpi/jwt_tool.git
```

**Basic Usage**

```bash
# Analyze JWT
python3 jwt_tool.py <JWT_TOKEN>

# Crack weak secret
python3 jwt_tool.py <JWT_TOKEN> -C -d /usr/share/wordlists/rockyou.txt

# Tamper algorithm to none
python3 jwt_tool.py <JWT_TOKEN> -X a

# Modify claims
python3 jwt_tool.py <JWT_TOKEN> -I -hc header -hv '{"alg":"HS256","typ":"JWT"}' -pc payload -pv '{"user":"admin","role":"admin"}'
```

</div>

### commix

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Command Injection</span></div>

**Install**

```bash
pip install commix
```

**Basic Usage**

```bash
# Test URL
python commix.py -u "https://target.com/ping?host=127.0.0.1" --batch

# POST data
python commix.py -u "https://target.com/api" --data="cmd=ping" --batch

# From Burp request
python commix.py -r request.txt --batch
```

</div>

---

## API & GraphQL

### kiterunner (kr)

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">API Discovery</span><span class="tool-tag">Brute Force</span></div>

**Install**

```bash
# Download from https://github.com/assetnote/kiterunner/releases
```

**Basic Usage**

```bash
# Scan for API routes
kr scan https://target.com -w routes.kite -o results.txt

# Wordlist scan
kr brute https://target.com -w /path/to/wordlist.txt
```

</div>

### grpcurl

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">gRPC</span><span class="tool-tag">CLI</span></div>

**Install**

```bash
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
```

**Basic Usage**

```bash
# List services (requires reflection)
grpcurl target.com:50051 list

# Describe a service
grpcurl target.com:50051 describe mypackage.MyService

# Call a method
grpcurl -d '{"name": "test"}' target.com:50051 mypackage.MyService/MyMethod
```

</div>

---

## Mobile

### jadx

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Android</span><span class="tool-tag">Decompiler</span></div>

**Install**

```bash
# Download from https://github.com/skylot/jadx/releases
# or: brew install jadx
```

**Basic Usage**

```bash
# Decompile APK to directory
jadx -d output/ app.apk

# GUI mode
jadx-gui app.apk

# Search for strings
grep -ri "api_key\|password\|secret" output/
```

</div>

### Frida & objection

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Dynamic Analysis</span><span class="tool-tag">Runtime</span></div>

**Install**

```bash
pip install frida-tools objection
# Download frida-server matching your device arch from github.com/frida/frida/releases
```

**Basic Usage**

```bash
# Push frida-server to device
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# Objection interactive shell
objection -g com.target.app explore

# Inside objection:
# android sslpinning disable
# android root disable
# memory list modules
# android hooking list activities
```

**Frida Scripts**

```javascript
// ssl_pinning_bypass.js
Java.perform(function() {
    var TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    // ... bypass implementation
});
```

```bash
frida -U -f com.target.app -l ssl_pinning_bypass.js --no-pause
```

</div>

---

## Network & Active Directory

### nmap

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Port Scanner</span><span class="tool-tag">Service Detection</span></div>

**Basic Usage**

```bash
# Quick scan top ports
nmap -sV -sC target.com

# Full port scan
nmap -p- -sV target.com -oA full_scan

# UDP scan
nmap -sU --top-ports 20 target.com

# Network sweep
nmap -sn 10.10.10.0/24

# Vulnerability scripts
nmap --script vuln target.com
```

</div>

### CrackMapExec (netexec)

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">SMB/WinRM</span><span class="tool-tag">Lateral Movement</span></div>

**Install**

```bash
pip install crackmapexec
# New name: pip install netexec
```

**Basic Usage**

```bash
# SMB enumeration
crackmapexec smb 10.10.10.0/24

# Password spray
crackmapexec smb 10.10.10.0/24 -u users.txt -p 'Password123!'

# Pass-the-hash
crackmapexec smb 10.10.10.10 -u administrator -H <NTLM_HASH>

# Execute command
crackmapexec smb 10.10.10.10 -u admin -p password -x "whoami"

# Dump SAM
crackmapexec smb 10.10.10.10 -u admin -p password --sam
```

</div>

### Impacket

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Windows Protocols</span><span class="tool-tag">Essential</span></div>

**Install**

```bash
pip install impacket
# Tools installed to PATH
```

**Key Tools**

```bash
# Kerberoasting
GetUserSPNs.py domain/user:password -dc-ip 10.10.10.10 -request -outputfile hashes.txt

# AS-REP Roasting
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.10.10.10

# Secrets dump (DCSync)
secretsdump.py domain/admin:password@10.10.10.10

# Remote command execution
psexec.py domain/admin:password@10.10.10.10

# SMB share enumeration
smbclient.py domain/user:password@10.10.10.10
```

</div>

### BloodHound

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">AD Graph</span><span class="tool-tag">Attack Paths</span></div>

**Setup**

```bash
# Install BloodHound GUI
# Download from https://github.com/BloodHoundAD/BloodHound/releases

# Collect data (Linux)
pip install bloodhound
bloodhound-python -u user -p 'password' -d domain.local -ns 10.10.10.10 -c All
```

**Usage**

1. Import generated ZIP into BloodHound
2. Click "Analysis" → "Find Shortest Paths to Domain Admins"
3. Review high-value targets and attack paths
4. Check "Kerberoastable Users" and "AS-REP Roastable Users"

</div>

---

## Cloud

### Prowler

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">AWS/Azure/GCP</span><span class="tool-tag">Audit</span></div>

**Install**

```bash
pip install prowler
```

**Basic Usage**

```bash
# AWS audit
prowler aws

# Specific checks
prowler aws --checks s3_bucket_public_access

# Output HTML report
prowler aws -M html html

# Azure
prowler azure --az-account-subscription-id <id>
```

</div>

### Pacu

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">AWS Exploitation</span></div>

**Install**

```bash
git clone https://github.com/RhinoSecurityLabs/pacu.git
cd pacu && bash install.sh
python3 pacu.py
```

**Basic Usage**

```bash
# Inside Pacu shell:
import_keys <access_key> <secret_key>
run iam__enum_users_roles_policies_groups
run s3__enum_buckets
run iam__privesc_scan
run lambda__enum
```

</div>

---

## Secrets & Code

### trufflehog

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Secret Scanner</span></div>

**Install**

```bash
pip install trufflehog
# or: brew install trufflehog
```

**Basic Usage**

```bash
# Scan git repo
trufflehog git https://github.com/org/repo

# Scan filesystem
trufflehog filesystem ./output/

# Scan GitHub org
trufflehog github --org=target-org
```

</div>

### gitleaks

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">Git Secrets</span></div>

**Install**

```bash
brew install gitleaks
# or download from github.com/gitleaks/gitleaks/releases
```

**Basic Usage**

```bash
# Scan current repo
gitleaks detect --source . -v

# Scan commit history
gitleaks detect --source . --log-opts="--all" -v
```

</div>

### semgrep

<div class="tool-block" markdown="1">

<div class="tool-meta"><span class="tool-tag">SAST</span><span class="tool-tag">Multi-language</span></div>

**Install**

```bash
pip install semgrep
```

**Basic Usage**

```bash
# Auto-detect language and scan
semgrep --config=auto .

# OWASP Top 10 rules
semgrep --config=p/owasp-top-ten .

# Custom rules
semgrep --config=./rules/ src/
```

</div>

---

## Utility Tools

### bbscope

```bash
go install github.com/sw33tLie/bbscope@latest

# HackerOne programs
bbscope hackerone -t "$H1_TOKEN" -o t

# Bugcrowd
bbscope bugcrowd -t "$BC_TOKEN" -o t
```

### interactsh

```bash
go install -v github.com/projectdiscovery/interactsh/cmd/interactsh@latest

# Start OOB server
interactsh-client

# Use in SSRF/blind XSS payloads
# http://<unique-id>.oast.fun
```

### testssl.sh

```bash
git clone https://github.com/drwetter/testssl.sh.git
./testssl.sh target.com
./testssl.sh --severity HIGH target.com
```

---

## Tool Installation Cheat Sheet

```bash
# ProjectDiscovery suite
for tool in subfinder httpx naabu nuclei katana dnsx; do
  go install -v github.com/projectdiscovery/${tool}/cmd/${tool}@latest
done

# Web testing
go install github.com/ffuf/ffuf/v2@latest
go install github.com/hahwul/dalfox/v2@latest
pip install sqlmap commix jwt_tool

# Secrets
pip install trufflehog semgrep

# AD
pip install impacket bloodhound crackmapexec

# Cloud
pip install prowler
```

See [Workflows](WORKFLOWS.md) for how to chain these tools together in real engagements.
