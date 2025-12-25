"""
Tests for heavy mover utility.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import json

from src.utils.heavy_mover import (
    move_heavy_files,
    generate_config_paths,
    generate_manifest,
    restore_files,
    get_external_dir,
    get_manifest_path,
    format_move_report,
    MovedFile,
    MoveResult
)
from src.utils.token_scanner import scan_project, get_moveable_files, FileCategory


@pytest.fixture
def temp_project():
    """Create a temporary project with heavy files."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create data directory with large JSON
    data_dir = project / "data"
    data_dir.mkdir()
    
    large_json = {"items": [{"id": i, "name": f"Item {i}" * 100} for i in range(100)]}
    (data_dir / "products.json").write_text(json.dumps(large_json))
    
    # Create large CSV
    csv_content = "id,name,value\n" + "\n".join(f"{i},{'Name'*50}{i},{i*100}" for i in range(200))
    (data_dir / "users.csv").write_text(csv_content)
    
    # Create logs
    logs_dir = project / "logs"
    logs_dir.mkdir()
    (logs_dir / "app.log").write_text("INFO: Log entry\n" * 2000)
    
    # Create main.py (should not be moved)
    (project / "main.py").write_text("print('hello')")
    
    yield project
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def heavy_files(temp_project):
    """Get heavy files from temp project."""
    result = scan_project(temp_project, threshold=500)
    return get_moveable_files(result)


class TestGetExternalDir:
    def test_creates_directory(self, temp_project):
        ext_dir = get_external_dir(temp_project)
        assert ext_dir.exists()
        assert ext_dir.name == "LARGE_TOKENS"
    
    def test_structure(self, temp_project):
        ext_dir = get_external_dir(temp_project)
        assert ext_dir.parent.name == temp_project.name
        assert ext_dir.parent.parent.name == "_data"


class TestMoveHeavyFiles:
    def test_moves_files(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        assert result.success_count > 0
        assert result.failed_count == 0
        
        # Check files were actually moved
        for mf in result.moved_files:
            assert mf.external_path.exists()
            assert not mf.original_path.exists()
    
    def test_preserves_structure(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        # Check directory structure is preserved
        for mf in result.moved_files:
            assert mf.external_relative == mf.original_relative
    
    def test_dry_run(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files, dry_run=True)
        
        # Files should NOT be moved
        for hf in heavy_files:
            assert hf.path.exists()
        
        # But result should still be populated
        assert result.success_count > 0
    
    def test_generates_config_paths(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        assert result.config_paths_file is not None
        assert result.config_paths_file.exists()
        assert result.config_paths_file.name == "config_paths.py"
    
    def test_generates_manifest(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        assert result.manifest_file is not None
        assert result.manifest_file.exists()


class TestGenerateConfigPaths:
    def test_creates_file(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        config_path = temp_project / "config_paths.py"
        assert config_path.exists()
    
    def test_importable(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        # Test that generated file is valid Python
        config_content = result.config_paths_file.read_text()
        compile(config_content, "config_paths.py", "exec")
    
    def test_contains_mappings(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        config_content = result.config_paths_file.read_text()
        assert "FILES_MAP" in config_content
        assert "get_path" in config_content
    
    def test_get_path_function_works(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        # Import the generated config_paths
        import sys
        sys.path.insert(0, str(temp_project))
        
        try:
            from config_paths import get_path, FILES_MAP
            
            # Check that get_path works for moved files
            for mf in result.moved_files:
                path = get_path(mf.original_relative)
                assert path.exists()
        finally:
            sys.path.remove(str(temp_project))


class TestGenerateManifest:
    def test_creates_json(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        manifest = json.loads(result.manifest_file.read_text())
        assert "project" in manifest
        assert "files" in manifest
        assert manifest["project"] == temp_project.name
    
    def test_records_all_files(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        manifest = json.loads(result.manifest_file.read_text())
        assert len(manifest["files"]) == len(result.moved_files)
    
    def test_includes_metadata(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        
        manifest = json.loads(result.manifest_file.read_text())
        assert "created" in manifest
        assert "toolkit_version" in manifest
        assert "total_tokens" in manifest


class TestRestoreFiles:
    def test_restores_files(self, temp_project, heavy_files):
        # First move files
        result = move_heavy_files(temp_project, heavy_files)
        moved_count = result.success_count
        
        # Then restore
        restored = restore_files(temp_project)
        
        assert restored == moved_count
        
        # Check files are back
        for mf in result.moved_files:
            assert mf.original_path.exists()
    
    def test_removes_config_paths(self, temp_project, heavy_files):
        # Move files
        move_heavy_files(temp_project, heavy_files)
        
        # Restore
        restore_files(temp_project)
        
        # config_paths.py should be removed
        assert not (temp_project / "config_paths.py").exists()
    
    def test_restore_with_manifest_path(self, temp_project, heavy_files):
        # Move files
        result = move_heavy_files(temp_project, heavy_files)
        manifest_path = result.manifest_file
        
        # Restore using explicit manifest path
        restored = restore_files(temp_project, manifest_path=manifest_path)
        
        assert restored == result.success_count


class TestFormatMoveReport:
    def test_generates_report(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        report = format_move_report(result)
        
        assert "DEEP CLEAN" in report
        assert temp_project.name in report
        assert "MOVED" in report
    
    def test_shows_file_count(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        report = format_move_report(result)
        
        assert str(result.success_count) in report
    
    def test_shows_generated_files(self, temp_project, heavy_files):
        result = move_heavy_files(temp_project, heavy_files)
        report = format_move_report(result)
        
        assert "config_paths.py" in report
        assert "manifest.json" in report


class TestPathCompatibility:
    def test_uses_new_path_for_new_projects(self, temp_project, heavy_files):
        """New projects should use simplified path."""
        result = move_heavy_files(temp_project, heavy_files)
        
        # Should use new path format
        assert "_data" not in str(result.external_dir)
        assert f"{temp_project.name}_data" in str(result.external_dir)
    
    def test_respects_old_path_if_exists(self, temp_project, heavy_files):
        """Projects with old path should continue using it."""
        # Create old-style directory with content
        old_path = temp_project.parent / "_data" / temp_project.name / "LARGE_TOKENS"
        old_path.mkdir(parents=True)
        (old_path / "existing_file.json").write_text("{}")
        
        # Should detect and use old path
        ext_dir = get_external_dir(temp_project, create=False)
        assert "_data" in str(ext_dir)
        assert "LARGE_TOKENS" in str(ext_dir)
    
    def test_manifest_found_in_old_path(self, temp_project):
        """Should find manifest in old-style path."""
        # Create old-style manifest
        old_path = temp_project.parent / "_data" / temp_project.name / "LARGE_TOKENS"
        old_path.mkdir(parents=True)
        (old_path / "manifest.json").write_text('{"project": "test"}')
        
        manifest = get_manifest_path(temp_project)
        assert manifest is not None
        assert manifest.exists()
    
    def test_manifest_found_in_new_path(self, temp_project):
        """Should find manifest in new-style path."""
        # Create new-style manifest
        new_path = temp_project.parent / f"{temp_project.name}_data"
        new_path.mkdir(parents=True)
        (new_path / "manifest.json").write_text('{"project": "test"}')
        
        manifest = get_manifest_path(temp_project)
        assert manifest is not None
        assert manifest.exists()

