# 🤝 Contributing Guide

Thank you for your interest in AI Toolkit! We welcome all contributions.

---

## 📋 Table of Contents

- [How to Help](#-how-to-help)
- [Report a Bug](#-report-a-bug)
- [Suggest a Feature](#-suggest-a-feature)
- [Setup Environment](#-setup-environment)
- [Code Style](#-code-style)
- [Pull Request Process](#-pull-request-process)
- [Project Structure](#-project-structure)

---

## 💡 How to Help

There are many ways to contribute:

| Method | Description |
|--------|-------------|
| 🐛 **Bugs** | Report a bug |
| 💡 **Features** | Suggest a new feature |
| 📖 **Documentation** | Improve documentation |
| 🌍 **Translation** | Translate to another language |
| 🧪 **Tests** | Add tests |
| 🔧 **Code** | Fix a bug or add a feature |

---

## 🐛 Report a Bug

1. Check that the bug hasn't been [reported](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
2. Create a [new Issue](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues/new)
3. Use this template:

```markdown
### Bug Description
What's happening wrong?

### Expected Behavior
What should happen?

### Steps to Reproduce
1. Run `ai-toolkit create test`
2. ...

### Environment
- OS: macOS 14.0
- Python: 3.12
- AI Toolkit: 3.0.0
```

---

## 💡 Suggest a Feature

1. Check [existing suggestions](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions/categories/ideas)
2. Create a new topic in Discussions → Ideas
3. Describe:
   - What problem does it solve?
   - How should it work?
   - Usage examples

---

## 🔧 Setup Environment

```bash
# Clone
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding

# Create venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"

# Check
ai-toolkit --version
```

### Run Tests

```bash
pytest tests/ -v
```

### Linting

```bash
ruff check src/
mypy src/
```

---

## 📝 Code Style

### Python

- **Formatter:** ruff (Black-compatible)
- **Linter:** ruff
- **Types:** mypy strict
- **Docstrings:** Google style

### Example

```python
"""Module description."""

from __future__ import annotations

from typing import Optional


def create_project(
    name: str,
    path: Path,
    template: str = "bot",
    *,
    include_docker: bool = True,
) -> bool:
    """
    Create a new project.

    Args:
        name: Project name
        path: Path to create project
        template: Project template
        include_docker: Include Docker files

    Returns:
        True if successful

    Raises:
        ValueError: If name is invalid
    """
    if not name:
        raise ValueError("Name cannot be empty")
    
    # ...
    return True
```

### Commits

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add monorepo template
fix: fix venv path on Windows
docs: update installation guide
style: format with ruff
refactor: extract template loader
test: add tests for cleanup
chore: update dependencies
```

---

## 🚀 Pull Request Process

### 1. Create Branch

```bash
git checkout -b feat/my-feature
# or
git checkout -b fix/bug-name
```

### 2. Make Changes

- Write code
- Add tests
- Update documentation

### 3. Check

```bash
# Tests
pytest tests/ -v

# Linting
ruff check src/
ruff format src/

# Types
mypy src/
```

### 4. Commit

```bash
git add .
git commit -m "feat: add new feature"
```

### 5. Push

```bash
git push origin feat/my-feature
```

### 6. Create PR

1. Go to GitHub
2. Click "New Pull Request"
3. Fill out description
4. Wait for review

---

## 📁 Project Structure

```
ai_toolkit/
├── src/                    # Main code
│   ├── cli.py              # CLI entry point
│   ├── core/               # Core utilities
│   │   ├── config.py       # Configuration
│   │   ├── constants.py    # Constants
│   │   ├── file_utils.py   # File operations
│   │   ├── i18n.py         # Internationalization
│   │   └── template_loader.py
│   │
│   ├── commands/           # CLI commands
│   │   ├── create.py       # Create project
│   │   ├── cleanup.py      # Cleanup
│   │   ├── health.py       # Health check
│   │   ├── migrate.py      # Migration
│   │   └── update.py       # Update
│   │
│   ├── generators/         # File generators
│   │   ├── ai_configs.py   # AI configs
│   │   ├── ci_cd.py        # CI/CD
│   │   ├── docker.py       # Docker
│   │   ├── git.py          # Git
│   │   ├── project_files.py
│   │   └── scripts.py
│   │
│   ├── locales/            # Translations
│   │   └── en.py           # English
│   │
│   └── types.py            # Type definitions
│
├── web/                    # Web Dashboard
│   ├── app.py              # FastAPI app
│   ├── i18n.py             # Web translations
│   ├── templates/          # HTML templates
│   └── static/             # Static files
│
├── gui/                    # GUI (Tkinter)
│   └── app.py
│
├── plugins/                # Plugin system
│   └── manager.py
│
├── templates/              # Project templates
├── tests/                  # Tests
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

---

## 💬 Questions?

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 💬 [GitHub Discussions](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)

---

## 📜 Code of Conduct

- Be respectful
- Be constructive
- Help others

Thank you for your contribution! 🎉
