from diagrams._base import STYLE

BUG_BOUNTY_DIAGRAMS = {
    "bug-bounty/recon": f"""
flowchart LR
    subgraph Sources["Passive Sources"]
        CT[CT Logs] --> E[Enumerate]
        DNS[DNS/WHOIS] --> E
        OSINT[OSINT APIs] --> E
    end
    E --> T{{Tools}}
    T --> SF[subfinder] & AM[amass] & GAU[gau]
    SF & AM & GAU --> LIVE
    LIVE --> NU --> R[Findings Report]
""",
    "bug-bounty/subdomain-enumeration": """
flowchart TD
    A[Root Domain] --> P[Passive Enum]
    A --> B[Brute Force]
    P --> CT[crt.sh / CT logs]
    P --> API[DNS APIs]
    B --> WL[Wordlists]
    CT & API & WL --> R[Resolve with dnsx]
    R --> V[Validate live subs]
""",
    "bug-bounty/asset-discovery": """
flowchart LR
    SUB[Subdomains] --> ASN[ASN / IP ranges]
    ASN --> PORT[Port scan]
    PORT --> HTTP[HTTP probe]
    HTTP --> CRAWL[katana crawl]
    CRAWL --> API[API endpoints]
    CRAWL --> STG[Staging / dev assets]
    API & STG --> INV[Asset inventory]
""",
    "bug-bounty/port-scanning": """
flowchart TD
    H[Live hosts] --> TOP[Top 1000 ports]
    TOP --> FULL[Full port on targets]
    FULL --> FP[Service fingerprint]
    FP --> ADMIN{Admin panels?}
    ADMIN -->|yes| FLAG[High priority]
    ADMIN -->|no| LOG[Document services]
""",
    "bug-bounty/http-probing": """
flowchart LR
    HOSTS[Host list] --> HX[httpx]
    HX --> SC[Status codes]
    HX --> TT[Page titles]
    HX --> TD[Tech detect]
    SC & TT & TD --> LIVE[Live web map]
    LIVE --> NU[nuclei templates]
""",
    "bug-bounty/dns-enumeration": """
flowchart TD
    D[Domain] --> REC[Record types]
    REC --> A[A/AAAA]
    REC --> MX[MX]
    REC --> TXT[TXT/SPF]
    REC --> NS[NS]
    REC --> AXFR{AXFR open?}
    AXFR -->|yes| ZONE[Zone transfer dump]
    A & MX & TXT & NS --> MAP[DNS map]
""",
    "bug-bounty/tech-detection": """
flowchart LR
    URL[URLs] --> WW[whatweb / httpx]
    WW --> STACK[Frameworks & versions]
    STACK --> CVE[Known CVEs]
    STACK --> MIS[Misconfig templates]
    CVE & MIS --> NU[nuclei targeted scan]
""",
}
