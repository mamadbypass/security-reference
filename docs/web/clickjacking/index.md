# Clickjacking

Frame sensitive actions to trick users into unintended clicks.

## How It Works

Clickjacking (UI redressing) tricks users into clicking hidden or overlaid elements on a victim site while believing they interact with the attacker's visible UI. The attack typically embeds the target in a transparent `<iframe>` over decoy buttons.

Requirements for exploitation:

- Target page lacks frame-busting or proper `X-Frame-Options` / CSP `frame-ancestors`
- Victim is authenticated
- Click performs a sensitive action without re-authentication (one-click purchase, follow, disable security, grant OAuth)

Variants:

- **Classic overlay**: opacity-0 iframe over "Win iPad" button
- **Double clickjacking**: rapid iframe repositioning on mouse down
- **Likejacking**: hidden Facebook like iframe (legacy social widgets)

Mobile WebViews and hybrid apps may omit frame protections entirely.

## Exploitation

**Verify framing**

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
- Document missing `frame-ancestors` and successful framed sensitive page

## Defense & Mitigation

**Frame denial headers**

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

- Secondary channel confirmation for financial transactions (out-of-band).

## Methodology

- [ ] Check X-Frame-Options and CSP frame-ancestors
- [ ] Build proof-of-concept iframe overlays
- [ ] Target high-impact actions (password change, payment)
- [ ] Test mobile WebView contexts

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `custom html poc` | [Minimal HTML page demonstrating clickjacking](../../TOOLS_GUIDE.md) |

## Resources

- [PortSwigger Clickjacking](https://portswigger.net/web-security/clickjacking)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
