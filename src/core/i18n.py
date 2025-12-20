"""
🌍 Internationalization (i18n) module

Provides translation functions for CLI and other components.
"""

from __future__ import annotations

from typing import Any

from .config import get_language, set_language


# Cache for loaded messages
_messages_cache: dict[str, dict[str, str]] = {}


def _load_messages(lang: str) -> dict[str, str]:
    """Load messages for specified language."""
    if lang in _messages_cache:
        return _messages_cache[lang]
    
    if lang == "ru":
        from ..locales.ru import MESSAGES
    else:
        from ..locales.en import MESSAGES
    
    _messages_cache[lang] = MESSAGES
    return MESSAGES


def t(key: str, **kwargs: Any) -> str:
    """
    Get translated text by key.
    
    Args:
        key: Message key from locales
        **kwargs: Format arguments for the message
        
    Returns:
        Translated and formatted string
        
    Example:
        >>> t("welcome")
        "🛠️  AI-NATIVE PROJECT SCAFFOLDING"
        
        >>> t("issues_found", n=3)
        "Found 3 issue(s):"
    """
    lang = get_language()
    messages = _load_messages(lang)
    
    text = messages.get(key, key)
    
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    
    return text


def select_language_prompt() -> str:
    """
    Show language selection prompt.
    Returns selected language code ('en' or 'ru').
    """
    from .constants import COLORS
    
    print(f"\n{COLORS.colorize('═' * 60, COLORS.BLUE)}")
    print(f"{COLORS.colorize('🌍 Select language / Выберите язык:', COLORS.MAGENTA)}\n")
    
    options = [
        ("en", "🇬🇧 English"),
        ("ru", "🇷🇺 Русский"),
    ]
    
    for i, (code, name) in enumerate(options, 1):
        print(f"  {COLORS.colorize(str(i) + '.', COLORS.CYAN)} {name}")
    print()
    
    while True:
        choice = input(f"Choice / Выбор (1-2) [{COLORS.colorize('1', COLORS.GREEN)}]: ").strip()
        if not choice:
            choice = "1"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                code, name = options[idx]
                set_language(code)
                
                if code == "en":
                    print(f"\n  {COLORS.success('Language saved: English')}\n")
                else:
                    print(f"\n  {COLORS.success('Язык сохранён: Русский')}\n")
                
                return code
        except (ValueError, IndexError):
            pass
        
        print(f"  {COLORS.error('Invalid choice / Неверный выбор')}")


def get_available_languages() -> list[tuple[str, str]]:
    """Get list of available languages."""
    return [
        ("en", "English"),
        ("ru", "Русский"),
    ]

