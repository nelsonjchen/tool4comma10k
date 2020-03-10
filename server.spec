# -*- mode: python -*-
# Purely for PyCharm to use and get information.
import os
import subprocess
import sys

import gooey
from PyInstaller.building.api import EXE, PYZ, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from PyInstaller.building.osx import BUNDLE

block_cipher = None

gooey_root = os.path.dirname(gooey.__file__)
gooey_languages = Tree(os.path.join(gooey_root, 'languages'), prefix='gooey/languages')
gooey_images = Tree(os.path.join(gooey_root, 'images'), prefix='gooey/images')

name = 'Tool4Comma10k'

# Generate burned in version
with open('_version.py', 'wb') as f:
    version = subprocess.check_output(['git', 'describe', '--long']).strip()
    f.write(b"""# Burned in PyInstaller version. Ignored by Git.
software = "%s"
""" % version)

# noinspection PyUnresolvedReferences
a = Analysis(
    ['server.py'],
    pathex=[os.path.abspath(SPECPATH)],
    binaries=[],
    datas=[
            ('static', 'static'),
            ('templates', 'templates'),
            ('cargo_root', 'cargo_root'),
            ('config.json', '.'),
    ],
    hiddenimports=[
        'pkg_resources.py2_warn'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    gooey_languages,
    gooey_images,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name
)
app = BUNDLE(
    coll,
    name=f'{name}.app',
    icon=None,
    bundle_identifier=None,
    info_plist={
        'NSHighResolutionCapable': 'True'
    }
)
