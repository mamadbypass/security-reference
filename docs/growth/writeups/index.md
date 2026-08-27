# Writeups & Reputation

Publish quality writeups to build bug bounty reputation.

## How It Works

**Security writeups** document how a vulnerability was found and exploited, building researcher reputation, educating the community, and demonstrating methodology to employers and program triagers.

Quality writeups explain root cause—not just the payload—and show unique techniques. Platforms like HackerOne Hacktivity, Infosec Writeups, and personal blogs serve as portfolio pieces. Poor writeups leak customer data or violate disclosure agreements.

## Exploitation

1. **Document during testing**: save requests, notes, and timestamps as you work.
2. **Structure**: summary, background, discovery, exploitation, impact, remediation, timeline.
3. **Teach**: explain why the bug exists, not only how to trigger it.
4. **Redact**: replace real domains, user emails, and tokens with placeholders.
5. **Respect disclosure**: wait for fix or program permission before publishing.
6. **Cross-post**: blog + Hacktivity + Twitter thread with link to full analysis.
7. **Engage**: respond to comments; correct errors; credit collaborators.

Unique writeups on novel attack classes attract program invites and conference talks.

## Defense & Mitigation

- Organizations should **welcome responsible writeups** after fixes ship.
- Provide researchers clear disclosure policies and safe harbor statements.
- Use public writeups as free QA—review for missed variants in your codebase.
- Encourage internal engineers to publish defensive perspectives and patch deep-dives.
- Monitor Hacktivity for reports against your products even outside formal programs.
- Build a culture where findings lead to systemic fixes, not just one-line patches.

## Methodology

- [ ] Document unique techniques and root cause
- [ ] Redact sensitive customer data
- [ ] Cross-post to blog and HackerOne Hacktivity
- [ ] Engage responsibly with the community

## Tools

| Tool | Usage |
|------|-------|
| `markdown` | [Write reports in Markdown for GitHub/HackerOne](../../TOOLS_GUIDE.md) |
| `obsidian` | [Personal knowledge base for writeups & notes](../../TOOLS_GUIDE.md) |

## Resources

- [Infosec Writeups](https://infosecwriteups.com/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
