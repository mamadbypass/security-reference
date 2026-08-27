# DCSync

Replicate directory credentials from domain controllers.

## How It Works

DCSync is a technique that abuses the **Directory Replication** protocol (MS-DRSR) to impersonate a Domain Controller and **replicate password hashes** from a real DC without running code on it. The attacker requests replication of user objects (including `unicodePwd` and `ntlmhash` attributes) as if they were a legitimate DC.

Required rights (any one suffices in practice):

- `Replicating Directory Changes`
- `Replicating Directory Changes All`
- Membership in **Domain Admins**, **Enterprise Admins**, or **Administrators** on the domain root object.

DCSync dumps **all domain password hashes**, enabling Golden Ticket creation, Pass-the-Hash across the domain, and offline cracking of every account. It is stealthier than running Mimikatz on a DC because it uses normal replication traffic.

## Exploitation

1. **Obtain replication rights** — Via prior escalation (ACL abuse granting `Replicating Directory Changes All`) or Domain Admin membership.
2. **Run DCSync** — `mimikatz # lsadump::dcsync /domain:corp.local /user:krbtgt` or `secretsdump.py domain/admin:pass@<DC> -just-dc`.
3. **Dump krbtgt hash** — Required for Golden Ticket forgery.
4. **Dump all users** — `secretsdump.py` outputs NTLM hashes for offline cracking or Pass-the-Hash.
5. **Avoid DC execution** — DCSync runs from any machine with rights; no need to compromise the DC itself.
6. **Golden Ticket** — Use krbtgt hash to forge TGTs for any user indefinitely (until krbtgt password is rotated twice).
7. **Handle evidence carefully** — Per engagement ROE; hashes are crown-jewel data.
8. **Report remediation** — Identify which ACL edge granted replication rights.

## Defense & Mitigation

- **Restrict replication rights** — Only Domain Controllers should hold `Replicating Directory Changes All`; audit ACLs on domain root.
- **Monitor Event ID 4662** — Operations with properties `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` (DS-Replication-Get-Changes-All) from non-DC sources.
- **Tier 0 isolation** — Limit Domain Admin membership; use JIT/JEA for admin tasks.
- **Rotate krbtgt twice** after compromise — Required to invalidate Golden Tickets.
- **Deploy Microsoft Defender for Identity** — Detects DCSync anomalies.
- **Use Protected Users** for admin accounts — Prevents NTLM and unconstrained delegation abuse.
- **Regular BloodHound ACL audits** — Find and remove unintended replication rights.

## Methodology

- [ ] Identify Replicating Directory Changes rights
- [ ] Use DCSync to dump hashes
- [ ] Protect evidence handling in engagements
- [ ] Recommend remediation for replication ACLs

## Tools

| Tool | Usage |
|------|-------|
| `mimikatz` | See [Tools Guide](/TOOLS_GUIDE/) |
| `impacket secretsdump` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
