import logging
import pandas as pd
from app.osm.pbf_parser import PbfParser
from app.routing.feeds.feed import Feed, NODE_ID, LATITUDE, LONGITUDE, FROM_NODE, TO_NODE, DISTANCE
from app.config import DATA_PATH


class OsmFeed(Feed):

    def __init__(self, ways: pd.DataFrame, nodes: pd.DataFrame):
        logging.debug('creating osm feed')
        self._osm_ways = ways
        self._osm_nodes = nodes
        self._check_columns()
        super().__init__()
        self._clean_nodes()

    def _check_columns(self):
        if not all([col in self._osm_ways.columns for col in (FROM_NODE, TO_NODE)]):
            raise ValueError(f'Columns of ways must contain {FROM_NODE} and {TO_NODE}!')
        if not all([col in self._osm_nodes.columns for col in (NODE_ID, LATITUDE, LONGITUDE)]):
            raise ValueError(f'Columns of nodes must contain {NODE_ID}, {LATITUDE} and {LONGITUDE}!')

    def _nodes(self):
        logging.debug('building nodes')
        logging.debug(f'dropping node columns, {self._osm_nodes.shape[0]} rows')
        nodes = self._osm_nodes
        nodes.set_index(NODE_ID, inplace=True)
        return nodes

    def _edges(self):
        logging.debug(f'dropping edge columns, {self._osm_ways.shape[0]} rows')
        edges = self._osm_ways
        edges = self._join(edges, self.nodes)
        edges = self._compute_distances(edges)
        reversible_edges = edges[edges['oneway']].copy(deep=True)
        edges = self._build_other_direction(edges, reversible_edges)
        return edges[[FROM_NODE, TO_NODE, DISTANCE]]

    def _clean_nodes(self):
        edge_nodes_ids = self.edges[FROM_NODE].unique()
        self.nodes = self.nodes.loc[edge_nodes_ids, :]


if __name__ == '__main__':
    pd.options.display.max_rows = None
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    osm_area = 'brandenburg'
    file_name = f'{DATA_PATH}/{osm_area}-latest.osm.pbf'
    parser = PbfParser(file_name, use_cache=True)

    feed = OsmFeed(ways=parser.ways, nodes=parser.nodes)
    logging.debug('finished')

    print(feed.nodes.head())
    print(feed.edges.head())
