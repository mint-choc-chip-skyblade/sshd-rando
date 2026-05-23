import os
from pathlib import Path
import re
import struct
from subprocess import call
import sys
import tempfile
import yaml

# Causes the assembler to print out each instruction it's assembling and it's binary.
DEBUG_SHOW_ASSEMBLY = False

# Yes, these are duplicated in filepathconstants.py
# This file should NEVER be run as part of the main randomization process.
# This file should ONLY be run after development changes to asm.
ASM_PATCHES_PATH = Path("./") / "patches"
ASM_PATCHES_DIFFS_PATH = ASM_PATCHES_PATH / "diffs"
ASM_ADDITIONS_PATH = Path("./") / "additions"
ASM_ADDITIONS_DIFFS_PATH = ASM_ADDITIONS_PATH / "diffs"
ASM_SDK_PATH = Path("./") / "sdk"
ASM_SDK_DIFFS_PATH = ASM_SDK_PATH / "diffs"

ASM_RUST_ADDITIONS_TARGET_PATH = (
    ASM_ADDITIONS_PATH
    / "rust-additions"
    / "target"
    / "aarch64-unknown-none"
    / "release"
    / "librust_additions.a"
)
ASM_RUST_ADDITIONS_PATH = ASM_ADDITIONS_PATH / "rust-additions.asm"
ASM_ADDITIONS_LANDINGPAD_PATH = ASM_ADDITIONS_PATH / "additions-landingpad.asm"

ASM_PATCHES_JUMPTABLE_PATH = ASM_PATCHES_PATH / "jumptable.asm"


EXE = ".exe"
COLON = ":"
SEMICOLON = ";"
NEWLINE = "\n"
OFFSET = ".offset"
OFFSET_PREFIX = "0x"
SPACE = " "
ONLYIF = "; onlyif "

# Change how yaml dumps lists so each element isn't on a separate line.
yaml.CDumper.add_representer(
    list,
    lambda dumper, data: dumper.represent_sequence(
        "tag:yaml.org,2002:seq", data, flow_style=True
    ),
)


# Helper to determine if data is a hex number or not
def is_hex(data: str) -> bool:
    data = data.lower()

    if data.startswith(OFFSET_PREFIX):
        data = data[2:]

    for char in data:
        if char not in "0123456789abcdef":
            return False

    return True


# Output integers as hexadecimal.
yaml.CDumper.add_representer(
    int,
    lambda dumper, data: yaml.ScalarNode("tag:yaml.org,2002:int", f"0x{data:02X}"),
)

# Output strings (the offsets) as hexadecimal.
yaml.CDumper.add_representer(
    str,
    lambda dumper, data: yaml.ScalarNode(
        "tag:yaml.org,2002:int" if is_hex(data) else "tag:yaml.org,2002:str",
        f"0x{int(data, 16):08X}" if is_hex(data) else data,
    ),
)

temp_dir = tempfile.TemporaryDirectory()

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
    # devkitpro = Path("/opt") / "devkitpro"

devkitA64 = devkitpro / "devkitA64" / "bin"

devkitA64_assembler = devkitA64 / assembler
devkitA64_linker = devkitA64 / linker
devkitA64_objcopy = devkitA64 / objcopy

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

if not devkitA64_assembler.is_file():
    raise Exception(
        f"Failed to find devkitA64 assembler at {devkitA64_assembler}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )

if not devkitA64_linker.is_file():
    raise Exception(
        f"Failed to find devkitA64 linker at {devkitA64_linker}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )

if not devkitA64_objcopy.is_file():
    raise Exception(
        f"Failed to find devkitA64 objcopy at {devkitA64_objcopy}. {DEVKIT_FILE_NOT_FOUND_HELP}"
    )


with open("symbols.yaml", "r", encoding="utf-8") as f:
    defined_symbols = yaml.safe_load(f)

with open("linker.ld", "r", encoding="utf-8") as f:
    linker_script = f.read()

linker_script += NEWLINE

for symbol, address in defined_symbols["main"].items():
    assert symbol is not None
    assert address is not None

    linker_script += f"{symbol} = 0x{address:x}" + SEMICOLON + NEWLINE

custom_symbols = {}


def assemble(temp_dir_name: Path, asmPaths: list[Path], outputPath: Path):
    addresses_overwritten = {}

    for asm_file_path in asmPaths:
        print(f"Assembling: {asm_file_path}")
        asm_file_name = asm_file_path.parts[-1]
        code_blocks = {}
        local_branches = []
        asm_read_offset = None
        current_only_if = ""

        temp_linker_script = linker_script + NEWLINE

        for symbol in custom_symbols:
            temp_linker_script += (
                symbol + " = " + hex(custom_symbols[symbol]) + SEMICOLON + NEWLINE
            )

        with open(asm_file_path, "r", encoding="utf-8") as f:
            asm_block = f.read()

        for line in asm_block.splitlines():
            line = line.strip()

            if line.startswith(ONLYIF):
                current_only_if = line.replace(ONLYIF, "")

            # Reset the current_only_if whenever a blank line is encountered
            if len(line) == 0:
                current_only_if = ""
                continue
            elif line.startswith(SEMICOLON):
                continue

            line = line.split(SEMICOLON)[0].strip()

            if line.startswith(OFFSET):
                asm_read_offset = current_only_if + hex(int(line.split(SPACE)[-1], 16))

                if asm_read_offset not in code_blocks:
                    code_blocks[asm_read_offset] = []
                else:
                    raise Exception(
                        f"Duplicate offset {asm_read_offset} section in {asm_file_path}."
                    )
            elif line.startswith(
                ("bl ", "b ", "b.", "bcc ", "cbz", "cbnz", "tbz", "tbnz")
            ):  # The blank space is necessary
                instruction_parts = line.split(SPACE)
                destination = instruction_parts[-1]

                if destination.startswith("0x"):
                    destination = int(destination, 16)
                    temp_branch_label = f"branch_label_0x{destination:x}"
                    new_local_branch = (
                        temp_branch_label
                        + f" = 0x{destination:x}"
                        + SEMICOLON
                        + NEWLINE
                    )

                    if new_local_branch not in local_branches:
                        local_branches.append(new_local_branch)

                    code_blocks[asm_read_offset].append(
                        SPACE.join(instruction_parts[:-1])
                        + SPACE
                        + temp_branch_label
                        + NEWLINE
                    )
                else:
                    code_blocks[asm_read_offset].append(line + NEWLINE)
            else:
                code_blocks[asm_read_offset].append(line + NEWLINE)

        for symbol in local_branches:
            temp_linker_script += symbol

        for code_block_identifier, code in code_blocks.items():
            if code_block_identifier.startswith(OFFSET_PREFIX):
                code_block_offset = code_block_identifier
            else:
                code_block_offset = (
                    OFFSET_PREFIX + code_block_identifier.split(OFFSET_PREFIX)[-1]
                )

            temp_linker_file_name = temp_dir_name / "temp-linker.ld"

            with open(temp_linker_file_name, "w", encoding="utf-8") as f:
                f.write(temp_linker_script)

            assembler_code_file_name = (
                temp_dir_name / f"{asm_file_name}-0x{code_block_offset}.asm"
            )

            with open(assembler_code_file_name, "w", encoding="utf-8") as f:
                for instruction in code:
                    f.write(instruction)

            assembled_file_name = (
                temp_dir_name / f"{asm_file_name}-0x{code_block_offset}.o"
            )

            # Assemble code block.
            assembler_command = [
                devkitA64_assembler,
                "-mcpu=cortex-a57",
                "-EL",  # little endian
                assembler_code_file_name,
                "-o",
                assembled_file_name,
            ]

            if DEBUG_SHOW_ASSEMBLY:
                assembler_command += [
                    "-al",
                ]  # output asm instructions assembled

            if result := call(assembler_command):
                raise Exception(f"Assembler call failed with error code: {result}")

            # Apply linker.
            elf_file_name = temp_dir_name / f"{asm_file_name}-0x{code_block_offset}.elf"

            map_file_name = temp_dir_name / f"{asm_file_name}.map"

            linker_command = [
                devkitA64_linker,
                "-EL",  # little endian
                "-Ttext",
                code_block_offset,
                "-T",
                temp_linker_file_name,
                f"-Map={map_file_name}",
                assembled_file_name,
                "-o",
                elf_file_name,
            ]

            if asm_file_path == ASM_RUST_ADDITIONS_PATH:
                linker_command.append("./" + ASM_RUST_ADDITIONS_TARGET_PATH.as_posix())

            # with open(temp_linker_file_name, "r", encoding="utf-8") as f:
            #     with open("./linker_file.txt", "w") as linker_f:
            #         linker_f.write(f.read())

            if result := call(linker_command):
                raise Exception(
                    f"Linker call {linker_command} failed with error code: {result}"
                )

            if asm_file_path == ASM_RUST_ADDITIONS_PATH:
                # Keep track of custom symbols so they can be passed in the linker script to future assembler calls.
                with open(map_file_name, encoding="utf-8") as f:
                    on_custom_symbols = False

                    for line in f.read().splitlines():
                        if line.startswith(" .text          "):
                            on_custom_symbols = True
                            continue

                        if on_custom_symbols:
                            if not line:
                                break

                            match = re.search(
                                r" +0x000000(?:0000000000)?([0-9a-f]{10}) +([a-zA-Z]\S+)",
                                line,
                            )

                            if not match:
                                continue

                            symbol_address = int(match.group(1), 16)
                            symbol_name = match.group(2)

                            # Rust sometimes outputs symbols with generics which the linker can't deal with.
                            # Not currently an issue but becomes one when updating the rust nightly channel.
                            # TODO: find a better way to deal with this.
                            # if "<" not in symbol_name:
                            custom_symbols[symbol_name] = symbol_address

            # Convert to binary.
            binary_file_name = (
                temp_dir_name / f"{asm_file_name}-0x{code_block_offset}.bin"
            )

            objcopy_command = [
                devkitA64_objcopy,
                "--output-target",
                "binary",
                # "-j",
                # ".text, .rodata",
                elf_file_name,
                binary_file_name,
            ]

            if result := call(objcopy_command):
                raise Exception(
                    f"Objcopy call {objcopy_command} failed with error code: {result}"
                )

            with open(binary_file_name, "rb") as f:
                binary_data = f.read()

            data_bytes = list(struct.unpack("B" * len(binary_data), binary_data))

            code_blocks[code_block_identifier] = data_bytes

        # Ensure there are no overlapping asm changes.
        for offset in code_blocks:
            # Can't check for overlapping condtional patches.
            if not offset.startswith(OFFSET_PREFIX):
                continue

            for byte_number in range(len(code_blocks[offset])):
                true_offset = int(offset, 16) + byte_number

                if true_offset in addresses_overwritten:
                    raise Exception(
                        f"Overlapping asm patch found at {offset} in file {asm_file_name}. {addresses_overwritten[true_offset]} is already using that address"
                    )
                else:
                    addresses_overwritten[true_offset] = asm_file_name

        diff_file_name = outputPath / f"{asm_file_name[:-4]}-diff.yaml"

        # Create a new dict that has all code patches under their respective only_ifs
        diff_dict = {}

        for offset, code_block in code_blocks.items():
            offset = str(offset)

            if offset.startswith(OFFSET_PREFIX):
                diff_dict[offset] = code_block
            else:
                # This is a bit contrived but it makes python happy :p
                only_if = offset.split(OFFSET_PREFIX)[0]
                offset = offset.split(only_if)[-1]

                if only_if not in diff_dict:
                    diff_dict[only_if] = {}

                diff_dict[only_if][offset] = code_block

        with open(diff_file_name, "w", encoding="utf-8", newline="") as f:
            f.write(yaml.dump(diff_dict, Dumper=yaml.CDumper, line_break=NEWLINE))


# Get patches from each asm file.
asm_additions_paths = list(ASM_ADDITIONS_PATH.rglob("*.asm"))
asm_patches_paths = list(ASM_PATCHES_PATH.rglob("*.asm"))
asm_sdk_paths = list(ASM_SDK_PATH.rglob("*.asm"))

# Keeps the temporary directory only within this with block.
with temp_dir as temp_dir_name:
    temp_dir_name = Path(temp_dir_name)

    # Format rust additions.
    print("Formatting rust code")
    if rust_build_command := call(
        [
            "cargo",
            "fmt",
        ],
        cwd="./additions/rust-additions",
    ):
        raise Exception("Formatting rust additions failed.")

    # Lint rust additions.
    print("Linting rust code")
    if rust_build_command := call(
        [
            "cargo",
            "clippy",
        ],
        cwd="./additions/rust-additions",
    ):
        raise Exception("Linting rust additions failed.")

    # Assemble rust additions.
    print("Building rust code")
    if rust_build_command := call(
        ["cargo", "build", "--release", "--target=aarch64-unknown-none"],
        cwd="./additions/rust-additions",
    ):
        raise Exception("Building rust additions failed.")

    # Ensure rust additions are assembled first.
    asm_additions_paths.remove(ASM_RUST_ADDITIONS_PATH)
    asm_additions_paths.remove(ASM_ADDITIONS_LANDINGPAD_PATH)
    asm_additions_paths = [
        ASM_RUST_ADDITIONS_PATH,
        ASM_ADDITIONS_LANDINGPAD_PATH,
    ] + asm_additions_paths

    assemble(temp_dir_name, asm_additions_paths, ASM_ADDITIONS_DIFFS_PATH)

    # Ensure patches jumptable is assembled first.
    asm_patches_paths.remove(ASM_PATCHES_JUMPTABLE_PATH)
    asm_patches_paths = [ASM_PATCHES_JUMPTABLE_PATH] + asm_patches_paths

    assemble(temp_dir_name, asm_patches_paths, ASM_PATCHES_DIFFS_PATH)

    # Assemble sdk stuff
    assemble(temp_dir_name, asm_sdk_paths, ASM_SDK_DIFFS_PATH)
