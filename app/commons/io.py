import pickle
from pathlib import Path
from typing import Any


def read(filepath: Path) -> Any:
    with filepath.open(mode='rb') as file:
        return pickle.load(file)


def write(content: Any, filepath: Path) -> Any:
    with filepath.open(mode='wb') as file:
        pickle.dump(content, file)
