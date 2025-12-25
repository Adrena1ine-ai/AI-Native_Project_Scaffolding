"""
Tests for schema_extractor module
"""

import pytest
from pathlib import Path
import json
import tempfile
import sqlite3

from src.utils.schema_extractor import (
    extract_json_schema,
    extract_csv_schema,
    extract_sqlite_schema,
    extract_schema,
    schema_to_markdown,
    _infer_type,
    _extract_structure
)


@pytest.fixture
def temp_json():
    """Create temporary JSON file"""
    data = {
        "users": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}],
        "config": {"debug": True, "version": "1.0"}
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data, f)
        return Path(f.name)


@pytest.fixture
def temp_csv():
    """Create temporary CSV file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        f.write("id,name,price\n1,Apple,1.50\n2,Banana,0.75\n3,Orange,2.00\n")
        return Path(f.name)


@pytest.fixture
def temp_sqlite():
    """Create temporary SQLite database"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            age INTEGER
        )
    """)
    cursor.execute("INSERT INTO users (email, age) VALUES ('test@example.com', 30)")
    cursor.execute("INSERT INTO users (email, age) VALUES ('user@example.com', 25)")
    conn.commit()
    conn.close()
    
    return db_path


class TestTypeInference:
    def test_infers_string(self):
        assert _infer_type("hello") == "string"
    
    def test_infers_integer(self):
        assert _infer_type(42) == "integer"
    
    def test_infers_float(self):
        assert _infer_type(3.14) == "number"
    
    def test_infers_boolean(self):
        assert _infer_type(True) == "boolean"
    
    def test_infers_null(self):
        assert _infer_type(None) == "null"
    
    def test_infers_array(self):
        assert _infer_type([1, 2, 3]) == "array"
    
    def test_infers_object(self):
        assert _infer_type({"key": "value"}) == "object"


class TestJsonSchema:
    def test_extracts_keys(self, temp_json):
        schema = extract_json_schema(temp_json)
        assert "keys" in schema
        assert "users" in schema["keys"]
        assert "config" in schema["keys"]
    
    def test_detects_array(self, temp_json):
        schema = extract_json_schema(temp_json)
        assert schema["keys"]["users"]["type"] == "array"
    
    def test_no_values_in_output(self, temp_json):
        schema = extract_json_schema(temp_json)
        schema_str = str(schema)
        assert "John" not in schema_str
        assert "30" not in schema_str
        assert "Jane" not in schema_str
    
    def test_detects_nested_structure(self, temp_json):
        schema = extract_json_schema(temp_json)
        users_schema = schema["keys"]["users"]
        assert users_schema["type"] == "array"
        assert "items" in users_schema
        assert users_schema["items"]["type"] == "object"
        assert "name" in users_schema["items"]["keys"]
        assert "age" in users_schema["items"]["keys"]


class TestCsvSchema:
    def test_extracts_columns(self, temp_csv):
        schema = extract_csv_schema(temp_csv)
        assert schema["columns"] == ["id", "name", "price"]
    
    def test_infers_types(self, temp_csv):
        schema = extract_csv_schema(temp_csv)
        assert schema["types"]["id"] == "int"
        assert schema["types"]["price"] == "float"
        assert schema["types"]["name"] == "str"
    
    def test_counts_rows(self, temp_csv):
        schema = extract_csv_schema(temp_csv)
        assert schema["row_count"] == 3
    
    def test_includes_sample(self, temp_csv):
        schema = extract_csv_schema(temp_csv)
        assert "sample" in schema
        assert len(schema["sample"]) > 0


class TestSqliteSchema:
    def test_extracts_tables(self, temp_sqlite):
        schema = extract_sqlite_schema(temp_sqlite)
        assert "tables" in schema
        assert "users" in schema["tables"]
    
    def test_extracts_columns(self, temp_sqlite):
        schema = extract_sqlite_schema(temp_sqlite)
        users_table = schema["tables"]["users"]
        assert "columns" in users_table
        
        column_names = [col["name"] for col in users_table["columns"]]
        assert "id" in column_names
        assert "email" in column_names
        assert "age" in column_names
    
    def test_detects_primary_key(self, temp_sqlite):
        schema = extract_sqlite_schema(temp_sqlite)
        users_table = schema["tables"]["users"]
        id_col = next(col for col in users_table["columns"] if col["name"] == "id")
        assert id_col["pk"] is True
    
    def test_counts_rows(self, temp_sqlite):
        schema = extract_sqlite_schema(temp_sqlite)
        users_table = schema["tables"]["users"]
        assert users_table["row_count"] == 2


class TestAutoDetect:
    def test_detects_json(self, temp_json):
        result = extract_schema(temp_json)
        assert result is not None
        assert result["type"] == "json"
        assert "schema" in result
    
    def test_detects_csv(self, temp_csv):
        result = extract_schema(temp_csv)
        assert result is not None
        assert result["type"] == "csv"
        assert "schema" in result
    
    def test_detects_sqlite(self, temp_sqlite):
        result = extract_schema(Path(temp_sqlite))
        assert result is not None
        assert result["type"] == "sqlite"
        assert "schema" in result
    
    def test_includes_metadata(self, temp_json):
        result = extract_schema(temp_json)
        assert "file" in result
        assert "size_bytes" in result
        assert "estimated_tokens" in result
    
    def test_returns_none_for_nonexistent_file(self):
        result = extract_schema(Path("/nonexistent/file.json"))
        assert result is None


class TestMarkdown:
    def test_generates_markdown(self, temp_json):
        schema = extract_schema(temp_json)
        md = schema_to_markdown(schema)
        assert "##" in md
        assert "json" in md.lower()
        assert temp_json.name in md
    
    def test_includes_token_estimate(self, temp_json):
        schema = extract_schema(temp_json)
        md = schema_to_markdown(schema)
        assert "tokens" in md.lower()
    
    def test_csv_markdown_format(self, temp_csv):
        schema = extract_schema(temp_csv)
        md = schema_to_markdown(schema)
        assert "Columns" in md
        assert "Rows" in md
        assert "|" in md  # Table format
    
    def test_sqlite_markdown_format(self, temp_sqlite):
        schema = extract_schema(Path(temp_sqlite))
        md = schema_to_markdown(schema)
        assert "Tables" in md
        assert "users" in md
        assert "|" in md  # Table format


class TestStructureExtraction:
    def test_handles_empty_dict(self):
        result = _extract_structure({}, 0, 3)
        assert result["type"] == "object"
        assert result["keys"] == {}
    
    def test_handles_empty_list(self):
        result = _extract_structure([], 0, 3)
        assert result["type"] == "array"
        assert result["items"] == "empty"
    
    def test_respects_max_depth(self):
        nested = {"level1": {"level2": {"level3": {"level4": "deep"}}}}
        result = _extract_structure(nested, 0, 2)
        assert "truncated" in result["keys"]["level1"]["keys"]["level2"]
    
    def test_preserves_array_length(self):
        arr = [1, 2, 3, 4, 5]
        result = _extract_structure(arr, 0, 3)
        assert result["length"] == 5

