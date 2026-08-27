SPECIALIZED_DIAGRAMS = {
    "blue-team/detection-engineering": """
flowchart LR
    LOGS[Log sources] --> NORM[Normalize]
    NORM --> RULE[Sigma / SPL rules]
    RULE --> SIEM[SIEM alerts]
    SIEM --> TUNE[Tune false positives]
    TUNE --> ATOMIC[Validate with Atomic Red Team]
""",
    "blue-team/siem-log-analysis": """
flowchart TD
    INGEST[Log ingestion] --> PARSE[Field extraction]
    PARSE --> QUERY[Correlation queries]
    QUERY --> ALERT[Alert triage]
    ALERT --> ESCALATE[Incident escalation]
""",
    "blue-team/threat-hunting": """
flowchart LR
    HYP[Hypothesis] --> DATA[Query endpoint / SIEM]
    DATA --> PATTERN[Anomaly pattern]
    PATTERN --> IOC[New IOC / detection rule]
""",
    "blue-team/incident-response": """
flowchart TD
    DETECT[Detection] --> TRIAGE[Triage severity]
    TRIAGE --> CONTAIN[Contain host / account]
    CONTAIN --> ERAD[Eradicate]
    ERAD --> RECOVER[Restore services]
    RECOVER --> LESSONS[Post-incident review]
""",
    "blue-team/malware-analysis": """
flowchart LR
    SAMPLE[Malware sample] --> STATIC[Static analysis]
    SAMPLE --> DYN[Sandbox / Cuckoo]
    STATIC & DYN --> IOC[IOCs & YARA rules]
    IOC --> BLOCK[Block in production]
""",
    "cryptography/crypto-flaws": """
flowchart TD
    APP[Application crypto] --> WEAK[Weak algorithms / keys]
    WEAK --> DECRYPT[Decrypt traffic / data]
    WEAK --> FORGE[Forge tokens / signatures]
""",
    "cryptography/padding-oracle": """
flowchart LR
    CIPHER[Ciphertext blocks] --> ORACLE[Padding error oracle]
    ORACLE --> BYTE[Decrypt byte-by-byte]
    BYTE --> PLAIN[Plaintext recovered]
""",
    "cryptography/tls-ssl": """
flowchart TD
    TLS[TLS config] --> SCAN[testssl.sh / sslyze]
    SCAN --> WEAK[Weak ciphers / protocols]
    WEAK --> MITM[Downgrade / MITM]
""",
    "devsecops/pipeline-security": """
flowchart LR
    CODE[Push code] --> CI[CI pipeline]
    CI --> SAST[SAST scan]
    CI --> DEPS[Dependency scan]
    SAST & DEPS --> GATE[Security gate]
    GATE --> DEPLOY[Deploy or block]
""",
    "devsecops/iac-security": """
flowchart TD
    TF[Terraform / K8s YAML] --> SCAN[checkov / tfsec]
    SCAN --> MIS[Public SG / open S3]
    MIS --> FIX[Block merge / remediate]
""",
    "devsecops/supply-chain": """
flowchart LR
    DEP[Dependencies] --> SBOM[syft SBOM]
    SBOM --> VULN[Known CVEs]
    VULN --> SIGN[cosign verify]
    SIGN --> TRUST[Trusted artifact]
""",
    "forensics/disk-memory": """
flowchart TD
    ACQ[Acquire image] --> HASH[Verify hash]
    HASH --> VOL[Volatility / Autopsy]
    VOL --> ART[Artifacts & timelines]
    ART --> REPORT[Forensic report]
""",
    "forensics/network": """
flowchart LR
    PCAP[PCAP capture] --> WS[Wireshark / Zeek]
    WS --> FLOWS[Connection analysis]
    FLOWS --> IOC[Extract IOCs]
""",
    "forensics/cloud": """
flowchart TD
    CLOUD[Cloud tenant] --> LOGS[CloudTrail / Audit logs]
    LOGS --> TIMELINE[Event timeline]
    TIMELINE --> ROOT[Root cause & scope]
""",
    "growth/cve-research": """
flowchart LR
    MON[Monitor advisories] --> REPRO[Reproduce in lab]
    REPRO --> POC[Minimal PoC]
    POC --> REPORT[Responsible disclosure]
""",
    "growth/writeups": """
flowchart TD
    FIND[Finding] --> DOC[Document steps]
    DOC --> IMPACT[Show impact safely]
    IMPACT --> PUBLISH[Publish writeup]
    PUBLISH --> REP[Build reputation]
""",
    "iot/firmware-analysis": """
flowchart TD
    FW[Firmware blob] --> BW[binwalk extract]
    BW --> FS[SquashFS / rootfs]
    FS --> GH[Ghidra reverse]
    GH --> VULN[Hardcoded creds / backdoors]
""",
    "iot/hardware-interfaces": """
flowchart LR
    CHIP[IoT device] --> UART[UART / JTAG]
    UART --> SHELL[Serial console]
    SHELL --> FLASH[Dump firmware]
""",
    "osint/people-org": """
flowchart TD
    ORG[Target org] --> TH[theHarvester]
    ORG --> MAL[Maltego transforms]
    TH & MAL --> EMAILS[Emails & employees]
    EMAILS --> PHISH[Phishing / cred spray scope]
""",
    "osint/data-breach-search": """
flowchart LR
    EMAIL[Email / domain] --> HIBP[HIBP API]
    HIBP --> EXP[Exposed in breach]
    EXP --> DEFEND[Force password reset]
""",
    "social-engineering/phishing": """
flowchart TD
    RECON[OSINT targets] --> LURE[Craft lure email]
    LURE --> SEND[gophish campaign]
    SEND --> CLICK[User clicks link]
    CLICK --> CRED[Credential harvest]
""",
    "social-engineering/pretexting": """
flowchart LR
    PRE[Build pretext] --> CALL[Phone / in-person]
    CALL --> TRUST[Establish trust]
    TRUST --> INFO[Sensitive info disclosed]
""",
    "reporting/vulnerability-reports": """
flowchart TD
    POC[PoC] --> WRITE[Clear reproduction steps]
    WRITE --> IMPACT[Business impact]
    IMPACT --> FIX[Remediation advice]
    FIX --> SUBMIT[Submit to program]
""",
    "secure-code-review/sast": """
flowchart LR
    SRC[Source code] --> SEM[semgrep / CodeQL]
    SEM --> FIND[Security findings]
    FIND --> TRIAGE[Dev triage & fix]
""",
    "secure-code-review/threat-modeling": """
flowchart TD
    DFD[Data flow diagram] --> STRIDE[STRIDE per component]
    STRIDE --> RANK[Risk ranking]
    RANK --> MIT[Mitigations & tests]
    MIT --> TRACK[Jira security tasks]
""",
    "web3/smart-contracts": """
flowchart TD
    SOL[Solidity contract] --> SLI[slither / mythril]
    SLI --> BUG[Reentrancy / overflow]
    BUG --> FUZZ[echidna / foundry fuzz]
    FUZZ --> REPORT[Bug bounty report]
""",
    "web3/wallet-dapp": """
flowchart LR
    USER[User wallet] --> DAPP[dApp UI]
    DAPP --> TX[Sign transaction]
    TX --> PHISH{Malicious approval?}
    PHISH -->|yes| DRAIN[Token drain]
""",
    "automation/js-analysis": """
flowchart LR
    JS[JS bundles] --> LF[linkfinder / katana]
    LF --> API[API routes & secrets]
    API --> NU[nuclei scan]
""",
    "automation/diffing": """
flowchart TD
    V1[Release v1] --> DIFF[Diff endpoints]
    V2[Release v2] --> DIFF
    DIFF --> NEW[New attack surface]
    NEW --> TEST[Security test new code]
""",
    "automation/scope-tooling": """
flowchart LR
    PLAT[H1 / BC / Intigriti] --> BB[bbscope export]
    BB --> LIST[In-scope asset list]
    LIST --> RECON[Feed into recon pipeline]
""",
}
