# 🛠️ AI-Native Project Scaffolding v3.0

<div align="center">

**Create AI-friendly Python projects in seconds**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg?style=for-the-badge)](tests/)
[![Typed](https://img.shields.io/badge/typed-mypy-blue.svg?style=for-the-badge)](src/py.typed)

[🚀 Quick Start](#-quick-start) •
[📖 Documentation](#-documentation) •
[🌐 Web Dashboard](#-web-dashboard) •
[🇷🇺 Русская версия](README.ru.md)

</div>

---

## 🌍 Languages / Языки

This tool supports **English** and **Russian**:
- 🇬🇧 CLI and Dashboard in English
- 🇷🇺 CLI и Dashboard на русском
- Language selection on first launch
- Language switcher in Web Dashboard

---

## 🎯 What is this?

**AI-Native Project Scaffolding** is a tool for creating Python projects optimized for AI assistants:

| IDE | Description | Config Files |
|-----|-------------|--------------|
| 💜 **Cursor** | AI-first IDE based on VS Code | `.cursorrules`, `.cursorignore` |
| 💙 **GitHub Copilot** | AI assistant in VS Code | `.github/copilot-instructions.md` |
| 🟢 **Claude** | Anthropic Claude | `CLAUDE.md` |
| 🌊 **Windsurf** | Codeium IDE | `.windsurfrules` |

---

## ❌ The Problem

When AI assistants work with your project, they often create `venv/` inside the project folder:

```
my_project/
├── venv/              ← 500 MB of junk! 😱
│   ├── lib/
│   │   └── python3.12/
│   │       └── site-packages/  ← 10,000+ files
│   └── ...
├── main.py
└── ...
```

**Result:**
- 🐌 IDE becomes slow — indexing thousands of files
- 🤯 AI gets confused — reading code from dependencies
- 💾 Repository bloats — 500+ MB
- 🔄 Git issues — too many unnecessary files

---

## ✅ The Solution

AI-Native Project Scaffolding creates projects with **venv OUTSIDE the project**:

```
projects/
├── _venvs/                      ← All venvs here!
│   ├── my_project-venv/
│   └── another_project-venv/
│
├── my_project/                  ← Clean project!
│   ├── _AI_INCLUDE/             ← Rules for AI
│   ├── scripts/
│   │   └── bootstrap.sh         ← Creates venv outside
│   └── main.py
```

**Result:**
- 🚀 IDE works fast
- 🧠 AI understands only your code
- 📦 Project is lightweight
- ✅ Git stays clean

---

## 🚀 Quick Start

### Installation

```bash
# From PyPI (recommended)
pip install ai-toolkit

# With Web Dashboard
pip install ai-toolkit[web]
```

### Installation from Source (One Command!)

```bash
# 1. Clone the repository
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git

# 2. Go to project folder  
cd AI-Native_Project_Scaffolding

# 3. Run ONE command to install and start! 🚀
# Windows:
.\start.ps1

# Linux/macOS:
./start.sh
```

The script will:
1. ✅ Check Python version
2. ✅ Install dependencies automatically
3. ✅ Start Web Dashboard
4. ✅ Open browser with Welcome screen

> 💡 **First launch:** You'll see a Welcome screen to select language (English/Russian).

#### Manual Installation (alternative)

```bash
# Install with dependencies
pip install -e ".[web]"

# Run
python -m web.app          # Web Dashboard
python -m src.cli          # Interactive CLI
```

> ⚠️ **Important:** After installation from source, run commands from the `AI-Native_Project_Scaffolding` folder!

### If `ai-toolkit` command doesn't work

On Windows, you may need to add Scripts to PATH:

```powershell
# Check where scripts are installed
pip show ai-toolkit

# Add to PATH (replace with your path)
$env:PATH += ";C:\Users\YourName\AppData\Roaming\Python\Python312\Scripts"

# Now this works:
ai-toolkit dashboard
```

Or just use Python module syntax:

```bash
python -m src.cli              # CLI
python -m web.app              # Dashboard
python -m web.app --port 3000  # Dashboard on different port
```

### Create Your First Project

**Option 1: Web Dashboard** (easiest)

```bash
ai-toolkit dashboard
```

A beautiful web interface opens in your browser.

**Option 2: Interactive mode**

```bash
ai-toolkit
```

**Option 3: Single command**

```bash
ai-toolkit create my_bot --template bot
```

### After Project Creation

```bash
cd my_bot

# Create venv OUTSIDE the project
./scripts/bootstrap.sh

# Activate venv
source ../_venvs/my_bot-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Run
python main.py
```

---

## 🌐 Web Dashboard

The easiest way to use the toolkit — through a web interface:

```bash
ai-toolkit dashboard
```

### Dashboard Features:

| Page | Functions |
|------|-----------|
| 🏠 **Home** | Project statistics, quick actions |
| 🆕 **Create** | Visual project builder with template selection |
| 🧹 **Cleanup** | Analyze issues + safe fixes |
| 🏥 **Health** | Check settings + migration + update |
| ⚙️ **Settings** | Default IDE selection |
| ❓ **Help** | Detailed documentation for beginners |

### Features:

- 🎨 Beautiful dark design with animations
- 🌍 **Language switcher** (🇬🇧 EN / 🇷🇺 RU)
- 📱 Responsive — works on mobile
- 🔒 Runs locally (127.0.0.1)
- 📋 "Copy" buttons for commands

---

## 💻 Usage Options

### 1. Web Dashboard (for everyone)

```bash
ai-toolkit dashboard
# or
ai-toolkit web
```

### 2. GUI mode (Tkinter)

```bash
ai-toolkit-gui
# or
python -m gui.app
```

### 3. Interactive CLI

```bash
ai-toolkit
# or
aitk
```

**On first launch — language selection:**

```
═══════════════════════════════════════════════════════════
🛠️  AI-NATIVE PROJECT SCAFFOLDING v3.0
═══════════════════════════════════════════════════════════

🌍 Select language / Выберите язык:

  1. 🇬🇧 English
  2. 🇷🇺 Русский

Choice / Выбор (1-2) [1]: 
```

**Then IDE selection and main menu:**

```
🖥️  Which IDE will you use?

  1. 💜 Cursor (AI-first IDE)
  2. 💙 VS Code + GitHub Copilot
  3. 🟢 VS Code + Claude
  4. 🌊 Windsurf
  5. 🔄 All (universal)

Choose (1-5) [5]: 5

What would you like to do?

  1. 🆕 Create new project
  2. 🧹 Cleanup existing project
  3. 📦 Migrate project
  4. 🏥 Health check
  5. ⬆️  Update project
  6. ⚙️  Change IDE
  7. 🌍 Change language
  0. ❌ Exit
```

### 4. CLI commands

```bash
# Create project
ai-toolkit create my_bot --template bot --ai cursor copilot

# Cleanup dirty project
ai-toolkit cleanup ./old_project --level medium

# Health check
ai-toolkit health ./my_project

# Migrate existing project
ai-toolkit migrate ./existing_project

# Update to new version
ai-toolkit update ./my_project

# Set language via CLI
ai-toolkit --lang en
ai-toolkit --lang ru
```

---

## 📦 Project Templates

| Template | Description | What's Created |
|----------|-------------|----------------|
| 🤖 `bot` | Telegram bot | aiogram 3.x, handlers, keyboards, database |
| 🌐 `webapp` | Telegram Mini App | HTML/CSS/JS, API endpoints |
| ⚡ `fastapi` | REST API | FastAPI, SQLAlchemy, Alembic |
| 🕷️ `parser` | Web scraper | aiohttp, BeautifulSoup, database |
| 🚀 `full` | Everything together | bot + webapp + api + parser |
| 📦 `monorepo` | Multiple projects | apps/, packages/, shared/ |

### Example: creating Telegram bot

```bash
# Create project
ai-toolkit create my_telegram_bot --template bot

# Go to project
cd my_telegram_bot

# Create venv
./scripts/bootstrap.sh

# Activate
source ../_venvs/my_telegram_bot-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env
nano .env  # Add BOT_TOKEN

# Run
python main.py
```

---

## 🛡️ All Features

### Project Creation

| Feature | Description |
|---------|-------------|
| 🆕 **Creation** | 6 project templates |
| 🐳 **Docker** | Dockerfile + docker-compose.yml |
| 🚀 **CI/CD** | GitHub Actions (lint, test, deploy) |
| 🔗 **Git** | Automatic init + .gitignore + first commit |
| 🔒 **pre-commit** | Hooks to protect from venv in project |

### Working with Existing Projects

| Feature | Description |
|---------|-------------|
| 🧹 **Cleanup** | Analyze issues + move venv + create configs |
| 📦 **Migration** | Add AI Toolkit to existing project |
| 🏥 **Health check** | Verify correct setup |
| ⬆️ **Update** | Update to new Toolkit version |

### Tools

| Feature | Description |
|---------|-------------|
| 🎮 **Context Switcher** | Hide modules from AI for focus |
| 🔌 **Plugins** | Extend functionality |
| 🌐 **Dashboard** | Web interface with language switcher |
| 🖥️ **GUI** | Graphical interface (Tkinter) |
| 🌍 **Localization** | English + Russian |

---

## 📁 Created Project Structure

```
my_project/
│
├── 📚 _AI_INCLUDE/              # Rules for AI
│   ├── PROJECT_CONVENTIONS.md   # Architecture, restrictions
│   └── WHERE_IS_WHAT.md         # Project map
│
├── 🤖 AI configs
│   ├── .cursorrules             # Cursor
│   ├── .cursorignore            # Cursor (exclusions)
│   ├── CLAUDE.md                # Claude
│   └── .windsurfrules           # Windsurf
│
├── 📁 .github/
│   ├── copilot-instructions.md  # GitHub Copilot
│   ├── dependabot.yml           # Auto-update dependencies
│   └── workflows/
│       ├── ci.yml               # Tests, lint
│       └── cd.yml               # Deploy
│
├── 🔧 scripts/
│   ├── bootstrap.sh             # Creates venv OUTSIDE project
│   ├── bootstrap.ps1            # Windows version
│   ├── health_check.sh          # Check settings
│   ├── check_repo_clean.sh      # pre-commit hook
│   └── context.py               # Context Switcher
│
├── 🤖 bot/                      # Bot code (bot template)
│   ├── __init__.py
│   ├── main.py
│   ├── handlers/
│   └── keyboards/
│
├── 💾 database/                 # Database
├── 🌐 webapp/                   # Mini App (webapp template)
├── ⚡ api/                      # FastAPI (fastapi template)
├── 🕷️ parser/                   # Scraper (parser template)
│
├── 📂 logs/                     # Logs (in .gitignore)
├── 📂 data/                     # Data (in .gitignore)
├── 🧪 tests/                    # Tests
│
├── 🐳 Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── 📋 Configuration
│   ├── .pre-commit-config.yaml
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── config.py
│   ├── .env.example
│   └── .toolkit-version
│
├── 📖 Git
│   ├── .gitignore
│   └── .gitattributes
│
└── 📖 README.md
```

---

## 🎮 Context Switcher

When AI gets confused on a large project — **hide unnecessary modules**:

```bash
# Focus on bot (hides webapp, api, parser)
python scripts/context.py bot

# Focus on webapp
python scripts/context.py webapp

# Focus on API
python scripts/context.py api

# Show everything
python scripts/context.py all

# Status
python scripts/context.py status
```

**How it works:**
- Updates `.cursorignore`
- AI sees only the needed module
- Rest is temporarily hidden

---

## 🧹 Cleanup Levels

For existing "dirty" projects:

| Level | What it does | Safety |
|-------|--------------|--------|
| `safe` | Analysis only, no changes | ✅ 100% safe |
| `medium` | Backup + move venv + configs | ⚠️ With backup |
| `full` | + move data + restructure | ⚠️ With backup |

```bash
# Just see what's wrong
ai-toolkit cleanup ./project --level safe

# Fix with backup
ai-toolkit cleanup ./project --level medium

# Full restructuring
ai-toolkit cleanup ./project --level full
```

---

## 🔌 Plugins

AI Toolkit supports extending through plugins:

```python
# ~/.ai_toolkit/plugins/my_plugin/__init__.py

def on_project_created(project_path, project_name):
    """Called after project creation"""
    print(f"🎉 Project {project_name} created!")

def on_cleanup_complete(project_path, level):
    """Called after cleanup"""
    pass
```

### Plugin Hooks:

| Hook | When called |
|------|-------------|
| `on_project_created` | After project creation |
| `on_cleanup_complete` | After cleanup |
| `on_migrate_complete` | After migration |
| `on_health_check` | After health check |

---

## 🧪 Development

### Setup for Development

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Create venv
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev,web]"
```

### Testing

```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Only fast tests
pytest -m "not slow"
```

### Code Checking

```bash
# Types
mypy src

# Linting
ruff check src

# Formatting
ruff format src
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📖 Full Guide](docs/GUIDE.md) | Detailed guide |
| [❓ FAQ](docs/FAQ.md) | Frequently asked questions |
| [⚡ Quick Start](docs/QUICK_START.md) | Get started in 2 minutes |
| [📋 Changelog](CHANGELOG.md) | Version history |
| [🇷🇺 Russian](README.ru.md) | Russian version |

---

## 📋 Roadmap

- [x] 🆕 Project creation (6 templates)
- [x] 🧹 Dirty project cleanup
- [x] 📦 Existing project migration
- [x] 🏥 Health check
- [x] 🎮 Context Switcher
- [x] 🌐 Web Dashboard
- [x] 🖥️ GUI (Tkinter)
- [x] 🔌 Plugin system
- [x] 🐳 Docker + CI/CD
- [x] 🌍 Localization (EN/RU)
- [ ] 📊 Analytics and reports
- [ ] 🎨 Custom templates
- [ ] 🔐 Secrets manager
- [ ] 🤖 AI assistant in CLI
- [ ] 📦 Plugin marketplace

---

## 🤝 Contributing

We welcome contributions!

1. **Fork** the repository
2. Create **feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. Open **Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT © [Michael Salmin](https://t.me/MichaelSalmin)

See [LICENSE](LICENSE) for details.

---

## 💬 Support

- 🐛 [Open Issue](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 [Discussions](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)
- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)

---

## ⭐ Star History

If this project is useful — give it a star! ⭐

---

<div align="center">

**Made with ❤️ for AI-first development**

[⬆️ Back to top](#️-ai-native-project-scaffolding-v30)

</div>
