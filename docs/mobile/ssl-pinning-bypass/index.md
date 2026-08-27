# SSL Pinning Bypass

Intercept HTTPS from mobile apps with certificate pinning.

## How It Works

**SSL/TLS certificate pinning** binds an app to specific public keys or certificates instead of trusting the device's CA store. Even if a tester installs Burp's CA on a rooted device, the app rejects the intercepted connection because the proxy certificate does not match the pinned hash.

Pinning may be implemented in the network stack (OkHttp `CertificatePinner`), NSURLSession delegates on iOS, or custom native TLS libraries. Some apps pin only production hosts while leaving staging environments interceptable—a common misconfiguration.

## Exploitation

1. **Identify pinning**: search decompiled code for `CertificatePinner`, `TrustKit`, `AFSSLPinningMode`, or `flutter_ssl_pinning`.
2. **Frida universal scripts**: run community scripts that hook common pinning APIs.
3. **Objection**: `android sslpinning disable` or `ios sslpinning disable`.
4. **APK patching**: repackage with a modified `network_security_config.xml` that trusts user CAs (`apk-mitm`, manual `apktool` workflow).
5. **Emulator with system CA**: Android 7+ requires placing the CA in the system store or using a Magisk module.
6. Confirm interception in Burp/mitmproxy and replay API calls.

Document which hosts were pinned and whether bypass affected all endpoints.

## Defense & Mitigation

- Pin **public keys** (SPKI hashes) rather than entire certificates to ease rotation.
- Implement **backup pins** and a documented rotation procedure.
- Combine pinning with **certificate transparency** monitoring for mis-issued certs.
- Do not pin staging/dev builds with production keys; use separate trust stores.
- Assume pinning can be bypassed on compromised devices; enforce auth and encryption at the application layer.
- Test pinning with tools like `nabla` or MobSF and verify failure on proxy connections.

## Methodology

- [ ] Identify pinning libraries in the binary
- [ ] Use Frida scripts to disable validation
- [ ] Patch APK with custom network security config
- [ ] Test on emulators with system CA installed

## Tools

| Tool | Usage |
|------|-------|
| `frida` | [Dynamic instrumentation](../../TOOLS_GUIDE.md#frida-objection) |
| `apk-mitm` | [Patch APK for MITM](https://github.com/shroudedcode/apk-mitm) |
| `objection` | [Runtime mobile exploration](../../TOOLS_GUIDE.md#frida-objection) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
