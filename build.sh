#!/bin/sh
# Install and package with the same Python; never use a global PyInstaller.
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_DIR"

if [ ! -x .venv/bin/python ]; then
    "${PYTHON:-python3}" -m venv .venv
fi
BUILD_PYTHON="$PROJECT_DIR/.venv/bin/python"
"$BUILD_PYTHON" -c 'import sys; print(sys.executable); print(sys.version); sys.exit(0 if sys.version_info >= (3, 10) else 1)'
"$BUILD_PYTHON" -m pip install -r requirements-build.txt
"$BUILD_PYTHON" -m pip check
"$BUILD_PYTHON" -c 'import arcade, pyglet, PIL, pymunk, pytiled_parser; print("Build dependencies import successfully")'
"$BUILD_PYTHON" -m PyInstaller --clean --noconfirm --workpath build/verified d44.spec
printf 'Built: %s/dist/d44\n' "$PROJECT_DIR"
