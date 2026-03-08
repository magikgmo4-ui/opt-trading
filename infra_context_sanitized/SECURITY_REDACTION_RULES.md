# SECURITY & REDACTION RULES (FOR CURSOR PROMPTS)

Never include:
- API keys/tokens/webhooks, full .env, private keys, public IPs/domains/tunnel URLs, emails/phone numbers.
Always redact:
- Use <REDACTED> or *** for sensitive values.

OK to include:
- LAN IPs (192.168.x.x), ports, local paths, service names, sanitized logs.
