# Information Disclosure

Find sensitive data exposed through errors, backups, and misconfigurations.

## Methodology

- [ ] Trigger verbose error messages
- [ ] Check /.git, /.env, backup files
- [ ] Review API responses for excessive data
- [ ] Search JS bundles for secrets and endpoints

## Tools

- `trufflehog`
- `gitleaks`
- `nuclei`
- `linkfinder`

## Resources

- [OWASP Information Exposure](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/05-Testing_for_Information_Disclosure)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
