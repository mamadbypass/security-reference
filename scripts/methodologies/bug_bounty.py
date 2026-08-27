from methodologies._base import REPORT, SCOPE, phases

BUG_BOUNTY_METHODOLOGIES = {
    "bug-bounty/recon": phases(
        SCOPE + ["Export in-scope domains/IPs from program policy or bbscope", "Create asset tracker spreadsheet or notion DB"],
        ["Run passive subdomain enum (subfinder, amass, gau)", "Resolve DNS and filter wildcards", "Probe live hosts with httpx", "Fingerprint tech stack per host"],
        ["Prioritize high-value targets: admin, api, staging, dev", "Run nuclei on exposures and misconfigs", "Correlate findings with known CVEs", "Validate each finding manually before deep testing"],
        ["Chain recon data into vuln testing workflows", "Document new assets for program notification if required", "Avoid aggressive scanning beyond ROE"],
        REPORT,
    ),
    "bug-bounty/subdomain-enumeration": phases(
        SCOPE + ["Confirm wildcard scope rules and out-of-scope patterns"],
        ["Passive: CT logs, DNS APIs, search engines", "Active: brute force with curated wordlists", "Permutation: alter discovered names (dev-, api-, staging-)", "Resolve and deduplicate results"],
        ["Validate ownership against scope", "Check for dangling DNS / takeover candidates", "Probe HTTP/HTTPS on all discovered subs", "Flag high-risk names (jenkins, gitlab, vpn)"],
        ["Test subdomain takeover on NXDOMAIN CNAMEs", "Document new in-scope assets", "Report out-of-scope discoveries without testing"],
        REPORT,
    ),
    "bug-bounty/asset-discovery": phases(
        SCOPE + ["Gather ASN, IP ranges, and acquisitions from scope"],
        ["Correlate IPs to cloud providers and CDNs", "Scan ports on discovered ranges", "Crawl live sites for API and mobile backends", "Search code repos and mobile apps for endpoints"],
        ["Validate each asset is in scope", "Identify forgotten acquisitions and dev environments", "Map API gateways and serverless functions", "Check S3 buckets and storage linked to org"],
        ["Prioritize assets with weak auth or old software", "Feed inventory into vulnerability scanning", "Notify program of critical exposed assets"],
        REPORT,
    ),
    "bug-bounty/port-scanning": phases(
        SCOPE + ["Confirm port scanning is allowed in program rules"],
        ["Start with top 1000 TCP ports on live hosts", "Expand to full scan on high-value targets only", "UDP scan critical services if permitted", "Document scan rate limits to avoid DoS"],
        ["Fingerprint service versions (nmap -sV)", "Identify management interfaces (8080, 8443, 3389)", "Check default credentials on exposed services", "Correlate with nuclei service templates"],
        ["Deep test only on in-scope services", "Avoid brute force unless explicitly allowed", "Report exposed admin panels and databases"],
        REPORT,
    ),
    "bug-bounty/http-probing": phases(
        SCOPE + ["Prepare host list from subdomain enumeration"],
        ["Run httpx with status, title, tech-detect", "Filter by status codes (200, 301, 302, 403)", "Capture screenshots for visual triage", "Export JSON for downstream tools"],
        ["Identify interesting 403/401 for bypass testing", "Cluster by technology for targeted scans", "Detect WAF/CDN from headers", "Flag login portals and API docs"],
        ["Hand off live URLs to manual and automated testing", "Update asset inventory with metadata", "Re-probe periodically for new services"],
        REPORT,
    ),
    "bug-bounty/dns-enumeration": phases(
        SCOPE + ["List root domains and approved TLD variants"],
        ["Query A, AAAA, MX, NS, TXT, CNAME, SRV records", "Attempt zone transfer (AXFR) on nameservers", "Extract SPF/DMARC/DKIM for email attack surface", "Find verification tokens in TXT records"],
        ["Validate dangling CNAMEs for takeover", "Map mail and third-party SaaS integrations", "Identify internal hostnames leaked in DNS", "Correlate with certificate transparency"],
        ["Report DNS misconfigurations and takeovers", "Document email spoofing risk from SPF gaps", "Avoid publishing sensitive internal DNS externally"],
        REPORT,
    ),
    "bug-bounty/tech-detection": phases(
        SCOPE + ["Build URL list from live host inventory"],
        ["Run whatweb, httpx -tech-detect, Wappalyzer", "Identify frameworks, CMS, and server versions", "Check JS libraries for known vulnerable versions", "Map CDN, WAF, and load balancer products"],
        ["Cross-reference versions with CVE databases", "Run targeted nuclei templates per stack", "Identify outdated WordPress plugins, etc.", "Note default install paths for each tech"],
        ["Prioritize CVE exploitation on in-scope targets", "Document tech stack per asset for reporting", "Retest after vendor patches"],
        REPORT,
    ),
}
