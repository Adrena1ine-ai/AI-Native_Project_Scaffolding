"""
Генератор Git файлов и инициализация репозитория
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from datetime import datetime

from ..core.file_utils import create_file
from ..core.constants import COLORS


def generate_gitignore(project_dir: Path, project_name: str) -> None:
    """Генерация .gitignore"""
    date = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Git Ignore — {project_name}
# Generated: {date}

# ══════════════════════════════════════
# Python
# ══════════════════════════════════════
venv/
.venv/
env/
.env/
**/.venv*/
**/site-packages/

__pycache__/
*.py[cod]
*$py.class
*.so

.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ══════════════════════════════════════
# Testing
# ══════════════════════════════════════
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/

# ══════════════════════════════════════
# Type checking & Linting
# ══════════════════════════════════════
.mypy_cache/
.dmypy.json
dmypy.json
.ruff_cache/
.pytype/

# ══════════════════════════════════════
# Secrets & Environment
# ══════════════════════════════════════
.env
.env.local
.env.*.local
*.pem
*.key
secrets.json
credentials.json

# ══════════════════════════════════════
# Logs & Data
# ══════════════════════════════════════
logs/
*.log
*.log.*

data/
*.csv
*.jsonl
*.db
*.sqlite
*.sqlite3

# ══════════════════════════════════════
# IDE & Editors
# ══════════════════════════════════════
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# ══════════════════════════════════════
# OS
# ══════════════════════════════════════
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini

# ══════════════════════════════════════
# Frontend (if applicable)
# ══════════════════════════════════════
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next/
dist/
build/

# ══════════════════════════════════════
# Docker
# ══════════════════════════════════════
.docker/

# ══════════════════════════════════════
# Playwright
# ══════════════════════════════════════
**/playwright/driver/
playwright-report/
test-results/
"""
    create_file(project_dir / ".gitignore", content)


def generate_gitattributes(project_dir: Path) -> None:
    """Генерация .gitattributes"""
    content = """# Git Attributes

# Auto detect text files and perform LF normalization
* text=auto

# Python
*.py text diff=python
*.pyw text diff=python
*.pyx text diff=python
*.pxd text diff=python
*.pxi text diff=python

# Scripts
*.sh text eol=lf
*.bash text eol=lf
*.ps1 text eol=crlf

# Configs
*.json text
*.yaml text
*.yml text
*.toml text
*.ini text
*.cfg text
*.conf text

# Documentation
*.md text diff=markdown
*.txt text
*.rst text

# Web
*.html text diff=html
*.css text diff=css
*.js text
*.jsx text
*.ts text
*.tsx text

# Binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.webp binary
*.pdf binary
*.zip binary
*.gz binary
*.tar binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary

# SQLite
*.db binary
*.sqlite binary
*.sqlite3 binary
"""
    create_file(project_dir / ".gitattributes", content)


def init_git_repo(project_dir: Path, project_name: str, initial_commit: bool = True) -> bool:
    """
    Инициализировать Git репозиторий
    
    Args:
        project_dir: Путь к проекту
        project_name: Название проекта
        initial_commit: Создать первый коммит
        
    Returns:
        True если успешно
    """
    print(f"\n{COLORS.colorize('🔗 Git...', COLORS.CYAN)}")
    
    # Генерируем файлы
    generate_gitignore(project_dir, project_name)
    generate_gitattributes(project_dir)
    
    try:
        # git init
        result = subprocess.run(
            ["git", "init"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  {COLORS.warning('git init failed')}")
            return False
        
        print(f"  {COLORS.success('git init')}")
        
        # Настраиваем main как default branch
        subprocess.run(
            ["git", "branch", "-M", "main"],
            cwd=project_dir,
            capture_output=True
        )
        
        if initial_commit:
            # git add .
            subprocess.run(
                ["git", "add", "."],
                cwd=project_dir,
                capture_output=True
            )
            
            # git commit
            result = subprocess.run(
                ["git", "commit", "-m", f"🎉 Initial commit — {project_name}\n\nGenerated by AI Toolkit v3.0"],
                cwd=project_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  {COLORS.success('Initial commit created')}")
            else:
                # Возможно git не настроен (user.email, user.name)
                print(f"  {COLORS.warning('Commit skipped (configure git user first)')}")
        
        return True
        
    except FileNotFoundError:
        print(f"  {COLORS.warning('git not installed')}")
        return False
    except Exception as e:
        print(f"  {COLORS.error(f'Git error: {e}')}")
        return False
