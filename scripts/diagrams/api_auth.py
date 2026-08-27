API_AUTH_DIAGRAMS = {
    "api/graphql": """
flowchart TD
    Q[GraphQL query] --> API[API endpoint]
    API --> INTRO{Introspection?}
    INTRO -->|enabled| SCHEMA[Full schema dump]
    API --> BATCH[Batching abuse]
    API --> AUTH{Field-level auth?}
    AUTH -->|missing| IDOR[Access other users' data]
""",
    "api/graphql/introspection": """
flowchart LR
    A[Attacker] -->|__schema query| GQL[GraphQL API]
    GQL --> TYPES[Types & mutations exposed]
    TYPES --> ATTACK[Target sensitive resolvers]
""",
    "api/graphql/batching": """
sequenceDiagram
    participant A as Attacker
    participant API as GraphQL
    A->>API: Batch 1000 queries in 1 HTTP request
    API->>API: Rate limit bypassed
    API-->>A: Mass data / brute force
""",
    "api/versioning": """
flowchart TD
    V1[/api/v1 deprecated] --> OLD[Weak auth / debug]
    V2[/api/v2 current] --> NEW[Hardened]
    A[Attacker] --> V1
    OLD --> BYPASS[Bypass v2 controls]
""",
    "api/shadow-zombie-apis": """
flowchart LR
    JS[JavaScript bundles] --> LF[linkfinder]
    LF --> HIDDEN[Hidden API routes]
    HIDDEN --> OLD[Unmaintained endpoints]
    OLD --> VULN[No auth / IDOR]
""",
    "api/grpc-protobuf": """
flowchart TD
    PB[Protobuf service] --> DECODE[Decode / grpcurl]
    DECODE --> METHODS[List RPC methods]
    METHODS --> AUTH{Auth on each RPC?}
    AUTH -->|no| ABUSE[Sensitive operations]
""",
    "authentication/jwt": """
flowchart TD
    JWT[JWT token] --> ALG{alg=none / HS confusion?}
    ALG -->|weak| FORGE[Forged token]
    FORGE --> ACCESS[Privileged access]
    JWT --> EXP[Expired? / missing aud]
""",
    "authentication/password-reset": """
flowchart LR
    REQ[Reset request] --> TOKEN[Reset token]
    TOKEN --> LEAK{Predictable / leaked?}
    LEAK -->|yes| HIJACK[Account takeover]
""",
    "authentication/sso-saml": """
flowchart TD
    SAML[SAML Response] --> SIG{Signature valid?}
    SIG -->|bypass| ASSERT[Modified Assertion]
    ASSERT --> LOGIN[Login as victim]
""",
    "authentication/passwordless": """
flowchart LR
    MAGIC[Magic link / OTP] --> EMAIL[Email channel]
    EMAIL --> LEAK[Token in referrer/logs]
    LEAK --> ATO[Account takeover]
""",
}
