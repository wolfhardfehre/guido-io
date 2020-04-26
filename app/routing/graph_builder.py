import logging
import pandas as pd
import pickle
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.config import NODES_PATH, EDGES_PATH, GRAPH_PATH
from app.routing.feeds.feed import Feed
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
            index = row.node1
            if index not in adjacent:
                adjacent[index] = Node(index, row.lat, row.lon)
            adjacent.get(index).add_neighbor(row.node2, row.distance)
        return adjacent

    @property
    def _joined(self):
        logging.debug('joining nodes and edges')
        edges = self.edges.join(self.nodes, on='node1', rsuffix='_from')
        edges = edges.join(self.nodes, on='node2', rsuffix='_to')
        return edges


if __name__ == '__main__':
    logging.debug('fetching ways')
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    ways = Ways()
    ways.location = Location(13.383333, 52.516667)
    ways.radius = 10000
    ways.selection = '["highway"]'
    ways_around = ways.around()

    overpass_feed = OverpassFeed(ways=ways_around)

    builder = GraphBuilder(feed=overpass_feed)
    builder.save()
