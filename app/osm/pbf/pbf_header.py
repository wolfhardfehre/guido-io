from dataclasses import dataclass
from pathlib import Path

from app.osm.pbf.osm_pb2 import HeaderBlock
from app.commons.io import read_blob


@dataclass
class PbfHeader:
    filepath: Path
    blob_position: int
    blob_size: int

    @property
    def required_features(self) -> set:
        data = read_blob(
            filepath=self.filepath,
            blob_position=self.blob_position,
            blob_size=self.blob_size
        )
        header_block = HeaderBlock()
        header_block.ParseFromString(data)
        return set(header_block.required_features)
