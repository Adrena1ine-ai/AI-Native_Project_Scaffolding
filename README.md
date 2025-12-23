# 🛠️ AI Toolkit

> **The "iPhone" of AI-powered development tools**  
> Create projects that AI assistants actually understand.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI-Ready](https://img.shields.io/badge/AI--Ready-Toolkit-purple)](https://github.com/user/ai-toolkit)
[![Tests](https://img.shields.io/badge/tests-82%20passed-green.svg)]()

---

## 🎯 What is AI Toolkit?

AI Toolkit creates Python projects **optimized for AI coding assistants** (Cursor, GitHub Copilot, Claude, Windsurf).

### The Problem

| Issue | Impact |
|-------|--------|
| AI creates `venv/` inside project | 🐌 Slow IDE, 500MB garbage |
| AI doesn't understand structure | 🤯 Poor suggestions, wasted tokens |
| AI reads unnecessary files | 💸 Expensive API calls |
| Manual setup every time | ⏰ Time waste, inconsistency |

### The Solution

```bash
toolkit create my_bot --template bot
# ✨ Clean project with venv OUTSIDE, AI configs ready
```

---

## 📊 Project Status

### ✅ Phase 0: Core Foundation — COMPLETE

| Feature | Description | Status |
|---------|-------------|--------|
| CLI Architecture | Modular command system | ✅ |
| Project Creation | 5 templates (bot, webapp, fastapi, parser, full) | ✅ |
| Project Cleanup | 3 levels (safe, medium, full) | ✅ |
| Migration | Add Toolkit to existing projects | ✅ |
| Health Check | 10+ parameter verification | ✅ |
| Update Command | Update Toolkit configs | ✅ |
| Auto Backup | .tar.gz before operations | ✅ |

### ✅ AI Assistant Support — COMPLETE

| IDE | Config Files | Status |
|-----|--------------|--------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` | ✅ |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` | ✅ |
| 🟢 Claude | `CLAUDE.md` | ✅ |
| 🌊 Windsurf | `.windsurfrules` | ✅ |
| 📁 Universal | `_AI_INCLUDE/` shared rules | ✅ |
| 🔄 Context Switcher | `scripts/context.py` | ✅ |

### ✅ Docker & CI/CD — COMPLETE

| Feature | Files | Status |
|---------|-------|--------|
| Docker | `Dockerfile`, `docker-compose.yml`, `.dockerignore` | ✅ |
| CI/CD | `ci.yml`, `cd.yml`, `dependabot.yml` | ✅ |
| Pre-commit | `.pre-commit-config.yaml` | ✅ |
| Git | `.gitignore`, `.gitattributes`, auto-init | ✅ |

### ✅ Generated Scripts — COMPLETE

| Script | Description | Status |
|--------|-------------|--------|
| `bootstrap.sh` | Create venv OUTSIDE project (Unix) | ✅ |
| `bootstrap.ps1` | Same for Windows | ✅ |
| `health_check.sh` | Project health verification | ✅ |
| `check_repo_clean.sh` | Verify clean repo (pre-commit) | ✅ |
| `context.py` | Context Switcher for modules | ✅ |

### ✅ Generated Modules — COMPLETE

| Module | Contents | Status |
|--------|----------|--------|
| `bot/` | main.py, handlers/, keyboards/, utils/, middlewares/ | ✅ |
| `database/` | db.py with CRUD operations | ✅ |
| `api/` | FastAPI with /health and CORS | ✅ |
| `webapp/` | Telegram WebApp SDK template | ✅ |
| `parser/` | httpx + BeautifulSoup scraper | ✅ |

### ✅ Testing — COMPLETE

| Metric | Value | Status |
|--------|-------|--------|
| Test Files | 10+ | ✅ |
| Total Tests | 82 | ✅ |
| Passing | 82/82 (100%) | ✅ |

---

## 🚀 Roadmap

### ✅ Phase 1: Foundation (v3.1) — COMPLETE

> **Goal:** Core utilities for token optimization  
> **Timeline:** Week 1

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 1.1 | Context Map Generator | AST-based `CURRENT_CONTEXT_MAP.md` | ✅ |
| 1.2 | Secret Scanner | 🦊 Fox detects API keys/tokens | ✅ |
| 1.3 | Export Context | `toolkit pack` → XML export | ✅ |
| 1.4 | XML Format | `context_dump.xml` for Claude | ✅ |
| 1.5 | PROMPTS_LIBRARY.md | Template-specific prompts | ✅ |
| 1.6 | README Badge | AI-Ready badge | ✅ |
| 1.7 | Manifesto Scripts | `bootstrap.sh`, `isolate_heavy.sh` | ✅ |
| 1.8 | Pre-commit Hook | 🦊 Fox guard for secrets | ✅ |

### ✅ Phase 2: CLI Wizard (v3.2) — COMPLETE

> **Goal:** Interactive project creation  
> **Timeline:** Week 2-3

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 2.1 | Friendly Wizard | Step-by-step Rich TUI prompts | ✅ |
| 2.2 | Doctor Mode | Optimize existing projects | ✅ |
| 2.3 | SDD Integration | Generate `spec.md` for new projects | ✅ |
| 2.4 | Token Estimator | `toolkit benchmark` + wizard metrics | ✅ |
| 2.5 | Rich Progress | Beautiful Rich panels and tables | ✅ |
| 2.6 | Artifact Archiver | Move garbage to `_AI_ARCHIVE/` | ✅ |
| 2.7 | Role-based .cursorrules | Auto-generated `.cursor/rules/` | ✅ |
| 2.8 | Grand Unification | Constitution + WHERE_THINGS_LIVE | ✅ |

### ✅ Phase 2.5: The Fox Update (v3.3) — COMPLETE

> **Goal:** Security, AST mapping, context sharing  
> **Timeline:** Week 4

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 2.5.1 | 🧠 AST Context Map | Python `ast` module parsing | ✅ |
| 2.5.2 | 🦊 Fox Security Scanner | Detects API keys, tokens, secrets | ✅ |
| 2.5.3 | 📦 XML Packer | `toolkit pack` → single XML file | ✅ |
| 2.5.4 | 🔌 Fox Pre-commit | "🦊 Fox is guarding your repo..." | ✅ |
| 2.5.5 | Entropy Detection | Filters placeholders from secrets | ✅ |
| 2.5.6 | 🔍 Fox Trace | Deep dependency tracker (AST) | ✅ |

### 📍 Phase 3: TUI Dashboard (v3.4) — PLANNED

> **Goal:** Professional terminal dashboard  
> **Timeline:** Week 5-6

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 3.1 | Main Dashboard | Full-screen Textual UI | ⬜ |
| 3.2 | Project Selector | Recent projects list | ⬜ |
| 3.3 | Module Selector | Visual checkbox selection | ⬜ |
| 3.4 | Live Token Counter | Real-time token display | ⬜ |
| 3.5 | Export Panel | Format, sanitize options | ⬜ |
| 3.6 | Health Panel | Visual health status | ⬜ |
| 3.7 | Keyboard Navigation | Vim-style shortcuts | ⬜ |
| 3.8 | Activity Log | Recent actions display | ⬜ |

**TUI Preview:**
```
╔══════════════════════════════════════════════════════════════════╗
║  AI TOOLKIT v3.3                                   [H]elp [Q]uit ║
╠══════════════════════════════════════════════════════════════════╣
║  ╭─ Quick Actions ────────────────────────────────────────────╮ ║
║  │  [N] New Project   [E] Export   [M] Map   [H] Health      │ ║
║  ╰────────────────────────────────────────────────────────────╯ ║
║  ╭─ Current: pizza_bot ───────────────────────────────────────╮ ║
║  │  Type:    🤖 Telegram Bot                                  │ ║
║  │  Health:  ✅ Good (9/10)     Tokens: ~45,000              │ ║
║  │  Modules: bot/ ✓  database/ ✓  api/ ○  webapp/ ○          │ ║
║  ╰────────────────────────────────────────────────────────────╯ ║
╚══════════════════════════════════════════════════════════════════╝
```

### 📍 Phase 4: Automation (v3.4) — PLANNED

> **Goal:** Smart features for power users  
> **Timeline:** Week 6-7

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 4.1 | Advanced Context Switcher | Role-aware switching | ⬜ |
| 4.2 | Diff Export | `--diff`, `--since HEAD~3` | ⬜ |
| 4.3 | Prompt Templates | `toolkit prompt review` | ⬜ |
| 4.4 | Pre-commit Hook | Block commits with secrets | ⬜ |
| 4.5 | Dependency Graph | `toolkit deps --module bot` | ⬜ |
| 4.6 | Smart .cursorignore | Auto-hide unused modules | ⬜ |

### 📍 Phase 5: Quality & PyPI (v3.5) — PLANNED

> **Goal:** Production-ready release  
> **Timeline:** Week 8-9

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 5.1 | PyPI Publication | `pip install ai-toolkit` | ⬜ |
| 5.2 | Type Hints (mypy) | Full code typing | ⬜ |
| 5.3 | pytest Coverage | 80%+ coverage | ⬜ |
| 5.4 | LLM-Friendly Linter | `toolkit lint` | ⬜ |
| 5.5 | Context Map v2 (AST) | `--detailed` option | ⬜ |
| 5.6 | Smart Truncate | `--max-tokens` | ⬜ |
| 5.7 | One-liner (Unix) | `curl \| bash` installer | ⬜ |
| 5.8 | One-liner (Windows) | `irm \| iex` installer | ⬜ |

### 📍 Phase 6: Web UI (v4.0) — PLANNED

> **Goal:** Browser interface for beginners  
> **Timeline:** Week 10-13

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 6.1 | Web Dashboard | FastAPI + Jinja2 | ⬜ |
| 6.2 | Visual Wizard | Step-by-step web form | ⬜ |
| 6.3 | Drag & Drop | Upload existing project | ⬜ |
| 6.4 | Download ZIP | Get created project | ⬜ |
| 6.5 | Online Demo | Try without install | ⬜ |
| 6.6 | API Endpoints | REST API for all features | ⬜ |

### 📍 Phase 7: Extensions (v4.1+) — FUTURE

> **Goal:** Advanced ecosystem  
> **Timeline:** Ongoing

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 7.1 | GUI (Desktop) | Tkinter/PyQt app | 💡 |
| 7.2 | Plugins System | Custom templates | 💡 |
| 7.3 | IDE Extension | VS Code/Cursor plugin | 💡 |
| 7.4 | toolkit share | Shareable project links | 💡 |
| 7.5 | Telegram Bot | @AIToolkitBot | 💡 |
| 7.6 | Auto-context | AI-driven focus detection | 💡 |
| 7.7 | Cost Dashboard | Track AI spending | 💡 |

### 📍 Phase 8: Localization (v4.2) — POST-RELEASE

> **Goal:** Russian language support  
> **Timeline:** After v4.0 stable

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| 8.1 | i18n Framework | gettext/babel setup | 💡 |
| 8.2 | RU Translation | All UI strings | 💡 |
| 8.3 | RU Documentation | README, guides | 💡 |
| 8.4 | RU PROMPTS_LIBRARY | Russian prompts | 💡 |
| 8.5 | Language Selector | Auto-detect or manual | 💡 |

---

## 📈 Progress Summary

```
OVERALL PROGRESS
════════════════════════════════════════════════════════════════════

Phase 0: Core Foundation        ████████████████████████████ 100% ✅
Phase 1: Foundation (v3.1)      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% 🔄
Phase 2: CLI Wizard (v3.2)      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 3: TUI Dashboard (v3.3)   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 4: Automation (v3.4)      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 5: Quality & PyPI (v3.5)  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 6: Web UI (v4.0)          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 7: Extensions (v4.1+)     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% 💡
Phase 8: Localization (v4.2)    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% 💡

════════════════════════════════════════════════════════════════════
TOTAL: 54/110 features (49%) | Next: Phase 1 (v3.1)
```

### Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🔄 | In Progress |
| ⬜ | Planned |
| 💡 | Future Idea |

### 📊 Statistics

| Metric | Current | Target |
|--------|---------|--------|
| Features Implemented | 54 | 110 |
| Lines of Code | 3,541 | ~8,000 |
| Tests Passing | 82/82 | 150+ |
| Templates | 6 | 10+ |
| Supported IDEs | 5 | 5 |
| Interfaces | CLI | CLI + TUI + Web |
| Languages | EN | EN + RU |

---

## 🚀 Quick Start


### Installation

```bash
# 1. Simplest way (recommended)
pipx install git+https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git

# 2. Or classically via pip
pip install git+https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git

# 3. With extras (Web Dashboard + TUI)
pipx install "git+https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git[web,tui]"

# 4. From source (for development)
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e ".[web,tui,dev]"

# Future (after PyPI release)
pip install ai-toolkit[ui]        # With wizard
pip install ai-toolkit[ui,tui]    # With TUI dashboard
pipx install ai-toolkit[ui]       # Isolated (recommended)
`

### Usage

```bash
# Interactive mode
python main.py

# Create project
python main.py create my_bot --template bot

# Export for AI (coming in v3.1)
python main.py export --module bot --format xml

# Health check
python main.py health ./my_project

# TUI Dashboard (coming in v3.3)
python main.py tui
```

---

## 📁 Project Structure

```
ai_toolkit/
├── src/
│   ├── cli.py              # Main CLI
│   ├── commands/           # CLI commands
│   │   ├── create.py       # ✅ Project creation
│   │   ├── cleanup.py      # ✅ Project cleanup
│   │   ├── migrate.py      # ✅ Migration
│   │   ├── health.py       # ✅ Health checks
│   │   ├── update.py       # ✅ Updates
│   │   ├── export.py       # 🔄 Context export (Phase 1)
│   │   ├── map.py          # 🔄 Context map (Phase 1)
│   │   └── prompt.py       # ⬜ Prompts (Phase 4)
│   ├── generators/         # ✅ File generators
│   ├── core/               # ✅ Core utilities
│   ├── ui/                 # ⬜ CLI Wizard (Phase 2)
│   ├── tui/                # ⬜ TUI Dashboard (Phase 3)
│   ├── utils/              # 🔄 Utilities (Phase 1)
│   └── i18n/               # 💡 Localization (Phase 8)
├── web/                    # ⬜ Web UI (Phase 6)
├── tests/                  # ✅ 82 tests
├── templates/              # ✅ 6 templates
├── plugins/                # ✅ Plugin system
└── docs/                   # Documentation
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing`
3. Make changes and add tests
4. Run tests: `python -m pytest tests/ -v`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing`
7. Open Pull Request

---

## 👥 Credits

**Mickhael** — Project Creator & Lead Developer

**Claude (Anthropic)** — AI Development Partner
- Technical specification
- Architecture recommendations
- Documentation

> *"This project was developed with significant assistance from my good colleague Claude (Anthropic)."*
> *"P.S. and Grok, Gemini too ^_^"*

---

## 📄 License

MIT © Michael Salmin

See [LICENSE](LICENSE) for details.

---

## 💬 Support

- 🐛 [Open an Issue](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 [Discussions](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)

---

<p align="center">
  <strong>Made with ❤️ for AI-first development</strong>
</p>

