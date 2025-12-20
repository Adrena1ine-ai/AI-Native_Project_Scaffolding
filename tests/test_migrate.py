"""
Тесты команды migrate
"""

import pytest
from pathlib import Path

from src.commands.migrate import migrate_project
from src.core.constants import VERSION


class TestMigrateProject:
    """Тесты миграции проекта"""

    def test_migrate_adds_ai_configs(self, temp_project):
        """Миграция добавляет AI конфиги"""
        result = migrate_project(temp_project, ["cursor", "copilot"], quiet=True)
        
        assert result is True
        assert (temp_project / "_AI_INCLUDE").is_dir()
        assert (temp_project / ".cursorrules").exists()
        assert (temp_project / ".github" / "copilot-instructions.md").exists()

    def test_migrate_adds_scripts(self, temp_project):
        """Миграция добавляет скрипты"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        scripts_dir = temp_project / "scripts"
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "context.py").exists()

    def test_migrate_adds_version(self, temp_project):
        """Миграция добавляет версию"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        version_file = temp_project / ".toolkit-version"
        assert version_file.exists()
        assert version_file.read_text().strip() == VERSION

    def test_migrate_skips_existing(self, temp_project):
        """Миграция не перезаписывает существующие файлы"""
        # Создаём _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        marker = "CUSTOM_CONTENT"
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text(marker)
        
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        # Содержимое должно сохраниться
        content = (ai_dir / "PROJECT_CONVENTIONS.md").read_text()
        assert marker in content

    def test_migrate_adds_ci_if_requested(self, temp_project):
        """Миграция добавляет CI если запрошено"""
        migrate_project(temp_project, ["cursor"], include_ci=True, quiet=True)
        
        workflows = temp_project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "ci.yml").exists()


Тесты команды migrate
"""

import pytest
from pathlib import Path

from src.commands.migrate import migrate_project
from src.core.constants import VERSION


class TestMigrateProject:
    """Тесты миграции проекта"""

    def test_migrate_adds_ai_configs(self, temp_project):
        """Миграция добавляет AI конфиги"""
        result = migrate_project(temp_project, ["cursor", "copilot"], quiet=True)
        
        assert result is True
        assert (temp_project / "_AI_INCLUDE").is_dir()
        assert (temp_project / ".cursorrules").exists()
        assert (temp_project / ".github" / "copilot-instructions.md").exists()

    def test_migrate_adds_scripts(self, temp_project):
        """Миграция добавляет скрипты"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        scripts_dir = temp_project / "scripts"
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "context.py").exists()

    def test_migrate_adds_version(self, temp_project):
        """Миграция добавляет версию"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        version_file = temp_project / ".toolkit-version"
        assert version_file.exists()
        assert version_file.read_text().strip() == VERSION

    def test_migrate_skips_existing(self, temp_project):
        """Миграция не перезаписывает существующие файлы"""
        # Создаём _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        marker = "CUSTOM_CONTENT"
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text(marker)
        
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        # Содержимое должно сохраниться
        content = (ai_dir / "PROJECT_CONVENTIONS.md").read_text()
        assert marker in content

    def test_migrate_adds_ci_if_requested(self, temp_project):
        """Миграция добавляет CI если запрошено"""
        migrate_project(temp_project, ["cursor"], include_ci=True, quiet=True)
        
        workflows = temp_project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "ci.yml").exists()


Тесты команды migrate
"""

import pytest
from pathlib import Path

from src.commands.migrate import migrate_project
from src.core.constants import VERSION


class TestMigrateProject:
    """Тесты миграции проекта"""

    def test_migrate_adds_ai_configs(self, temp_project):
        """Миграция добавляет AI конфиги"""
        result = migrate_project(temp_project, ["cursor", "copilot"], quiet=True)
        
        assert result is True
        assert (temp_project / "_AI_INCLUDE").is_dir()
        assert (temp_project / ".cursorrules").exists()
        assert (temp_project / ".github" / "copilot-instructions.md").exists()

    def test_migrate_adds_scripts(self, temp_project):
        """Миграция добавляет скрипты"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        scripts_dir = temp_project / "scripts"
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "context.py").exists()

    def test_migrate_adds_version(self, temp_project):
        """Миграция добавляет версию"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        version_file = temp_project / ".toolkit-version"
        assert version_file.exists()
        assert version_file.read_text().strip() == VERSION

    def test_migrate_skips_existing(self, temp_project):
        """Миграция не перезаписывает существующие файлы"""
        # Создаём _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        marker = "CUSTOM_CONTENT"
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text(marker)
        
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        # Содержимое должно сохраниться
        content = (ai_dir / "PROJECT_CONVENTIONS.md").read_text()
        assert marker in content

    def test_migrate_adds_ci_if_requested(self, temp_project):
        """Миграция добавляет CI если запрошено"""
        migrate_project(temp_project, ["cursor"], include_ci=True, quiet=True)
        
        workflows = temp_project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "ci.yml").exists()


Тесты команды migrate
"""

import pytest
from pathlib import Path

from src.commands.migrate import migrate_project
from src.core.constants import VERSION


class TestMigrateProject:
    """Тесты миграции проекта"""

    def test_migrate_adds_ai_configs(self, temp_project):
        """Миграция добавляет AI конфиги"""
        result = migrate_project(temp_project, ["cursor", "copilot"], quiet=True)
        
        assert result is True
        assert (temp_project / "_AI_INCLUDE").is_dir()
        assert (temp_project / ".cursorrules").exists()
        assert (temp_project / ".github" / "copilot-instructions.md").exists()

    def test_migrate_adds_scripts(self, temp_project):
        """Миграция добавляет скрипты"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        scripts_dir = temp_project / "scripts"
        assert (scripts_dir / "bootstrap.sh").exists()
        assert (scripts_dir / "context.py").exists()

    def test_migrate_adds_version(self, temp_project):
        """Миграция добавляет версию"""
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        version_file = temp_project / ".toolkit-version"
        assert version_file.exists()
        assert version_file.read_text().strip() == VERSION

    def test_migrate_skips_existing(self, temp_project):
        """Миграция не перезаписывает существующие файлы"""
        # Создаём _AI_INCLUDE
        ai_dir = temp_project / "_AI_INCLUDE"
        ai_dir.mkdir()
        marker = "CUSTOM_CONTENT"
        (ai_dir / "PROJECT_CONVENTIONS.md").write_text(marker)
        
        migrate_project(temp_project, ["cursor"], quiet=True)
        
        # Содержимое должно сохраниться
        content = (ai_dir / "PROJECT_CONVENTIONS.md").read_text()
        assert marker in content

    def test_migrate_adds_ci_if_requested(self, temp_project):
        """Миграция добавляет CI если запрошено"""
        migrate_project(temp_project, ["cursor"], include_ci=True, quiet=True)
        
        workflows = temp_project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "ci.yml").exists()

