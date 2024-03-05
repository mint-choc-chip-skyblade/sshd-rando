# -*- mode: python ; coding: utf-8 -*-

import os
import glob

from constants.randoconstants import VERSION

block_cipher = None

def build_datas_recursive(paths):
    datas = []
    
    for path in paths:
        for filename in glob.iglob(path, recursive=True):
            dest_dirname = os.path.dirname(filename)

            if dest_dirname == "":
                dest_dirname = "."
            
            data_entry = (filename, dest_dirname)
            datas.append(data_entry)
            # print(data_entry)
    
    return datas


a = Analysis(
    ["sshdrando.py"],
    pathex=[],
    binaries=[],
    datas=build_datas_recursive(
        [
            "asm/*.*",  # includes assemble.py but it shouldn't matter
            "asm/additions/diffs/*.yaml",
            "asm/patchs/diffs/*.yaml",
            "assets/**/*",
            "data/**/*",
            "gui/custom_themes/**/*",
            "plandomizers/**/*",
            "presets/**/*",
            "sshd_extract/README.md",
            "*.md",
            "LICENSE",
        ]
    ),
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [
        ("--nogui", None, "OPTION"),
    ],
    a.binaries,
    a.datas,
    name=f"Skyward Sword HD Randomizer {VERSION}",
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    # icon="assets/icon.png", # causes the exe to get flagged as a trojan :/
)

app = BUNDLE(
    exe,
    name=f"Skyward Sword HD Randomizer {VERSION}.app",
    icon="assets/icon.png",
    bundle_identifier=None,
    info_plist={
        "LSBackgroundOnly": False,
        "CFBundleDisplayName": "Skyward Sword HD Randomizer",
        "CFBundleName": "SSHD Randomizer", # 15 character maximum
        "CFBundleShortVersionString": VERSION,
    },
)
