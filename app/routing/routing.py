from typing import Tuple

import pandas as pd

from app.overpass.location import Location
from app.routing.algorithms.algorithm import Algorithm
from app.routing.graph import Graph
from app.routing.algorithms.dijkstra import Dijkstra
from app.routing.path import Path


class Routing:

    def __init__(self):
        self._graph = Graph.load_default()
        self._algorithm = Dijkstra()

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        return self._graph.bounds

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph) -> None:
        self._graph = graph
        self._algorithm.graph = graph

    @property
    def algorithm(self) -> Algorithm:
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: Algorithm) -> None:
        self._algorithm = algorithm
        self._algorithm.graph = self.graph

    def path(self, origin: Location, destination: Location) -> Path:
        origin_node: pd.Series = self.graph.closest_to(origin)[0]
        destination_node: pd.Series = self.graph.closest_to(destination)[0]
        print(origin_node)
        shortest_path, distance = self.algorithm.shortest_path(
            origin=origin_node.name,
            destination=destination_node.name
        )
        return Path(shortest_path, distance)


if __name__ == '__main__':
    routing = Routing()
    path = routing.path(
        origin=Location(longitude=13.3587658, latitude=52.4857809),
        destination=Location(longitude=13.412003, latitude=52.522625)
    )
    print(f'distance = {path.distance} m')
    print(path.nodes)
