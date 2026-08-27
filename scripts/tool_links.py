"""Tool link registry and MkDocs-safe relative link helpers."""

from __future__ import annotations

from pathlib import Path

# Anchors that exist as ### headers in docs/TOOLS_GUIDE.md
GUIDE_ANCHORS: frozenset[str] = frozenset({
    "subfinder", "httpx", "nuclei", "naabu", "gau", "katana",
    "burp-suite", "ffuf", "sqlmap", "dalfox", "jwt_tool", "commix",
    "kiterunner-kr", "grpcurl", "jadx", "frida-objection",
    "nmap", "crackmapexec-netexec", "impacket", "bloodhound", "prowler", "pacu",
    "trufflehog", "gitleaks", "semgrep",
    "drawio", "microsoft-threat-modeling-tool", "owasp-threat-dragon",
    "amass", "assetfinder", "waybackurls", "dnsx",
    "owasp-zap", "tplmap", "xsstrike", "autorize", "linkfinder", "smuggler",
    "ssrfmap", "ghauri", "nosqlmap", "openredirex", "corsy", "crlfuzz", "ppmap",
    "param-miner", "web-cache-vulnerability-scanner", "lfi-suite", "h2csmuggler",
    "race-the-web", "ws-harness", "xxeinjector", "oxmlxxe", "ysoserial", "phpggc",
    "gophish", "recon-ng", "sonarqube",
    "slither", "foundry", "echidna", "mythril",
    "rubeus", "mimikatz", "responder", "linpeas", "winpeas",
    "scout-suite", "kube-hunter", "trivy", "checkov",
    "codeql", "ghidra", "binwalk", "volatility",
    "bbscope", "interactsh", "testsslsh", "clairvoyance", "apktool", "mobsf",
})


def docs_relpath(from_file: str, to_file: str) -> str:
    """Return a relative markdown path between two docs files."""
    from_dir = Path(from_file).parent
    to_path = Path(to_file)
    try:
        rel = Path(os_path_relpath(from_dir, to_path.parent)) / to_path.name
    except ValueError:
        rel = to_path
    return rel.as_posix()


def os_path_relpath(from_dir: Path, to_dir: Path) -> str:
    """Pure-path relpath without requiring paths to exist on disk."""
    from_parts = from_dir.parts
    to_parts = to_dir.parts
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a != b:
            break
        common += 1
    up = [".."] * (len(from_parts) - common)
    down = list(to_parts[common:])
    return "/".join(up + down) if up or down else "."


def guide_link(from_file: str, anchor: str | None = None) -> str:
    path = docs_relpath(from_file, "TOOLS_GUIDE.md")
    return f"{path}#{anchor}" if anchor else path


# guide: anchor slug in TOOLS_GUIDE.md (### header)
# url: official project/docs link when not covered in guide
# label: short link text for topic tables
TOOL_REGISTRY: dict[str, dict[str, str]] = {
    # Recon
    "subfinder": {"guide": "subfinder", "label": "Passive subdomain discovery"},
    "amass": {"guide": "amass", "url": "https://github.com/owasp-amass/amass", "label": "OSINT & subdomain enum"},
    "assetfinder": {"guide": "assetfinder", "url": "https://github.com/tomnomnom/assetfinder", "label": "Related domains & subdomains"},
    "httpx": {"guide": "httpx", "label": "HTTP probing & tech detection"},
    "httpx -tech-detect": {"guide": "httpx", "label": "Technology fingerprinting"},
    "naabu": {"guide": "naabu", "label": "Fast port scanner"},
    "nuclei": {"guide": "nuclei", "label": "Template-based vuln scanner"},
    "gau": {"guide": "gau", "label": "Archive URL collection"},
    "katana": {"guide": "katana", "label": "Web crawler"},
    "waybackurls": {"guide": "waybackurls", "url": "https://github.com/tomnomnom/waybackurls", "label": "Wayback Machine URLs"},
    "dnsx": {"guide": "dnsx", "url": "https://github.com/projectdiscovery/dnsx", "label": "DNS toolkit"},
    "puredns": {"guide": "puredns", "url": "https://github.com/d3mondev/puredns", "label": "DNS resolver & wildcard filter"},
    "massdns": {"guide": "massdns", "url": "https://github.com/blechschmidt/massdns", "label": "High-performance DNS stub"},
    "shuffledns": {"guide": "shuffledns", "url": "https://github.com/projectdiscovery/shuffledns", "label": "Subdomain brute force"},
    "asnmap": {"guide": "asnmap", "url": "https://github.com/projectdiscovery/asnmap", "label": "ASN mapping"},
    "mapcidr": {"guide": "mapcidr", "url": "https://github.com/projectdiscovery/mapcidr", "label": "CIDR expansion"},
    "whatweb": {"guide": "whatweb", "url": "https://github.com/urbanadventurer/WhatWeb", "label": "Web technology fingerprinting"},
    "wappalyzer": {"guide": "wappalyzer", "url": "https://www.wappalyzer.com/", "label": "Stack detection"},
    "theharvester": {"guide": "theharvester", "url": "https://github.com/laramies/theHarvester", "label": "Email & subdomain OSINT"},
    "recon-ng": {"guide": "recon-ng", "url": "https://github.com/lanmaster53/recon-ng", "label": "OSINT framework"},
    "maltego": {"guide": "maltego", "url": "https://www.maltego.com/", "label": "Link analysis & OSINT"},
    # Web
    "burp": {"guide": "burp-suite", "label": "Intercept, repeater & scanner"},
    "burp turbo intruder": {"guide": "burp-suite", "label": "Race condition & burst attacks"},
    "burp grpc assistant": {"guide": "burp-suite", "label": "gRPC testing in Burp"},
    "ffuf": {"guide": "ffuf", "label": "Web fuzzer"},
    "sqlmap": {"guide": "sqlmap", "label": "Automated SQL injection"},
    "ghauri": {"guide": "ghauri", "url": "https://github.com/r0oth3x49/ghauri", "label": "SQL injection tool"},
    "dalfox": {"guide": "dalfox", "label": "XSS scanner"},
    "xsstrike": {"guide": "xsstrike", "url": "https://github.com/s0md3v/XSStrike", "label": "XSS detection"},
    "commix": {"guide": "commix", "label": "Command injection"},
    "jwt_tool": {"guide": "jwt_tool", "label": "JWT analysis & attacks"},
    "tplmap": {"guide": "tplmap", "url": "https://github.com/epinna/tplmap", "label": "Server-side template injection"},
    "interactsh": {"guide": "interactsh", "label": "Out-of-band interaction server"},
    "owasp zap": {"guide": "owasp-zap", "url": "https://www.zaproxy.org/", "label": "Open-source web scanner"},
    "smuggler": {"guide": "smuggler", "url": "https://github.com/defparam/smuggler", "label": "HTTP request smuggling"},
    "h2csmuggler": {"guide": "h2csmuggler", "url": "https://github.com/nccgroup/h2csmuggler", "label": "H2C smuggling detection"},
    "ssrfmap": {"guide": "ssrfmap", "url": "https://github.com/swisskyrepo/SSRFmap", "label": "SSRF exploitation"},
    "nosqlmap": {"guide": "nosqlmap", "url": "https://github.com/codingo/NoSQLMap", "label": "NoSQL injection"},
    "openredirex": {"guide": "openredirex", "url": "https://github.com/devanshbatham/OpenRedireX", "label": "Open redirect fuzzer"},
    "param-miner": {"guide": "param-miner", "url": "https://github.com/portswigger/param-miner", "label": "Hidden parameter discovery"},
    "web-cache-vulnerability-scanner": {
        "guide": "web-cache-vulnerability-scanner",
        "url": "https://github.com/Hackmanit/Web-Cache-Vulnerability-Scanner",
        "label": "Cache poisoning scanner",
    },
    "lfi-suite": {"guide": "lfi-suite", "url": "https://github.com/D35m0nd142/LFISuite", "label": "LFI exploitation"},
    "autorize": {"guide": "autorize", "url": "https://github.com/Quitten/Autorize", "label": "Authorization testing (Burp)"},
    "linkfinder": {"guide": "linkfinder", "url": "https://github.com/GerbenJavado/LinkFinder", "label": "JS endpoint discovery"},
    "corsy": {"guide": "corsy", "url": "https://github.com/s0md3v/Corsy", "label": "CORS misconfiguration scan"},
    "corscanner": {"guide": "corsy", "label": "CORS misconfiguration scan"},
    "crlfuzz": {"guide": "crlfuzz", "url": "https://github.com/dwisiswant0/crlfuzz", "label": "CRLF injection fuzzer"},
    "ppmap": {"guide": "ppmap", "url": "https://github.com/RhinoSecurityLabs/ppmap", "label": "Prototype pollution scanner"},
    "xxeinjector": {"guide": "xxeinjector", "url": "https://github.com/enjoiz/XXEinjector", "label": "XXE payload generator"},
    "oxmlxxe": {"guide": "oxmlxxe", "url": "https://github.com/Bo0oM/oxml_xxe", "label": "Office XML XXE"},
    "race-the-web": {"guide": "race-the-web", "url": "https://github.com/TheHackerDev/race-the-web", "label": "Race condition testing"},
    "ws-harness": {"guide": "ws-harness", "url": "https://github.com/PortSwigger/ws-harness", "label": "WebSocket testing"},
  # API
    "kiterunner": {"guide": "kiterunner-kr", "label": "API route brute force"},
    "grpcurl": {"guide": "grpcurl", "label": "gRPC CLI client"},
    "clairvoyance": {"guide": "clairvoyance", "url": "https://github.com/jakob-p/clairvoyance", "label": "GraphQL schema recovery"},
    "inql": {"guide": "inql", "url": "https://github.com/doyensec/inql", "label": "GraphQL security (Burp)"},
    "graphql-cop": {"guide": "graphql-cop", "url": "https://github.com/dolevf/graphql-cop", "label": "GraphQL security audit"},
    "graphql-voyager": {"guide": "graphql-voyager", "url": "https://github.com/graphql-kit/graphql-voyager", "label": "Schema visualization"},
    # Mobile
    "jadx": {"guide": "jadx", "label": "Android decompiler"},
    "apktool": {"guide": "apktool", "url": "https://github.com/iBotPeaches/Apktool", "label": "APK reverse engineering"},
    "mobsf": {"guide": "mobsf", "url": "https://github.com/MobSF/Mobile-Security-Framework-MobSF", "label": "Mobile security framework"},
    "frida": {"guide": "frida-objection", "label": "Dynamic instrumentation"},
    "objection": {"guide": "frida-objection", "label": "Runtime mobile exploration"},
    "r2frida": {"guide": "frida-objection", "url": "https://github.com/nowsecure/r2frida", "label": "Radare2 + Frida bridge"},
    "adb": {"guide": "adb", "url": "https://developer.android.com/tools/adb", "label": "Android Debug Bridge"},
    "apk-mitm": {"guide": "apk-mitm", "url": "https://github.com/shroudedcode/apk-mitm", "label": "Patch APK for MITM"},
    # Network / AD
    "nmap": {"guide": "nmap", "label": "Network scanner"},
    "masscan": {"guide": "masscan", "url": "https://github.com/robertdavidgraham/masscan", "label": "High-speed port scanner"},
    "rustscan": {"guide": "rustscan", "url": "https://github.com/RustScan/RustScan", "label": "Fast port scanner"},
    "crackmapexec": {"guide": "crackmapexec-netexec", "label": "Network pentest swiss army knife"},
    "impacket": {"guide": "impacket", "label": "Network protocol tools"},
    "impacket getuserspns": {"guide": "impacket", "label": "Kerberoasting with GetUserSPNs"},
    "impacket secretsdump": {"guide": "impacket", "label": "DCSync / credential dumping"},
    "bloodhound": {"guide": "bloodhound", "label": "AD attack path analysis"},
    "bloodhound.py": {"guide": "bloodhound", "label": "BloodHound ingestor (Python)"},
    "sharphound": {"guide": "bloodhound", "url": "https://github.com/BloodHoundAD/SharpHound", "label": "BloodHound collector"},
    "rubeus": {"guide": "rubeus", "url": "https://github.com/GhostPack/Rubeus", "label": "Kerberos abuse toolkit"},
    "mimikatz": {"guide": "mimikatz", "url": "https://github.com/gentilkiwi/mimikatz", "label": "Credential extraction"},
    "responder": {"guide": "responder", "url": "https://github.com/lgandx/Responder", "label": "LLMNR/NBT-NS poisoning"},
    "enum4linux-ng": {"guide": "enum4linux-ng", "url": "https://github.com/cddmp/enum4linux-ng", "label": "SMB/LDAP enumeration"},
    "evil-winrm": {"guide": "evil-winrm", "url": "https://github.com/Hackplayers/evil-winrm", "label": "WinRM shell"},
    "powerview": {"guide": "powerview", "url": "https://github.com/PowerShellMafia/PowerSploit", "label": "AD situational awareness"},
    "linpeas": {"guide": "linpeas", "url": "https://github.com/carlospolop/PEASS-ng", "label": "Linux privesc enumeration"},
    "winpeas": {"guide": "winpeas", "url": "https://github.com/carlospolop/PEASS-ng", "label": "Windows privesc enumeration"},
    "linux-exploit-suggester": {
        "guide": "linux-exploit-suggester",
        "url": "https://github.com/mzet-/linux-exploit-suggester",
        "label": "Kernel exploit suggestions",
    },
    "powerup": {"guide": "powerup", "url": "https://github.com/PowerShellMafia/PowerSploit", "label": "Windows privesc checks"},
    "watson": {"guide": "watson", "url": "https://github.com/rasta-mouse/Watson", "label": "Windows patch enumeration"},
    "hashcat": {"guide": "hashcat", "url": "https://hashcat.net/hashcat/", "label": "Password cracking"},
    "aircrack-ng": {"guide": "aircrack-ng", "url": "https://www.aircrack-ng.org/", "label": "Wi-Fi security auditing"},
    "bettercap": {"guide": "bettercap", "url": "https://github.com/bettercap/bettercap", "label": "Network attack & monitoring"},
    "kismet": {"guide": "kismet", "url": "https://www.kismetwireless.net/", "label": "Wireless network detector"},
    "hping3": {"guide": "hping3", "url": "https://github.com/antirez/hping", "label": "Firewall probing"},
    # Cloud
    "pacu": {"guide": "pacu", "label": "AWS exploitation framework"},
    "prowler": {"guide": "prowler", "label": "Cloud security assessment"},
    "scout suite": {"guide": "scout-suite", "url": "https://github.com/nccgroup/ScoutSuite", "label": "Multi-cloud audit"},
    "cloudfox": {"guide": "cloudfox", "url": "https://github.com/BishopFox/cloudfox", "label": "AWS situational awareness"},
    "kube-hunter": {"guide": "kube-hunter", "url": "https://github.com/aquasecurity/kube-hunter", "label": "Kubernetes pentest"},
    "kubectl": {"guide": "kubectl", "url": "https://kubernetes.io/docs/reference/kubectl/", "label": "Kubernetes CLI"},
    "kubescape": {"guide": "kubescape", "url": "https://github.com/kubescape/kubescape", "label": "K8s security posture"},
    "roadtools": {"guide": "roadtools", "url": "https://github.com/dirkjanm/ROADtools", "label": "Azure AD exploration"},
    "azurehound": {"guide": "azurehound", "url": "https://github.com/BloodHoundAD/AzureHound", "label": "Azure BloodHound collector"},
    "microburst": {"guide": "microburst", "url": "https://github.com/NetSPI/MicroBurst", "label": "Azure security assessment"},
    "gcp_scanner": {"guide": "gcp-scanner", "url": "https://github.com/google/gcp_scanner", "label": "GCP misconfiguration scan"},
    # Secrets / SAST
    "trufflehog": {"guide": "trufflehog", "label": "Secret scanner"},
    "gitleaks": {"guide": "gitleaks", "label": "Git secret scanner"},
    "semgrep": {"guide": "semgrep", "label": "Static analysis (SAST)"},
    "codeql": {"guide": "codeql", "url": "https://github.com/github/codeql", "label": "Semantic code analysis"},
    "sonarqube": {"guide": "sonarqube", "url": "https://www.sonarqube.org/", "label": "Code quality & security"},
    # Threat modeling
    "draw.io": {"guide": "drawio", "url": "https://www.drawio.com/", "label": "Data-flow & architecture diagrams"},
    "microsoft threat modeling tool": {
        "guide": "microsoft-threat-modeling-tool",
        "url": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool",
        "label": "STRIDE threat modeling (Windows)",
    },
    "owasp threat dragon": {
        "guide": "owasp-threat-dragon",
        "url": "https://owasp.org/www-project-threat-dragon/",
        "label": "OWASP threat modeling",
    },
    # Web3
    "slither": {"guide": "slither", "url": "https://github.com/crytic/slither", "label": "Solidity static analyzer"},
    "mythril": {"guide": "mythril", "url": "https://github.com/ConsenSys/mythril", "label": "EVM bytecode analysis"},
    "foundry": {"guide": "foundry", "url": "https://github.com/foundry-rs/foundry", "label": "Smart contract dev & testing"},
    "echidna": {"guide": "echidna", "url": "https://github.com/crytic/echidna", "label": "Smart contract fuzzer"},
    # Binary / forensics
    "ghidra": {"guide": "ghidra", "url": "https://ghidra-sre.org/", "label": "Reverse engineering suite"},
    "binwalk": {"guide": "binwalk", "url": "https://github.com/ReFirmLabs/binwalk", "label": "Firmware analysis"},
    "volatility": {"guide": "volatility", "url": "https://github.com/volatilityfoundation/volatility", "label": "Memory forensics"},
    "wireshark": {"guide": "wireshark", "url": "https://www.wireshark.org/", "label": "Packet analysis"},
    "pwntools": {"guide": "pwntools", "url": "https://github.com/Gallopsled/pwntools", "label": "Exploit development"},
    # Containers / DevSecOps
    "trivy": {"guide": "trivy", "url": "https://github.com/aquasecurity/trivy", "label": "Container vulnerability scan"},
    "checkov": {"guide": "checkov", "url": "https://github.com/bridgecrewio/checkov", "label": "IaC security scanner"},
    "tfsec": {"guide": "tfsec", "url": "https://github.com/aquasecurity/tfsec", "label": "Terraform security scanner"},
    "kics": {"guide": "kics", "url": "https://github.com/Checkmarx/kics", "label": "IaC security (multi-cloud)"},
    "syft": {"guide": "syft", "url": "https://github.com/anchore/syft", "label": "SBOM generator"},
    "cosign": {"guide": "cosign", "url": "https://github.com/sigstore/cosign", "label": "Container signing"},
    # Blue team
    "sigma": {"guide": "sigma", "url": "https://github.com/SigmaHQ/sigma", "label": "Detection rule format"},
    "velociraptor": {"guide": "velociraptor", "url": "https://github.com/Velocidex/velociraptor", "label": "Endpoint visibility"},
    "sysmon": {"guide": "sysmon", "url": "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "label": "Windows monitoring"},
    "atomic red team": {"guide": "atomic-red-team", "url": "https://github.com/redcanaryco/atomic-red-team", "label": "Detection validation"},
  # Utility
    "bbscope": {"guide": "bbscope", "label": "Bug bounty scope aggregation"},
    "testssl.sh": {"guide": "testsslsh", "label": "TLS configuration testing"},
    "sslscan": {"guide": "sslscan", "url": "https://github.com/rbsec/sslscan", "label": "SSL/TLS scanner"},
    "sslyze": {"guide": "sslyze", "url": "https://github.com/nabla-c0d3/sslyze", "label": "TLS configuration analysis"},
    "ysoserial": {"guide": "ysoserial", "url": "https://github.com/frohoff/ysoserial", "label": "Java deserialization payloads"},
    "phpggc": {"guide": "phpggc", "url": "https://github.com/ambionics/phpggc", "label": "PHP deserialization payloads"},
    "padbuster": {"guide": "padbuster", "url": "https://github.com/AonCyberLabs/PadBuster", "label": "Padding oracle attacks"},
    "gophish": {"guide": "gophish", "url": "https://github.com/gophish/gophish", "label": "Phishing campaign framework"},
    "king phisher": {"guide": "gophish", "url": "https://github.com/rsmusllp/king-phisher", "label": "Phishing campaigns"},
}

# Generic / manual techniques — describe inline instead of linking to a missing guide entry
GENERIC_TOOLS: dict[str, str] = {
    "manual testing": "Hands-on business logic testing with Burp Repeater",
    "manual fuzzing": "Custom wordlists and Burp Intruder payloads",
    "manual payloads": "Craft payloads from OWASP cheat sheets",
    "custom scripts": "Python/Bash automation for repeatable tests",
    "custom probes": "ICMP/TCP probes to map firewall rules",
    "custom html poc": "Minimal HTML page demonstrating clickjacking",
    "custom spreadsheets": "Track assets, findings, and retest status",
    "dom clobbering scanners": "Browser DevTools + DOM XSS sinks review",
    "dompurify bypass research": "Review DOMPurify bypass advisories & test sinks",
    "python asyncio": "Async HTTP for race condition PoCs",
    "markdown": "Write reports in Markdown for GitHub/HackerOne",
    "cvss calculator": "Score severity with [FIRST CVSS calculator](https://www.first.org/cvscalc/)",
    "obsidian": "Personal knowledge base for writeups & notes",
    "wallet simulators": "Test dApp flows in local EVM simulators",
    "dehashed (authorized)": "Authorized breach monitoring services only",
    "have i been pwned api": "Defensive credential exposure checks via [HIBP API](https://haveibeenpwned.com/API/v3)",
    "cisa kev": "Known exploited vulns — [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)",
    "vulners": "Vuln intelligence — [vulners.com](https://vulners.com/)",
    "github actions": "CI/CD pipeline security review",
    "gitlab ci": "Pipeline config & secret exposure review",
    "snyk": "Dependency scanning — [snyk.io](https://snyk.io/)",
    "dependabot": "GitHub dependency alerts & automated PRs",
    "aws cli": "Cloud forensics with `aws cloudtrail lookup-events`",
    "azure monitor": "Azure log analytics & Sentinel queries",
    "gcp logging": "Cloud Logging & Chronicle investigation",
    "ftk imager": "Disk imaging — [AccessData FTK](https://www.exterro.com/ftk-imager)",
    "autopsy": "Digital forensics — [Autopsy](https://www.autopsy.com/)",
    "zeek": "Network security monitoring — [zeek.org](https://zeek.org/)",
    "networkminer": "Network forensics — [networkminer.com](https://www.networkminer.com/)",
    "bus pirate": "Hardware hacking — [dangerousprototypes.com](http://dangerousprototypes.com/docs/Bus_Pirate)",
    "jtagulator": "JTAG/UART discovery — [Grand Idea Studio](https://www.grandideastudio.com/jtagulator)",
    "logic analyzer": "Signal analysis with Saleae or PulseView",
    "firmadyne": "Firmware emulation — [Firmadyne](https://github.com/firmadyne/firmadyne)",
    "deepce": "Container escape enumeration",
    "cdk": "Container penetration toolkit — [cdk](https://github.com/cdk-team/CDK)",
    "docker bench": "Docker CIS benchmark — [docker-bench-security](https://github.com/docker/docker-bench-security)",
    "grype": "Container vulnerability scanner — [Anchore Grype](https://github.com/anchore/grype)",
    "falco": "Runtime threat detection — [falco.org](https://falco.org/)",
    "kyverno": "Kubernetes policy engine — [kyverno.io](https://kyverno.io/)",
    "splunk": "SIEM search & correlation",
    "elastic": "Elastic Security SIEM & detection",
    "sentinel": "Microsoft Sentinel analytics",
    "chronicle": "Google Chronicle threat detection",
    "thehive": "Incident response case management",
    "cuckoo": "Malware sandbox analysis",
    "yara": "Malware detection rules — [virustotal.github.io/yara](https://virustotal.github.io/yara/)",
    "flare-vm": "Windows malware analysis VM — [FLARE-VM](https://github.com/mandiant/flare-vm)",
    "binary ninja": "Commercial reverse engineering — [binary.ninja](https://binary.ninja/)",
    "ida": "Interactive disassembler — [hex-rays.com](https://hex-rays.com/ida-pro/)",
    "radare2": "Open-source reversing — [rada.re](https://rada.re/n/)",
    "gdb": "GNU debugger for binary analysis",
    "gef": "GDB Enhanced Features — [hugsy/gef](https://github.com/hugsy/gef)",
    "pwndbg": "GDB plugin for exploit dev — [pwndbg/pwndbg](https://github.com/pwndbg/pwndbg)",
    "ropper": "ROP gadget finder — [sashs/Ropper](https://github.com/sashs/Ropper)",
    "heap exploitation scripts": "Custom heap feng shui PoCs for CTF targets",
    "hackerone cli": "HackerOne API CLI for program management",
    "aquatone": "Visual subdomain recon — [michenriksen/aquatone](https://github.com/michenriksen/aquatone)",
    "gowitness": "Screenshot live web hosts — [sensepost/gowitness](https://github.com/sensepost/gowitness)",
    "httprobe": "Legacy HTTP probe — prefer **httpx**",
    "dig": "DNS lookup — built into Linux/macOS",
    "dnsrecon": "DNS enumeration — [darkoperator/dnsrecon](https://github.com/darkoperator/dnsrecon)",
    "fierce": "DNS recon — [mschwager/fierce](https://github.com/mschwager/fierce)",
    "secretfinder": "JS secret extraction — [m4ll0k/SecretFinder](https://github.com/m4ll0k/SecretFinder)",
    "saml raider": "SAML testing Burp extension — [SAML Raider](https://github.com/SAMLRaider/SAMLRaider)",
    "grpcui": "gRPC web UI — [fullstorydev/grpcui](https://github.com/fullstorydev/grpcui)",
}


def lookup_tool(tool: str) -> dict[str, str]:
    key = tool.strip().lower()
    if key in TOOL_REGISTRY:
        return TOOL_REGISTRY[key]
    if key in GENERIC_TOOLS:
        return {"label": GENERIC_TOOLS[key]}
    return {}


def format_tool_row(from_file: str, tool: str) -> str:
    info = lookup_tool(tool)
    label = info.get("label", "Install & usage")
    guide = info.get("guide")

    if guide and guide in GUIDE_ANCHORS:
        href = guide_link(from_file, guide)
        usage = f"[{label}]({href})"
    elif "http" in label or "[" in label:
        usage = label
    elif info.get("url"):
        usage = f"[{label}]({info['url']})"
    else:
        href = guide_link(from_file)
        usage = f"[{label}]({href})"

    return f"| `{tool}` | {usage} |"


def format_tools_guide_tip(from_file: str) -> str:
    href = guide_link(from_file)
    return f"See the [Tools Guide]({href}) for install instructions, all flags, and pro tips."
