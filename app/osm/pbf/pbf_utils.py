import zlib
from pathlib import Path

from app.osm.pbf.osm_pb2 import Blob, StringTable


def decoded_string_table(string_table: StringTable):
    result = []
    for string in string_table:
        result.append(string.decode('utf-8'))
    return result


def read_blob_data(
        filepath: Path,
        blob_position: int,
        blob_size: int
) -> bytes:
    with filepath.open(mode='rb') as file:
        file.seek(blob_position)
        blob_data = file.read(blob_size)
    blob = Blob()
    blob.ParseFromString(blob_data)
    raw_data = blob.raw
    if raw_data:
        return raw_data
    return zlib.decompress(blob.zlib_data)
