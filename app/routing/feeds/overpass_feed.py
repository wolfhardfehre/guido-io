import logging
import pandas as pd
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.routing.feeds.feed import Feed, NODE_ID, LATITUDE, LONGITUDE, FROM_NODE, TO_NODE, DISTANCE


class OverpassFeed(Feed):

    def __init__(self, ways: pd.DataFrame):
        self.ways = ways
        super().__init__()

    def _nodes(self):
        logging.debug('building nodes')
        nodes = []
        for way in self.ways.itertuples():
            for nid, geom in zip(way.nodes, way.geometry):
                nodes.append({NODE_ID: nid, LATITUDE: geom['lat'], LONGITUDE: geom['lon']})
        return self._build_nodes(nodes)

    def _edges(self):
        logging.debug('building edges')
        edges = []
        for way in self.ways.itertuples():
            nodes = way.nodes
            for first, second in zip(nodes[:-1], nodes[1:]):
                edges.append({FROM_NODE: first, TO_NODE: second})
        return self._build_edges(edges)

    @staticmethod
    def _build_nodes(node_list):
        nodes = pd.DataFrame(node_list)
        nodes.drop_duplicates(NODE_ID, inplace=True)
        nodes.set_index(NODE_ID, inplace=True)
        return nodes

    def _build_edges(self, edge_list):
        edges = pd.DataFrame(edge_list)
        edges = self._join(edges, self.nodes)
        edges = self._compute_distances(edges)
        reversible_edges = edges.copy(deep=True)
        edges = self._build_other_direction(edges, reversible_edges)
        return edges[[FROM_NODE, TO_NODE, DISTANCE]]


if __name__ == '__main__':
    logging.debug('fetching ways')
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    overpass_ways = Ways()
    overpass_ways.location = Location(13.383333, 52.516667)
    overpass_ways.radius = 1000
    overpass_ways.selection = '["highway"]'
    ways_around = overpass_ways.around()

    overpass_feed = OverpassFeed(ways=ways_around)
    logging.debug('finished')

    print(overpass_feed.nodes.head())
    print(overpass_feed.edges.head())
