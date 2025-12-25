# 🚀 AI Toolkit — AI-Native Project Scaffolding

<div align="center">

[![Version](https://img.shields.io/badge/version-3.5-blue.svg)](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-220%20passed-brightgreen.svg)](tests/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AI-Ready](https://img.shields.io/badge/AI-Ready-purple.svg)](#-ai-assistant-support)

**Create projects optimized for AI-assisted development in seconds.**

*Stop wasting tokens on venv garbage. Start building.*

[Quick Start](#-quick-start) •
[Features](#-features) •
[Commands](#-commands) •
[Roadmap](#-roadmap) •
[Documentation](#-documentation)

</div>

---

## 🎯 The Problem

Every AI coding assistant (Cursor, Copilot, Claude, Windsurf) has the same problem:

```
Your project: 50 files of actual code
AI context:   5,000,000 tokens of venv garbage
Result:       Slow, expensive, hallucinating AI
```

**AI Toolkit solves this.** One command creates a clean, optimized project structure that AI assistants actually understand.

---

## ✨ Features

### 🏗️ Project Creation

| Feature | Description |
|---------|-------------|
| 6 Templates | `bot`, `webapp`, `fastapi`, `parser`, `full`, `monorepo` |
| Multi-IDE Support | Cursor, VS Code + Copilot, Claude, Windsurf |
| External venv | Dependencies live outside project (`../_venvs/`) |
| Smart .cursorignore | AI never sees garbage again |
| Bootstrap Scripts | One command setup on any machine |

### 🦊 The Fox Update (v3.3) — Token Optimization

| Feature | Command | What It Does |
|---------|---------|--------------|
| 🧠 AST Map | `generate_map.py` | Parse Python with `ast`, not regex |
| 🦊 Secret Scanner | `review` | Detect API keys, tokens, secrets |
| 📦 XML Packer | `pack` | Export context in XML for AI |
| 🔍 Fox Trace | `trace` | Follow imports, extract only needed code |

**Result:** 5.1M tokens → 13K tokens (99% reduction!)

### 🏥 The Doctor Update (v3.4) — One-Button Fix

| Feature | Command | What It Does |
|---------|---------|--------------|
| 🏥 Doctor | `doctor --auto` | Diagnose + fix ALL issues automatically |
| 📊 Status | `status` | Auto-generate PROJECT_STATUS.md |
| Auto-Update | `generate_map.py` | Updates context map AND status |

### 🧹 Deep Clean & Bridge (v3.5) — Ultimate Token Optimization

| Feature | Command | What It Does |
|---------|---------|--------------|
| 🧹 Deep Clean | `doctor --deep-clean` | Move ALL heavy files + auto-patch code |
| 🔄 Restore | `doctor --restore` | Restore project to original state |
| 📊 Threshold | `--threshold 500` | Custom token threshold |
| 👁️ Preview | `--dry-run` | Preview changes without applying |

**Result:** 5.1M tokens → 47K tokens (99% reduction!) + AI Navigation Map

---

## 🚀 Quick Start

### Installation

```bash
# Option 1: From source (recommended for development)
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Create external venv (following our own philosophy!)
python -m venv ../_venvs/ai-toolkit-main
source ../_venvs/ai-toolkit-main/bin/activate  # Linux/Mac
# or
..\_venvs\ai-toolkit-main\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Option 2: pipx (isolated, recommended for users)
pipx install git+https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git

# Option 3: pip with extras
pip install "git+https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git[dev]"

# Future (after PyPI release - Phase 5)
pip install ai-toolkit           # Basic
pip install ai-toolkit[tui]      # With TUI dashboard
pip install ai-toolkit[web]      # With Web UI
pip install ai-toolkit[all]      # Everything
```

### Create Your First Project

```bash
# Interactive mode
python main.py

# Or direct command
python main.py create my_awesome_bot --template bot

# Then bootstrap your new project
cd my_awesome_bot
./scripts/bootstrap.sh  # Linux/Mac
# or
.\scripts\bootstrap.ps1  # Windows
```

### Fix an Existing Project

```bash
# See what's wrong
python main.py doctor /path/to/messy/project --report

# Fix everything with one command
python main.py doctor /path/to/messy/project --auto
```

---

## 📋 Commands

### Core Commands (12 total)

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Generate new AI-optimized project | `python main.py create mybot --template bot` |
| `cleanup` | Analyze and fix project garbage | `python main.py cleanup ./project --level medium` |
| `migrate` | Add Toolkit to existing project | `python main.py migrate ./old_project` |
| `health` | Health check (find problems) | `python main.py health ./project` |
| `update` | Update toolkit configs | `python main.py update ./project` |
| `wizard` | Interactive project wizard | `python main.py wizard` |

### 🦊 Fox Commands (Token Optimization)

| Command | Description | Example |
|---------|-------------|---------|
| `trace` | 🔍 AST dependency tracker | `python main.py trace src/main.py --depth 2` |
| `pack` | 📦 XML context packer | `python main.py pack src/handlers/ --output context.xml` |
| `review` | 🦊 Security scanner (secrets) | `python main.py review ./project` |

### 🏥 Doctor Commands

| Command | Description | Example |
|---------|-------------|---------|
| `doctor` | Diagnose + auto-fix issues | `python main.py doctor ./project --auto` |
| `doctor --deep-clean` | 🧹 Move heavy files + patch code | `python main.py doctor ./project --deep-clean` |
| `doctor --restore` | 🔄 Restore from deep clean | `python main.py doctor ./project --restore` |
| `status` | Regenerate PROJECT_STATUS.md | `python main.py status . --preview` |
| `hooks` | Git pre-commit hook management | `python main.py hooks install` |

---

## 🤖 AI Assistant Support

AI Toolkit generates configuration files for all major AI coding assistants:

| Assistant | Config File | Purpose |
|-----------|-------------|---------|
| **Cursor** | `.cursorrules` | AI behavior rules |
| **Cursor** | `.cursorignore` | Files to exclude from AI |
| **Cursor** | `.cursor/rules/*.md` | Modular context rules |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Copilot instructions |
| **Claude** | `CLAUDE.md` | Claude-specific instructions |
| **Windsurf** | `.windsurfrules` | Windsurf configuration |
| **All** | `_AI_INCLUDE/` | Shared rules for any AI |

---

## 📁 Generated Project Structure

```
my_project/
├── .cursor/
│   └── rules/
│       └── project.md          # Cursor rules
├── .github/
│   ├── copilot-instructions.md # Copilot rules
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       └── cd.yml              # CD pipeline
├── _AI_INCLUDE/
│   ├── PROJECT_CONVENTIONS.md  # Coding standards
│   └── WHERE_THINGS_LIVE.md    # Location guide
├── scripts/
│   ├── bootstrap.sh            # Linux/Mac setup
│   ├── bootstrap.ps1           # Windows setup
│   └── context.py              # Context switcher
├── src/
│   └── ...                     # Your code here
├── .cursorrules                # Main Cursor config
├── .cursorignore               # Smart ignore patterns
├── .windsurfrules              # Windsurf config
├── CLAUDE.md                   # Claude instructions
├── Dockerfile                  # Container config
├── docker-compose.yml          # Multi-container setup
└── requirements.txt            # Dependencies

# External (not in project):
../_venvs/my_project-main/      # Virtual environment
../_artifacts/my_project/logs/  # Archived logs
../_data/my_project/            # Large data files
```

---

## 📊 Project Templates

| Template | Description | Includes |
|----------|-------------|----------|
| `bot` | Telegram bot (aiogram) | handlers, keyboards, middlewares, FSM |
| `webapp` | Web application | HTML, CSS, JS, Telegram WebApp SDK |
| `fastapi` | REST API | FastAPI, routers, schemas, CRUD |
| `parser` | Web scraper | httpx, BeautifulSoup, async |
| `full` | All modules | bot + webapp + api + parser + database |
| `monorepo` | Multi-project | Shared libraries, multiple services |

---

## 🦊 Fox Trace — Deep Dive Technology

Fox Trace is our implementation of "Deep Dive" (similar to Windsurf's Cascade):

```bash
# You want to refactor payment.py
# Old way: paste entire project → 5M tokens

# Fox Trace way:
python main.py trace src/handlers/payment.py --depth 2
```

**What happens:**
1. Parse `payment.py` with AST
2. Find all imports: `from utils import calculate_tax`
3. Go to `src/utils.py`
4. Extract ONLY `calculate_tax` function (not entire file!)
5. Package into XML with proper context

**Result:**
```xml
<context_dump>
  <file path="src/handlers/payment.py">
    def pay():
        tax = calculate_tax(100)
        ...
  </file>
  
  <dependency path="src/utils.py" source="trace">
    def calculate_tax(amount):
        return amount * 0.2
  </dependency>
</context_dump>
```

**Token savings:** 5.1M → 13K (99.7% reduction)

---

## 🏥 Doctor — One-Button Project Fix

The Doctor command diagnoses and fixes ALL project issues automatically:

```bash
python main.py doctor /path/to/project --auto
```

**What it detects:**
- 🔴 CRITICAL: venv inside project, node_modules
- 🟡 WARNING: `__pycache__`, logs, large data files
- 🟢 SUGGESTION: missing configs, outdated files

**What it fixes:**
1. Creates backup (`.tar.gz`)
2. Deletes venv/pycache/logs
3. Moves large files to `../_data/`
4. Creates `_AI_INCLUDE/` folder
5. Generates `.cursorignore`
6. Creates bootstrap scripts
7. Sets up external venv
8. Shows before/after comparison

**Example output:**
```
╔══════════════════════════════════════════════════════════════════╗
║  ✅ DOCTOR COMPLETE — All issues fixed!                         ║
╠══════════════════════════════════════════════════════════════════╣
║                      BEFORE           AFTER                      ║
║  Tokens:            5.1M     →       47K    (99% reduction!)     ║
║  Critical:             3     →         0                         ║
║  Warnings:             2     →         0                         ║
╠══════════════════════════════════════════════════════════════════╣
║  📦 Backup: my_project_backup_20241223.tar.gz                    ║
║  🌐 Venv: ../_venvs/my_project-main                              ║
║                                                                  ║
║  Your project is now AI-ready! 🚀                                ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🧹 Deep Clean & Bridge — Ultimate Token Optimization

**NEW in v3.5!** The most powerful feature — automatically move heavy files AND patch your code!

```bash
# Preview what will be cleaned (dry run)
python main.py doctor /path/to/project --deep-clean --dry-run

# Full automatic deep clean
python main.py doctor /path/to/project --deep-clean --auto

# Custom threshold (default: 1000 tokens)
python main.py doctor /path/to/project --deep-clean --threshold 500

# Restore to original state
python main.py doctor /path/to/project --restore
```

### How Deep Clean Works

```
BEFORE Deep Clean:                    AFTER Deep Clean:
─────────────────────                ─────────────────────
my_bot/                              my_bot/
├── data/                            ├── config_paths.py      ← Bridge
│   ├── products.json (50K tok)      ├── AST_FOX_TRACE.md     ← AI Map
│   └── users.csv (100K tok)         ├── .cursor/rules/
├── handlers/                        │   └── external_data.md
│   └── shop.py                      ├── handlers/
└── main.py                          │   └── shop.py          ← Patched!
                                     └── main.py
Total: 160K tokens
                                     ../_data/my_bot/LARGE_TOKENS/
                                     ├── data/products.json
                                     └── data/users.csv
                                     
                                     Total: 10K tokens (94% reduction!)
```

### What Gets Generated

| File | Purpose |
|------|---------|
| `config_paths.py` | Bridge to external files with `get_path()` |
| `AST_FOX_TRACE.md` | Navigation map showing schemas WITHOUT data |
| `.cursor/rules/external_data.md` | Compact context for Cursor AI |
| `manifest.json` | Recovery info (in external storage) |

### Code Auto-Patching

Deep Clean automatically updates your Python code:

```python
# BEFORE
with open("data/products.json") as f:
    data = json.load(f)

# AFTER (auto-patched!)
from config_paths import get_path
with open(get_path("data/products.json")) as f:
    data = json.load(f)
```

**Supported patterns:**
- `open("file.json")` → `open(get_path("file.json"))`
- `Path("file.csv")` → `get_path("file.csv")`
- `pd.read_csv("file.csv")` → `pd.read_csv(get_path("file.csv"))`
- `sqlite3.connect("db.sqlite")` → `sqlite3.connect(get_path("db.sqlite"))`

### AST_FOX_TRACE.md — AI Navigation Map

Instead of loading 50K tokens of data, AI reads a 500-token map:

```markdown
## 📦 data/products.json

**Tokens:** ~50K
**External:** `../_data/my_bot/LARGE_TOKENS/data/products.json`

**Schema (structure only, no data):**
- type: array (1500 items)
- fields: {id: integer, name: string, price: number}

**Used in:**
- `handlers/shop.py:23` — `products = json.load(...)`
```

Now when you ask Cursor *"How does the buy button work?"*, it reads the schema and understands WITHOUT loading the actual 50K-token file!

---

## 🗺️ Roadmap

### ✅ Completed

| Version | Name | Features |
|---------|------|----------|
| v3.0 | Core | CLI, 6 templates, multi-IDE, Docker, CI/CD |
| v3.3 | The Fox Update | AST Map, Fox Trace, XML Packer, Secret Scanner |
| v3.4 | The Doctor Update | Doctor command, Status generator, Auto-update |
| v3.5 | Deep Clean & Bridge | Heavy file mover, Code auto-patcher, AI navigation map |

### 🔄 In Progress

| Version | Name | Features | Status |
|---------|------|----------|--------|
| v3.6 | CLI Wizard | Questionary prompts, natural language, skill levels | 🔄 Partial |

### ⬜ Planned

| Version | Name | Features | Timeline |
|---------|------|----------|----------|
| v3.7 | TUI Dashboard | Textual full-screen UI, live tokens, keyboard nav | Week 4-5 |
| v3.8 | Automation | Diff export, pre-commit integration, deps graph | Week 6-7 |
| v3.9 | Quality & PyPI | 80% test coverage, mypy, `pip install ai-toolkit` | Week 8-9 |
| v4.0 | Web UI | Browser dashboard, drag & drop, visual wizards | Week 10-13 |

### 💡 Future Ideas

| Version | Name | Features |
|---------|------|----------|
| v4.1+ | Extensions | Plugin system, custom templates |
| v4.1+ | IDE Plugin | VS Code/Cursor extension |
| v4.1+ | GUI Desktop | Tkinter/PyQt application |
| v4.1+ | Telegram Bot | @AIToolkitBot for quick actions |
| v4.1+ | Auto-context | AI-driven focus detection |
| v4.1+ | Cost Dashboard | Track AI spending per project |
| v4.2 | Localization | Full RU/EN support, i18n framework |
| v4.2 | RU Documentation | README, guides, PROMPTS_LIBRARY in Russian |

### 📈 Feature Progress

```
v3.0  ████████████████████████████████████████ 54 features (Core)
v3.3  ████████████████████████████████████████████ 62 features (+Fox Update)
v3.4  ██████████████████████████████████████████████ 68 features (+Doctor)
v3.5  ████████████████████████████████████████████████ 76 features (+Deep Clean)
      ─────────────────────────────────────────────────────────────────
v3.7  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 84 (+TUI)
v4.0  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 98 (+Web)
v4.2  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 110 (Full)
      ─────────────────────────────────────────────────────────────────
      0%              25%              50%              75%         100%
      
Current: 76/110 features (69%)
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | This file — overview and quick start |
| [CLAUDE.md](CLAUDE.md) | Instructions for Claude AI |
| [PROMPTS_LIBRARY.md](PROMPTS_LIBRARY.md) | Ready-to-use prompts for AI |
| [TRADEOFFS.md](TRADEOFFS.md) | Architectural decisions explained |
| [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md) | Full roadmap and specs |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [first manifesto.md](first%20manifesto.md) | Philosophy and core rules |

### Auto-Generated Docs

| Document | Purpose | Command |
|----------|---------|---------|
| [CURRENT_CONTEXT_MAP.md](CURRENT_CONTEXT_MAP.md) | Code structure map | `python generate_map.py` |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Implementation status | `python main.py status` |

---

## 🏗️ Architecture

```
AI-Native_Project_Scaffolding/
├── src/
│   ├── commands/           # CLI commands (12 total)
│   │   ├── create.py       # Project creation
│   │   ├── cleanup.py      # Project cleanup
│   │   ├── doctor.py       # 🏥 Diagnose & fix + Deep Clean
│   │   ├── trace.py        # 🔍 AST dependency tracker
│   │   ├── pack.py         # 📦 XML context packer
│   │   ├── review.py       # 🦊 Secret scanner
│   │   └── ...
│   ├── generators/         # File generators (6 total)
│   │   ├── ai_configs.py   # AI assistant configs
│   │   ├── scripts.py      # Bootstrap scripts
│   │   ├── docker.py       # Docker files
│   │   └── ...
│   ├── utils/              # Utilities (9 total)
│   │   ├── context_map.py     # 🧠 AST code mapping
│   │   ├── metrics.py         # Token scanning
│   │   ├── status_generator.py # Auto-status
│   │   ├── schema_extractor.py # 📊 JSON/CSV/SQLite schema
│   │   ├── token_scanner.py    # 🔍 Find heavy files
│   │   ├── heavy_mover.py      # 📦 Move + generate bridges
│   │   ├── ast_patcher.py      # 🔧 Auto-refactor code
│   │   ├── fox_trace_map.py    # 🦊 AI navigation map
│   │   └── cleaner.py          # 🧹 Archive garbage
│   └── core/               # Core modules
│       ├── constants.py    # Templates, patterns
│       └── config.py       # Configuration
├── templates/              # Project templates
├── tests/                  # 220 tests
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_doctor.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

**Current status:** 220 tests passing ✅

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Setup development environment
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
python -m venv ../_venvs/ai-toolkit-dev
source ../_venvs/ai-toolkit-dev/bin/activate
pip install -e ".[dev]"

# Run tests before submitting
pytest tests/ -v
mypy src/
ruff check src/
```

---

## 📜 Philosophy

> **"The project must remain clean for the AI assistant"**

Three fundamental rules:
1. **Never create venv inside project** — 500MB of garbage kills AI performance
2. **Never read large files entirely** — logs, CSVs destroy context window
3. **Always check before creating** — read `_AI_INCLUDE/` first

See [first manifesto.md](first%20manifesto.md) for the complete philosophy.

---

## 📈 Progress Summary

```
OVERALL PROGRESS
════════════════════════════════════════════════════════════════════

Phase 0: Core Foundation        ████████████████████████████ 100% ✅
Phase 1: Foundation (v3.1)      ████████████████████████████ 100% ✅
Phase 2: CLI Wizard (v3.2)      ████████████████████████████ 100% ✅
Phase 2.5: Fox Update (v3.3)    ████████████████████████████ 100% ✅
Phase 2.6: Doctor Update (v3.4) ████████████████████████████ 100% ✅
Phase 2.7: Deep Clean (v3.5)    ████████████████████████████ 100% ✅
Phase 3: TUI Dashboard (v3.7)   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 4: Automation (v3.8)      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 5: Quality & PyPI (v3.9)  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 6: Web UI (v4.0)          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% ⬜
Phase 7: Extensions (v4.1+)     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% 💡
Phase 8: Localization (v4.2)    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% 💡

════════════════════════════════════════════════════════════════════
TOTAL: 76/110 features (69%) | Next: Phase 3 (TUI Dashboard)
```

### 📊 Statistics

| Metric | Current | Target |
|--------|---------|--------|
| Features Implemented | 76 | 110 |
| Commands | 12 | 15+ |
| Utilities | 9 | 12+ |
| Tests Passing | 220 | 250+ |
| Templates | 6 | 10+ |
| Supported IDEs | 5 | 5 |
| Interfaces | CLI | CLI + TUI + Web |
| Languages | EN | EN + RU |

### Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🔄 | In Progress |
| ⬜ | Planned |
| 💡 | Future Idea |

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for:
- Supported versions
- How to report vulnerabilities
- Security best practices

---

## 💬 Support

- 🐛 [Open an Issue](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 [Discussions](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)
- 📧 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)

---

## 👥 Team

**Mickhael** — Project Creator & Lead Developer
- Original vision
- Architecture decisions
- Business requirements

**Claude (Anthropic)** — AI Development Partner
- Technical specification
- Code implementation
- Documentation

> *"This project was developed with significant assistance from my good colleague Claude (Anthropic)."*
> *"P.S. and Grok, Gemini too ^_^"*

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with 🤝 by Mickhael & Claude**

*December 2024*

[⬆ Back to Top](#-ai-toolkit--ai-native-project-scaffolding)

</div>
