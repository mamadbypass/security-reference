# Passwordless & WebAuthn

Test magic links, OTP, and passkey implementations.

## How It Works

Passwordless authentication replaces passwords with **magic links** (email URLs with embedded tokens), **OTP codes** (SMS/email/TOTP), or **WebAuthn/FIDO2 passkeys** (public-key cryptography bound to origin and challenge). Each mechanism has distinct risks:

- Magic links: token entropy, transport security, device sharing, open redirects on landing URLs.
- OTP: short code brute force, race conditions, SIM swapping, lack of attempt limits.
- WebAuthn: incorrect `rpId` validation, missing challenge binding, permissive `userVerification`, and account enumeration via credential ID lookup.

Because there is no password, **the token or authenticator becomes the sole secret**—any guessable or interceptable factor fully compromises the account.

## Exploitation

1. **Magic link analysis** — Request a link; inspect token length, encoding, and whether it works after multiple uses or from different IPs.
2. **Brute-force OTP** — If 4–6 digit codes, attempt all combinations with parallel requests; test whether lockout applies per session vs per IP.
3. **Bypass delivery** — Register with attacker-controlled email/phone on victim alias (plus addressing, disposable domains) if verification is weak.
4. **Fixation** — Start login on attacker device, trick victim into completing WebAuthn on attacker's session if challenges are not bound.
5. **Enumerate accounts** — Different errors for registered vs unregistered emails or WebAuthn credential IDs.
6. **Race OTP validation** — Submit the same code simultaneously from multiple clients before invalidation.
7. **Deep link hijacking** — Mobile apps handling magic links via intents may leak tokens to other apps.
8. **WebAuthn downgrade** — Force `userVerification: discouraged` or cross-origin flows if the server allows it.

## Defense & Mitigation

- **High-entropy, single-use tokens** for magic links; expire within minutes.
- **Rate-limit OTP verification** aggressively; use 6+ digit or alphanumeric codes with lockout and backoff.
- **Bind challenges to session** for WebAuthn; verify `origin`, `rpId`, and `challenge` server-side.
- **Require user verification** (biometric/PIN) for sensitive accounts.
- **Uniform messaging** to prevent account enumeration.
- **Prefer WebAuthn over SMS OTP** where possible; monitor SIM-swap risk for SMS.
- **Invalidate sessions** after passwordless login on new devices; notify users of new sign-ins.
- See [WebAuthn Guide](https://webauthn.guide/) for implementation details.

## Methodology

- [ ] Brute force short OTP codes
- [ ] Test magic link token entropy
- [ ] Review WebAuthn challenge binding
- [ ] Check credential enumeration

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |

## Resources

- [WebAuthn Guide](https://webauthn.guide/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
