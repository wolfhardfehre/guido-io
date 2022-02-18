import os
import struct
from pathlib import Path
from typing import Generator, Optional

from app.osm.pbf.osm_pb2 import BlobHeader
from app.osm.pbf.pbf_header import PbfHeader

SUPPORTED_FEATURES = {'OsmSchema-V0.6', 'DenseNodes'}


class PbfFile:
    def __init__(self, filepath: Path):
        self._filepath = filepath
        self._file = filepath.open('rb')
        self._file.seek(0, os.SEEK_END)
        self._file.seek(0, 0)
        self._next_blob_position = self.prev_blob_position = 0
        header_offsets = next(self.blobs())
        header = PbfHeader(
            filepath=self._filepath,
            blob_position=header_offsets['blob_position'],
            blob_size=header_offsets['blob_size']
        )
        self._check_features(header)

    def blobs(self) -> Generator[dict, None, None]:
        while True:
            self._file.seek(self._next_blob_position)
            blob_header_size = self._blob_header_size()
            if not blob_header_size:
                break
            blob_size = self._blob_size(self._file.read(blob_header_size))
            blob_position = self._next_blob_position + 4 + blob_header_size
            self.prev_blob_position = self._next_blob_position
            self._next_blob_position = blob_position + blob_size
            yield dict(
                blob_position=blob_position,
                blob_size=blob_size,
                file_name=self._filepath
            )

    def _check_features(self, header: PbfHeader) -> None:
        missing_features = header.required_features.difference(SUPPORTED_FEATURES)
        if missing_features:
            missing_features_str = ", ".join(missing_features)
            message = f'{self._filepath} requires features not implemented by this parser: {missing_features_str}'
            raise NotImplementedError(message)

    @staticmethod
    def _blob_size(data: bytes) -> int:
        blob_header = BlobHeader()
        blob_header.ParseFromString(data)
        return blob_header.datasize

    def _blob_header_size(self) -> Optional[int]:
        header_length_bytes = self._file.read(4)
        if header_length_bytes:
            return struct.unpack('!i', header_length_bytes)[0]
        return None
