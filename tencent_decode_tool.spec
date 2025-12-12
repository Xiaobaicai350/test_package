# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import os

# 收集 openpyxl 的数据文件
openpyxl_datas = collect_data_files('openpyxl')

# 添加资源文件
resource_files = [
    ('resources/上下行命令.xlsx', 'resources'),
    ('resources/上下行命令_转码_20251212_100955.xlsx', 'resources'),
]

# 检查资源文件是否存在
datas = openpyxl_datas
for src, dst in resource_files:
    if os.path.exists(src):
        datas.append((src, dst))
    else:
        print(f"警告: 资源文件不存在: {src}")

a = Analysis(
    ['tencent_decode_tool.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'openpyxl.cell',
        'openpyxl.styles',
        'openpyxl.utils',
        'openpyxl.compat',
        'openpyxl.packaging',
        'openpyxl.xml',
        'xlrd',
        'xlwt',
        'et_xmlfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas', 'numpy', 'scipy', 'matplotlib', 'IPython', 'jupyter'],
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
    name='腾讯云转码工具',
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
)
app = BUNDLE(
    exe,
    name='腾讯云转码工具.app',
    icon=None,
    bundle_identifier=None,
)
