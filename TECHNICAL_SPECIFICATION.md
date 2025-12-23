# 📋 Technical Specification — AI Toolkit v3.3

> This document is the **ROADMAP** — the strategic vision for the project.

---

## 🎯 Vision

AI Toolkit creates Python projects optimized for AI assistants by:
1. Keeping virtual environments **outside** the project directory
2. Providing strict ignore rules to minimize AI context pollution
3. Generating AI-friendly configuration files for all major IDEs

---

## 📦 Phases

### Phase 0: Core Infrastructure [COMPLETED] ✅

- [x] Project structure (`src/`, `templates/`, `scripts/`)
- [x] CLI entry point (`main.py`, `src/cli.py`)
- [x] Configuration system (`src/core/config.py`)
- [x] Constants and templates (`src/core/constants.py`)
- [x] File utilities (`src/core/file_utils.py`)
- [x] Color output (`src/core/constants.py` → COLORS)

### Phase 1: Project Generation [COMPLETED] ✅

- [x] `create` command — generate new projects
- [x] Template system (bot, webapp, fastapi, parser, monorepo)
- [x] AI config generators (`.cursorrules`, `CLAUDE.md`, copilot)
- [x] Script generators (`bootstrap.sh`, `health_check.sh`)
- [x] Docker generators (`Dockerfile`, `docker-compose.yml`)
- [x] CI/CD generators (GitHub Actions)
- [x] Git initialization

### Phase 2: Doctor Mode & Optimization [COMPLETED] ✅

- [x] `cleanup` command — analyze and fix existing projects
- [x] `migrate` command — add AI Toolkit to existing projects
- [x] `health` command — health check
- [x] `update` command — update to latest version
- [x] `review` command — 🦊 Fox security scanner
- [x] `wizard` command — interactive TUI
- [x] `pack` command — 📦 XML context packer
- [x] Metrics module (`src/utils/metrics.py`)
- [x] Cleaner module (`src/utils/cleaner.py`)
- [x] Context Map AST (`src/utils/context_map.py`)
- [x] Hooks module (`src/commands/hooks.py`)
- [x] Token benchmark (`benchmark.py`)
- [x] The Ultimate Doctor (7-step optimization flow)

### Phase 2.5: The Fox Update (v3.3) [COMPLETED] ✅

- [x] 🧠 AST-based context map (replaces regex)
- [x] 🦊 Fox security scanner (detects secrets)
- [x] 📦 XML Context Packer (for AI sharing)
- [x] Pre-commit hook with Fox guard
- [x] 🔍 Fox Trace (deep dependency tracker)

### Phase 3: Advanced TUI [PLANNED] 🔜

- [ ] Full-screen TUI mode (textual/rich)
- [ ] Real-time token monitoring
- [ ] Project dashboard
- [ ] Plugin management UI

### Phase 4: Ecosystem [FUTURE] 📅

- [ ] Plugin marketplace
- [ ] Template marketplace
- [ ] Cloud sync for settings
- [ ] Team collaboration features

---

## 🏗️ Architecture

```
ai_toolkit/
├── src/
│   ├── cli.py              # Main CLI entry point
│   ├── core/               # Shared utilities
│   │   ├── config.py       # User configuration
│   │   ├── constants.py    # VERSION, TEMPLATES, IDE_CONFIGS
│   │   └── file_utils.py   # File operations
│   ├── commands/           # CLI commands
│   │   ├── create.py       # Project creation
│   │   ├── cleanup.py      # Project cleanup
│   │   ├── migrate.py      # Project migration
│   │   ├── health.py       # Health check
│   │   ├── update.py       # Update project
│   │   ├── review.py       # AI review prompt
│   │   ├── wizard.py       # Interactive wizard
│   │   └── hooks.py        # Git hooks
│   ├── generators/         # File generators
│   │   ├── ai_configs.py   # AI IDE configs
│   │   ├── docker.py       # Docker files
│   │   ├── ci_cd.py        # CI/CD workflows
│   │   ├── git.py          # Git files
│   │   ├── scripts.py      # Shell scripts
│   │   └── project_files.py# Project files
│   └── utils/              # Utility modules
│       ├── metrics.py      # Token scanning
│       └── cleaner.py      # Artifact archiving
├── templates/              # Output templates
├── scripts/                # Toolkit scripts
├── docs/                   # Documentation
└── tests/                  # Test suite
```

---

## 📚 Development Standards

### Source of Truth

1. **Strategy:** This file (`TECHNICAL_SPECIFICATION.md`) is the Roadmap
2. **Tactics:** `_AI_INCLUDE/WHERE_THINGS_LIVE.md` is the Law
3. **Status:** `PROJECT_STATUS.md` tracks completion

### Code Standards

- Python 3.10+ with type hints
- English only (no Russian text)
- PEP 8 formatting
- Docstrings for all public functions
- 100% test coverage for commands

### File Locations

See `_AI_INCLUDE/WHERE_THINGS_LIVE.md` for the complete guide.

---

*Last updated: v3.3 — The Fox Update*
