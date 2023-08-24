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
    textOffset=0x08004000,
    rodataOffset=0x09061000,
    dataOffset=0x09563000,
    size=0x09842000 - 0x08004000,
)

# Start of next subsdk - start of subsdk1.
subsdk1Size = 0x360A5000 - 0x359FF000

# Offsets defined as the equivalent subsdk1 offset plus its size.
SUBSDK_NSO_OFFSETS = NsoOffsets(
    textOffset=0x359FF000 + subsdk1Size,
    rodataOffset=0x35D49000 + subsdk1Size,
    dataOffset=0x35F59000 + subsdk1Size,
    size=subsdk1Size,
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
        textHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))
        rodataHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))
        dataHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))

        return textHeader, rodataHeader, dataHeader

    def patch_asm(
        self, nsoPath: Path, asmDiffsPath: Path, outputPath: Path, offsets: NsoOffsets
    ):
        # Get asm patch diffs.
        asmPatchDiffPaths = tuple(asmDiffsPath.glob("*-diff.yaml"))

        # Get segment headers.
        nso = BytesIO(nsoPath.read_bytes())
        textHeader, rodataHeader, dataHeader = self.get_segments(nso)

        nso.seek(textHeader.get_file_offset())
        compressedText = nso.read(
            rodataHeader.get_file_offset() - textHeader.get_file_offset()
        )
        compressedRodata = nso.read(
            dataHeader.get_file_offset() - rodataHeader.get_file_offset()
        )
        compressedData = nso.read()

        # Decompress them.
        textSegment = BytesIO(
            self.decompress(compressedText, textHeader.get_decompressed_size())
        )
        rodataSegment = BytesIO(
            self.decompress(compressedRodata, rodataHeader.get_decompressed_size())
        )
        dataSegment = BytesIO(
            self.decompress(compressedData, dataHeader.get_decompressed_size())
        )

        for diffFilename in asmPatchDiffPaths:
            binaryDiffs = yaml_load(diffFilename)

            # Write patch data for each segment.
            for relativeOffset, data in binaryDiffs.items():
                if relativeOffset < offsets.get_rodata_offset():
                    fileOffset = relativeOffset - offsets.get_text_offset()
                    write_bytes(textSegment, fileOffset, bytes(data))
                elif relativeOffset < offsets.get_data_offset():
                    fileOffset = relativeOffset - offsets.get_rodata_offset()
                    write_bytes(rodataSegment, fileOffset, bytes(data))
                else:
                    fileOffset = relativeOffset - offsets.get_data_offset()
                    write_bytes(dataSegment, fileOffset, bytes(data))

                # print(f"data {bytes(data)}")

        newCompressedText = self.compress(textSegment.getvalue())
        newCompressedRodata = self.compress(rodataSegment.getvalue())
        newCompressedData = self.compress(dataSegment.getvalue())

        newTextSizeDiff = len(newCompressedText) - len(compressedText)
        newRodataSizeDiff = len(newCompressedRodata) - len(compressedRodata)
        newDataSizeDiff = len(newCompressedData) - len(compressedData)

        # Update NSO header.
        #
        # Each segment size can change due to the compression.
        # If the new size is smaller, don't bother updating it - there's no point.
        if newTextSizeDiff > 0:
            # Update rodata and data segment headers.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 2,
                rodataHeader.get_file_offset() + newTextSizeDiff,
                isLittleEndian=True,
            )
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                dataHeader.get_file_offset() + newTextSizeDiff,
                isLittleEndian=True,
            )

            # Update segment headers in case the rodata size is different too.
            textHeader, rodataHeader, dataHeader = self.get_segments(nso)

        if newRodataSizeDiff > 0:
            # Update data segment header.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                dataHeader.get_file_offset() + newRodataSizeDiff,
                isLittleEndian=True,
            )

        if newDataSizeDiff > 0:
            # Update .bss size.
            write_u32(
                nso,
                (SegmentHeader.SEGMENT_HEADER_SIZE * 3) + 0xC,
                dataHeader.get_other() + newDataSizeDiff,
                isLittleEndian=True,
            )

        # Update segment headers one final time before writing them.
        textHeader, rodataHeader, dataHeader = self.get_segments(nso)

        write_bytes(nso, textHeader.get_file_offset(), newCompressedText)
        write_bytes(nso, rodataHeader.get_file_offset(), newCompressedRodata)
        write_bytes(nso, dataHeader.get_file_offset(), newCompressedData)

        # Update compressed sizes (each is 4 bytes).
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET,
            len(newCompressedText),
            isLittleEndian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 4,
            len(newCompressedRodata),
            isLittleEndian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 8,
            len(newCompressedData),
            isLittleEndian=True,
        )

        # Patch nso flags to tell consoles not to check the segment hashes.
        # See https://switchbrew.org/wiki/NSO#Flags for more info.
        write_u8(nso, NSO_FLAGS_OFFSET, 0x7, isLittleEndian=True)

        write_bytes_create_dirs(outputPath, nso.getvalue())

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
