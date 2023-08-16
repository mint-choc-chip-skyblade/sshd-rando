from filepathconstants import (
    ASM_PATCHES_DIFFS_PATH,
    MAIN_NSO_FILE_PATH,
    OUTPUT_MAIN_NSO,
)
from io import BytesIO
from lz4.block import compress, decompress

from sslib.fs_helpers import read_u32, write_bytes, write_u32
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load

MAIN_GHIDRA_START_ADDRESS = 0x08004000


class SegmentHeader:
    SEGMENT_HEADER_SIZE = 0x10

    def __init__(self, fOffset: int, mOffset: int, dSize: int, o: int):
        self._fileOffset = fOffset
        self._memoryOffset = mOffset
        self._decompressedSize = dSize
        self._other = o

    def get_file_offset(self) -> int:
        return self._fileOffset

    def get_memory_offset(self) -> int:
        return self._memoryOffset

    def get_decompressed_size(self) -> int:
        return self._decompressedSize

    def get_other(self) -> int:
        return self._other

    @classmethod
    def bytes_to_segment_header(cls, data: bytes):
        if len(data) != SegmentHeader.SEGMENT_HEADER_SIZE:
            raise ValueError(
                f"Provided data is the wrong size. Expected {SegmentHeader.SEGMENT_HEADER_SIZE} bytes but found {len(data)}."
            )

        segmentHeader = SegmentHeader(
            *list(
                read_u32(BytesIO(data), byteOffset, isLittleEndian=True)
                for byteOffset in range(0, SegmentHeader.SEGMENT_HEADER_SIZE, 4)
            )
        )

        return segmentHeader


class ASMPatchHandler:
    def compress(self, data: bytes) -> bytes:
        # Uses the lz4 compression.
        return compress(data)[4:]  # trims lz4 junk off the start

    def decompress(self, data: bytes, size: int) -> bytes:
        # Uses the lz4 decompression.
        return decompress(data, size)

    def do_asm_patches(self):
        # Get asm patch diffs.
        asmPatchDiffPaths = tuple(ASM_PATCHES_DIFFS_PATH.glob("*-diff.yaml"))

        # Get segment headers.
        mainNSO = BytesIO(MAIN_NSO_FILE_PATH.read_bytes())
        size = SegmentHeader.SEGMENT_HEADER_SIZE
        mainNSO.seek(size)  # Start of .text SegmentHeader
        textHeader = SegmentHeader.bytes_to_segment_header(mainNSO.read(size))
        rodataHeader = SegmentHeader.bytes_to_segment_header(mainNSO.read(size))
        dataHeader = SegmentHeader.bytes_to_segment_header(mainNSO.read(size))

        mainNSO.seek(textHeader.get_file_offset())
        compressedText = mainNSO.read(
            rodataHeader.get_file_offset() - textHeader.get_file_offset()
        )
        compressedRodata = mainNSO.read(
            dataHeader.get_file_offset() - rodataHeader.get_file_offset()
        )
        compressedData = mainNSO.read()

        textSegment = self.decompress(
            compressedText, textHeader.get_decompressed_size()
        )
        rodataSegment = self.decompress(
            compressedRodata, rodataHeader.get_decompressed_size()
        )
        dataSegment = self.decompress(
            compressedData, dataHeader.get_decompressed_size()
        )

        allSegments = BytesIO(textSegment + rodataSegment + dataSegment)
        # assert len(allSegments) == len(textSegment) + len(rodataSegment) + len(dataSegment)

        for diffFilename in asmPatchDiffPaths:
            binaryDiffs = yaml_load(diffFilename)

            for relativeOffset, data in binaryDiffs.items():
                fileOffset = relativeOffset - MAIN_GHIDRA_START_ADDRESS

                print(f"data {bytes(data)}")

                # print(bytes(data))
                # print(allSegments.getvalue()[fileOffset:fileOffset + len(data)])

                write_bytes(allSegments, fileOffset, bytes(data))

                # print(allSegments.getvalue()[fileOffset:fileOffset + len(data)])

        textSegmentStart = 0
        rodataSegmentStart = textHeader.get_decompressed_size()
        dataSegmentStart = rodataSegmentStart + rodataHeader.get_decompressed_size()

        compressedText = self.compress(
            allSegments.getvalue()[textSegmentStart:rodataSegmentStart]
        )
        compressedRodata = self.compress(
            allSegments.getvalue()[rodataSegmentStart:dataSegmentStart]
        )
        compressedData = self.compress(allSegments.getvalue()[dataSegmentStart:])

        write_bytes(mainNSO, textHeader.get_file_offset(), compressedText)
        write_bytes(mainNSO, rodataHeader.get_file_offset(), compressedRodata)
        write_bytes(mainNSO, dataHeader.get_file_offset(), compressedData)

        write_bytes_create_dirs(OUTPUT_MAIN_NSO, mainNSO.getvalue())
