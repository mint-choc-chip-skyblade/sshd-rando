from io import BytesIO
from sslib.fs_helpers import read_u32


class NsoOffsets:
    def __init__(self, textOffset: int, rodataOffset: int, dataOffset: int, size: int):
        self._textOffset = textOffset
        self._rodataOffset = rodataOffset
        self._dataOffset = dataOffset
        self._totalSize = size

    def get_text_offset(self) -> int:
        return self._textOffset

    def get_rodata_offset(self) -> int:
        return self._rodataOffset

    def get_data_offset(self) -> int:
        return self._dataOffset


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
