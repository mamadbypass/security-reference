# BloodHound

Graph-based Active Directory attack path analysis.

## How It Works

BloodHound is a graph analysis tool that maps **Active Directory attack paths**. Collectors (`SharpHound`, `bloodhound.py`) ingest LDAP, session, ACL, GPO, and trust data into a Neo4j graph database. Nodes represent users, computers, groups, GPOs, and domains; edges represent relationships like **MemberOf**, **HasSession**, **GenericAll**, **AdminTo**, and **CanRDP**.

Pre-built queries find:

- Shortest path from owned principals to **Domain Admins**.
- **Kerberoastable** and **AS-REP roastable** users.
- Computers where Domain Users have **local admin**.
- **Unconstrained delegation** and **ADCS ESC** misconfigurations (with SharpHound CE).

BloodHound turns manual ACL review into visual, queryable attack planning—used by both red and blue teams.

## Exploitation

1. **Collect data** — `SharpHound.exe -c All,GPOLocalGroup` from a domain-joined host or `bloodhound-python -u user -p pass -d domain -ns <DC>`.
2. **Import ZIP** — Upload collector output to BloodHound CE or legacy GUI.
3. **Mark owned nodes** — Right-click compromised users/computers as "Owned".
4. **Run path queries** — "Shortest Path to Domain Admins from Owned".
5. **Review high-value edges** — `GenericAll`, `WriteDACL`, `ForceChangePassword`, `AddMember`, `Owns`.
6. **Check session data** — `HasSession` edges show where domain admins are logged in (credential theft targets).
7. **Iterate** — After each escalation, re-mark owned and re-query paths.
8. **Export for reporting** — Screenshot attack paths for pentest deliverables.

## Defense & Mitigation

- **Run BloodHound defensively** — Schedule monthly collections; remediate paths before attackers find them.
- **Break attack paths** — Remove `GenericAll` on users/groups, disable unnecessary SPNs, enforce tiered admin.
- **Limit session exposure** — Admins should use PAW (Privileged Access Workstations); avoid daily DA logons on workstations.
- **Monitor collector activity** — LDAP enumeration from non-admin workstations may indicate SharpHound execution.
- **Harden ADCS** — BloodHound CE ESC queries reveal certificate template misconfigurations; apply [SpecterOps hardening guidance](https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf).
- **Integrate with SIEM** — Alert on mass LDAP queries and unusual SPN enumeration.

## Methodology

- [ ] Ingest SharpHound/BloodHound.py data
- [ ] Find shortest paths to high-value targets
- [ ] Review ACL abuse opportunities
- [ ] Prioritize edges for exploitation

## Tools

| Tool | Usage |
|------|-------|
| `bloodhound` | [AD attack path analysis](../../TOOLS_GUIDE.md#bloodhound) |
| `sharphound` | [BloodHound collector](../../TOOLS_GUIDE.md#bloodhound) |
| `bloodhound.py` | [BloodHound ingestor (Python)](../../TOOLS_GUIDE.md#bloodhound) |

## Resources

- [BloodHound Docs](https://bloodhound.readthedocs.io/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
