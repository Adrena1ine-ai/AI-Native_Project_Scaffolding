# 🔌 Cursor/VSCode Integration — Automatic Setup

## Overview

The Doctor command now automatically configures Cursor and VSCode to use your external virtual environment, eliminating manual setup steps.

## What Gets Configured

### 1. `.vscode/settings.json`

Doctor creates this file with:

```json
{
  "python.defaultInterpreterPath": "../_venvs/project-main/bin/python",
  "python.terminal.activateEnvironment": true
}
```

This tells Cursor/VSCode:
- ✅ Use the external venv automatically
- ✅ Activate it when opening terminals
- ✅ Use it for IntelliSense and linting

### 2. Relative Paths (Portable)

The path is **relative** to your project:
```
../_venvs/project-main/
```

This means:
- ✅ Works on any machine
- ✅ Works on Windows, Linux, Mac
- ✅ Can commit to git (team-wide)

### 3. Platform Detection

Doctor automatically uses the correct Python executable:

| Platform | Path |
|----------|------|
| Windows | `../_venvs/project-main/Scripts/python.exe` |
| Linux/Mac | `../_venvs/project-main/bin/python` |

## How It Works

### Automatic Detection

When you run `doctor --auto`, it:

1. **Checks** if external venv exists at `../_venvs/project-main/`
2. **Detects** if `.vscode/settings.json` is missing
3. **Creates** the configuration automatically

### Manual Trigger

```bash
# Run doctor
python main.py doctor /path/to/project

# In interactive mode, fix the issue:
> Enter choice: [issue_number]
```

The issue will show as:
```
🟢 SUGGESTION
├─ [X] Missing Cursor/VSCode interpreter configuration
```

## Verification

### Check Configuration

```bash
# View the created settings
cat .vscode/settings.json
```

Should show:
```json
{
  "python.defaultInterpreterPath": "../_venvs/YourProject-main/bin/python",
  "python.terminal.activateEnvironment": true
}
```

### Test in Cursor

1. **Open project** in Cursor
2. **Open terminal** (Ctrl+`)
3. **Check Python path**:
   ```bash
   which python  # Linux/Mac
   where python  # Windows
   ```

Should point to: `../_venvs/project-main/...`

### Test IntelliSense

1. Open a `.py` file
2. Import a package from your venv
3. IntelliSense should work (autocomplete, go-to-definition)

## Troubleshooting

### Cursor Still Uses Wrong Python

**Solution 1: Reload Window**
```
Ctrl+Shift+P → Developer: Reload Window
```

**Solution 2: Manual Selection**
```
Ctrl+Shift+P → Python: Select Interpreter
→ Choose: ../_venvs/project-main/bin/python
```

**Solution 3: Delete Cache**
```bash
# Close Cursor first
rm -rf .vscode/.ropeproject
rm -rf .vscode/__pycache__
```

### Path Not Found

Check that venv exists:
```bash
ls ../_venvs/project-main/
```

If missing, run bootstrap:
```bash
./scripts/bootstrap.sh  # Linux/Mac
./scripts/bootstrap.ps1  # Windows
```

### Relative Path Issues

If you move the project, the relative path breaks.

**Fix:**
```bash
# Re-run doctor to regenerate settings
python main.py doctor . --auto
```

## Advanced Configuration

### Custom Venv Location

If your venv is elsewhere, edit `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "/custom/path/to/venv/bin/python"
}
```

### Multiple Python Versions

For projects with multiple Python versions:

```json
{
  "python.defaultInterpreterPath": "../_venvs/project-py311/bin/python",
  "python.pythonPath": "../_venvs/project-py311/bin/python"
}
```

### Additional Settings

Doctor creates minimal settings. You can add more:

```json
{
  "python.defaultInterpreterPath": "../_venvs/project-main/bin/python",
  "python.terminal.activateEnvironment": true,
  
  // Additional settings
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true
}
```

## Integration with Other Tools

### PyCharm

PyCharm doesn't use `.vscode/settings.json`. Configure manually:
```
File → Settings → Project → Python Interpreter
→ Add → Existing Environment
→ Browse to: ../_venvs/project-main/bin/python
```

### VS Code (non-Cursor)

Works identically! The `.vscode/settings.json` is standard.

### Jupyter Notebooks

If using Jupyter in Cursor:
```json
{
  "python.defaultInterpreterPath": "../_venvs/project-main/bin/python",
  "jupyter.jupyterServerType": "local"
}
```

## Best Practices

### 1. Commit `.vscode/settings.json`

```bash
git add .vscode/settings.json
git commit -m "chore: add vscode interpreter config"
```

This helps your team use the same setup.

### 2. Add to `.gitignore` (Optional)

If you want personal settings:
```gitignore
# .gitignore
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
```

### 3. Document in README

```markdown
## Setup

1. Run bootstrap: `./scripts/bootstrap.sh`
2. Open in Cursor — interpreter auto-configured!
3. Start coding
```

### 4. CI/CD Compatibility

The relative path works in CI/CD:
```yaml
# .github/workflows/test.yml
- name: Setup venv
  run: ./scripts/bootstrap.sh

- name: Run tests
  run: |
    source ../_venvs/${{ github.event.repository.name }}-main/bin/activate
    pytest
```

## FAQ

### Q: Does this work with Windsurf?

**A:** Yes! Windsurf is based on VSCode and uses the same settings.

### Q: What if I have multiple projects?

**A:** Each project gets its own venv:
```
_venvs/
  ├── project1-main/
  ├── project2-main/
  └── project3-main/
```

Each `.vscode/settings.json` points to its own venv.

### Q: Can I use virtualenvwrapper?

**A:** Yes, but you'll need to manually configure the path:
```json
{
  "python.defaultInterpreterPath": "~/.virtualenvs/project/bin/python"
}
```

### Q: Does this affect system Python?

**A:** No! The venv is isolated. System Python remains untouched.

## See Also

- [Doctor Command Guide](DOCTOR_COMMAND.md)
- [Bootstrap Scripts](BOOTSTRAP.md)
- [Virtual Environment Best Practices](VENV_BEST_PRACTICES.md)

