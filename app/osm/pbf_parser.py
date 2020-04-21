import logging
import multiprocessing
import pandas as pd

from app.osm.pbf.pbf_file import PbfFile
from app.osm.pbf.pbf_primitive_block import PdfPrimitiveBlock
from app.routing.config import DATA_PATH


def parse_block(blob):
    filename, offset, size = blob['file_name'], blob['blob_position'], blob['blob_size']
    block_parser = PdfPrimitiveBlock(filename, offset, size)
    return [e for es in block_parser.parse() for e in es]


class PbfParser:

    def __init__(self, file_path):
        pdf_file = PbfFile(file_path)
        logging.info('start parsing pbf file')
        results = self._parse(pdf_file)
        logging.info('finished parsing pbf file')
        self.nodes = None
        self.ways = None
        self.relations = None
        self._merge(results)
        logging.info('finished merging pbf file')

    @staticmethod
    def _parse(pdf_file):
        processors = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=processors) as pool:
            return pool.map(parse_block, pdf_file.blobs())

    def _merge(self, results):
        nodes, ways, relations = [], [], []
        for elements in results:
            for element in elements:
                if element[0] == 0:
                    nodes.append(element[1:])
                elif element[0] == 1:
                    ways.append(element[1:])
                elif element[0] == 2:
                    relations.append(element[1:])
        self.nodes = pd.DataFrame(nodes, columns=['id', 'tags', 'lon', 'lat'])
        self.ways = pd.DataFrame(ways, columns=['id', 'tags', 'refs'])
        self.relations = pd.DataFrame(relations, columns=['id', 'tags', 'members'])


if __name__ == '__main__':
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    file_name = f'{DATA_PATH}/berlin-latest.osm.pbf'
    parser = PbfParser(file_name)
    print(parser.nodes.head())
    print(parser.ways.head())
    print(parser.relations.head())
