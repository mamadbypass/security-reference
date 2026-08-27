from tips._base import t

API_AUTH_TIPS = {
    "api/graphql": [
        t("Introspection query", "POST `{\"query\": \"{ __schema { types { name } } }\"}` — disable in prod but often forgotten on staging."),
        t("Batch brute force", "Send 100 login mutations in one HTTP request to bypass rate limits."),
        t("Field-level auth", "Query other users' `email`, `ssn`, `balance` fields with victim IDs."),
        t("Alias DoS", "Deeply nested aliases can CPU-DoS — test cost limits responsibly."),
        t("clairvoyance recovery", "When introspection off: `clairvoyance -u URL -d wordlist.txt`"),
    ],
    "api/graphql/introspection": [
        t("GET introspection", "Some servers allow introspection via GET query param."),
        t("GraphiQL exposure", "/graphiql, /playground, /console — often have introspection on."),
        t("Staging only?", "Production may block introspection but staging.graphql.target.com may not."),
        t("Partial introspection", "Some fields hidden but mutations still listed — read carefully."),
        t("Save schema", "Export schema JSON for offline analysis and IDOR field hunting."),
    ],
    "api/graphql/batching": [
        t("Array of operations", "Wrap queries: `[{query: ...}, {query: ...}]` in single POST."),
        t("Alias duplication", "`{ a1: user(id:1){email} a2: user(id:2){email} ... }`"),
        t("Rate limit bypass", "Document requests-per-HTTP vs requests-per-operation difference."),
        t("OTP brute force", "Batch 10k OTP attempts if server counts HTTP not operations.", "warning"),
        t("Cost analysis", "Measure server time vs batch size for DoS report evidence."),
    ],
    "api/versioning": [
        t("Fuzz versions", "Try /v0/, /v1/, /v2/, /beta/, /internal/, /legacy/ on same base path."),
        t("Mobile app APIs", "Old API versions stay live for mobile clients years after deprecation."),
        t("Header versioning", "`Accept: application/vnd.api+json; version=1` vs version=2"),
        t("Diff auth between versions", "v1 may lack auth added in v2 — always test oldest version."),
        t("Changelog mining", "Read public API changelog for removed security controls."),
    ],
    "api/shadow-zombie-apis": [
        t("linkfinder on JS", "`python linkfinder.py -i https://target.com/app.js -o cli`"),
        t("wayback URLs", "Old API paths in Wayback Machine still respond on legacy servers."),
        t("APK strings", "`strings app.apk | grep -i api` finds hidden endpoints."),
        t("Swagger leaks", "/swagger.json, /openapi.json, /api-docs — unauthenticated docs."),
        t("404 vs 401", "Shadow APIs often return 401 not 404 — fuzz paths and watch auth differences."),
    ],
    "api/grpc-protobuf": [
        t("grpcurl list", "`grpcurl -plaintext host:50051 list` — reflection exposes all RPCs."),
        t("Burp gRPC", "Enable HTTP/2 in Burp and use gRPC tab for message editing."),
        t("Protobuf without proto", "Use `grpcurl describe` or blackbox protobuf decoding."),
        t("Metadata auth", "Test `authorization` metadata per RPC — not just at connection."),
        t("grpcui browser", "Web UI for manual RPC testing when CLI is awkward."),
    ],
    "authentication/jwt": [
        t("jwt_tool all tests", "`python3 jwt_tool.py TOKEN -M at` runs all attacks."),
        t("alg=none", "Set header `{\"alg\":\"none\"}` and remove signature — still works on bad libs."),
        t("HS/RS confusion", "Sign with public key as HMAC secret when server expects RS256."),
        t("kid injection", "`{\"kid\": \"../../dev/key\"}` or SQLi in kid field."),
        t("Check exp claim", "Many APIs ignore expiration — test expired tokens."),
    ],
    "authentication/password-reset": [
        t("Token in response", "Reset tokens sometimes returned in JSON body or URL referrer."),
        t("Host header poison", "Poison Host header in reset request — token link goes to attacker."),
        t("Parameter tamper", "Change `email` or `userId` in reset POST while using victim token."),
        t("Token entropy", "Request 10 tokens — check for sequential or short patterns."),
        t("Reuse after reset", "Old reset link may still work after password changed."),
    ],
    "authentication/sso-saml": [
        t("SAML Raider", "Burp extension for signing, wrapping, and comment injection."),
        t("Signature stripping", "Remove `<ds:Signature>` block — some SPs don't validate."),
        t("Comment injection", "XML comments inside Assertion to break signature coverage."),
        t("ACS URL swap", "Change AssertionConsumerServiceURL to attacker endpoint."),
        t("Replay assertions", "Save valid assertion and replay before NotOnOrAfter expires."),
    ],
    "authentication/passwordless": [
        t("Magic link leakage", "Check Referer header leaks token to third-party resources."),
        t("OTP rate limits", "Test 6-digit OTP — 1M combos need rate limit or lockout."),
        t("Same link twice", "Magic links should be single-use — test double redemption."),
        t("WebAuthn challenge", "Replay old challenge/response if server doesn't store nonce."),
        t("Email pre-account", "Request magic link for unregistered email — user enumeration."),
    ],
}
