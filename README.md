# 🛠️ AI Toolkit

**A robust CLI for bootstrapping and managing AI-powered Python projects.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-82%20passed-brightgreen.svg)](#testing)

---

## 🎯 What is AI Toolkit?

AI Toolkit is a command-line tool that creates Python projects optimized for AI coding assistants. It solves a critical problem: **AI assistants often create `venv/` inside your project**, causing:

- 🐌 **Slow IDEs** — indexing thousands of dependency files
- 🤯 **Confused AI** — reading code from site-packages instead of your code
- 💾 **Bloated repos** — 500+ MB of unnecessary files

**AI Toolkit creates projects with `venv` OUTSIDE the project**, keeping your workspace clean and AI-focused.

---

## ✨ Features

### CLI Commands

| Command | Description |
|---------|-------------|
| `create` | Create new project from templates (bot, webapp, fastapi, parser, full) |
| `cleanup` | Analyze and fix existing projects (move venv, remove pycache) |
| `migrate` | Add AI Toolkit configs to existing projects |
| `health` | Check project configuration status |
| `update` | Update project to latest toolkit version |

### Generators

- **AI Configs** — `.cursorrules`, `.cursorignore`, `CLAUDE.md`, `.windsurfrules`, `.github/copilot-instructions.md`
- **CI/CD** — GitHub Actions workflows, Dependabot, pre-commit hooks
- **Docker** — Dockerfile, docker-compose.yml, .dockerignore
- **Git** — .gitignore, .gitattributes, auto-init repository
- **Scripts** — bootstrap.sh/ps1, health_check.sh, context.py (Context Switcher)
- **Project Files** — requirements.txt, config.py, .env.example, README.md

### Multi-IDE Support

| IDE | Config Files |
|-----|--------------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### Plugin System

Extend functionality with custom plugins:

```python
# ~/.ai_toolkit/plugins/my_plugin/__init__.py
def on_project_created(project_path, project_name):
    print(f"🎉 Project {project_name} created!")
```

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- PyYAML

### From Source

```bash
# Clone repository
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Install dependencies
pip install pyyaml

# Run
python3 main.py
```

---

## 🚀 Usage

### Interactive Mode

```bash
python3 main.py
```

This launches the interactive CLI where you can:
1. Select your IDE (Cursor, Copilot, Claude, Windsurf, or All)
2. Choose an action from the menu
3. Follow the prompts

### CLI Mode

```bash
# Create a new Telegram bot project
python3 main.py create my_bot --template bot

# Create a FastAPI project with Docker
python3 main.py create my_api --template fastapi

# Cleanup an existing project
python3 main.py cleanup ./old_project --level medium

# Health check
python3 main.py health ./my_project

# Migrate existing project
python3 main.py migrate ./existing_project
```

### After Project Creation

```bash
cd my_project

# Create venv OUTSIDE the project
./scripts/bootstrap.sh

# Activate venv
source ../_venvs/my_project-venv/bin/activate

# Configure environment
cp .env.example .env

# Run
python main.py
```

---

## 📁 Project Structure

```
ai_toolkit/
├── main.py                 # Entry point
├── src/
│   ├── cli.py              # Interactive & CLI mode
│   ├── commands/           # CLI commands
│   │   ├── create.py       # Project creation
│   │   ├── cleanup.py      # Project cleanup
│   │   ├── migrate.py      # Migration to toolkit
│   │   ├── health.py       # Health checks
│   │   └── update.py       # Version updates
│   ├── generators/         # File generators
│   │   ├── ai_configs.py   # AI IDE configs
│   │   ├── ci_cd.py        # GitHub Actions
│   │   ├── docker.py       # Docker files
│   │   ├── git.py          # Git setup
│   │   ├── project_files.py # Project files
│   │   └── scripts.py      # Shell scripts
│   └── core/               # Core utilities
│       ├── config.py       # Configuration
│       ├── constants.py    # Constants & colors
│       └── file_utils.py   # File operations
├── templates/              # Project templates
│   ├── bot/                # Telegram bot
│   ├── webapp/             # Web application
│   ├── fastapi/            # REST API
│   └── parser/             # Web scraper
├── plugins/                # Plugin system
│   └── manager.py          # Plugin manager
├── tests/                  # Test suite (82 tests)
└── docs/                   # Documentation
```

---

## 🧪 Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_create.py -v

# Run with short output
python3 -m pytest tests/ --tb=short
```

**Current Status:** ✅ 82/82 tests passing

---

## 🚀 Roadmap

### Phase 1: Foundation ✅ *Completed*

- [x] Core CLI architecture
- [x] Project creation with 5 templates (bot, webapp, fastapi, parser, full)
- [x] Multi-IDE support (Cursor, Copilot, Claude, Windsurf)
- [x] Plugin system with hooks
- [x] Docker & CI/CD generation
- [x] Cleanup, migrate, health, update commands
- [x] Comprehensive test suite (82 tests)

### Phase 2: Optimization 🔄 *Current*

- [ ] Full English localization (i18n cleanup)
- [ ] Token usage optimization for AI context
- [ ] Context Map auto-generation (`generate_map.py`)
- [ ] Pre-commit hook integration
- [ ] Documentation improvements

### Phase 3: Advanced Features 📋 *Next*

- [ ] Advanced AI Agent templates
- [ ] Cursor-specific integration patterns
- [ ] Web UI dashboard
- [ ] Monorepo support
- [ ] Custom template creation wizard
- [ ] Plugin marketplace

---

## 🔧 Configuration

### toolkit.yaml

```yaml
version: "3.0.0"
paths:
  venvs: "../_venvs"
  data: "../_data"
defaults:
  template: bot
  ide: all
  docker: true
  ci: true
```

### Environment Variables

Projects created with AI Toolkit use `.env` files:

```bash
# .env.example
BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///./data.db
DEBUG=false
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Run tests: `python3 -m pytest tests/ -v`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

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
