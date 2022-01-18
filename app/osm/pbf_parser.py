import logging
from multiprocessing import Pool, cpu_count
import os
import re
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from tqdm import tqdm

from app.osm.pbf.pbf_file import PbfFile
from app.osm.pbf.pbf_primitive_block import PdfPrimitiveBlock
from app.paths import DATA_PATH, CACHE_PATH

NODE_COLUMNS = ['type', 'id', 'lon', 'lat']
WAY_COLUMNS = ['type', 'origin', 'destination', 'highway', 'oneway', 'max_speed', 'access']


def parse_block(blob) -> List[Tuple]:
    filename, offset, size = blob['file_name'], blob['blob_position'], blob['blob_size']
    block_parser = PdfPrimitiveBlock(filename, offset, size)
    return [e for es in block_parser.parse() for e in es]


class PbfParser:

    def __init__(self, filepath: Path, use_cache: bool = False):
        self._filepath = filepath
        self._use_cache = use_cache
        self.area_name = self._cut_out_area_name()
        self._nodes_path = CACHE_PATH / f'{self.area_name}-nodes.osm.pkl'
        self._ways_path = CACHE_PATH / f'{self.area_name}-ways.osm.pkl'
        self.nodes = None
        self.ways = None
        self.relations = None
        self._load_osm_elements()

    def _cut_out_area_name(self) -> str:
        result = re.search(f'{CACHE_PATH}/(.*)-latest', str(self._filepath))
        return result.group(1)

    def _load_osm_elements(self) -> None:
        if self._use_cache:
            self._load_from_pickle()
        if self.nodes is None or self.ways is None:
            self._parse_from_pbf()
            self._save_osm_elements()

    def _load_from_pickle(self) -> None:
        logging.debug('trying to load osm nodes and ways from pickle files')
        if os.path.isfile(self._nodes_path):
            logging.info('reading osm nodes from: %s', self._nodes_path)
            self.nodes = pd.read_pickle(self._nodes_path)
        if os.path.isfile(self._ways_path):
            logging.info('reading osm ways from: %s', self._ways_path)
            self.ways = pd.read_pickle(self._ways_path)

    def _parse_from_pbf(self) -> None:
        pbf_file = PbfFile(self._filepath)
        logging.debug('start parsing pbf file')
        results = self._parse_parallel(pbf_file)
        logging.debug('finished parsing pbf file')
        self._merge(results)
        logging.debug('finished merging pbf file')

    def _save_osm_elements(self) -> None:
        logging.debug('saving osm nodes and ways to pickle files')
        if self._use_cache:
            logging.debug('saving osm nodes to: %s', self._nodes_path)
            self.nodes.to_pickle(self._nodes_path)
            logging.debug('saving osm ways to: %s', self._ways_path)
            self.ways.to_pickle(self._ways_path)

    def _parse_parallel(self, pbf_file) -> List[Tuple]:
        with Pool(processes=cpu_count()) as pool:
            results = []
            blobs = [b for b in pbf_file.blobs()]
            prefix = f'Parsing Protobuf [{self.area_name}]'
            for result in tqdm(pool.imap(parse_block, blobs), desc=prefix):
                results.append(result)
        return results

    def _merge(self, results) -> None:
        logging.debug('separating nodes, ways and relations')
        nodes, ways, relations = [], [], []
        for elements in results:
            if not elements:
                continue
            osm_type = elements[0][0]
            if osm_type == 0:
                nodes.extend(elements)
            elif osm_type == 1:
                ways.extend(elements)
        logging.debug('building nodes and ways data frame')
        self.nodes = pd.DataFrame(nodes, columns=NODE_COLUMNS)
        self.nodes.drop(columns='type', inplace=True)
        self.ways = pd.DataFrame(ways, columns=WAY_COLUMNS)
        self.ways.drop(columns='type', inplace=True)


if __name__ == '__main__':
    file_name = DATA_PATH / 'germany-latest.osm.pbf'
    parser = PbfParser(file_name, use_cache=True)
    print(parser.nodes.head())
    print(parser.ways.head())
