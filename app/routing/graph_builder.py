from __future__ import annotations

import logging
import pickle

from tqdm import tqdm

from app.paths import NODES_PATH, GRAPH_PATH, INDEX_PATH
from app.routing.feeds.factory import Factory
from app.routing.feeds.feed_type import FeedType
from app.routing.feeds.feed import Feed
from app.routing.spatial_index import SpatialIndex


class GraphBuilder:

    def __init__(self, feed: Feed):
        self.nodes = feed.nodes
        self.edges = feed.edges
        self.graph = self._build_graph(feed.name)
        self.index = SpatialIndex(feed.nodes)
        logging.debug('finished building graph')

    @classmethod
    def build(cls, feed: Feed) -> GraphBuilder:
        if feed.type in FeedType:
            return GraphBuilder(feed)
        raise RuntimeError(f'No valid feed type selected. Valid feed types are {" or ".join(FeedType)}!')

    def save(self) -> None:
        self._save_nodes()
        self._save_routing_graph()
        self._save_spatial_index()

    def _save_nodes(self) -> None:
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)

    def _save_routing_graph(self) -> None:
        logging.debug(f'Saving graph with {len(self.graph)} nodes')
        with GRAPH_PATH.open(mode='wb') as handle:
            pickle.dump(self.graph, handle)

    def _save_spatial_index(self) -> None:
        logging.debug(f'Saving spatial index')
        with INDEX_PATH.open(mode='wb') as handle:
            pickle.dump(self.index, handle)

    def _build_graph(self, feed_name: str) -> dict:
        logging.debug('building graph')
        adjacent = {}
        prefix = f'Building Graph [{feed_name}]'
        for row in tqdm(self.edges.sort_index().itertuples(), desc=prefix):
            index = row.origin
            if index not in adjacent:
                adjacent[index] = {'neighbors': {}}
            adjacent.get(index)['neighbors'][row.destination] = row.meters
        return adjacent


if __name__ == '__main__':
    logging.debug('fetching ways')
    selected_feed = Factory.feed_of(
        feed_type=FeedType.OSM,
        region='berlin'
    )
    logging.info('building graph')
    builder = GraphBuilder.build(feed=selected_feed)
    logging.info('saving graph')
    builder.save()
    logging.debug('finished building and saving the graph')
