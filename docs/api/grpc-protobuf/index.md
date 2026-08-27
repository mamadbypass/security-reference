# gRPC & Protobuf

Test gRPC services and protobuf-encoded APIs.

## How It Works

gRPC uses HTTP/2 with Protocol Buffers (protobuf) for compact binary messages. Services expose RPC methods (`/package.Service/Method`) instead of REST paths. **gRPC server reflection** allows clients to list services and message types at runtime—similar to GraphQL introspection. Many internal microservices speak gRPC on ports like 50051, sometimes exposed through gRPC-Web, Envoy transcoding, or misconfigured load balancers.

Protobuf is not encryption: messages can be decoded with a `.proto` file or inferred via reflection. Metadata headers carry JWTs and API keys; mTLS is optional and often missing on "internal" networks reachable from SSRF or VPN gaps.

## Exploitation

1. **Discover gRPC ports** — Scan for 50051, 443 with HTTP/2, and `content-type: application/grpc` responses.
2. **Enable reflection** — `grpcurl -plaintext host:50051 list` or `grpcui` to enumerate services when reflection is on.
3. **Obtain `.proto` files** — From repos, APKs, reflection, or transcoding gateway configs; use `protoc` or Burp gRPC assistant to craft messages.
4. **Call methods without auth** — Invoke `GetUser`, `Admin`, `Export` RPCs with empty or forged metadata.
5. **Fuzz fields** — Protobuf parsers may ignore unknown fields; test oversized strings, negative IDs, and enum overflows.
6. **Test metadata tokens** — Replay JWTs across services; try missing/alternate `:authority` headers.
7. **Exploit gRPC-Web bridges** — Browser-facing transcoding may weaken auth applied on native gRPC hops.
8. **SSRF to gRPC** — If an app can reach internal gRPC, pivot from HTTP SSRF to binary RPC calls.

## Defense & Mitigation

- **Disable server reflection in production**; distribute protos only through secure artifact registries.
- **Require mTLS and/or signed JWTs** on every RPC; enforce per-method authorization.
- **Do not expose raw gRPC to the internet**; use API gateways with policy enforcement.
- **Network segmentation** so only trusted meshes (service mesh sidecars) can reach gRPC backends.
- **Validate all protobuf fields** server-side; never trust client-supplied IDs for access control.
- **Log RPC method, peer identity, and latency**; alert on reflection probes and unauthenticated calls.

## Methodology

- [ ] Identify gRPC ports and reflection
- [ ] Decode protobuf messages from traffic
- [ ] Fuzz RPC methods for auth bypass
- [ ] Test TLS and metadata token handling

## Tools

| Tool | Usage |
|------|-------|
| `grpcurl` | See [Tools Guide](/TOOLS_GUIDE/) |
| `grpcui` | See [Tools Guide](/TOOLS_GUIDE/) |
| `burp grpc assistant` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [gRPC Security](https://grpc.io/docs/guides/auth/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
