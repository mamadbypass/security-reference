INFRA_DIAGRAMS = {
    "network/active-directory": """
flowchart TD
    RECON[LDAP enum / BloodHound] --> PATH[Attack paths]
    PATH --> KERB[Kerberoasting]
    PATH --> RELAY[NTLM relay]
    PATH --> ACL[ACL abuse]
    KERB & RELAY & ACL --> DA[Domain Admin]
""",
    "network/active-directory/kerberoasting": """
flowchart LR
    USER[Any domain user] --> TGS[Request service ticket]
    TGS --> HASH[RC4 hash offline]
    HASH --> CRACK[hashcat]
    CRACK --> SVC[Service account creds]
    SVC --> PRIV[Privilege escalation]
""",
    "network/bloodhound": """
flowchart TD
    SH[SharpHound collect] --> BH[BloodHound ingest]
    BH --> GRAPH[Attack path graph]
    GRAPH --> PATH[Shortest path to DA]
    PATH --> EXEC[Execute AD attack]
""",
    "network/dcsync": """
flowchart LR
    PRIV[Replicating privileges] --> DC[Domain Controller]
    DC --> DUMP[secretsdump all hashes]
    DUMP --> GOLD[Golden ticket / pass-the-hash]
""",
    "network/pentesting": """
flowchart TD
    SCAN[nmap / rustscan] --> ENUM[SMB / LDAP enum]
    ENUM --> VULN[Known vulns / creds]
    VULN --> EXPLOIT[Exploit / relay]
    EXPLOIT --> SHELL[Initial access]
""",
    "network/privilege-escalation/windows": """
flowchart TD
    SHELL[Low priv shell] --> ENUM[winPEAS / Watson]
    ENUM --> MISCONFIG[Unquoted path / service]
    ENUM --> TOKEN[Token impersonation]
    MISCONFIG & TOKEN --> ADMIN[SYSTEM / Admin]
""",
    "network/privilege-escalation/linux": """
flowchart TD
    SHELL[Low priv shell] --> LIN[linPEAS]
    LIN --> SUDO[SUID / sudo misconfig]
    LIN --> KERNEL[Kernel exploit]
    SUDO & KERNEL --> ROOT[root access]
""",
    "network/lateral-movement": """
flowchart LR
    CRED[Captured hashes] --> PTH[Pass-the-hash]
    CRED --> WINRM[evil-winrm]
    PTH & WINRM --> HOST[Next host]
    HOST --> MORE[Expand foothold]
""",
    "network/wireless": """
flowchart TD
    CAP[Capture handshake] --> CRACK[aircrack-ng]
    EVIL[Evil twin AP] --> MITM[bettercap MITM]
    CRACK & MITM --> NET[Network access]
""",
    "network/firewall-segmentation": """
flowchart LR
    ZONE[DMZ] -->|allowed port| INT[Internal zone]
    PROBE[Probe rules] --> GAP[Segmentation gaps]
    GAP --> PIVOT[Lateral pivot]
""",
    "cloud/aws": """
flowchart TD
    ENUM[Account enum / Pacu] --> IAM[IAM misconfigs]
    ENUM --> S3[S3 public buckets]
    ENUM --> META[IMDSv1 metadata]
    IAM & S3 & META --> COMPROMISE[AWS account compromise]
""",
    "cloud/azure": """
flowchart TD
    ROAD[ROADtools enum] --> AAD[Azure AD paths]
    AAD --> SP[Over-privileged SPs]
    AAD --> STORAGE[Storage keys exposed]
    SP & STORAGE --> TENANT[Tenant compromise]
""",
    "cloud/gcp": """
flowchart LR
    SCAN[gcp_scanner] --> IAM[GCP IAM bindings]
    SCAN --> BUCKET[Open GCS buckets]
    IAM & BUCKET --> PERSIST[Project takeover]
""",
    "cloud/kubernetes": """
flowchart TD
    KUBE[kube-hunter / kubectl] --> RBAC[Weak RBAC]
    KUBE --> POD[Privileged pods]
    RBAC & POD --> CLUSTER[Cluster admin]
""",
    "containers/docker": """
flowchart LR
    IMG[Container image] --> TRIVY[trivy scan]
    TRIVY --> CVE[Known CVEs]
    RUN[Running container] --> SOCK[Docker socket mount]
    SOCK --> ESC[Host escape]
""",
    "containers/kubernetes-security": """
flowchart TD
    K8S[Cluster] --> KUBE[kubescape / Falco]
    KUBE --> MIS[Misconfigs]
    MIS --> NET[Network policies missing]
    MIS --> SEC[Secrets in env vars]
""",
    "containers/container-escape": """
flowchart LR
    POD[Compromised pod] --> CAP[Capabilities / privileged]
    CAP --> HOST[Host namespace]
    HOST --> NODE[Node takeover]
""",
    "mobile/apk-ipa-analysis": """
flowchart TD
    APK[APK/IPA] --> JADX[jadx decompile]
    JADX --> SECRETS[Hardcoded keys]
    JADX --> API[Hidden API endpoints]
    SECRETS & API --> TEST[Dynamic test with Frida]
""",
    "mobile/frida": """
flowchart LR
    APP[Mobile app] --> FRIDA[Frida hook]
    FRIDA --> BYPASS[SSL pin / root detect bypass]
    FRIDA --> LOG[Log crypto & API calls]
""",
    "mobile/ssl-pinning-bypass": """
flowchart TD
  APP[App with pinning] --> MITM[Proxy blocked]
  MITM --> FRIDA[Frida ssl-kill-switch]
  FRIDA --> BURP[Burp intercepts HTTPS]
""",
    "mobile/deep-links": """
flowchart LR
    LINK[myapp://path] --> APP[App handler]
    APP --> AUTH{Validate intent?}
    AUTH -->|no| XSS[WebView XSS / IDOR]
""",
    "binary/reverse-engineering": """
flowchart TD
    BIN[Binary] --> GH[Ghidra analyze]
    GH --> FUNCS[Functions & strings]
    FUNCS --> VULN[Find vuln logic]
    VULN --> POC[Exploit PoC]
""",
    "binary/stack-overflow": """
flowchart LR
    BUF[Overflow buffer] --> RET[Overwrite return addr]
    RET --> SHELL[shellcode / ROP chain]
""",
    "binary/heap-exploitation": """
flowchart TD
    ALLOC[Heap alloc/free] --> BUG[Use-after-free / overflow]
    BUG --> HEAP[Heap feng shui]
    HEAP --> RCE[Code execution]
""",
}
