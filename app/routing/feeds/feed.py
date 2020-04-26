import abc
import logging
from app.config import NODES_PATH, EDGES_PATH


class Feed(abc.ABC):

    def __init__(self):
        self.nodes = self._nodes()
        self.edges = self._edges()

    def save(self):
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)
        logging.debug(f'Saving {len(self.edges)} edges')
        self.edges.to_pickle(EDGES_PATH)

    @abc.abstractmethod
    def _nodes(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _edges(self):
        raise NotImplementedError
