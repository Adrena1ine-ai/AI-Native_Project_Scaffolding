# 📚 Prompts Library — AI Toolkit

> A curated collection of effective prompts for working with this codebase.
> Copy-paste these into Cursor to accelerate your workflow.

---

## 🧠 Section 1: Architecture (Composer Mode)

Use these prompts in **Composer** (Ctrl+I / Cmd+I) for multi-file changes.

### 🆕 Create New Command

```
Create a new CLI command called "export" that exports project configuration to JSON.

Requirements:
1. Create src/commands/export.py with export_project() and cmd_export() functions
2. Follow the pattern in src/commands/create.py
3. Add to src/commands/__init__.py
4. Add to src/cli.py (menu option + argparse subcommand)
5. Use COLORS for output formatting
6. Add type hints and docstrings

After: Run python3 generate_map.py
```

### 🔄 Refactor Module

```
Refactor src/generators/ai_configs.py to reduce duplication.

Current issue: Similar patterns repeat for each IDE config.
Solution: Extract common logic into a helper function.

Constraints:
- Don't break existing tests
- Keep the same public API
- Add docstrings to new functions
```

### 📦 Add New Template

```
Add a new project template called "discord" for Discord bots.

Steps:
1. Add template definition to TEMPLATES in src/core/constants.py
2. Add generate_discord_module() in src/commands/create.py
3. Include: bot.py, cogs/, utils/, config handling
4. Use discord.py library in requirements

Follow the pattern of the "bot" template.
```

### 🧹 Cleanup Task

```
Analyze src/commands/cleanup.py for potential improvements:
1. Are there any unused variables or imports?
2. Can any logic be simplified?
3. Are error messages clear and helpful?

Report findings in a table, then fix if approved.
```

### 🔍 Security Audit

```
Perform a security review of src/core/file_utils.py:

Check for:
- Path traversal vulnerabilities
- Unsafe file permissions
- Missing input validation

Output: Markdown table with | File | Line | Issue | Fix |
```

---

## 💬 Section 2: Coding (Chat Mode)

Use these prompts in **Chat** (Ctrl+L / Cmd+L) for explanations and small changes.

### 📖 Explain Logic

```
Explain how the create_project() function in src/commands/create.py works.
Focus on the order of operations and what each generator does.
```

### 📝 Generate Docstrings

```
Generate comprehensive docstrings for all functions in src/core/file_utils.py.
Use Google-style docstrings with Args, Returns, Raises sections.
```

### 🐛 Debug Help

```
I'm getting this error when running the cleanup command:
[paste error here]

The relevant code is in src/commands/cleanup.py.
What's causing this and how do I fix it?
```

### 🧪 Write Tests

```
Write pytest tests for the health_check() function in src/commands/health.py.

Cover:
- Clean project (should pass)
- Project with venv inside (should fail)
- Missing _AI_INCLUDE (should warn)
- Missing .env.example (should warn)
```

### 🔧 Quick Fix

```
In src/cli.py, the menu numbering is off after adding the review command.
Fix the numbering to be sequential: 1, 2, 3, 4, 5, 6, 7, 0 (exit).
```

### 📊 Code Review

```
Review this diff for potential issues:
[paste diff here]

Check for:
- Russian text (forbidden)
- Logic bugs
- PEP 8 violations
- Missing type hints
```

---

## 🚀 Section 3: Workflow Prompts

### 🏁 Start Session

```
I'm starting work on AI Toolkit.
1. Read CURRENT_CONTEXT_MAP.md
2. Summarize what commands are available
3. What's the current VERSION?
```

### 📋 Pre-Commit Check

```
Before I commit, please verify:
1. No Russian text in any changed files
2. All functions have docstrings
3. No unused imports
4. Type hints are present

Files changed: [list files]
```

### 🎯 Feature Planning

```
I want to add [feature description].

Please:
1. Identify which files need to change
2. Estimate complexity (Low/Medium/High)
3. List potential risks
4. Propose implementation steps
```

---

## 💡 Pro Tips

1. **Be Specific**: Include file paths and function names
2. **Set Constraints**: "Don't break tests", "Keep API stable"
3. **Request Format**: "Output as table", "Use bullet points"
4. **Chain Prompts**: Start broad, then narrow down
5. **Verify**: Always run tests after AI changes

---

*Last updated: v3.1*

