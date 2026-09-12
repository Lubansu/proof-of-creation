# Contributing to proof-of-creation

Thank you for your interest in improving Proof of Creation for Claude Code users.

## Priority contributions needed

### 1. Jurisdiction coverage
The most impactful contribution is adding or improving country-specific legal
guidance in `skills/proof-of-creation/references/legal-by-country.md`.

**High priority:**
- Middle East (UAE, Saudi Arabia, Israel)
- Southeast Asia (Singapore, Thailand, Vietnam, Indonesia)
- Sub-Saharan Africa (South Africa, Nigeria, Kenya)
- Latin America (Mexico, Argentina, Colombia)

Each jurisdiction entry should include:
- Automatic protection: Yes/No + legal basis
- Registration authority + URL + cost
- Duration
- Special notes relevant to software developers

### 2. API integrations
Connect directly to IP office APIs for automated guidance:
- INPI France (Enveloppe Soleau form pre-fill)
- USPTO (registration status check)
- Bernstein.io or OriginStamp (one-command blockchain timestamp)

### 3. License detection improvements
Improve dependency license scanning for:
- Python (`requirements.txt`, `pyproject.toml`, `setup.py`)
- Node.js (`package.json`, `package-lock.json`, `yarn.lock`)
- Rust (`Cargo.toml`, `Cargo.lock`)
- PHP (`composer.json`)
- Go (`go.mod`)

### 4. Translations
The SKILL.md description should be available in:
- Spanish, German, Portuguese, Japanese, Chinese

## How to contribute

1. Fork this repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Validate the skill: `python3 install_skill.py --list`
5. Open a pull request with a clear description

## Code of conduct

Be respectful. This project serves creators protecting their work.
Contributions that undermine Proof of Creation or assist circumvention
of copyright law will not be accepted.

## Legal note

By contributing, you agree your contributions are licensed under MIT
and you have the right to make them available under that license.
