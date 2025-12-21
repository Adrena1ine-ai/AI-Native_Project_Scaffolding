# 🤖 Claude Instructions — AI Toolkit

## 🚨 FIRST ACTION

Read `_AI_INCLUDE/` — it contains the rules for this project.

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  ← Architecture, restrictions, rules
└── WHERE_IS_WHAT.md        ← Where to find what
```

---

## 📌 This is the AI Toolkit project

A tool for creating AI-friendly projects. It generates:
- Project structure
- AI configs (.cursorrules, copilot-instructions.md, CLAUDE.md)
- Scripts (bootstrap.sh, health_check.sh)
- Docker, CI/CD, Git

---

## 🏗️ Key Architecture

```
src/
├── core/           # Base components
│   ├── constants.py    ← ALL constants here!
│   └── config.py       ← Configuration management
├── generators/     # File generators
│   ├── ai_configs.py   ← .cursorrules, copilot, CLAUDE.md
│   ├── scripts.py      ← bootstrap.sh, health_check.sh
│   ├── docker.py       ← Dockerfile
│   └── ci_cd.py        ← GitHub Actions
├── commands/       # CLI commands
│   ├── create.py       ← Project creation
│   └── cleanup.py      ← Cleanup
└── cli.py          # Main CLI
```

---

## ⚠️ RESTRICTIONS

1. **DO NOT create venv/** inside this project
2. **DO NOT modify constants.py** without understanding dependencies
3. **DO NOT add dependencies** without necessity

---

## ✅ How to add a new feature

### New generator:
1. Create in `src/generators/new_generator.py`
2. Add to `src/generators/__init__.py`
3. Call in `src/commands/create.py`

### New command:
1. Create in `src/commands/new_command.py`
2. Add to `src/commands/__init__.py`
3. Add to `src/cli.py` (menu + argparse)

### New template:
1. Add to `TEMPLATES` in `src/core/constants.py`
2. Add generation in `src/commands/create.py`

---

## 🧪 Testing

```bash
# Run
python __main__.py

# CLI
python __main__.py create test_bot --template bot --ai copilot

# Check
./scripts/health_check.sh (if available)
```

---

## 📁 Quick Links

| Need | File |
|------|------|
| All templates | `src/core/constants.py` → `TEMPLATES` |
| All IDEs | `src/core/constants.py` → `IDE_CONFIGS` |
| AI file generation | `src/generators/ai_configs.py` |
| Main creation logic | `src/commands/create.py` |
| CLI menu | `src/cli.py` |
