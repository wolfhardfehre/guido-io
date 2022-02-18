import pickle
import zlib
from pathlib import Path
from typing import Any

from app.osm.pbf.osm_pb2 import Blob


def read(filepath: Path) -> Any:
    with filepath.open(mode='rb') as file:
        return pickle.load(file)


def write(content: Any, filepath: Path) -> Any:
    with filepath.open(mode='wb') as file:
        pickle.dump(content, file)


def read_blob(filepath: Path, blob_position: int, blob_size: int) -> bytes:
    with filepath.open(mode='rb') as file:
        file.seek(blob_position)
        blob_data = file.read(blob_size)
    blob = Blob()
    blob.ParseFromString(blob_data)
    raw_data = blob.raw
    if raw_data:
        return raw_data
    return zlib.decompress(blob.zlib_data)
