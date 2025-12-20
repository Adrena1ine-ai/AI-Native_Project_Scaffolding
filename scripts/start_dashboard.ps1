# ═══════════════════════════════════════════════════════════
# 🌐 AI Toolkit — Start Web Dashboard (Windows)
# ═══════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot\..

Write-Host "🌐 Starting AI Toolkit Dashboard..." -ForegroundColor Cyan
Write-Host ""

# Check dependencies
try {
    python -c "import fastapi, uvicorn, jinja2" 2>$null
} catch {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install fastapi uvicorn jinja2
}

# Start server
python -m web.app

