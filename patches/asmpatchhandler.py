from filepathconstants import (
    ASM_ADDITIONS_DIFFS_PATH,
    ASM_PATCHES_DIFFS_PATH,
    MAIN_NSO_FILE_PATH,
    OUTPUT_ADDITIONAL_SUBSDK,
    OUTPUT_MAIN_NSO,
    SUBSDK1_FILE_PATH,
)
from io import BytesIO
from pathlib import Path

from lz4.block import compress, decompress

from patches.asmpatchhelper import NsoOffsets, SegmentHeader

from sslib.fs_helpers import write_bytes, write_u32, write_u8
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load

MAIN_NSO_OFFSETS = NsoOffsets(
    text_offset=0x08004000,
    rodata_offset=0x09061000,
    data_offset=0x09563000,
    size=0x09842000 - 0x08004000,
)

# Start of next subsdk - start of subsdk1.
subsdk1_size = 0x360A5000 - 0x359FF000

# Offsets defined as the equivalent subsdk1 offset plus its size.
SUBSDK_NSO_OFFSETS = NsoOffsets(
    text_offset=0x359FF000 + subsdk1_size,
    rodata_offset=0x35D49000 + subsdk1_size,
    data_offset=0x35F59000 + subsdk1_size,
    size=subsdk1_size,
)

NSO_FLAGS_OFFSET = 0xC
COMPRESSED_SEGMENT_NSO_OFFSET = 0x60


class ASMPatchHandler:
    def compress(self, data: bytes) -> bytes:
        # Uses the lz4 compression.
        return compress(data)[4:]  # trims lz4 junk off the start

    def decompress(self, data: bytes, size: int) -> bytes:
        # Uses the lz4 decompression.
        return decompress(data, size)

    def get_segments(self, nso):
        size = SegmentHeader.SEGMENT_HEADER_SIZE
        nso.seek(size)  # Start of .text SegmentHeader
        text_header = SegmentHeader.bytes_to_segment_header(nso.read(size))
        rodata_header = SegmentHeader.bytes_to_segment_header(nso.read(size))
        data_header = SegmentHeader.bytes_to_segment_header(nso.read(size))

        return text_header, rodata_header, data_header

    def patch_asm(
        self,
        nso_path: Path,
        asm_diffs_path: Path,
        output_path: Path,
        offsets: NsoOffsets,
    ):
        # Get asm patch diffs.
        asm_patch_diff_paths = tuple(asm_diffs_path.glob("*-diff.yaml"))

        # Get segment headers.
        nso = BytesIO(nso_path.read_bytes())
        text_header, rodata_header, data_header = self.get_segments(nso)

        nso.seek(text_header.get_file_offset())
        compressed_text = nso.read(
            rodata_header.get_file_offset() - text_header.get_file_offset()
        )
        compressed_rodata = nso.read(
            data_header.get_file_offset() - rodata_header.get_file_offset()
        )
        compressed_data = nso.read()

        # Decompress them.
        text_segment = BytesIO(
            self.decompress(compressed_text, text_header.get_decompressed_size())
        )
        rodata_segment = BytesIO(
            self.decompress(compressed_rodata, rodata_header.get_decompressed_size())
        )
        data_segment = BytesIO(
            self.decompress(compressed_data, data_header.get_decompressed_size())
        )

        for diff_file_name in asm_patch_diff_paths:
            binary_diffs = yaml_load(diff_file_name)

            # Write patch data for each segment.
            for relative_offset, data in binary_diffs.items():
                if relative_offset < offsets.get_rodata_offset():
                    file_offset = relative_offset - offsets.get_text_offset()
                    write_bytes(text_segment, file_offset, bytes(data))
                elif relative_offset < offsets.get_data_offset():
                    file_offset = relative_offset - offsets.get_rodata_offset()
                    write_bytes(rodata_segment, file_offset, bytes(data))
                else:
                    file_offset = relative_offset - offsets.get_data_offset()
                    write_bytes(data_segment, file_offset, bytes(data))

                # print(f"data {bytes(data)}")

        new_compressed_text = self.compress(text_segment.getvalue())
        new_compressed_rodata = self.compress(rodata_segment.getvalue())
        new_compressed_data = self.compress(data_segment.getvalue())

        new_text_size_diff = len(new_compressed_text) - len(compressed_text)
        new_rodata_size_diff = len(new_compressed_rodata) - len(compressed_rodata)
        new_data_size_diff = len(new_compressed_data) - len(compressed_data)

        # Update NSO header.
        #
        # Each segment size can change due to the compression.
        # If the new size is smaller, don't bother updating it - there's no point.
        if new_text_size_diff > 0:
            # Update rodata and data segment headers.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 2,
                rodata_header.get_file_offset() + new_text_size_diff,
                is_little_endian=True,
            )
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                data_header.get_file_offset() + new_text_size_diff,
                is_little_endian=True,
            )

            # Update segment headers in case the rodata size is different too.
            text_header, rodata_header, data_header = self.get_segments(nso)

        if new_rodata_size_diff > 0:
            # Update data segment header.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                data_header.get_file_offset() + new_rodata_size_diff,
                is_little_endian=True,
            )

        if new_data_size_diff > 0:
            # Update .bss size.
            write_u32(
                nso,
                (SegmentHeader.SEGMENT_HEADER_SIZE * 3) + 0xC,
                data_header.get_other() + new_data_size_diff,
                is_little_endian=True,
            )

        # Update segment headers one final time before writing them.
        text_header, rodata_header, data_header = self.get_segments(nso)

        write_bytes(nso, text_header.get_file_offset(), new_compressed_text)
        write_bytes(nso, rodata_header.get_file_offset(), new_compressed_rodata)
        write_bytes(nso, data_header.get_file_offset(), new_compressed_data)

        # Update compressed sizes (each is 4 bytes).
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET,
            len(new_compressed_text),
            is_little_endian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 4,
            len(new_compressed_rodata),
            is_little_endian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 8,
            len(new_compressed_data),
            is_little_endian=True,
        )

        # Patch nso flags to tell consoles not to check the segment hashes.
        # See https://switchbrew.org/wiki/NSO#Flags for more info.
        write_u8(nso, NSO_FLAGS_OFFSET, 0x7, is_little_endian=True)

        write_bytes_create_dirs(output_path, nso.getvalue())

    # Applies both asm patches and additions.
    def patch_all_asm(self):
        print("Applying asm patches")
        self.patch_asm(
            MAIN_NSO_FILE_PATH,
            ASM_PATCHES_DIFFS_PATH,
            OUTPUT_MAIN_NSO,
            MAIN_NSO_OFFSETS,
        )

        print("Applying asm additions")
        self.patch_asm(
            SUBSDK1_FILE_PATH,
            ASM_ADDITIONS_DIFFS_PATH,
            OUTPUT_ADDITIONAL_SUBSDK,
            SUBSDK_NSO_OFFSETS,
        )
