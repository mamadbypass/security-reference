# Insecure Deserialization

Exploit unsafe object deserialization in web applications.

## Methodology

- [ ] Identify serialized object formats (Java, PHP, .NET, Python)
- [ ] Use known gadget chains for the stack
- [ ] Test tampered cookies and API bodies
- [ ] Validate impact with safe proof-of-concept payloads

## Tools

- `ysoserial`
- `phpggc`
- `burp`

## Resources

- [OWASP Deserialization](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/16-Testing_for_HTTP_Insecure_Deserialization)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
