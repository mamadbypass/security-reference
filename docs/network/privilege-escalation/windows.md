# Windows Privilege Escalation

Escalate privileges on Windows hosts.

## How It Works

Windows privilege escalation elevates access from a **low-privilege user** to **LOCAL SYSTEM** or **Administrator** on a host. Common vectors:

- **Misconfigured services** — Unquoted service paths, weak service binary permissions, modifiable service DLLs.
- **Registry and scheduled tasks** — Writable `AutoRun` keys, tasks running as SYSTEM.
- **Token impersonation** — `SeImpersonatePrivilege` (PrintSpoofer, Juicy Potato) on service accounts.
- **Credential storage** — Saved RDP creds, WiFi passwords, browser vaults, DPAPI.
- **Kernel exploits** — Unpatched CVEs when patching is behind.
- **AlwaysInstallElevated** — MSI installs run as SYSTEM.

Post-exploitation enumeration (`winPEAS`, `PowerUp`) automates checking hundreds of misconfiguration patterns.

## Exploitation

1. **Enumerate** — `winPEAS.exe`, `seatbelt.exe system`, or manual `whoami /priv`.
2. **Check service misconfigs** — `accesschk.exe` on service binaries and unquoted paths (`wmic service get pathname`).
3. **Exploit SeImpersonate** — `PrintSpoofer.exe -i -c cmd` or `GodPotato` on Windows Server 2019+.
4. **Writable directories** — Replace DLLs in PATH or service folders.
5. **Scheduled tasks** — `schtasks` listing; modify scripts run as SYSTEM.
6. **Stored credentials** — `cmdkey /list`, `mimikatz vault::list`.
7. **Kernel exploits** — Last resort; `systeminfo` for patch level vs exploit-db.
8. **Document** — Capture `whoami` before/after; note exact misconfiguration.

## Defense & Mitigation

- **Apply CIS Windows benchmarks** — Harden service permissions, UAC, and PowerShell logging.
- **Quote all service paths** and set restrictive ACLs on service binaries.
- **Disable SeImpersonate** for service accounts that do not require it.
- **Patch aggressively** — Automate WSUS/Intune patching; prioritize critical CVEs.
- **Remove local admin rights** from standard users.
- **Enable Credential Guard** and LSA protection on supported Windows versions.
- **Deploy EDR** with tamper protection; alert on Mimikatz, Potato exploits, and suspicious service modifications.

## Methodology

- [ ] Run winPEAS or manual enumeration
- [ ] Check unquoted service paths and weak permissions
- [ ] Review token impersonation opportunities
- [ ] Exploit missing patches when in scope

## Tools

| Tool | Usage |
|------|-------|
| `winpeas` | [Windows privesc enumeration](../../TOOLS_GUIDE.md#winpeas) |
| `powerup` | [Windows privesc checks](https://github.com/PowerShellMafia/PowerSploit) |
| `watson` | [Windows patch enumeration](https://github.com/rasta-mouse/Watson) |

## Resources

- [HackTricks Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
