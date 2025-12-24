# Auto-update PROJECT_STATUS.md and CURRENT_CONTEXT_MAP.md for AI Toolkit
# This script should be run after any changes to the AI Toolkit codebase

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

Write-Host "📊 Auto-updating project documentation..." -ForegroundColor Cyan

# Update PROJECT_STATUS.md
if (Test-Path "src/utils/status_generator.py") {
    Write-Host "  → Updating PROJECT_STATUS.md..." -ForegroundColor Yellow
    python -m src.cli status . --skip-tests 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ PROJECT_STATUS.md updated" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Failed to update PROJECT_STATUS.md" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  status_generator.py not found" -ForegroundColor Yellow
}

# Update CURRENT_CONTEXT_MAP.md
if (Test-Path "generate_map.py") {
    Write-Host "  → Updating CURRENT_CONTEXT_MAP.md..." -ForegroundColor Yellow
    python generate_map.py 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ CURRENT_CONTEXT_MAP.md updated" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Failed to update CURRENT_CONTEXT_MAP.md" -ForegroundColor Yellow
    }
} elseif (Test-Path "src/utils/context_map.py") {
    Write-Host "  → Updating CURRENT_CONTEXT_MAP.md (via module)..." -ForegroundColor Yellow
    python -c "from src.utils.context_map import write_context_map; from pathlib import Path; write_context_map(Path('.'), 'CURRENT_CONTEXT_MAP.md')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ CURRENT_CONTEXT_MAP.md updated" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Failed to update CURRENT_CONTEXT_MAP.md" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  Context map generator not found" -ForegroundColor Yellow
}

Write-Host "✅ Documentation auto-update complete" -ForegroundColor Green



