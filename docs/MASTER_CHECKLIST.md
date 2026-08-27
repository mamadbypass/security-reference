# Master Checklist

End-to-end penetration testing and bug bounty engagement checklist. Use this as a starting point and adapt to program scope.

## Pre-Engagement

- [ ] Obtain written authorization and define scope
- [ ] Review program rules (HackerOne, Bugcrowd, Intigriti, private)
- [ ] Set up isolated testing environment and VPN if required
- [ ] Configure Burp Suite / proxy tooling
- [ ] Create asset tracking spreadsheet or note vault
- [ ] Document out-of-scope items and testing windows

## Reconnaissance

- [ ] Passive subdomain enumeration (CT logs, archives)
- [ ] Active subdomain brute force
- [ ] DNS record enumeration (A, AAAA, CNAME, MX, TXT, NS)
- [ ] ASN and IP range mapping
- [ ] Port scanning on live hosts
- [ ] HTTP probing and technology fingerprinting
- [ ] JavaScript file analysis for endpoints
- [ ] Wayback machine and GAU URL collection
- [ ] Identify staging, dev, and legacy environments
- [ ] Map third-party integrations and CDNs

## Web Application Testing

- [ ] Map application functionality and user roles
- [ ] Test authentication (brute force, lockout, MFA bypass)
- [ ] Test authorization (IDOR, privilege escalation)
- [ ] SQL injection (error, boolean, time-based, UNION)
- [ ] Cross-site scripting (reflected, stored, DOM)
- [ ] SSRF on URL import and webhook features
- [ ] File upload restrictions and path traversal
- [ ] LFI / RFI on file parameters
- [ ] XXE on XML parsers
- [ ] Insecure deserialization
- [ ] SSTI in template engines
- [ ] Open redirect parameters
- [ ] CORS misconfiguration
- [ ] Clickjacking on sensitive actions
- [ ] HTTP request smuggling
- [ ] Web cache poisoning
- [ ] CRLF injection
- [ ] Command injection
- [ ] NoSQL injection
- [ ] HTTP parameter pollution
- [ ] WebSocket authorization
- [ ] Business logic flaws (pricing, coupons, workflows)
- [ ] Race conditions on limits and tokens
- [ ] Prototype pollution / DOM clobbering
- [ ] Information disclosure (errors, backups, .git)
- [ ] Security headers (CSP, HSTS, X-Frame-Options)

## API Testing

- [ ] Discover API documentation (Swagger, OpenAPI, GraphQL)
- [ ] GraphQL introspection and batching
- [ ] Test deprecated API versions
- [ ] Shadow / zombie API endpoints from JS
- [ ] Rate limiting and auth on all methods
- [ ] Mass assignment vulnerabilities
- [ ] gRPC reflection and method fuzzing

## Authentication & Session

- [ ] JWT algorithm confusion and weak secrets
- [ ] Password reset token predictability
- [ ] Host header poisoning on reset links
- [ ] OAuth redirect URI validation
- [ ] SAML signature wrapping
- [ ] Session fixation and invalidation
- [ ] OTP / magic link brute force
- [ ] WebAuthn challenge binding

## Mobile Application Testing

- [ ] Static analysis of APK / IPA
- [ ] Hardcoded secrets and API keys
- [ ] SSL pinning bypass
- [ ] Deep link and intent filter testing
- [ ] Exported component exposure
- [ ] Frida runtime instrumentation
- [ ] Root / jailbreak detection bypass

## Cloud & Infrastructure

- [ ] S3 / blob storage public access
- [ ] IAM privilege escalation paths
- [ ] Security group and firewall rules
- [ ] Metadata service access (SSRF chains)
- [ ] Kubernetes RBAC and privileged pods
- [ ] Container image vulnerability scanning
- [ ] Terraform / IaC misconfigurations
- [ ] CI/CD pipeline secret exposure

## Network & Active Directory

- [ ] Internal network segmentation validation
- [ ] SMB, RDP, WinRM enumeration
- [ ] LLMNR / NBT-NS poisoning (authorized)
- [ ] Kerberoasting and AS-REP roasting
- [ ] BloodHound attack path analysis
- [ ] Local privilege escalation (Windows / Linux)
- [ ] Lateral movement with harvested creds
- [ ] DCSync and golden ticket (lab / authorized)

## Blue Team Validation

- [ ] Verify detections for tested techniques
- [ ] Review SIEM alert coverage
- [ ] Test incident response playbooks
- [ ] Validate log retention and integrity

## Cryptography & Transport

- [ ] TLS version and cipher suite review
- [ ] Certificate validation and pinning
- [ ] Weak random number generation
- [ ] Padding oracle conditions
- [ ] Hardcoded encryption keys

## Binary & Specialized

- [ ] Firmware extraction and analysis (IoT)
- [ ] Smart contract reentrancy and access control
- [ ] Stack / heap overflow in lab binaries
- [ ] OSINT on people and organization (legal scope)

## Post-Testing

- [ ] Remove all testing accounts and artifacts
- [ ] Document findings with reproducible steps
- [ ] Rate severity using CVSS or program matrix
- [ ] Provide remediation recommendations
- [ ] Submit reports through proper channels
- [ ] Retest fixes when available

## Reporting Quality

- [ ] Clear title and affected asset
- [ ] Step-by-step reproduction
- [ ] Impact statement for the business
- [ ] Proof-of-concept (minimal, safe)
- [ ] Suggested fix with references

---

**Total items:** 100+ core checks across all domains. Expand per engagement type.
