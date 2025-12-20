# 📍 Where Is What — AI Toolkit

## Быстрая навигация для AI

---

### 🎯 Хочу изменить...

| Что | Где |
|-----|-----|
| **Список шаблонов** | `src/core/constants.py` → `TEMPLATES` |
| **Список IDE** | `src/core/constants.py` → `IDE_CONFIGS` |
| **Уровни очистки** | `src/core/constants.py` → `CLEANUP_LEVELS` |
| **Версию** | `src/core/constants.py` → `VERSION` |
| **Цвета терминала** | `src/core/constants.py` → `COLORS` |

---

### 📄 Генерация файлов

| Файл проекта | Генератор |
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

### 🤖 Модули проекта

| Модуль | Генератор |
|--------|-----------|
| `bot/` | `commands/create.py` → `generate_bot_module()` |
| `database/` | `commands/create.py` → `generate_database_module()` |
| `api/` | `commands/create.py` → `generate_api_module()` |
| `webapp/` | `commands/create.py` → `generate_webapp_module()` |
| `parser/` | `commands/create.py` → `generate_parser_module()` |

---

### 🖥️ CLI

| Команда | Интерактивная | CLI |
|---------|---------------|-----|
| create | `commands/create.py` → `cmd_create()` | `--template --ai --path` |
| cleanup | `commands/cleanup.py` → `cmd_cleanup()` | `--level` |
| migrate | `commands/migrate.py` → `cmd_migrate()` | `--ai` |
| health | `commands/health.py` → `cmd_health()` | path |
| update | `commands/update.py` → `cmd_update()` | path |

---

### 📦 Импорты

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

### 🧪 Тесты

```
tests/
├── test_create.py      # Тесты создания
├── test_cleanup.py     # Тесты очистки
├── test_generators.py  # Тесты генераторов
└── conftest.py         # Fixtures
```

---

### 📚 Документация

```
docs/
├── manifesto.md        # Философия (копируется в проекты)
├── templates.md        # Описание шаблонов
├── prompts.md          # Промпты для AI
└── api.md              # API документация
```
