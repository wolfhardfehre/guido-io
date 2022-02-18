from pathlib import Path

from app.osm.pbf.osm_pb2 import HeaderBlock
from app.osm.pbf.pbf_utils import read_blob_data


class PbfHeader:
    def __init__(
            self,
            filepath: Path,
            blob_position: int,
            blob_size: int
    ):
        data = read_blob_data(
            filepath=filepath,
            blob_position=blob_position,
            blob_size=blob_size
        )
        self.header_block = HeaderBlock()
        self.header_block.ParseFromString(data)

    def required_features(self) -> set:
        return set(self.header_block.required_features)
