#!/usr/bin/python3

from pathlib import Path
import platform
import shutil

from constants.randoconstants import VERSION

base_name = f"Skyward Sword HD Randomizer {VERSION}"

exe_ext = ""

if platform.system() == "Windows":
    exe_ext = ".exe"
    platform_name = "windows"
if platform.system() == "Darwin":
    exe_ext = ".app"
    platform_name = "macos"
if platform.system() == "Linux":
    platform_name = "linux"

exe_path = Path("dist") / (base_name + exe_ext)

if not exe_path.is_file() and not exe_path.is_dir():
    raise Exception(f"Executable not found: {exe_path}")

# Give non-windows builds execute permissions
if platform.system() != "Windows":
    exe_path.chmod(0o755)

release_archive_path = Path("dist") / f"release_archive_{VERSION}_{platform_name}"
print(f"Writing build to path: {release_archive_path}")

if release_archive_path.exists() and release_archive_path.is_dir():
    shutil.rmtree(release_archive_path)

release_archive_path.mkdir(exist_ok=True)
shutil.copyfile("README.md", release_archive_path / "README.txt")

shutil.copytree(
    Path("plandomizers") / "examples",
    release_archive_path / "plandomizers" / "examples",
)
shutil.copyfile(
    Path("plandomizers") / "vanilla_boko_base.yaml",
    release_archive_path / "plandomizers" / "vanilla_boko_base.yaml",
)

(release_archive_path / "presets").mkdir(exist_ok=True)
shutil.copyfile(
    Path("presets") / "README.md", release_archive_path / "presets" / "README.txt"
)

(release_archive_path / "sshd_extract").mkdir(exist_ok=True)
shutil.copyfile(
    Path("sshd_extract") / "README.md",
    release_archive_path / "sshd_extract" / "README.txt",
)

if platform.system() == "Linux":
    base_name.replace(".", "_")

shutil.move(exe_path, release_archive_path / (base_name + exe_ext))
