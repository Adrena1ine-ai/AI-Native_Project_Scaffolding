# 🤖 Claude Instructions — AI Toolkit

## 🚨 FIRST ACTION

Read `_AI_INCLUDE/` — that's where the project rules are.

```
_AI_INCLUDE/
├── PROJECT_CONVENTIONS.md  ← Architecture, restrictions, rules
└── WHERE_IS_WHAT.md        ← Where to find what
```

---

## 📌 This is the AI Toolkit project

A tool for creating AI-friendly projects. Generates:
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
│   └── config.py       ← Config management
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

## ⚠️ FORBIDDEN

1. **DO NOT create venv/** inside this project
2. **DO NOT change constants.py** without understanding dependencies
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
./scripts/health_check.sh (if exists)
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

---

## 🚀 Onboarding (New Developers)

**3 steps to get productive:**

### Step 1: Understand the Structure
```bash
# Read the auto-generated project map
cat CURRENT_CONTEXT_MAP.md

# Key directories:
# src/commands/  → CLI commands (create, cleanup, migrate, etc.)
# src/core/      → Shared utilities (constants, config, file_utils)
# src/generators/→ File generators (AI configs, Docker, scripts)
```

### Step 2: Run the Toolkit
```bash
# Interactive mode
python main.py

# Direct command
python main.py create test_project --template bot

# Run tests
pytest tests/ -v
```

### Step 3: Make Your First Change
```bash
# 1. Edit code in src/
# 2. Run tests to verify
pytest tests/ -v

# 3. Update the context map
python3 generate_map.py

# 4. Check token impact
python3 benchmark.py
```

---

## 🧠 Thinking Keywords

Use these keywords in your prompts to control Claude's reasoning depth:

| Keyword | Behavior | Use When |
|---------|----------|----------|
| **"Think"** | Standard analysis, quick response | Simple questions, small changes |
| **"Think step by step"** | Methodical breakdown | Multi-step tasks, debugging |
| **"Think hard"** | Deep analysis, consider edge cases | Complex architecture, security review |
| **"Think very hard"** | Maximum depth, explore alternatives | Critical decisions, tricky bugs |

### Examples

```
Think: What does create_project() return?
→ Quick answer: Returns bool (True on success)

Think hard: Is there a security issue in file_utils.py?
→ Deep analysis of path traversal, permissions, etc.

Think step by step: How do I add a new CLI command?
→ Numbered steps with file paths and code examples
```

---

## 📚 Additional Resources

| Document | Purpose |
|----------|---------|
| `PROMPTS_LIBRARY.md` | Ready-to-use prompts for common tasks |
| `TRADEOFFS.md` | Architectural decisions and rationale |
| `.cursor/rules/` | Detailed rules for different contexts |
| `CURRENT_CONTEXT_MAP.md` | Auto-generated project structure |
