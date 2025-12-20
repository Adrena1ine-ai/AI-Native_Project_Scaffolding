<# 
.SYNOPSIS
    AI-Native Project Scaffolding — Quick Start Script (Windows)
.DESCRIPTION
    Installs dependencies and starts the Dashboard with one command
.EXAMPLE
    .\start.ps1
    .\start.ps1 -Port 3000
#>

param(
    [int]$Port = 8080,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

# Colors
function Write-Color($Text, $Color = "White") {
    Write-Host $Text -ForegroundColor $Color
}

# Header
Write-Host ""
Write-Color "╔══════════════════════════════════════════════════════════╗" Cyan
Write-Color "║  🛠️  AI-Native Project Scaffolding                       ║" Cyan
Write-Color "║  Quick Start Script for Windows                          ║" Cyan
Write-Color "╚══════════════════════════════════════════════════════════╝" Cyan
Write-Host ""

# Check Python
Write-Color "🔍 Checking Python..." Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Color "   ✅ $pythonVersion" Green
} catch {
    Write-Color "   ❌ Python not found! Please install Python 3.10+" Red
    Write-Color "   Download: https://www.python.org/downloads/" Yellow
    exit 1
}

# Check Python version
$versionMatch = [regex]::Match($pythonVersion, "Python (\d+)\.(\d+)")
if ($versionMatch.Success) {
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
        Write-Color "   ❌ Python 3.10+ required, found $major.$minor" Red
        exit 1
    }
}

# Install dependencies
Write-Color "📦 Installing dependencies..." Yellow
try {
    pip install -q pyyaml fastapi uvicorn jinja2 python-multipart 2>&1 | Out-Null
    Write-Color "   ✅ Dependencies installed" Green
} catch {
    Write-Color "   ⚠️  Some dependencies may need manual installation" Yellow
}

# Check if port is available
$portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Color "   ⚠️  Port $Port is in use, trying $($Port + 1)..." Yellow
    $Port = $Port + 1
}

# Start Dashboard
Write-Host ""
Write-Color "🚀 Starting Dashboard on http://127.0.0.1:$Port ..." Green
Write-Host ""

# Open browser
if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:$Port"
}

# Run
try {
    python -m web.app --port $Port --no-browser
} catch {
    Write-Color "❌ Failed to start. Try: python -m web.app" Red
    exit 1
}

