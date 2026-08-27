# Cryptographic Flaws

Identify weak algorithms, modes, and key management issues.

## How It Works

Applications misuse cryptography in predictable ways: **weak algorithms** (MD5, SHA1 for passwords, DES, RC4), **ECB mode** leaking block patterns, **static IVs** enabling replay, **hardcoded keys** in source, and **insufficient entropy** in tokens.

Custom crypto implementations almost always fail. Even standard libraries are misused when developers skip authentication (encrypt-only AES-CBC), truncate HMACs, or compose primitives incorrectly.

## Exploitation

1. **Inventory crypto usage**: search code for `Cipher.getInstance`, `AES`, `RSA`, `random`, `Math.random`.
2. **Protocol review**: identify what is encrypted vs signed vs both (encrypt-then-MAC).
3. **Test weak modes**: ECB ciphertext reveals repeated blocks; compare identical plaintext blocks across messages.
4. **Key recovery**: grep for PEM files, base64 keys in configs, and default passwords.
5. **Token analysis**: decode session tokens; check length, charset, and predictability.
6. **Oracle conditions**: distinguish error messages for padding vs MAC failures.

Use testssl.sh and manual review for TLS; Burp for application-layer crypto tokens.

## Defense & Mitigation

- Use **AES-GCM or ChaCha20-Poly1305** for authenticated encryption; avoid ECB.
- Hash passwords with **Argon2id** or bcrypt with per-user salts.
- Generate keys and IVs with `SecureRandom` or platform CSPRNG APIs.
- Never implement custom ciphers or MAC constructions.
- Rotate keys with documented procedures; use HSMs or KMS for master keys.
- Follow OWASP Cryptographic Storage Cheat Sheet and NIST SP 800-57.

## Methodology

- [ ] Review cipher suites and protocol versions
- [ ] Check for ECB mode and static IVs
- [ ] Test padding oracle conditions
- [ ] Validate random number generation

## Tools

| Tool | Usage |
|------|-------|
| `testssl.sh` | See [Tools Guide](/TOOLS_GUIDE/) |
| `sslscan` | See [Tools Guide](/TOOLS_GUIDE/) |
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
