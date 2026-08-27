# Kubernetes Hardening

Secure Kubernetes clusters and workloads.

## How It Works

**Kubernetes** orchestrates containers across nodes with RBAC, admission controllers, network policies, and secrets stored in etcd. Misconfigurations—overly permissive ClusterRoleBindings, default service accounts with API access, secrets in ConfigMaps, missing NetworkPolicies—allow lateral movement and cluster takeover.

The API server, kubelet, and etcd are high-value targets. Workloads in the same cluster often share flat network visibility unless policies segment traffic.

## Exploitation

1. **Recon from pod**: `kubectl auth can-i --list` if kubeconfig or token is available.
2. **Enumerate**: pods, secrets, configmaps, rolebindings across namespaces.
3. **Privileged pods**: create or exec into pods with hostPath, hostPID, or privileged securityContext.
4. **Secrets theft**: read secrets in accessible namespaces; decode base64 credentials.
5. **kube-hunter / kubescape**: automated misconfiguration scans.
6. **Network**: if no NetworkPolicy, scan cluster internal services from compromised pod.

Peirates and CDK automate common K8s privilege escalation paths from inside a pod.

## Defense & Mitigation

- Apply **least-privilege RBAC**; avoid cluster-admin bindings for applications.
- Enable **Pod Security Standards** (restricted baseline) via admission controllers.
- Encrypt etcd; restrict API server access; enable audit logging.
- Use **NetworkPolicies** for default-deny between namespaces.
- Rotate service account tokens; disable auto-mount where not needed.
- Run kubescape, kube-bench, and Falco for policy and runtime threat detection.

## Methodology

- [ ] Apply least privilege RBAC
- [ ] Enable admission controllers
- [ ] Restrict pod security standards
- [ ] Audit secrets management

## Tools

| Tool | Usage |
|------|-------|
| `kubescape` | [K8s security posture](https://github.com/kubescape/kubescape) |
| `falco` | Runtime threat detection — [falco.org](https://falco.org/) |
| `kyverno` | Kubernetes policy engine — [kyverno.io](https://kyverno.io/) |

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
