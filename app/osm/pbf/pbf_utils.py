import zlib
from app.osm.pbf.osm_pb2 import Blob


def decoded_string_table(string_table):
    result = []
    for s in string_table:
        result.append(s.decode('utf-8'))
    return result


def read_blob_data(filename, blob_pos, blob_size):
    with open(filename, 'rb') as f:
        f.seek(blob_pos)
        blob_data = f.read(blob_size)

    blob = Blob()
    blob.ParseFromString(blob_data)
    raw_data = blob.raw
    if raw_data:
        return raw_data
    return zlib.decompress(blob.zlib_data)
