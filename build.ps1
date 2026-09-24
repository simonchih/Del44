$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $buildPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $buildPython)) {
        throw 'Create .venv with Python 3.10 or newer first: py -3.13 -m venv .venv'
    }
    & $buildPython -c 'import sys; print(sys.executable); print(sys.version); sys.exit(0 if sys.version_info >= (3, 10) else 1)'
    if ($LASTEXITCODE -ne 0) { throw 'The build requires Python 3.10 or newer.' }
    & $buildPython -m pip install -r requirements-build.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not install the build dependencies.' }
    # Never call a global PyInstaller: it may belong to an older Python.
    & $buildPython -m PyInstaller --noconfirm --workpath build/verified d44.spec
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed.' }
    Write-Host "Built: $PSScriptRoot\dist\d44.exe"
}
finally {
    Pop-Location
}
