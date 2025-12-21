# ❓ Frequently Asked Questions (FAQ)

---

## 🤔 General Questions

### What is AI Toolkit?

AI Toolkit is a tool for creating Python projects optimized for AI assistants (Cursor, GitHub Copilot, Claude, Windsurf).

### Why store venv outside the project?

AI assistants index all files in the project. If venv is inside:
- 🐌 IDE slows down (500+ MB of files)
- 🤯 AI reads dependency code and gets confused
- 💾 Git repository bloats

When venv is outside — AI sees only your code.

### Which IDEs are supported?

| IDE | Status |
|-----|--------|
| Cursor | ✅ Full support |
| VS Code + Copilot | ✅ Full support |
| VS Code + Claude | ✅ Full support |
| Windsurf | ✅ Full support |
| PyCharm | ⚠️ Partial (_AI_INCLUDE only) |

### Is AI Toolkit free?

Yes, completely free and open source (MIT License).

---

## 🔧 Installation and Setup

### What is the minimum Python version?

Python 3.10 or higher.

### How to install?

```bash
pip install ai-toolkit
```

### How to update?

```bash
pip install --upgrade ai-toolkit
```

### How to uninstall?

```bash
pip uninstall ai-toolkit
```

---

## 📁 Projects

### Where is venv stored?

In `../_venvs/project-name-venv/` — one level up from the project.

### How to activate venv?

```bash
# Linux/macOS
source ../_venvs/my_project-venv/bin/activate

# Windows
..\_venvs\my_project-venv\Scripts\activate
```

### How to add venv to existing project?

```bash
ai-toolkit migrate ./my_project
./my_project/scripts/bootstrap.sh
```

### Which templates are available?

| Template | Description |
|----------|-------------|
| `bot` | Telegram Bot (aiogram) |
| `webapp` | Telegram Mini App |
| `fastapi` | REST API |
| `parser` | Web Scraper |
| `full` | All modules |
| `monorepo` | Multi-project |

---

## 🤖 AI Configuration

### What is _AI_INCLUDE?

A folder with rules for AI. Contains:
- `PROJECT_CONVENTIONS.md` — what AI can and can't do
- `WHERE_IS_WHAT.md` — project architecture

AI reads these files FIRST.

### What is .cursorrules?

A configuration file for Cursor AI. Describes:
- Coding style
- Allowed patterns
- Forbidden patterns

### What is CLAUDE.md?

A file for Claude AI. Contains the same rules as `.cursorrules` but in Claude format.

### Why isn't AI following my rules?

1. Check that `_AI_INCLUDE/` exists
2. Restart IDE
3. Ask AI: "Read PROJECT_CONVENTIONS.md and follow it"

---

## 🧹 Cleanup

### What cleanup levels are there?

| Level | Actions |
|-------|---------|
| `safe` | Analysis only |
| `medium` | Backup + move venv |
| `full` | + data restructure |

### Is cleanup dangerous?

- `safe` — completely safe
- `medium` — creates backup first
- `full` — use with caution

### How to restore after cleanup?

Backup is saved to `../_backups/project-name-timestamp/`

---

## 🐛 Troubleshooting

### AI still indexes venv

1. Check `.cursorignore` exists
2. Restart IDE
3. Clear IDE cache

### Dashboard won't start

```bash
pip install fastapi uvicorn jinja2 python-multipart
python -m web.app
```

### "Permission denied" on bootstrap.sh

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

### Project not created

1. Check you have write permissions
2. Check the path exists
3. Check project name (only a-z, 0-9, _, -)

---

## 💬 Support

- 📱 Telegram: [@MichaelSalmin](https://t.me/MichaelSalmin)
- 🐙 GitHub: [Issues](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/issues)
- 💬 Discussions: [Q&A](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding/discussions)
