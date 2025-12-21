# 🛠️ AI Toolkit — Project Conventions

## 📌 This file is required reading for AI assistants!

---

## 🏗️ Project Architecture

```
ai_toolkit/
├── src/                    # Source code
│   ├── core/               # Base components
│   │   ├── config.py       # Configuration
│   │   ├── constants.py    # Constants (COLORS, TEMPLATES)
│   │   └── file_utils.py   # File operations
│   ├── generators/         # File generators
│   │   ├── ai_configs.py   # .cursorrules, copilot-instructions.md
│   │   ├── scripts.py      # bootstrap.sh, health_check.sh
│   │   ├── docker.py       # Dockerfile, docker-compose
│   │   ├── ci_cd.py        # GitHub Actions
│   │   ├── git.py          # .gitignore, git init
│   │   └── project_files.py # requirements, config.py, README
│   ├── commands/           # CLI commands
│   │   ├── create.py       # Project creation
│   │   ├── cleanup.py      # Cleanup
│   │   ├── migrate.py      # Migration
│   │   ├── health.py       # Health check
│   │   └── update.py       # Update
│   └── cli.py              # Main CLI
├── templates/              # External templates (TODO)
├── plugins/                # Plugins (TODO)
├── gui/                    # GUI (TODO)
├── tests/                  # Tests
└── docs/                   # Documentation
```

---

## 🚫 RESTRICTIONS

### When working with this project, AI MUST NOT:

1. **DO NOT create venv inside ai_toolkit/**
   - Venv should be in `../_venvs/ai_toolkit-venv`

2. **DO NOT modify without understanding:**
   - `src/core/constants.py` — all constants are interconnected
   - `src/generators/*.py` — generates code, test after changes

3. **DO NOT add dependencies without necessity**
   - Project should work with minimal dependencies
   - Required: `pyyaml`
   - Optional: `pytest`, `tkinter` (GUI)

---

## ✅ CORRECT ACTIONS

### Adding a new generator:

1. Create file in `src/generators/`
2. Add function `generate_xxx(project_dir, project_name, ...)`
3. Import in `src/generators/__init__.py`
4. Call in `src/commands/create.py`

### Adding a new command:

1. Create file in `src/commands/`
2. Add `cmd_xxx()` for interactive mode
3. Add to `src/commands/__init__.py`
4. Add to `src/cli.py` (menu + argparse)

### Adding a new template:

1. Add to `TEMPLATES` in `src/core/constants.py`
2. Add module generation in `src/commands/create.py`
3. Update `generate_requirements()` in `src/generators/project_files.py`

---

## 📏 Code Style

- Python 3.10+
- Type hints required
- Docstrings for public functions
- f-strings for formatting
- pathlib.Path instead of os.path
- Maximum 100 characters per line

---

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Manual testing
python __main__.py create test_bot --template bot --ai copilot
./scripts/health_check.sh
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/core/constants.py` | ALL constants, templates, configs |
| `src/commands/create.py` | Main project creation logic |
| `src/generators/ai_configs.py` | AI file generation |
| `src/cli.py` | CLI interface |

---

## 🔄 Project Creation Flow

```
1. cli.py → select_ide()
2. cli.py → cmd_create()
3. commands/create.py → create_project()
   ├── generators/ai_configs.py → AI files
   ├── generators/scripts.py → Scripts
   ├── generators/project_files.py → Core files
   ├── commands/create.py → Modules (bot, db, api)
   ├── generators/docker.py → Docker
   ├── generators/ci_cd.py → CI/CD
   └── generators/git.py → Git init
```
