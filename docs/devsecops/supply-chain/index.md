# Supply Chain Security

Protect software dependencies and build integrity.

## How It Works

**Software supply chain** attacks compromise dependencies, build tools, or distribution channels so malicious code reaches downstream users. Examples include npm/PyPI typosquatting, compromised maintainer accounts, SolarWinds-style build injection, and unsigned container images.

Modern apps depend on hundreds of transitive packages. A single hijacked dependency version can steal environment variables, add backdoors, or sabotage builds.

## Exploitation

1. **Dependency audit**: `npm audit`, `pip-audit`, Dependabot alerts; review transitive deps.
2. **Typosquatting hunt**: search registries for packages mimicking internal names.
3. **SBOM diff**: compare Syft-generated SBOMs between releases for new publishers.
4. **Build review**: inspect CI for unpinned tools and post-install scripts (`preinstall`).
5. **Registry hygiene**: verify image signatures before deploy (`cosign verify`).
6. **Maintainer impersonation**: monitor for sudden major version bumps from new contributors.

Researcher perspective: report malicious packages to registries; publish IOCs responsibly.

## Defense & Mitigation

- **Pin dependencies** to exact versions; commit lockfiles; review lockfile changes in PRs.
- Generate and store **SBOMs** (CycloneDX, SPDX) for every release.
- Sign artifacts and images; enforce signature verification in deploy pipelines.
- Use private registries and npm/pypi proxies with malware scanning.
- Disable arbitrary post-install scripts in CI sandboxes where possible.
- Adopt **SLSA** levels incrementally; monitor CISA guidance on supply chain security.

## Methodology

- [ ] Pin dependency versions
- [ ] Monitor for typosquatting
- [ ] Use SBOM generation
- [ ] Verify package signatures

## Tools

| Tool | Usage |
|------|-------|
| `syft` | [SBOM generator](https://github.com/anchore/syft) |
| `cosign` | [Container signing](https://github.com/sigstore/cosign) |
| `dependabot` | [GitHub dependency alerts & automated PRs](../../TOOLS_GUIDE.md) |

## Resources

- [SLSA Framework](https://slsa.dev/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
