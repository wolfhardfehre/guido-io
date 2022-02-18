import abc
import logging
from typing import Optional

import pandas as pd
from app.paths import NODES_PATH, EDGES_PATH
from app.routing.feeds.feed_type import FeedType
from app.utils.geoutils import meters

FROM_NODE = 'origin'
TO_NODE = 'destination'
DISTANCE = 'meters'
NODE_ID = 'id'
LATITUDE = 'lat'
LONGITUDE = 'lon'


class Feed(abc.ABC):
    __TYPE__: Optional[FeedType] = None

    def __init__(self):
        self.nodes = self._nodes()
        self.edges = self._edges()

    def save(self):
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)
        logging.debug(f'Saving {len(self.edges)} edges')
        self.edges.to_pickle(EDGES_PATH)

    @property
    def type(self) -> FeedType:
        return self.__TYPE__

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _nodes(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _edges(self):
        raise NotImplementedError

    @staticmethod
    def _join(edges, nodes):
        logging.debug('join nodes onto edges')
        edges = edges.join(nodes, on=FROM_NODE)
        edges = edges.join(nodes, on=TO_NODE, rsuffix='_to')
        return edges

    @staticmethod
    def _compute_distances(edges):
        logging.debug('compute distances')
        edges[DISTANCE] = meters(
            edges[LATITUDE],
            edges[LONGITUDE],
            edges[f'{LATITUDE}_to'],
            edges[f'{LONGITUDE}_to']
        )
        return edges

    def _build_other_direction(self, edges, reversible_edges):
        logging.debug('append swapped none oneways')
        reversible_edges = self._swap_origin_destination(reversible_edges)
        edges = pd.concat([edges, reversible_edges])
        edges = edges.reset_index(drop=True)
        return edges

    @staticmethod
    def _swap_origin_destination(edges):
        columns = list(edges.columns)
        idx_from, idx_to = columns.index(FROM_NODE), columns.index(TO_NODE)
        columns[idx_to], columns[idx_from] = columns[idx_from], columns[idx_to]
        edges.columns = columns
        return edges
