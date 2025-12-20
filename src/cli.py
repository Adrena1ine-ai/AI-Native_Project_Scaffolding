#!/usr/bin/env python3
"""
🛠️ AI Toolkit v3.0 — CLI
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path

from .core.constants import COLORS, VERSION, IDE_CONFIGS
from .core.config import set_default_ide, get_default_ide, get_default_ai_targets

from .commands import (
    cmd_create,
    cmd_cleanup,
    cmd_migrate,
    cmd_health,
    cmd_update,
    create_project,
    cleanup_project,
    migrate_project,
    health_check,
    update_project,
)


def print_header():
    """Заголовок"""
    print(f"""
{COLORS.colorize('═' * 60, COLORS.BLUE)}
{COLORS.colorize(f'🛠️  AI TOOLKIT v{VERSION}', COLORS.BLUE)}
{COLORS.colorize('═' * 60, COLORS.BLUE)}
""")


def select_ide() -> str:
    """Выбор IDE"""
    print(f"{COLORS.colorize('🖥️  В какой IDE будешь работать?', COLORS.MAGENTA)}\n")
    
    options = [
        ("cursor", "💜 Cursor (AI-first IDE)"),
        ("vscode_copilot", "💙 VS Code + GitHub Copilot"),
        ("vscode_claude", "🟢 VS Code + Claude"),
        ("windsurf", "🌊 Windsurf"),
        ("all", "🔄 Все сразу (универсальный)"),
    ]
    
    for i, (key, name) in enumerate(options, 1):
        print(f"  {COLORS.colorize(str(i) + '.', COLORS.CYAN)} {name}")
    print()
    
    while True:
        choice = input(f"Выбери (1-{len(options)}) [{COLORS.colorize('5', COLORS.GREEN)}]: ").strip()
        if not choice:
            choice = "5"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                key, name = options[idx]
                config = IDE_CONFIGS[key]
                set_default_ide(key, config["ai_targets"])
                print(f"\n  {COLORS.success(f'Выбрано: {config["icon"]} {config["name"]}')}\n")
                return key
        except (ValueError, IndexError):
            pass
        
        print(f"  {COLORS.error('Неверный выбор')}")


def print_menu():
    """Главное меню"""
    ide = get_default_ide()
    ide_config = IDE_CONFIGS.get(ide, {})
    
    print(f"IDE: {ide_config.get('icon', '')} {ide_config.get('name', ide)}\n")
    print("Что хочешь сделать?\n")
    
    items = [
        ("1", "🆕 Создать новый проект"),
        ("2", "🧹 Очистить существующий проект"),
        ("3", "📦 Мигрировать проект"),
        ("4", "🏥 Health check"),
        ("5", "⬆️  Обновить проект"),
        ("6", "⚙️  Сменить IDE"),
        ("0", "❌ Выход"),
    ]
    
    for key, name in items:
        print(f"  {COLORS.colorize(key + '.', COLORS.CYAN)} {name}")
    print()


def interactive_mode():
    """Интерактивный режим"""
    print_header()
    select_ide()
    
    commands = {
        "1": cmd_create,
        "2": cmd_cleanup,
        "3": cmd_migrate,
        "4": cmd_health,
        "5": cmd_update,
        "6": select_ide,
    }
    
    while True:
        print_menu()
        
        choice = input("Выбери (0-6): ").strip()
        
        if choice == "0":
            print(f"\n{COLORS.colorize('👋 Пока!', COLORS.CYAN)}\n")
            break
        
        if choice in commands:
            commands[choice]()
            print()
            cont = input("Продолжить? (Y/n): ").strip().lower()
            if cont == 'n':
                print(f"\n{COLORS.colorize('👋 Пока!', COLORS.CYAN)}\n")
                break
            print()
        else:
            print(f"  {COLORS.error('Неверный выбор')}")


def cli_mode():
    """CLI режим с аргументами"""
    parser = argparse.ArgumentParser(
        prog="ai-toolkit",
        description="🛠️ AI Toolkit — создание AI-friendly проектов",
    )
    parser.add_argument("-v", "--version", action="version", version=f"AI Toolkit v{VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="Команды")
    
    # create
    create_p = subparsers.add_parser("create", help="Создать проект")
    create_p.add_argument("name", help="Название проекта")
    create_p.add_argument("--path", "-p", type=Path, default=Path.cwd(), help="Путь")
    create_p.add_argument("--template", "-t", default="bot", 
                         choices=["bot", "webapp", "fastapi", "parser", "full", "monorepo"])
    create_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"],
                         choices=["cursor", "copilot", "claude", "windsurf"])
    create_p.add_argument("--no-docker", action="store_true", help="Без Docker")
    create_p.add_argument("--no-ci", action="store_true", help="Без CI/CD")
    create_p.add_argument("--no-git", action="store_true", help="Без Git")
    
    # dashboard (Web UI)
    dash_p = subparsers.add_parser("dashboard", aliases=["web", "ui"], help="Открыть Web Dashboard")
    dash_p.add_argument("--host", default="127.0.0.1", help="Хост (по умолчанию: 127.0.0.1)")
    dash_p.add_argument("--port", "-p", type=int, default=8080, help="Порт (по умолчанию: 8080)")
    dash_p.add_argument("--no-browser", action="store_true", help="Не открывать браузер")
    
    # cleanup
    cleanup_p = subparsers.add_parser("cleanup", help="Очистить проект")
    cleanup_p.add_argument("path", type=Path, help="Путь к проекту")
    cleanup_p.add_argument("--level", "-l", default="safe",
                          choices=["safe", "medium", "full"])
    
    # migrate
    migrate_p = subparsers.add_parser("migrate", help="Мигрировать проект")
    migrate_p.add_argument("path", type=Path, help="Путь к проекту")
    migrate_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"])
    
    # health
    health_p = subparsers.add_parser("health", help="Health check")
    health_p.add_argument("path", type=Path, help="Путь к проекту")
    
    # update
    update_p = subparsers.add_parser("update", help="Обновить проект")
    update_p.add_argument("path", type=Path, help="Путь к проекту")
    
    args = parser.parse_args()
    
    if not args.command:
        interactive_mode()
        return
    
    if args.command == "create":
        set_default_ide("all", args.ai)
        create_project(
            name=args.name,
            path=args.path,
            template=args.template,
            ai_targets=args.ai,
            include_docker=not args.no_docker,
            include_ci=not args.no_ci,
            include_git=not args.no_git,
        )
    
    elif args.command == "cleanup":
        from .commands.cleanup import analyze_project
        print(f"\n{COLORS.colorize('🔍 Анализирую...', COLORS.CYAN)}\n")
        issues = analyze_project(args.path)
        for issue in issues:
            print(f"   {issue}")
        if args.level != "safe":
            cleanup_project(args.path, args.level)
    
    elif args.command == "migrate":
        migrate_project(args.path, args.ai)
    
    elif args.command == "health":
        health_check(args.path)
    
    elif args.command == "update":
        update_project(args.path)
    
    elif args.command in ("dashboard", "web", "ui"):
        try:
            from web.app import run_server
            run_server(
                host=args.host,
                port=args.port,
                open_browser=not args.no_browser
            )
        except ImportError:
            print(f"{COLORS.error('Не установлены зависимости для Dashboard!')}")
            print(f"Установи: {COLORS.colorize('pip install fastapi uvicorn jinja2', COLORS.CYAN)}")


def main():
    """Entry point"""
    try:
        if len(sys.argv) > 1:
            cli_mode()
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print(f"\n\n{COLORS.colorize('👋 Пока!', COLORS.CYAN)}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
