# 📋 Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> 🇷🇺 [Русская версия](CHANGELOG.ru.md)

---

## [3.0.0] - 2024-12-20

### 🎉 First Public Release!

#### ✨ Added

**Project Creation:**
- 6 project templates: `bot`, `webapp`, `fastapi`, `parser`, `full`, `monorepo`
- Support for 4 AI assistants: Cursor, GitHub Copilot, Claude, Windsurf
- Docker integration (Dockerfile, docker-compose.yml)
- CI/CD (GitHub Actions: ci.yml, cd.yml)
- Dependabot for auto-updating dependencies
- pre-commit hooks to prevent venv in project
- Git integration (auto init + first commit)

**Working with Existing Projects:**
- Analysis and cleanup of "dirty" projects (3 levels: safe/medium/full)
- Migration of existing projects (adding AI Toolkit)
- Health check to verify settings
- Project updates to new version

**Tools:**
- Context Switcher to focus AI on needed modules
- Plugin system for extending functionality
- Support for toolkit.yaml for custom settings

**Interfaces:**
- 🌐 Web Dashboard (FastAPI + beautiful UI)
- 🖥️ GUI (Tkinter)
- 💻 Interactive CLI
- ⌨️ CLI with arguments

**AI Configs:**
- `.cursorrules` + `.cursorignore` for Cursor
- `.github/copilot-instructions.md` for GitHub Copilot
- `CLAUDE.md` for Claude
- `.windsurfrules` for Windsurf
- `_AI_INCLUDE/` with project rules

**Scripts:**
- `bootstrap.sh` / `bootstrap.ps1` — create venv OUTSIDE project
- `health_check.sh` — verify configuration
- `context.py` — hide/show modules from AI
- `check_repo_clean.sh` — pre-commit hook

**Documentation:**
- README.md with detailed description
- CONTRIBUTING.md for contributors
- CHANGELOG.md
- docs/GUIDE.md — complete guide
- docs/FAQ.md — frequently asked questions
- docs/QUICK_START.md — quick start

**Localization:**
- Full English and Russian support
- Language selection at first launch
- Language switcher in Web Dashboard
- All documentation in both languages

#### 🛡️ Security

- venv stored OUTSIDE project — AI doesn't read dependencies
- `.cursorignore` / `.gitignore` — proper file exclusion
- No sensitive data committed (pre-commit hooks)

---

## [2.0.0] - 2024-12-01 (internal)

### Changed
- Modular architecture
- Separated generators
- Added tests

---

## [1.0.0] - 2024-11-01 (internal)

### Added
- Initial prototype
- Basic project creation
- Cursor support
