# Container Escape

Break out of container isolation to the host.

## How It Works

**Container escape** breaks isolation between a container and the host kernel or other containers. Vectors include **privileged containers**, **host namespace sharing**, mounted **host paths** (`/`, `/proc`, docker.sock), **kernel exploits**, and abuse of **Linux capabilities** (CAP_SYS_ADMIN, CAP_DAC_READ_SEARCH).

cgroups v1 `release_agent` attacks write commands executed on the host when cgroup limits are exceeded. CVEs in runc, containerd, and the kernel periodically enable new escape primitives.

## Exploitation

1. **Enumerate**: `capsh --print`, check `/proc/1/cgroup`, mount points, and `id`.
2. **docker.sock**: instantiate host-root container as described in Docker section.
3. **Privileged + hostPath**: mount host disk and chroot into host filesystem.
4. **release_agent**: CDK/deepce automate cgroup escape on vulnerable configurations.
5. **Kernel exploits**: match `uname -r` to known CVEs (Dirty Pipe, etc.) in lab only.
6. **Confirm escape**: create file on host or read `/etc/shadow` from host mount.

Document exact misconfiguration; escapes are often configuration bugs not kernel bugs.

## Defense & Mitigation

- Never run **privileged** containers in production; validate with admission policy.
- Block hostPath mounts except tightly controlled exceptions.
- Keep kernel, runc, and containerd **patched**; subscribe to security advisories.
- Use gVisor or Kata Containers for stronger isolation on multi-tenant workloads.
- Monitor for escape indicators: unexpected mounts, cgroup writes, docker API from pods.
- Regularly pentest cluster configurations with kube-hunter from both outside and inside.

## Methodology

- [ ] Identify privileged containers
- [ ] Abuse mounted docker.sock
- [ ] Exploit kernel vulnerabilities when in scope
- [ ] Test cgroup release_agent techniques

## Tools

| Tool | Usage |
|------|-------|
| `deepce` | [Container escape enumeration](../../TOOLS_GUIDE.md) |
| `cdk` | Container penetration toolkit — [cdk](https://github.com/cdk-team/CDK) |

## Resources

- [HackTricks Docker Escape](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
