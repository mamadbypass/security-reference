# APK / IPA Analysis

Static and dynamic analysis of mobile applications.

## How It Works

Mobile applications ship as **APK** (Android) or **IPA** (iOS) packages containing compiled bytecode, native libraries, resources, and manifest metadata. Attackers and researchers reverse these packages to recover API endpoints, hardcoded secrets, cryptographic keys, and business logic that was never meant to be public.

On Android, DEX bytecode is decompiled to Java-like source with tools like JADX. The `AndroidManifest.xml` declares permissions, exported components (activities, services, broadcast receivers), deep link handlers, and backup/debug flags. Native `lib/` binaries may contain additional logic or anti-tamper checks.

On iOS, IPA binaries are ARM Mach-O executables. Class metadata, strings, and Objective-C/Swift symbols reveal functionality. Keychain usage, URL schemes, and entitlements define what the app can access on the device.

## Exploitation

1. **Obtain the package** from Play Store, App Store, or program scope assets.
2. **Decompile and map surface**: `jadx -d out app.apk` or use MobSF for a guided report.
3. **Search for secrets**: grep decompiled output for API keys, tokens, AWS credentials, and internal hostnames.
4. **Review manifest exports**: identify `android:exported="true"` components that accept intents without authentication.
5. **Trace network layer**: find Retrofit/OkHttp configs, certificate pinning hooks, and WebView JavaScript bridges.
6. **Dynamic validation**: install on emulator/device, intercept traffic (after pinning bypass if needed), and confirm static findings.

Chain findings: hardcoded admin API key + exported activity that loads arbitrary URLs can escalate to account takeover or data exfiltration.

## Defense & Mitigation

- **Never store secrets in the client**; use short-lived tokens from a backend.
- Minimize exported components; require signature-level permissions for IPC.
- Enable **ProGuard/R8** and native obfuscation; understand this is deterrence, not encryption.
- Disable `android:allowBackup` unless backups are encrypted and scoped.
- Implement certificate pinning and root/jailbreak detection as layered controls.
- Run MobSF or similar in CI for every release build.
- Follow **OWASP MASTG** and MASVS for structured testing and verification.

## Methodology

- [ ] Decompile APK/IPA and review hardcoded secrets
- [ ] Map API endpoints and certificate pinning
- [ ] Test exported components and deep links
- [ ] Intercept traffic with rooted/jailbroken devices or patches

## Tools

| Tool | Usage |
|------|-------|
| `jadx` | See [Tools Guide](/TOOLS_GUIDE/) |
| `apktool` | See [Tools Guide](/TOOLS_GUIDE/) |
| `mobsf` | See [Tools Guide](/TOOLS_GUIDE/) |
| `objection` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [OWASP MASTG](https://owasp.org/www-project-mobile-app-security-testing-guide/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
