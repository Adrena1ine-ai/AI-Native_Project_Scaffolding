"""
Pytest fixtures for AI Toolkit tests
"""

import pytest
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests"""
    return tmp_path


@pytest.fixture
def temp_project(tmp_path):
    """Create a basic temporary project structure"""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create basic structure
    (project_dir / "main.py").write_text("# Main file\n")
    (project_dir / ".gitignore").write_text("*.pyc\n__pycache__/\n")
    
    return project_dir


@pytest.fixture
def temp_project_with_venv(temp_project):
    """Create a project with venv inside (problematic state)"""
    venv_dir = temp_project / "venv"
    venv_dir.mkdir()
    (venv_dir / "pyvenv.cfg").write_text("home = /usr/bin/python3\n")
    (venv_dir / "lib").mkdir()
    
    return temp_project


@pytest.fixture
def clean_project(tmp_path):
    """Create a properly configured AI Toolkit project"""
    project_dir = tmp_path / "clean_project"
    project_dir.mkdir()
    
    # Create proper structure
    (project_dir / "main.py").write_text("# Main file\n")
    (project_dir / ".gitignore").write_text("*.pyc\n__pycache__/\nvenv/\n")
    (project_dir / "requirements.txt").write_text("pyyaml>=6.0\n")
    (project_dir / ".env.example").write_text("API_KEY=your_key_here\n")
    (project_dir / ".cursorrules").write_text("# Cursor rules\n")
    (project_dir / ".cursorignore").write_text("venv/\n")
    (project_dir / ".toolkit-version").write_text("3.0.0\n")
    
    # Create _AI_INCLUDE
    ai_include = project_dir / "_AI_INCLUDE"
    ai_include.mkdir()
    (ai_include / "PROJECT_CONVENTIONS.md").write_text("# Conventions\n")
    (ai_include / "WHERE_IS_WHAT.md").write_text("# Where is what\n")
    
    # Create scripts
    scripts = project_dir / "scripts"
    scripts.mkdir()
    (scripts / "bootstrap.sh").write_text("#!/bin/bash\necho 'bootstrap'\n")
    (scripts / "bootstrap.ps1").write_text("# PowerShell bootstrap\n")
    
    return project_dir

