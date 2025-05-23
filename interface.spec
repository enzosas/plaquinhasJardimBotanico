# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
    datas=[('placa-fundo.pdf', '.'), ('placa-fundo-1.pdf', '.'), ('placa-fundo-2.pdf', '.'), ('open-sans.bold.ttf', '.'), ('open-sans.italic.ttf', '.'), ('open-sans.regular.ttf', '.'), ('icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='interface',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
