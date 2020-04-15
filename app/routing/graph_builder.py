import logging
import pandas as pd
import pickle
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.routing.config import NODES_PATH, EDGES_PATH, GRAPH_PATH
from app.utils.geoutils import meters
from app.routing.node import Node


class GraphBuilder:

    def __init__(self, feed: pd.DataFrame):
        self.ways = feed
        self.nodes = self._nodes()
        self.edges = self._edges()
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

    builder = GraphBuilder(ways_around)
    builder.save()
