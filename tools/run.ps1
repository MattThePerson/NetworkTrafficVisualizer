$currentPrincipal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator. Right-click PowerShell and select 'Run as administrator'."
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Error ".venv not found, please run tools\install.ps1 first"
    exit 1
}

.venv\Scripts\python.exe main.py @args
