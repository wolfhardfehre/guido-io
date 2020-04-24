from app.osm.pbf.osm_pb2 import HeaderBlock
from app.osm.pbf.utils import read_blob_data


class PbfHeader:
    def __init__(self, filename, blob_pos, blob_size):
        data = read_blob_data(filename, blob_pos, blob_size)
        self.header_block = HeaderBlock()
        self.header_block.ParseFromString(data)

    def required_features(self):
        return set(self.header_block.required_features)
