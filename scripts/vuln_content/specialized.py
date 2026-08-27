"""Detailed content for specialized security topics."""

SPECIALIZED_CONTENT: dict[str, dict[str, str]] = {
    "mobile/apk-ipa-analysis": {
        "how_it_works": (
            "Mobile applications ship as **APK** (Android) or **IPA** (iOS) packages containing "
            "compiled bytecode, native libraries, resources, and manifest metadata. Attackers and "
            "researchers reverse these packages to recover API endpoints, hardcoded secrets, "
            "cryptographic keys, and business logic that was never meant to be public.\n\n"
            "On Android, DEX bytecode is decompiled to Java-like source with tools like JADX. "
            "The `AndroidManifest.xml` declares permissions, exported components (activities, "
            "services, broadcast receivers), deep link handlers, and backup/debug flags. Native "
            "`lib/` binaries may contain additional logic or anti-tamper checks.\n\n"
            "On iOS, IPA binaries are ARM Mach-O executables. Class metadata, strings, and "
            "Objective-C/Swift symbols reveal functionality. Keychain usage, URL schemes, and "
            "entitlements define what the app can access on the device."
        ),
        "exploitation": (
            "1. **Obtain the package** from Play Store, App Store, or program scope assets.\n"
            "2. **Decompile and map surface**: `jadx -d out app.apk` or use MobSF for a guided report.\n"
            "3. **Search for secrets**: grep decompiled output for API keys, tokens, AWS credentials, "
            "and internal hostnames.\n"
            "4. **Review manifest exports**: identify `android:exported=\"true\"` components that "
            "accept intents without authentication.\n"
            "5. **Trace network layer**: find Retrofit/OkHttp configs, certificate pinning hooks, "
            "and WebView JavaScript bridges.\n"
            "6. **Dynamic validation**: install on emulator/device, intercept traffic (after pinning "
            "bypass if needed), and confirm static findings.\n\n"
            "Chain findings: hardcoded admin API key + exported activity that loads arbitrary URLs "
            "can escalate to account takeover or data exfiltration."
        ),
        "defense": (
            "- **Never store secrets in the client**; use short-lived tokens from a backend.\n"
            "- Minimize exported components; require signature-level permissions for IPC.\n"
            "- Enable **ProGuard/R8** and native obfuscation; understand this is deterrence, not encryption.\n"
            "- Disable `android:allowBackup` unless backups are encrypted and scoped.\n"
            "- Implement certificate pinning and root/jailbreak detection as layered controls.\n"
            "- Run MobSF or similar in CI for every release build.\n"
            "- Follow **OWASP MASTG** and MASVS for structured testing and verification."
        ),
    },
    "mobile/frida": {
        "how_it_works": (
            "**Frida** is a dynamic instrumentation framework that injects a JavaScript runtime "
            "into running processes. On mobile, `frida-server` runs on the device and exposes an "
            "API to hook functions, replace return values, and inspect memory at runtime—without "
            "repackaging the app.\n\n"
            "Hooks attach to Java methods (via ART), native functions (via `Interceptor.attach`), "
            "and Objective-C selectors on iOS. Because checks execute in the app's process, Frida "
            "can bypass SSL pinning, root detection, and integrity verification that static "
            "analysis alone cannot defeat.\n\n"
            "Objection wraps Frida with a REPL for common mobile pentest tasks. **r2frida** "
            "combines Radare2's analysis with live Frida hooks for deeper native debugging."
        ),
        "exploitation": (
            "1. Deploy `frida-server` matching the device architecture (arm64).\n"
            "2. List apps: `frida-ps -Uai` and attach: `frida -U -f com.target.app -l script.js`.\n"
            "3. **Hook SSL pinning**: intercept `TrustManager`, `OkHttp CertificatePinner`, or "
            "BoringSSL verification routines and force success.\n"
            "4. **Bypass root checks**: hook `File.exists` on `/system/bin/su` or custom "
            "integrity classes to return false.\n"
            "5. **Extract crypto material**: hook `Cipher.doFinal`, `SecretKeySpec`, or token "
            "generation methods to log keys and plaintext.\n"
            "6. **Patch logic**: replace method implementations to skip license checks or enable "
            "debug features.\n\n"
            "Use Frida only on apps you own or have explicit authorization to test."
        ),
        "defense": (
            "- Detect Frida artifacts: named pipes, `frida-server` ports, suspicious loaded libraries.\n"
            "- Use **multiple integrity checks** at different layers (Java + native + server-side).\n"
            "- Rely on **server-side authorization**; client bypasses should not grant privilege.\n"
            "- Obfuscate sensitive native code; avoid single-point pinning implementations.\n"
            "- Monitor for hook frameworks in production via attestation (Play Integrity, DeviceCheck).\n"
            "- Rate-limit and anomaly-detect API usage patterns that indicate automated abuse."
        ),
    },
    "mobile/ssl-pinning-bypass": {
        "how_it_works": (
            "**SSL/TLS certificate pinning** binds an app to specific public keys or certificates "
            "instead of trusting the device's CA store. Even if a tester installs Burp's CA on a "
            "rooted device, the app rejects the intercepted connection because the proxy certificate "
            "does not match the pinned hash.\n\n"
            "Pinning may be implemented in the network stack (OkHttp `CertificatePinner`), "
            "NSURLSession delegates on iOS, or custom native TLS libraries. Some apps pin only "
            "production hosts while leaving staging environments interceptable—a common misconfiguration."
        ),
        "exploitation": (
            "1. **Identify pinning**: search decompiled code for `CertificatePinner`, `TrustKit`, "
            "`AFSSLPinningMode`, or `flutter_ssl_pinning`.\n"
            "2. **Frida universal scripts**: run community scripts that hook common pinning APIs.\n"
            "3. **Objection**: `android sslpinning disable` or `ios sslpinning disable`.\n"
            "4. **APK patching**: repackage with a modified `network_security_config.xml` that trusts "
            "user CAs (`apk-mitm`, manual `apktool` workflow).\n"
            "5. **Emulator with system CA**: Android 7+ requires placing the CA in the system store "
            "or using a Magisk module.\n"
            "6. Confirm interception in Burp/mitmproxy and replay API calls.\n\n"
            "Document which hosts were pinned and whether bypass affected all endpoints."
        ),
        "defense": (
            "- Pin **public keys** (SPKI hashes) rather than entire certificates to ease rotation.\n"
            "- Implement **backup pins** and a documented rotation procedure.\n"
            "- Combine pinning with **certificate transparency** monitoring for mis-issued certs.\n"
            "- Do not pin staging/dev builds with production keys; use separate trust stores.\n"
            "- Assume pinning can be bypassed on compromised devices; enforce auth and encryption "
            "at the application layer.\n"
            "- Test pinning with tools like `nabla` or MobSF and verify failure on proxy connections."
        ),
    },
    "mobile/deep-links": {
        "how_it_works": (
            "**Deep links** route users into specific app screens via custom URL schemes "
            "(`myapp://path`) or **App Links / Universal Links** (`https://domain/path`) verified "
            "by `assetlinks.json` (Android) or `apple-app-site-association` (iOS).\n\n"
            "When a link is opened, the OS dispatches an intent or hands off to the app with "
            "parameters that the target activity parses. If validation is missing, attackers can "
            "trigger unintended navigation, inject WebView content, steal tokens from URLs, or "
            "bypass authentication by reaching protected screens directly."
        ),
        "exploitation": (
            "1. **Enumerate schemes**: parse manifest for `intent-filter` data elements and iOS "
            "Info.plist URL types.\n"
            "2. **Fuzz parameters**: `adb shell am start -a android.intent.action.VIEW "
            "-d \"myapp://login?token=attacker\"`.\n"
            "3. **Test path traversal in handlers**: `myapp://../../admin` or open redirect chains.\n"
            "4. **WebView deep links**: if a handler loads URLs in WebView, test `javascript:` "
            "and file:// schemes for XSS.\n"
            "5. **Verify App Link ownership**: check if `assetlinks.json` is missing or allows "
            "wildcard paths—attackers may register overlapping domains.\n"
            "6. **Chain with phishing**: send malicious links that auto-open the app and exfiltrate "
            "session data via query parameters reflected in logs or analytics.\n\n"
            "Use Burp Collaborator or custom logging to detect server-side callbacks from deep link opens."
        ),
        "defense": (
            "- **Validate every parameter** before navigation; use allowlists for paths and hosts.\n"
            "- Require authentication before sensitive screens; deep links should not skip login.\n"
            "- Disable WebView JavaScript or use `shouldOverrideUrlLoading` with strict allowlists.\n"
            "- Implement **App Link / Universal Link verification** correctly; avoid wildcard paths.\n"
            "- Never put secrets (tokens, PII) in deep link query strings.\n"
            "- Log and monitor anomalous deep link patterns; test with OWASP MASTG deep link test cases."
        ),
    },
    "automation/js-analysis": {
        "how_it_works": (
            "Modern web apps ship large **JavaScript bundles** (webpack, Vite, Next.js) that contain "
            "API routes, internal admin paths, GraphQL queries, AWS keys, and business logic. "
            "Source maps—often left on production—reconstruct original TypeScript files.\n\n"
            "Attackers crawl live sites, archive historical JS from Wayback/Common Crawl, and run "
            "pattern matchers to extract endpoints and secrets faster than manual browsing. "
            "Minification hides names but not string literals, so hardcoded URLs and keys remain visible."
        ),
        "exploitation": (
            "1. **Collect JS**: use Katana, gau, or browser devtools to download all `.js` assets.\n"
            "2. **LinkFinder / SecretFinder**: scan for paths, API keys, S3 buckets, and JWT patterns.\n"
            "3. **Source maps**: probe `main.js.map` or `webpack://` references; decompile to source.\n"
            "4. **Chunk diffing**: compare bundle hashes between deployments for new hidden routes.\n"
            "5. **Beautify and grep**: search for `fetch(`, `axios`, `graphql`, `admin`, `internal`.\n"
            "6. **Validate findings**: probe discovered endpoints with httpx/nuclei; never assume "
            "secrets are live without testing.\n\n"
            "Automate in CI recon pipelines to alert when new secrets appear in client bundles."
        ),
        "defense": (
            "- **Never embed secrets** in client-side code; use backend proxies for third-party APIs.\n"
            "- Disable or restrict **source map** publication in production builds.\n"
            "- Split admin and internal tooling into separate origins not linked from public JS.\n"
            "- Use environment-specific builds; strip debug routes from production bundles.\n"
            "- Scan releases with trufflehog or custom regex in CI before deploy.\n"
            "- Implement CSP and avoid exposing sensitive logic that should live server-side only."
        ),
    },
    "automation/diffing": {
        "how_it_works": (
            "**Change detection** compares snapshots of targets over time—subdomains, HTTP responses, "
            "JavaScript bundles, OpenAPI specs, and DNS records—to surface new attack surface without "
            "re-running full manual recon.\n\n"
            "Bug bounty programs and mature security teams baseline assets after each deploy. "
            "Diffing highlights newly exposed APIs, forgotten staging hosts, or relaxed CORS policies "
            "that static one-time scans miss."
        ),
        "exploitation": (
            "1. **Baseline**: store subs, live URLs, JS hashes, and nuclei results in dated snapshots.\n"
            "2. **Schedule periodic runs**: GitHub Actions, cron, or axiom fleets on weekly cadence.\n"
            "3. **Diff tools**: `diff` on sorted lists; `nuclei -compare` or custom Python set operations.\n"
            "4. **OpenAPI diff**: compare Swagger versions for new parameters and auth changes.\n"
            "5. **Alert on deltas**: notify Slack when new subdomains or 200 responses appear on "
            "high-value paths.\n"
            "6. **Prioritize**: new `/api/v2/admin` endpoint warrants immediate manual review.\n\n"
            "Combine passive sources (crt.sh, SecurityTrails) with active probing for complete coverage."
        ),
        "defense": (
            "- Maintain an **asset inventory** with ownership and expected change windows.\n"
            "- Require security review for new public endpoints before production deploy.\n"
            "- Monitor external attack surface continuously (ASM platforms or open-source stacks).\n"
            "- Lock down staging with VPN/IP allowlists; do not rely on obscurity.\n"
            "- Automate drift detection on IaC and firewall rules alongside application diffs.\n"
            "- Document which assets are in scope so unauthorized new hosts are caught quickly."
        ),
    },
    "automation/scope-tooling": {
        "how_it_works": (
            "Bug bounty **scope** defines which domains, apps, and IP ranges researchers may test "
            "and what is forbidden (DoS, social engineering, out-of-scope subsidiaries). Programs "
            "publish scope on HackerOne, Bugcrowd, Intigriti, or private portals—often in inconsistent formats.\n\n"
            "**Scope tooling** parses these rules into machine-readable lists, validates targets before "
            "scanning, and tracks program-specific notes. Testing out-of-scope assets violates program "
            "rules and may have legal consequences."
        ),
        "exploitation": (
            "1. **Import scope**: use `bbscope` for HackerOne/Bugcrowd/Intigriti YAML exports.\n"
            "2. **Normalize rules**: convert wildcards (`*.target.com`) to regex or explicit lists.\n"
            "3. **Pre-flight check**: before nuclei/ffuf, verify hostname matches in-scope patterns.\n"
            "4. **Track assets**: spreadsheet or Notion with program, asset, bounty tier, and status.\n"
            "5. **Monitor scope changes**: programs add acquisitions and new APIs frequently.\n"
            "6. **Respect exclusions**: shared infrastructure, third-party SaaS, and customer data "
            "are typically out of scope even if technically reachable.\n\n"
            "When scope is ambiguous, ask the program before testing—document the response."
        ),
        "defense": (
            "- Publish **clear, machine-readable scope** with examples of in/out boundaries.\n"
            "- Separate production from sandbox assets in scope documentation.\n"
            "- Provide a **safe reporting channel** for scope questions.\n"
            "- Monitor for scans against out-of-scope assets and correlate with program engagement.\n"
            "- Update scope promptly when launching new products or domains.\n"
            "- Use asset tags in ASM tools so internal teams know which surfaces are bounty-eligible."
        ),
    },
    "reporting/vulnerability-reports": {
        "how_it_works": (
            "A **vulnerability report** translates a technical finding into actionable intelligence "
            "for developers and risk owners. Effective reports include impact, reproduction steps, "
            "evidence, and remediation—structured so triagers can validate quickly and engineers can fix without guesswork.\n\n"
            "Bug bounty triagers process hundreds of submissions; vague reports get closed as "
            "N/A or informative. Pentest deliverables add executive summaries mapping findings to "
            "business risk and compliance frameworks (PCI, SOC 2)."
        ),
        "exploitation": (
            "1. **Title**: concise impact statement (e.g., \"IDOR exposes all user invoices\").\n"
            "2. **Severity**: use program matrix or CVSS 3.1 with vector string justification.\n"
            "3. **Steps to reproduce**: numbered, minimal, with exact URLs, headers, and bodies.\n"
            "4. **Proof of concept**: screenshots, HTTP requests (Burp export), or short video.\n"
            "5. **Impact**: what an attacker gains—data types, account types, regulatory exposure.\n"
            "6. **Remediation**: specific fix (parameterized queries, authz check on resource ID).\n"
            "7. **References**: CWE, OWASP, prior similar reports if helpful.\n\n"
            "Redact PII and production credentials; use test accounts created for the engagement."
        ),
        "defense": (
            "- Establish **internal report templates** for consistent triage and metrics.\n"
            "- Train developers on reading PoCs and reproducing in staging.\n"
            "- Set SLA targets for acknowledgment and resolution by severity.\n"
            "- Use structured intake (HackerOne, Jira security) with required fields.\n"
            "- Feed confirmed bugs into regression tests and threat models.\n"
            "- Publish safe disclosure timelines and thank researchers who report in good faith."
        ),
    },
    "growth/cve-research": {
        "how_it_works": (
            "**CVE** (Common Vulnerabilities and Exposures) identifiers catalog publicly known "
            "security flaws. The NVD enriches CVEs with CVSS scores; CISA KEV lists actively exploited "
            "issues. Security researchers monitor disclosures to patch their stacks, build detections, "
            "and publish analysis.\n\n"
            "New CVEs often include insufficient detail for reproduction; vendor advisories and "
            "GitHub commits may be needed to understand exploitability in real deployments."
        ),
        "exploitation": (
            "1. **Monitor feeds**: NVD RSS, vendor security bulletins, GitHub Security Advisories, "
            "exploit-db, Packet Storm.\n"
            "2. **Map to inventory**: correlate CVE product strings with your CMDB and nuclei templates.\n"
            "3. **Prioritize**: CISA KEV + internet-exposed + high CVSS = immediate action.\n"
            "4. **Lab reproduction**: isolate vulnerable version in VM/container; never test on "
            "production without authorization.\n"
            "5. **Build detections**: Sigma rules, WAF signatures, or version checks for blue team.\n"
            "6. **Share responsibly**: coordinate disclosure if you discover variants or bypasses.\n\n"
            "Track patch availability and compensating controls when immediate upgrade is impossible."
        ),
        "defense": (
            "- Maintain **accurate asset inventory** with version numbers for critical software.\n"
            "- Subscribe to vendor security mailing lists and enable Dependabot/Renovate.\n"
            "- Patch KEV-listed vulnerabilities on aggressive timelines.\n"
            "- Use virtual patching (WAF, IPS) only as temporary mitigation.\n"
            "- Segment networks so vulnerable services are not internet-exposed.\n"
            "- Run continuous vulnerability scanning with authenticated checks where possible."
        ),
    },
    "growth/writeups": {
        "how_it_works": (
            "**Security writeups** document how a vulnerability was found and exploited, building "
            "researcher reputation, educating the community, and demonstrating methodology to employers "
            "and program triagers.\n\n"
            "Quality writeups explain root cause—not just the payload—and show unique techniques. "
            "Platforms like HackerOne Hacktivity, Infosec Writeups, and personal blogs serve as "
            "portfolio pieces. Poor writeups leak customer data or violate disclosure agreements."
        ),
        "exploitation": (
            "1. **Document during testing**: save requests, notes, and timestamps as you work.\n"
            "2. **Structure**: summary, background, discovery, exploitation, impact, remediation, timeline.\n"
            "3. **Teach**: explain why the bug exists, not only how to trigger it.\n"
            "4. **Redact**: replace real domains, user emails, and tokens with placeholders.\n"
            "5. **Respect disclosure**: wait for fix or program permission before publishing.\n"
            "6. **Cross-post**: blog + Hacktivity + Twitter thread with link to full analysis.\n"
            "7. **Engage**: respond to comments; correct errors; credit collaborators.\n\n"
            "Unique writeups on novel attack classes attract program invites and conference talks."
        ),
        "defense": (
            "- Organizations should **welcome responsible writeups** after fixes ship.\n"
            "- Provide researchers clear disclosure policies and safe harbor statements.\n"
            "- Use public writeups as free QA—review for missed variants in your codebase.\n"
            "- Encourage internal engineers to publish defensive perspectives and patch deep-dives.\n"
            "- Monitor Hacktivity for reports against your products even outside formal programs.\n"
            "- Build a culture where findings lead to systemic fixes, not just one-line patches."
        ),
    },
    "cryptography/crypto-flaws": {
        "how_it_works": (
            "Applications misuse cryptography in predictable ways: **weak algorithms** (MD5, SHA1 "
            "for passwords, DES, RC4), **ECB mode** leaking block patterns, **static IVs** enabling "
            "replay, **hardcoded keys** in source, and **insufficient entropy** in tokens.\n\n"
            "Custom crypto implementations almost always fail. Even standard libraries are misused "
            "when developers skip authentication (encrypt-only AES-CBC), truncate HMACs, or compose "
            "primitives incorrectly."
        ),
        "exploitation": (
            "1. **Inventory crypto usage**: search code for `Cipher.getInstance`, `AES`, `RSA`, "
            "`random`, `Math.random`.\n"
            "2. **Protocol review**: identify what is encrypted vs signed vs both (encrypt-then-MAC).\n"
            "3. **Test weak modes**: ECB ciphertext reveals repeated blocks; compare identical "
            "plaintext blocks across messages.\n"
            "4. **Key recovery**: grep for PEM files, base64 keys in configs, and default passwords.\n"
            "5. **Token analysis**: decode session tokens; check length, charset, and predictability.\n"
            "6. **Oracle conditions**: distinguish error messages for padding vs MAC failures.\n\n"
            "Use testssl.sh and manual review for TLS; Burp for application-layer crypto tokens."
        ),
        "defense": (
            "- Use **AES-GCM or ChaCha20-Poly1305** for authenticated encryption; avoid ECB.\n"
            "- Hash passwords with **Argon2id** or bcrypt with per-user salts.\n"
            "- Generate keys and IVs with `SecureRandom` or platform CSPRNG APIs.\n"
            "- Never implement custom ciphers or MAC constructions.\n"
            "- Rotate keys with documented procedures; use HSMs or KMS for master keys.\n"
            "- Follow OWASP Cryptographic Storage Cheat Sheet and NIST SP 800-57."
        ),
    },
    "cryptography/padding-oracle": {
        "how_it_works": (
            "A **padding oracle** arises when an application using **CBC mode** returns different "
            "errors for invalid padding vs invalid plaintext—often after decryption. The attacker "
            "can submit modified ciphertext blocks and learn whether padding is valid, enabling "
            "**byte-by-byte decryption** without the key.\n\n"
            "Classic examples include ASP.NET `ViewState`, WAF-decrypted cookies, and legacy "
            "APIs that decrypt client-supplied blobs. Modern **authenticated encryption** (GCM) "
            "and proper error handling eliminate this class when implemented correctly."
        ),
        "exploitation": (
            "1. **Identify encrypted cookies or parameters** (base64, block-aligned lengths).\n"
            "2. **Confirm oracle**: flip bits in the last byte of a block; observe padding error vs "
            "success/other error.\n"
            "3. **Automate**: PadBuster, Poracle, or custom scripts for byte-at-a-time decryption.\n"
            "4. **Decrypt**: recover session tokens, serialized objects, or JSON claims.\n"
            "5. **Encrypt/forgery**: reverse the oracle to craft valid ciphertext (e.g., elevate "
            "role in decrypted cookie).\n"
            "6. **Validate impact**: replay forged tokens in the application.\n\n"
            "Timing-based oracles require statistical analysis of response times instead of error strings."
        ),
        "defense": (
            "- Use **AES-GCM, AES-CCM, or ChaCha20-Poly1305** instead of CBC without authentication.\n"
            "- If CBC is required, apply **encrypt-then-MAC** with constant-time MAC verification.\n"
            "- Return **generic errors** for all decryption failures; log details server-side only.\n"
            "- Implement constant-time comparison for MACs and tags.\n"
            "- Migrate legacy ViewState and cookie encryption to signed, authenticated formats.\n"
            "- Test with padding oracle scanners during security assessments."
        ),
    },
    "cryptography/tls-ssl": {
        "how_it_works": (
            "**TLS** negotiates cipher suites, certificates, and key exchange between client and server. "
            "Misconfigurations expose **deprecated protocols** (SSLv3, TLS 1.0/1.1), **weak ciphers** "
            "(RC4, 3DES, NULL), **certificate problems** (expired, wrong hostname, weak RSA keys), "
            "and **missing features** (HSTS, OCSP stapling).\n\n"
            "Termination at load balancers, CDNs, and Kubernetes ingress adds layers where settings "
            "may differ from origin servers. Mixed content and TLS downgrades remain relevant on "
            "legacy applications."
        ),
        "exploitation": (
            "1. **Scan**: `testssl.sh target.com` or `sslyze --regular target:443`.\n"
            "2. **Protocol downgrade**: test SSLv3/TLS1.0 support and POODLE/BEAST relevance.\n"
            "3. **Cipher audit**: identify NULL, EXPORT, or anonymous suites.\n"
            "4. **Certificate review**: weak key length, SHA-1 signatures, missing SANs.\n"
            "5. **HSTS**: check for absent or short `max-age`; test subdomain inclusion.\n"
            "6. **Renegotiation and compression**: CRIME/BREACH on HTTPS compression.\n"
            "7. **Internal TLS**: scan management interfaces (Kubernetes API, Elasticsearch).\n\n"
            "Document findings per endpoint; CDN-fronted sites may show different configs than origin."
        ),
        "defense": (
            "- Enforce **TLS 1.2+** (prefer TLS 1.3); disable SSLv2/v3 and TLS 1.0/1.1.\n"
            "- Use strong cipher suites; prefer ECDHE with AES-GCM or ChaCha20.\n"
            "- Deploy **HSTS** with `max-age` ≥ one year and `includeSubDomains` where appropriate.\n"
            "- Automate certificate renewal (Let's Encrypt, ACME) and monitor expiry.\n"
            "- Enable OCSP stapling; use CA/Browser Forum baseline requirements.\n"
            "- Align CDN, load balancer, and origin TLS policies; scan continuously with sslyze or Mozilla SSL Config Generator."
        ),
    },
    "containers/docker": {
        "how_it_works": (
            "**Docker** packages applications with dependencies into images run as isolated containers "
            "on shared kernels. Security depends on namespace/cgroup isolation, image contents, "
            "runtime flags (`--privileged`, volume mounts, capabilities), and daemon configuration.\n\n"
            "Images often contain CVEs, leaked secrets in layers, and root-default processes. "
            "The Docker socket (`/var/run/docker.sock`) mounted into a container grants host-level "
            "control—equivalent to root on the host."
        ),
        "exploitation": (
            "1. **Image scan**: `trivy image target:tag` and `grype` for CVEs and secrets.\n"
            "2. **Runtime config**: check `docker inspect` for privileged mode, cap_add, host PID/network.\n"
            "3. **Socket mount**: if `docker.sock` is mounted, run `docker -H unix:///var/run/docker.sock run` "
            "to escape to host.\n"
            "4. **Secrets in layers**: `docker history` and dive for env vars and files in image history.\n"
            "5. **Registry exposure**: scan for public registries with pull access to prod images.\n"
            "6. **Container escape**: test known kernel CVEs only in authorized lab scope.\n\n"
            "Use Docker Bench for Security for host-level configuration checks."
        ),
        "defense": (
            "- Run containers as **non-root**; use read-only root filesystems where possible.\n"
            "- Drop all capabilities; add only required ones; apply default seccomp/AppArmor profiles.\n"
            "- Never mount **docker.sock** into containers; use dedicated CI builders.\n"
            "- Scan images in CI/CD; block deploy on critical CVEs.\n"
            "- Use minimal base images (distroless, Alpine) and pin digests.\n"
            "- Follow CIS Docker Benchmark; enable user namespaces and rootless Docker where feasible."
        ),
    },
    "containers/kubernetes-security": {
        "how_it_works": (
            "**Kubernetes** orchestrates containers across nodes with RBAC, admission controllers, "
            "network policies, and secrets stored in etcd. Misconfigurations—overly permissive "
            "ClusterRoleBindings, default service accounts with API access, secrets in ConfigMaps, "
            "missing NetworkPolicies—allow lateral movement and cluster takeover.\n\n"
            "The API server, kubelet, and etcd are high-value targets. Workloads in the same cluster "
            "often share flat network visibility unless policies segment traffic."
        ),
        "exploitation": (
            "1. **Recon from pod**: `kubectl auth can-i --list` if kubeconfig or token is available.\n"
            "2. **Enumerate**: pods, secrets, configmaps, rolebindings across namespaces.\n"
            "3. **Privileged pods**: create or exec into pods with hostPath, hostPID, or privileged securityContext.\n"
            "4. **Secrets theft**: read secrets in accessible namespaces; decode base64 credentials.\n"
            "5. **kube-hunter / kubescape**: automated misconfiguration scans.\n"
            "6. **Network**: if no NetworkPolicy, scan cluster internal services from compromised pod.\n\n"
            "Peirates and CDK automate common K8s privilege escalation paths from inside a pod."
        ),
        "defense": (
            "- Apply **least-privilege RBAC**; avoid cluster-admin bindings for applications.\n"
            "- Enable **Pod Security Standards** (restricted baseline) via admission controllers.\n"
            "- Encrypt etcd; restrict API server access; enable audit logging.\n"
            "- Use **NetworkPolicies** for default-deny between namespaces.\n"
            "- Rotate service account tokens; disable auto-mount where not needed.\n"
            "- Run kubescape, kube-bench, and Falco for policy and runtime threat detection."
        ),
    },
    "containers/container-escape": {
        "how_it_works": (
            "**Container escape** breaks isolation between a container and the host kernel or "
            "other containers. Vectors include **privileged containers**, **host namespace sharing**, "
            "mounted **host paths** (`/`, `/proc`, docker.sock), **kernel exploits**, and "
            "abuse of **Linux capabilities** (CAP_SYS_ADMIN, CAP_DAC_READ_SEARCH).\n\n"
            "cgroups v1 `release_agent` attacks write commands executed on the host when cgroup "
            "limits are exceeded. CVEs in runc, containerd, and the kernel periodically enable "
            "new escape primitives."
        ),
        "exploitation": (
            "1. **Enumerate**: `capsh --print`, check `/proc/1/cgroup`, mount points, and `id`.\n"
            "2. **docker.sock**: instantiate host-root container as described in Docker section.\n"
            "3. **Privileged + hostPath**: mount host disk and chroot into host filesystem.\n"
            "4. **release_agent**: CDK/deepce automate cgroup escape on vulnerable configurations.\n"
            "5. **Kernel exploits**: match `uname -r` to known CVEs (Dirty Pipe, etc.) in lab only.\n"
            "6. **Confirm escape**: create file on host or read `/etc/shadow` from host mount.\n\n"
            "Document exact misconfiguration; escapes are often configuration bugs not kernel bugs."
        ),
        "defense": (
            "- Never run **privileged** containers in production; validate with admission policy.\n"
            "- Block hostPath mounts except tightly controlled exceptions.\n"
            "- Keep kernel, runc, and containerd **patched**; subscribe to security advisories.\n"
            "- Use gVisor or Kata Containers for stronger isolation on multi-tenant workloads.\n"
            "- Monitor for escape indicators: unexpected mounts, cgroup writes, docker API from pods.\n"
            "- Regularly pentest cluster configurations with kube-hunter from both outside and inside."
        ),
    },
    "devsecops/pipeline-security": {
        "how_it_works": (
            "**CI/CD pipelines** build, test, and deploy software with access to source code, "
            "cloud credentials, signing keys, and production deploy triggers. Compromise of a "
            "pipeline job (malicious PR, stolen `GITHUB_TOKEN`, poisoned action) equals compromise "
            "of everything the pipeline can touch.\n\n"
            "GitHub Actions, GitLab CI, Jenkins, and CircleCI each have distinct permission models. "
            "Fork PR workflows, cached secrets in logs, and unpinned third-party actions are "
            "recurring vulnerability patterns."
        ),
        "exploitation": (
            "1. **Review workflows**: read `.github/workflows` for `pull_request_target`, excessive permissions.\n"
            "2. **Poisoned PR**: submit workflow change that exfiltrates secrets on `pull_request_target`.\n"
            "3. **Action pinning**: unpinned `@main` actions can be swapped to malicious versions.\n"
            "4. **Log leakage**: trigger builds that print secrets to stdout (env vars, masked poorly).\n"
            "5. **Artifact tampering**: replace build artifacts if signing and provenance are absent.\n"
            "6. **OIDC abuse**: misconfigured cloud trust policies accepting tokens from any repo.\n\n"
            "Use GitHub's workflow permission settings and branch protection as baseline controls."
        ),
        "defense": (
            "- Use **least-privilege** workflow permissions; default `contents: read` only.\n"
            "- Pin actions to **full commit SHAs**; verify with allowed-actions policies.\n"
            "- Avoid `pull_request_target` unless strictly necessary; never checkout untrusted PR code with secrets.\n"
            "- Store secrets in vault/OIDC; rotate tokens; never echo secrets in logs.\n"
            "- Sign artifacts with **Sigstore/cosign**; verify provenance with SLSA builders.\n"
            "- Follow OWASP Top 10 CI/CD Security Risks; audit pipelines quarterly."
        ),
    },
    "devsecops/iac-security": {
        "how_it_works": (
            "**Infrastructure as Code** (Terraform, CloudFormation, Pulumi, Kubernetes YAML) defines "
            "cloud resources declaratively. Misconfigurations—public S3 buckets, open security groups, "
            "overly permissive IAM, unencrypted databases—are committed to git and deployed at scale.\n\n"
            "State files (Terraform `.tfstate`) often contain secrets in plaintext. PR-based IaC "
            "changes bypass traditional change boards if policy checks are not enforced in CI."
        ),
        "exploitation": (
            "1. **Static scan**: `checkov -d .`, `tfsec`, `kics` on all IaC directories.\n"
            "2. **Manual review**: `0.0.0.0/0` ingress, `Principal: *`, missing encryption flags.\n"
            "3. **State file access**: if `.tfstate` is in S3 without encryption/IAM, extract secrets.\n"
            "4. **Drift detection**: compare deployed resources vs templates for shadow admin accounts.\n"
            "5. **Module supply chain**: third-party Terraform modules pulling unexpected providers.\n"
            "6. **Kubernetes manifests**: privileged pods, hostNetwork, wildcard RBAC in git.\n\n"
            "Integrate IaC scanning in PR checks; block merge on critical findings."
        ),
        "defense": (
            "- Run **policy-as-code** (OPA, Sentinel, Kyverno) on every IaC PR.\n"
            "- Encrypt and restrict access to **Terraform state**; use remote backends with locking.\n"
            "- Prohibit public access defaults; use SCPs at org level as guardrails.\n"
            "- Peer review all infrastructure changes; separate prod apply roles.\n"
            "- Scan for secrets in IaC with git-secrets and trufflehog.\n"
            "- Maintain golden modules with secure defaults; deprecate risky patterns."
        ),
    },
    "devsecops/supply-chain": {
        "how_it_works": (
            "**Software supply chain** attacks compromise dependencies, build tools, or distribution "
            "channels so malicious code reaches downstream users. Examples include npm/PyPI "
            "typosquatting, compromised maintainer accounts, SolarWinds-style build injection, and "
            "unsigned container images.\n\n"
            "Modern apps depend on hundreds of transitive packages. A single hijacked dependency "
            "version can steal environment variables, add backdoors, or sabotage builds."
        ),
        "exploitation": (
            "1. **Dependency audit**: `npm audit`, `pip-audit`, Dependabot alerts; review transitive deps.\n"
            "2. **Typosquatting hunt**: search registries for packages mimicking internal names.\n"
            "3. **SBOM diff**: compare Syft-generated SBOMs between releases for new publishers.\n"
            "4. **Build review**: inspect CI for unpinned tools and post-install scripts (`preinstall`).\n"
            "5. **Registry hygiene**: verify image signatures before deploy (`cosign verify`).\n"
            "6. **Maintainer impersonation**: monitor for sudden major version bumps from new contributors.\n\n"
            "Researcher perspective: report malicious packages to registries; publish IOCs responsibly."
        ),
        "defense": (
            "- **Pin dependencies** to exact versions; commit lockfiles; review lockfile changes in PRs.\n"
            "- Generate and store **SBOMs** (CycloneDX, SPDX) for every release.\n"
            "- Sign artifacts and images; enforce signature verification in deploy pipelines.\n"
            "- Use private registries and npm/pypi proxies with malware scanning.\n"
            "- Disable arbitrary post-install scripts in CI sandboxes where possible.\n"
            "- Adopt **SLSA** levels incrementally; monitor CISA guidance on supply chain security."
        ),
    },
    "binary/reverse-engineering": {
        "how_it_works": (
            "**Reverse engineering** recovers program logic from compiled binaries without source code. "
            "Disassemblers (Ghidra, IDA) lift machine code to intermediate representations; debuggers "
            "(gdb, x64dbg) observe runtime state. Analysts identify **entry points**, **string references**, "
            "**crypto constants**, and **network protocols**.\n\n"
            "Binaries may be stripped of symbols, obfuscated, or packed. Anti-debug and anti-VM "
            "techniques slow analysis but rarely stop determined researchers with sufficient time."
        ),
        "exploitation": (
            "1. **Initial triage**: `strings`, `file`, `binwalk`, entropy analysis for packing.\n"
            "2. **Load in Ghidra**: auto-analyze, rename functions, annotate key logic.\n"
            "3. **Cross-references**: follow calls from `strcmp`, `recv`, `printf` to validation routines.\n"
            "4. **Dynamic trace**: gdb with breakpoints on compare instructions for license checks.\n"
            "5. **Patch binary**: NOP out jumps or modify constants for proof-of-concept (authorized only).\n"
            "6. **Document**: export decompiler output with comments for report appendices.\n\n"
            "For malware, work only in isolated VMs with no network egress."
        ),
        "defense": (
            "- Assume binaries can be reversed; **do not rely on client-side secrecy**.\n"
            "- Use server-side validation for licenses, auth, and critical business rules.\n"
            "- Apply obfuscation and anti-tamper as **delay layers**, not primary security.\n"
            "- Strip symbols in release builds; avoid embedding secrets in binaries.\n"
            "- Monitor for cracked distributions; use legal and technical responses as appropriate.\n"
            "- For sensitive firmware, encrypt payloads and verify integrity at boot."
        ),
    },
    "binary/stack-overflow": {
        "how_it_works": (
            "A **stack buffer overflow** writes past the end of a stack-allocated buffer, corrupting "
            "adjacent data—the saved return address, stack canaries, or frame pointers. When the "
            "function returns, execution may jump to attacker-controlled addresses, enabling arbitrary code execution.\n\n"
            "Modern mitigations include stack canaries, ASLR, DEP/NX, and FORTIFY_SOURCE. Exploitation "
            "often requires leaking addresses, building ROP chains, or finding misconfigured binaries "
            "compiled without protections."
        ),
        "exploitation": (
            "1. **Fuzz input**: trigger crashes with long strings, format strings, or malformed packets.\n"
            "2. **Determine offset**: pattern create (`pwntools cyclic`) to find return address overwrite offset.\n"
            "3. **Check protections**: `checksec` for NX, canary, RELRO, PIE.\n"
            "4. **Canary bypass**: leak canary via format string or partial overwrite if possible.\n"
            "5. **ROP**: build chain with ropper/ROPgadget when NX is enabled.\n"
            "6. **Shellcode**: direct jump to mapped executable stack only in legacy/lab binaries.\n\n"
            "Practice on CTF binaries and authorized vuln servers; document reliability and mitigations."
        ),
        "defense": (
            "- Compile with **stack canaries**, `-fstack-protector-strong`, and FORTIFY_SOURCE.\n"
            "- Enable **ASLR and DEP/NX**; use RELRO and PIE for shared libraries and binaries.\n"
            "- Replace unsafe functions (`strcpy`, `sprintf`) with bounded alternatives.\n"
            "- Use memory-safe languages for new components; sandbox native code with seccomp.\n"
            "- Fuzz native code with AFL++, libFuzzer; fix crashes before release.\n"
            "- Deploy WAF/IPS only as supplement; fix root cause in binary."
        ),
    },
    "binary/heap-exploitation": {
        "how_it_works": (
            "**Heap exploitation** targets dynamic memory allocators (glibc malloc, jemalloc, tcmalloc). "
            "Bugs like **buffer overflows into adjacent chunks**, **use-after-free**, **double free**, "
            "and **integer overflows** corrupt heap metadata or freed object contents.\n\n"
            "Attackers forge chunk headers or abuse allocator behavior to achieve arbitrary write "
            "primitives, then overwrite `__free_hook`, GOT entries, or function pointers for code execution. "
            "Heap attacks are less linear than stack overflows and allocator-specific."
        ),
        "exploitation": (
            "1. **Identify allocator**: glibc version from `ldd` or `/proc/version`.\n"
            "2. **Trigger bug**: UAF by racing threads, or overflow into next chunk.\n"
            "3. **Study allocator**: read how2heap for tcache, fastbin, unsorted bin techniques.\n"
            "4. **Build primitive**: overlap chunks (house of spirit, tcache poisoning) for arbitrary write.\n"
            "5. **Target**: overwrite `__malloc_hook`, `__free_hook`, or C++ vtable pointers.\n"
            "6. **pwntools/gdb**: debug heap layout with `heap` commands in pwndbg/gef.\n\n"
            "Heap exploitation is advanced; validate only in CTF/lab with explicit authorization."
        ),
        "defense": (
            "- Fix memory corruption at source; use **AddressSanitizer** and UBSan in CI tests.\n"
            "- Update glibc and allocator libraries; enable hardened malloc options where available.\n"
            "- Reduce attack surface: minimize native code, use Rust with safe defaults.\n"
            "- Fuzz heap-heavy code paths continuously.\n"
            "- Enable **Control Flow Integrity** and sandboxing for untrusted native modules.\n"
            "- For browsers and JITs, follow industry standard isolation (site isolation, sandbox processes)."
        ),
    },
    "osint/people-org": {
        "how_it_works": (
            "**OSINT** on people and organizations collects publicly available data—social profiles, "
            "job postings, press releases, WHOIS, certificate transparency, GitHub commits, and "
            "government filings—to map structure, technology stack, and personnel without touching "
            "target systems directly.\n\n"
            "Attackers use OSINT for spear-phishing target selection, password guessing (company "
            "mascot + year), and identifying forgotten subdomains. Researchers must respect privacy "
            "laws (GDPR, CFAA boundaries) and program rules."
        ),
        "exploitation": (
            "1. **Organization mapping**: LinkedIn employees, job ads listing tech stack, Crunchbase.\n"
            "2. **Email format**: discover `first.last@` patterns from press releases or Hunter.io.\n"
            "3. **Infrastructure**: reverse WHOIS, crt.sh for cert names, Shodan for org netblocks.\n"
            "4. **Code leaks**: GitHub search for `org:target password`, Pastebin monitoring.\n"
            "5. **Social graphs**: Maltego transforms linking domains, people, and email addresses.\n"
            "6. **Document sources**: maintain citation list for report defensibility.\n\n"
            "Stay within legal boundaries and program scope; OSINT on individuals may be restricted."
        ),
        "defense": (
            "- **Minimize public exposure**: review what job posts and social media reveal.\n"
            "- Enforce **GitHub secret scanning** and DLP on code repositories.\n"
            "- Register defensive domains for common typosquats.\n"
            "- Train employees on social media and LinkedIn information sharing policies.\n"
            "- Monitor certificate transparency and new subdomain registrations for impersonation.\n"
            "- Conduct periodic OSINT self-assessments to see attacker-visible attack surface."
        ),
    },
    "osint/data-breach-search": {
        "how_it_works": (
            "**Data breach datasets** aggregate credentials and PII from past compromises, sold or "
            "leaked on criminal forums and indexed by services like Have I Been Pwned. Security teams "
            "check whether employee or customer emails appear in breaches to drive password resets and MFA adoption.\n\n"
            "Unauthorized use of breach data for account takeover violates computer fraud laws and "
            "bug bounty rules. Legitimate use is defensive: credential stuffing prevention and awareness."
        ),
        "exploitation": (
            "1. **Authorized services only**: HIBP API with k-anonymity, enterprise breach monitoring.\n"
            "2. **Scope check**: verify testing corporate emails is permitted in engagement ROE.\n"
            "3. **Validate passwords**: never log into user accounts with leaked creds outside lab.\n"
            "4. **Report findings**: count of affected emails, breach sources, recommendation for MFA.\n"
            "5. **Credential stuffing test**: in pentest, use known breach pairs only on client-owned "
            "test accounts with permission.\n"
            "6. **Monitor dark web**: brand monitoring for new dumps mentioning the organization.\n\n"
            "Researchers: do not publish raw breach data; reference breach name and date only."
        ),
        "defense": (
            "- Enforce **MFA** on all external-facing and admin authentication.\n"
            "- Block password reuse via breach password list checks at registration and login.\n"
            "- Subscribe to HIBP Domain Search or equivalent for employee credential monitoring.\n"
            "- Force reset when breaches affect corporate identities.\n"
            "- Detect credential stuffing with rate limits, CAPTCHA, and impossible travel signals.\n"
            "- Never store passwords in reversible encryption; use strong hashing for any secrets."
        ),
    },
    "social-engineering/phishing": {
        "how_it_works": (
            "**Phishing** deceives users into clicking malicious links, opening attachments, or "
            "entering credentials on fake sites. **Authorized phishing assessments** simulate these "
            "attacks to measure awareness and technical controls (email filtering, link protection).\n\n"
            "Campaigns use cloned login pages, OAuth consent phishing, QR codes, and thread hijacking. "
            "Success rates inform training priorities; unauthorized phishing is illegal and harmful."
        ),
        "exploitation": (
            "1. **Written authorization** specifying targets, timing, and forbidden tactics.\n"
            "2. **Platform setup**: Gophish or King Phisher with tracking on controlled infrastructure.\n"
            "3. **Template design**: realistic but safe—no malware attachments unless explicitly scoped.\n"
            "4. **Landing page**: clone internal portal; capture metrics only, not real passwords "
            "(or use unique tokens per user).\n"
            "5. **Measure**: open rate, click rate, submission rate, report-to-security rate.\n"
            "6. **Debrief**: immediate training for clickers; positive reinforcement for reporters.\n\n"
            "Coordinate with IT to whitelist test infrastructure and avoid help desk overload."
        ),
        "defense": (
            "- Deploy **email authentication** (DMARC p=reject), anti-phishing gateways, and URL rewriting.\n"
            "- Enable **FIDO2/WebAuthn**; phishing-resistant MFA stops credential theft.\n"
            "- Run regular simulations with improving metrics over time.\n"
            "- Easy **report phish** button integrated with SOC workflows.\n"
            "- Browser isolation for risky links; block newly registered domains at egress.\n"
            "- Executive protection program for high-value targets (spear-phish monitoring)."
        ),
    },
    "social-engineering/pretexting": {
        "how_it_works": (
            "**Pretexting** builds a fabricated scenario (IT support, vendor, auditor) to manipulate "
            "people into revealing information or performing actions. **Vishing** applies this via "
            "phone; **in-person** pretexting tests physical security and help desk procedures.\n\n"
            "Authorized exercises validate whether staff verify caller identity, challenge unknown "
            "visitors, and follow escalation procedures before resetting passwords or granting access."
        ),
        "exploitation": (
            "1. **ROE defines allowed pretexts**: no fake law enforcement, medical, or family emergencies unless approved.\n"
            "2. **Scenario design**: \"new vendor needing VPN access\", \"CEO urgent wire transfer\" (if in scope).\n"
            "3. **Vishing**: call help desk requesting password reset; test verification questions.\n"
            "4. **Physical**: tailgating, badge cloning tests, dropping USBs (if authorized).\n"
            "5. **Record outcomes**: who verified, who bypassed policy, time to escalation.\n"
            "6. **Blue team debrief**: share indicators without humiliating individuals.\n\n"
            "Never use obtained credentials beyond proof-of-concept in controlled validation."
        ),
        "defense": (
            "- **Help desk procedures**: out-of-band callback to registered numbers for resets.\n"
            "- Physical security: badge checks, mantrap entries, visitor escorts.\n"
            "- Security awareness including vishing and in-person social engineering.\n"
            "- Limit information on public phone directories and org charts.\n"
            "- Incident playbooks for suspected social engineering attempts.\n"
            "- Regular tabletop exercises combining digital and human attack vectors."
        ),
    },
    "iot/firmware-analysis": {
        "how_it_works": (
            "**IoT firmware** is the operating system and application stack on embedded devices—routers, "
            "cameras, industrial controllers. Firmware images may be downloaded from vendor sites, "
            "extracted via UART, or intercepted during OTA updates.\n\n"
            "Images often contain compressed root filesystems (squashfs, cramfs), kernel modules, "
            "default credentials, private keys, and unpatched open-source components. Many devices "
            "never receive updates after sale."
        ),
        "exploitation": (
            "1. **Acquire image**: vendor download, `binwalk -e firmware.bin`, or UART dump.\n"
            "2. **Extract filesystem**: identify and mount squashfs/cramfs contents.\n"
            "3. **Static analysis**: grep for `password`, `api_key`, hardcoded IPs, telnet enable flags.\n"
            "4. **Binary analysis**: Ghidra on `httpd`, `upnp`, and management daemons.\n"
            "5. **Emulation**: Firmadyne/QEMU to run services and fuzz network interfaces.\n"
            "6. **CVE mapping**: match embedded OpenSSL, busybox versions to known vulnerabilities.\n\n"
            "Test only on devices you own; IoT botnets harm real users."
        ),
        "defense": (
            "- **Signed firmware** with verified boot chains; reject unsigned updates.\n"
            "- No default credentials; force unique passwords or certificate-based provisioning.\n"
            "- Minimize attack surface: disable telnet, close unused ports, remove debug binaries from release.\n"
            "- Automated **firmware SBOM** and CVE monitoring for embedded components.\n"
            "- Secure OTA with encrypted, authenticated update channels.\n"
            "- Bug bounty or coordinated disclosure program for hardware products."
        ),
    },
    "iot/hardware-interfaces": {
        "how_it_works": (
            "Embedded devices expose **hardware debug interfaces**—UART, JTAG, SWD, SPI, I2C—that "
            "provide direct memory access, firmware download, and breakpoint debugging when "
            "physically connected. Manufacturers sometimes leave pads unpopulated or protect with "
            "fuses, but many consumer devices expose full shells over UART.\n\n"
            "Logic analyzers identify pin functions by observing boot traffic. **Bus Pirate** and "
            "**JTAGulator** automate pin discovery. Physical access defeats many software-only protections."
        ),
        "exploitation": (
            "1. **PCB inspection**: locate test pads, silkscreen labels (TX, RX, GND, TDI, TDO).\n"
            "2. **UART**: logic analyzer at 115200/8N1 common baud rates; connect GND, TX, RX.\n"
            "3. **Shell access**: interrupt boot via UART for u-boot prompt; dump flash.\n"
            "4. **JTAG**: JTAGulator scan; OpenOCD for memory read and boundary scan.\n"
            "5. **SPI flash**: desolder or clip SOIC8 reader to extract full firmware offline.\n"
            "6. **Safety**: ESD precautions, correct voltage levels (3.3V vs 1.8V).\n\n"
            "Document pinout for responsible disclosure; do not publish keys that enable mass compromise."
        ),
        "defense": (
            "- **Disable JTAG/UART** in production via fuses or firmware locks after manufacturing.\n"
            "- Encrypt flash contents; bind decryption to secure element or TPM.\n"
            "- Physical tamper detection and enclosure hardening for high-security devices.\n"
            "- Separate manufacturing debug credentials from field firmware.\n"
            "- Pen-test hardware before launch with physical access assumptions.\n"
            "- Provide secure update path so UART is not the only recovery mechanism."
        ),
    },
    "web3/smart-contracts": {
        "how_it_works": (
            "**Smart contracts** are immutable (or upgradeable) programs on blockchains—primarily "
            "EVM (Solidity) and Solana (Rust). They hold tokens, enforce DeFi logic, and govern DAOs. "
            "Bugs cause direct financial loss with no recourse: reentrancy, integer overflow (pre-0.8), "
            "access control failures, oracle manipulation, and flash loan attacks.\n\n"
            "Contracts interact via external calls; composability means vulnerabilities chain across protocols."
        ),
        "exploitation": (
            "1. **Static analysis**: Slither, Mythril for reentrancy, unchecked sends, tx.origin auth.\n"
            "2. **Manual review**: trace `call`/`delegatecall`, modifier coverage, initialization functions.\n"
            "3. **Fuzzing**: Echidna property tests (`echidna-test`) for invariant violations.\n"
            "4. **Foundry/Hardhat tests**: fork mainnet state; simulate attacks with flash loans.\n"
            "5. **Oracle checks**: spot price from single DEX pool vs Chainlink aggregators.\n"
            "6. **Upgradeability**: proxy admin keys, uninitialized implementation contracts.\n\n"
            "Report via Immunefi or protocol bug bounty; never exploit mainnet without authorization."
        ),
        "defense": (
            "- Follow **checks-effects-interactions**; use ReentrancyGuard on external calls.\n"
            "- Use Solidity 0.8+ built-in overflow checks; explicit casting with care.\n"
            "- **Least privilege**: Ownable/AccessControl on every sensitive function.\n"
            "- Multi-sig and timelocks for admin operations; monitor with Forta/Tenderly.\n"
            "- Use audited libraries (OpenZeppelin); minimize custom low-level assembly.\n"
            "- Independent audits, bug bounties, and gradual rollout with TVL caps."
        ),
    },
    "web3/wallet-dapp": {
        "how_it_works": (
            "**Wallets** (MetaMask, Rabby, hardware wallets) sign transactions and messages. "
            "**dApp frontends** request signatures via `eth_sendTransaction` or `personal_sign`. "
            "Users often approve malicious **token approvals**, **permit signatures**, or "
            "transactions to attacker contracts without reading hex calldata.\n\n"
            "Frontend compromises (DNS hijack, CDN supply chain) replace contract addresses. "
            "Phishing sites mimic legitimate dApps with infinite approval prompts."
        ),
        "exploitation": (
            "1. **Review signing UX**: does the wallet show decoded function names and spender addresses?\n"
            "2. **Approval audit**: check `approve`/`permit` for unlimited allowances to unknown contracts.\n"
            "3. **Frontend review**: CSP, SRI on scripts, wallet connect domain binding.\n"
            "4. **Chain ID**: test if dApp validates chainId prevents cross-chain replay confusion.\n"
            "5. **Address poisoning**: verify UI highlights matching characters in recipient addresses.\n"
            "6. **Simulate**: Tenderly or wallet dev mode to preview transaction effects before sign.\n\n"
            "Bug bounty focus: phishing via dApp UI, not unauthorized mainnet theft."
        ),
        "defense": (
            "- Display **human-readable** transaction previews; warn on unlimited approvals.\n"
            "- Hardcode or allowlist contract addresses; verify on multiple channels.\n"
            "- Strong **CSP**, Subresource Integrity, and integrity monitoring on frontend hosting.\n"
            "- Educate users on approval hygiene; integrate revoke.cash-style tooling.\n"
            "- Wallet vendors: clear signing screens, domain binding in EIP-712 messages.\n"
            "- Monitor deployed frontend hashes; alert on deploy changes."
        ),
    },
    "forensics/disk-memory": {
        "how_it_works": (
            "**Disk forensics** analyzes filesystem images acquired with write blockers to recover "
            "deleted files, registry hives, browser history, and malware persistence. **Memory forensics** "
            "examines RAM dumps for running processes, network connections, injected code, and "
            "credentials not present on disk.\n\n"
            "Timestamps (MFT, USN journal, prefetch) build activity timelines. Volatility/Rekall "
            "parse kernel structures to extract artifacts without booting the suspect system."
        ),
        "exploitation": (
            "1. **Acquire**: FTK Imager or `dd` with hardware write blocker; document hashes.\n"
            "2. **Mount safely**: read-only loop mount or forensic suites (Autopsy, Arsenal Image Mounter).\n"
            "3. **Parse artifacts**: MFT entries, `$LogFile`, registry `Run` keys, Shimcache.\n"
            "4. **Memory dump**: WinPMEM, LiME on Linux; capture before power-off when possible.\n"
            "5. **Volatility**: `windows.pslist`, `windows.malfind`, `windows.netscan` for IoCs.\n"
            "6. **Timeline**: Plaso/log2timeline to correlate file, registry, and event log activity.\n\n"
            "Maintain chain of custody documentation for legal admissibility."
        ),
        "defense": (
            "- Enable **centralized logging** and EDR memory scanning for live response.\n"
            "- Full disk encryption with secure key management; TPM binding.\n"
            "- Restrict physical access; secure boot and measured boot where applicable.\n"
            "- Regular forensic readiness drills; pre-approved acquisition playbooks.\n"
            "- Retain logs and images per policy; immutable WORM storage for evidence.\n"
            "- Train IR team on proper acquisition to avoid spoliation."
        ),
    },
    "forensics/network": {
        "how_it_works": (
            "**Network forensics** reconstructs incidents from PCAP files, firewall logs, proxy logs, "
            "DNS queries, and NetFlow. Analysts extract C2 channels, exfiltration volumes, lateral "
            "movement paths, and malware downloads embedded in HTTP/SMTP traffic.\n\n"
            "Encrypted traffic limits payload visibility; metadata (SNI, JA3, timing, volumes) still "
            "supports detection. SSL decryption in enterprise proxies enables deeper inspection where lawful."
        ),
        "exploitation": (
            "1. **Collect PCAP**: span ports, Zeek logs, or full packet capture during incidents.\n"
            "2. **Wireshark**: filter `http`, `dns`, `tls.handshake`; export objects from HTTP.\n"
            "3. **Zeek/Suricata**: generate structured logs for long-term retention vs raw PCAP size.\n"
            "4. **Session rebuild**: NetworkMiner or `tcpflow` for file extraction.\n"
            "5. **Timeline**: correlate firewall deny/allow with endpoint telemetry.\n"
            "6. **C2 identification**: beaconing intervals, rare JA3 fingerprints, DGA domains.\n\n"
            "Document IoCs: IPs, domains, URIs, user-agents, certificate serials."
        ),
        "defense": (
            "- **Retain logs** with sufficient TTL for investigation (90+ days minimum for many threats).\n"
            "- Deploy Zeek/Suricata at network boundaries and critical VLANs.\n"
            "- Enable DNS logging; block known malicious resolvers at egress.\n"
            "- Network segmentation limits PCAP scope during lateral movement.\n"
            "- TLS inspection on corporate proxies with privacy policy compliance.\n"
            "- Regular PCAP exercises in IR tabletop scenarios."
        ),
    },
    "forensics/cloud": {
        "how_it_works": (
            "**Cloud forensics** investigates incidents in AWS, Azure, and GCP where attackers lack "
            "physical access but abuse IAM, APIs, and misconfigurations. Evidence lives in **audit logs** "
            "(CloudTrail, Azure Activity Log, GCP Audit Logs), flow logs, snapshot APIs, and SaaS integrations.\n\n"
            "Multi-region deployments, ephemeral instances, and shared responsibility models complicate "
            "acquisition. Logs may be disabled, encrypted, or in attacker-controlled accounts."
        ),
        "exploitation": (
            "1. **Preserve logs**: export CloudTrail to immutable S3; enable organization trail.\n"
            "2. **Snapshot volumes**: EBS/Azure disk snapshots for offline disk forensics.\n"
            "3. **Memory**: SSM Run Command or vendor-specific memory capture where supported.\n"
            "4. **IAM trace**: session issuer, `AssumeRole` chains, access key creation events.\n"
            "5. **Network**: VPC Flow Logs, GuardDuty findings, WAF logs.\n"
            "6. **Cross-account**: identify role trust policies abused for pivot.\n\n"
            "Use dedicated forensics account with read-only roles; avoid modifying evidence in-place."
        ),
        "defense": (
            "- **Organization-wide audit logging** with log file validation and MFA delete on buckets.\n"
            "- Central SIEM ingestion for all cloud audit and flow logs.\n"
            "- Restrict IAM ability to disable logging or delete trails (SCPs).\n"
            "- Automated snapshots and **Velociraptor/osquery** on cloud workloads.\n"
            "- Incident response runbooks specific to cloud API abuse.\n"
            "- Regular purple-team exercises simulating credential theft in cloud consoles."
        ),
    },
    "secure-code-review/sast": {
        "how_it_works": (
            "**SAST** (Static Application Security Testing) analyzes source or bytecode without execution "
            "to find patterns matching vulnerabilities—SQL injection sinks, XSS, hardcoded secrets, "
            "weak crypto. Tools include Semgrep, CodeQL, SonarQube, and language-specific analyzers.\n\n"
            "SAST produces high false-positive rates; **manual code review** traces data flow from "
            "sources (HTTP params) to sinks (SQL queries, shell exec) and validates authorization on "
            "every sensitive operation."
        ),
        "exploitation": (
            "1. **Run SAST in CI**: Semgrep with OWASP rulesets, CodeQL `security-extended`.\n"
            "2. **Triage**: prioritize findings in auth, payment, admin, and file upload modules.\n"
            "3. **Data flow**: manually trace untrusted input to dangerous functions.\n"
            "4. **Authz review**: for each endpoint, verify object-level checks on IDs from user input.\n"
            "5. **Business logic**: race conditions, state machine bypasses SAST cannot see.\n"
            "6. **Confirm**: dynamic test (Burp) on suspected lines to validate exploitability.\n\n"
            "Integrate SARIF output into PR comments for developer-friendly remediation."
        ),
        "defense": (
            "- **Shift-left**: mandatory SAST on every PR with blocking rules for critical patterns.\n"
            "- Customize rules for framework-specific pitfalls (Django ORM, Spring Security).\n"
            "- Pair SAST with **DAST** and dependency scanning for defense in depth.\n"
            "- Security champions review high-risk modules quarterly.\n"
            "- Track mean time to remediate SAST findings by severity.\n"
            "- Follow OWASP Code Review Guide checklists for manual coverage gaps."
        ),
    },
    "secure-code-review/threat-modeling": {
        "how_it_works": (
            "**Threat modeling** systematically identifies threats to a system using structured "
            "approaches—**STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, "
            "Denial of Service, Elevation of Privilege), **PASTA**, or **Attack Trees**.\n\n"
            "Practitioners diagram **data flow diagrams** with trust boundaries, enumerate threats per "
            "component, rank risk, and define mitigations and test cases. Threat models should update "
            "when architecture changes—not a one-time paperwork exercise."
        ),
        "exploitation": (
            "1. **Scope the system**: define assets, actors, entry points, and dependencies.\n"
            "2. **Draw DFD**: processes, data stores, external entities, trust boundaries.\n"
            "3. **Apply STRIDE**: per element, ask what spoofing/tampering/etc. is possible.\n"
            "4. **Prioritize**: likelihood × impact; focus pentest on highest-ranked threats.\n"
            "5. **Derive test cases**: each threat maps to security requirements and validation steps.\n"
            "6. **Tools**: OWASP Threat Dragon, Microsoft Threat Modeling Tool for structured output.\n\n"
            "Use threat models to guide bug bounty scope and internal red team objectives."
        ),
        "defense": (
            "- Integrate threat modeling into **design reviews** before major features ship.\n"
            "- Store models in version control; diff on architecture changes.\n"
            "- Link threats to **Jira security tasks** and verification tests in CI.\n"
            "- Train developers on STRIDE with hands-on workshops on their actual services.\n"
            "- Revisit models after incidents and pen test findings.\n"
            "- Align mitigations with OWASP ASVS levels appropriate to application risk tier."
        ),
    },
}
