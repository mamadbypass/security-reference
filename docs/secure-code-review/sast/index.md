# SAST & Manual Code Review

Combine static analysis with manual review for vulnerability discovery.

## Methodology

- [ ] Run SAST tools on repositories
- [ ] Triage false positives manually
- [ ] Trace data flow for high-risk sinks
- [ ] Review authz checks on sensitive operations

## Tools

- `semgrep`
- `codeql`
- `sonarqube`

## Resources

- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
