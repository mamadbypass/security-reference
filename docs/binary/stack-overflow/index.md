# Stack Buffer Overflow

Classic stack-based memory corruption exploitation.

## Methodology

- [ ] Fuzz for crash inputs
- [ ] Calculate offset to return address
- [ ] Bypass DEP/ASLR where applicable
- [ ] Develop reliable proof-of-concept in lab

## Tools

- `gdb`
- `pwndbg`
- `gef`
- `ropper`

## Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
