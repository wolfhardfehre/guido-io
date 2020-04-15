import logging
import pickle
import pandas as pd

from app.overpass.location import Location
from app.routing.config import NODES_PATH, EDGES_PATH, GRAPH_PATH
from app.routing.spatial_index import SpatialIndex


class Graph:
    instance = None

    def __init__(self, graph, nodes, edges):
        self.graph = graph
        self.nodes = nodes
        self.edges = edges
        self.index = SpatialIndex(nodes)

    @classmethod
    def load_default(cls):
        if cls.instance is None:
            logging.debug('load nodes from file')
            nodes = pd.read_pickle(NODES_PATH)
            logging.debug('load edges from file')
            edges = pd.read_pickle(EDGES_PATH)
            logging.debug('load graph from file')
            with open(GRAPH_PATH, 'rb') as handle:
                graph = pickle.load(handle)
            logging.debug('load graph finished')
            cls.instance = Graph(graph, nodes, edges)
        return cls.instance

    def closest_to(self, location: Location):
        return self.index.closest_to(location)

    @property
    def bounds(self):
        return self.index.bounds


if __name__ == '__main__':
    g = Graph.load_default()
    loc = Location(longitude=13.412003, latitude=52.522625)
    node, degrees = g.closest_to(loc)
    print(f'graph with {len(g.graph)} elements')
    print(f'closest: {node.name}, distance: {degrees}°')
