$PROJ = Split-Path -Leaf (Get-Location)
$VENV_DIR = "..\_venvs\$PROJ-main"

if (-not (Test-Path $VENV_DIR)) {
  Write-Host "Create venv: $VENV_DIR"
  python -m venv $VENV_DIR
}

& "$VENV_DIR\Scripts\python.exe" -m pip install -U pip wheel

if (Test-Path .\requirements.txt) {
  & "$VENV_DIR\Scripts\pip.exe" install -r requirements.txt
} else {
  Write-Host "No requirements.txt found. Create it (pip freeze > requirements.txt) in the currently working env."
}

Write-Host "Activate: $VENV_DIR\Scripts\Activate.ps1"

