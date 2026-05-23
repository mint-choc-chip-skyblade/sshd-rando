from pathlib import Path
from subprocess import call
import sys
import tempfile

EXE = ".exe"

temp_dir = tempfile.TemporaryDirectory()

# Get devkitpro paths.
objdump = "aarch64-none-elf-objdump"

if sys.platform == "win32":
    devkitpro = Path("C:/") / "devkitpro"
    objdump += EXE
else:
    devkitpro = Path(os.environ.get("DEVKITPRO"))

devkitA64 = devkitpro / "devkitA64" / "bin"

devkitA64_objdump = devkitA64 / objdump

DEVKIT_DIR_NOT_FOUND_HELP = "Please visit https://devkitpro.org/wiki/devkitPro_pacman for installation instructions."
DEVKIT_FILE_NOT_FOUND_HELP = "On Windows, devkitA64 should be installed to: C:\\devkitPro\\devkitA64. On other operating systems, the DEVKITA64 environment variable should be declared."

if not devkitpro.is_dir():
    raise FileNotFoundError(
        f"Failed to find devkitpro at {devkitpro}. {DEVKIT_DIR_NOT_FOUND_HELP}"
    )

if not devkitA64.is_dir():
    raise FileNotFoundError(
        f"Failed to find devkitA64 at {devkitA64}. {DEVKIT_DIR_NOT_FOUND_HELP}"
    )

if not devkitA64_objdump.is_file():
    raise Exception(
        f"Failed to find devkitA64 assembler at {devkitA64_objdump}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )


def disassemble():
    binary_file_name = (
        Path(".")
        / "additions"
        / "rust-additions"
        / "target"
        / "aarch64-unknown-none"
        / "release"
        / "librust_additions.a"
    )
    asm_file_name = Path(".") / "disassemble"
    asm_file_name.mkdir(exist_ok=True)
    asm_file_name = asm_file_name / "rust-additions.asm"

    objdump_command = [
        devkitA64_objdump,
        "-Dr",
        binary_file_name,
        asm_file_name,
    ]

    with open(asm_file_name, "w") as f:
        call(objdump_command, stdout=f)


disassemble()
