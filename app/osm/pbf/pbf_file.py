import struct

from app.osm.pbf.osm_pb2 import BlobHeader
from app.osm.pbf.pbf_header import PbfHeader
from app.osm.pbf.pbf_primitive_block import PdfPrimitiveBlock

SUPPORTED_FEATURES = {'OsmSchema-V0.6', 'DenseNodes'}


class PbfFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'rb')
        self.next_blob_position = self.prev_blob_position = 0
        header_offsets = self._skip_header()
        header = PbfHeader(self.file_name, header_offsets['blob_position'], header_offsets['blob_size'])
        self._check_features(header)

    def primitive_blocks(self):
        for pos in self.blobs():
            yield PdfPrimitiveBlock(self.file_name, pos['blob_position'], pos['blob_size'])

    def blobs(self):
        while True:
            self.file.seek(self.next_blob_position)
            blob_header_size = self._blob_header_size()
            if not blob_header_size:
                break
            blob_size = self._blob_size(self.file.read(blob_header_size))
            blob_position = self.next_blob_position + 4 + blob_header_size
            self.prev_blob_position = self.next_blob_position
            self.next_blob_position = blob_position + blob_size
            yield dict(
                blob_position=blob_position,
                blob_size=blob_size,
                file_name=self.file_name
            )

    def _check_features(self, header):
        missing_features = header.required_features().difference(SUPPORTED_FEATURES)
        if missing_features:
            missing_features_str = ", ".join(missing_features)
            message = f'{self.file_name} requires features not implemented by this parser: {missing_features_str}'
            raise NotImplementedError(message)

    def _skip_header(self):
        return next(self.blobs())

    @staticmethod
    def _blob_size(data):
        blob_header = BlobHeader()
        blob_header.ParseFromString(data)
        return blob_header.datasize

    def _blob_header_size(self):
        header_length_bytes = self.file.read(4)
        if header_length_bytes:
            return struct.unpack('!i', header_length_bytes)[0]
        return None
