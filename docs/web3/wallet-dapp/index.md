# Wallet & dApp Security

Test wallet connectors and decentralized application frontends.

## How It Works

**Wallets** (MetaMask, Rabby, hardware wallets) sign transactions and messages. **dApp frontends** request signatures via `eth_sendTransaction` or `personal_sign`. Users often approve malicious **token approvals**, **permit signatures**, or transactions to attacker contracts without reading hex calldata.

Frontend compromises (DNS hijack, CDN supply chain) replace contract addresses. Phishing sites mimic legitimate dApps with infinite approval prompts.

## Exploitation

1. **Review signing UX**: does the wallet show decoded function names and spender addresses?
2. **Approval audit**: check `approve`/`permit` for unlimited allowances to unknown contracts.
3. **Frontend review**: CSP, SRI on scripts, wallet connect domain binding.
4. **Chain ID**: test if dApp validates chainId prevents cross-chain replay confusion.
5. **Address poisoning**: verify UI highlights matching characters in recipient addresses.
6. **Simulate**: Tenderly or wallet dev mode to preview transaction effects before sign.

Bug bounty focus: phishing via dApp UI, not unauthorized mainnet theft.

## Defense & Mitigation

- Display **human-readable** transaction previews; warn on unlimited approvals.
- Hardcode or allowlist contract addresses; verify on multiple channels.
- Strong **CSP**, Subresource Integrity, and integrity monitoring on frontend hosting.
- Educate users on approval hygiene; integrate revoke.cash-style tooling.
- Wallet vendors: clear signing screens, domain binding in EIP-712 messages.
- Monitor deployed frontend hashes; alert on deploy changes.

## Methodology

- [ ] Review transaction signing flows
- [ ] Test for phishing via malicious approvals
- [ ] Check frontend integrity and CSP
- [ ] Validate chain ID and contract address display

## Tools

| Tool | Usage |
|------|-------|
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |
| `wallet simulators` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
