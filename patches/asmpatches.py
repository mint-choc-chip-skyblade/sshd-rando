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

TEXT_START_ADDRESS = 0x08004000
RODATA_START_ADDRESS = 0x09061000
DATA_START_ADDRESS = 0x09563000


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

    def getSegments(self, nso):
        size = SegmentHeader.SEGMENT_HEADER_SIZE
        nso.seek(size)  # Start of .text SegmentHeader
        textHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))
        rodataHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))
        dataHeader = SegmentHeader.bytes_to_segment_header(nso.read(size))

        return textHeader, rodataHeader, dataHeader

    def do_asm_patches(self):
        # Get asm patch diffs.
        asmPatchDiffPaths = tuple(ASM_PATCHES_DIFFS_PATH.glob("*-diff.yaml"))

        # Get segment headers.
        mainNSO = BytesIO(MAIN_NSO_FILE_PATH.read_bytes())
        textHeader, rodataHeader, dataHeader = self.getSegments(mainNSO)

        mainNSO.seek(textHeader.get_file_offset())
        compressedText = mainNSO.read(
            rodataHeader.get_file_offset() - textHeader.get_file_offset()
        )
        compressedRodata = mainNSO.read(
            dataHeader.get_file_offset() - rodataHeader.get_file_offset()
        )
        compressedData = mainNSO.read()

        textSegment = BytesIO(
            self.decompress(compressedText, textHeader.get_decompressed_size())
        )
        rodataSegment = BytesIO(
            self.decompress(compressedRodata, rodataHeader.get_decompressed_size())
        )
        dataSegment = BytesIO(
            self.decompress(compressedData, dataHeader.get_decompressed_size())
        )

        # allSegments = BytesIO(textSegment + rodataSegment + dataSegment)
        # assert len(allSegments) == len(textSegment) + len(rodataSegment) + len(dataSegment)

        for diffFilename in asmPatchDiffPaths:
            binaryDiffs = yaml_load(diffFilename)

            for relativeOffset, data in binaryDiffs.items():
                if relativeOffset < RODATA_START_ADDRESS:
                    fileOffset = relativeOffset - TEXT_START_ADDRESS
                    write_bytes(textSegment, fileOffset, bytes(data))
                elif relativeOffset < DATA_START_ADDRESS:
                    fileOffset = relativeOffset - RODATA_START_ADDRESS
                    write_bytes(rodataSegment, fileOffset, bytes(data))
                else:
                    fileOffset = relativeOffset - DATA_START_ADDRESS
                    write_bytes(dataSegment, fileOffset, bytes(data))

                print(f"data {bytes(data)}")

        newCompressedText = self.compress(textSegment.getvalue())
        newCompressedRodata = self.compress(rodataSegment.getvalue())
        newCompressedData = self.compress(dataSegment.getvalue())

        newTextSizeDiff = len(newCompressedText) - len(compressedText)
        newRodataSizeDiff = len(newCompressedRodata) - len(compressedRodata)
        newDataSizeDiff = len(newCompressedData) - len(compressedData)

        # Update segment size from compression shifting.
        # If new size is smaller, don't bother updating it - there's no point.
        if newTextSizeDiff > 0:
            # Update rodata and data segment headers.
            write_u32(
                mainNSO,
                SegmentHeader.SEGMENT_HEADER_SIZE * 2,
                rodataHeader.get_file_offset() + newTextSizeDiff,
                isLittleEndian=True,
            )
            write_u32(
                mainNSO,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                dataHeader.get_file_offset() + newTextSizeDiff,
                isLittleEndian=True,
            )

            # Update segment headers.
            textHeader, rodataHeader, dataHeader = self.getSegments(mainNSO)

        if newRodataSizeDiff > 0:
            print("rodiff")
            # Update data segment header.
            write_u32(
                mainNSO,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                dataHeader.get_file_offset() + newRodataSizeDiff,
                isLittleEndian=True,
            )

        if newDataSizeDiff > 0:
            print("data diff")
            # Update .bss size.
            write_u32(
                mainNSO,
                (SegmentHeader.SEGMENT_HEADER_SIZE * 3) + 0xC,
                dataHeader.get_other() + newDataSizeDiff,
                isLittleEndian=True,
            )

        # Update segment headers.
        textHeader, rodataHeader, dataHeader = self.getSegments(mainNSO)

        write_bytes(mainNSO, textHeader.get_file_offset(), newCompressedText)
        write_bytes(mainNSO, rodataHeader.get_file_offset(), newCompressedRodata)
        write_bytes(mainNSO, dataHeader.get_file_offset(), newCompressedData)

        # Update compressed sizes.
        compressedSizeOffset = 0x60
        write_u32(
            mainNSO, compressedSizeOffset, len(newCompressedText), isLittleEndian=True
        )
        write_u32(
            mainNSO,
            compressedSizeOffset + 4,
            len(newCompressedRodata),
            isLittleEndian=True,
        )
        write_u32(
            mainNSO,
            compressedSizeOffset + 8,
            len(newCompressedData),
            isLittleEndian=True,
        )

        write_bytes_create_dirs(OUTPUT_MAIN_NSO, mainNSO.getvalue())
