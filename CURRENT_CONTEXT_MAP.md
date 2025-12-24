# 🗺️ PROJECT CONTEXT MAP
> Auto-generated structure. AI: Read this file to understand where code is located.

- `.gitignore`

- `CHANGELOG.md`

- `CLAUDE.md`

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

- `first manifesto.md`

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

- `web/__init__.py`

- `web/app.py`
  📦 CreateProjectRequest
  📦 CleanupRequest
  📦 ProjectPath
  📦 ApplyManifestoRequest
    ƒ get_lang_from_request
    ƒ get_template_context
    ƒ detect_ides_in_project
    ƒ create_app
    ƒ set_lang
    ƒ welcome_page
    ƒ home
    ƒ create_page
    ƒ cleanup_page
    ƒ health_page
    ƒ settings_page
    ƒ help_page
    ƒ existing_page
    ƒ api_create_project
    ƒ api_analyze
    ƒ api_detect_ides
    ƒ api_apply_manifesto
    ƒ api_get_manifesto
    ƒ api_cleanup
    ƒ api_health
    ƒ api_migrate
    ƒ api_update
    ƒ api_set_ide
    ƒ api_stats
    ƒ run_server

- `web/i18n.py`
    ƒ get_translations

- `web/templates/base.html`

- `web/templates/cleanup.html`

- `web/templates/create.html`

- `web/templates/existing.html`

- `web/templates/health.html`

- `web/templates/help.html`

- `web/templates/index.html`

- `web/templates/settings.html`

- `web/templates/welcome.html`

- `web/static/.gitkeep`

- `gui/__init__.py`

- `gui/app.py`
  📦 AIToolkitApp
    ƒ __init__
    ƒ setup_styles
    ƒ create_ui
    ƒ create_create_tab
    ƒ create_cleanup_tab
    ƒ create_health_tab
    ƒ create_settings_tab
    ƒ browse_path
    ƒ browse_folder
    ƒ do_create_project
    ƒ create
    ƒ do_analyze
    ƒ do_cleanup
    ƒ do_health_check
    ƒ save_settings
    ƒ run
    ƒ run_gui

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

- `docs/CURSOR_INTEGRATION.md`

- `docs/DOCTOR_COMMAND.md`

- `docs/FAQ.md`

- `docs/FUTURE_IMPROVEMENTS.md`

- `docs/GUIDE.md`

- `docs/QUICK_START.md`

- `docs/TOKEN_CALCULATION.md`

- `docs/manifesto.md`

- `.pytest_cache/.gitignore`

- `.pytest_cache/CACHEDIR.TAG`

- `.pytest_cache/README.md`

- `.pytest_cache/v/cache/lastfailed`

- `.pytest_cache/v/cache/nodeids`

- `.pytest_cache/v/cache/stepwise`

- `tests/__init__.py`

- `tests/conftest.py`

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

- `tests/test_doctor.py`
    ƒ temp_project
    ƒ project_with_venv
    ƒ project_with_pycache
  📦 TestDoctorDiagnosis
    ƒ test_empty_project_has_suggestions
    ƒ test_detects_venv_inside
    ƒ test_detects_pycache
    ƒ test_detects_missing_cursorignore
    ƒ test_detects_missing_ai_include
    ƒ test_detects_log_files
    ƒ test_healthy_project_no_critical
  📦 TestDoctorFixes
    ƒ test_fix_pycache
    ƒ test_fix_missing_cursorignore
    ƒ test_fix_missing_ai_include
    ƒ test_fix_missing_bootstrap
    ƒ test_fix_log_files
    ƒ test_fix_venv_inside
  📦 TestDoctorBackup
    ƒ test_creates_backup
    ƒ test_backup_excludes_venv
  📦 TestDoctorReport
    ƒ test_report_properties
    ƒ test_token_estimation

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
  📦 TestDocker
    ƒ test_dockerfile_created
    ƒ test_docker_compose_created
    ƒ test_dockerignore_created
  📦 TestCICD
    ƒ test_ci_workflow_created
    ƒ test_cd_workflow_created
    ƒ test_pre_commit_created
    ƒ test_dependabot_created
  📦 TestProjectFiles
    ƒ test_requirements_created
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

- `tests/test_status.py`
    ƒ temp_project
    ƒ cmd_test
    ƒ cmd_another
  📦 TestScanCommands
    ƒ test_scan_commands_finds_cmd_functions
    ƒ test_scan_commands_extracts_docstrings
    ƒ test_scan_commands_empty_dir
    ƒ test_scan_commands_ignores_private_files
    ƒ cmd_hidden
  📦 TestScanUtilities
    ƒ test_scan_utilities_finds_modules
    ƒ test_scan_utilities_extracts_docstrings
  📦 TestScanGenerators
    ƒ test_scan_generators_finds_modules
  📦 TestGetVersion
    ƒ test_get_version_from_constants
    ƒ test_get_version_fallback
  📦 TestCheckFileExists
    ƒ test_check_existing_file
    ƒ test_check_missing_file
    ƒ test_check_nested_file
  📦 TestGenerateStatusMd
    ƒ test_generate_status_md_contains_header
    ƒ test_generate_status_md_lists_commands
    ƒ test_generate_status_md_lists_utilities
    ƒ test_generate_status_md_shows_version
    ƒ test_generate_status_md_skip_tests
  📦 TestUpdateStatus
    ƒ test_update_status_creates_file
    ƒ test_update_status_writes_content
    ƒ test_update_status_overwrites_existing

- `tests/test_update.py`
  📦 TestUpdateProject
    ƒ test_update_changes_version
    ƒ test_update_same_version_skips
    ƒ test_update_refreshes_scripts

- `scripts/auto_update_docs.ps1`

- `scripts/auto_update_docs.sh`

- `scripts/build.sh`

- `scripts/publish.sh`

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

- `src/py.typed`

- `src/types.py`
  📦 TemplateConfig
  📦 IDEConfig
  📦 CleanupLevelConfig
  📦 ProjectContext
  📦 IssueDict
  📦 HealthCheckResult
  📦 GeneratorFunc
    ƒ __call__
  📦 CommandFunc
    ƒ __call__

- `src/locales/__init__.py`

- `src/locales/en.py`

- `src/utils/__init__.py`

- `src/utils/cleaner.py`
  📦 ArchiveResult
    ƒ formatted_size
    ƒ matches_pattern
    ƒ get_file_size
    ƒ archive_artifacts
    ƒ _generate_archive_report

- `src/utils/context_map.py`
  📦 FunctionInfo
  📦 ClassInfo
  📦 ModuleInfo
    ƒ extract_docstring
    ƒ extract_function_info
    ƒ extract_class_info
    ƒ parse_python_file
    ƒ format_function
    ƒ format_class
    ƒ generate_map
    ƒ write_context_map

- `src/utils/metrics.py`
  📦 ScanResult
    ƒ formatted_tokens
    ƒ formatted_size
    ƒ parse_cursorignore
    ƒ should_ignore
    ƒ scan_project

- `src/utils/status_generator.py`
    ƒ scan_commands
    ƒ scan_utilities
    ƒ scan_generators
    ƒ run_tests
    ƒ check_file_exists
    ƒ get_version
    ƒ parse_technical_spec
    ƒ check_manifesto_compliance
    ƒ generate_status_md
    ƒ update_status

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
    ƒ get_language
    ƒ set_language
    ƒ is_first_run

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

- `src/core/i18n.py`
    ƒ t

- `src/core/manifesto.py`
  📦 ManifestoRules
    ƒ load_manifesto
    ƒ extract_code_block
    ƒ parse_manifesto
    ƒ get_manifesto_rules
    ƒ get_cursorignore_content
    ƒ get_gitignore_content
    ƒ get_bootstrap_script
    ƒ apply_manifesto_to_project

- `src/core/template_loader.py`
    ƒ load_template
    ƒ render_template
    ƒ replacer
    ƒ copy_template_file
    ƒ list_templates
    ƒ get_template_info

- `src/commands/__init__.py`

- `src/commands/architect.py`
    ƒ setup_logger
    ƒ create_config_paths
    ƒ get_path
    ƒ restructure_project
    ƒ fix_launch_scripts
    ƒ update_cursor_ignore
    ƒ run

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

- `src/commands/doctor.py`
    ƒ is_protected_file
  📦 Severity
  📦 Issue
  📦 FileTokens
  📦 ChangeRecord
  📦 DiagnosticReport
    ƒ critical_count
    ƒ warning_count
    ƒ suggestion_count
    ƒ high_token_files
  📦 Doctor
    ƒ __init__
    ƒ _next_issue_id
    ƒ _count_tokens
    ƒ _get_dir_size
    ƒ _format_size
    ƒ _format_tokens
    ƒ diagnose
    ƒ create_backup
    ƒ should_exclude
    ƒ fix_venv_inside
    ƒ fix_pycache
    ƒ fix_logs
    ƒ fix_log_files
    ƒ fix_node_modules
    ƒ fix_large_files
    ƒ fix_artifacts
    ƒ fix_large_docs
    ƒ fix_missing_ai_include
    ƒ fix_missing_cursorignore
    ƒ fix_missing_bootstrap
    ƒ fix_create_venv
    ƒ fix_issue
    ƒ fix_all
    ƒ _create_config_paths_fallback
    ƒ get_path
    ƒ _update_project_docs
    ƒ print_report
    ƒ print_token_breakdown
    ƒ print_detailed_changes
    ƒ print_result
    ƒ run_doctor
    ƒ cmd_doctor
    ƒ run_doctor_interactive
  📦 Args

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

- `src/commands/pack.py`
    ƒ pack_context
    ƒ cmd_pack

- `src/commands/review.py`
  📦 SecretFinding
    ƒ calculate_entropy
    ƒ is_placeholder
    ƒ check_secrets
    ƒ run_fox_scan
    ƒ get_git_diff
    ƒ get_context_map
    ƒ get_cursor_rules
    ƒ build_review_prompt
    ƒ review_changes
    ƒ _print_prompt
    ƒ cmd_review

- `src/commands/status.py`
    ƒ cmd_status
    ƒ run_status_interactive
  📦 Args

- `src/commands/trace.py`
  📦 ImportInfo
  📦 TracedFile
    ƒ extract_imports
    ƒ is_stdlib_or_thirdparty
    ƒ resolve_import_path
    ƒ trace_dependencies
    ƒ trace_file
    ƒ generate_trace_xml
    ƒ trace_file_dependencies
    ƒ cmd_trace

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

- `.cursor/rules/auto_update.md`

- `.cursor/rules/project.md`

---
**Stats:** Scanned 131 files. Map size: ~3847 tokens.