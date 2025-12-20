# ⚡ Quick Start

Get started in 1 minute with just ONE command!

> 🇷🇺 [Русская версия](QUICK_START.ru.md)

---

## 🚀 One-Command Start (Recommended)

### Step 1: Download

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
```

### Step 2: Run ONE command!

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/macOS:**
```bash
./start.sh
```

### Step 3: Done! 🎉

The browser opens automatically with:

1. **Welcome Screen** → Select language (English/Russian)
2. **Dashboard** → Create projects, cleanup, health check

---

## 📸 What You'll See

### Welcome Screen (First Launch)
```
🛠️ AI-Native Project Scaffolding

🌍 Select language / Выберите язык

🇬🇧 English          🇷🇺 Русский
```

### Main Dashboard
| Page | Description |
|------|-------------|
| 🏠 Home | Quick actions, project stats |
| 🆕 Create | Visual project builder |
| 🧹 Cleanup | Analyze & fix dirty projects |
| 🏥 Health | Check project configuration |
| ⚙️ Settings | Default IDE selection |
| ❓ Help | Documentation for beginners |

---

## 💻 Alternative Installation

### From PyPI

```bash
# Install
pip install ai-toolkit[web]

# Run Dashboard
ai-toolkit dashboard

# Or Interactive CLI
ai-toolkit
```

### Manual from Source

```bash
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
python -m web.app
```

---

## 🛠️ Creating Your First Project

### Via Dashboard (Easiest)

1. Open Dashboard: http://127.0.0.1:8080
2. Click **"🆕 Create"**
3. Enter project name: `my_bot`
4. Select template: **bot**
5. Select IDE: **Cursor** (or your IDE)
6. Click **"Create Project"** ✅

### Via CLI

```bash
ai-toolkit create my_bot --template bot
```

### After Creation

```bash
cd my_bot

# Create venv OUTSIDE project (key feature!)
./scripts/bootstrap.sh          # Linux/macOS
.\scripts\bootstrap.ps1         # Windows

# Activate venv
source ../_venvs/my_bot-venv/bin/activate    # Linux/macOS
..\_venvs\my_bot-venv\Scripts\activate       # Windows

# Configure & run
cp .env.example .env
python main.py
```

---

## 📦 Available Templates

| Template | Description | What's Created |
|----------|-------------|----------------|
| 🤖 `bot` | Telegram Bot | aiogram 3.x, handlers, keyboards |
| 🌐 `webapp` | Mini App | HTML/CSS/JS, API |
| ⚡ `fastapi` | REST API | FastAPI, SQLAlchemy |
| 🕷️ `parser` | Web Scraper | aiohttp, BeautifulSoup |
| 🚀 `full` | Everything | bot + webapp + api + parser |
| 📦 `monorepo` | Multi-project | apps/, packages/, shared/ |

---

## 🔧 Working with Existing Projects

### Cleanup (Fix Dirty Project)

```bash
# Via Dashboard
# → Go to "🧹 Cleanup" → Enter path → Analyze

# Via CLI
ai-toolkit cleanup ./my_project --level safe     # Just analyze
ai-toolkit cleanup ./my_project --level medium   # Fix with backup
```

### Health Check

```bash
ai-toolkit health ./my_project
```

### Add Toolkit to Existing Project

```bash
ai-toolkit migrate ./my_project
```

---

## 🖥️ Supported IDEs

| IDE | Config Files | Auto-Detected |
|-----|--------------|---------------|
| 💜 **Cursor** | `.cursorrules`, `.cursorignore` | ✅ |
| 💙 **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| 🟢 **Claude** | `CLAUDE.md` | ✅ |
| 🌊 **Windsurf** | `.windsurfrules` | ✅ |

> 💡 Dashboard **auto-detects** which IDEs are configured in your project!

---

## ❓ Troubleshooting

### Port Already in Use

```bash
# Use different port
.\start.ps1 -Port 3000          # Windows
./start.sh --port 3000          # Linux/macOS

# Or manually
python -m web.app --port 3000
```

### `ai-toolkit` Command Not Found

```bash
# Use Python module syntax instead
python -m src.cli              # CLI
python -m web.app              # Dashboard
```

### Wrong Directory

> ⚠️ Always run from `AI-Native_Project_Scaffolding` folder!

```bash
cd AI-Native_Project_Scaffolding
.\start.ps1
```

---

## 📚 Learn More

- 📖 [Full Guide](GUIDE.md) — detailed documentation
- ❓ [FAQ](FAQ.md) — common questions
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — star the project ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — get help

---

## 🎯 The Magic: venv OUTSIDE Project

```
projects/
├── _venvs/                  ← All venvs here!
│   └── my_bot-venv/         (not in project!)
│
└── my_bot/                  ← Clean project!
    ├── _AI_INCLUDE/         ← Rules for AI
    ├── scripts/
    │   └── bootstrap.sh     ← Creates venv outside
    └── main.py
```

**Result:** Fast IDE, smart AI, clean Git! 🚀

Get started in 1 minute with just ONE command!

> 🇷🇺 [Русская версия](QUICK_START.ru.md)

---

## 🚀 One-Command Start (Recommended)

### Step 1: Download

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
```

### Step 2: Run ONE command!

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/macOS:**
```bash
./start.sh
```

### Step 3: Done! 🎉

The browser opens automatically with:

1. **Welcome Screen** → Select language (English/Russian)
2. **Dashboard** → Create projects, cleanup, health check

---

## 📸 What You'll See

### Welcome Screen (First Launch)
```
🛠️ AI-Native Project Scaffolding

🌍 Select language / Выберите язык

🇬🇧 English          🇷🇺 Русский
```

### Main Dashboard
| Page | Description |
|------|-------------|
| 🏠 Home | Quick actions, project stats |
| 🆕 Create | Visual project builder |
| 🧹 Cleanup | Analyze & fix dirty projects |
| 🏥 Health | Check project configuration |
| ⚙️ Settings | Default IDE selection |
| ❓ Help | Documentation for beginners |

---

## 💻 Alternative Installation

### From PyPI

```bash
# Install
pip install ai-toolkit[web]

# Run Dashboard
ai-toolkit dashboard

# Or Interactive CLI
ai-toolkit
```

### Manual from Source

```bash
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
python -m web.app
```

---

## 🛠️ Creating Your First Project

### Via Dashboard (Easiest)

1. Open Dashboard: http://127.0.0.1:8080
2. Click **"🆕 Create"**
3. Enter project name: `my_bot`
4. Select template: **bot**
5. Select IDE: **Cursor** (or your IDE)
6. Click **"Create Project"** ✅

### Via CLI

```bash
ai-toolkit create my_bot --template bot
```

### After Creation

```bash
cd my_bot

# Create venv OUTSIDE project (key feature!)
./scripts/bootstrap.sh          # Linux/macOS
.\scripts\bootstrap.ps1         # Windows

# Activate venv
source ../_venvs/my_bot-venv/bin/activate    # Linux/macOS
..\_venvs\my_bot-venv\Scripts\activate       # Windows

# Configure & run
cp .env.example .env
python main.py
```

---

## 📦 Available Templates

| Template | Description | What's Created |
|----------|-------------|----------------|
| 🤖 `bot` | Telegram Bot | aiogram 3.x, handlers, keyboards |
| 🌐 `webapp` | Mini App | HTML/CSS/JS, API |
| ⚡ `fastapi` | REST API | FastAPI, SQLAlchemy |
| 🕷️ `parser` | Web Scraper | aiohttp, BeautifulSoup |
| 🚀 `full` | Everything | bot + webapp + api + parser |
| 📦 `monorepo` | Multi-project | apps/, packages/, shared/ |

---

## 🔧 Working with Existing Projects

### Cleanup (Fix Dirty Project)

```bash
# Via Dashboard
# → Go to "🧹 Cleanup" → Enter path → Analyze

# Via CLI
ai-toolkit cleanup ./my_project --level safe     # Just analyze
ai-toolkit cleanup ./my_project --level medium   # Fix with backup
```

### Health Check

```bash
ai-toolkit health ./my_project
```

### Add Toolkit to Existing Project

```bash
ai-toolkit migrate ./my_project
```

---

## 🖥️ Supported IDEs

| IDE | Config Files | Auto-Detected |
|-----|--------------|---------------|
| 💜 **Cursor** | `.cursorrules`, `.cursorignore` | ✅ |
| 💙 **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| 🟢 **Claude** | `CLAUDE.md` | ✅ |
| 🌊 **Windsurf** | `.windsurfrules` | ✅ |

> 💡 Dashboard **auto-detects** which IDEs are configured in your project!

---

## ❓ Troubleshooting

### Port Already in Use

```bash
# Use different port
.\start.ps1 -Port 3000          # Windows
./start.sh --port 3000          # Linux/macOS

# Or manually
python -m web.app --port 3000
```

### `ai-toolkit` Command Not Found

```bash
# Use Python module syntax instead
python -m src.cli              # CLI
python -m web.app              # Dashboard
```

### Wrong Directory

> ⚠️ Always run from `AI-Native_Project_Scaffolding` folder!

```bash
cd AI-Native_Project_Scaffolding
.\start.ps1
```

---

## 📚 Learn More

- 📖 [Full Guide](GUIDE.md) — detailed documentation
- ❓ [FAQ](FAQ.md) — common questions
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — star the project ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — get help

---

## 🎯 The Magic: venv OUTSIDE Project

```
projects/
├── _venvs/                  ← All venvs here!
│   └── my_bot-venv/         (not in project!)
│
└── my_bot/                  ← Clean project!
    ├── _AI_INCLUDE/         ← Rules for AI
    ├── scripts/
    │   └── bootstrap.sh     ← Creates venv outside
    └── main.py
```

**Result:** Fast IDE, smart AI, clean Git! 🚀



Get started in 1 minute with just ONE command!

> 🇷🇺 [Русская версия](QUICK_START.ru.md)

---

## 🚀 One-Command Start (Recommended)

### Step 1: Download

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
```

### Step 2: Run ONE command!

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/macOS:**
```bash
./start.sh
```

### Step 3: Done! 🎉

The browser opens automatically with:

1. **Welcome Screen** → Select language (English/Russian)
2. **Dashboard** → Create projects, cleanup, health check

---

## 📸 What You'll See

### Welcome Screen (First Launch)
```
🛠️ AI-Native Project Scaffolding

🌍 Select language / Выберите язык

🇬🇧 English          🇷🇺 Русский
```

### Main Dashboard
| Page | Description |
|------|-------------|
| 🏠 Home | Quick actions, project stats |
| 🆕 Create | Visual project builder |
| 🧹 Cleanup | Analyze & fix dirty projects |
| 🏥 Health | Check project configuration |
| ⚙️ Settings | Default IDE selection |
| ❓ Help | Documentation for beginners |

---

## 💻 Alternative Installation

### From PyPI

```bash
# Install
pip install ai-toolkit[web]

# Run Dashboard
ai-toolkit dashboard

# Or Interactive CLI
ai-toolkit
```

### Manual from Source

```bash
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
python -m web.app
```

---

## 🛠️ Creating Your First Project

### Via Dashboard (Easiest)

1. Open Dashboard: http://127.0.0.1:8080
2. Click **"🆕 Create"**
3. Enter project name: `my_bot`
4. Select template: **bot**
5. Select IDE: **Cursor** (or your IDE)
6. Click **"Create Project"** ✅

### Via CLI

```bash
ai-toolkit create my_bot --template bot
```

### After Creation

```bash
cd my_bot

# Create venv OUTSIDE project (key feature!)
./scripts/bootstrap.sh          # Linux/macOS
.\scripts\bootstrap.ps1         # Windows

# Activate venv
source ../_venvs/my_bot-venv/bin/activate    # Linux/macOS
..\_venvs\my_bot-venv\Scripts\activate       # Windows

# Configure & run
cp .env.example .env
python main.py
```

---

## 📦 Available Templates

| Template | Description | What's Created |
|----------|-------------|----------------|
| 🤖 `bot` | Telegram Bot | aiogram 3.x, handlers, keyboards |
| 🌐 `webapp` | Mini App | HTML/CSS/JS, API |
| ⚡ `fastapi` | REST API | FastAPI, SQLAlchemy |
| 🕷️ `parser` | Web Scraper | aiohttp, BeautifulSoup |
| 🚀 `full` | Everything | bot + webapp + api + parser |
| 📦 `monorepo` | Multi-project | apps/, packages/, shared/ |

---

## 🔧 Working with Existing Projects

### Cleanup (Fix Dirty Project)

```bash
# Via Dashboard
# → Go to "🧹 Cleanup" → Enter path → Analyze

# Via CLI
ai-toolkit cleanup ./my_project --level safe     # Just analyze
ai-toolkit cleanup ./my_project --level medium   # Fix with backup
```

### Health Check

```bash
ai-toolkit health ./my_project
```

### Add Toolkit to Existing Project

```bash
ai-toolkit migrate ./my_project
```

---

## 🖥️ Supported IDEs

| IDE | Config Files | Auto-Detected |
|-----|--------------|---------------|
| 💜 **Cursor** | `.cursorrules`, `.cursorignore` | ✅ |
| 💙 **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| 🟢 **Claude** | `CLAUDE.md` | ✅ |
| 🌊 **Windsurf** | `.windsurfrules` | ✅ |

> 💡 Dashboard **auto-detects** which IDEs are configured in your project!

---

## ❓ Troubleshooting

### Port Already in Use

```bash
# Use different port
.\start.ps1 -Port 3000          # Windows
./start.sh --port 3000          # Linux/macOS

# Or manually
python -m web.app --port 3000
```

### `ai-toolkit` Command Not Found

```bash
# Use Python module syntax instead
python -m src.cli              # CLI
python -m web.app              # Dashboard
```

### Wrong Directory

> ⚠️ Always run from `AI-Native_Project_Scaffolding` folder!

```bash
cd AI-Native_Project_Scaffolding
.\start.ps1
```

---

## 📚 Learn More

- 📖 [Full Guide](GUIDE.md) — detailed documentation
- ❓ [FAQ](FAQ.md) — common questions
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — star the project ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — get help

---

## 🎯 The Magic: venv OUTSIDE Project

```
projects/
├── _venvs/                  ← All venvs here!
│   └── my_bot-venv/         (not in project!)
│
└── my_bot/                  ← Clean project!
    ├── _AI_INCLUDE/         ← Rules for AI
    ├── scripts/
    │   └── bootstrap.sh     ← Creates venv outside
    └── main.py
```

**Result:** Fast IDE, smart AI, clean Git! 🚀

Get started in 1 minute with just ONE command!

> 🇷🇺 [Русская версия](QUICK_START.ru.md)

---

## 🚀 One-Command Start (Recommended)

### Step 1: Download

```bash
git clone https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding.git
cd AI-Native_Project_Scaffolding
```

### Step 2: Run ONE command!

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/macOS:**
```bash
./start.sh
```

### Step 3: Done! 🎉

The browser opens automatically with:

1. **Welcome Screen** → Select language (English/Russian)
2. **Dashboard** → Create projects, cleanup, health check

---

## 📸 What You'll See

### Welcome Screen (First Launch)
```
🛠️ AI-Native Project Scaffolding

🌍 Select language / Выберите язык

🇬🇧 English          🇷🇺 Русский
```

### Main Dashboard
| Page | Description |
|------|-------------|
| 🏠 Home | Quick actions, project stats |
| 🆕 Create | Visual project builder |
| 🧹 Cleanup | Analyze & fix dirty projects |
| 🏥 Health | Check project configuration |
| ⚙️ Settings | Default IDE selection |
| ❓ Help | Documentation for beginners |

---

## 💻 Alternative Installation

### From PyPI

```bash
# Install
pip install ai-toolkit[web]

# Run Dashboard
ai-toolkit dashboard

# Or Interactive CLI
ai-toolkit
```

### Manual from Source

```bash
cd AI-Native_Project_Scaffolding
pip install -e ".[web]"
python -m web.app
```

---

## 🛠️ Creating Your First Project

### Via Dashboard (Easiest)

1. Open Dashboard: http://127.0.0.1:8080
2. Click **"🆕 Create"**
3. Enter project name: `my_bot`
4. Select template: **bot**
5. Select IDE: **Cursor** (or your IDE)
6. Click **"Create Project"** ✅

### Via CLI

```bash
ai-toolkit create my_bot --template bot
```

### After Creation

```bash
cd my_bot

# Create venv OUTSIDE project (key feature!)
./scripts/bootstrap.sh          # Linux/macOS
.\scripts\bootstrap.ps1         # Windows

# Activate venv
source ../_venvs/my_bot-venv/bin/activate    # Linux/macOS
..\_venvs\my_bot-venv\Scripts\activate       # Windows

# Configure & run
cp .env.example .env
python main.py
```

---

## 📦 Available Templates

| Template | Description | What's Created |
|----------|-------------|----------------|
| 🤖 `bot` | Telegram Bot | aiogram 3.x, handlers, keyboards |
| 🌐 `webapp` | Mini App | HTML/CSS/JS, API |
| ⚡ `fastapi` | REST API | FastAPI, SQLAlchemy |
| 🕷️ `parser` | Web Scraper | aiohttp, BeautifulSoup |
| 🚀 `full` | Everything | bot + webapp + api + parser |
| 📦 `monorepo` | Multi-project | apps/, packages/, shared/ |

---

## 🔧 Working with Existing Projects

### Cleanup (Fix Dirty Project)

```bash
# Via Dashboard
# → Go to "🧹 Cleanup" → Enter path → Analyze

# Via CLI
ai-toolkit cleanup ./my_project --level safe     # Just analyze
ai-toolkit cleanup ./my_project --level medium   # Fix with backup
```

### Health Check

```bash
ai-toolkit health ./my_project
```

### Add Toolkit to Existing Project

```bash
ai-toolkit migrate ./my_project
```

---

## 🖥️ Supported IDEs

| IDE | Config Files | Auto-Detected |
|-----|--------------|---------------|
| 💜 **Cursor** | `.cursorrules`, `.cursorignore` | ✅ |
| 💙 **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ |
| 🟢 **Claude** | `CLAUDE.md` | ✅ |
| 🌊 **Windsurf** | `.windsurfrules` | ✅ |

> 💡 Dashboard **auto-detects** which IDEs are configured in your project!

---

## ❓ Troubleshooting

### Port Already in Use

```bash
# Use different port
.\start.ps1 -Port 3000          # Windows
./start.sh --port 3000          # Linux/macOS

# Or manually
python -m web.app --port 3000
```

### `ai-toolkit` Command Not Found

```bash
# Use Python module syntax instead
python -m src.cli              # CLI
python -m web.app              # Dashboard
```

### Wrong Directory

> ⚠️ Always run from `AI-Native_Project_Scaffolding` folder!

```bash
cd AI-Native_Project_Scaffolding
.\start.ps1
```

---

## 📚 Learn More

- 📖 [Full Guide](GUIDE.md) — detailed documentation
- ❓ [FAQ](FAQ.md) — common questions
- 🐙 [GitHub](https://github.com/Adrena1ine-ai/AI-Native_Project_Scaffolding) — star the project ⭐
- 📱 [Telegram](https://t.me/MichaelSalmin) — get help

---

## 🎯 The Magic: venv OUTSIDE Project

```
projects/
├── _venvs/                  ← All venvs here!
│   └── my_bot-venv/         (not in project!)
│
└── my_bot/                  ← Clean project!
    ├── _AI_INCLUDE/         ← Rules for AI
    ├── scripts/
    │   └── bootstrap.sh     ← Creates venv outside
    └── main.py
```

**Result:** Fast IDE, smart AI, clean Git! 🚀
