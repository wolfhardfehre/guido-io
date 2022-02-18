import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional

from app.osm.pbf.blob_meta import BlobMeta
from app.osm.pbf.osm_pb2 import BlobHeader


@dataclass
class PbfFile:
    filepath: Path

    def blobs(self) -> Generator[BlobMeta, None, None]:
        next_blob_position = 0
        with self.filepath.open('rb') as file:
            while True:
                file.seek(next_blob_position)
                blob_header_size = self._blob_header_size(file)
                if not blob_header_size:
                    break
                blob_size = self._blob_size(file.read(blob_header_size))
                blob_position = next_blob_position + 4 + blob_header_size
                next_blob_position = blob_position + blob_size
                yield BlobMeta(
                    position=blob_position,
                    size=blob_size,
                    filepath=self.filepath
                )

    @staticmethod
    def _blob_size(data: bytes) -> int:
        blob_header = BlobHeader()
        blob_header.ParseFromString(data)
        return blob_header.datasize

    @staticmethod
    def _blob_header_size(file) -> Optional[int]:
        header_length_bytes = file.read(4)
        if header_length_bytes:
            return struct.unpack('!i', header_length_bytes)[0]
        return None
