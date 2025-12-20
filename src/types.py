"""
Типы для AI Toolkit
"""

from __future__ import annotations

from typing import TypedDict, Literal, TypeAlias
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# Type Aliases
# ══════════════════════════════════════════════════════════════

TemplateName: TypeAlias = Literal["bot", "webapp", "fastapi", "parser", "full", "monorepo"]
IDEName: TypeAlias = Literal["cursor", "vscode_copilot", "vscode_claude", "windsurf", "all"]
AITarget: TypeAlias = Literal["cursor", "copilot", "claude", "windsurf"]
CleanupLevel: TypeAlias = Literal["safe", "medium", "full"]
IssueSeverity: TypeAlias = Literal["error", "warning", "info"]
IssueType: TypeAlias = Literal["venv", "cache", "logs", "data", "config"]


# ══════════════════════════════════════════════════════════════
# TypedDicts
# ══════════════════════════════════════════════════════════════

class TemplateConfig(TypedDict):
    """Конфигурация шаблона проекта"""
    name: str
    description: str
    modules: list[str]
    icon: str


class IDEConfig(TypedDict):
    """Конфигурация IDE"""
    name: str
    icon: str
    files: list[str]
    ai_targets: list[AITarget]


class CleanupLevelConfig(TypedDict):
    """Конфигурация уровня очистки"""
    name: str
    description: str
    actions: list[str]


class ProjectContext(TypedDict, total=False):
    """Контекст проекта для шаблонов"""
    project_name: str
    date: str
    python_version: str
    template: TemplateName
    ai_targets: list[AITarget]
    include_docker: bool
    include_ci: bool
    include_git: bool


class IssueDict(TypedDict):
    """Проблема в проекте"""
    type: IssueType
    severity: IssueSeverity
    path: Path | None
    size_mb: float
    message: str
    fix_action: str


class HealthCheckResult(TypedDict):
    """Результат health check"""
    passed: bool
    errors: int
    warnings: int
    checks: list[dict[str, str | bool]]


# ══════════════════════════════════════════════════════════════
# Callable Types
# ══════════════════════════════════════════════════════════════

from typing import Callable, Protocol


class GeneratorFunc(Protocol):
    """Протокол для функций-генераторов"""
    def __call__(self, project_dir: Path, project_name: str, *args: object) -> None:
        ...


class CommandFunc(Protocol):
    """Протокол для интерактивных команд"""
    def __call__(self) -> None:
        ...


Типы для AI Toolkit
"""

from __future__ import annotations

from typing import TypedDict, Literal, TypeAlias
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# Type Aliases
# ══════════════════════════════════════════════════════════════

TemplateName: TypeAlias = Literal["bot", "webapp", "fastapi", "parser", "full", "monorepo"]
IDEName: TypeAlias = Literal["cursor", "vscode_copilot", "vscode_claude", "windsurf", "all"]
AITarget: TypeAlias = Literal["cursor", "copilot", "claude", "windsurf"]
CleanupLevel: TypeAlias = Literal["safe", "medium", "full"]
IssueSeverity: TypeAlias = Literal["error", "warning", "info"]
IssueType: TypeAlias = Literal["venv", "cache", "logs", "data", "config"]


# ══════════════════════════════════════════════════════════════
# TypedDicts
# ══════════════════════════════════════════════════════════════

class TemplateConfig(TypedDict):
    """Конфигурация шаблона проекта"""
    name: str
    description: str
    modules: list[str]
    icon: str


class IDEConfig(TypedDict):
    """Конфигурация IDE"""
    name: str
    icon: str
    files: list[str]
    ai_targets: list[AITarget]


class CleanupLevelConfig(TypedDict):
    """Конфигурация уровня очистки"""
    name: str
    description: str
    actions: list[str]


class ProjectContext(TypedDict, total=False):
    """Контекст проекта для шаблонов"""
    project_name: str
    date: str
    python_version: str
    template: TemplateName
    ai_targets: list[AITarget]
    include_docker: bool
    include_ci: bool
    include_git: bool


class IssueDict(TypedDict):
    """Проблема в проекте"""
    type: IssueType
    severity: IssueSeverity
    path: Path | None
    size_mb: float
    message: str
    fix_action: str


class HealthCheckResult(TypedDict):
    """Результат health check"""
    passed: bool
    errors: int
    warnings: int
    checks: list[dict[str, str | bool]]


# ══════════════════════════════════════════════════════════════
# Callable Types
# ══════════════════════════════════════════════════════════════

from typing import Callable, Protocol


class GeneratorFunc(Protocol):
    """Протокол для функций-генераторов"""
    def __call__(self, project_dir: Path, project_name: str, *args: object) -> None:
        ...


class CommandFunc(Protocol):
    """Протокол для интерактивных команд"""
    def __call__(self) -> None:
        ...


Типы для AI Toolkit
"""

from __future__ import annotations

from typing import TypedDict, Literal, TypeAlias
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# Type Aliases
# ══════════════════════════════════════════════════════════════

TemplateName: TypeAlias = Literal["bot", "webapp", "fastapi", "parser", "full", "monorepo"]
IDEName: TypeAlias = Literal["cursor", "vscode_copilot", "vscode_claude", "windsurf", "all"]
AITarget: TypeAlias = Literal["cursor", "copilot", "claude", "windsurf"]
CleanupLevel: TypeAlias = Literal["safe", "medium", "full"]
IssueSeverity: TypeAlias = Literal["error", "warning", "info"]
IssueType: TypeAlias = Literal["venv", "cache", "logs", "data", "config"]


# ══════════════════════════════════════════════════════════════
# TypedDicts
# ══════════════════════════════════════════════════════════════

class TemplateConfig(TypedDict):
    """Конфигурация шаблона проекта"""
    name: str
    description: str
    modules: list[str]
    icon: str


class IDEConfig(TypedDict):
    """Конфигурация IDE"""
    name: str
    icon: str
    files: list[str]
    ai_targets: list[AITarget]


class CleanupLevelConfig(TypedDict):
    """Конфигурация уровня очистки"""
    name: str
    description: str
    actions: list[str]


class ProjectContext(TypedDict, total=False):
    """Контекст проекта для шаблонов"""
    project_name: str
    date: str
    python_version: str
    template: TemplateName
    ai_targets: list[AITarget]
    include_docker: bool
    include_ci: bool
    include_git: bool


class IssueDict(TypedDict):
    """Проблема в проекте"""
    type: IssueType
    severity: IssueSeverity
    path: Path | None
    size_mb: float
    message: str
    fix_action: str


class HealthCheckResult(TypedDict):
    """Результат health check"""
    passed: bool
    errors: int
    warnings: int
    checks: list[dict[str, str | bool]]


# ══════════════════════════════════════════════════════════════
# Callable Types
# ══════════════════════════════════════════════════════════════

from typing import Callable, Protocol


class GeneratorFunc(Protocol):
    """Протокол для функций-генераторов"""
    def __call__(self, project_dir: Path, project_name: str, *args: object) -> None:
        ...


class CommandFunc(Protocol):
    """Протокол для интерактивных команд"""
    def __call__(self) -> None:
        ...


Типы для AI Toolkit
"""

from __future__ import annotations

from typing import TypedDict, Literal, TypeAlias
from pathlib import Path


# ══════════════════════════════════════════════════════════════
# Type Aliases
# ══════════════════════════════════════════════════════════════

TemplateName: TypeAlias = Literal["bot", "webapp", "fastapi", "parser", "full", "monorepo"]
IDEName: TypeAlias = Literal["cursor", "vscode_copilot", "vscode_claude", "windsurf", "all"]
AITarget: TypeAlias = Literal["cursor", "copilot", "claude", "windsurf"]
CleanupLevel: TypeAlias = Literal["safe", "medium", "full"]
IssueSeverity: TypeAlias = Literal["error", "warning", "info"]
IssueType: TypeAlias = Literal["venv", "cache", "logs", "data", "config"]


# ══════════════════════════════════════════════════════════════
# TypedDicts
# ══════════════════════════════════════════════════════════════

class TemplateConfig(TypedDict):
    """Конфигурация шаблона проекта"""
    name: str
    description: str
    modules: list[str]
    icon: str


class IDEConfig(TypedDict):
    """Конфигурация IDE"""
    name: str
    icon: str
    files: list[str]
    ai_targets: list[AITarget]


class CleanupLevelConfig(TypedDict):
    """Конфигурация уровня очистки"""
    name: str
    description: str
    actions: list[str]


class ProjectContext(TypedDict, total=False):
    """Контекст проекта для шаблонов"""
    project_name: str
    date: str
    python_version: str
    template: TemplateName
    ai_targets: list[AITarget]
    include_docker: bool
    include_ci: bool
    include_git: bool


class IssueDict(TypedDict):
    """Проблема в проекте"""
    type: IssueType
    severity: IssueSeverity
    path: Path | None
    size_mb: float
    message: str
    fix_action: str


class HealthCheckResult(TypedDict):
    """Результат health check"""
    passed: bool
    errors: int
    warnings: int
    checks: list[dict[str, str | bool]]


# ══════════════════════════════════════════════════════════════
# Callable Types
# ══════════════════════════════════════════════════════════════

from typing import Callable, Protocol


class GeneratorFunc(Protocol):
    """Протокол для функций-генераторов"""
    def __call__(self, project_dir: Path, project_name: str, *args: object) -> None:
        ...


class CommandFunc(Protocol):
    """Протокол для интерактивных команд"""
    def __call__(self) -> None:
        ...

