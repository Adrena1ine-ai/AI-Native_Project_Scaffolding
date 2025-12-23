"""
🦊 Fox Trace — Deep Dependency Tracker
Recursively traces imports to build minimal, perfect AI context
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from dataclasses import dataclass, field
from xml.sax.saxutils import escape
from datetime import datetime

from ..core.constants import COLORS, VERSION


# Standard library modules to ignore (Python 3.10+)
# This is a comprehensive but not exhaustive list
STDLIB_MODULES = {
    # Built-ins
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore",
    "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect",
    "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd",
    "code", "codecs", "codeop", "collections", "colorsys", "compileall",
    "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg",
    "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime",
    "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email",
    "encodings", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass",
    "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac",
    "html", "http", "idlelib", "imaplib", "imghdr", "imp", "importlib", "inspect",
    "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache",
    "locale", "logging", "lzma", "mailbox", "mailcap", "marshal", "math",
    "mimetypes", "mmap", "modulefinder", "multiprocessing", "netrc", "nis",
    "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib",
    "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib",
    "poplib", "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd",
    "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re",
    "readline", "reprlib", "resource", "rlcompleter", "runpy", "sched", "secrets",
    "select", "selectors", "shelve", "shlex", "shutil", "signal", "site",
    "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd", "sqlite3",
    "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile",
    "telnetlib", "tempfile", "termios", "test", "textwrap", "threading", "time",
    "timeit", "tkinter", "token", "tokenize", "tomllib", "trace", "traceback",
    "tracemalloc", "tty", "turtle", "turtledemo", "types", "typing", "unicodedata",
    "unittest", "urllib", "uu", "uuid", "venv", "warnings", "wave", "weakref",
    "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
    "zipapp", "zipfile", "zipimport", "zlib", "_thread",
    # Common typing extensions
    "typing_extensions",
}

# Common third-party packages to ignore
THIRD_PARTY_PREFIXES = {
    "aiogram", "aiohttp", "aiosqlite", "alembic", "anyio", "asyncpg",
    "beautifulsoup4", "bs4", "celery", "certifi", "click", "cryptography",
    "django", "dotenv", "environs", "fastapi", "flask", "grpcio", "httpx",
    "jinja2", "marshmallow", "motor", "numpy", "openai", "pandas", "passlib",
    "pillow", "PIL", "playwright", "psycopg2", "pydantic", "pygments",
    "pymongo", "pyperclip", "pytest", "python_dotenv", "redis", "requests",
    "rich", "scipy", "scrapy", "selenium", "sqlalchemy", "starlette",
    "tenacity", "textual", "toml", "tortoise", "trio", "typer", "uvicorn",
    "websockets", "yaml", "pyyaml",
}


@dataclass
class ImportInfo:
    """Information about an import"""
    module: str
    names: list[str] = field(default_factory=list)
    is_from: bool = False
    level: int = 0  # For relative imports


@dataclass
class TracedFile:
    """A traced file with its content and metadata"""
    path: Path
    relative_path: str
    content: str
    reason: str  # "entry" or "import"
    depth: int


def extract_imports(file_path: Path) -> list[ImportInfo]:
    """
    Extract all imports from a Python file using AST
    
    Args:
        file_path: Path to Python file
        
    Returns:
        List of ImportInfo objects
    """
    imports = []
    
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(content, filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(ImportInfo(
                        module=alias.name,
                        names=[alias.asname or alias.name],
                        is_from=False,
                        level=0
                    ))
            
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names = [alias.name for alias in node.names]
                    imports.append(ImportInfo(
                        module=node.module,
                        names=names,
                        is_from=True,
                        level=node.level
                    ))
    
    except SyntaxError:
        pass
    except Exception:
        pass
    
    return imports


def is_stdlib_or_thirdparty(module: str) -> bool:
    """
    Check if a module is standard library or third-party
    
    Args:
        module: Module name (e.g., "os", "pandas", "utils.db")
        
    Returns:
        True if stdlib/third-party, False if likely local
    """
    # Get the top-level module name
    top_level = module.split(".")[0]
    
    # Check stdlib
    if top_level in STDLIB_MODULES:
        return True
    
    # Check third-party prefixes
    if top_level.lower() in THIRD_PARTY_PREFIXES:
        return True
    
    # Check if it's a known third-party by trying to find in sys.modules
    # that starts with common patterns
    if top_level.startswith("_"):
        return True  # Private stdlib modules
    
    return False


def resolve_import_path(
    import_info: ImportInfo,
    current_file: Path,
    project_root: Path
) -> Path | None:
    """
    Resolve an import to its actual file path
    
    Args:
        import_info: Import information
        current_file: The file containing the import
        project_root: Project root directory
        
    Returns:
        Resolved Path or None if not found/not local
    """
    module = import_info.module
    
    # Skip stdlib and third-party
    if is_stdlib_or_thirdparty(module):
        return None
    
    # Handle relative imports
    if import_info.level > 0:
        # Relative import: go up `level` directories from current file
        base_dir = current_file.parent
        for _ in range(import_info.level - 1):
            base_dir = base_dir.parent
        
        if module:
            module_parts = module.split(".")
            candidate = base_dir / "/".join(module_parts)
        else:
            # from . import X — imports from same package
            candidate = base_dir
    else:
        # Absolute import: try various locations
        module_parts = module.split(".")
        
        # Try from project root
        candidate = project_root / "/".join(module_parts)
    
    # Check for module.py
    py_file = candidate.with_suffix(".py")
    if py_file.exists():
        return py_file
    
    # Check for package/__init__.py
    init_file = candidate / "__init__.py"
    if init_file.exists():
        return init_file
    
    # Try src/ prefix (common pattern)
    src_candidate = project_root / "src" / "/".join(module.split("."))
    py_file = src_candidate.with_suffix(".py")
    if py_file.exists():
        return py_file
    init_file = src_candidate / "__init__.py"
    if init_file.exists():
        return init_file
    
    return None


def trace_dependencies(
    entry_file: Path,
    project_root: Path,
    max_depth: int = 2
) -> list[TracedFile]:
    """
    Recursively trace all dependencies of an entry file
    
    Args:
        entry_file: The starting file to trace from
        project_root: Project root directory
        max_depth: Maximum recursion depth
        
    Returns:
        List of TracedFile objects (deduplicated)
    """
    traced: dict[str, TracedFile] = {}  # path -> TracedFile
    
    def trace_file(file_path: Path, depth: int, reason: str) -> None:
        """Recursively trace a single file"""
        # Resolve to absolute path
        file_path = file_path.resolve()
        
        # Get relative path for deduplication
        try:
            rel_path = str(file_path.relative_to(project_root))
        except ValueError:
            rel_path = str(file_path)
        
        # Skip if already traced
        if rel_path in traced:
            return
        
        # Skip if file doesn't exist
        if not file_path.exists():
            return
        
        # Read content
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return
        
        # Add to traced
        traced[rel_path] = TracedFile(
            path=file_path,
            relative_path=rel_path,
            content=content,
            reason=reason,
            depth=depth
        )
        
        # Stop recursion if at max depth
        if depth >= max_depth:
            return
        
        # Extract and trace imports
        imports = extract_imports(file_path)
        
        for imp in imports:
            resolved = resolve_import_path(imp, file_path, project_root)
            if resolved:
                trace_file(resolved, depth + 1, "import")
    
    # Start tracing from entry file
    trace_file(entry_file, 0, "entry")
    
    # Sort by depth then path
    result = sorted(traced.values(), key=lambda f: (f.depth, f.relative_path))
    
    return result


def generate_trace_xml(
    entry_file: str,
    traced_files: list[TracedFile]
) -> str:
    """
    Generate XML output for traced dependencies
    
    Args:
        entry_file: Original entry file path
        traced_files: List of traced files
        
    Returns:
        XML string
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!--',
        f'  🦊 Fox Trace — Dependency Context v{VERSION}',
        f'  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'  Entry: {entry_file}',
        f'  Files traced: {len(traced_files)}',
        '',
        '  This context contains only files mathematically related to the entry point.',
        '  Perfect for focused AI analysis.',
        '-->',
        f'<context_trace entry="{escape(entry_file)}">',
    ]
    
    for tf in traced_files:
        tag = "file" if tf.reason == "entry" else "dependency"
        attrs = f'path="{escape(tf.relative_path)}"'
        if tf.reason != "entry":
            attrs += f' reason="{tf.reason}" depth="{tf.depth}"'
        
        lines.append(f'  <{tag} {attrs}>')
        lines.append(escape(tf.content))
        lines.append(f'  </{tag}>')
    
    lines.append('</context_trace>')
    
    return "\n".join(lines)


def trace_file_dependencies(
    entry_file: str | Path,
    project_root: str | Path | None = None,
    depth: int = 2,
    output_file: str | None = None
) -> tuple[bool, int, str]:
    """
    Main function to trace dependencies and generate output
    
    Args:
        entry_file: Path to entry file
        project_root: Project root (defaults to cwd)
        depth: Maximum trace depth
        output_file: Optional output file path
        
    Returns:
        Tuple of (success, file_count, xml_content)
    """
    entry_path = Path(entry_file).resolve()
    
    if not entry_path.exists():
        return False, 0, f"File not found: {entry_file}"
    
    if not entry_path.suffix == ".py":
        return False, 0, "Entry file must be a Python file (.py)"
    
    # Determine project root
    if project_root:
        root = Path(project_root).resolve()
    else:
        # Try to find project root (look for common markers)
        root = entry_path.parent
        for _ in range(5):  # Max 5 levels up
            if any((root / marker).exists() for marker in [
                "pyproject.toml", "setup.py", ".git", "requirements.txt"
            ]):
                break
            parent = root.parent
            if parent == root:
                break
            root = parent
    
    # Trace dependencies
    traced = trace_dependencies(entry_path, root, depth)
    
    # Generate XML
    try:
        rel_entry = str(entry_path.relative_to(root))
    except ValueError:
        rel_entry = str(entry_path)
    
    xml_content = generate_trace_xml(rel_entry, traced)
    
    # Save if output file specified
    if output_file:
        try:
            Path(output_file).write_text(xml_content, encoding="utf-8")
        except Exception as e:
            return False, len(traced), f"Failed to write: {e}"
    
    return True, len(traced), xml_content


def cmd_trace() -> None:
    """Interactive trace command"""
    print(COLORS.colorize("\n🦊 FOX TRACE — Dependency Tracker\n", COLORS.GREEN))
    
    # Get entry file
    entry = input("  Entry file (e.g., handlers/payment.py): ").strip()
    if not entry:
        print(COLORS.error("No entry file specified"))
        return
    
    entry_path = Path(entry)
    if not entry_path.exists():
        print(COLORS.error(f"File not found: {entry}"))
        return
    
    # Get depth
    depth_str = input("  Trace depth [2]: ").strip() or "2"
    try:
        depth = int(depth_str)
    except ValueError:
        depth = 2
    
    # Get output file
    output = input("  Output file [print to stdout]: ").strip() or None
    
    print(f"\n  🔍 Tracing from {entry} (depth={depth})...\n")
    
    success, count, result = trace_file_dependencies(entry, depth=depth, output_file=output)
    
    if success:
        print(f"  {COLORS.success(f'Traced {count} files')}")
        
        if output:
            print(f"  📄 Saved to: {output}")
        else:
            # Estimate tokens
            tokens = len(result) // 4
            print(f"  📊 Context size: {len(result)} chars (~{tokens} tokens)")
            print()
            print("=" * 60)
            # Print truncated if very large
            if len(result) > 10000:
                print(result[:5000])
                print("\n... (truncated) ...\n")
                print(result[-2000:])
            else:
                print(result)
            print("=" * 60)
    else:
        print(COLORS.error(result))

