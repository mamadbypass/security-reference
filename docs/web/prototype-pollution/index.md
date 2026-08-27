# Prototype Pollution

Pollute JavaScript object prototypes for XSS and RCE.

## How It Works

Prototype pollution is a JavaScript vulnerability where attackers modify `Object.prototype` (or other builtins) by injecting properties through unsafe object merge, extend, or clone operations.

Typical vulnerable pattern:

```javascript
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key];
  }
}
```

Payload via query string or JSON:

```json
{"__proto__": {"polluted": true}}
```

or

```json
{"constructor": {"prototype": {"polluted": true}}}
```

After pollution, `{}.polluted` is true because new objects inherit the poisoned prototype.

**Client-side**: Gadgets in libraries read from `obj.polluted` options → XSS.

**Server-side (Node.js)**: Pollution affects template engines, authorization checks, or `child_process` options → RCE in severe cases.

## Exploitation

**Client-side**

1. Find `lodash.merge`, `jQuery.extend`, or custom deep merge on `location.hash` or JSON configs.
2. Pollute: `?__proto__[test]=polluted` or JSON `__proto__` key.
3. Chain gadgets: if app checks `if (obj.isAdmin)` and `isAdmin` can be set on prototype, bypass auth UI.

**Server-side Node**

```json
{"__proto__": {"shell": "node", "NODE_OPTIONS": "--require /proc/self/environ"}}
```

When polluted properties flow into `child_process.spawn` options or template engines.

**Attack flow**

```
Malicious key in merge → prototype polluted → later object access reads attacker property → XSS / RCE / auth bypass
```

**Tools**

- ppmap for gadget research
- Burp to fuzz JSON bodies with `__proto__`, `constructor.prototype`

**Detection**

- After payload, evaluate `({}).polluted` in console or check behavior changes globally.

## Defense & Mitigation

**Safe merging**

- Use `Object.create(null)` for dictionaries without prototype chain.
- Freeze `Object.prototype` in hardened environments (`Object.freeze(Object.prototype)`).
- Libraries: upgrade lodash (CVE fixes), use `structuredClone` or safe merge utilities that block `__proto__`, `constructor`, `prototype`.

**Input validation**

- Reject keys matching `__proto__`, `constructor`, `prototype` in JSON parsers for untrusted input.
- JSON schema validation with additional property restrictions.

**Server-side Node**

- Avoid recursive merge on request bodies; validate schema explicitly.
- Run with least privilege; isolate workers.

**Dependencies**

- Audit client bundles for vulnerable merge helpers; pin patched versions.

## Methodology

- [ ] Identify merge/extend utilities in client code
- [ ] Test __proto__ and constructor.prototype keys
- [ ] Look for gadget chains leading to XSS
- [ ] Check server-side Node.js pollution

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `ppmap` | [Prototype pollution scanner](../../TOOLS_GUIDE.md#ppmap) |
| `dom clobbering scanners` | [Browser DevTools + DOM XSS sinks review](../../TOOLS_GUIDE.md) |

## Resources

- [PortSwigger Prototype Pollution](https://portswigger.net/web-security/prototype-pollution)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
