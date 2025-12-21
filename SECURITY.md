# 🔒 Security Policy

## Supported Versions

| Version | Support |
|---------|---------|
| 3.x     | ✅ Active |
| 2.x     | ❌ Not supported |
| 1.x     | ❌ Not supported |

## Report a Vulnerability

If you find a security vulnerability:

1. **DO NOT** create a public Issue
2. Contact via Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
3. Include:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Time

- Acknowledgment of receipt: 48 hours
- Initial assessment: 7 days
- Fix: depends on severity

## Rewards

Currently there is no bug bounty program, but we thank everyone who helps improve project security.

## Best Practices

When using AI Toolkit:

1. **Don't store secrets in code** — use `.env`
2. **Add `.env` to `.gitignore`** — AI Toolkit does this automatically
3. **Use pre-commit hooks** — protection against accidental commits
4. **Check dependencies** — use `pip audit`
