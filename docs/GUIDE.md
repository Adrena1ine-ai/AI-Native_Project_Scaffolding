# 📖 AI Toolkit Complete Guide

This guide will help you master AI Toolkit from start to finish.

> 🇷🇺 [Русская версия](GUIDE.ru.md)

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First Project](#first-project)
4. [Interfaces](#interfaces)
5. [Project Templates](#project-templates)
6. [Working with venv](#working-with-venv)
7. [AI Configuration](#ai-configuration)
8. [Context Switcher](#context-switcher)
9. [Project Cleanup](#project-cleanup)
10. [Migration](#migration)
11. [Docker and CI/CD](#docker-and-cicd)
12. [Plugins](#plugins)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is AI Toolkit?

AI Toolkit is a tool for creating Python projects optimized for AI assistants (Cursor, GitHub Copilot, Claude, Windsurf).

### Why is this needed?

When an AI assistant works with a project, it reads ALL files. If `venv/` is inside the project:

- 📦 AI indexes 500+ MB of dependencies
- 🐌 IDE slows down
- 🤯 AI gets confused reading library code
- 💾 Repository bloats

**Solution:** AI Toolkit creates projects with venv OUTSIDE the project and special configs for AI.

---

## Installation

### Requirements

- Python 3.10 or higher
- pip

### 🚀 One-Command Start (Recommended)

The easiest way to get started:

```bash
# Download
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Run ONE command!
# Windows:
.\start.ps1

# Linux/macOS:
./start.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install dependencies
3. ✅ Launch Web Dashboard
4. ✅ Open browser with Welcome screen

### Via pip

```bash
# Basic installation
pip install ai-toolkit

# With Web Dashboard
pip install ai-toolkit[web]
```

### Manual from source

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
```

### Verify installation

```bash
ai-toolkit --version
# or
python -m web.app --help
```

---

## First Project

### Interactive mode

```bash
ai-toolkit
```

1. Select language (🇬🇧 English / 🇷🇺 Русский)
2. Choose your IDE
3. Select "Create new project"
4. Enter project name
5. Choose template
6. Done! 🎉

### CLI mode

```bash
ai-toolkit create my_bot --template bot --path ~/projects
```

### Next steps after creation

```bash
cd ~/projects/my_bot
./scripts/bootstrap.sh
source ../_venvs/my_bot-venv/bin/activate
cp .env.example .env
```

---

## Interfaces

### CLI (Command Line)

```bash
# Interactive mode
ai-toolkit

# Create project
ai-toolkit create my_bot

# Cleanup
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project
```

### Web Dashboard

```bash
ai-toolkit dashboard
# or
ai-toolkit web
```

Opens a beautiful web interface at http://127.0.0.1:8080

### GUI (Tkinter)

```bash
python -m gui.app
```

---

## Project Templates

| Template | Description | Includes |
|----------|-------------|----------|
| `bot` | Telegram Bot | aiogram 3.x, handlers, FSM |
| `webapp` | Telegram Mini App | HTML/CSS/JS, Telegram Web App API |
| `fastapi` | REST API | FastAPI, Pydantic, async |
| `parser` | Web Scraper | aiohttp, BeautifulSoup |
| `full` | All modules | bot + webapp + parser + API |
| `monorepo` | Multi-project | Shared libs, multiple services |

### Template selection

```bash
# CLI
ai-toolkit create my_project --template fastapi

# Interactive - choose from menu
```

---

## Working with venv

### Why venv outside?

```
projects/
├── _venvs/                 ← All venvs here!
│   ├── bot1-venv/
│   ├── bot2-venv/
│   └── api-venv/
│
├── bot1/                   ← Clean project!
├── bot2/
└── api/
```

**Benefits:**

- ✅ AI sees only your code
- ✅ IDE works fast
- ✅ Repository is lightweight
- ✅ Easy to delete/recreate venv

### bootstrap.sh

The `scripts/bootstrap.sh` script creates venv outside the project:

```bash
./scripts/bootstrap.sh
```

What it does:

1. Creates `../_venvs/project-name-venv/`
2. Installs dependencies from `requirements.txt`
3. Shows activation command

### Activation

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

---

## AI Configuration

### Files for each IDE

| IDE | Files |
|-----|-------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### _AI_INCLUDE folder

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  # Rules: what AI can/can't do
└── WHERE_IS_WHAT.md        # Architecture: where to find what
```

**AI reads these files FIRST** and follows the rules.

### .cursorignore / .gitignore

Prevents AI from indexing unnecessary files:

```
venv/
__pycache__/
*.pyc
.env
logs/
data/
node_modules/
```

---

## Context Switcher

When AI struggles with a large project — hide unnecessary modules!

### Usage

```bash
# Show help
python scripts/context.py

# Hide module from AI
python scripts/context.py hide parser

# Show module again
python scripts/context.py show parser

# List hidden modules
python scripts/context.py list
```

### How it works

The script renames folders to `_hidden_module_name`. Cursor/Copilot ignore files starting with `_`.

---

## Project Cleanup

### Cleanup levels

| Level | Actions |
|-------|---------|
| `safe` | Analysis only, no changes |
| `medium` | Backup + move venv + create configs |
| `full` | + move data + restructure |

### CLI

```bash
# Analysis only
ai-toolkit cleanup ./my_project --level safe

# Move venv + create configs
ai-toolkit cleanup ./my_project --level medium
```

### What is checked

- ❌ venv inside project
- ❌ site-packages in repo
- ⚠️ Large logs (>10MB)
- ⚠️ Large data folder
- ⚠️ __pycache__ folders
- ⚠️ Missing AI configs

---

## Migration

Add AI Toolkit to an existing project:

```bash
ai-toolkit migrate ./my_old_project
```

### What is added

- `_AI_INCLUDE/` folder
- `.cursorrules`, `.cursorignore`
- `CLAUDE.md`
- `scripts/bootstrap.sh`
- `scripts/context.py`
- `.toolkit-version`

---

## Docker and CI/CD

### Docker

```dockerfile
# Dockerfile created automatically
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```bash
# Build and run
docker-compose up --build
```

### GitHub Actions

**CI (ci.yml):**

- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)

**CD (cd.yml):**

- Build on tag push
- Deploy to production

### Dependabot

Auto-updates dependencies weekly.

---

## Plugins

### Plugin structure

```
~/.ai_toolkit/plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

### plugin.py

```python
def on_project_created(project_path: str, template: str) -> None:
    """Called after project creation."""
    print(f"Project created: {project_path}")

def on_cleanup(project_path: str, level: str) -> None:
    """Called after cleanup."""
    pass
```

---

## Troubleshooting

### venv not activating

```bash
# Check if venv exists
ls ../_venvs/

# Recreate
rm -rf ../_venvs/my_project-venv
./scripts/bootstrap.sh
```

### AI still indexes venv

1. Check `.cursorignore` exists
2. Restart IDE
3. Clear IDE cache

### Dashboard won't start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Start manually
python -m web.app
```

### "Module not found" errors

```bash
# Ensure venv is activated
which python
# Should show: ../_venvs/my_project-venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Support

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub Issues: [Report a bug](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Ask a question](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)

This guide will help you master AI Toolkit from start to finish.

> 🇷🇺 [Русская версия](GUIDE.ru.md)

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First Project](#first-project)
4. [Interfaces](#interfaces)
5. [Project Templates](#project-templates)
6. [Working with venv](#working-with-venv)
7. [AI Configuration](#ai-configuration)
8. [Context Switcher](#context-switcher)
9. [Project Cleanup](#project-cleanup)
10. [Migration](#migration)
11. [Docker and CI/CD](#docker-and-cicd)
12. [Plugins](#plugins)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is AI Toolkit?

AI Toolkit is a tool for creating Python projects optimized for AI assistants (Cursor, GitHub Copilot, Claude, Windsurf).

### Why is this needed?

When an AI assistant works with a project, it reads ALL files. If `venv/` is inside the project:

- 📦 AI indexes 500+ MB of dependencies
- 🐌 IDE slows down
- 🤯 AI gets confused reading library code
- 💾 Repository bloats

**Solution:** AI Toolkit creates projects with venv OUTSIDE the project and special configs for AI.

---

## Installation

### Requirements

- Python 3.10 or higher
- pip

### 🚀 One-Command Start (Recommended)

The easiest way to get started:

```bash
# Download
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Run ONE command!
# Windows:
.\start.ps1

# Linux/macOS:
./start.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install dependencies
3. ✅ Launch Web Dashboard
4. ✅ Open browser with Welcome screen

### Via pip

```bash
# Basic installation
pip install ai-toolkit

# With Web Dashboard
pip install ai-toolkit[web]
```

### Manual from source

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
```

### Verify installation

```bash
ai-toolkit --version
# or
python -m web.app --help
```

---

## First Project

### Interactive mode

```bash
ai-toolkit
```

1. Select language (🇬🇧 English / 🇷🇺 Русский)
2. Choose your IDE
3. Select "Create new project"
4. Enter project name
5. Choose template
6. Done! 🎉

### CLI mode

```bash
ai-toolkit create my_bot --template bot --path ~/projects
```

### Next steps after creation

```bash
cd ~/projects/my_bot
./scripts/bootstrap.sh
source ../_venvs/my_bot-venv/bin/activate
cp .env.example .env
```

---

## Interfaces

### CLI (Command Line)

```bash
# Interactive mode
ai-toolkit

# Create project
ai-toolkit create my_bot

# Cleanup
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project
```

### Web Dashboard

```bash
ai-toolkit dashboard
# or
ai-toolkit web
```

Opens a beautiful web interface at http://127.0.0.1:8080

### GUI (Tkinter)

```bash
python -m gui.app
```

---

## Project Templates

| Template | Description | Includes |
|----------|-------------|----------|
| `bot` | Telegram Bot | aiogram 3.x, handlers, FSM |
| `webapp` | Telegram Mini App | HTML/CSS/JS, Telegram Web App API |
| `fastapi` | REST API | FastAPI, Pydantic, async |
| `parser` | Web Scraper | aiohttp, BeautifulSoup |
| `full` | All modules | bot + webapp + parser + API |
| `monorepo` | Multi-project | Shared libs, multiple services |

### Template selection

```bash
# CLI
ai-toolkit create my_project --template fastapi

# Interactive - choose from menu
```

---

## Working with venv

### Why venv outside?

```
projects/
├── _venvs/                 ← All venvs here!
│   ├── bot1-venv/
│   ├── bot2-venv/
│   └── api-venv/
│
├── bot1/                   ← Clean project!
├── bot2/
└── api/
```

**Benefits:**

- ✅ AI sees only your code
- ✅ IDE works fast
- ✅ Repository is lightweight
- ✅ Easy to delete/recreate venv

### bootstrap.sh

The `scripts/bootstrap.sh` script creates venv outside the project:

```bash
./scripts/bootstrap.sh
```

What it does:

1. Creates `../_venvs/project-name-venv/`
2. Installs dependencies from `requirements.txt`
3. Shows activation command

### Activation

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

---

## AI Configuration

### Files for each IDE

| IDE | Files |
|-----|-------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### _AI_INCLUDE folder

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  # Rules: what AI can/can't do
└── WHERE_IS_WHAT.md        # Architecture: where to find what
```

**AI reads these files FIRST** and follows the rules.

### .cursorignore / .gitignore

Prevents AI from indexing unnecessary files:

```
venv/
__pycache__/
*.pyc
.env
logs/
data/
node_modules/
```

---

## Context Switcher

When AI struggles with a large project — hide unnecessary modules!

### Usage

```bash
# Show help
python scripts/context.py

# Hide module from AI
python scripts/context.py hide parser

# Show module again
python scripts/context.py show parser

# List hidden modules
python scripts/context.py list
```

### How it works

The script renames folders to `_hidden_module_name`. Cursor/Copilot ignore files starting with `_`.

---

## Project Cleanup

### Cleanup levels

| Level | Actions |
|-------|---------|
| `safe` | Analysis only, no changes |
| `medium` | Backup + move venv + create configs |
| `full` | + move data + restructure |

### CLI

```bash
# Analysis only
ai-toolkit cleanup ./my_project --level safe

# Move venv + create configs
ai-toolkit cleanup ./my_project --level medium
```

### What is checked

- ❌ venv inside project
- ❌ site-packages in repo
- ⚠️ Large logs (>10MB)
- ⚠️ Large data folder
- ⚠️ __pycache__ folders
- ⚠️ Missing AI configs

---

## Migration

Add AI Toolkit to an existing project:

```bash
ai-toolkit migrate ./my_old_project
```

### What is added

- `_AI_INCLUDE/` folder
- `.cursorrules`, `.cursorignore`
- `CLAUDE.md`
- `scripts/bootstrap.sh`
- `scripts/context.py`
- `.toolkit-version`

---

## Docker and CI/CD

### Docker

```dockerfile
# Dockerfile created automatically
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```bash
# Build and run
docker-compose up --build
```

### GitHub Actions

**CI (ci.yml):**

- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)

**CD (cd.yml):**

- Build on tag push
- Deploy to production

### Dependabot

Auto-updates dependencies weekly.

---

## Plugins

### Plugin structure

```
~/.ai_toolkit/plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

### plugin.py

```python
def on_project_created(project_path: str, template: str) -> None:
    """Called after project creation."""
    print(f"Project created: {project_path}")

def on_cleanup(project_path: str, level: str) -> None:
    """Called after cleanup."""
    pass
```

---

## Troubleshooting

### venv not activating

```bash
# Check if venv exists
ls ../_venvs/

# Recreate
rm -rf ../_venvs/my_project-venv
./scripts/bootstrap.sh
```

### AI still indexes venv

1. Check `.cursorignore` exists
2. Restart IDE
3. Clear IDE cache

### Dashboard won't start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Start manually
python -m web.app
```

### "Module not found" errors

```bash
# Ensure venv is activated
which python
# Should show: ../_venvs/my_project-venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Support

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub Issues: [Report a bug](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Ask a question](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)



This guide will help you master AI Toolkit from start to finish.

> 🇷🇺 [Русская версия](GUIDE.ru.md)

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First Project](#first-project)
4. [Interfaces](#interfaces)
5. [Project Templates](#project-templates)
6. [Working with venv](#working-with-venv)
7. [AI Configuration](#ai-configuration)
8. [Context Switcher](#context-switcher)
9. [Project Cleanup](#project-cleanup)
10. [Migration](#migration)
11. [Docker and CI/CD](#docker-and-cicd)
12. [Plugins](#plugins)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is AI Toolkit?

AI Toolkit is a tool for creating Python projects optimized for AI assistants (Cursor, GitHub Copilot, Claude, Windsurf).

### Why is this needed?

When an AI assistant works with a project, it reads ALL files. If `venv/` is inside the project:

- 📦 AI indexes 500+ MB of dependencies
- 🐌 IDE slows down
- 🤯 AI gets confused reading library code
- 💾 Repository bloats

**Solution:** AI Toolkit creates projects with venv OUTSIDE the project and special configs for AI.

---

## Installation

### Requirements

- Python 3.10 or higher
- pip

### 🚀 One-Command Start (Recommended)

The easiest way to get started:

```bash
# Download
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Run ONE command!
# Windows:
.\start.ps1

# Linux/macOS:
./start.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install dependencies
3. ✅ Launch Web Dashboard
4. ✅ Open browser with Welcome screen

### Via pip

```bash
# Basic installation
pip install ai-toolkit

# With Web Dashboard
pip install ai-toolkit[web]
```

### Manual from source

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
```

### Verify installation

```bash
ai-toolkit --version
# or
python -m web.app --help
```

---

## First Project

### Interactive mode

```bash
ai-toolkit
```

1. Select language (🇬🇧 English / 🇷🇺 Русский)
2. Choose your IDE
3. Select "Create new project"
4. Enter project name
5. Choose template
6. Done! 🎉

### CLI mode

```bash
ai-toolkit create my_bot --template bot --path ~/projects
```

### Next steps after creation

```bash
cd ~/projects/my_bot
./scripts/bootstrap.sh
source ../_venvs/my_bot-venv/bin/activate
cp .env.example .env
```

---

## Interfaces

### CLI (Command Line)

```bash
# Interactive mode
ai-toolkit

# Create project
ai-toolkit create my_bot

# Cleanup
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project
```

### Web Dashboard

```bash
ai-toolkit dashboard
# or
ai-toolkit web
```

Opens a beautiful web interface at http://127.0.0.1:8080

### GUI (Tkinter)

```bash
python -m gui.app
```

---

## Project Templates

| Template | Description | Includes |
|----------|-------------|----------|
| `bot` | Telegram Bot | aiogram 3.x, handlers, FSM |
| `webapp` | Telegram Mini App | HTML/CSS/JS, Telegram Web App API |
| `fastapi` | REST API | FastAPI, Pydantic, async |
| `parser` | Web Scraper | aiohttp, BeautifulSoup |
| `full` | All modules | bot + webapp + parser + API |
| `monorepo` | Multi-project | Shared libs, multiple services |

### Template selection

```bash
# CLI
ai-toolkit create my_project --template fastapi

# Interactive - choose from menu
```

---

## Working with venv

### Why venv outside?

```
projects/
├── _venvs/                 ← All venvs here!
│   ├── bot1-venv/
│   ├── bot2-venv/
│   └── api-venv/
│
├── bot1/                   ← Clean project!
├── bot2/
└── api/
```

**Benefits:**

- ✅ AI sees only your code
- ✅ IDE works fast
- ✅ Repository is lightweight
- ✅ Easy to delete/recreate venv

### bootstrap.sh

The `scripts/bootstrap.sh` script creates venv outside the project:

```bash
./scripts/bootstrap.sh
```

What it does:

1. Creates `../_venvs/project-name-venv/`
2. Installs dependencies from `requirements.txt`
3. Shows activation command

### Activation

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

---

## AI Configuration

### Files for each IDE

| IDE | Files |
|-----|-------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### _AI_INCLUDE folder

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  # Rules: what AI can/can't do
└── WHERE_IS_WHAT.md        # Architecture: where to find what
```

**AI reads these files FIRST** and follows the rules.

### .cursorignore / .gitignore

Prevents AI from indexing unnecessary files:

```
venv/
__pycache__/
*.pyc
.env
logs/
data/
node_modules/
```

---

## Context Switcher

When AI struggles with a large project — hide unnecessary modules!

### Usage

```bash
# Show help
python scripts/context.py

# Hide module from AI
python scripts/context.py hide parser

# Show module again
python scripts/context.py show parser

# List hidden modules
python scripts/context.py list
```

### How it works

The script renames folders to `_hidden_module_name`. Cursor/Copilot ignore files starting with `_`.

---

## Project Cleanup

### Cleanup levels

| Level | Actions |
|-------|---------|
| `safe` | Analysis only, no changes |
| `medium` | Backup + move venv + create configs |
| `full` | + move data + restructure |

### CLI

```bash
# Analysis only
ai-toolkit cleanup ./my_project --level safe

# Move venv + create configs
ai-toolkit cleanup ./my_project --level medium
```

### What is checked

- ❌ venv inside project
- ❌ site-packages in repo
- ⚠️ Large logs (>10MB)
- ⚠️ Large data folder
- ⚠️ __pycache__ folders
- ⚠️ Missing AI configs

---

## Migration

Add AI Toolkit to an existing project:

```bash
ai-toolkit migrate ./my_old_project
```

### What is added

- `_AI_INCLUDE/` folder
- `.cursorrules`, `.cursorignore`
- `CLAUDE.md`
- `scripts/bootstrap.sh`
- `scripts/context.py`
- `.toolkit-version`

---

## Docker and CI/CD

### Docker

```dockerfile
# Dockerfile created automatically
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```bash
# Build and run
docker-compose up --build
```

### GitHub Actions

**CI (ci.yml):**

- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)

**CD (cd.yml):**

- Build on tag push
- Deploy to production

### Dependabot

Auto-updates dependencies weekly.

---

## Plugins

### Plugin structure

```
~/.ai_toolkit/plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

### plugin.py

```python
def on_project_created(project_path: str, template: str) -> None:
    """Called after project creation."""
    print(f"Project created: {project_path}")

def on_cleanup(project_path: str, level: str) -> None:
    """Called after cleanup."""
    pass
```

---

## Troubleshooting

### venv not activating

```bash
# Check if venv exists
ls ../_venvs/

# Recreate
rm -rf ../_venvs/my_project-venv
./scripts/bootstrap.sh
```

### AI still indexes venv

1. Check `.cursorignore` exists
2. Restart IDE
3. Clear IDE cache

### Dashboard won't start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Start manually
python -m web.app
```

### "Module not found" errors

```bash
# Ensure venv is activated
which python
# Should show: ../_venvs/my_project-venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Support

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub Issues: [Report a bug](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Ask a question](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)

This guide will help you master AI Toolkit from start to finish.

> 🇷🇺 [Русская версия](GUIDE.ru.md)

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First Project](#first-project)
4. [Interfaces](#interfaces)
5. [Project Templates](#project-templates)
6. [Working with venv](#working-with-venv)
7. [AI Configuration](#ai-configuration)
8. [Context Switcher](#context-switcher)
9. [Project Cleanup](#project-cleanup)
10. [Migration](#migration)
11. [Docker and CI/CD](#docker-and-cicd)
12. [Plugins](#plugins)
13. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is AI Toolkit?

AI Toolkit is a tool for creating Python projects optimized for AI assistants (Cursor, GitHub Copilot, Claude, Windsurf).

### Why is this needed?

When an AI assistant works with a project, it reads ALL files. If `venv/` is inside the project:

- 📦 AI indexes 500+ MB of dependencies
- 🐌 IDE slows down
- 🤯 AI gets confused reading library code
- 💾 Repository bloats

**Solution:** AI Toolkit creates projects with venv OUTSIDE the project and special configs for AI.

---

## Installation

### Requirements

- Python 3.10 or higher
- pip

### 🚀 One-Command Start (Recommended)

The easiest way to get started:

```bash
# Download
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Run ONE command!
# Windows:
.\start.ps1

# Linux/macOS:
./start.sh
```

This will:
1. ✅ Check Python version
2. ✅ Install dependencies
3. ✅ Launch Web Dashboard
4. ✅ Open browser with Welcome screen

### Via pip

```bash
# Basic installation
pip install ai-toolkit

# With Web Dashboard
pip install ai-toolkit[web]
```

### Manual from source

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
```

### Verify installation

```bash
ai-toolkit --version
# or
python -m web.app --help
```

---

## First Project

### Interactive mode

```bash
ai-toolkit
```

1. Select language (🇬🇧 English / 🇷🇺 Русский)
2. Choose your IDE
3. Select "Create new project"
4. Enter project name
5. Choose template
6. Done! 🎉

### CLI mode

```bash
ai-toolkit create my_bot --template bot --path ~/projects
```

### Next steps after creation

```bash
cd ~/projects/my_bot
./scripts/bootstrap.sh
source ../_venvs/my_bot-venv/bin/activate
cp .env.example .env
```

---

## Interfaces

### CLI (Command Line)

```bash
# Interactive mode
ai-toolkit

# Create project
ai-toolkit create my_bot

# Cleanup
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project
```

### Web Dashboard

```bash
ai-toolkit dashboard
# or
ai-toolkit web
```

Opens a beautiful web interface at http://127.0.0.1:8080

### GUI (Tkinter)

```bash
python -m gui.app
```

---

## Project Templates

| Template | Description | Includes |
|----------|-------------|----------|
| `bot` | Telegram Bot | aiogram 3.x, handlers, FSM |
| `webapp` | Telegram Mini App | HTML/CSS/JS, Telegram Web App API |
| `fastapi` | REST API | FastAPI, Pydantic, async |
| `parser` | Web Scraper | aiohttp, BeautifulSoup |
| `full` | All modules | bot + webapp + parser + API |
| `monorepo` | Multi-project | Shared libs, multiple services |

### Template selection

```bash
# CLI
ai-toolkit create my_project --template fastapi

# Interactive - choose from menu
```

---

## Working with venv

### Why venv outside?

```
projects/
├── _venvs/                 ← All venvs here!
│   ├── bot1-venv/
│   ├── bot2-venv/
│   └── api-venv/
│
├── bot1/                   ← Clean project!
├── bot2/
└── api/
```

**Benefits:**

- ✅ AI sees only your code
- ✅ IDE works fast
- ✅ Repository is lightweight
- ✅ Easy to delete/recreate venv

### bootstrap.sh

The `scripts/bootstrap.sh` script creates venv outside the project:

```bash
./scripts/bootstrap.sh
```

What it does:

1. Creates `../_venvs/project-name-venv/`
2. Installs dependencies from `requirements.txt`
3. Shows activation command

### Activation

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

---

## AI Configuration

### Files for each IDE

| IDE | Files |
|-----|-------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 GitHub Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |

### _AI_INCLUDE folder

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  # Rules: what AI can/can't do
└── WHERE_IS_WHAT.md        # Architecture: where to find what
```

**AI reads these files FIRST** and follows the rules.

### .cursorignore / .gitignore

Prevents AI from indexing unnecessary files:

```
venv/
__pycache__/
*.pyc
.env
logs/
data/
node_modules/
```

---

## Context Switcher

When AI struggles with a large project — hide unnecessary modules!

### Usage

```bash
# Show help
python scripts/context.py

# Hide module from AI
python scripts/context.py hide parser

# Show module again
python scripts/context.py show parser

# List hidden modules
python scripts/context.py list
```

### How it works

The script renames folders to `_hidden_module_name`. Cursor/Copilot ignore files starting with `_`.

---

## Project Cleanup

### Cleanup levels

| Level | Actions |
|-------|---------|
| `safe` | Analysis only, no changes |
| `medium` | Backup + move venv + create configs |
| `full` | + move data + restructure |

### CLI

```bash
# Analysis only
ai-toolkit cleanup ./my_project --level safe

# Move venv + create configs
ai-toolkit cleanup ./my_project --level medium
```

### What is checked

- ❌ venv inside project
- ❌ site-packages in repo
- ⚠️ Large logs (>10MB)
- ⚠️ Large data folder
- ⚠️ __pycache__ folders
- ⚠️ Missing AI configs

---

## Migration

Add AI Toolkit to an existing project:

```bash
ai-toolkit migrate ./my_old_project
```

### What is added

- `_AI_INCLUDE/` folder
- `.cursorrules`, `.cursorignore`
- `CLAUDE.md`
- `scripts/bootstrap.sh`
- `scripts/context.py`
- `.toolkit-version`

---

## Docker and CI/CD

### Docker

```dockerfile
# Dockerfile created automatically
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

```bash
# Build and run
docker-compose up --build
```

### GitHub Actions

**CI (ci.yml):**

- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)

**CD (cd.yml):**

- Build on tag push
- Deploy to production

### Dependabot

Auto-updates dependencies weekly.

---

## Plugins

### Plugin structure

```
~/.ai_toolkit/plugins/
└── my_plugin/
    ├── __init__.py
    └── plugin.py
```

### plugin.py

```python
def on_project_created(project_path: str, template: str) -> None:
    """Called after project creation."""
    print(f"Project created: {project_path}")

def on_cleanup(project_path: str, level: str) -> None:
    """Called after cleanup."""
    pass
```

---

## Troubleshooting

### venv not activating

```bash
# Check if venv exists
ls ../_venvs/

# Recreate
rm -rf ../_venvs/my_project-venv
./scripts/bootstrap.sh
```

### AI still indexes venv

1. Check `.cursorignore` exists
2. Restart IDE
3. Clear IDE cache

### Dashboard won't start

```bash
# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Start manually
python -m web.app
```

### "Module not found" errors

```bash
# Ensure venv is activated
which python
# Should show: ../_venvs/my_project-venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Support

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub Issues: [Report a bug](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Ask a question](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)
