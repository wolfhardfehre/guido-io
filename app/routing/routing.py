from app.overpass.location import Location
from app.routing.algorithm import Algorithm
from app.routing.graph import Graph
from app.routing.dijkstra import Dijkstra
from app.routing.path import Path


class Routing:

    def __init__(self):
        self._graph = Graph.load_default()
        self._algorithm = Dijkstra()

    @property
    def bounds(self):
        return self._graph.bounds

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        self._graph = graph
        self._algorithm.graph = graph

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm: Algorithm):
        self._algorithm = algorithm
        self._algorithm.graph = self.graph

    def path(self, origin, destination):
        origin_node, _ = self.graph.closest_to(origin)
        destination_node, _ = self.graph.closest_to(destination)
        shortest_path, distance = self.algorithm.shortest_path(
            start=origin_node.name,
            end=destination_node.name
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
