# run-windows.ps1 - run this project natively on Windows, straight from its
# folder in Ubuntu (one copy of the code; you keep editing and committing in
# Ubuntu). Use it only for things that must run on Windows, such as reading
# another Windows program's memory or using Windows-only libraries.
#
# From Ubuntu (easiest):   ./scripts/run-windows.sh status
# From PowerShell:         powershell -ExecutionPolicy Bypass -File \\wsl.localhost\<distro>\home\<you>\code\magnum-fultopus\scripts\run-windows.ps1 status
#
# Needs uv on Windows (installed by dotfiles\windows\setup-local-ai.ps1).
# The Windows Python environment lives in %LOCALAPPDATA%\uv-projects\<name>,
# separate from Ubuntu's .venv, so the two never clash.

$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $PSScriptRoot
$name = Split-Path -Leaf $project

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv isn't installed on Windows. Run dotfiles\windows\setup-local-ai.ps1 first." -ForegroundColor Yellow
    exit 1
}

$env:UV_PROJECT_ENVIRONMENT = Join-Path $env:LOCALAPPDATA "uv-projects\$name"
Set-Location $project
# --frozen: use uv.lock exactly as committed; never rewrite files in Ubuntu from Windows
uv run --frozen app @args
exit $LASTEXITCODE
