WEB_DIAGRAMS = {
    "web/sqli": """
flowchart TD
    subgraph Input["① User Input"]
        U[Attacker controlled parameter]
    end
    subgraph Vuln["② Vulnerable Code"]
        APP[String concatenation into SQL]
    end
    subgraph DBLayer["③ Database"]
        DB[(SQL Engine executes injected syntax)]
    end
    subgraph Impact["④ Impact"]
        OUT[Data leak / Auth bypass / RCE]
    end
    U --> APP --> DB --> OUT
    class U attacker
    class APP,DB target
    class OUT warn
""",
    "web/xss": """
flowchart TD
    IN[Malicious input] --> STORED{Stored or reflected?}
    STORED -->|stored| DB[(Database)]
    STORED -->|reflected| RESP[HTTP response]
    DB --> VICTIM[Victim browser]
    RESP --> VICTIM
    VICTIM --> JS[Execute attacker JS]
    JS --> COOK[Steal session / actions]
""",
    "web/ssrf": """
flowchart LR
    A[Attacker] -->|crafted URL| APP[Server-side fetch]
    APP --> INT[Internal services]
    APP --> META[Cloud metadata 169.254.169.254]
    APP --> OOB[OOB via interactsh]
    INT & META & OOB --> IMPACT[Data / pivot]
""",
    "web/idor": """
flowchart TD
    AUTH[Authenticated user] --> REQ[Request object by ID]
    REQ --> APP{Authorization check?}
    APP -->|missing| LEAK[Other user's data]
    APP -->|present| OK[Access denied]
""",
    "web/ssti": """
flowchart LR
    IN[Template input] --> ENG[Template engine]
    ENG --> EXEC[Server-side code exec]
    EXEC --> RCE[Read files / shell]
""",
    "web/lfi-rfi": """
flowchart TD
    PARAM[File parameter] --> LFI{Local or remote?}
    LFI -->|local| READ[/etc/passwd, configs]
    LFI -->|remote| RFI[Host malicious PHP]
    READ --> ESC[Log poison / RCE chain]
    RFI --> SHELL[Web shell]
""",
    "web/xxe": """
flowchart LR
    XML[Malicious XML] --> PARSER[XML parser]
    PARSER --> FILE[Local file read]
    PARSER --> SSRF[SSRF to internal]
    PARSER --> DOS[Billion laughs DoS]
""",
    "web/deserialization": """
flowchart TD
    SER[Serialized object] --> APP[App unmarshals]
    APP --> GADGET[Gadget chain]
    GADGET --> RCE[Remote code execution]
""",
    "web/race-condition": """
sequenceDiagram
    participant A as Attacker
    participant S as Server
    participant DB as Database
    par Parallel requests
        A->>S: Transfer $100
        A->>S: Transfer $100
    end
    S->>DB: Check balance once
    DB-->>S: OK
    S->>DB: Double spend
""",
    "web/open-redirect": """
flowchart LR
    LINK[redirect?url=] --> APP[App redirects]
    APP --> PHISH[Attacker domain]
    PHISH --> STEAL[Credential harvest]
""",
    "web/prototype-pollution": """
flowchart TD
    JSON[__proto__ payload] --> MERGE[Object merge]
    MERGE --> POLL[Prototype polluted]
    POLL --> AUTH[Bypass auth checks]
    POLL --> RCE[Template / RCE gadgets]
""",
    "web/cors": """
flowchart LR
    EVIL[evil.com] --> BROWSER[Victim browser]
    BROWSER -->|Origin: evil.com| API[API with ACAO: *]
    API --> DATA[Sensitive JSON]
    DATA --> EVIL
""",
    "web/clickjacking": """
flowchart TD
    ATT[Attacker page] --> IFRAME[Invisible iframe]
    IFRAME --> VICTIM[Victim clicks visible button]
    VICTIM --> ACTION[Hidden action on bank.com]
""",
    "web/http-request-smuggling": """
flowchart LR
    FE[Front-end server] --> BE[Back-end server]
    A[Smuggled request] --> FE
    FE -->|desync| BE
    BE --> HIJACK[Poison next user's request]
""",
    "web/web-cache-poisoning": """
flowchart TD
    A[Attacker] -->|unkeyed header/param| CACHE[CDN cache]
    CACHE --> STORE[Stores poisoned response]
    STORE --> VICTIM[All users get XSS/redirect]
""",
    "web/business-logic": """
flowchart TD
    FLOW[Normal purchase flow] --> ABUSE[Skip / reorder steps]
    ABUSE --> NEG[Negative price]
    ABUSE --> COUP[Coupon stacking]
    ABUSE --> ROLE[Privilege via workflow]
""",
    "web/crlf-injection": """
flowchart LR
    CRLF[%0d%0a injected] --> RESP[HTTP response headers]
    RESP --> SPLIT[Response splitting]
    SPLIT --> XSS[Reflected XSS]
    SPLIT --> CACHE[Cache poison]
""",
    "web/command-injection": """
flowchart LR
    IN[; | && payload] --> SHELL[OS shell invoked]
    SHELL --> EXEC[id, cat /etc/passwd]
""",
    "web/nosql-injection": """
flowchart TD
    JSON[$ne / $gt operators] --> NOSQL[(MongoDB query)]
    NOSQL --> BYPASS[Auth bypass]
    NOSQL --> LEAK[Data extraction]
""",
    "web/http-parameter-pollution": """
flowchart LR
    DUP[id=1&id=2] --> FE[Front-end uses first]
    DUP --> BE[Back-end uses last]
    FE & BE --> BYPASS[Auth / logic bypass]
""",
    "web/websockets": """
flowchart TD
    WS[WebSocket connection] --> MSG[Messages]
    MSG --> AUTH{Per-message auth?}
    AUTH -->|no| IDOR[Subscribe to others' channels]
    AUTH -->|no| INJ[SQL/cmd in message handler]
""",
    "web/information-disclosure": """
flowchart LR
    SRC[Git / .env / backups] --> SCAN[trufflehog / nuclei]
    SCAN --> SECRETS[API keys & creds]
    SECRETS --> ABUSE[Account takeover]
""",
    "web/ldap-xpath-injection": """
flowchart LR
    IN[LDAP filter input] --> QUERY[(Directory query)]
    QUERY --> BYPASS[Auth bypass]
    QUERY --> ENUM[User enumeration]
""",
    "web/dom-clobbering": """
flowchart TD
    HTML[Named DOM nodes] --> CLOB[Overwrite window.config]
    CLOB --> GADGET[Gadget in trusted script]
    GADGET --> XSS[XSS / data leak]
""",
}
