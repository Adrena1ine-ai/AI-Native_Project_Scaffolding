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
    cmd_review,
    create_project,
    cleanup_project,
    migrate_project,
    health_check,
    update_project,
    review_changes,
)


def print_header():
    """Print header"""
    print(f"""
{COLORS.colorize('═' * 60, COLORS.BLUE)}
{COLORS.colorize(f'🛠️  AI TOOLKIT v{VERSION}', COLORS.BLUE)}
{COLORS.colorize('═' * 60, COLORS.BLUE)}
""")


def select_ide() -> str:
    """IDE selection"""
    print(f"{COLORS.colorize('🖥️  Which IDE will you use?', COLORS.MAGENTA)}\n")
    
    options = [
        ("cursor", "💜 Cursor (AI-first IDE)"),
        ("vscode_copilot", "💙 VS Code + GitHub Copilot"),
        ("vscode_claude", "🟢 VS Code + Claude"),
        ("windsurf", "🌊 Windsurf"),
        ("all", "🔄 All (universal)"),
    ]
    
    for i, (key, name) in enumerate(options, 1):
        print(f"  {COLORS.colorize(str(i) + '.', COLORS.CYAN)} {name}")
    print()
    
    while True:
        choice = input(f"Choose (1-{len(options)}) [{COLORS.colorize('5', COLORS.GREEN)}]: ").strip()
        if not choice:
            choice = "5"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                key, name = options[idx]
                config = IDE_CONFIGS[key]
                set_default_ide(key, config["ai_targets"])
                icon = config["icon"]
                name = config["name"]
                print(f"\n  {COLORS.success(f'Selected: {icon} {name}')}\n")
                return key
        except (ValueError, IndexError):
            pass
        
        print(f"  {COLORS.error('Invalid choice')}")


def print_menu():
    """Main menu"""
    ide = get_default_ide()
    ide_config = IDE_CONFIGS.get(ide, {})
    
    print(f"IDE: {ide_config.get('icon', '')} {ide_config.get('name', ide)}\n")
    print("What would you like to do?\n")
    
    items = [
        ("1", "🆕 Create new project"),
        ("2", "🧹 Cleanup existing project"),
        ("3", "📦 Migrate project"),
        ("4", "🏥 Health check"),
        ("5", "⬆️  Update project"),
        ("6", "🔍 Review changes (AI prompt)"),
        ("7", "⚙️  Change IDE"),
        ("0", "❌ Exit"),
    ]
    
    for key, name in items:
        print(f"  {COLORS.colorize(key + '.', COLORS.CYAN)} {name}")
    print()


def interactive_mode():
    """Interactive mode"""
    print_header()
    select_ide()
    
    commands = {
        "1": cmd_create,
        "2": cmd_cleanup,
        "3": cmd_migrate,
        "4": cmd_health,
        "5": cmd_update,
        "6": cmd_review,
        "7": select_ide,
    }
    
    while True:
        print_menu()
        
        choice = input("Choose (0-7): ").strip()
        
        if choice == "0":
            print(f"\n{COLORS.colorize('👋 Goodbye!', COLORS.CYAN)}\n")
            break
        
        if choice in commands:
            commands[choice]()
            print()
            cont = input("Continue? (Y/n): ").strip().lower()
            if cont == 'n':
                print(f"\n{COLORS.colorize('👋 Goodbye!', COLORS.CYAN)}\n")
                break
            print()
        else:
            print(f"  {COLORS.error('Invalid choice')}")


def cli_mode():
    """CLI mode with arguments"""
    parser = argparse.ArgumentParser(
        prog="ai-toolkit",
        description="🛠️ AI Toolkit — create AI-friendly projects",
    )
    parser.add_argument("-v", "--version", action="version", version=f"AI Toolkit v{VERSION}")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # create
    create_p = subparsers.add_parser("create", help="Create project")
    create_p.add_argument("name", help="Project name")
    create_p.add_argument("--path", "-p", type=Path, default=Path.cwd(), help="Path")
    create_p.add_argument("--template", "-t", default="bot", 
                         choices=["bot", "webapp", "fastapi", "parser", "full", "monorepo"])
    create_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"],
                         choices=["cursor", "copilot", "claude", "windsurf"])
    create_p.add_argument("--no-docker", action="store_true", help="Without Docker")
    create_p.add_argument("--no-ci", action="store_true", help="Without CI/CD")
    create_p.add_argument("--no-git", action="store_true", help="Without Git")
    
    # cleanup
    cleanup_p = subparsers.add_parser("cleanup", help="Cleanup project")
    cleanup_p.add_argument("path", type=Path, help="Project path")
    cleanup_p.add_argument("--level", "-l", default="safe",
                          choices=["safe", "medium", "full"])
    
    # migrate
    migrate_p = subparsers.add_parser("migrate", help="Migrate project")
    migrate_p.add_argument("path", type=Path, help="Project path")
    migrate_p.add_argument("--ai", nargs="+", default=["cursor", "copilot", "claude"])
    
    # health
    health_p = subparsers.add_parser("health", help="Health check")
    health_p.add_argument("path", type=Path, help="Project path")
    
    # update
    update_p = subparsers.add_parser("update", help="Update project")
    update_p.add_argument("path", type=Path, help="Project path")
    
    # review
    review_p = subparsers.add_parser("review", help="Generate AI review prompt for changes")
    
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
        print(f"\n{COLORS.colorize('🔍 Analyzing...', COLORS.CYAN)}\n")
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
    
    elif args.command == "review":
        review_changes()


def main():
    """Entry point"""
    try:
        if len(sys.argv) > 1:
            cli_mode()
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print(f"\n\n{COLORS.colorize('👋 Goodbye!', COLORS.CYAN)}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
