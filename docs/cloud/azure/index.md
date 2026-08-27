# Azure Security Testing

Assess Microsoft Azure identity and resource misconfigurations.

## How It Works

Microsoft Azure security spans **Azure Active Directory (Entra ID)**, subscriptions, resource groups, and platform services. Key attack surfaces:

- **Entra ID** — User enumeration, password spray, OAuth consent phishing, misconfigured app registrations with excessive API permissions.
- **Storage accounts** — Public blob containers and shared access signatures (SAS) with long expiry.
- **Virtual machines** — NSG rules exposing RDP/SSH; managed identities with broad RBAC.
- **Key Vault** — Access policies granting secrets to overprivileged principals.
- **Azure DevOps / GitHub** — Pipeline secrets and service connections.

Azure uses **RBAC** (Owner, Contributor, Reader) at subscription/resource scope. Managed identities allow VMs and functions to authenticate without stored keys—but over-assigned roles create lateral movement paths.

## Exploitation

1. **Enumerate Entra ID** — `ROADtools` or `azurehound` for users, groups, apps, and role assignments.
2. **Password spray** — `MSOLSpray` or `o365creeper` against synced accounts (authorized only).
3. **Hunt storage exposure** — `MicroBurst` `Get-AzureBlobContent` and public container scanners.
4. **Abuse managed identities** — From compromised VM, request tokens from `http://169.254.169.254/metadata/identity/oauth2/token`.
5. **App registration abuse** — Excessive `Microsoft Graph` permissions (`Directory.ReadWrite.All`).
6. **Conditional access bypass** — Legacy auth protocols, device code flow.
7. **Key Vault access** — `az keyvault secret list` with compromised Contributor role.
8. **Map to MITRE** — Document Entra vs Azure Resource Manager attack paths.

## Defense & Mitigation

- **Enforce Conditional Access** — MFA, compliant devices, block legacy auth.
- **Disable public blob access** on storage accounts by default.
- **Use Privileged Identity Management (PIM)** — Just-in-time admin roles.
- **Audit app registrations** — Restrict admin consent; review API permissions.
- **Enable Defender for Cloud** and Entra ID Protection.
- **NSG default deny** — No RDP/SSH from internet; use Bastion or VPN.
- **Log Analytics** — Centralize Activity Log, Sign-in logs, and Sentinel analytics.

## Methodology

- [ ] Enumerate Azure AD and app registrations
- [ ] Review storage account public access
- [ ] Check managed identity permissions
- [ ] Test conditional access bypass scenarios

## Tools

| Tool | Usage |
|------|-------|
| `roadtools` | See [Tools Guide](/TOOLS_GUIDE/) |
| `azurehound` | See [Tools Guide](/TOOLS_GUIDE/) |
| `microburst` | See [Tools Guide](/TOOLS_GUIDE/) |

## Resources

- [HackTricks Azure](https://book.hacktricks.xyz/cloud-security/azure-security)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
