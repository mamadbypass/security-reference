# Kubernetes Security

Assess cluster RBAC, secrets, and workload isolation.

## How It Works

Kubernetes orchestrates containerized workloads across clusters of nodes. Security boundaries include:

- **API server** — Authenticates and authorizes all cluster operations via RBAC, admission controllers, and optional OPA/Gatekeeper policies.
- **etcd** — Stores all cluster state including Secrets (base64, not encrypted by default).
- **Nodes** — Run kubelet, container runtime; compromise grants access to all pods on the node.
- **Pods** — Service accounts with projected tokens; privileged pods can escape to the host.
- **Network policies** — Optional L3/L4 firewall between pods (often not deployed).

Common misconfigs: anonymous API access, cluster-admin bindings to default service accounts, secrets mounted in env vars, and exposed Dashboard/etcd.

## Exploitation

1. **Enumerate RBAC** — `kubectl auth can-i --list`; `kubectl get clusterrolebindings -o wide`.
2. **Hunt secrets** — `kubectl get secrets -A`; decode base64 values.
3. **Privileged pods** — `kubectl run pwn --image=alpine --privileged --overrides='...hostPID:true'` for node escape.
4. **Service account token abuse** — Steal mounted tokens; test permissions with `kubectl --token=`.
5. **kube-hunter/kube-bench** — Scan for exposed API, dashboard, and CIS benchmark failures.
6. **etcd exposure** — Port 2379 without TLS/auth dumps entire cluster state.
7. **Supply chain** — Malicious images in registries without admission scanning.
8. **Document namespace scope** — Findings per namespace and ClusterRole impact.

## Defense & Mitigation

- **Enable RBAC** — No anonymous access; audit cluster-admin bindings.
- **Pod Security Standards** (restricted) — No privileged, host namespaces, or root users.
- **Network policies** — Default deny inter-namespace traffic.
- **Encrypt etcd at rest**; restrict etcd to control plane only.
- **Rotate service account tokens**; use bound tokens with short TTL.
- **Admission controllers** — OPA/Gatekeeper, Kyverno for policy enforcement.
- **Image scanning** — Trivy/Grype in CI; sign with cosign.
- Follow [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/).

## Methodology

- [ ] Enumerate pods, roles, and clusterrolebindings
- [ ] Check privileged containers and host mounts
- [ ] Review network policies
- [ ] Test etcd and API server exposure

## Tools

| Tool | Usage |
|------|-------|
| `kubectl` | [Kubernetes CLI](https://kubernetes.io/docs/reference/kubectl/) |
| `kube-hunter` | [Kubernetes pentest](../../TOOLS_GUIDE.md#kube-hunter) |
| `kubescape` | [K8s security posture](https://github.com/kubescape/kubescape) |

## Resources

- [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
