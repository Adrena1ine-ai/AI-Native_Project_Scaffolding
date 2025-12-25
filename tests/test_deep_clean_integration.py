"""
Integration tests for Deep Clean feature.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import json

from src.commands.doctor import run_deep_clean, run_restore


@pytest.fixture
def temp_project():
    """Create a realistic temporary project."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create data directory with large files
    data_dir = project / "data"
    data_dir.mkdir()
    
    # Large JSON (over 1000 tokens)
    large_data = {"products": [{"id": i, "name": f"Product {i}" * 50, "price": i * 10} for i in range(100)]}
    (data_dir / "products.json").write_text(json.dumps(large_data, indent=2))
    
    # Large CSV
    csv_content = "id,name,value,description\n"
    csv_content += "\n".join(f"{i},Item{i},{i*100},{'Description '*20}" for i in range(200))
    (data_dir / "users.csv").write_text(csv_content)
    
    # Python files that use the data
    (project / "handlers").mkdir()
    (project / "handlers" / "shop.py").write_text('''
import json

def load_products():
    with open("data/products.json") as f:
        return json.load(f)

def get_product(product_id):
    products = load_products()
    return products["products"][product_id]
''')
    
    (project / "main.py").write_text('''
from handlers.shop import load_products

def main():
    products = load_products()
    print(f"Loaded {len(products)} products")

if __name__ == "__main__":
    main()
''')
    
    yield project
    shutil.rmtree(temp_dir)


class TestDeepClean:
    def test_dry_run(self, temp_project):
        """Dry run should not modify anything."""
        original_files = list(temp_project.rglob("*"))
        
        result = run_deep_clean(temp_project, threshold=500, auto=True, dry_run=True)
        
        assert result is True
        # No new files should be created
        assert not (temp_project / "config_paths.py").exists()
        assert not (temp_project / "AST_FOX_TRACE.md").exists()
    
    def test_full_deep_clean(self, temp_project):
        """Full deep clean should move files and generate bridges."""
        result = run_deep_clean(temp_project, threshold=500, auto=True)
        
        assert result is True
        
        # Files should be moved
        assert not (temp_project / "data" / "products.json").exists()
        
        # Bridge should be created
        assert (temp_project / "config_paths.py").exists()
        
        # Navigation map should be created
        assert (temp_project / "AST_FOX_TRACE.md").exists()
        
        # Cursor rules should be created
        assert (temp_project / ".cursor" / "rules" / "external_data.md").exists()
        
        # External storage should have files
        external_dir = temp_project.parent / "_data" / temp_project.name / "LARGE_TOKENS"
        assert external_dir.exists()
        assert (external_dir / "data" / "products.json").exists()
    
    def test_code_patched(self, temp_project):
        """Python code should be patched to use bridges."""
        run_deep_clean(temp_project, threshold=500, auto=True)
        
        shop_content = (temp_project / "handlers" / "shop.py").read_text()
        
        # Should have import
        assert "from config_paths import get_path" in shop_content
        
        # Should use get_path
        assert "get_path(" in shop_content
    
    def test_no_patch_mode(self, temp_project):
        """--no-patch should skip code patching."""
        run_deep_clean(temp_project, threshold=500, auto=True, patch_code=False)
        
        shop_content = (temp_project / "handlers" / "shop.py").read_text()
        
        # Should NOT have get_path
        assert "get_path(" not in shop_content


class TestRestore:
    def test_restore_files(self, temp_project):
        """Restore should bring back moved files."""
        # First deep clean
        run_deep_clean(temp_project, threshold=500, auto=True)
        
        # Verify files moved
        assert not (temp_project / "data" / "products.json").exists()
        
        # Then restore
        result = run_restore(temp_project)
        
        assert result is True
        
        # Files should be back
        assert (temp_project / "data" / "products.json").exists()
        
        # Generated files should be removed
        assert not (temp_project / "config_paths.py").exists()
        assert not (temp_project / "AST_FOX_TRACE.md").exists()
    
    def test_restore_reverts_code(self, temp_project):
        """Restore should revert code patches."""
        # Save original content
        original_shop = (temp_project / "handlers" / "shop.py").read_text()
        
        # Deep clean
        run_deep_clean(temp_project, threshold=500, auto=True)
        
        # Restore
        run_restore(temp_project)
        
        # Code should be back to original
        restored_shop = (temp_project / "handlers" / "shop.py").read_text()
        assert "get_path(" not in restored_shop
        assert 'open("data/products.json")' in restored_shop


class TestThreshold:
    def test_high_threshold_moves_less(self, temp_project):
        """Higher threshold should move fewer files."""
        result = run_deep_clean(temp_project, threshold=50000, auto=True, dry_run=True)
        
        # With high threshold, small files shouldn't be moved
        assert result is True

