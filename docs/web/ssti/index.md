# Server-Side Template Injection (SSTI)

Inject template syntax for code execution.

## Methodology

- [ ] Detect template engine with polyglot probes
- [ ] Escalate to read files or execute commands
- [ ] Test blind SSTI via out-of-band channels
- [ ] Identify sandbox escapes per engine

## Tools

- `tplmap`
- `burp`

## Resources

- [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
