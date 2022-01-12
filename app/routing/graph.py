from __future__ import annotations

import logging
import pickle
from typing import Tuple

import pandas as pd

from app.overpass.location import Location
from app.paths import NODES_PATH, GRAPH_PATH, INDEX_PATH
from app.routing.spatial_index import SpatialIndex


class Graph:
    __instance__ = None

    def __init__(self, graph: dict, nodes: pd.DataFrame, index: SpatialIndex):
        self.graph = graph
        self.nodes = nodes
        self.index = index

    @classmethod
    def load_default(cls) -> Graph:
        if cls.__instance__ is None:
            nodes = cls._read_nodes()
            graph = cls._read_graph()
            index = cls._read_index()
            cls.__instance__ = Graph(graph, nodes, index)
        return cls.__instance__

    @staticmethod
    def _read_nodes() -> pd.DataFrame:
        logging.debug('load nodes from file')
        return pd.read_pickle(NODES_PATH)

    @staticmethod
    def _read_graph() -> dict:
        logging.debug('load graph from file')
        with GRAPH_PATH.open(mode='rb') as file:
            return pickle.load(file)

    @staticmethod
    def _read_index() -> SpatialIndex:
        logging.debug('load spatial index from file')
        with INDEX_PATH.open(mode='rb') as file:
            return pickle.load(file)

    def path_of(self, node_id_sequence) -> pd.DataFrame:
        return self.nodes.loc[node_id_sequence]

    def closest_to(self, location: Location) -> Tuple[pd.Series, float]:
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
