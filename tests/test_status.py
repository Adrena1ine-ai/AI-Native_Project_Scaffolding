"""Tests for status generator."""

import pytest
from pathlib import Path

from src.utils.status_generator import (
    scan_commands,
    scan_utilities,
    scan_generators,
    generate_status_md,
    update_status,
    get_version,
    check_file_exists,
)


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project with src structure."""
    project_path = tmp_path / "test_project"
    project_path.mkdir()
    
    # Create src structure
    src = project_path / "src"
    src.mkdir()
    (src / "__init__.py").write_text("")
    
    # Create commands
    commands = src / "commands"
    commands.mkdir()
    (commands / "__init__.py").write_text("")
    (commands / "test_cmd.py").write_text('''
def cmd_test(args):
    """Test command description."""
    pass

def cmd_another(args):
    """Another test command."""
    pass
''')
    
    # Create utils
    utils = src / "utils"
    utils.mkdir()
    (utils / "__init__.py").write_text("")
    (utils / "helper.py").write_text('"""Helper utilities for testing."""')
    (utils / "parser.py").write_text('"""Parser utilities."""')
    
    # Create generators
    generators = src / "generators"
    generators.mkdir()
    (generators / "__init__.py").write_text("")
    (generators / "template_gen.py").write_text('"""Template generator module."""')
    
    # Create core with version
    core = src / "core"
    core.mkdir()
    (core / "__init__.py").write_text("")
    (core / "constants.py").write_text('VERSION = "1.2.3"')
    
    return project_path


class TestScanCommands:
    """Tests for command scanning."""
    
    def test_scan_commands_finds_cmd_functions(self, temp_project):
        """Should find cmd_* functions."""
        commands = scan_commands(temp_project / "src")
        
        assert len(commands) >= 2
        names = [c["name"] for c in commands]
        assert "test" in names
        assert "another" in names
    
    def test_scan_commands_extracts_docstrings(self, temp_project):
        """Should extract docstrings as descriptions."""
        commands = scan_commands(temp_project / "src")
        
        test_cmd = next(c for c in commands if c["name"] == "test")
        assert "Test command description" in test_cmd["description"]
    
    def test_scan_commands_empty_dir(self, tmp_path):
        """Should return empty list for missing commands dir."""
        commands = scan_commands(tmp_path / "nonexistent")
        assert commands == []
    
    def test_scan_commands_ignores_private_files(self, temp_project):
        """Should ignore files starting with underscore."""
        # Create a private command file
        (temp_project / "src" / "commands" / "_private.py").write_text('''
def cmd_hidden(args):
    """This should be hidden."""
    pass
''')
        
        commands = scan_commands(temp_project / "src")
        names = [c["name"] for c in commands]
        assert "hidden" not in names


class TestScanUtilities:
    """Tests for utility scanning."""
    
    def test_scan_utilities_finds_modules(self, temp_project):
        """Should find utility modules."""
        utils = scan_utilities(temp_project / "src")
        
        assert len(utils) >= 2
        names = [u["name"] for u in utils]
        assert "helper" in names
        assert "parser" in names
    
    def test_scan_utilities_extracts_docstrings(self, temp_project):
        """Should extract module docstrings."""
        utils = scan_utilities(temp_project / "src")
        
        helper = next(u for u in utils if u["name"] == "helper")
        assert "Helper utilities" in helper["description"]


class TestScanGenerators:
    """Tests for generator scanning."""
    
    def test_scan_generators_finds_modules(self, temp_project):
        """Should find generator modules."""
        generators = scan_generators(temp_project / "src")
        
        assert len(generators) >= 1
        names = [g["name"] for g in generators]
        assert "template_gen" in names


class TestGetVersion:
    """Tests for version extraction."""
    
    def test_get_version_from_constants(self, temp_project):
        """Should extract version from constants.py."""
        version = get_version(temp_project)
        assert version == "1.2.3"
    
    def test_get_version_fallback(self, tmp_path):
        """Should return fallback version if not found."""
        version = get_version(tmp_path)
        assert version == "3.3"


class TestCheckFileExists:
    """Tests for file existence checking."""
    
    def test_check_existing_file(self, temp_project):
        """Should return True for existing file."""
        (temp_project / "README.md").write_text("# Test")
        assert check_file_exists(temp_project, "README.md") is True
    
    def test_check_missing_file(self, temp_project):
        """Should return False for missing file."""
        assert check_file_exists(temp_project, "MISSING.md") is False
    
    def test_check_nested_file(self, temp_project):
        """Should work with nested paths."""
        assert check_file_exists(temp_project, "src/core/constants.py") is True


class TestGenerateStatusMd:
    """Tests for status markdown generation."""
    
    def test_generate_status_md_contains_header(self, temp_project):
        """Should contain proper header."""
        content = generate_status_md(temp_project, skip_tests=True)
        
        assert "# 📊 Project Status" in content
        assert "Auto-generated" in content
    
    def test_generate_status_md_lists_commands(self, temp_project):
        """Should list found commands."""
        content = generate_status_md(temp_project, skip_tests=True)
        
        assert "test" in content.lower()
        assert "another" in content.lower()
    
    def test_generate_status_md_lists_utilities(self, temp_project):
        """Should list found utilities."""
        content = generate_status_md(temp_project, skip_tests=True)
        
        assert "helper" in content.lower()
    
    def test_generate_status_md_shows_version(self, temp_project):
        """Should show project version."""
        content = generate_status_md(temp_project, skip_tests=True)
        
        assert "1.2.3" in content
    
    def test_generate_status_md_skip_tests(self, temp_project):
        """Should indicate tests were skipped."""
        content = generate_status_md(temp_project, skip_tests=True)
        
        assert "Skipped" in content


class TestUpdateStatus:
    """Tests for status file writing."""
    
    def test_update_status_creates_file(self, temp_project):
        """Should create PROJECT_STATUS.md file."""
        status_file = update_status(temp_project, skip_tests=True)
        
        assert status_file.exists()
        assert status_file.name == "PROJECT_STATUS.md"
    
    def test_update_status_writes_content(self, temp_project):
        """Should write valid markdown content."""
        status_file = update_status(temp_project, skip_tests=True)
        content = status_file.read_text()
        
        assert "# 📊 Project Status" in content
        assert len(content) > 100
    
    def test_update_status_overwrites_existing(self, temp_project):
        """Should overwrite existing file."""
        status_file = temp_project / "PROJECT_STATUS.md"
        status_file.write_text("old content")
        
        update_status(temp_project, skip_tests=True)
        
        new_content = status_file.read_text()
        assert "old content" not in new_content
        assert "Auto-generated" in new_content
