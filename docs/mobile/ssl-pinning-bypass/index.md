# SSL Pinning Bypass

Intercept HTTPS from mobile apps with certificate pinning.

## Methodology

- [ ] Identify pinning libraries in the binary
- [ ] Use Frida scripts to disable validation
- [ ] Patch APK with custom network security config
- [ ] Test on emulators with system CA installed

## Tools

- `frida`
- `apk-mitm`
- `objection`

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
