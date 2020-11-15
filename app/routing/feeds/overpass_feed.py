import logging
import pandas as pd
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.routing.feeds.feed import Feed, NODE_ID, LATITUDE, LONGITUDE, FROM_NODE, TO_NODE, DISTANCE


class OverpassFeed(Feed):
    __TYPE__ = 'overpass'

    @classmethod
    def around(cls, longitude, latitude, **kwargs):
        radius = kwargs.get('radius', 10_000)
        selection = kwargs.get('selection', '["highway"]')

        ways = Ways()
        ways.location = Location(longitude=longitude, latitude=latitude)
        ways.radius = radius
        ways.selection = selection
        return OverpassFeed(name=f'around({round(longitude, 3)}, {round(latitude, 3)})', ways=ways.around())

    def __init__(self, name: str, ways: pd.DataFrame):
        self._name = name
        self.ways = ways
        super().__init__()

    @property
    def name(self):
        return self._name

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

    feed = OverpassFeed.around(longitude=13.383333, latitude=52.516667)
    logging.debug('finished')

    print(feed.nodes.head())
    print(feed.edges.head())
