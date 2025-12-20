#!/usr/bin/env python3
"""
🛠️ AI-Native Project Scaffolding v3.0 — CLI
"""

from __future__ import annotations

import sys
import argparse
from pathlib import Path

from .core.constants import COLORS, VERSION, IDE_CONFIGS
from .core.config import (
    set_default_ide, 
    get_default_ide, 
    get_default_ai_targets,
    is_first_run,
    set_language,
    get_language,
)
from .core.i18n import t, select_language_prompt

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
    """Print header"""
    print(f"""
{COLORS.colorize('═' * 60, COLORS.BLUE)}
{COLORS.colorize(f'🛠️  AI-NATIVE PROJECT SCAFFOLDING v{VERSION}', COLORS.BLUE)}
{COLORS.colorize('═' * 60, COLORS.BLUE)}
""")


def select_ide() -> str:
    """IDE selection"""
    print(f"{COLORS.colorize(t('select_ide'), COLORS.MAGENTA)}\n")
    
    options = [
        ("cursor", t("ide_cursor")),
        ("vscode_copilot", t("ide_copilot")),
        ("vscode_claude", t("ide_claude")),
        ("windsurf", t("ide_windsurf")),
        ("all", t("ide_all")),
    ]
    
    for i, (key, name) in enumerate(options, 1):
        print(f"  {COLORS.colorize(str(i) + '.', COLORS.CYAN)} {name}")
    print()
    
    while True:
        prompt = t("choose_1_to_n", n=len(options), default="5")
        choice = input(prompt).strip()
        if not choice:
            choice = "5"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                key, name = options[idx]
                config = IDE_CONFIGS[key]
                set_default_ide(key, config["ai_targets"])
                print(f"\n  {COLORS.success(f'{t(\"ide_selected\")} {config[\"icon\"]} {config[\"name\"]}')}\n")
                return key
        except (ValueError, IndexError):
            pass
        
        print(f"  {COLORS.error(t('invalid_choice'))}")


def select_lang() -> str:
    """Language selection"""
    return select_language_prompt()


def print_menu():
    """Main menu"""
    ide = get_default_ide()
    ide_config = IDE_CONFIGS.get(ide, {})
    lang = get_language()
    
    print(f"{t('current_ide')} {ide_config.get('icon', '')} {ide_config.get('name', ide)}")
    print(f"🌍 {'English' if lang == 'en' else 'Русский'}\n")
    print(f"{t('what_to_do')}\n")
    
    items = [
        ("1", t("menu_create")),
        ("2", t("menu_cleanup")),
        ("3", t("menu_migrate")),
        ("4", t("menu_health")),
        ("5", t("menu_update")),
        ("6", t("menu_change_ide")),
        ("7", t("menu_change_lang")),
        ("0", t("menu_exit")),
    ]
    
    for key, name in items:
        print(f"  {COLORS.colorize(key + '.', COLORS.CYAN)} {name}")
    print()


def interactive_mode():
    """Interactive mode"""
    print_header()
    
    # First run - select language
    if is_first_run():
        select_language_prompt()
    
    select_ide()
    
    commands = {
        "1": cmd_create,
        "2": cmd_cleanup,
        "3": cmd_migrate,
        "4": cmd_health,
        "5": cmd_update,
        "6": select_ide,
        "7": select_lang,
    }
    
    while True:
        print_menu()
        
        choice = input(t("choose_0_to_n", n=7)).strip()
        
        if choice == "0":
            print(f"\n{COLORS.colorize(t('goodbye'), COLORS.CYAN)}\n")
            break
        
        if choice in commands:
            commands[choice]()
            print()
            cont = input(t("continue")).strip().lower()
            if cont == 'n':
                print(f"\n{COLORS.colorize(t('goodbye'), COLORS.CYAN)}\n")
                break
            print()
        else:
            print(f"  {COLORS.error(t('invalid_choice'))}")


def cli_mode():
    """CLI mode with arguments"""
    parser = argparse.ArgumentParser(
        prog="ai-toolkit",
        description=t("cli_description"),
    )
    parser.add_argument("-v", "--version", action="version", version=f"AI-Native Project Scaffolding v{VERSION}")
    parser.add_argument("--lang", choices=["en", "ru"], help="Set language")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # create
    create_p = subparsers.add_parser("create", help=t("cli_create_help"))
    create_p.add_argument("name", help=t("cli_arg_name"))
    create_p.add_argument("--path", "-p", type=Path, default=Path.cwd(), help=t("cli_arg_path"))
    create_p.add_argument("--template", "-t", default="bot", 
                         choices=["bot", "webapp", "fastapi", "parser", "full", "monorepo"],
                         help=t("cli_arg_template"))
    create_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"],
                         choices=["cursor", "copilot", "claude", "windsurf"])
    create_p.add_argument("--no-docker", action="store_true", help=t("cli_arg_no_docker"))
    create_p.add_argument("--no-ci", action="store_true", help=t("cli_arg_no_ci"))
    create_p.add_argument("--no-git", action="store_true", help=t("cli_arg_no_git"))
    
    # dashboard (Web UI)
    dash_p = subparsers.add_parser("dashboard", aliases=["web", "ui"], help=t("cli_dashboard_help"))
    dash_p.add_argument("--host", default="127.0.0.1", help=t("cli_arg_host"))
    dash_p.add_argument("--port", "-P", type=int, default=8080, help=t("cli_arg_port"))
    dash_p.add_argument("--no-browser", action="store_true", help=t("cli_arg_no_browser"))
    
    # cleanup
    cleanup_p = subparsers.add_parser("cleanup", help=t("cli_cleanup_help"))
    cleanup_p.add_argument("path", type=Path, help=t("cli_arg_path"))
    cleanup_p.add_argument("--level", "-l", default="safe",
                          choices=["safe", "medium", "full"], help=t("cli_arg_level"))
    
    # migrate
    migrate_p = subparsers.add_parser("migrate", help=t("cli_migrate_help"))
    migrate_p.add_argument("path", type=Path, help=t("cli_arg_path"))
    migrate_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"])
    
    # health
    health_p = subparsers.add_parser("health", help=t("cli_health_help"))
    health_p.add_argument("path", type=Path, help=t("cli_arg_path"))
    
    # update
    update_p = subparsers.add_parser("update", help=t("cli_update_help"))
    update_p.add_argument("path", type=Path, help=t("cli_arg_path"))
    
    args = parser.parse_args()
    
    # Set language if specified
    if hasattr(args, 'lang') and args.lang:
        set_language(args.lang)
    
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
        print(f"\n{COLORS.colorize(t('analyzing'), COLORS.CYAN)}\n")
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
            print(f"{COLORS.error(t('dashboard_deps_missing'))}")
            print(f"{t('dashboard_install')} {COLORS.colorize('pip install fastapi uvicorn jinja2', COLORS.CYAN)}")


def main():
    """Entry point"""
    try:
        if len(sys.argv) > 1:
            cli_mode()
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print(f"\n\n{COLORS.colorize(t('goodbye'), COLORS.CYAN)}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
