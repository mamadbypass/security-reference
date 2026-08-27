# Pretexting & Vishing

Phone and in-person social engineering with strict authorization.

## How It Works

**Pretexting** builds a fabricated scenario (IT support, vendor, auditor) to manipulate people into revealing information or performing actions. **Vishing** applies this via phone; **in-person** pretexting tests physical security and help desk procedures.

Authorized exercises validate whether staff verify caller identity, challenge unknown visitors, and follow escalation procedures before resetting passwords or granting access.

## Exploitation

1. **ROE defines allowed pretexts**: no fake law enforcement, medical, or family emergencies unless approved.
2. **Scenario design**: "new vendor needing VPN access", "CEO urgent wire transfer" (if in scope).
3. **Vishing**: call help desk requesting password reset; test verification questions.
4. **Physical**: tailgating, badge cloning tests, dropping USBs (if authorized).
5. **Record outcomes**: who verified, who bypassed policy, time to escalation.
6. **Blue team debrief**: share indicators without humiliating individuals.

Never use obtained credentials beyond proof-of-concept in controlled validation.

## Defense & Mitigation

- **Help desk procedures**: out-of-band callback to registered numbers for resets.
- Physical security: badge checks, mantrap entries, visitor escorts.
- Security awareness including vishing and in-person social engineering.
- Limit information on public phone directories and org charts.
- Incident playbooks for suspected social engineering attempts.
- Regular tabletop exercises combining digital and human attack vectors.

## Methodology

- [ ] Define allowed pretexts in ROE
- [ ] Record outcomes without harming staff
- [ ] Test help desk verification procedures
- [ ] Debrief with blue team after exercise

## Tools

| Tool | Usage |
|------|-------|
| `custom scripts` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
