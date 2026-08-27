# Reverse Engineering

Analyze binaries to understand program behavior.

## Overview Diagram

Visual summary of the **attack/data flow** and the **five-phase testing workflow** for this topic.

### Attack / Data Flow

<div class="sr-diagram" markdown="1">

```mermaid
flowchart TD
    BIN[Binary] --> GH[Ghidra analyze]
    GH --> FUNCS[Functions & strings]
    FUNCS --> VULN[Find vuln logic]
    VULN --> POC[Exploit PoC]
classDef attacker fill:#ef4444,stroke:#b91c1c,color:#fff
classDef target fill:#6c3ce0,stroke:#5429c4,color:#fff
classDef tool fill:#f59e0b,stroke:#d97706,color:#1a1a1a
classDef success fill:#10b981,stroke:#059669,color:#fff
classDef warn fill:#f97316,stroke:#ea580c,color:#fff

```

</div>

### Testing Workflow

<div class="sr-diagram sr-diagram-methodology" markdown="1">

```mermaid
flowchart LR
    P1["1. Preparation & Scoping"]
    P2["2. Discovery & Mapping"]
    P3["3. Validation & Testing"]
    P4["4. Exploitation & Impact Proof"]
    P5["5. Documentation & Reporting"]
    P1 --> P2 --> P3 --> P4 --> P5
```

</div>

## How It Works

**Reverse engineering** recovers program logic from compiled binaries without source code. Disassemblers (Ghidra, IDA) lift machine code to intermediate representations; debuggers (gdb, x64dbg) observe runtime state. Analysts identify **entry points**, **string references**, **crypto constants**, and **network protocols**.

Binaries may be stripped of symbols, obfuscated, or packed. Anti-debug and anti-VM techniques slow analysis but rarely stop determined researchers with sufficient time.

## Exploitation

1. **Initial triage**: `strings`, `file`, `binwalk`, entropy analysis for packing.
2. **Load in Ghidra**: auto-analyze, rename functions, annotate key logic.
3. **Cross-references**: follow calls from `strcmp`, `recv`, `printf` to validation routines.
4. **Dynamic trace**: gdb with breakpoints on compare instructions for license checks.
5. **Patch binary**: NOP out jumps or modify constants for proof-of-concept (authorized only).
6. **Document**: export decompiler output with comments for report appendices.

For malware, work only in isolated VMs with no network egress.

## Defense & Mitigation

- Assume binaries can be reversed; **do not rely on client-side secrecy**.
- Use server-side validation for licenses, auth, and critical business rules.
- Apply obfuscation and anti-tamper as **delay layers**, not primary security.
- Strip symbols in release builds; avoid embedding secrets in binaries.
- Monitor for cracked distributions; use legal and technical responses as appropriate.
- For sensitive firmware, encrypt payloads and verify integrity at boot.

## Testing Methodology

Work through each phase in order. Every step has a checkbox — complete them all for thorough, reproducible coverage.

### Phase 1 — Preparation & Scoping

- [ ] Confirm target is in program scope and ROE allows this test type
- [ ] Set up isolated lab or proxy (Burp/ZAP) with scope filters
- [ ] Document baseline application behavior and account roles
- [ ] Identify test accounts for each privilege level
- [ ] Obtain binary and legal authorization to analyze

### Phase 2 — Discovery & Mapping

- [ ] Identify architecture, packing, and anti-debug
- [ ] Load in Ghidra/IDA and run auto-analysis
- [ ] Rename key functions and map call graph
- [ ] Extract strings, imports, and crypto constants

### Phase 3 — Validation & Testing

- [ ] Trace vulnerable function (strcpy, format string)
- [ ] Debug with gdb/gef to confirm flow
- [ ] Develop minimal PoC input
- [ ] Document offset and mitigation (ASLR, PIE, NX)

### Phase 4 — Exploitation & Impact Proof

- [ ] Demonstrate controlled crash or exploit in lab
- [ ] Provide patched pseudocode recommendation

### Phase 5 — Documentation & Reporting

- [ ] Write step-by-step reproduction with HTTP requests/responses
- [ ] Capture screenshots or video showing impact (redact sensitive data)
- [ ] Rate severity using program CVSS or impact matrix
- [ ] Provide concrete remediation guidance for developers
- [ ] Retest after fix if program allows verification

## Tools

| Tool | Usage |
|------|-------|
| `ghidra` | [Reverse engineering suite](../../TOOLS_GUIDE.md#ghidra) |
| `ida` | Interactive disassembler — [hex-rays.com](https://hex-rays.com/ida-pro/) |
| `radare2` | Open-source reversing — [rada.re](https://rada.re/n/) |
| `binary ninja` | Commercial reverse engineering — [binary.ninja](https://binary.ninja/) |

## Resources

- [Ghidra Training](https://ghidra-sre.org/)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
