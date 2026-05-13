# Security Policy

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 1.0.x   | ✓ Yes             |
| < 1.0   | ✗ No              |

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

To report a security issue responsibly:

1. **Email:** Send details to [security@example.com] (or use GitHub's security advisory feature)
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Any suggested fixes (optional)

3. **Timeline:**
   - We will acknowledge receipt within 48 hours
   - We aim to release a fix within 7 days for critical issues
   - Reporters will be credited (with permission)

## Security Best Practices

### For Users
- Keep Xiom and its dependencies updated
- Never commit API keys or credentials to version control
- Use environment variables for sensitive data
- Only scan systems you own or have written permission to test
- Review configuration files before sharing

### For Developers
- Do not hardcode API keys or secrets
- Validate all user input (URLs, parameters)
- Use HTTPS for all external API calls
- Follow PEP 8 and security best practices
- Run dependency security checks: `pip-audit` or `safety check`

## Known Limitations

- Xiom performs active scanning and may trigger IDS/WAF alerts
- Some servers may block or rate-limit fingerprinting attempts
- Results depend on external APIs and DNS resolver availability
- Port scanning may be slow on networks with high latency

## Disclaimer

Xiom is a security research tool. Users are responsible for ensuring they have explicit authorization before scanning any systems or networks. Unauthorized access to computer systems is illegal.

---

Thank you for helping keep Xiom secure!
