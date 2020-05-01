import logging
import pandas as pd
import pickle

from app.osm.pbf_parser import PbfParser
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.config import NODES_PATH, EDGES_PATH, GRAPH_PATH, DATA_PATH
from app.routing.feeds.feed import Feed, TO_NODE, FROM_NODE
from app.routing.feeds.osm_feed import OsmFeed
from app.routing.feeds.overpass_feed import OverpassFeed
from app.routing.node import Node


class GraphBuilder:

    def __init__(self, feed: Feed):
        self.nodes = feed.nodes
        self.edges = feed.edges
        self.graph = self._build_graph()
        logging.debug('finished building graph')

    def save(self):
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)
        logging.debug(f'Saving {len(self.edges)} edges')
        self.edges.to_pickle(EDGES_PATH)
        logging.debug(f'Saving graph')
        with open(GRAPH_PATH, 'wb') as handle:
            pickle.dump(self.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def _build_graph(self):
        joined = self._joined
        logging.debug('building graph')
        adjacent = {}
        for row in joined.itertuples():
            index = row.origin
            if index not in adjacent:
                adjacent[index] = Node(index, row.lat, row.lon)
            adjacent.get(index).add_neighbor(row.destination, row.meters)
        return adjacent

    @property
    def _joined(self):
        logging.debug('joining nodes and edges')
        edges = self.edges.join(self.nodes, on=FROM_NODE, rsuffix='_from')
        edges = edges.join(self.nodes, on=TO_NODE, rsuffix='_to')
        return edges


def feed_factory(feed_type='overpass'):
    if feed_type == 'overpass':
        ways = Ways()
        ways.location = Location(13.383333, 52.516667)
        ways.radius = 10000
        ways.selection = '["highway"]'
        ways_around = ways.around()
        return OverpassFeed(ways=ways_around)
    elif feed_type == 'osm':
        file_name = f'{DATA_PATH}/berlin-latest.osm.pbf'
        parser = PbfParser(file_name, use_cache=True)
        return OsmFeed(ways=parser.ways, nodes=parser.nodes)
    else:
        raise RuntimeError('no valid feed type selected. Valid feed types are "overpass" or "osm"!')


if __name__ == '__main__':
    logging.debug('fetching ways')
    builder = GraphBuilder(feed=feed_factory('osm'))
    builder.save()
