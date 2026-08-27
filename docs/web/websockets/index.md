# WebSockets Security

Test real-time channels for auth bypass and injection.

## Methodology

- [ ] Capture WebSocket handshake and messages
- [ ] Test origin validation on the handshake
- [ ] Fuzz message types for injection
- [ ] Check authorization per channel or room

## Tools

- `burp`
- `ws-harness`
- `owasp zap`

## Resources

- [PortSwigger WebSockets](https://portswigger.net/web-security/websockets)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
