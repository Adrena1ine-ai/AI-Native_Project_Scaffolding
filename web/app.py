"""
🌐 AI Toolkit Web Dashboard — FastAPI Backend

Веб-интерфейс для управления проектами.
"""

from __future__ import annotations

import sys
import asyncio
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import Any

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS, CLEANUP_LEVELS
from src.core.config import set_default_ide, get_default_ide, get_default_ai_targets
from src.core.file_utils import get_dir_size
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project
from src.commands.update import update_project


# ══════════════════════════════════════════════════════════════
# Pydantic Models
# ══════════════════════════════════════════════════════════════

class CreateProjectRequest(BaseModel):
    name: str
    path: str
    template: str = "bot"
    ide: str = "all"
    include_docker: bool = True
    include_ci: bool = True
    include_git: bool = True


class CleanupRequest(BaseModel):
    path: str
    level: str = "safe"


class ProjectPath(BaseModel):
    path: str


# ══════════════════════════════════════════════════════════════
# Application
# ══════════════════════════════════════════════════════════════

def create_app() -> FastAPI:
    """Создать FastAPI приложение"""
    
    app = FastAPI(
        title="AI Toolkit Dashboard",
        description="Веб-интерфейс для управления AI-friendly проектами",
        version=VERSION,
    )
    
    # Статические файлы
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Templates
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    templates = Jinja2Templates(directory=str(templates_dir))
    
    # ══════════════════════════════════════════════════════════════
    # HTML Pages
    # ══════════════════════════════════════════════════════════════
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Главная страница"""
        return templates.TemplateResponse("index.html", {
            "request": request,
            "version": VERSION,
            "templates": TEMPLATES,
            "ide_configs": IDE_CONFIGS,
            "cleanup_levels": CLEANUP_LEVELS,
            "current_ide": get_default_ide(),
            "home_path": str(Path.home()),
        })
    
    @app.get("/create", response_class=HTMLResponse)
    async def create_page(request: Request):
        """Страница создания проекта"""
        return templates.TemplateResponse("create.html", {
            "request": request,
            "version": VERSION,
            "templates": TEMPLATES,
            "ide_configs": IDE_CONFIGS,
            "home_path": str(Path.home()),
        })
    
    @app.get("/cleanup", response_class=HTMLResponse)
    async def cleanup_page(request: Request):
        """Страница очистки"""
        return templates.TemplateResponse("cleanup.html", {
            "request": request,
            "version": VERSION,
            "cleanup_levels": CLEANUP_LEVELS,
            "home_path": str(Path.home()),
        })
    
    @app.get("/health", response_class=HTMLResponse)
    async def health_page(request: Request):
        """Страница health check"""
        return templates.TemplateResponse("health.html", {
            "request": request,
            "version": VERSION,
            "home_path": str(Path.home()),
        })
    
    @app.get("/settings", response_class=HTMLResponse)
    async def settings_page(request: Request):
        """Страница настроек"""
        return templates.TemplateResponse("settings.html", {
            "request": request,
            "version": VERSION,
            "ide_configs": IDE_CONFIGS,
            "current_ide": get_default_ide(),
        })
    
    @app.get("/help", response_class=HTMLResponse)
    async def help_page(request: Request):
        """Страница помощи"""
        return templates.TemplateResponse("help.html", {
            "request": request,
            "version": VERSION,
        })
    
    # ══════════════════════════════════════════════════════════════
    # API Endpoints
    # ══════════════════════════════════════════════════════════════
    
    @app.post("/api/create")
    async def api_create_project(data: CreateProjectRequest):
        """API: Создать проект"""
        try:
            # Устанавливаем IDE
            ide_config = IDE_CONFIGS.get(data.ide, IDE_CONFIGS["all"])
            set_default_ide(data.ide, ide_config["ai_targets"])
            
            # Создаём проект
            result = create_project(
                name=data.name,
                path=Path(data.path),
                template=data.template,
                ai_targets=ide_config["ai_targets"],
                include_docker=data.include_docker,
                include_ci=data.include_ci,
                include_git=data.include_git,
            )
            
            if result:
                project_path = Path(data.path) / data.name
                return {
                    "success": True,
                    "message": f"Проект {data.name} создан!",
                    "path": str(project_path),
                    "next_steps": [
                        f"cd {project_path}",
                        "./scripts/bootstrap.sh",
                        f"source ../_venvs/{data.name}-venv/bin/activate",
                        "cp .env.example .env",
                    ]
                }
            else:
                return {"success": False, "message": "Не удалось создать проект"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/analyze")
    async def api_analyze(data: ProjectPath):
        """API: Анализ проекта"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Путь не существует"}
            
            issues = analyze_project(path)
            
            return {
                "success": True,
                "project_name": path.name,
                "issues_count": len(issues),
                "issues": [
                    {
                        "type": i.type,
                        "severity": i.severity,
                        "message": i.message,
                        "size_mb": round(i.size_mb, 1),
                        "path": str(i.path) if i.path else None,
                    }
                    for i in issues
                ]
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/cleanup")
    async def api_cleanup(data: CleanupRequest):
        """API: Очистка проекта"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Путь не существует"}
            
            result = cleanup_project(path, data.level)
            
            return {
                "success": result,
                "message": "Очистка завершена!" if result else "Ошибка очистки"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/health")
    async def api_health(data: ProjectPath):
        """API: Health check"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Путь не существует"}
            
            # Перехватываем вывод
            import io
            import re
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            try:
                result = health_check(path)
            finally:
                output = buffer.getvalue()
                sys.stdout = old_stdout
            
            # Убираем ANSI коды
            clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
            
            return {
                "success": True,
                "passed": result,
                "output": clean_output,
                "project_name": path.name,
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/migrate")
    async def api_migrate(data: ProjectPath):
        """API: Миграция проекта"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Путь не существует"}
            
            result = migrate_project(path, get_default_ai_targets())
            
            return {
                "success": result,
                "message": "Миграция завершена!" if result else "Ошибка миграции"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/update")
    async def api_update(data: ProjectPath):
        """API: Обновление проекта"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Путь не существует"}
            
            result = update_project(path)
            
            return {
                "success": result,
                "message": f"Обновлено до v{VERSION}!" if result else "Ошибка обновления"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/settings/ide")
    async def api_set_ide(ide: str = Form(...)):
        """API: Установить IDE"""
        if ide not in IDE_CONFIGS:
            return {"success": False, "message": "Неизвестная IDE"}
        
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        return {
            "success": True,
            "message": f"IDE: {cfg['icon']} {cfg['name']}"
        }
    
    @app.get("/api/stats")
    async def api_stats():
        """API: Статистика"""
        # Ищем проекты в домашней папке
        home = Path.home()
        projects = []
        
        # Проверяем типичные места
        for check_dir in [home, home / "projects", home / "dev", Path("/opt/bots")]:
            if check_dir.exists():
                for item in check_dir.iterdir():
                    if item.is_dir() and (item / ".toolkit-version").exists():
                        try:
                            version = (item / ".toolkit-version").read_text().strip()
                            size = get_dir_size(item)
                            projects.append({
                                "name": item.name,
                                "path": str(item),
                                "version": version,
                                "size_mb": round(size, 1),
                            })
                        except:
                            pass
        
        return {
            "success": True,
            "projects_count": len(projects),
            "projects": projects,
            "toolkit_version": VERSION,
        }
    
    return app


def run_server(host: str = "127.0.0.1", port: int = 8080, open_browser: bool = True):
    """Запустить сервер"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🌐 AI Toolkit Dashboard v{VERSION}                        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Открой в браузере: http://{host}:{port}                 ║
║                                                          ║
║  Нажми Ctrl+C чтобы остановить                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    run_server()

