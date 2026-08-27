# Business Logic Flaws

Abuse application workflows beyond technical vulnerabilities.

## How It Works

Business logic flaws violate application rules and workflow assumptions rather than breaking technical controls. The code executes "correctly" from a programmer's view but allows abuse of intended process.

Examples:

- Purchasing items for negative prices or zero totals via cart manipulation
- Applying stacked discounts beyond policy
- Skipping payment step by direct URL to confirmation page
- Voting or rating more than once by parameter tampering
- Tier downgrade not enforced when subscription expires
- Referral bonuses farmed with self-referrals

These bugs arise from incomplete threat modeling of multi-step flows, trusting client-side state, race windows between microservices, and missing server-side validation of prices, quantities, and roles.

Automated scanners rarely detect logic flaws; they require understanding domain rules and adversarial creativity.

## Exploitation

**Workflow mapping**

1. Document every step: browse → cart → coupon → payment → fulfillment.
2. Identify assumptions: "user already paid", "coupon applied once", "role checked on page load only".
3. Test skipping steps: jump to `/checkout/complete` without payment.

**Parameter tampering**

- Change `quantity=-1`, `price=0.01`, `currency=USD` → `currency=XXX`
- Swap `product_id` to higher-value SKU after price locked client-side
- Replay old promotional API calls after campaign ended

**Race conditions**

- Parallel coupon application (see race-condition topic)
- Simultaneous withdrawal requests exceeding balance

**Attack flow**

```
Attacker manipulates workflow state or parameters → server enforces incomplete rules → financial/governance impact without classic injection
```

**Authorization logic**

- Feature flags in JSON: `"isPremium": true` accepted from client
- Admin functions gated only by hidden URL

**Documentation for reports**

- Exact $ impact or policy violated
- Minimal reproduction with two accounts or single account steps

## Defense & Mitigation

**Server-side authority**

- All prices, discounts, inventory, and permissions computed server-side from authoritative DB state.
- Never trust hidden fields, client JSON, or previous step cookies for security decisions.

**Workflow enforcement**

- State machine tokens: each step issues signed token required for next step.
- Idempotent payment callbacks verified against gateway records.

**Validation rules**

- Business rule engine or centralized policy layer for promotions and limits.
- Negative quantity, zero price, and cross-product constraints rejected at API layer.

**Monitoring**

- Anomaly detection: sudden spike in coupon usage, negative orders, refund patterns.
- Audit logs for manual review of high-value transactions.

**Testing**

- Threat modeling per feature (STRIDE on purchase flow).
- Pair QA testers with security reviewers for "what if I try..." scenarios.

## Methodology

- [ ] Map purchase, refund, and privilege workflows
- [ ] Test negative quantities and price manipulation
- [ ] Bypass multi-step validations
- [ ] Check role transitions and feature gating

## Tools

| Tool | Usage |
|------|-------|
| `burp` | See [Tools Guide](/TOOLS_GUIDE/) |
| `manual testing` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [OWASP Business Logic](https://owasp.org/www-community/vulnerabilities/Business_logic_vulnerability)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
