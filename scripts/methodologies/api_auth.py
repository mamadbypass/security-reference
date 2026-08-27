from methodologies._base import REPORT, SCOPE, phases

API_AUTH_METHODOLOGIES = {
    "api/graphql": phases(
        SCOPE + ["Obtain GraphQL endpoint and test credentials for each role"],
        ["Run introspection query or clairvoyance if disabled", "Map types, queries, mutations, and subscriptions", "Identify sensitive fields (PII, admin, payment)", "Review batching and alias abuse potential"],
        ["Test field-level auth on every mutation", "Replay operations as unauthenticated and low-priv user", "Fuzz variables for injection and IDOR", "Test depth/complexity limits for DoS"],
        ["Extract unauthorized data via IDOR or introspection", "Demonstrate batching brute-force if applicable", "Show cost/DoS impact with measured query complexity"],
        REPORT + ["Recommend disabling introspection in prod and field-level auth"],
    ),
    "api/graphql/introspection": phases(
        SCOPE + ["Locate GraphQL endpoint URLs"],
        ["Send `__schema` and `__type` introspection queries", "Try clairvoyance wordlist recovery if blocked", "Check GET vs POST introspection", "Review GraphiQL/Playground exposure"],
        ["Validate full schema download", "Identify hidden admin mutations", "Compare introspection across environments", "Test introspection with auth vs without"],
        ["Document sensitive types discovered via schema", "Map unauthorized mutations for further testing", "Do not exfiltrate production user data"],
        REPORT,
    ),
    "api/graphql/batching": phases(
        SCOPE + ["Confirm rate limits on GraphQL endpoint"],
        ["Send array of queries in single HTTP request", "Test alias-based field duplication", "Measure server response time vs query count", "Identify auth checks per sub-query"],
        ["Bypass rate limits with 100+ batched login attempts", "Brute force OTP or coupon codes via batching", "Demonstrate DoS with expensive nested queries", "Compare single vs batch request outcomes"],
        ["Show account enumeration or 2FA bypass via batch", "Document rate limit bypass with request counts", "Recommend query cost analysis"],
        REPORT,
    ),
    "api/versioning": phases(
        SCOPE + ["Discover API versions: /v1/, /v2/, headers, Accept types"],
        ["Fuzz version numbers and deprecated paths", "Compare auth between old and new versions", "Find debug endpoints only in old versions", "Review changelog and mobile app for legacy APIs"],
        ["Access v1 endpoints with weaker auth from v2", "Test removed IDOR fixes still present in v1", "Validate shadow APIs in mobile binaries", "Document version sunset policy gaps"],
        ["Demonstrate bypass of v2 security via v1", "Show data access only possible on deprecated API", "Recommend version deprecation and uniform auth"],
        REPORT,
    ),
    "api/shadow-zombie-apis": phases(
        SCOPE + ["Collect JS bundles, mobile apps, and old documentation"],
        ["Run linkfinder and katana on all web assets", "Extract API paths from APK/IPA strings", "Search Swagger/OpenAPI leaks and Postman collections", "Review GitHub for exposed API specs"],
        ["Probe discovered endpoints for responses", "Compare auth on shadow vs documented APIs", "Test zombie endpoints still accepting requests", "Map internal/staging APIs referenced in code"],
        ["Demonstrate IDOR or missing auth on hidden API", "Document discovery source (JS line, app version)", "Report zombie endpoints for decommission"],
        REPORT,
    ),
    "api/grpc-protobuf": phases(
        SCOPE + ["Identify gRPC ports and .proto definitions if available"],
        ["Use grpcurl to list services and methods", "Decode protobuf with grpcui or custom descriptors", "Intercept gRPC-over-HTTP/2 in Burp", "Map authentication metadata headers"],
        ["Fuzz each RPC with malformed protobuf", "Test auth on every method independently", "Replay privileged RPCs with low-priv metadata", "Check reflection service exposure"],
        ["Call sensitive RPC without authorization", "Demonstrate data read or state change", "Document service/method names and impact"],
        REPORT + ["Disable reflection in production; enforce per-RPC auth"],
    ),
    "authentication/jwt": phases(
        SCOPE + ["Collect JWTs for each role and note signing algorithm"],
        ["Decode header and payload (jwt_tool)", "Check alg=none, HS/RS confusion, weak secrets", "Review exp, aud, iss claims enforcement", "Test token in header, cookie, and body"],
        ["Forge token with modified claims (role, user id)", "Brute force weak HMAC secrets", "Swap RS256 public key for self-signed", "Test expired and revoked token acceptance"],
        ["Escalate to admin with forged JWT", "Demonstrate account takeover via kid/jku injection", "Document algorithm and claim bypass"],
        REPORT + ["Use RS256, validate all claims, rotate keys, short TTL"],
    ),
    "authentication/password-reset": phases(
        SCOPE + ["Create two test accounts for reset flow testing"],
        ["Map reset request, token delivery, and password change steps", "Analyze token format: random, JWT, timestamp", "Check token binding to email/session/IP", "Review rate limiting on reset requests"],
        ["Reuse reset token after password change", "Modify userId/email in reset POST body", "Brute force short tokens", "Hostile subdomain takeover on reset link domain"],
        ["Take over account via token leak or parameter tampering", "Demonstrate host header poisoning on reset email", "Document full chain with timestamps"],
        REPORT + ["Use single-use cryptographic tokens bound to user session"],
    ),
    "authentication/sso-saml": phases(
        SCOPE + ["Obtain SAML metadata and test IdP/SP accounts"],
        ["Capture SAML Request/Response in Burp", "Review signature algorithm and certificate", "Check Assertion Consumer Service URL validation", "Map attribute mapping to application roles"],
        ["Test signature stripping and wrapping attacks", "Modify NameID and attributes without invalidating sig", "Replay assertions across sessions", "Use SAML Raider extension for mutations"],
        ["Login as victim via forged or replayed assertion", "Escalate role via AttributeStatement tampering", "Document XML signature bypass variant"],
        REPORT + ["Validate signatures, encrypt assertions, strict ACS URL check"],
    ),
    "authentication/passwordless": phases(
        SCOPE + ["Map magic link, OTP, and WebAuthn flows"],
        ["Analyze token entropy and expiration", "Check if OTP is rate limited", "Review magic link binding to browser/session", "Test WebAuthn challenge replay"],
        ["Intercept magic link on shared machine scenario", "Brute force short OTP codes", "Reuse magic link multiple times", "Swap credential ID in WebAuthn assertion"],
        ["Demonstrate account access without possession factor", "Show OTP bypass or link replay", "Document token lifetime and binding gaps"],
        REPORT + ["Bind tokens to session, rate limit OTP, single-use links"],
    ),
}
