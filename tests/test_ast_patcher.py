"""
Tests for AST patcher utility.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import ast

from src.utils.ast_patcher import (
    patch_file,
    patch_project,
    add_import_statement,
    revert_patches,
    format_patch_report,
    PathPatcher,
    PatchResult,
    PatchReport
)


@pytest.fixture
def temp_project():
    """Create a temporary project with Python files."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create Python file with file paths
    (project / "main.py").write_text('''
import json
from pathlib import Path

def load_data():
    with open("data/products.json") as f:
        return json.load(f)

def get_config():
    config_path = Path("data/config.yaml")
    return config_path.read_text()

def process():
    data = open("data/users.csv", "r").read()
    return data
''')
    
    # Create another file with pandas
    (project / "analysis.py").write_text('''
import pandas as pd

def analyze():
    df = pd.read_csv("data/users.csv")
    df.to_csv("output/results.csv")
    return df
''')
    
    # Create file with sqlite
    (project / "database.py").write_text('''
import sqlite3

def get_connection():
    return sqlite3.connect("data/app.db")
''')
    
    yield project
    shutil.rmtree(temp_dir)


@pytest.fixture
def moved_files():
    """Set of files that were 'moved'."""
    return {
        "data/products.json",
        "data/config.yaml",
        "data/users.csv",
        "data/app.db",
    }


class TestAddImport:
    def test_adds_import(self):
        source = "import json\n\ndef foo():\n    pass"
        result = add_import_statement(source)
        assert "from config_paths import get_path" in result
    
    def test_no_duplicate(self):
        source = "from config_paths import get_path\n\ndef foo():\n    pass"
        result = add_import_statement(source)
        assert result.count("from config_paths import get_path") == 1
    
    def test_after_imports(self):
        source = "import json\nimport os\n\ndef foo():\n    pass"
        result = add_import_statement(source)
        lines = result.split('\n')
        import_idx = next(i for i, l in enumerate(lines) if "config_paths" in l)
        assert import_idx >= 2  # After json and os imports
    
    def test_handles_docstring(self):
        source = '"""Module docstring."""\nimport json\n\ndef foo():\n    pass'
        result = add_import_statement(source)
        assert "from config_paths import get_path" in result
        # Import should be after docstring
        lines = result.split('\n')
        assert lines[0].startswith('"""')


class TestPatchFile:
    def test_patches_open(self, temp_project, moved_files):
        result = patch_file(temp_project / "main.py", moved_files, dry_run=True)
        
        assert result.success
        assert len(result.patches) > 0
        assert any("open" in p.pattern_type for p in result.patches)
    
    def test_patches_path(self, temp_project, moved_files):
        result = patch_file(temp_project / "main.py", moved_files, dry_run=True)
        
        assert any("path" in p.pattern_type for p in result.patches)
    
    def test_patches_pandas(self, temp_project, moved_files):
        result = patch_file(temp_project / "analysis.py", moved_files, dry_run=True)
        
        assert any("pandas" in p.pattern_type for p in result.patches)
    
    def test_patches_sqlite(self, temp_project, moved_files):
        result = patch_file(temp_project / "database.py", moved_files, dry_run=True)
        
        assert any("sqlite" in p.pattern_type for p in result.patches)
    
    def test_creates_backup(self, temp_project, moved_files):
        patch_file(temp_project / "main.py", moved_files, dry_run=False)
        
        assert (temp_project / "main.py.bak").exists()
    
    def test_adds_import(self, temp_project, moved_files):
        result = patch_file(temp_project / "main.py", moved_files, dry_run=True)
        
        assert "from config_paths import get_path" in result.patched_content
    
    def test_dry_run_no_changes(self, temp_project, moved_files):
        original = (temp_project / "main.py").read_text()
        patch_file(temp_project / "main.py", moved_files, dry_run=True)
        
        assert (temp_project / "main.py").read_text() == original
    
    def test_valid_syntax_after_patch(self, temp_project, moved_files):
        result = patch_file(temp_project / "main.py", moved_files, dry_run=True)
        
        # Should not raise SyntaxError
        ast.parse(result.patched_content)
    
    def test_skips_unmoved_files(self, temp_project):
        # Only move one file
        moved = {"data/products.json"}
        result = patch_file(temp_project / "main.py", moved, dry_run=True)
        
        # Should only patch products.json, not users.csv
        patched_paths = [p.original for p in result.patches]
        assert any("products.json" in p for p in patched_paths)


class TestPatchProject:
    def test_scans_all_files(self, temp_project, moved_files):
        report = patch_project(temp_project, moved_files, dry_run=True)
        
        assert report.files_scanned >= 3
    
    def test_patches_multiple_files(self, temp_project, moved_files):
        report = patch_project(temp_project, moved_files, dry_run=True)
        
        assert report.files_patched >= 2
    
    def test_excludes_patterns(self, temp_project, moved_files):
        # Create a test file
        (temp_project / "test_main.py").write_text('open("data/products.json")')
        
        report = patch_project(
            temp_project, 
            moved_files, 
            dry_run=True,
            exclude_patterns=["test_*.py"]
        )
        
        # test_main.py should not be patched
        patched_files = [r.file.name for r in report.results if r.patches]
        assert "test_main.py" not in patched_files
    
    def test_excludes_config_paths(self, temp_project, moved_files):
        # Create config_paths.py
        (temp_project / "config_paths.py").write_text('def get_path(x): pass')
        
        report = patch_project(temp_project, moved_files, dry_run=True)
        
        # config_paths.py should not be patched
        patched_files = [r.file.name for r in report.results if r.patches]
        assert "config_paths.py" not in patched_files


class TestRevertPatches:
    def test_reverts_files(self, temp_project, moved_files):
        # Patch files
        patch_project(temp_project, moved_files, dry_run=False)
        
        # Verify patched
        assert "get_path" in (temp_project / "main.py").read_text()
        
        # Revert
        reverted = revert_patches(temp_project)
        
        assert reverted >= 1
        assert "get_path" not in (temp_project / "main.py").read_text()


class TestFormatReport:
    def test_generates_report(self, temp_project, moved_files):
        report = patch_project(temp_project, moved_files, dry_run=True)
        formatted = format_patch_report(report)
        
        assert "AST PATCHER" in formatted
        assert str(report.files_patched) in formatted
    
    def test_shows_patches(self, temp_project, moved_files):
        report = patch_project(temp_project, moved_files, dry_run=True)
        formatted = format_patch_report(report)
        
        if report.total_patches > 0:
            assert "PATCHES APPLIED" in formatted


class TestPathPatcher:
    def test_identifies_moved_files(self):
        patcher = PathPatcher({"data/file.json"})
        assert patcher._is_moved_file("data/file.json")
        assert patcher._is_moved_file("./data/file.json")
        assert not patcher._is_moved_file("other/file.json")
    
    def test_creates_get_path_call(self):
        patcher = PathPatcher(set())
        call = patcher._create_get_path_call("data/file.json")
        
        assert isinstance(call, ast.Call)
        assert isinstance(call.func, ast.Name)
        assert call.func.id == "get_path"

