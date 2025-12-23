# 🔧 AI Toolkit — CLI Architecture

## Entry Points

```bash
python main.py          # Direct execution
python -m src.cli       # Module execution
ai-toolkit              # After pip install
```

## Adding a New Command

1. Create `src/commands/yourcommand.py`:
   ```python
   """Your command description"""
   from ..core.constants import COLORS
   
   def yourcommand_action(path: Path, **kwargs) -> bool:
       """Core logic (testable)"""
       # Implementation
       return True
   
   def cmd_yourcommand() -> None:
       """Interactive wrapper (CLI)"""
       print(COLORS.colorize("\n🆕 YOUR COMMAND\n", COLORS.GREEN))
       # Get user input, call yourcommand_action()
   ```

2. Export in `src/commands/__init__.py`:
   ```python
   from .yourcommand import cmd_yourcommand, yourcommand_action
   __all__ = [..., "cmd_yourcommand", "yourcommand_action"]
   ```

3. Add to CLI in `src/cli.py`:
   - Import the command
   - Add to `print_menu()` list
   - Add to `interactive_mode()` dispatch dict
   - Add subparser in `cli_mode()`

4. Add tests in `tests/test_yourcommand.py`

## Generator Pattern

Generators in `src/generators/` follow this pattern:

```python
def generate_something(project_dir: Path, project_name: str, **context) -> None:
    """Generate something for the project"""
    content = f'''Template content for {project_name}'''
    create_file(project_dir / "path/to/file", content)
```

## Constants

All magic values live in `src/core/constants.py`:
- `VERSION` — Current version string
- `TEMPLATES` — Project template definitions
- `IDE_CONFIGS` — IDE-specific file mappings
- `COLORS` — Terminal color codes

## Testing

```bash
pytest tests/ -v                    # All tests
pytest tests/test_create.py -v      # Specific file
pytest -k "test_bot" -v             # Pattern match
```

## Automation Rule

**ALWAYS run after creating/deleting files:**
```bash
python3 generate_map.py
```
Then read `CURRENT_CONTEXT_MAP.md` to update your mental model.

