"""
Tests for core modules
"""

import pytest
from pathlib import Path

from src.core.constants import COLORS, VERSION, TEMPLATES, IDE_CONFIGS, CLEANUP_LEVELS
from src.core.config import get_config, set_default_ide, get_default_ide, get_default_ai_targets
from src.core.file_utils import create_file, make_executable, get_dir_size


class TestColors:
    """Tests for COLORS class"""

    def test_colorize(self):
        """Colorize text"""
        result = COLORS.colorize("test", COLORS.RED)
        assert "test" in result
        assert COLORS.RED in result
        assert COLORS.END in result

    def test_success(self):
        """Success method"""
        result = COLORS.success("test")
        assert "✅" in result
        assert COLORS.GREEN in result

    def test_error(self):
        """Error method"""
        result = COLORS.error("test")
        assert "❌" in result
        assert COLORS.RED in result

    def test_warning(self):
        """Warning method"""
        result = COLORS.warning("test")
        assert "⚠️" in result
        assert COLORS.YELLOW in result

    def test_info(self):
        """Info method"""
        result = COLORS.info("test")
        assert "ℹ️" in result
        assert COLORS.CYAN in result


class TestConstants:
    """Tests for constants"""

    def test_version_format(self):
        """Version in correct format"""
        parts = VERSION.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_templates_exist(self):
        """Templates are defined"""
        assert "bot" in TEMPLATES
        assert "webapp" in TEMPLATES
        assert "fastapi" in TEMPLATES
        assert "parser" in TEMPLATES
        assert "full" in TEMPLATES

    def test_template_has_required_fields(self):
        """Templates have required fields"""
        for name, tmpl in TEMPLATES.items():
            assert "name" in tmpl
            assert "modules" in tmpl
            assert isinstance(tmpl["modules"], list)

    def test_ide_configs_exist(self):
        """IDE configs are defined"""
        assert "cursor" in IDE_CONFIGS
        assert "vscode_copilot" in IDE_CONFIGS
        assert "vscode_claude" in IDE_CONFIGS
        assert "windsurf" in IDE_CONFIGS
        assert "all" in IDE_CONFIGS

    def test_ide_config_has_required_fields(self):
        """IDE configs have required fields"""
        for name, cfg in IDE_CONFIGS.items():
            assert "name" in cfg
            assert "ai_targets" in cfg

    def test_cleanup_levels_exist(self):
        """Cleanup levels are defined"""
        assert "safe" in CLEANUP_LEVELS
        assert "medium" in CLEANUP_LEVELS
        assert "full" in CLEANUP_LEVELS


class TestConfig:
    """Tests for configuration"""

    def test_set_and_get_default_ide(self):
        """Set and get IDE"""
        set_default_ide("cursor", ["cursor"])
        assert get_default_ide() == "cursor"

    def test_get_default_ai_targets(self):
        """Get AI targets"""
        set_default_ide("all", ["cursor", "copilot"])
        targets = get_default_ai_targets()
        assert "cursor" in targets
        assert "copilot" in targets


class TestFileUtils:
    """Tests for file utilities"""

    def test_create_file(self, temp_dir):
        """Create file"""
        path = temp_dir / "test.txt"
        create_file(path, "content")
        
        assert path.exists()
        assert path.read_text() == "content\n"

    def test_create_file_creates_dirs(self, temp_dir):
        """Create file creates directories"""
        path = temp_dir / "a" / "b" / "c" / "test.txt"
        create_file(path, "content")
        
        assert path.exists()

    def test_create_executable(self, temp_dir):
        """Create executable file"""
        path = temp_dir / "test.sh"
        create_file(path, "#!/bin/bash", executable=True)
        
        import os
        import stat
        mode = os.stat(path).st_mode
        assert mode & stat.S_IXUSR

    def test_get_dir_size(self, temp_dir):
        """Get directory size"""
        # Create files
        (temp_dir / "file1.txt").write_bytes(b"x" * 1000)
        (temp_dir / "file2.txt").write_bytes(b"x" * 2000)
        
        size = get_dir_size(temp_dir)
        assert size > 0  # Size in MB

    def test_get_dir_size_empty(self, temp_dir):
        """Size of empty directory"""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        
        size = get_dir_size(empty_dir)
        assert size == 0.0
