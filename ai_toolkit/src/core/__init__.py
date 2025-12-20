"""
Core модуль — базовые компоненты
"""

from .config import Config, get_config, set_default_ide, get_default_ide, get_default_ai_targets
from .constants import COLORS, VERSION
from .file_utils import create_file, copy_template, make_executable

__all__ = [
    "Config",
    "get_config", 
    "set_default_ide",
    "get_default_ide",
    "get_default_ai_targets",
    "COLORS",
    "VERSION",
    "create_file",
    "copy_template",
    "make_executable",
]
