import logging
from multiprocessing import Pool, cpu_count
import os
import re
import pandas as pd

from app.commons.progress_bar import ProgressBar
from app.config import CACHE_PATH
from app.osm.pbf.pbf_file import PbfFile
from app.osm.pbf.pbf_primitive_block import PdfPrimitiveBlock
from app.config import DATA_PATH


def parse_block(blob):
    filename, offset, size = blob['file_name'], blob['blob_position'], blob['blob_size']
    block_parser = PdfPrimitiveBlock(filename, offset, size)
    return [e for es in block_parser.parse() for e in es]


class PbfParser:

    def __init__(self, file_path, use_cache=False):
        self._file_path = file_path
        self._use_cache = use_cache
        self.area_name = self._cut_out_area_name()
        self._nodes_path = f'{CACHE_PATH}/osm-{self.area_name}-nodes.pkl'
        self._ways_path = f'{CACHE_PATH}/osm-{self.area_name}-ways.pkl'
        self.nodes = None
        self.ways = None
        self.relations = None
        self._load_osm_elements()

    def _cut_out_area_name(self):
        result = re.search(f'{CACHE_PATH}/(.*)-latest', self._file_path)
        return result.group(1)

    def _load_osm_elements(self):
        if self._use_cache:
            self._load_from_pickle()
        if self.nodes is None or self.ways is None:
            self._parse_from_pbf()
            self._save_osm_elements()

    def _load_from_pickle(self):
        logging.debug('trying to load osm nodes and ways from pickle files')
        if os.path.isfile(self._nodes_path):
            logging.info(f'reading osm nodes from: {self._nodes_path}')
            self.nodes = pd.read_pickle(self._nodes_path)
        if os.path.isfile(self._ways_path):
            logging.info(f'reading osm ways from: {self._ways_path}')
            self.ways = pd.read_pickle(self._ways_path)

    def _parse_from_pbf(self):
        pbf_file = PbfFile(self._file_path)
        logging.debug('start parsing pbf file')
        results = self._parse_parallel(pbf_file)
        logging.debug('finished parsing pbf file')
        self._merge(results)
        logging.debug('finished merging pbf file')

    def _save_osm_elements(self):
        logging.debug('saving osm nodes and ways to pickle files')
        if self._use_cache:
            logging.debug(f'saving osm nodes to: {self._nodes_path}')
            self.nodes.to_pickle(self._nodes_path)
            logging.debug(f'saving osm ways to: {self._ways_path}')
            self.ways.to_pickle(self._ways_path)

    def _parse_parallel(self, pbf_file):
        with Pool(processes=cpu_count()) as pool:
            results = []
            blobs = [b for b in pbf_file.blobs()]
            prefix = f'Parsing Protobuf [{self.area_name}]'
            progress_bar = ProgressBar(total=len(blobs), prefix=prefix)
            for result in pool.imap(parse_block, blobs):
                progress_bar.update()
                results.append(result)
        return results

    def _merge(self, results):
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
        node_columns = ['type', 'id', 'lon', 'lat']
        self.nodes = pd.DataFrame(nodes, columns=node_columns)
        self.nodes.drop(columns='type', inplace=True)
        way_columns = ['type', 'origin', 'destination', 'highway', 'oneway', 'max_speed', 'access']
        self.ways = pd.DataFrame(ways, columns=way_columns)
        self.ways.drop(columns='type', inplace=True)


if __name__ == '__main__':
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    osm_area = 'germany'
    file_name = f'{DATA_PATH}/{osm_area}-latest.osm.pbf'
    parser = PbfParser(file_name, use_cache=True)
    print(parser.nodes.head())
    print(parser.ways.head())
