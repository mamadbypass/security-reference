# Firewall & Segmentation

Validate network segmentation and firewall rule effectiveness.

## How It Works

Firewall and network segmentation testing validates that **security zones** are properly isolated and that firewall rules enforce least-privilege access. Organizations define zones such as:

- **DMZ** — Public-facing web servers.
- **Internal/Corporate** — Workstations and general servers.
- **Restricted/PCI** — Payment systems, databases, domain controllers.
- **Management** — Jump hosts, backup systems, monitoring.

Testing maps **allowed paths** between zones by probing from compromised or test hosts in each segment. Common failures: overly permissive egress (`any:any` outbound), flat networks without VLANs, and "temporary" rules never removed.

## Exploitation

1. **Document zone map** — Obtain network diagram and rule sets from client (or infer from traceroute and ARP).
2. **Baseline from each zone** — Place test hosts in DMZ, corp, and guest VLANs.
3. **Probe cross-zone** — `nmap` and `hping3` to targets in other segments; record allowed ports.
4. **Test egress filtering** — Attempt outbound connections to internet, DNS tunneling, and C2 ports from internal hosts.
5. **Verify DMZ isolation** — From DMZ host, attempt direct access to database and DC subnets.
6. **Check dual-homed hosts** — Systems spanning zones become pivot points.
7. **Review rule sprawl** — Compare documented policy vs actual `iptables`/`pf`/Palo Alto configs.
8. **Report gaps** — Rank findings by data sensitivity of reachable assets.

## Defense & Mitigation

- **Default-deny** firewall policies between all zones.
- **Micro-segmentation** — Workload-level policies (NSX, Illumio) beyond VLANs.
- **Quarterly rule reviews** — Remove stale permits; document business justification.
- **Restrict egress** — Allow only required destinations; block direct internet from servers.
- **Separate management plane** — Admin access only via PAM/jump hosts.
- **Log and alert** — Deny-rule hits may indicate lateral movement attempts.
- **Validate with continuous testing** — Internal scanners that verify segmentation after every change.

## Methodology

- [ ] Map allowed paths between zones
- [ ] Test egress filtering
- [ ] Verify DMZ isolation
- [ ] Document overly permissive rules

## Tools

| Tool | Usage |
|------|-------|
| `nmap` | See [Tools Guide](/TOOLS_GUIDE/) |
| `hping3` | See [Tools Guide](/TOOLS_GUIDE/) |
| `custom probes` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
