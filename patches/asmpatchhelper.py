from io import BytesIO
from sslib.fs_helpers import read_u32


class NsoOffsets:
    def __init__(
        self, text_offset: int, rodata_offset: int, data_offset: int, size: int
    ):
        self._text_offset = text_offset
        self._rodata_offset = rodata_offset
        self._data_offset = data_offset
        self._total_size = size

    def get_text_offset(self) -> int:
        return self._text_offset

    def get_rodata_offset(self) -> int:
        return self._rodata_offset

    def get_data_offset(self) -> int:
        return self._data_offset


class SegmentHeader:
    SEGMENT_HEADER_SIZE = 0x10

    def __init__(
        self, file_offset: int, memory_offset: int, decompressed_size: int, other: int
    ):
        self._file_offset = file_offset
        self._memory_offset = memory_offset
        self._decompressed_size = decompressed_size
        self._other = other

    def get_file_offset(self) -> int:
        return self._file_offset

    def get_memory_offset(self) -> int:
        return self._memory_offset

    def get_decompressed_size(self) -> int:
        return self._decompressed_size

    def get_other(self) -> int:
        return self._other

    @classmethod
    def bytes_to_segment_header(cls, data: bytes):
        if len(data) != SegmentHeader.SEGMENT_HEADER_SIZE:
            raise ValueError(
                f"Provided data is the wrong size. Expected {SegmentHeader.SEGMENT_HEADER_SIZE} bytes but found {len(data)}."
            )

        segment_header = SegmentHeader(
            *list(
                read_u32(BytesIO(data), byte_offset, is_little_endian=True)
                for byte_offset in range(0, SegmentHeader.SEGMENT_HEADER_SIZE, 4)
            )
        )

        return segment_header
