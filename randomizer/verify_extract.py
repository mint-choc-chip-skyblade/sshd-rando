import hashlib
from constants.verificationconstants import *
from filepathconstants import EXEFS_EXTRACT_PATH, ROMFS_EXTRACT_PATH, SSHD_EXTRACT_PATH
from gui.dialogs.dialog_header import (
    print_progress_text,
    print_verify_text,
    update_verify_value,
)


class SSHDExtractError(RuntimeError):
    pass


def verify_extract(verify_all_files: bool = False):
    print_progress_text("Verifying game extract")
    print_verify_text("Verifying game extract")

    # Verify top level stuff
    if not SSHD_EXTRACT_PATH.is_dir():
        raise SSHDExtractError(
            f"Extract path is not a directory: {SSHD_EXTRACT_PATH}. Could not verify extract."
        )

    extract_dirs = tuple(dirs.name for dirs in SSHD_EXTRACT_PATH.iterdir())

    if "exefs" not in extract_dirs or not EXEFS_EXTRACT_PATH.is_dir():
        raise SSHDExtractError(
            f"Folder 'exefs' not found in extract. Could not verify extract."
        )

    if "romfs" not in extract_dirs or not ROMFS_EXTRACT_PATH.is_dir():
        raise SSHDExtractError(
            f"Folder 'romfs' not found in extract. Could not verify extract."
        )

    # Verify important files
    important_file_hashs = IMPORTANT_FILE_HASHS

    if verify_all_files:
        print_progress_text("Verifying all extract files")
        print_verify_text("Verifying all extract files")
        important_file_hashs = ALL_FILE_HASHES

    files_checked = []
    all_files = tuple(SSHD_EXTRACT_PATH.rglob("*"))
    all_files_count = len(all_files)

    for file_index, filepath in enumerate(all_files):
        update_verify_value(int((file_index / all_files_count) * 100))

        if filepath.is_file():
            short_name = filepath.as_posix().split("sshd_extract/")[-1]
            print_verify_text(f"Verifying {short_name}")

            if short_name in important_file_hashs:
                files_checked.append(short_name)

                with open(filepath, "rb") as f:
                    hash = hashlib.sha256(f.read()).hexdigest()

                if hash != important_file_hashs[short_name]:
                    if (
                        short_name in BASE_VER_FILE_HASHES
                        and hash == BASE_VER_FILE_HASHES[short_name]
                    ):
                        raise SSHDExtractError(f"""
'{short_name}' is from the 1.0.0 version of the game.
Ensure your extract is from the 1.0.1 version of the game.
Could not verify extract.
                        """)

                    raise SSHDExtractError(f"""
Data in file '{short_name}' is incorrect.
Expected sha256 hash of '{important_file_hashs[short_name]}' but got '{hash}'.
Could not verify extract.
                    """)

            print_verify_text(f"Verified {short_name}")

    print_verify_text(f"Verifying all files exist")

    for short_name in important_file_hashs:
        if short_name not in files_checked:
            raise SSHDExtractError(
                f"File '{short_name}' is missing. Could not verify extract."
            )

    update_verify_value(100)
