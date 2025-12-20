"""
Генератор Docker файлов
"""

from __future__ import annotations

from pathlib import Path

from ..core.file_utils import create_file
from ..core.constants import COLORS


def generate_dockerfile(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация Dockerfile"""
    
    # Определяем команду запуска в зависимости от шаблона
    cmd_map = {
        "bot": 'CMD ["python", "bot/main.py"]',
        "webapp": 'CMD ["python", "-m", "http.server", "8000", "--directory", "webapp"]',
        "fastapi": 'CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]',
        "parser": 'CMD ["python", "parser/main.py"]',
        "full": 'CMD ["python", "bot/main.py"]',
    }
    
    cmd = cmd_map.get(template, 'CMD ["python", "main.py"]')
    
    # Дополнительные пакеты для разных шаблонов
    extra_packages = ""
    if template in ["parser", "full"]:
        extra_packages = """
# Playwright (если нужен)
# RUN pip install playwright && playwright install chromium --with-deps
"""
    
    content = f"""# Dockerfile — {project_name}
# Build: docker build -t {project_name} .
# Run: docker run -d --env-file .env {project_name}

FROM python:3.12-slim

# Метаданные
LABEL maintainer="your@email.com"
LABEL version="1.0.0"
LABEL description="{project_name}"

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Рабочая директория
WORKDIR /app

# Установка системных зависимостей (если нужны)
# RUN apt-get update && apt-get install -y --no-install-recommends \\
#     gcc \\
#     && rm -rf /var/lib/apt/lists/*
{extra_packages}
# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаём непривилегированного пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открываем порт (если нужен)
# EXPOSE 8000

# Команда запуска
{cmd}
"""
    create_file(project_dir / "Dockerfile", content)


def generate_docker_compose(project_dir: Path, project_name: str, template: str) -> None:
    """Генерация docker-compose.yml"""
    
    # Дополнительные сервисы
    extra_services = ""
    
    if template in ["bot", "full", "fastapi"]:
        extra_services = f"""
  # Redis (раскомментируй если нужен)
  # redis:
  #   image: redis:7-alpine
  #   restart: unless-stopped
  #   volumes:
  #     - redis_data:/data

  # PostgreSQL (раскомментируй если нужен)
  # postgres:
  #   image: postgres:16-alpine
  #   restart: unless-stopped
  #   environment:
  #     POSTGRES_USER: ${{POSTGRES_USER:-{project_name}}}
  #     POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:-secret}}
  #     POSTGRES_DB: ${{POSTGRES_DB:-{project_name}}}
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
"""

    volumes_section = """
# volumes:
#   redis_data:
#   postgres_data:
""" if extra_services else ""

    # Порты
    ports = ""
    if template in ["webapp", "fastapi"]:
        ports = """
    ports:
      - "8000:8000"
"""

    content = f"""# Docker Compose — {project_name}
# Start: docker-compose up -d
# Logs: docker-compose logs -f
# Stop: docker-compose down

version: "3.8"

services:
  {project_name}:
    build: .
    container_name: {project_name}
    restart: unless-stopped
    env_file:
      - .env
{ports}
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    # depends_on:
    #   - redis
    #   - postgres
{extra_services}
{volumes_section}
"""
    create_file(project_dir / "docker-compose.yml", content)


def generate_dockerignore(project_dir: Path, project_name: str) -> None:
    """Генерация .dockerignore"""
    content = f"""# Docker Ignore — {project_name}

# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/
env/
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Tests
.pytest_cache/
.coverage
htmlcov/
.tox/

# Logs (монтируем как volume)
logs/
*.log

# Data (монтируем как volume)
data/
*.db
*.sqlite3

# Docker
Dockerfile
docker-compose*.yml
.docker/

# Documentation
docs/
*.md
!README.md

# AI configs (не нужны в контейнере)
_AI_INCLUDE/
.cursorrules
.cursorignore
CLAUDE.md
.windsurfrules
"""
    create_file(project_dir / ".dockerignore", content)


def generate_docker_files(project_dir: Path, project_name: str, template: str) -> None:
    """
    Создать все Docker файлы
    
    Args:
        project_dir: Путь к проекту
        project_name: Название проекта
        template: Шаблон проекта
    """
    print(f"\n{COLORS.colorize('🐳 Docker...', COLORS.CYAN)}")
    
    generate_dockerfile(project_dir, project_name, template)
    generate_docker_compose(project_dir, project_name, template)
    generate_dockerignore(project_dir, project_name)
