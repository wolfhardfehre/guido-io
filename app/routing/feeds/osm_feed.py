from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from app.osm.geofabrik.geofabrik import Geofabrik
from app.osm.pbf_parser import PbfParser
from app.routing.feeds.feed_type import FeedType
from app.routing.feeds.feed import Feed, NODE_ID, LATITUDE, LONGITUDE, FROM_NODE, TO_NODE, DISTANCE

GOOD_HIGHWAYS = [
    'motorway',
    'trunk',
    'primary',
    'secondary',
    'tertiary',
    'unclassified',
    'residential',
    'motorway_link',
    'trunk_link',
    'primary_link',
    'secondary_link',
    'tertiary_link',
    'living_street',
    #'track',
    #'path',
    #'cycleway'
]


class OsmFeed(Feed):
    __TYPE__: FeedType = FeedType.OSM

    @classmethod
    def area(cls, **kwargs: Any) -> OsmFeed:
        use_cache = kwargs.get('use_cache', True)
        filepath = Geofabrik.fetch(region=kwargs['region'])
        parser = PbfParser(filepath, use_cache=use_cache)
        logging.debug(f'before: {parser.ways.shape[0]}')
        ways = parser.ways[parser.ways['highway'].isin(GOOD_HIGHWAYS)]
        logging.debug(f'after: {ways.shape[0]}')
        return OsmFeed(name=parser.area_name, ways=ways, nodes=parser.nodes)

    def __init__(self, name: str, ways: pd.DataFrame, nodes: pd.DataFrame):
        logging.debug('creating osm feed')
        self._name = name
        self._osm_ways = ways
        self._osm_nodes = nodes
        self._check_columns()
        super().__init__()
        self._clean_nodes()

    @property
    def name(self) -> str:
        return self._name

    def _check_columns(self) -> None:
        if not all([col in self._osm_ways.columns for col in (FROM_NODE, TO_NODE)]):
            raise ValueError(f'Columns of ways must contain {FROM_NODE} and {TO_NODE}!')
        if not all([col in self._osm_nodes.columns for col in (NODE_ID, LATITUDE, LONGITUDE)]):
            raise ValueError(f'Columns of nodes must contain {NODE_ID}, {LATITUDE} and {LONGITUDE}!')

    def _nodes(self) -> pd.DataFrame:
        logging.debug('building nodes')
        logging.debug(f'dropping node columns, {self._osm_nodes.shape[0]} rows')
        nodes = self._osm_nodes
        nodes.set_index(NODE_ID, inplace=True)
        return nodes

    def _edges(self) -> pd.DataFrame:
        logging.debug(f'dropping edge columns, {self._osm_ways.shape[0]} rows')
        edges = self._osm_ways
        edges = self._join(edges, self.nodes)
        edges = self._compute_distances(edges)
        reversible_edges = edges[~edges['oneway']].copy(deep=True)
        edges = self._build_other_direction(edges, reversible_edges)
        return edges[[FROM_NODE, TO_NODE, DISTANCE]]

    def _clean_nodes(self) -> None:
        edge_nodes_ids = self.edges[FROM_NODE].unique()
        self.nodes = self.nodes.loc[edge_nodes_ids, :]


if __name__ == '__main__':
    feed = OsmFeed.area(region='berlin')
    logging.debug('finished')
    print(feed.nodes.head())
    print(feed.edges.head())
