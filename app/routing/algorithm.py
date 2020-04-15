import abc

from app.overpass.location import Location
from app.routing.graph import Graph


class Algorithm(abc.ABC):
    """Base class for routing algorithms, uses loaded graph by default"""

    def __init__(self):
        self._graph = Graph.load_default()

    @property
    def graph(self):
        return self._graph.graph

    @property
    def nodes(self):
        return self._graph.nodes

    @graph.setter
    def graph(self, graph: Graph):
        self._graph = graph

    @abc.abstractmethod
    def shortest_path(self, origin: Location, destination: Location):
        raise NotImplementedError
