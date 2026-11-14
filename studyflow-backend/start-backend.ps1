$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$backendPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $backendPython)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment.' }
    & $backendPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not install backend dependencies.' }
}
& $backendPython bootstrap.py
if ($LASTEXITCODE -ne 0) { throw 'Could not prepare local settings.' }
& $backendPython manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Database migration failed.' }
& $backendPython manage.py runserver 127.0.0.1:8000
