"""
🌐 AI-Native Project Scaffolding Web Dashboard — FastAPI Backend

Web interface for project management with i18n support.
"""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS, CLEANUP_LEVELS
from src.core.config import set_default_ide, get_default_ide, get_default_ai_targets, get_language, set_language, is_first_run
from src.core.file_utils import get_dir_size
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project
from src.commands.update import update_project

from .i18n import get_translations, EN, RU


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
# Helper Functions
# ══════════════════════════════════════════════════════════════

def get_lang_from_request(request: Request) -> str:
    """Get language from query param, cookie, or default."""
    # Check query param first
    lang = request.query_params.get("lang")
    if lang in ("en", "ru"):
        return lang
    
    # Check cookie
    lang = request.cookies.get("lang")
    if lang in ("en", "ru"):
        return lang
    
    # Use global setting or default to English
    return get_language() or "en"


def get_template_context(request: Request, **extra: Any) -> dict[str, Any]:
    """Get common template context with translations."""
    lang = get_lang_from_request(request)
    translations = get_translations(lang)
    
    return {
        "request": request,
        "version": VERSION,
        "lang": lang,
        "t": translations,
        "templates": TEMPLATES,
        "ide_configs": IDE_CONFIGS,
        "cleanup_levels": CLEANUP_LEVELS,
        "current_ide": get_default_ide(),
        "home_path": str(Path.home()),
        **extra,
    }


def detect_ides_in_project(project_path: Path) -> dict[str, bool]:
    """
    Detect which IDE configs exist in a project.
    
    Returns dict like:
    {
        "cursor": True,
        "copilot": True,
        "claude": False,
        "windsurf": False
    }
    """
    detected = {
        "cursor": False,
        "copilot": False,
        "claude": False,
        "windsurf": False,
    }
    
    if not project_path.exists():
        return detected
    
    # Check for Cursor
    if (project_path / ".cursorrules").exists() or (project_path / ".cursorignore").exists():
        detected["cursor"] = True
    
    # Check for Copilot
    copilot_file = project_path / ".github" / "copilot-instructions.md"
    if copilot_file.exists():
        detected["copilot"] = True
    
    # Check for Claude
    if (project_path / "CLAUDE.md").exists():
        detected["claude"] = True
    
    # Check for Windsurf
    if (project_path / ".windsurfrules").exists():
        detected["windsurf"] = True
    
    return detected


# ══════════════════════════════════════════════════════════════
# Application
# ══════════════════════════════════════════════════════════════

def create_app() -> FastAPI:
    """Create FastAPI application"""
    
    app = FastAPI(
        title="AI-Native Project Scaffolding Dashboard",
        description="Web interface for managing AI-friendly projects",
        version=VERSION,
    )
    
    # Static files
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Templates
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    templates = Jinja2Templates(directory=str(templates_dir))
    
    # ══════════════════════════════════════════════════════════════
    # Language Switch
    # ══════════════════════════════════════════════════════════════
    
    @app.get("/set-lang/{lang}")
    async def set_lang(lang: str, request: Request):
        """Set language and redirect back."""
        if lang not in ("en", "ru"):
            lang = "en"
        
        set_language(lang)
        
        # Check for ?next= parameter
        next_url = request.query_params.get("next")
        if next_url:
            redirect_url = next_url
        else:
            # Get referer or redirect to home
            referer = request.headers.get("referer", "/")
            
            # Remove old lang param from referer
            if "?" in referer:
                base, params = referer.split("?", 1)
                params_list = [p for p in params.split("&") if not p.startswith("lang=")]
                if params_list:
                    referer = f"{base}?{'&'.join(params_list)}"
                else:
                    referer = base
            redirect_url = referer
        
        response = RedirectResponse(url=redirect_url, status_code=302)
        response.set_cookie("lang", lang, max_age=31536000)  # 1 year
        response.set_cookie("welcomed", "true", max_age=31536000)  # Mark as welcomed
        return response
    
    # ══════════════════════════════════════════════════════════════
    # Welcome Screen
    # ══════════════════════════════════════════════════════════════
    
    @app.get("/welcome", response_class=HTMLResponse)
    async def welcome_page(request: Request):
        """Welcome page with language selection"""
        return templates.TemplateResponse("welcome.html", {
            "request": request,
            "version": VERSION,
        })
    
    # ══════════════════════════════════════════════════════════════
    # HTML Pages
    # ══════════════════════════════════════════════════════════════
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Home page - redirects to welcome if first visit"""
        # Check if user has been welcomed (has lang cookie)
        welcomed = request.cookies.get("welcomed")
        lang_cookie = request.cookies.get("lang")
        
        if not welcomed and not lang_cookie:
            # First visit - show welcome screen
            return RedirectResponse(url="/welcome", status_code=302)
        
        context = get_template_context(request)
        return templates.TemplateResponse("index.html", context)
    
    @app.get("/create", response_class=HTMLResponse)
    async def create_page(request: Request):
        """Create project page"""
        context = get_template_context(request)
        return templates.TemplateResponse("create.html", context)
    
    @app.get("/cleanup", response_class=HTMLResponse)
    async def cleanup_page(request: Request):
        """Cleanup page"""
        context = get_template_context(request)
        return templates.TemplateResponse("cleanup.html", context)
    
    @app.get("/health", response_class=HTMLResponse)
    async def health_page(request: Request):
        """Health check page"""
        context = get_template_context(request)
        return templates.TemplateResponse("health.html", context)
    
    @app.get("/settings", response_class=HTMLResponse)
    async def settings_page(request: Request):
        """Settings page"""
        context = get_template_context(request)
        return templates.TemplateResponse("settings.html", context)
    
    @app.get("/help", response_class=HTMLResponse)
    async def help_page(request: Request):
        """Help page"""
        context = get_template_context(request)
        return templates.TemplateResponse("help.html", context)
    
    # ══════════════════════════════════════════════════════════════
    # API Endpoints
    # ══════════════════════════════════════════════════════════════
    
    @app.post("/api/create")
    async def api_create_project(data: CreateProjectRequest):
        """API: Create project"""
        try:
            # Set IDE
            ide_config = IDE_CONFIGS.get(data.ide, IDE_CONFIGS["all"])
            set_default_ide(data.ide, ide_config["ai_targets"])
            
            # Create project
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
                    "message": f"Project {data.name} created!",
                    "path": str(project_path),
                    "next_steps": [
                        f"cd {project_path}",
                        "./scripts/bootstrap.sh",
                        f"source ../_venvs/{data.name}-venv/bin/activate",
                        "cp .env.example .env",
                    ]
                }
            else:
                return {"success": False, "message": "Failed to create project"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/analyze")
    async def api_analyze(data: ProjectPath):
        """API: Analyze project"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            issues = analyze_project(path)
            
            # Also detect IDEs
            detected_ides = detect_ides_in_project(path)
            
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
                ],
                "detected_ides": detected_ides,
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/detect-ides")
    async def api_detect_ides(data: ProjectPath):
        """API: Detect IDE configs in project"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            detected = detect_ides_in_project(path)
            detected_list = [ide for ide, found in detected.items() if found]
            
            return {
                "success": True,
                "project_name": path.name,
                "detected_ides": detected,
                "detected_list": detected_list,
                "has_any": any(detected.values()),
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/cleanup")
    async def api_cleanup(data: CleanupRequest):
        """API: Cleanup project"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            result = cleanup_project(path, data.level)
            
            return {
                "success": result,
                "message": "Cleanup complete!" if result else "Cleanup failed"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/health")
    async def api_health(data: ProjectPath):
        """API: Health check"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            # Capture output
            import io
            import re
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            try:
                result = health_check(path)
            finally:
                output = buffer.getvalue()
                sys.stdout = old_stdout
            
            # Remove ANSI codes
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
        """API: Migrate project"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            result = migrate_project(path, get_default_ai_targets())
            
            return {
                "success": result,
                "message": "Migration complete!" if result else "Migration failed"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/update")
    async def api_update(data: ProjectPath):
        """API: Update project"""
        try:
            path = Path(data.path)
            if not path.exists():
                return {"success": False, "message": "Path does not exist"}
            
            result = update_project(path)
            
            return {
                "success": result,
                "message": f"Updated to v{VERSION}!" if result else "Update failed"
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/settings/ide")
    async def api_set_ide(ide: str = Form(...)):
        """API: Set IDE"""
        if ide not in IDE_CONFIGS:
            return {"success": False, "message": "Unknown IDE"}
        
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        return {
            "success": True,
            "message": f"IDE: {cfg['icon']} {cfg['name']}"
        }
    
    @app.get("/api/stats")
    async def api_stats():
        """API: Statistics"""
        # Find projects in home folder
        home = Path.home()
        projects = []
        
        # Check typical locations
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
    """Run server"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🌐 AI-Native Project Scaffolding Dashboard v{VERSION}     ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Open in browser: http://{host}:{port}                     ║
║                                                          ║
║  Press Ctrl+C to stop                                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Toolkit Dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    
    args = parser.parse_args()
    
    run_server(
        host=args.host,
        port=args.port,
        open_browser=not args.no_browser
    )
