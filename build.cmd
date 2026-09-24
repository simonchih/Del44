@echo off
setlocal
pushd "%~dp0"
if errorlevel 1 exit /b 1

set "BUILD_PYTHON=%~dp0.venv\Scripts\python.exe"
if not exist "%BUILD_PYTHON%" (
    echo Create .venv with Python 3.10 or newer first: py -3.13 -m venv .venv
    goto :failed
)

"%BUILD_PYTHON%" -c "import sys; print(sys.executable); print(sys.version); sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo The build requires Python 3.10 or newer.
    goto :failed
)

"%BUILD_PYTHON%" -m pip install -r requirements-build.txt
if errorlevel 1 (
    echo Could not install the build dependencies.
    goto :failed
)

rem Always use the project environment, never a global PyInstaller.
"%BUILD_PYTHON%" -m PyInstaller --noconfirm --workpath build/verified d44.spec
if errorlevel 1 (
    echo PyInstaller failed.
    goto :failed
)

echo Built: %~dp0dist\d44.exe
popd
exit /b 0

:failed
popd
exit /b 1
