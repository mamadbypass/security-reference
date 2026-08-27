# Shadow & Zombie APIs

Uncover undocumented and forgotten API endpoints.

## How It Works

**Shadow APIs** are undocumented endpoints—microservices, serverless functions, admin panels, or feature branches reachable in production but absent from official docs. **Zombie APIs** are formerly documented services that should have been retired but still accept traffic (old load balancer rules, forgotten containers, or DNS to decommissioned environments that were cloned).

They often lack WAF coverage, OAuth scopes, audit logging, and patch cadence. Discovery vectors include JavaScript bundles, mobile apps, proxy logs, certificate transparency, cloud API gateways, and leaked OpenAPI files in `.git` or S3 buckets.

## Exploitation

1. **Mine client-side code** — Run `LinkFinder`, `katana`, and `nuclei` on JS bundles for `/api/`, `/internal/`, GraphQL, and WebSocket URLs.
2. **Intercept mobile traffic** — Proxy iOS/Android apps to find alternate base URLs and hidden REST/gRPC backends.
3. **Scan for spec leaks** — Probe `/swagger.json`, `/openapi.yaml`, `/api-docs`, `/redoc`, and `/.well-known/` paths.
4. **Review infrastructure** — Cloud API Gateway stages, Lambda function URLs, and Kubernetes ingress rules may expose services engineers forgot.
5. **Use historical data** — `gau`, Wayback Machine, and breach dumps for old subdomains and paths.
6. **Diff deployments** — Compare responses before/after releases; new routes sometimes appear without documentation.
7. **Test without auth** — Shadow endpoints frequently ship before auth middleware is wired up.
8. **Chain findings** — A zombie admin API on `staging-api.example.com` may share production credentials.

## Defense & Mitigation

- **Central API gateway** with mandatory auth, logging, and schema registration for all public traffic.
- **Automated asset inventory** tied to CI/CD—block deploy if routes are not registered.
- **Decommission runbooks**: remove DNS, certs, LB rules, and cloud resources together; verify with external scans.
- **Restrict internal hostnames** to private networks; never reuse production secrets on shadow environments.
- **Scan repositories and buckets** for OpenAPI leaks; rotate any exposed keys.
- **Continuous external attack surface monitoring** (EASM) to detect unknown endpoints early.

## Methodology

- [ ] Mine JavaScript for API routes
- [ ] Review mobile app traffic and Swagger leaks
- [ ] Scan for /swagger, /openapi.json, /graphql
- [ ] Diff API behavior after deployments

## Tools

| Tool | Usage |
|------|-------|
| `linkfinder` | See [Tools Guide](/TOOLS_GUIDE/) |
| `katana` | See [Tools Guide](/TOOLS_GUIDE/) |
| `nuclei` | See [Tools Guide](/TOOLS_GUIDE/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
