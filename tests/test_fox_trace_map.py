"""
Tests for Fox Trace Map generator.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import json

from src.utils.fox_trace_map import (
    find_file_usages,
    generate_file_description,
    generate_fox_trace_map,
    write_fox_trace_md,
    generate_cursor_context,
    write_cursor_rules,
    TracedFile,
    FoxTraceMap,
    FileUsage
)
from src.utils.heavy_mover import MovedFile
from src.utils.token_scanner import FileCategory


@pytest.fixture
def temp_project():
    """Create a temporary project."""
    temp_dir = tempfile.mkdtemp()
    project = Path(temp_dir) / "test_project"
    project.mkdir()
    
    # Create Python file that uses data files
    (project / "handlers").mkdir()
    (project / "handlers" / "buy.py").write_text('''
import json
from config_paths import get_path

def get_products():
    with open(get_path("data/products.json")) as f:
        return json.load(f)

def process_order(product_id):
    products = get_products()
    return products[product_id]
''')
    
    (project / "api").mkdir()
    (project / "api" / "products.py").write_text('''
import pandas as pd
from config_paths import get_path

def load_products():
    return pd.read_csv(get_path("data/products.csv"))
''')
    
    yield project
    shutil.rmtree(temp_dir)


@pytest.fixture
def moved_files():
    """Sample moved files."""
    return [
        MovedFile(
            original_path=Path("data/products.json"),
            original_relative="data/products.json",
            external_path=Path("../_data/test/LARGE_TOKENS/data/products.json"),
            external_relative="data/products.json",
            size_bytes=50000,
            estimated_tokens=12500,
            category=FileCategory.DATA,
            schema={
                "type": "json",
                "schema": {
                    "type": "array",
                    "keys": {"id": "integer", "name": "string", "price": "number"}
                }
            }
        ),
        MovedFile(
            original_path=Path("data/products.csv"),
            original_relative="data/products.csv",
            external_path=Path("../_data/test/LARGE_TOKENS/data/products.csv"),
            external_relative="data/products.csv",
            size_bytes=100000,
            estimated_tokens=25000,
            category=FileCategory.DATA,
            schema={
                "type": "csv",
                "schema": {
                    "columns": ["id", "name", "price", "category"],
                    "row_count": 1500
                }
            }
        ),
    ]


class TestFindFileUsages:
    def test_finds_usages(self, temp_project):
        usages = find_file_usages(temp_project, "data/products.json")
        
        assert len(usages) >= 1
        assert any(u.file.name == "buy.py" for u in usages)
    
    def test_detects_usage_type(self, temp_project):
        usages = find_file_usages(temp_project, "data/products.json")
        
        # Should detect json.load usage
        assert any("json" in u.usage_type.lower() or "read" in u.usage_type.lower() for u in usages)
    
    def test_finds_csv_usage(self, temp_project):
        usages = find_file_usages(temp_project, "data/products.csv")
        
        assert len(usages) >= 1
        assert any("pandas" in u.usage_type.lower() for u in usages)


class TestGenerateFileDescription:
    def test_generates_description(self, moved_files):
        traced = TracedFile(
            original_path=moved_files[0].original_relative,
            external_path=str(moved_files[0].external_path),
            category="data",
            estimated_tokens=moved_files[0].estimated_tokens,
            schema=moved_files[0].schema,
            schema_markdown="",
            usages=[FileUsage(Path("test.py"), 1, "test", "read")]
        )
        
        desc = generate_file_description(traced)
        
        assert "Data" in desc or "JSON" in desc
        assert len(desc) > 10


class TestGenerateFoxTraceMap:
    def test_generates_map(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        
        assert trace_map.project_name == temp_project.name
        assert trace_map.total_moved_files == 2
        assert trace_map.total_tokens_saved > 0
        assert len(trace_map.traced_files) == 2
    
    def test_finds_usages_in_map(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        
        # Should find usages for at least one file
        files_with_usages = [tf for tf in trace_map.traced_files if tf.usages]
        assert len(files_with_usages) >= 1


class TestWriteFoxTraceMd:
    def test_creates_file(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        output = write_fox_trace_md(trace_map, temp_project)
        
        assert output.exists()
        assert output.name == "AST_FOX_TRACE.md"
    
    def test_contains_summary(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        output = write_fox_trace_md(trace_map, temp_project)
        
        content = output.read_text()
        assert "Summary" in content
        assert "Files Moved" in content
    
    def test_contains_schemas(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        output = write_fox_trace_md(trace_map, temp_project)
        
        content = output.read_text()
        assert "Schema" in content
    
    def test_contains_access_pattern(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        output = write_fox_trace_md(trace_map, temp_project)
        
        content = output.read_text()
        assert "get_path" in content
        assert "config_paths" in content


class TestGenerateCursorContext:
    def test_generates_table(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        context = generate_cursor_context(trace_map)
        
        assert "| File |" in context
        assert "products.json" in context
    
    def test_compact_format(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        context = generate_cursor_context(trace_map)
        
        # Should be relatively compact
        assert len(context) < 2000


class TestWriteCursorRules:
    def test_creates_file(self, temp_project, moved_files):
        trace_map = generate_fox_trace_map(temp_project, moved_files)
        output = write_cursor_rules(trace_map, temp_project)
        
        assert output.exists()
        assert output.name == "external_data.md"
        assert ".cursor/rules" in str(output)

