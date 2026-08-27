from tips._base import t

BUG_BOUNTY_TIPS = {
    "bug-bounty/recon": [
        t("One-liner recon chain", "`subfinder -d target.com -silent | httpx -title -tech-detect -o live.txt`"),
        t("Scope first", "Load scope into Burp and all tools before touching anything — out-of-scope = instant ban.", "warning"),
        t("Passive before active", "Run passive enum 24h before active scans — programs notice aggressive scanning."),
        t("Track everything", "Use a spreadsheet: asset, tech, status, findings, last tested."),
        t("Refresh weekly", "Recon is never done — new subdomains appear on every CT log update."),
    ],
    "bug-bounty/subdomain-enumeration": [
        t("Combine passive sources", "subfinder + amass + assetfinder + crt.sh — union beats any single tool."),
        t("Wildcard handling", "Use puredns or shuffledns to filter wildcard DNS before httpx."),
        t("Permutation attacks", "altdns or gotator on discovered subs finds `dev-api-v2.target.com`."),
        t("Monitor CT logs", "crt.sh RSS + Slack alert for new certs on in-scope domains."),
        t("Validate ownership", "Never test a subdomain until confirmed in program scope."),
    ],
    "bug-bounty/asset-discovery": [
        t("ASN mapping", "`asnmap -d target.com` then scan owned IP ranges."),
        t("Acquisition hunting", "Check acquired companies' domains still in DNS CNAME chains."),
        t("Mobile app strings", "Extract API hosts from APK strings — often staging environments."),
        t("GitHub dorking", "`org:target filename:.env` or `target.com password` in public repos."),
        t("Certificate transparency", "New certs reveal hosts before DNS propagates publicly."),
    ],
    "bug-bounty/port-scanning": [
        t("Top ports first", "naabu `-top-ports 1000` on all hosts before full 65535 on gold targets."),
        t("Rate limit scans", "`-rate 1000` max on bug bounty — avoid tripping IDS or program bans.", "warning"),
        t("Service scripts", "nmap `-sV -sC` on interesting ports finds default creds and versions."),
        t("Admin panels", "8080, 8443, 9090, 3000, 5000 — high-value non-standard ports."),
        t("UDP selectively", "UDP full scan is slow and noisy — SNMP 161 and DNS 53 only unless internal."),
    ],
    "bug-bounty/http-probing": [
        t("httpx flags", "`-title -status-code -tech-detect -follow-redirects -json -o out.json`"),
        t("Screenshot triage", "`-screenshot` flags interesting login pages visually."),
        t("Filter noise", "`-mc 200,301,302,403` — 403 often hides admin panels worth bypass testing."),
        t("Chain to nuclei", "`httpx -l subs.txt -silent | nuclei -t exposures/`"),
        t("Re-probe after changes", "Run httpx daily on scope — new services appear constantly."),
    ],
    "bug-bounty/dns-enumeration": [
        t("dnsx for resolution", "`cat subs.txt | dnsx -a -aaaa -cname -resp -o resolved.txt`"),
        t("AXFR attempt", "Always try `dig axfr @ns1.target.com target.com` — still works surprisingly often."),
        t("TXT record intel", "SPF records leak internal IPs and third-party services."),
        t("CNAME takeover", "NXDOMAIN on CNAME to dead SaaS = subdomain takeover candidate."),
        t("fierce for zones", "`fierce --domain target.com` maps adjacent IP blocks."),
    ],
    "bug-bounty/tech-detection": [
        t("Stack fingerprint", "httpx `-tech-detect` + whatweb for double coverage."),
        t("Version to CVE", "Match detected versions to nuclei CVE templates immediately."),
        t("JS framework", "React/Vue/Angular versions in bundle comments — check known XSS gadgets."),
        t("WAF detection", "wafw00f identifies WAF — choose tamper scripts accordingly."),
        t("WordPress/plugins", "wpscan when WordPress detected — low-hanging fruit on many programs."),
    ],
}
