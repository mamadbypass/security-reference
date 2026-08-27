#!/usr/bin/env python3
"""Generate security reference documentation structure."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

STRUCTURE = {
    "index.md": None,
    "bug-bounty/recon/index.md": {
        "title": "Reconnaissance",
        "description": "Information gathering and target mapping for bug bounty programs.",
        "methodology": [
            "Define scope and rules of engagement",
            "Identify in-scope domains, IPs, and mobile apps",
            "Collect passive intelligence before active scanning",
            "Document all discovered assets in a tracker",
        ],
        "tools": ["amass", "subfinder", "assetfinder", "httpx", "nuclei", "gau", "waybackurls"],
        "resources": [
            ("OWASP Testing Guide - Information Gathering", "https://owasp.org/www-project-web-security-testing-guide/"),
            ("HackTricks Recon", "https://book.hacktricks.xyz/generic-methodologies-and-resources/external-recon-methodology"),
        ],
    },
    "bug-bounty/subdomain-enumeration/index.md": {
        "title": "Subdomain Enumeration",
        "description": "Discover subdomains and expand the attack surface.",
        "methodology": [
            "Run passive enumeration from certificate transparency and archives",
            "Brute-force with curated wordlists",
            "Resolve and probe live hosts",
            "Track wildcard DNS behavior",
        ],
        "tools": ["subfinder", "amass", "puredns", "massdns", "dnsx", "shuffledns"],
        "resources": [
            ("Certificate Transparency", "https://crt.sh/"),
            ("HackTricks Subdomain Enumeration", "https://book.hacktricks.xyz/generic-methodologies-and-resources/external-recon-methodology#subdomain-enumeration"),
        ],
    },
    "bug-bounty/asset-discovery/index.md": {
        "title": "Asset Discovery",
        "description": "Map all in-scope assets including APIs, mobile backends, and cloud resources.",
        "methodology": [
            "Correlate subdomains with ASN and IP ranges",
            "Identify staging, dev, and legacy environments",
            "Check acquisition domains and forgotten properties",
            "Validate ownership against program scope",
        ],
        "tools": ["asnmap", "mapcidr", "naabu", "httpx", "katana"],
        "resources": [
            ("ProjectDiscovery Tools", "https://projectdiscovery.io/"),
        ],
    },
    "bug-bounty/port-scanning/index.md": {
        "title": "Port Scanning",
        "description": "Identify open services and exposed management interfaces.",
        "methodology": [
            "Start with top ports on live hosts",
            "Expand to full port scans on high-value targets",
            "Fingerprint services and versions",
            "Check for default credentials and admin panels",
        ],
        "tools": ["naabu", "nmap", "masscan", "rustscan"],
        "resources": [
            ("Nmap Reference", "https://nmap.org/book/man.html"),
        ],
    },
    "bug-bounty/http-probing/index.md": {
        "title": "HTTP Probing",
        "description": "Identify live web services, technologies, and response behaviors.",
        "methodology": [
            "Probe HTTP/HTTPS on discovered hosts",
            "Capture status codes, titles, and redirects",
            "Detect WAF and CDN behavior",
            "Build a prioritized target list",
        ],
        "tools": ["httpx", "httprobe", "aquatone", "gowitness"],
        "resources": [
            ("ProjectDiscovery httpx", "https://github.com/projectdiscovery/httpx"),
        ],
    },
    "bug-bounty/dns-enumeration/index.md": {
        "title": "DNS Enumeration",
        "description": "Extract DNS records, zone transfer opportunities, and mail infrastructure.",
        "methodology": [
            "Query A, AAAA, CNAME, MX, TXT, NS records",
            "Look for SPF/DKIM/DMARC misconfigurations",
            "Attempt zone transfers on authoritative nameservers",
            "Identify dangling DNS records",
        ],
        "tools": ["dnsx", "dig", "dnsrecon", "fierce"],
        "resources": [
            ("HackTricks DNS", "https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network/dns"),
        ],
    },
    "bug-bounty/tech-detection/index.md": {
        "title": "Technology Detection",
        "description": "Fingerprint frameworks, CMS platforms, and third-party integrations.",
        "methodology": [
            "Analyze response headers and HTML comments",
            "Check JavaScript bundles and known library paths",
            "Map CDN, WAF, and analytics providers",
            "Correlate versions with known CVEs",
        ],
        "tools": ["whatweb", "wappalyzer", "nuclei", "httpx -tech-detect"],
        "resources": [
            ("Wappalyzer", "https://www.wappalyzer.com/"),
        ],
    },
    "web/lfi-rfi/index.md": {
        "title": "LFI / RFI",
        "description": "Local and remote file inclusion testing.",
        "methodology": [
            "Identify file/path parameters",
            "Test path traversal sequences",
            "Attempt log poisoning and PHP wrappers",
            "Check for RFI via remote URL inclusion",
        ],
        "tools": ["ffuf", "burp", "lfi-suite"],
        "resources": [
            ("PayloadsAllTheThings LFI", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion"),
            ("PortSwigger File Path Traversal", "https://portswigger.net/web-security/file-path-traversal"),
        ],
    },
    "web/xxe/index.md": {
        "title": "XXE",
        "description": "XML External Entity injection testing.",
        "methodology": [
            "Identify XML input endpoints",
            "Test file read via external entities",
            "Attempt SSRF through XXE",
            "Check blind XXE with out-of-band callbacks",
        ],
        "tools": ["burp", "xxeinjector", "oxmlxxe"],
        "resources": [
            ("PortSwigger XXE", "https://portswigger.net/web-security/xxe"),
        ],
    },
    "web/deserialization/index.md": {
        "title": "Insecure Deserialization",
        "description": "Exploit unsafe object deserialization in web applications.",
        "methodology": [
            "Identify serialized object formats (Java, PHP, .NET, Python)",
            "Use known gadget chains for the stack",
            "Test tampered cookies and API bodies",
            "Validate impact with safe proof-of-concept payloads",
        ],
        "tools": ["ysoserial", "phpggc", "burp"],
        "resources": [
            ("OWASP Deserialization", "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/16-Testing_for_HTTP_Insecure_Deserialization"),
        ],
    },
    "web/race-condition/index.md": {
        "title": "Race Condition",
        "description": "Exploit time-of-check to time-of-use flaws.",
        "methodology": [
            "Identify limit checks on coupons, transfers, or votes",
            "Send parallel requests with Turbo Intruder or custom scripts",
            "Test single-use tokens and rate limits",
            "Measure window timing for reliable exploitation",
        ],
        "tools": ["burp turbo intruder", "race-the-web", "python asyncio"],
        "resources": [
            ("PortSwigger Race Conditions", "https://portswigger.net/web-security/race-conditions"),
        ],
    },
    "web/open-redirect/index.md": {
        "title": "Open Redirect",
        "description": "Abuse redirect parameters for phishing and OAuth token theft.",
        "methodology": [
            "Find redirect, next, url, return parameters",
            "Test external domain acceptance",
            "Chain with OAuth and SSO flows",
            "Validate bypasses using //evil.com and encoded URLs",
        ],
        "tools": ["burp", "openredirex"],
        "resources": [
            ("PayloadsAllTheThings Open Redirect", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Open%20Redirect"),
        ],
    },
    "web/prototype-pollution/index.md": {
        "title": "Prototype Pollution",
        "description": "Pollute JavaScript object prototypes for XSS and RCE.",
        "methodology": [
            "Identify merge/extend utilities in client code",
            "Test __proto__ and constructor.prototype keys",
            "Look for gadget chains leading to XSS",
            "Check server-side Node.js pollution",
        ],
        "tools": ["burp", "ppmap", "dom clobbering scanners"],
        "resources": [
            ("PortSwigger Prototype Pollution", "https://portswigger.net/web-security/prototype-pollution"),
        ],
    },
    "web/cors/index.md": {
        "title": "CORS Misconfiguration",
        "description": "Exploit overly permissive cross-origin resource sharing.",
        "methodology": [
            "Check Access-Control-Allow-Origin on sensitive endpoints",
            "Test null origin and subdomain reflection",
            "Verify credentials with ACAO + ACAC",
            "Demonstrate data exfiltration impact",
        ],
        "tools": ["burp", "corsy", "CORScanner"],
        "resources": [
            ("PortSwigger CORS", "https://portswigger.net/web-security/cors"),
        ],
    },
    "web/clickjacking/index.md": {
        "title": "Clickjacking",
        "description": "Frame sensitive actions to trick users into unintended clicks.",
        "methodology": [
            "Check X-Frame-Options and CSP frame-ancestors",
            "Build proof-of-concept iframe overlays",
            "Target high-impact actions (password change, payment)",
            "Test mobile WebView contexts",
        ],
        "tools": ["burp", "custom html poc"],
        "resources": [
            ("PortSwigger Clickjacking", "https://portswigger.net/web-security/clickjacking"),
        ],
    },
    "web/http-request-smuggling/index.md": {
        "title": "HTTP Request Smuggling",
        "description": "Desynchronize front-end and back-end HTTP parsers.",
        "methodology": [
            "Identify CL.TE and TE.CL behavior",
            "Use timing-based detection",
            "Exploit for cache poisoning or request hijacking",
            "Test HTTP/2 downgrade scenarios",
        ],
        "tools": ["burp", "smuggler", "h2csmuggler"],
        "resources": [
            ("PortSwigger Request Smuggling", "https://portswigger.net/web-security/request-smuggling"),
        ],
    },
    "web/web-cache-poisoning/index.md": {
        "title": "Web Cache Poisoning",
        "description": "Poison shared caches to serve malicious content.",
        "methodology": [
            "Identify unkeyed headers and parameters",
            "Test cacheable responses",
            "Confirm poisoning with unique cache keys",
            "Assess victim impact on CDN edges",
        ],
        "tools": ["burp", "param-miner", "web-cache-vulnerability-scanner"],
        "resources": [
            ("PortSwigger Web Cache Poisoning", "https://portswigger.net/web-security/web-cache-poisoning"),
        ],
    },
    "web/business-logic/index.md": {
        "title": "Business Logic Flaws",
        "description": "Abuse application workflows beyond technical vulnerabilities.",
        "methodology": [
            "Map purchase, refund, and privilege workflows",
            "Test negative quantities and price manipulation",
            "Bypass multi-step validations",
            "Check role transitions and feature gating",
        ],
        "tools": ["burp", "manual testing"],
        "resources": [
            ("OWASP Business Logic", "https://owasp.org/www-community/vulnerabilities/Business_logic_vulnerability"),
        ],
    },
    "web/crlf-injection/index.md": {
        "title": "CRLF Injection",
        "description": "Inject carriage return and line feed to manipulate HTTP responses.",
        "methodology": [
            "Test redirect and header-reflecting parameters",
            "Attempt response splitting",
            "Inject Set-Cookie or Location headers",
            "Chain with XSS via injected headers",
        ],
        "tools": ["burp", "crlfuzz"],
        "resources": [
            ("PayloadsAllTheThings CRLF", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/CRLF%20Injection"),
        ],
    },
    "web/command-injection/index.md": {
        "title": "Command Injection",
        "description": "Execute OS commands through vulnerable input handlers.",
        "methodology": [
            "Identify ping, traceroute, and file conversion features",
            "Test command separators for the target OS",
            "Use time delays and out-of-band callbacks",
            "Escalate from blind to interactive execution",
        ],
        "tools": ["commix", "burp", "ffuf"],
        "resources": [
            ("PayloadsAllTheThings Command Injection", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection"),
        ],
    },
    "web/nosql-injection/index.md": {
        "title": "NoSQL Injection",
        "description": "Manipulate NoSQL query operators in MongoDB and similar databases.",
        "methodology": [
            "Test JSON bodies with $ne, $gt, $regex operators",
            "Bypass authentication with operator injection",
            "Extract data via boolean-based inference",
            "Review ORM and driver sanitization",
        ],
        "tools": ["burp", "nosqlmap"],
        "resources": [
            ("PayloadsAllTheThings NoSQL", "https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection"),
        ],
    },
    "web/http-parameter-pollution/index.md": {
        "title": "HTTP Parameter Pollution",
        "description": "Abuse duplicate parameters handled differently by proxies and backends.",
        "methodology": [
            "Send duplicate GET/POST parameters",
            "Test WAF bypass via parameter splitting",
            "Check auth bypass on access control checks",
            "Compare framework-specific parsing behavior",
        ],
        "tools": ["burp", "manual fuzzing"],
        "resources": [
            ("OWASP HPP", "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution"),
        ],
    },
    "web/websockets/index.md": {
        "title": "WebSockets Security",
        "description": "Test real-time channels for auth bypass and injection.",
        "methodology": [
            "Capture WebSocket handshake and messages",
            "Test origin validation on the handshake",
            "Fuzz message types for injection",
            "Check authorization per channel or room",
        ],
        "tools": ["burp", "ws-harness", "owasp zap"],
        "resources": [
            ("PortSwigger WebSockets", "https://portswigger.net/web-security/websockets"),
        ],
    },
    "web/information-disclosure/index.md": {
        "title": "Information Disclosure",
        "description": "Find sensitive data exposed through errors, backups, and misconfigurations.",
        "methodology": [
            "Trigger verbose error messages",
            "Check /.git, /.env, backup files",
            "Review API responses for excessive data",
            "Search JS bundles for secrets and endpoints",
        ],
        "tools": ["trufflehog", "gitleaks", "nuclei", "linkfinder"],
        "resources": [
            ("OWASP Information Exposure", "https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/05-Testing_for_Information_Disclosure"),
        ],
    },
    "web/ldap-xpath-injection/index.md": {
        "title": "LDAP / XPath Injection",
        "description": "Manipulate directory and XML query syntax.",
        "methodology": [
            "Identify search and login filters using LDAP/XPath",
            "Test wildcard and boolean injection",
            "Extract attributes via blind inference",
            "Validate input encoding bypasses",
        ],
        "tools": ["burp", "manual payloads"],
        "resources": [
            ("OWASP LDAP Injection", "https://owasp.org/www-community/attacks/LDAP_Injection"),
        ],
    },
    "web/dom-clobbering/index.md": {
        "title": "DOM Clobbering",
        "description": "Overwrite DOM properties using named HTML elements.",
        "methodology": [
            "Review client-side sinks relying on window or form properties",
            "Inject elements with id and name attributes",
            "Chain with prototype pollution or XSS",
            "Test sanitizer bypass via clobbered globals",
        ],
        "tools": ["burp", "dompurify bypass research"],
        "resources": [
            ("PortSwigger DOM Clobbering", "https://portswigger.net/web-security/dom-based/dom-clobbering"),
        ],
    },
    "web/sqli/index.md": {
        "title": "SQL Injection",
        "description": "Classic SQL injection across query types and database engines.",
        "methodology": [
            "Identify injectable parameters with error and boolean tests",
            "Determine query type (UNION, blind, stacked)",
            "Extract schema and sensitive records",
            "Document minimal proof for reporting",
        ],
        "tools": ["sqlmap", "burp", "ghauri"],
        "resources": [
            ("PortSwigger SQLi", "https://portswigger.net/web-security/sql-injection"),
        ],
    },
    "web/xss/index.md": {
        "title": "Cross-Site Scripting (XSS)",
        "description": "Reflected, stored, and DOM-based XSS testing.",
        "methodology": [
            "Map input vectors and output contexts",
            "Test HTML, attribute, and JavaScript contexts",
            "Bypass filters and CSP where possible",
            "Demonstrate impact without harm",
        ],
        "tools": ["burp", "xsstrike", "dalfox"],
        "resources": [
            ("PortSwigger XSS", "https://portswigger.net/web-security/cross-site-scripting"),
        ],
    },
    "web/ssrf/index.md": {
        "title": "Server-Side Request Forgery (SSRF)",
        "description": "Force server-side requests to internal and cloud metadata endpoints.",
        "methodology": [
            "Find URL import, webhook, and preview features",
            "Probe localhost and cloud metadata IPs",
            "Use DNS rebinding and redirect chains",
            "Escalate to internal service access",
        ],
        "tools": ["burp", "ssrfmap", "interactsh"],
        "resources": [
            ("PortSwigger SSRF", "https://portswigger.net/web-security/ssrf"),
        ],
    },
    "web/idor/index.md": {
        "title": "Insecure Direct Object Reference (IDOR)",
        "description": "Access unauthorized objects by manipulating identifiers.",
        "methodology": [
            "Collect object IDs across roles",
            "Swap IDs between low and high privilege accounts",
            "Test UUID, hash, and encoded identifiers",
            "Check mass assignment alongside IDOR",
        ],
        "tools": ["burp", "autorize"],
        "resources": [
            ("PortSwigger Access Control", "https://portswigger.net/web-security/access-control"),
        ],
    },
    "web/ssti/index.md": {
        "title": "Server-Side Template Injection (SSTI)",
        "description": "Inject template syntax for code execution.",
        "methodology": [
            "Detect template engine with polyglot probes",
            "Escalate to read files or execute commands",
            "Test blind SSTI via out-of-band channels",
            "Identify sandbox escapes per engine",
        ],
        "tools": ["tplmap", "burp"],
        "resources": [
            ("PortSwigger SSTI", "https://portswigger.net/web-security/server-side-template-injection"),
        ],
    },
    "api/graphql/index.md": {
        "title": "GraphQL Security",
        "description": "Test GraphQL APIs for introspection, batching, and authorization flaws.",
        "methodology": [
            "Enable and review schema introspection",
            "Test batch queries for brute force and rate limit bypass",
            "Check field-level authorization",
            "Look for debug endpoints and IDE exposure",
        ],
        "tools": ["clairvoyance", "graphql-voyager", "burp", "inql"],
        "resources": [
            ("OWASP GraphQL Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html"),
        ],
    },
    "api/graphql/introspection.md": {
        "title": "GraphQL Introspection",
        "description": "Enumerate schema when introspection is enabled.",
        "methodology": [
            "Send __schema and __type queries",
            "Export schema for hidden mutations",
            "Check introspection on staging endpoints",
            "Review sensitive fields and admin mutations",
        ],
        "tools": ["clairvoyance", "graphql-cop"],
        "resources": [],
    },
    "api/graphql/batching.md": {
        "title": "GraphQL Batching Attacks",
        "description": "Abuse query batching to bypass rate limits and brute force.",
        "methodology": [
            "Send arrays of login or OTP mutations",
            "Measure rate limit behavior on batched requests",
            "Combine aliases for parallel extraction",
            "Report auth bypass impact",
        ],
        "tools": ["burp", "custom scripts"],
        "resources": [],
    },
    "api/versioning/index.md": {
        "title": "API Versioning Issues",
        "description": "Find deprecated API versions with weaker security controls.",
        "methodology": [
            "Discover /v1, /v2, /beta, /internal paths",
            "Compare auth requirements across versions",
            "Test legacy mobile API backends",
            "Check unauthenticated debug versions",
        ],
        "tools": ["ffuf", "burp", "kiterunner"],
        "resources": [
            ("OWASP API Security Top 10", "https://owasp.org/API-Security/"),
        ],
    },
    "api/shadow-zombie-apis/index.md": {
        "title": "Shadow & Zombie APIs",
        "description": "Uncover undocumented and forgotten API endpoints.",
        "methodology": [
            "Mine JavaScript for API routes",
            "Review mobile app traffic and Swagger leaks",
            "Scan for /swagger, /openapi.json, /graphql",
            "Diff API behavior after deployments",
        ],
        "tools": ["linkfinder", "katana", "nuclei"],
        "resources": [],
    },
    "api/grpc-protobuf/index.md": {
        "title": "gRPC & Protobuf",
        "description": "Test gRPC services and protobuf-encoded APIs.",
        "methodology": [
            "Identify gRPC ports and reflection",
            "Decode protobuf messages from traffic",
            "Fuzz RPC methods for auth bypass",
            "Test TLS and metadata token handling",
        ],
        "tools": ["grpcurl", "grpcui", "burp grpc assistant"],
        "resources": [
            ("gRPC Security", "https://grpc.io/docs/guides/auth/"),
        ],
    },
    "authentication/password-reset/index.md": {
        "title": "Password Reset Flaws",
        "description": "Exploit weak password reset and account recovery flows.",
        "methodology": [
            "Test token predictability and reuse",
            "Host header poisoning on reset links",
            "Race reset token validation",
            "Check reset for arbitrary email change",
        ],
        "tools": ["burp"],
        "resources": [
            ("OWASP Forgot Password", "https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html"),
        ],
    },
    "authentication/sso-saml/index.md": {
        "title": "SSO & SAML",
        "description": "Test single sign-on and SAML assertion handling.",
        "methodology": [
            "Review SAML response signature validation",
            "Test XML signature wrapping",
            "Check redirect URI in OAuth/OIDC flows",
            "Attempt token replay and mix-up attacks",
        ],
        "tools": ["burp", "saml raider"],
        "resources": [
            ("OWASP SAML Security", "https://owasp.org/www-community/vulnerabilities/SAML_Security_Cheat_Sheet"),
        ],
    },
    "authentication/passwordless/index.md": {
        "title": "Passwordless & WebAuthn",
        "description": "Test magic links, OTP, and passkey implementations.",
        "methodology": [
            "Brute force short OTP codes",
            "Test magic link token entropy",
            "Review WebAuthn challenge binding",
            "Check credential enumeration",
        ],
        "tools": ["burp"],
        "resources": [
            ("WebAuthn Guide", "https://webauthn.guide/"),
        ],
    },
    "authentication/jwt/index.md": {
        "title": "JWT Attacks",
        "description": "Exploit weak JSON Web Token implementations.",
        "methodology": [
            "Test alg:none and key confusion",
            "Brute force weak HMAC secrets",
            "Modify claims for privilege escalation",
            "Check jku and kid header injection",
        ],
        "tools": ["jwt_tool", "burp"],
        "resources": [
            ("PortSwigger JWT", "https://portswigger.net/web-security/jwt"),
        ],
    },
    "mobile/apk-ipa-analysis/index.md": {
        "title": "APK / IPA Analysis",
        "description": "Static and dynamic analysis of mobile applications.",
        "methodology": [
            "Decompile APK/IPA and review hardcoded secrets",
            "Map API endpoints and certificate pinning",
            "Test exported components and deep links",
            "Intercept traffic with rooted/jailbroken devices or patches",
        ],
        "tools": ["jadx", "apktool", "mobsf", "objection"],
        "resources": [
            ("OWASP MASTG", "https://owasp.org/www-project-mobile-app-security-testing-guide/"),
        ],
    },
    "mobile/frida/index.md": {
        "title": "Frida Instrumentation",
        "description": "Dynamic instrumentation for mobile runtime manipulation.",
        "methodology": [
            "Hook SSL pinning validation functions",
            "Bypass root/jailbreak detection",
            "Intercept crypto and token generation",
            "Patch method return values at runtime",
        ],
        "tools": ["frida", "objection", "r2frida"],
        "resources": [
            ("Frida Docs", "https://frida.re/docs/home/"),
        ],
    },
    "mobile/ssl-pinning-bypass/index.md": {
        "title": "SSL Pinning Bypass",
        "description": "Intercept HTTPS from mobile apps with certificate pinning.",
        "methodology": [
            "Identify pinning libraries in the binary",
            "Use Frida scripts to disable validation",
            "Patch APK with custom network security config",
            "Test on emulators with system CA installed",
        ],
        "tools": ["frida", "apk-mitm", "objection"],
        "resources": [],
    },
    "mobile/deep-links/index.md": {
        "title": "Deep Links & Universal Links",
        "description": "Test mobile deep link handlers for auth bypass and XSS.",
        "methodology": [
            "Enumerate custom URL schemes",
            "Test intent filters and path parameters",
            "Check app link verification files",
            "Chain open redirects in WebViews",
        ],
        "tools": ["adb", "objection", "burp"],
        "resources": [],
    },
    "automation/js-analysis/index.md": {
        "title": "JavaScript File Analysis",
        "description": "Extract endpoints, secrets, and logic from client-side code.",
        "methodology": [
            "Collect JS from crawlers and source maps",
            "Run link and secret discovery tools",
            "Review webpack chunks for hidden routes",
            "Track changes between deployments",
        ],
        "tools": ["linkfinder", "secretfinder", "nuclei", "katana"],
        "resources": [],
    },
    "automation/diffing/index.md": {
        "title": "Diffing & Change Detection",
        "description": "Monitor target changes for new attack surface.",
        "methodology": [
            "Baseline responses and JS bundles",
            "Alert on new subdomains and endpoints",
            "Diff Swagger/OpenAPI documents",
            "Automate periodic recon pipelines",
        ],
        "tools": ["nuclei", "custom scripts", "github actions"],
        "resources": [],
    },
    "automation/scope-tooling/index.md": {
        "title": "Bug Bounty Scope Tooling",
        "description": "Manage program scope and asset tracking.",
        "methodology": [
            "Import scope from HackerOne/Bugcrowd/Intigriti",
            "Validate in-scope before testing",
            "Track new assets against scope rules",
            "Maintain engagement notes per program",
        ],
        "tools": ["bbscope", "hackerone cli", "custom spreadsheets"],
        "resources": [
            ("HackerOne Hacktivity", "https://hackerone.com/hacktivity"),
        ],
    },
    "network/active-directory/index.md": {
        "title": "Active Directory",
        "description": "Attack and assess Windows domain environments.",
        "methodology": [
            "Enumerate users, groups, and ACLs",
            "Identify Kerberoastable and AS-REP roastable accounts",
            "Map attack paths with BloodHound",
            "Escalate to Domain Admin safely in lab scope",
        ],
        "tools": ["bloodhound", "rubeus", "impacket", "powerview"],
        "resources": [
            ("HackTricks AD", "https://book.hacktricks.xyz/windows-hardening/active-directory-methodology"),
        ],
    },
    "network/active-directory/kerberoasting.md": {
        "title": "Kerberoasting",
        "description": "Extract and crack service ticket hashes offline.",
        "methodology": [
            "Find SPN accounts with sufficient rights",
            "Request TGS tickets for offline cracking",
            "Use strong wordlists and rules",
            "Validate cracked creds for lateral movement",
        ],
        "tools": ["rubeus", "impacket GetUserSPNs", "hashcat"],
        "resources": [],
    },
    "network/bloodhound/index.md": {
        "title": "BloodHound",
        "description": "Graph-based Active Directory attack path analysis.",
        "methodology": [
            "Ingest SharpHound/BloodHound.py data",
            "Find shortest paths to high-value targets",
            "Review ACL abuse opportunities",
            "Prioritize edges for exploitation",
        ],
        "tools": ["bloodhound", "sharphound", "bloodhound.py"],
        "resources": [
            ("BloodHound Docs", "https://bloodhound.readthedocs.io/"),
        ],
    },
    "network/dcsync/index.md": {
        "title": "DCSync",
        "description": "Replicate directory credentials from domain controllers.",
        "methodology": [
            "Identify Replicating Directory Changes rights",
            "Use DCSync to dump hashes",
            "Protect evidence handling in engagements",
            "Recommend remediation for replication ACLs",
        ],
        "tools": ["mimikatz", "impacket secretsdump"],
        "resources": [],
    },
    "network/pentesting/index.md": {
        "title": "Network Pentesting",
        "description": "Internal and external network penetration testing methodology.",
        "methodology": [
            "Scope subnets and critical assets",
            "Scan, enumerate, and exploit services",
            "Document segmentation effectiveness",
            "Produce risk-ranked findings",
        ],
        "tools": ["nmap", "crackmapexec", "responder", "enum4linux-ng"],
        "resources": [
            ("PTES", "http://www.pentest-standard.org/"),
        ],
    },
    "network/privilege-escalation/windows.md": {
        "title": "Windows Privilege Escalation",
        "description": "Escalate privileges on Windows hosts.",
        "methodology": [
            "Run winPEAS or manual enumeration",
            "Check unquoted service paths and weak permissions",
            "Review token impersonation opportunities",
            "Exploit missing patches when in scope",
        ],
        "tools": ["winpeas", "powerup", "watson"],
        "resources": [
            ("HackTricks Windows Local Privilege Escalation", "https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation"),
        ],
    },
    "network/privilege-escalation/linux.md": {
        "title": "Linux Privilege Escalation",
        "description": "Escalate privileges on Linux systems.",
        "methodology": [
            "Run linpeas and review SUID binaries",
            "Check sudo rules and cron jobs",
            "Enumerate kernel version for exploits",
            "Review Docker socket and capabilities",
        ],
        "tools": ["linpeas", "linux-exploit-suggester"],
        "resources": [
            ("HackTricks Linux Privilege Escalation", "https://book.hacktricks.xyz/linux-hardening/privilege-escalation"),
        ],
    },
    "network/lateral-movement/index.md": {
        "title": "Lateral Movement",
        "description": "Move through networks using harvested credentials and trust relationships.",
        "methodology": [
            "Pass-the-hash and pass-the-ticket where applicable",
            "Abuse WinRM, SMB, and RDP",
            "Leverage trust relationships between domains",
            "Maintain operational security per ROE",
        ],
        "tools": ["crackmapexec", "evil-winrm", "impacket"],
        "resources": [],
    },
    "network/wireless/index.md": {
        "title": "Wireless Security",
        "description": "Assess Wi-Fi networks and rogue access point risks.",
        "methodology": [
            "Capture handshakes and test WPA2/WPA3",
            "Check enterprise EAP configurations",
            "Test guest network segmentation",
            "Evaluate rogue AP detection",
        ],
        "tools": ["aircrack-ng", "bettercap", "kismet"],
        "resources": [],
    },
    "network/firewall-segmentation/index.md": {
        "title": "Firewall & Segmentation",
        "description": "Validate network segmentation and firewall rule effectiveness.",
        "methodology": [
            "Map allowed paths between zones",
            "Test egress filtering",
            "Verify DMZ isolation",
            "Document overly permissive rules",
        ],
        "tools": ["nmap", "hping3", "custom probes"],
        "resources": [],
    },
    "blue-team/detection-engineering/index.md": {
        "title": "Detection Engineering",
        "description": "Build detections mapped to MITRE ATT&CK techniques.",
        "methodology": [
            "Select high-risk techniques for coverage",
            "Author Sigma rules and SIEM queries",
            "Validate detections with atomic tests",
            "Tune to reduce false positives",
        ],
        "tools": ["sigma", "splunk", "elastic", "atomic red team"],
        "resources": [
            ("MITRE ATT&CK", "https://attack.mitre.org/"),
            ("Sigma Rules", "https://github.com/SigmaHQ/sigma"),
        ],
    },
    "blue-team/siem-log-analysis/index.md": {
        "title": "SIEM & Log Analysis",
        "description": "Investigate events using centralized logging.",
        "methodology": [
            "Normalize log sources into SIEM",
            "Build correlation searches",
            "Create triage playbooks",
            "Hunt using IoCs and behavioral baselines",
        ],
        "tools": ["splunk", "elastic", "sentinel", "chronicle"],
        "resources": [],
    },
    "blue-team/threat-hunting/index.md": {
        "title": "Threat Hunting",
        "description": "Proactively search for adversary activity.",
        "methodology": [
            "Develop hypotheses from threat intel",
            "Query endpoint and network telemetry",
            "Stack rank anomalies",
            "Document hunts and outcomes",
        ],
        "tools": ["velociraptor", "sysmon", "yara"],
        "resources": [],
    },
    "blue-team/incident-response/index.md": {
        "title": "Incident Response",
        "description": "Contain, eradicate, and recover from security incidents.",
        "methodology": [
            "Activate IR playbook and assign roles",
            "Preserve forensic evidence",
            "Contain affected systems",
            "Perform root cause analysis and lessons learned",
        ],
        "tools": ["thehive", "velociraptor", "ftk imager"],
        "resources": [
            ("NIST SP 800-61", "https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final"),
        ],
    },
    "blue-team/malware-analysis/index.md": {
        "title": "Malware Analysis Basics",
        "description": "Static and dynamic analysis fundamentals for malware samples.",
        "methodology": [
            "Work in isolated analysis VMs",
            "Extract strings, hashes, and imports",
            "Observe behavior in sandbox",
            "Document IoCs for detection",
        ],
        "tools": ["ghidra", "ida", "cuckoo", "flare-vm"],
        "resources": [],
    },
    "cloud/aws/index.md": {
        "title": "AWS Security Testing",
        "description": "Assess Amazon Web Services misconfigurations and IAM issues.",
        "methodology": [
            "Review IAM policies and privilege escalation paths",
            "Check S3 bucket public access",
            "Audit security groups and exposed services",
            "Test SSRF to metadata service where applicable",
        ],
        "tools": ["pacu", "prowler", "scout suite", "cloudfox"],
        "resources": [
            ("AWS Security Best Practices", "https://docs.aws.amazon.com/security/"),
        ],
    },
    "cloud/azure/index.md": {
        "title": "Azure Security Testing",
        "description": "Assess Microsoft Azure identity and resource misconfigurations.",
        "methodology": [
            "Enumerate Azure AD and app registrations",
            "Review storage account public access",
            "Check managed identity permissions",
            "Test conditional access bypass scenarios",
        ],
        "tools": ["roadtools", "azurehound", "microburst"],
        "resources": [
            ("HackTricks Azure", "https://book.hacktricks.xyz/cloud-security/azure-security"),
        ],
    },
    "cloud/gcp/index.md": {
        "title": "GCP Security Testing",
        "description": "Assess Google Cloud Platform IAM and storage security.",
        "methodology": [
            "Review service account keys and permissions",
            "Check GCS bucket IAM bindings",
            "Audit firewall rules and VPC design",
            "Test metadata server access from workloads",
        ],
        "tools": ["gcp_scanner", "scout suite"],
        "resources": [
            ("HackTricks GCP", "https://book.hacktricks.xyz/cloud-security/gcp-security"),
        ],
    },
    "cloud/kubernetes/index.md": {
        "title": "Kubernetes Security",
        "description": "Assess cluster RBAC, secrets, and workload isolation.",
        "methodology": [
            "Enumerate pods, roles, and clusterrolebindings",
            "Check privileged containers and host mounts",
            "Review network policies",
            "Test etcd and API server exposure",
        ],
        "tools": ["kubectl", "kube-hunter", "kubescape"],
        "resources": [
            ("OWASP Kubernetes Top 10", "https://owasp.org/www-project-kubernetes-top-ten/"),
        ],
    },
    "reporting/vulnerability-reports/index.md": {
        "title": "Vulnerability Reporting",
        "description": "Write clear, actionable security reports for bug bounty and pentest engagements.",
        "methodology": [
            "Use executive summary plus technical detail",
            "Provide reproducible steps and proof-of-concept",
            "Rate severity with CVSS or program matrix",
            "Include remediation guidance",
        ],
        "tools": ["burp", "markdown", "cvss calculator"],
        "resources": [
            ("HackerOne Disclosure Guidelines", "https://www.hackerone.com/disclosure-guidelines"),
        ],
    },
    "growth/cve-research/index.md": {
        "title": "CVE Research",
        "description": "Track and analyze newly disclosed vulnerabilities.",
        "methodology": [
            "Monitor NVD, vendor advisories, and exploit-db",
            "Map CVEs to your tech stack detections",
            "Build safe lab reproductions",
            "Share writeups for community learning",
        ],
        "tools": ["nuclei", "vulners", "cisa kev"],
        "resources": [
            ("NVD", "https://nvd.nist.gov/"),
        ],
    },
    "growth/writeups/index.md": {
        "title": "Writeups & Reputation",
        "description": "Publish quality writeups to build bug bounty reputation.",
        "methodology": [
            "Document unique techniques and root cause",
            "Redact sensitive customer data",
            "Cross-post to blog and HackerOne Hacktivity",
            "Engage responsibly with the community",
        ],
        "tools": ["markdown", "obsidian"],
        "resources": [
            ("Infosec Writeups", "https://infosecwriteups.com/"),
        ],
    },
    "cryptography/crypto-flaws/index.md": {
        "title": "Cryptographic Flaws",
        "description": "Identify weak algorithms, modes, and key management issues.",
        "methodology": [
            "Review cipher suites and protocol versions",
            "Check for ECB mode and static IVs",
            "Test padding oracle conditions",
            "Validate random number generation",
        ],
        "tools": ["testssl.sh", "sslscan", "burp"],
        "resources": [
            ("OWASP Cryptographic Storage", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"),
        ],
    },
    "cryptography/padding-oracle/index.md": {
        "title": "Padding Oracle Attacks",
        "description": "Decrypt ciphertext by observing padding error differences.",
        "methodology": [
            "Identify CBC mode with error side channels",
            "Automate byte-by-byte decryption",
            "Forge valid ciphertext blocks",
            "Recommend authenticated encryption",
        ],
        "tools": ["padbuster", "custom scripts"],
        "resources": [],
    },
    "cryptography/tls-ssl/index.md": {
        "title": "TLS / SSL Testing",
        "description": "Assess transport layer security configuration.",
        "methodology": [
            "Scan for weak protocols and ciphers",
            "Check certificate validity and chain",
            "Test HSTS and certificate pinning",
            "Review TLS termination at load balancers",
        ],
        "tools": ["testssl.sh", "sslyze"],
        "resources": [],
    },
    "containers/docker/index.md": {
        "title": "Docker Security",
        "description": "Assess container images and runtime configurations.",
        "methodology": [
            "Scan images for CVEs and secrets",
            "Check privileged mode and volume mounts",
            "Review capabilities and seccomp profiles",
            "Test container escape primitives",
        ],
        "tools": ["trivy", "docker bench", "grype"],
        "resources": [
            ("CIS Docker Benchmark", "https://www.cisecurity.org/benchmark/docker"),
        ],
    },
    "containers/kubernetes-security/index.md": {
        "title": "Kubernetes Hardening",
        "description": "Secure Kubernetes clusters and workloads.",
        "methodology": [
            "Apply least privilege RBAC",
            "Enable admission controllers",
            "Restrict pod security standards",
            "Audit secrets management",
        ],
        "tools": ["kubescape", "falco", "kyverno"],
        "resources": [],
    },
    "containers/container-escape/index.md": {
        "title": "Container Escape",
        "description": "Break out of container isolation to the host.",
        "methodology": [
            "Identify privileged containers",
            "Abuse mounted docker.sock",
            "Exploit kernel vulnerabilities when in scope",
            "Test cgroup release_agent techniques",
        ],
        "tools": ["deepce", "cdk"],
        "resources": [
            ("HackTricks Docker Escape", "https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation"),
        ],
    },
    "devsecops/pipeline-security/index.md": {
        "title": "CI/CD Pipeline Security",
        "description": "Secure build pipelines against secret leakage and supply chain attacks.",
        "methodology": [
            "Protect pipeline secrets and tokens",
            "Restrict who can modify workflows",
            "Sign artifacts and verify provenance",
            "Scan dependencies in CI",
        ],
        "tools": ["github actions", "gitlab ci", "snyk", "dependabot"],
        "resources": [
            ("OWASP CI/CD Security", "https://owasp.org/www-project-top-10-ci-cd-security-risks/"),
        ],
    },
    "devsecops/iac-security/index.md": {
        "title": "Infrastructure as Code Security",
        "description": "Scan Terraform, CloudFormation, and Kubernetes manifests.",
        "methodology": [
            "Run static analysis on IaC templates",
            "Check for public resources and open security groups",
            "Enforce policy as code in PRs",
            "Review state file access controls",
        ],
        "tools": ["checkov", "tfsec", "kics"],
        "resources": [],
    },
    "devsecops/supply-chain/index.md": {
        "title": "Supply Chain Security",
        "description": "Protect software dependencies and build integrity.",
        "methodology": [
            "Pin dependency versions",
            "Monitor for typosquatting",
            "Use SBOM generation",
            "Verify package signatures",
        ],
        "tools": ["syft", "cosign", "dependabot"],
        "resources": [
            ("SLSA Framework", "https://slsa.dev/"),
        ],
    },
    "binary/reverse-engineering/index.md": {
        "title": "Reverse Engineering",
        "description": "Analyze binaries to understand program behavior.",
        "methodology": [
            "Load samples in disassembler/debugger",
            "Identify key functions and strings",
            "Trace input validation logic",
            "Document findings with annotations",
        ],
        "tools": ["ghidra", "ida", "radare2", "binary ninja"],
        "resources": [
            ("Ghidra Training", "https://ghidra-sre.org/"),
        ],
    },
    "binary/stack-overflow/index.md": {
        "title": "Stack Buffer Overflow",
        "description": "Classic stack-based memory corruption exploitation.",
        "methodology": [
            "Fuzz for crash inputs",
            "Calculate offset to return address",
            "Bypass DEP/ASLR where applicable",
            "Develop reliable proof-of-concept in lab",
        ],
        "tools": ["gdb", "pwndbg", "gef", "ropper"],
        "resources": [],
    },
    "binary/heap-exploitation/index.md": {
        "title": "Heap Exploitation",
        "description": "Exploit heap allocators through use-after-free and overflow primitives.",
        "methodology": [
            "Understand allocator behavior (glibc, jemalloc)",
            "Build primitives from vulnerabilities",
            "Chain for arbitrary write or RCE",
            "Practice in CTF and isolated labs",
        ],
        "tools": ["pwntools", "gdb", "heap exploitation scripts"],
        "resources": [
            ("how2heap", "https://github.com/shellphish/how2heap"),
        ],
    },
    "osint/people-org/index.md": {
        "title": "People & Organization OSINT",
        "description": "Gather open-source intelligence on people and organizations.",
        "methodology": [
            "Search social profiles and job postings",
            "Review breach data responsibly",
            "Map corporate infrastructure from public records",
            "Document sources and legal boundaries",
        ],
        "tools": ["maltego", "theharvester", "recon-ng"],
        "resources": [
            ("OSINT Framework", "https://osintframework.com/"),
        ],
    },
    "osint/data-breach-search/index.md": {
        "title": "Data Breach Search",
        "description": "Check for credential exposure in breach datasets.",
        "methodology": [
            "Use authorized breach search services",
            "Validate findings before reporting",
            "Recommend password resets and MFA",
            "Never exploit leaked credentials outside scope",
        ],
        "tools": ["have i been pwned api", "dehashed (authorized)"],
        "resources": [],
    },
    "social-engineering/phishing/index.md": {
        "title": "Phishing Assessments",
        "description": "Authorized phishing simulations for security awareness.",
        "methodology": [
            "Obtain written authorization",
            "Craft realistic but safe templates",
            "Track click and credential submission rates",
            "Provide training for affected users",
        ],
        "tools": ["gophish", "king phisher"],
        "resources": [],
    },
    "social-engineering/pretexting/index.md": {
        "title": "Pretexting & Vishing",
        "description": "Phone and in-person social engineering with strict authorization.",
        "methodology": [
            "Define allowed pretexts in ROE",
            "Record outcomes without harming staff",
            "Test help desk verification procedures",
            "Debrief with blue team after exercise",
        ],
        "tools": ["custom scripts"],
        "resources": [],
    },
    "iot/firmware-analysis/index.md": {
        "title": "Firmware Analysis",
        "description": "Extract and analyze embedded device firmware.",
        "methodology": [
            "Obtain firmware from vendor or UART",
            "Extract file systems with binwalk",
            "Search for hardcoded credentials",
            "Identify vulnerable services",
        ],
        "tools": ["binwalk", "firmadyne", "ghidra"],
        "resources": [],
    },
    "iot/hardware-interfaces/index.md": {
        "title": "Hardware Interfaces",
        "description": "Interact with UART, JTAG, and SPI on embedded devices.",
        "methodology": [
            "Identify debug pads on PCB",
            "Connect logic analyzer or bus pirate",
            "Dump firmware via UART",
            "Follow electrostatic and safety precautions",
        ],
        "tools": ["bus pirate", "jtagulator", "logic analyzer"],
        "resources": [],
    },
    "web3/smart-contracts/index.md": {
        "title": "Smart Contract Auditing",
        "description": "Review Solidity and EVM contracts for common vulnerabilities.",
        "methodology": [
            "Check reentrancy and access control",
            "Review oracle and price manipulation risks",
            "Test with Foundry or Hardhat",
            "Use static analyzers for baseline coverage",
        ],
        "tools": ["slither", "mythril", "foundry", "echidna"],
        "resources": [
            ("SWC Registry", "https://swcregistry.io/"),
        ],
    },
    "web3/wallet-dapp/index.md": {
        "title": "Wallet & dApp Security",
        "description": "Test wallet connectors and decentralized application frontends.",
        "methodology": [
            "Review transaction signing flows",
            "Test for phishing via malicious approvals",
            "Check frontend integrity and CSP",
            "Validate chain ID and contract address display",
        ],
        "tools": ["burp", "wallet simulators"],
        "resources": [],
    },
    "forensics/disk-memory/index.md": {
        "title": "Disk & Memory Forensics",
        "description": "Acquire and analyze disk images and memory dumps.",
        "methodology": [
            "Create forensic images with write blockers",
            "Parse filesystem artifacts",
            "Extract processes and network connections from memory",
            "Maintain chain of custody",
        ],
        "tools": ["ftk imager", "volatility", "autopsy"],
        "resources": [],
    },
    "forensics/network/index.md": {
        "title": "Network Forensics",
        "description": "Analyze PCAPs and network logs during investigations.",
        "methodology": [
            "Extract IoCs from packet captures",
            "Rebuild sessions and file transfers",
            "Correlate firewall and proxy logs",
            "Timeline attacker activity",
        ],
        "tools": ["wireshark", "zeek", "networkminer"],
        "resources": [],
    },
    "forensics/cloud/index.md": {
        "title": "Cloud Forensics",
        "description": "Investigate incidents in cloud environments.",
        "methodology": [
            "Collect CloudTrail and audit logs",
            "Snapshot volumes and memory where supported",
            "Trace IAM session activity",
            "Preserve evidence across regions",
        ],
        "tools": ["aws cli", "azure monitor", "gcp logging"],
        "resources": [],
    },
    "secure-code-review/sast/index.md": {
        "title": "SAST & Manual Code Review",
        "description": "Combine static analysis with manual review for vulnerability discovery.",
        "methodology": [
            "Run SAST tools on repositories",
            "Triage false positives manually",
            "Trace data flow for high-risk sinks",
            "Review authz checks on sensitive operations",
        ],
        "tools": ["semgrep", "codeql", "sonarqube"],
        "resources": [
            ("OWASP Code Review Guide", "https://owasp.org/www-project-code-review-guide/"),
        ],
    },
    "secure-code-review/threat-modeling/index.md": {
        "title": "Threat Modeling",
        "description": "Identify threats using structured modeling approaches.",
        "methodology": [
            "Diagram data flows and trust boundaries",
            "Apply STRIDE per component",
            "Prioritize threats by risk",
            "Define mitigations and test cases",
        ],
        "tools": ["draw.io", "microsoft threat modeling tool", "owasp threat dragon"],
        "resources": [
            ("OWASP Threat Modeling", "https://owasp.org/www-community/Threat_Modeling"),
        ],
    },
}


def render_page(meta: dict) -> str:
    lines = [f"# {meta['title']}", "", meta["description"], ""]
    lines += ["## Methodology", ""]
    for step in meta.get("methodology", []):
        lines.append(f"- [ ] {step}")
    lines.append("")
    if meta.get("tools"):
        lines += ["## Tools", ""]
        for tool in meta["tools"]:
            lines.append(f"- `{tool}`")
        lines.append("")
    if meta.get("resources"):
        lines += ["## Resources", ""]
        for name, url in meta["resources"]:
            lines.append(f"- [{name}]({url})")
        lines.append("")
    lines += [
        "## Checklist",
        "",
        "- [ ] Review scope and rules of engagement",
        "- [ ] Document baseline behavior",
        "- [ ] Test edge cases and parser differentials",
        "- [ ] Capture proof-of-concept safely",
        "- [ ] Write remediation guidance",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    for rel_path, meta in STRUCTURE.items():
        path = DOCS / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if meta is None:
            continue
        path.write_text(render_page(meta), encoding="utf-8")
    print(f"Generated {len([k for k, v in STRUCTURE.items() if v is not None])} pages")


if __name__ == "__main__":
    main()
