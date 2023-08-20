import os
from pathlib import Path
import struct
from subprocess import call
import sys
import tempfile
import yaml


# Causes the assembler to print out each instruction it's assembling and it's binary.
DEBUG_SHOW_ASSEMBLY = True

# Yes, these are duplicated in filepathconstants.py
# This file should NEVER be run as part of the main randomization process.
# This file should ONLY be run after development changes to asm.
ASM_PATCHES_PATH = Path("./") / "patches"
ASM_PATCHES_DIFFS_PATH = ASM_PATCHES_PATH / "diffs"

EXE = ".exe"
SEMICOLON = ";"
NEWLINE = "\n"
OFFSET = ".offset"
SPACE = " "

# Change how yaml dumps lists so each element isn't on a separate line.
yaml.CDumper.add_representer(
    list,
    lambda dumper, data: dumper.represent_sequence(
        "tag:yaml.org,2002:seq", data, flow_style=True
    ),
)

# Output integers as hexadecimal.
yaml.CDumper.add_representer(
    int,
    lambda dumper, data: yaml.ScalarNode("tag:yaml.org,2002:int", f"0x{data:02X}"),
)

# Output strings (the offsets) as hexadecimal.
yaml.CDumper.add_representer(
    str,
    lambda dumper, data: yaml.ScalarNode(
        "tag:yaml.org,2002:int", f"0x{int(data, 16):08X}"
    ),
)

tempDir = tempfile.TemporaryDirectory()

# Get devkitpro paths.
assembler = "aarch64-none-elf-as"
linker = "aarch64-none-elf-ld"
objcopy = "aarch64-none-elf-objcopy"

if sys.platform == "win32":
    devkitpro = Path("C:/") / "devkitpro"
    assembler += EXE
    linker += EXE
    objcopy += EXE
else:
    devkitpro = Path(os.environ.get("DEVKITPRO"))

devkitA64 = devkitpro / "devkitA64" / "bin"

devkitA64Assembler = devkitA64 / assembler
devkitA64Linker = devkitA64 / linker
devkitA64Objcopy = devkitA64 / objcopy

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

if not devkitA64Assembler.is_file():
    raise Exception(
        f"Failed to find devkitA64 assembler at {devkitA64Assembler}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )

if not devkitA64Linker.is_file():
    raise Exception(
        f"Failed to find devkitA64 linker at {devkitA64Linker}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )

if not devkitA64Objcopy.is_file():
    raise Exception(
        f"Failed to find devkitA64 linker at {devkitA64Linker}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )


with open("original-symbols.yaml", "r") as f:
    originalSymbols = yaml.safe_load(f)

with open("linker.ld", "r") as f:
    linkerScript = f.read()

for symbol, address in originalSymbols["main"].items():
    assert symbol is not None
    assert address is not None

    linkerScript += f"{symbol} = 0x{address:x}" + SEMICOLON + NEWLINE


# Get patches from each asm file.
asmPatchesPaths = tuple(ASM_PATCHES_PATH.glob("*.asm"))

# Keeps the temporary directory only within this with block.
with tempDir as tempDirName:
    tempDirName = Path(tempDirName)

    for patchFilePath in asmPatchesPaths:
        print(f"patchFilePath = {patchFilePath}")
        patchFilename = patchFilePath.parts[-1]
        codeBlocks = {}
        localBranches = []
        asmReadOffset = None

        with open(patchFilePath, "r") as f:
            asmPatch = f.read()

        tempLinkerScript = linkerScript + NEWLINE

        for line in asmPatch.splitlines():
            line = line.strip()

            if len(line) == 0 or line.startswith(SEMICOLON):
                continue

            line = line.split(SEMICOLON)[0] + NEWLINE

            if line.startswith(OFFSET):
                asmReadOffset = hex(int(line.split(SPACE)[-1], 16))

                if asmReadOffset not in codeBlocks:
                    codeBlocks[asmReadOffset] = []
                else:
                    raise Exception(
                        f"Duplicate offset {asmReadOffset} section in {patchFilePath}."
                    )
            elif line.startswith("b"):
                branch, destination = line.split(SPACE)
                destination = int(destination, 16)

                tempBranchLabel = f"branch_label_0x{destination:x}"
                localBranches.append(
                    tempBranchLabel + f" = 0x{destination:x}" + SEMICOLON + NEWLINE
                )

                codeBlocks[asmReadOffset].append(branch + SPACE + tempBranchLabel + NEWLINE)
            else:
                codeBlocks[asmReadOffset].append(line)

            for symbol in localBranches:
                tempLinkerScript += symbol

        for codeBlockOffset, code in codeBlocks.items():
            tempLinkerFilename = tempDirName / "temp-linker.ld"

            with open(tempLinkerFilename, "w") as f:
                f.write(tempLinkerScript)

            assemblerCodeFilename = (
                tempDirName / f"{patchFilename}-0x{codeBlockOffset}.asm"
            )
            # assemblerCodeFilename.mkdir(parents=True, exist_ok=True)

            with open(assemblerCodeFilename, "w") as f:
                for instruction in code:
                    f.write(instruction)

            outputFilename = tempDirName / f"{patchFilename}-0x{codeBlockOffset}.o"

            # Assemble code block.
            assemblerCommand = [
                devkitA64Assembler,
                "-mcpu=cortex-a57",
                "-EL",  # little endian
                assemblerCodeFilename,
                "-o",
                outputFilename,
            ]

            if DEBUG_SHOW_ASSEMBLY:
                assemblerCommand += [
                    "-al",
                ]  # output asm instructions assembled

            if result := call(assemblerCommand):
                raise Exception(f"Assembler call failed with error code: {result}")

            # Apply linker.
            elfFilename = tempDirName / f"{patchFilename}-0x{codeBlockOffset}.elf"

            mapFilename = tempDirName / f"{patchFilename}.map"

            linkerCommand = [
                devkitA64Linker,
                "-EL",  # little endian
                "-Ttext",
                codeBlockOffset,
                "-T",
                tempLinkerFilename,
                f"-Map={mapFilename}",
                outputFilename,
                "-o",
                elfFilename,
            ]

            if result := call(linkerCommand):
                raise Exception(
                    f"Linker call {linkerCommand} failed with error code: {result}"
                )

            # Convert to binary.
            binaryFilename = tempDirName / f"{patchFilename}-0x{codeBlockOffset}.bin"

            objcopyCommand = [
                devkitA64Objcopy,
                "--output-target",
                "binary",
                elfFilename,
                binaryFilename,
            ]

            if result := call(objcopyCommand):
                raise Exception(
                    f"Objcopy call {objcopyCommand} failed with error code: {result}"
                )

            with open(binaryFilename, "rb") as f:
                binaryData = f.read()

            dataBytes = list(struct.unpack("B" * len(binaryData), binaryData))

            codeBlocks[codeBlockOffset] = dataBytes

        diffFilename = ASM_PATCHES_DIFFS_PATH / f"{patchFilename[:-4]}-diff.yaml"

        with open(diffFilename, "w") as f:
            f.write(yaml.dump(codeBlocks, Dumper=yaml.CDumper, line_break=NEWLINE))
