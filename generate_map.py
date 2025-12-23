import os
import re
from pathlib import Path

# ==========================================
# ⚙️ SETTINGS (FROM AI TOOLKIT MANIFESTO)
# ==========================================

# Directories the AI should never see
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', 
    'venv', '.venv', 'env', 
    '__pycache__', 
    'node_modules', 'dist', 'build',
    'logs', 'data', 'media', 'staticfiles'
}

# Files not needed in the map (binaries, locks, cache)
IGNORE_FILES = {
    'generate_map.py', 'CURRENT_CONTEXT_MAP.md', 
    '.DS_Store', 'poetry.lock', 'package-lock.json', 'yarn.lock'
}

# Extensions we ignore
IGNORE_EXT = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.class', '.exe', 
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', 
    '.woff', '.woff2', '.ttf', '.eot', 
    '.zip', '.tar', '.gz', '.7z', '.rar',
    '.db', '.sqlite', '.sqlite3'
}

# Regex for finding classes and functions (Regex - Architect's choice)
# Catches: class Name, def name, async def name
DEFINITION_PATTERN = re.compile(r'^\s*(class|def|async\s+def)\s+([a-zA-Z0-9_]+)')

def estimate_tokens(text):
    """Approximate token estimation (1 token ≈ 4 chars)"""
    return len(text) // 4

def get_definitions(file_path):
    """Fast file reading via Regex without AST parsing"""
    definitions = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = DEFINITION_PATTERN.match(line)
                if match:
                    type_ = match.group(1).replace('async def', 'async_def') # Simplify for output
                    name = match.group(2)
                    
                    # Format with icons for clarity
                    if 'class' in type_:
                        definitions.append(f"  📦 {name}")
                    else:
                        definitions.append(f"    ƒ {name}")
    except Exception:
        pass # If file is broken or unreadable - skip
    return definitions

def generate_map():
    root_path = Path('.')
    output_lines = []
    
    # Header for AI
    output_lines.append("# 🗺️ PROJECT CONTEXT MAP")
    output_lines.append("> Auto-generated structure. AI: Read this file to understand where code is located.\n")
    
    total_files = 0
    
    for root, dirs, files in os.walk(root_path):
        # 1. In-place folder filtration
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_root = Path(root)
        
        # Sort for aesthetics
        files.sort()
        
        for file in files:
            file_path = rel_root / file
            
            # Skip ignored files and extensions
            if file in IGNORE_FILES or file_path.suffix in IGNORE_EXT:
                continue
                
            total_files += 1
            
            # Add file to list
            output_lines.append(f"- `{file_path}`")
            
            # If it's a Python file - dive inside
            if file.endswith('.py'):
                defs = get_definitions(file_path)
                if defs:
                    output_lines.extend(defs)
            
            output_lines.append("") # Empty line separator

    # Final write
    result_text = "\n".join(output_lines)
    
    # Statistics
    map_tokens = estimate_tokens(result_text)
    stats = f"\n---\n**Stats:** Scanned {total_files} files. Map size: ~{map_tokens} tokens."
    result_text += stats

    with open("CURRENT_CONTEXT_MAP.md", "w", encoding="utf-8") as f:
        f.write(result_text)
        
    print(f"✅ Context Map Updated! (~{map_tokens} tokens)")
    print(f"   Created: CURRENT_CONTEXT_MAP.md")

if __name__ == "__main__":
    generate_map()
    
    # Also update PROJECT_STATUS.md
    try:
        from pathlib import Path
        from src.utils.status_generator import update_status
        update_status(Path.cwd(), skip_tests=True)
        print("📊 PROJECT_STATUS.md updated")
    except ImportError:
        pass  # status_generator not yet created

