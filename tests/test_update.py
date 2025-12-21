"""
Tests for update command
"""

import pytest
from pathlib import Path

from src.commands.update import update_project
from src.core.constants import VERSION


class TestUpdateProject:
    """Tests for project update"""

    def test_update_changes_version(self, clean_project):
        """Update changes version"""
        version_file = clean_project / ".toolkit-version"
        version_file.write_text("1.0.0")  # Old version
        
        result = update_project(clean_project)
        
        assert result is True
        assert version_file.read_text().strip() == VERSION

    def test_update_same_version_skips(self, clean_project):
        """Update with same version is skipped"""
        version_file = clean_project / ".toolkit-version"
        version_file.write_text(VERSION)
        
        result = update_project(clean_project)
        
        assert result is True

    def test_update_refreshes_scripts(self, clean_project):
        """Update refreshes scripts"""
        version_file = clean_project / ".toolkit-version"
        version_file.write_text("1.0.0")
        
        # Modify script
        bootstrap = clean_project / "scripts" / "bootstrap.sh"
        bootstrap.write_text("OLD CONTENT")
        
        update_project(clean_project)
        
        # Script should be updated
        content = bootstrap.read_text()
        assert "OLD CONTENT" not in content
        assert "_venvs" in content
