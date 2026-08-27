# GraphQL Introspection

Enumerate schema when introspection is enabled.

## How It Works

GraphQL introspection is a built-in meta-query capability defined in the GraphQL specification. Clients can query special fields `__schema` and `__type` to discover all types, fields, arguments, enums, interfaces, and directives the server supports. A standard introspection query recursively walks `queryType`, `mutationType`, and `subscriptionType`, exporting names like `adminDeleteUser`, `internalApiKey`, or `ssn` that were never documented publicly.

Introspection is invaluable during development but dangerous when exposed to attackers: it turns black-box API testing into full schema-driven fuzzing. Some frameworks disable it by default in production; others require explicit configuration. WAF rules that block the word `__schema` are brittle—attackers can use fragments, whitespace tricks, or pre-built schema files from CI leaks.

## Exploitation

1. **Send the standard introspection query** — Use Burp, `curl`, or `graphql-cli` with the full `IntrospectionQuery` payload against `/graphql`.
2. **Try variants if blocked** — Alternate HTTP methods (GET with `query` param), different `Content-Type` values, or POST to `/graphql?query=` endpoints used by some CDNs.
3. **Check staging and old hosts** — Staging, preview, and legacy subdomains often leave introspection enabled while production disables it.
4. **Use blind schema recovery** — If introspection is disabled, tools like `clairvoyance` infer the schema from error messages (`Cannot query field "foo" on type "Query"`).
5. **Prioritize high-value types** — Search exported SDL for `Mutation` names containing `admin`, `internal`, `delete`, `export`, `impersonate`, `password`.
6. **Cross-reference with auth** — For each discovered mutation, test without tokens, with expired tokens, and across user roles.
7. **Export for automation** — Feed the schema into `graphql-voyager`, custom fuzzers, or InQL to systematically test every field.

## Defense & Mitigation

- **Turn off introspection in production** via server config (Apollo: `introspection: false`; Hasura: disable from console settings).
- **Never rely on WAF keyword blocking alone**; enforce at the GraphQL execution layer.
- **Restrict schema access** to CI, schema registry, and internal VPN if developers need SDL at runtime.
- **Return generic errors** in production to hinder clairvoyance-style inference.
- **Audit deployments** so preview environments are not publicly routable without auth.
- **Monitor for `__schema` and `__type` in request bodies** and alert on spikes.

## Methodology

- [ ] Send __schema and __type queries
- [ ] Export schema for hidden mutations
- [ ] Check introspection on staging endpoints
- [ ] Review sensitive fields and admin mutations

## Tools

| Tool | Usage |
|------|-------|
| `clairvoyance` | See [Tools Guide](/TOOLS_GUIDE/) |
| `graphql-cop` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
