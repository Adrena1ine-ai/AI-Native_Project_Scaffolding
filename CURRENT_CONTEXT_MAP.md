# 🗺️ PROJECT CONTEXT MAP
> Auto-generated structure. AI: Read this file to understand where code is located.

- `.cursorignore`

- `.cursorrules`

- `.gitignore`

- `CHANGELOG.md`

- `CLAUDE.md`

- `CLEANUP_REPORT.md`

- `CONTRIBUTING.md`

- `LICENSE`

- `MANIFEST.in`

- `PROJECT_STATUS.md`

- `PROMPTS_LIBRARY.md`

- `README.md`

- `SECURITY.md`

- `TECHNICAL_SPECIFICATION.md`

- `TRADEOFFS.md`

- `__main__.py`

- `benchmark.py`
  📦 ScanResult
    ƒ estimated_cost
    ƒ estimate_tokens
    ƒ parse_cursorignore
    ƒ should_ignore
    ƒ scan_directory
    ƒ format_number
    ƒ format_tokens
    ƒ print_results_rich
    ƒ print_results_plain
    ƒ run_benchmark
    ƒ main

- `first manifesto.md`

- `main.py`

- `pyproject.toml`

- `requirements.txt`

- `start.ps1`

- `start.sh`

- `toolkit.yaml`

- `.github/FUNDING.yml`

- `.github/PULL_REQUEST_TEMPLATE.md`

- `.github/ISSUE_TEMPLATE/bug_report.md`

- `.github/ISSUE_TEMPLATE/feature_request.md`

- `.github/ISSUE_TEMPLATE/question.md`

- `AI-Native Project Scaffolding/CONTEXT SWITCHER.py`
    ƒ update
    ƒ create_file
    ƒ run

- `AI-Native Project Scaffolding/START.py`
    ƒ main

- `AI-Native Project Scaffolding/builder.py`
    ƒ update_cursorignore
    ƒ show_status
    ƒ create_file
    ƒ create_project
    ƒ main
  📦 Settings
  📦 Config
    ƒ main
    ƒ run

- `AI-Native Project Scaffolding/manifesto.md`

- `templates/parser/scraper.py.template`

- `templates/webapp/app.js.template`

- `templates/webapp/index.html.template`

- `templates/webapp/styles.css.template`

- `templates/bot/main.py.template`

- `templates/bot/handlers/__init__.py.template`

- `templates/bot/handlers/start.py.template`

- `templates/common/config.py.template`

- `templates/common/database.py.template`

- `templates/fastapi/main.py.template`

- `_AI_INCLUDE/PROJECT_CONVENTIONS.md`

- `_AI_INCLUDE/WHERE_IS_WHAT.md`

- `_AI_INCLUDE/WHERE_THINGS_LIVE.md`

- `docs/FAQ.md`

- `docs/FUTURE_IMPROVEMENTS.md`

- `docs/GUIDE.md`

- `docs/QUICK_START.md`

- `docs/manifesto.md`

- `.pytest_cache/.gitignore`

- `.pytest_cache/CACHEDIR.TAG`

- `.pytest_cache/README.md`

- `.pytest_cache/v/cache/lastfailed`

- `.pytest_cache/v/cache/nodeids`

- `.pytest_cache/v/cache/stepwise`

- `tests/__init__.py`

- `tests/conftest.py`
    ƒ temp_dir
    ƒ temp_project
    ƒ temp_project_with_venv
    ƒ clean_project

- `tests/test_cleanup.py`
  📦 TestAnalyzeProject
    ƒ test_detect_venv_inside_project
    ƒ test_detect_missing_configs
    ƒ test_detect_pycache
    ƒ test_detect_large_logs
    ƒ test_clean_project_no_issues
  📦 TestCleanupProject
    ƒ test_safe_level_no_changes
    ƒ test_medium_level_moves_venv
    ƒ test_cleanup_removes_pycache
  📦 TestIssueClass
    ƒ test_issue_str_with_size
    ƒ test_issue_str_without_size
    ƒ test_issue_icons

- `tests/test_core.py`
  📦 TestColors
    ƒ test_colorize
    ƒ test_success
    ƒ test_error
    ƒ test_warning
    ƒ test_info
  📦 TestConstants
    ƒ test_version_format
    ƒ test_templates_exist
    ƒ test_template_has_required_fields
    ƒ test_ide_configs_exist
    ƒ test_ide_config_has_required_fields
    ƒ test_cleanup_levels_exist
  📦 TestConfig
    ƒ test_set_and_get_default_ide
    ƒ test_get_default_ai_targets
  📦 TestFileUtils
    ƒ test_create_file
    ƒ test_create_file_creates_dirs
    ƒ test_create_executable
    ƒ test_get_dir_size
    ƒ test_get_dir_size_empty

- `tests/test_create.py`
  📦 TestCreateProject
    ƒ test_create_bot_project
    ƒ test_create_webapp_project
    ƒ test_create_fastapi_project
    ƒ test_create_full_project
    ƒ test_create_with_docker
    ƒ test_create_with_ci
    ƒ test_create_with_multiple_ides
    ƒ test_create_fails_if_exists
    ƒ test_create_with_invalid_name
  📦 TestProjectStructure
    ƒ test_ai_include_created
    ƒ test_scripts_created
    ƒ test_requirements_created

- `tests/test_generators.py`
  📦 TestAIConfigs
    ƒ test_common_rules_contains_project_name
    ƒ test_cursor_rules_created
    ƒ test_cursor_ignore_created
    ƒ test_copilot_instructions_created
    ƒ test_claude_md_created
    ƒ test_windsurf_rules_created
    ƒ test_ai_include_created
  📦 TestScripts
    ƒ test_bootstrap_sh_created
    ƒ test_bootstrap_ps1_created
    ƒ test_context_switcher_created
    ƒ test_health_check_created
    ƒ test_check_repo_clean_created
  📦 TestDocker
    ƒ test_dockerfile_bot
    ƒ test_dockerfile_fastapi
    ƒ test_docker_compose_created
    ƒ test_dockerignore_created
  📦 TestCICD
    ƒ test_ci_workflow_created
    ƒ test_cd_workflow_created
    ƒ test_pre_commit_config_created
    ƒ test_dependabot_created
  📦 TestProjectFiles
    ƒ test_requirements_bot
    ƒ test_requirements_fastapi
    ƒ test_requirements_parser
    ƒ test_config_py_created
    ƒ test_env_example_created
    ƒ test_readme_created
    ƒ test_gitignore_created

- `tests/test_health.py`
  📦 TestHealthCheck
    ƒ test_clean_project_passes
    ƒ test_missing_ai_include_fails
    ƒ test_venv_inside_project_fails
    ƒ test_with_ai_include_better
  📦 TestHealthCheckFiles
    ƒ test_detects_missing_env
    ƒ test_detects_missing_requirements

- `tests/test_migrate.py`
  📦 TestMigrateProject
    ƒ test_migrate_adds_ai_configs
    ƒ test_migrate_adds_scripts
    ƒ test_migrate_adds_version
    ƒ test_migrate_skips_existing
    ƒ test_migrate_adds_ci_if_requested

- `tests/test_update.py`
  📦 TestUpdateProject
    ƒ test_update_changes_version
    ƒ test_update_same_version_skips
    ƒ test_update_refreshes_scripts

- `scripts/bootstrap.ps1`

- `scripts/bootstrap.sh`

- `scripts/build.sh`

- `scripts/isolate_heavy.sh`

- `scripts/publish.sh`

- `scripts/restore_heavy.sh`

- `scripts/start_dashboard.ps1`

- `scripts/start_dashboard.sh`

- `src/__init__.py`

- `src/cli.py`
    ƒ print_header
    ƒ select_ide
    ƒ print_menu
    ƒ interactive_mode
    ƒ cli_mode
    ƒ main

- `src/utils/__init__.py`

- `src/utils/cleaner.py`
  📦 ArchiveResult
    ƒ formatted_size
    ƒ matches_pattern
    ƒ get_file_size
    ƒ archive_artifacts
    ƒ _generate_archive_report

- `src/utils/metrics.py`
  📦 ScanResult
    ƒ formatted_tokens
    ƒ formatted_size
    ƒ parse_cursorignore
    ƒ should_ignore
    ƒ scan_project

- `src/generators/__init__.py`

- `src/generators/ai_configs.py`
    ƒ get_common_rules
    ƒ generate_cursor_rules
    ƒ generate_cursor_ignore
    ƒ generate_copilot_instructions
    ƒ generate_claude_md
    ƒ generate_windsurf_rules
    ƒ generate_ai_include
    ƒ generate_ai_configs

- `src/generators/ci_cd.py`
    ƒ generate_ci_workflow
    ƒ generate_cd_workflow
    ƒ generate_dependabot
    ƒ generate_pre_commit_config
    ƒ generate_ci_files

- `src/generators/docker.py`
    ƒ generate_dockerfile
    ƒ generate_docker_compose
    ƒ generate_dockerignore
    ƒ generate_docker_files

- `src/generators/git.py`
    ƒ generate_gitignore
    ƒ generate_gitattributes
    ƒ init_git_repo

- `src/generators/project_files.py`
    ƒ generate_requirements
    ƒ generate_requirements_dev
    ƒ generate_env_example
    ƒ generate_config_py
  📦 Settings
    ƒ generate_readme
    ƒ generate_toolkit_version
    ƒ generate_pyproject_toml
    ƒ generate_project_files

- `src/generators/scripts.py`
    ƒ generate_bootstrap_sh
    ƒ generate_bootstrap_ps1
    ƒ generate_check_repo_clean
    ƒ generate_health_check
    ƒ generate_context_switcher
    ƒ get_current_mode
    ƒ update_ignore
    ƒ show_status
    ƒ main
    ƒ generate_scripts

- `src/core/__init__.py`

- `src/core/config.py`
  📦 Config
    ƒ load
    ƒ save
    ƒ get_template
    ƒ get_ide_config
    ƒ get_cleanup_level
    ƒ get_config
    ƒ set_default_ide
    ƒ get_default_ide
    ƒ get_default_ai_targets

- `src/core/constants.py`
  📦 COLORS
    ƒ colorize
    ƒ success
    ƒ error
    ƒ warning
    ƒ info

- `src/core/file_utils.py`
    ƒ create_file
    ƒ make_executable
    ƒ copy_template
    ƒ get_dir_size
    ƒ remove_dir
    ƒ copy_dir
    ƒ move_dir

- `src/commands/__init__.py`

- `src/commands/cleanup.py`
  📦 Issue
    ƒ __str__
    ƒ analyze_project
    ƒ select_cleanup_level
    ƒ create_backup
    ƒ cleanup_project
    ƒ cmd_cleanup

- `src/commands/create.py`
    ƒ select_template
    ƒ generate_bot_module
    ƒ main
    ƒ setup_handlers
    ƒ cmd_start
    ƒ cmd_help
    ƒ generate_database_module
    ƒ init_db
    ƒ get_user
    ƒ generate_api_module
    ƒ root
    ƒ health
    ƒ generate_webapp_module
    ƒ generate_parser_module
    ƒ fetch_page
    ƒ parse_html
    ƒ generate_module_files
    ƒ create_project
    ƒ cmd_create

- `src/commands/health.py`
    ƒ health_check
    ƒ cmd_health

- `src/commands/hooks.py`
    ƒ install_pre_commit_hook
    ƒ uninstall_pre_commit_hook
    ƒ check_hook_installed
    ƒ cmd_hooks

- `src/commands/migrate.py`
    ƒ migrate_project
    ƒ cmd_migrate

- `src/commands/review.py`
    ƒ get_git_diff
    ƒ get_context_map
    ƒ get_cursor_rules
    ƒ build_review_prompt
    ƒ review_changes
    ƒ cmd_review

- `src/commands/update.py`
    ƒ update_project
    ƒ cmd_update

- `src/commands/wizard.py`
    ƒ validate_project_name
    ƒ generate_spec_md
    ƒ run_rabbit_check
    ƒ generate_doctor_report
    ƒ flow_create_rich
    ƒ flow_optimize_rich
    ƒ flow_create_plain
    ƒ flow_optimize_plain
    ƒ run_wizard_rich
    ƒ run_wizard_plain
    ƒ run_wizard
    ƒ cmd_wizard

- `plugins/__init__.py`

- `plugins/manager.py`
  📦 PluginHook
  📦 HookHandler
    ƒ __call__
  📦 Plugin
    ƒ __post_init__
  📦 PluginManager
    ƒ __init__
    ƒ _get_default_plugins_dir
    ƒ discover_plugins
    ƒ load_plugin
    ƒ load_all_plugins
    ƒ register_hook
    ƒ call_hook
    ƒ get_plugin
    ƒ list_plugins
    ƒ get_all_templates
    ƒ get_all_commands
    ƒ create_plugin_skeleton
    ƒ register
    ƒ on_project_created
    ƒ get_plugin_manager

- `plugins/installed/.gitkeep`

- `.cursor/rules/project.md`

- `.cursor/rules/review_guidelines.md`

- `.cursor/rules/toolkit.md`

---
**Stats:** Scanned 105 files. Map size: ~2480 tokens.