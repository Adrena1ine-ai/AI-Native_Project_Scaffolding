# ⚖️ Tradeoffs — Architectural Decisions

> This document explains the "why" behind key architectural choices in AI Toolkit.
> Understanding these tradeoffs helps contributors make consistent decisions.

---

## 🖥️ Why CLI-First?

### Decision
AI Toolkit is a **command-line tool** first, with optional web/GUI interfaces.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Web App | Visual, accessible | Requires server, dependencies |
| GUI (Tkinter) | Native, no server | Platform-specific, heavy |
| **CLI** ✅ | Fast, scriptable, universal | Less visual |

### Rationale
1. **Speed**: CLI starts instantly, no browser/runtime overhead
2. **Automation**: Easily integrated into scripts, CI/CD, Makefiles
3. **Universality**: Works on any system with Python 3.10+
4. **AI-Native**: AI assistants work better with text-based interfaces
5. **Minimal Dependencies**: No web framework, no GUI toolkit

### Tradeoff Accepted
Users must be comfortable with terminal. Mitigated by interactive prompts and clear help messages.

---

## 📁 Why `.cursor/rules/` Structure?

### Decision
Rules are split into modular files under `.cursor/rules/` instead of one monolithic `.cursorrules`.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Single `.cursorrules` | Simple, one file | Gets long, hard to maintain |
| **Modular `.cursor/rules/`** ✅ | Organized, focused | More files to manage |
| README-embedded | Visible to humans | Mixed concerns |

### Rationale
1. **AI-Native Config**: Follows Cursor's recommended structure
2. **Separation of Concerns**: Project context vs CLI patterns vs review guidelines
3. **Maintainability**: Edit one aspect without touching others
4. **Reusability**: Rules can be copied to generated projects

### Tradeoff Accepted
Multiple files to manage. Mitigated by clear naming and root `.cursorrules` as index.

---

## 💾 Why No Database?

### Decision
All data is stored in **files** (JSON, YAML, Markdown). No SQLite, no ORM.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| SQLite | Query power, ACID | Dependency, migration complexity |
| TinyDB | Simple, JSON-based | Another dependency |
| **File System** ✅ | Zero dependencies, human-readable | No queries, manual parsing |

### Rationale
1. **Simplicity**: No schema migrations, no connection handling
2. **Portability**: Copy folder = copy everything
3. **Transparency**: Users can read/edit config files directly
4. **Scope**: This tool generates projects, it doesn't manage long-term data
5. **AI-Friendly**: AI can read JSON/YAML easily

### Tradeoff Accepted
No complex queries. Acceptable because our data model is simple (config, templates).

---

## 🌍 Why English-Only in Code?

### Decision
All code, comments, docstrings, and error messages must be in **English**.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Localized code | Native speakers comfortable | Maintenance nightmare |
| **English-only** ✅ | Universal, standard | Non-native speakers slower |
| Mixed | Flexible | Inconsistent, confusing |

### Rationale
1. **Industry Standard**: Python community uses English
2. **AI Compatibility**: LLMs trained primarily on English code
3. **Collaboration**: Contributors worldwide can understand
4. **Searchability**: Stack Overflow, docs, all in English

### Tradeoff Accepted
Russian-speaking developers must write in English. Mitigated by simple vocabulary and the `review` command that catches Russian text.

---

## 📦 Why External venv?

### Decision
Virtual environments are stored **outside** the project directory in `../_venvs/`.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| `venv/` inside project | Standard, expected | Pollutes AI context, 500MB+ |
| **External `_venvs/`** ✅ | Clean project, fast AI | Non-standard, requires bootstrap |
| No venv (global) | Simple | Dependency conflicts |

### Rationale
1. **AI Context**: 50,000+ files in venv confuse AI assistants
2. **IDE Performance**: Cursor/VS Code index faster without venv
3. **Git Cleanliness**: No risk of accidentally committing venv
4. **Token Savings**: ~500MB of code AI doesn't need to see

### Tradeoff Accepted
Users must run `bootstrap.sh` instead of `python -m venv venv`. Mitigated by clear documentation and scripts.

---

## 🔌 Why Plugin System (Future)?

### Decision
Extensibility via a `plugins/` directory with hook-based architecture.

### Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| Monolithic | Simple, all-in-one | Hard to extend |
| **Plugin hooks** ✅ | Extensible, community contributions | Complexity |
| Config-only | No code needed | Limited power |

### Rationale
1. **Extensibility**: Users can add custom templates without forking
2. **Separation**: Core stays stable, experiments go in plugins
3. **Community**: Lower barrier to contribution

### Tradeoff Accepted
Plugin API must be stable (breaking changes hurt users). Currently minimal implementation.

---

## 📊 Summary Matrix

| Decision | Priority | Tradeoff |
|----------|----------|----------|
| CLI-First | Speed, Automation | Less visual |
| Modular Rules | Maintainability | More files |
| No Database | Simplicity | No queries |
| English-Only | Universality | Language barrier |
| External venv | AI Performance | Non-standard |
| Plugin System | Extensibility | API stability |

---

*These decisions are not permanent. If requirements change significantly, we revisit.*

