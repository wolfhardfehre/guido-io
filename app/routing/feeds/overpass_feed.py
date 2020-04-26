import logging
import pandas as pd

from app.overpass.location import Location
from app.overpass.ways import Ways
from app.routing.feeds.feed import Feed
from app.utils.geoutils import meters


class OverpassFeed(Feed):

    def __init__(self, ways: pd.DataFrame):
        self.ways = ways
        super().__init__()

    def _nodes(self):
        logging.debug('building nodes')
        nodes = []
        for way in self.ways.itertuples():
            for nid, geom in zip(way.nodes, way.geometry):
                nodes.append({'id': nid, 'lat': geom['lat'], 'lon': geom['lon']})
        return self._build_nodes(nodes)

    def _edges(self):
        logging.debug('building edges')
        edges = []
        for way in self.ways.itertuples():
            nodes = way.nodes
            for first, second in zip(nodes[:-1], nodes[1:]):
                edges.append({'node1': first, 'node2': second})
        return self._build_edges(edges)

    def _build_edges(self, edge_list):
        edges = pd.DataFrame(edge_list)
        edges = edges.join(self.nodes, on='node1', rsuffix='_from')
        edges = edges.join(self.nodes, on='node2', rsuffix='_to')
        edges['distance'] = edges.apply(lambda row: self._distance(row), axis=1)
        edges = self._build_other_direction(edges)
        return edges

    @staticmethod
    def _build_other_direction(edges):
        copy = edges.copy(deep=True)
        copy = copy[['node1', 'node2', 'distance']]
        copy.columns = ['node2', 'node1', 'distance']
        return pd.concat([edges, copy]).reset_index()[['node1', 'node2', 'distance']]

    @staticmethod
    def _build_nodes(node_list):
        nodes = pd.DataFrame(node_list)
        nodes.drop_duplicates('id', inplace=True)
        nodes.set_index('id', inplace=True)
        return nodes

    @staticmethod
    def _distance(row):
        return meters(row['lat'], row['lon'], row['lat_to'], row['lon_to'])


if __name__ == '__main__':
    logging.debug('fetching ways')
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    overpass_ways = Ways()
    overpass_ways.location = Location(13.383333, 52.516667)
    overpass_ways.radius = 10000
    overpass_ways.selection = '["highway"]'
    ways_around = overpass_ways.around()

    overpass_feed = OverpassFeed(ways=ways_around)

    print(overpass_feed.nodes.head())
    print(overpass_feed.edges.head())
