# Phishing Assessments

Authorized phishing simulations for security awareness.

## How It Works

**Phishing** deceives users into clicking malicious links, opening attachments, or entering credentials on fake sites. **Authorized phishing assessments** simulate these attacks to measure awareness and technical controls (email filtering, link protection).

Campaigns use cloned login pages, OAuth consent phishing, QR codes, and thread hijacking. Success rates inform training priorities; unauthorized phishing is illegal and harmful.

## Exploitation

1. **Written authorization** specifying targets, timing, and forbidden tactics.
2. **Platform setup**: Gophish or King Phisher with tracking on controlled infrastructure.
3. **Template design**: realistic but safe—no malware attachments unless explicitly scoped.
4. **Landing page**: clone internal portal; capture metrics only, not real passwords (or use unique tokens per user).
5. **Measure**: open rate, click rate, submission rate, report-to-security rate.
6. **Debrief**: immediate training for clickers; positive reinforcement for reporters.

Coordinate with IT to whitelist test infrastructure and avoid help desk overload.

## Defense & Mitigation

- Deploy **email authentication** (DMARC p=reject), anti-phishing gateways, and URL rewriting.
- Enable **FIDO2/WebAuthn**; phishing-resistant MFA stops credential theft.
- Run regular simulations with improving metrics over time.
- Easy **report phish** button integrated with SOC workflows.
- Browser isolation for risky links; block newly registered domains at egress.
- Executive protection program for high-value targets (spear-phish monitoring).

## Methodology

- [ ] Obtain written authorization
- [ ] Craft realistic but safe templates
- [ ] Track click and credential submission rates
- [ ] Provide training for affected users

## Tools

| Tool | Usage |
|------|-------|
| `gophish` | [Phishing campaign framework](../../TOOLS_GUIDE.md#gophish) |
| `king phisher` | [Phishing campaigns](../../TOOLS_GUIDE.md#gophish) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
