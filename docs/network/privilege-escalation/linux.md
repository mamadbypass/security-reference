# Linux Privilege Escalation

Escalate privileges on Linux systems.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    SHELL[Low priv shell] --> LIN[linPEAS]
    LIN --> SUDO[SUID / sudo misconfig]
    LIN --> KERNEL[Kernel exploit]
    SUDO & KERNEL --> ROOT[root access]
```

</div>

## How It Works

Linux privilege escalation gains **root** from an unprivileged shell. Attack surface includes:

- **SUID/SGID binaries** — Programs running with elevated privileges (find, vim, custom apps with command injection).
- **Sudo misconfigurations** — `(ALL) NOPASSWD: ALL` or exploitable allowed commands (`sudo vim`, `sudo find`).
- **Cron jobs** — World-writable scripts executed as root.
- **Capabilities** — `cap_setuid` on binaries like `python3`.
- **Kernel exploits** — Dirty COW, PwnKit, OverlayFS when unpatched.
- **Container escapes** — Docker socket (`/var/run/docker.sock`), privileged containers, mounted host paths.
- **Secrets in files** — `.bash_history`, config files, SSH keys, `/etc/shadow` if readable.

`linpeas.sh` automates enumeration across these categories.

## Exploitation

1. **Run linpeas** — `curl -L linpeas.sh | sh` or upload and execute offline.
2. **Check sudo** — `sudo -l` for NOPASSWD entries; GTFOBins for exploit paths.
3. **Find SUID** — `find / -perm -4000 2>/dev/null`; cross-reference GTFOBins.
4. **Review cron** — `cat /etc/crontab`, `/etc/cron.d/`, user crontabs.
5. **Capabilities** — `getcap -r / 2>/dev/null`.
6. **Writable /etc/passwd** — Add root user with known password hash.
7. **Container escape** — If in Docker, check `docker.sock`, `--privileged`, host mounts; use `cdk` or `deepce`.
8. **Kernel exploit** — `uname -a` vs exploit-db; lab-only unless explicitly in scope.

## Defense & Mitigation

- **Minimize SUID binaries** — Remove unnecessary setuid; audit with `find / -perm -4000`.
- **Restrict sudo** — Explicit command lists; no NOPASSWD for shells or editors.
- **Secure cron** — Root-only writable cron directories; validate script permissions.
- **Patch kernels** — Automated unattended-upgrades; monitor CVE feeds.
- **Harden containers** — Non-root users, drop capabilities, read-only rootfs, no docker.sock mounts.
- **AppArmor/SELinux** — Enforce mandatory access controls.
- **Audit logging** — `auditd` rules for privilege changes and sudo usage.

## Methodology

- [ ] Run linpeas and review SUID binaries
- [ ] Check sudo rules and cron jobs
- [ ] Enumerate kernel version for exploits
- [ ] Review Docker socket and capabilities

## Tools

| Tool | Usage |
|------|-------|
| `linpeas` | [Linux privesc enumeration](../../TOOLS_GUIDE.md#linpeas) |
| `linux-exploit-suggester` | [Kernel exploit suggestions](https://github.com/mzet-/linux-exploit-suggester) |

## Resources

- [HackTricks Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
