# ⚡ Quick Start

Create your first project in 2 minutes!

> 🇷🇺 [Русская версия](QUICK_START.ru.md)

---

## 1️⃣ Installation

```bash
pip install ai-toolkit
```

---

## 2️⃣ Create Project

**Option A: Web Dashboard**
```bash
ai-toolkit dashboard
```

**Option B: One command**
```bash
ai-toolkit create my_bot --template bot
```

**Option C: Interactive mode**
```bash
ai-toolkit
```

---

## 3️⃣ Setup

```bash
cd my_bot

# Create venv (outside project!)
./scripts/bootstrap.sh

# Activate
source ../_venvs/my_bot-venv/bin/activate

# Configure .env
cp .env.example .env
```

---

## 4️⃣ Run

```bash
python main.py
```

---

## 🎉 Done!

### What's next?

- 📖 [Full Guide](GUIDE.md) — detailed documentation
- ❓ [FAQ](FAQ.md) — common questions
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — star the project ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — get help

---

## 📦 Available Templates

| Command | Description |
|---------|-------------|
| `--template bot` | Telegram Bot (aiogram) |
| `--template webapp` | Mini App (HTML/JS) |
| `--template fastapi` | REST API |
| `--template parser` | Web Scraper |
| `--template full` | All modules |
| `--template monorepo` | Multi-project |

---

## 🛠️ Useful Commands

```bash
# Cleanup dirty project
ai-toolkit cleanup ./my_project --level medium

# Health check
ai-toolkit health ./my_project

# Add toolkit to existing project
ai-toolkit migrate ./my_project

# Open Web Dashboard
ai-toolkit dashboard
```

---

## 🖥️ IDE Selection

When creating a project, select your IDE:

| IDE | Files Created |
|-----|---------------|
| 💜 Cursor | `.cursorrules`, `.cursorignore` |
| 💙 Copilot | `.github/copilot-instructions.md` |
| 🟢 Claude | `CLAUDE.md` |
| 🌊 Windsurf | `.windsurfrules` |
| 🔄 All | All files |
