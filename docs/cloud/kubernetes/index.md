# Kubernetes Security

Assess cluster RBAC, secrets, and workload isolation.

## Methodology

- [ ] Enumerate pods, roles, and clusterrolebindings
- [ ] Check privileged containers and host mounts
- [ ] Review network policies
- [ ] Test etcd and API server exposure

## Tools

- `kubectl`
- `kube-hunter`
- `kubescape`

## Resources

- [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/)

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
