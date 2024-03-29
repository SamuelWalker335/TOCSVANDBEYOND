# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/swalker_/Desktop/python_projects/pdf_to_csv/test.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Python312/Lib/tkinter', 'tkinter/'), ('C:/Python312/Lib/site-packages/tabula', 'tabula/'), ('C:/Python312/Lib/site-packages/tabula_py-2.9.0.dist-info', 'tabula_py-2.9.0.dist-info/'), ('C:/Python312/Lib/site-packages/tabula-1.0.5.dist-info', 'tabula-1.0.5.dist-info/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='test',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='test',
)
