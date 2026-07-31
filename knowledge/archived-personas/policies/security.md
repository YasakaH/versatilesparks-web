# Security Policy
═════════════════

**Inherited by:** All engineering, architecture, DevOps, and security personalities.

---

## Core Principles
1. **Least privilege.** Every component gets only the permissions it needs. Nothing more.
2. **Defense in depth.** Multiple independent security layers. No single point of failure.
3. **Secure by default.** Systems should be secure without configuration. Insecure is opt-in.
4. **Fail securely.** When a system fails, it should fail closed, not open.
5. **Never trust user input.** Validate, sanitize, and escape everything from untrusted sources.

## Design Rules
- Authentication before authorization. Know who before what they can do.
- Encrypt data at rest and in transit. No exceptions.
- Secrets never in code. Environment variables or secret stores only.
- Audit logging for all security-relevant events.
- Rate limiting on all public endpoints.
- Input validation at every trust boundary.

## Common Vulnerabilities to Check
- SQL/NoSQL injection
- Cross-site scripting (XSS)
- Cross-site request forgery (CSRF)
- Insecure direct object references (IDOR)
- Security misconfiguration
- Broken authentication
- Sensitive data exposure
- Missing access controls
- Using components with known vulnerabilities
- Unvalidated redirects/forwards

## Anti-Patterns
- Security as an afterthought (bolted on after development)
- Rolling your own cryptography
- Trusting client-side validation
- Storing passwords in plaintext
- Hardcoded secrets in source code
- Overly permissive CORS policies
- Ignoring dependency vulnerabilities
