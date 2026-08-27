# Password Reset Flaws

Exploit weak password reset and account recovery flows.

## How It Works

Password reset flows typically: (1) user submits an email, (2) server generates a one-time token and emails a link, (3) user clicks the link and sets a new password. Weaknesses appear at every step: **predictable tokens** (timestamp, user ID, weak PRNG), **tokens that never expire or are reusable**, **user enumeration** via different responses, **Host header poisoning** that embeds attacker domains in reset links, **parameter tampering** (`email`, `userId`, `account`), and **race conditions** between token validation and password update.

Some implementations leak tokens in Referer headers, browser history, or server logs; others allow resetting another user's password when only the token is required without re-binding to the initiating session.

## Exploitation

1. **Request reset for your account** — Capture the token format, length, entropy, and URL structure.
2. **Test predictability** — Request multiple tokens; check for sequential IDs, base64-encoded emails, or HMAC with weak secrets.
3. **Host / X-Forwarded-Host poisoning** — Submit reset with `Host: evil.com` and see if the email link points to the attacker domain.
4. **Token reuse** — Complete a reset, then reuse the same link; try using one token twice in parallel tabs.
5. **Change email parameter** — Modify `email` or `user_id` in POST body while using another user's token (or none).
6. **Race conditions** — Send concurrent reset-completion requests with the same token using Burp Turbo Intruder.
7. **Enumerate users** — Compare timing, status codes, and message text for valid vs invalid accounts.
8. **Intercept delivery** — If SMS reset, test SIM-swap social paths; if security questions exist, test weak answers.
9. **Check mobile deep links** — Custom URL schemes may pass tokens without HTTPS.

## Defense & Mitigation

- **Generate tokens with CSPRNG** (≥128 bits); store only a hashed token server-side.
- **Single-use, short TTL** (15–60 minutes); invalidate all sessions after reset.
- **Bind tokens to user agent or session** where UX allows; require current password for logged-in users.
- **Ignore client Host headers**; build reset URLs from a configured canonical base URL.
- **Uniform responses** — always return "If an account exists, we sent email".
- **Rate-limit reset requests** per email and IP; monitor brute-force on token endpoints.
- **Use HTTPS-only links**; add `Referrer-Policy: no-referrer` on reset pages.
- Follow the [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).

## Methodology

- [ ] Test token predictability and reuse
- [ ] Host header poisoning on reset links
- [ ] Race reset token validation
- [ ] Check reset for arbitrary email change

## Tools

| Tool | Usage |
|------|-------|
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [OWASP Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
