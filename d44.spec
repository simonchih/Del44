# -*- mode: python ; coding: utf-8 -*-
from importlib.util import find_spec
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

root = Path(SPECPATH)
for package in ('arcade', 'pyglet', 'PIL', 'pymunk', 'pytiled_parser'):
    if find_spec(package) is None:
        raise RuntimeError(
            f'Missing build dependency: {package}. '
            'Run build.sh (macOS/Linux) or build.cmd (Windows) first.'
        )

# Arcade loads fonts, shaders and other package resources at runtime.
arcade_datas, arcade_binaries, arcade_imports = collect_all('arcade')

a = Analysis(
    [str(root / 'd44.py')],
    pathex=[str(root)],
    binaries=arcade_binaries,
    datas=[(str(root / 'images'), 'images'), (str(root / 'sounds'), 'sounds')] + arcade_datas,
    hiddenimports=arcade_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
# Arcade 3.3.3's hook incorrectly treats the VERSION file as a destination
# directory. collect_all already supplies the correct arcade/VERSION file.
# Drop the conflicting nested entry before creating the one-file archive.
a.datas = [entry for entry in a.datas if entry[0] != 'arcade/VERSION/VERSION']
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='d44',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
