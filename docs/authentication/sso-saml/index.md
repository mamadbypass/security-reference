# SSO & SAML

Test single sign-on and SAML assertion handling.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    SAML[SAML Response] --> SIG{Signature valid?}
    SIG -->|bypass| ASSERT[Modified Assertion]
    ASSERT --> LOGIN[Login as victim]
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff

```

</div>

### Testing Workflow

<div class="sr-diagram sr-diagram-methodology" markdown="1">

```mermaid
flowchart LR
    P1["1. Preparation & Scoping"]
    P2["2. Discovery & Mapping"]
    P3["3. Validation & Testing"]
    P4["4. Exploitation & Impact Proof"]
    P5["5. Documentation & Reporting"]
    P1 --> P2 --> P3 --> P4 --> P5
```

</div>

## How It Works

Single Sign-On (SSO) federates authentication to an Identity Provider (IdP). **SAML 2.0** flows exchange XML assertions—often via POST bindings—containing attributes like email and group membership. The Service Provider (SP) must **validate XML signatures**, check `NotBefore`/`NotOnOrAfter`, match `Audience`, and prevent **XML signature wrapping (XSW)** attacks where attackers smuggle unsigned assertions alongside valid signed copies.

**OAuth 2.0 / OpenID Connect** variants introduce `redirect_uri` validation bugs, authorization code interception, **mix-up attacks** (confusing codes between clients), and weak `state`/`nonce` handling. Misconfigured SAML metadata, certificate rollover, and unsigned `Response` elements are common in enterprise integrations.

## Exploitation

1. **Capture a legitimate SAML Response** — Use Burp during login; note signature placement, `NameID`, `Conditions`, and `Recipient`.
2. **Test signature wrapping** — Duplicate assertions, move signatures, or inject unsigned assertions with attacker `NameID` (tools: SAML Raider, `samltool`).
3. **Tamper with attributes** — Modify `Role`, `Groups`, or `email` fields if signature verification is flawed or only signs part of the document.
4. **Replay assertions** — Resend captured responses; check if `InResponseTo` and timestamps are enforced.
5. **OAuth redirect abuse** — Open redirect in `redirect_uri`, subdomain takeover on allowed callback URLs, or path traversal (`/callback/../evil`).
6. **Mix-up / confusion** — Swap authorization codes between mobile and web client IDs if the token endpoint does not bind `client_id`.
7. **Metadata poisoning** — If you can supply IdP metadata URL, point SP at attacker-controlled signing keys.
8. **Downgrade flows** — Force SAML instead of stronger OIDC, or disable encryption if both are optional.

## Defense & Mitigation

- **Strictly validate SAML signatures** on the assertion or entire response per library best practice; reject unsigned assertions.
- **Use well-tested libraries** (python3-saml, OneLogin toolkit) and keep them patched against XSW variants.
- **Enforce one-time use** of assertions (`InResponseTo`, short `NotOnOrAfter`, replay caches).
- **Pin IdP certificates**; monitor metadata fetch endpoints for tampering.
- **OAuth/OIDC**: exact-match `redirect_uri` allowlists, PKCE for public clients, mandatory `state` and `nonce`.
- **Rotate keys safely**; log failed signature validations and anomalous attribute changes.
- Review [OWASP SAML Security guidance](https://owasp.org/www-community/vulnerabilities/SAML_Security_Cheat_Sheet).

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Obtain SAML metadata and test IdP/SP accounts

### Phase 2 — Discovery & Mapping

- [ ] Capture SAML Request/Response in Burp
- [ ] Review signature algorithm and certificate
- [ ] Check Assertion Consumer Service URL validation
- [ ] Map attribute mapping to application roles

### Phase 3 — Validation & Testing

- [ ] Test signature stripping and wrapping attacks
- [ ] Modify NameID and attributes without invalidating sig
- [ ] Replay assertions across sessions
- [ ] Use SAML Raider extension for mutations

### Phase 4 — Exploitation & Impact Proof

- [ ] Login as victim via forged or replayed assertion
- [ ] Escalate role via AttributeStatement tampering
- [ ] Document XML signature bypass variant

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification
- [ ] Validate signatures, encrypt assertions, strict ACS URL check

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `saml raider` | SAML testing Burp extension — [SAML Raider](https://github.com/SAMLRaider/SAMLRaider) |

## Resources

- [OWASP SAML Security](https://owasp.org/www-community/vulnerabilities/SAML_Security_Cheat_Sheet)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
