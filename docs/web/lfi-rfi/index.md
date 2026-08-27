# LFI / RFI

Local and remote file inclusion testing.

## Methodology

- [ ] Identify file/path parameters
- [ ] Test path traversal sequences
- [ ] Attempt log poisoning and PHP wrappers
- [ ] Check for RFI via remote URL inclusion

## Tools

- `ffuf`
- `burp`
- `lfi-suite`

## Resources

- [PayloadsAllTheThings LFI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion)
- [PortSwigger File Path Traversal](https://portswigger.net/web-security/file-path-traversal)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
