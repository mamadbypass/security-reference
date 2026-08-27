# Kerberoasting

Extract and crack service ticket hashes offline.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    USER[Any domain user] --> TGS[Request service ticket]
    TGS --> HASH[RC4 hash offline]
    HASH --> CRACK[hashcat]
    CRACK --> SVC[Service account creds]
    SVC --> PRIV[Privilege escalation]
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff

```

</div>

### Testing Workflow

<div class="sr-diagram sr-diagram-methodology" markdown="1">

```mermaid
flowchart LR
    P1["1. Preparation & Scoping"]
    P2["2. Discovery & Mapping"]
    P3["3. Validation & Testing"]
    P4["4. Exploitation & Impact Proof"]
    P5["5. Documentation & Reporting"]
    P1 --> P2 --> P3 --> P4 --> P5
```

</div>

## How It Works

Kerberoasting exploits how Kerberos issues **Ticket Granting Service (TGS) tickets** for accounts with **Service Principal Names (SPNs)**. When a domain user requests access to a service (e.g., MSSQL, HTTP, CIFS), the DC returns a TGS ticket encrypted with the **service account's password hash**.

Any authenticated domain user can request TGS tickets for SPNs they can see in AD. Because the ticket is encrypted with the service account's credentials, an attacker can **extract the ciphertext offline** and crack it with hashcat without triggering account lockout—the attack never guesses passwords against the DC.

High-value targets: service accounts with weak passwords, accounts with `GenericAll` on other objects, and SQL/IIS service accounts running as domain users.

## Exploitation

1. **Find SPN accounts** — `GetUserSPNs.py domain/user:pass -dc-ip <DC>` or `Rubeus.exe kerberoast /stats`.
2. **Request TGS tickets** — `Rubeus.exe kerberoast /outfile:hashes.txt` or Impacket `GetUserSPNs -request`.
3. **Extract hashes** — Output format `$krb5tgs$23$*` for hashcat mode 13100.
4. **Crack offline** — `hashcat -m 13100 hashes.txt rockyou.txt -r rules/best64.rule`.
5. **Target AES tickets if available** — Mode 19700 for `$krb5tgs$18$*` (slower but captures stronger accounts).
6. **Validate cracked creds** — `crackmapexec smb <target> -u svc_account -p password`.
7. **Pivot** — Use recovered service account for lateral movement, ACL abuse, or further Kerberoasting if the account has new SPNs.
8. **Report** — Document SPN list, crack time, and downstream access gained.

## Defense & Mitigation

- **Use Group Managed Service Accounts (gMSA)** — Automatic 120-character passwords rotated by AD; not crackable via Kerberoasting.
- **Strong service account passwords** — 25+ random characters if gMSA is not feasible.
- **Least privilege on SPN accounts** — Service accounts should not be domain admins or have excessive ACLs.
- **Monitor Event ID 4769** — Alert on unusual TGS requests (many SPNs from one user, RC4 encryption type 0x17).
- **Prefer AES Kerberos encryption** — RC4 (etype 23) tickets are faster to crack.
- **Audit SPN registrations** — Remove stale SPNs from decommissioned services.
- **Deploy honeypot SPN accounts** — Canary SPNs that alert on any TGS request.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Confirm low-priv domain user credentials available

### Phase 2 — Discovery & Mapping

- [ ] Enumerate SPNs with GetUserSPNs or Rubeus
- [ ] Request TGS tickets for service accounts
- [ ] Export hashes to crackable format
- [ ] Prioritize accounts without preauth or old passwords

### Phase 3 — Validation & Testing

- [ ] Crack RC4 tickets with hashcat rules
- [ ] Validate cracked password against service login
- [ ] Check if service account is over-privileged
- [ ] Test password reuse on other systems

### Phase 4 — Exploitation & Impact Proof

- [ ] Demonstrate lateral movement with cracked service creds
- [ ] Document SPN account and cracked password policy
- [ ] Recommend gMSA and strong service passwords

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification

## Tools

| Tool | Usage |
|------|-------|
| `rubeus` | [Kerberos abuse toolkit](../../TOOLS_GUIDE.md#rubeus) |
| `impacket GetUserSPNs` | [Kerberoasting with GetUserSPNs](../../TOOLS_GUIDE.md#impacket) |
| `hashcat` | [Password cracking](https://hashcat.net/hashcat/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
