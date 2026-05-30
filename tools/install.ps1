$useUv = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)

if ($useUv) {
    Write-Host "uv available"
} else {
    Write-Host "uv NOT available"
}

if (Test-Path ".venv") {
    Write-Host ".venv exists"
    exit 0
}

Write-Host "Creating virtual environment..."
if ($useUv) {
    uv venv .venv
} else {
    python -m venv .venv
}

Write-Host "Installing dependencies..."
if ($useUv) {
    uv pip install --python .venv\Scripts\python.exe -r requirements.txt
} else {
    .venv\Scripts\pip.exe install -r requirements.txt
}
