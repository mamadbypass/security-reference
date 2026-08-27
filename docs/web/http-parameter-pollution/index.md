# HTTP Parameter Pollution

Abuse duplicate parameters handled differently by proxies and backends.

## Overview Diagram

<div class="sr-diagram" markdown="1">

```mermaid
flowchart LR
    DUP[id=1&id=2] --> FE[Front-end uses first]
    DUP --> BE[Back-end uses last]
    FE & BE --> BYPASS[Auth / logic bypass]
```

</div>

## How It Works

HTTP Parameter Pollution (HPP) sends duplicate parameters in one request (`?id=1&id=2`) knowing different components parse duplicates inconsistently.

Split behavior examples:

- **ASP.NET/IIS**: concatenates `id=1,2`
- **PHP**: often uses last value `id=2`
- **Apache**: often first value `id=1`
- **WAF vs app**: WAF inspects first; app uses second (bypass)

Impact scenarios:

- WAF/filter bypass for XSS/SQLi payloads in second parameter
- Access control: `user=attacker&user=admin`—front-end checks first, back-end authorizes second
- OAuth scope manipulation with duplicate query keys
- HPP in redirects and tracking links altering payment amounts

## Exploitation

**WAF bypass**

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
- Custom scripts doubling every parameter

## Defense & Mitigation

**Consistent parsing**

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

- Log full parameter lists, not only first occurrence.

## Methodology

- [ ] Send duplicate GET/POST parameters
- [ ] Test WAF bypass via parameter splitting
- [ ] Check auth bypass on access control checks
- [ ] Compare framework-specific parsing behavior

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `manual fuzzing` | [Custom wordlists and Burp Intruder payloads](../../TOOLS_GUIDE.md) |

## Resources

- [OWASP HPP](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
