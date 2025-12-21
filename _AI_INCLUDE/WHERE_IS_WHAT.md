# 📍 Where Is What — AI Toolkit

## Quick Navigation for AI

---

### 🎯 I want to change...

| What | Where |
|------|-------|
| **Template list** | `src/core/constants.py` → `TEMPLATES` |
| **IDE list** | `src/core/constants.py` → `IDE_CONFIGS` |
| **Cleanup levels** | `src/core/constants.py` → `CLEANUP_LEVELS` |
| **Version** | `src/core/constants.py` → `VERSION` |
| **Terminal colors** | `src/core/constants.py` → `COLORS` |

---

### 📄 File Generation

| Project File | Generator |
|--------------|-----------|
| `.cursorrules` | `generators/ai_configs.py` → `generate_cursor_rules()` |
| `.cursorignore` | `generators/ai_configs.py` → `generate_cursor_ignore()` |
| `copilot-instructions.md` | `generators/ai_configs.py` → `generate_copilot_instructions()` |
| `CLAUDE.md` | `generators/ai_configs.py` → `generate_claude_md()` |
| `_AI_INCLUDE/` | `generators/ai_configs.py` → `generate_ai_include()` |
| `bootstrap.sh` | `generators/scripts.py` → `generate_bootstrap_sh()` |
| `health_check.sh` | `generators/scripts.py` → `generate_health_check()` |
| `context.py` | `generators/scripts.py` → `generate_context_switcher()` |
| `Dockerfile` | `generators/docker.py` → `generate_dockerfile()` |
| `docker-compose.yml` | `generators/docker.py` → `generate_docker_compose()` |
| `ci.yml` | `generators/ci_cd.py` → `generate_ci_workflow()` |
| `cd.yml` | `generators/ci_cd.py` → `generate_cd_workflow()` |
| `.pre-commit-config.yaml` | `generators/ci_cd.py` → `generate_pre_commit_config()` |
| `.gitignore` | `generators/git.py` → `generate_gitignore()` |
| `requirements.txt` | `generators/project_files.py` → `generate_requirements()` |
| `config.py` | `generators/project_files.py` → `generate_config_py()` |
| `README.md` | `generators/project_files.py` → `generate_readme()` |

---

### 🤖 Project Modules

| Module | Generator |
|--------|-----------|
| `bot/` | `commands/create.py` → `generate_bot_module()` |
| `database/` | `commands/create.py` → `generate_database_module()` |
| `api/` | `commands/create.py` → `generate_api_module()` |
| `webapp/` | `commands/create.py` → `generate_webapp_module()` |
| `parser/` | `commands/create.py` → `generate_parser_module()` |

---

### 🖥️ CLI

| Command | Interactive | CLI |
|---------|-------------|-----|
| create | `commands/create.py` → `cmd_create()` | `--template --ai --path` |
| cleanup | `commands/cleanup.py` → `cmd_cleanup()` | `--level` |
| migrate | `commands/migrate.py` → `cmd_migrate()` | `--ai` |
| health | `commands/health.py` → `cmd_health()` | path |
| update | `commands/update.py` → `cmd_update()` | path |

---

### 📦 Imports

```python
# Core
from src.core.constants import COLORS, VERSION, TEMPLATES, IDE_CONFIGS
from src.core.config import get_config, get_default_ide, get_default_ai_targets
from src.core.file_utils import create_file, make_executable

# Generators
from src.generators import (
    generate_ai_configs,
    generate_scripts,
    generate_docker_files,
    generate_ci_files,
    init_git_repo,
)

# Commands
from src.commands import (
    create_project,
    cleanup_project,
    migrate_project,
    health_check,
    update_project,
)
```

---

### 🧪 Tests

```
tests/
├── test_create.py      # Creation tests
├── test_cleanup.py     # Cleanup tests
├── test_generators.py  # Generator tests
└── conftest.py         # Fixtures
```

---

### 📚 Documentation

```
docs/
├── manifesto.md        # Philosophy (copied to projects)
├── templates.md        # Template descriptions
├── prompts.md          # AI prompts
└── api.md              # API documentation
```
