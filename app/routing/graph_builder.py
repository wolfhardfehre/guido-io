import logging
import pickle

from app.commons.progress_bar import ProgressBar
from app.config import NODES_PATH, GRAPH_PATH, INDEX_PATH
from app.routing.feeds.factory import ACCEPTABLE_FEED_TYPES, Factory
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
    def build(cls, feed: Feed):
        if feed.type in ACCEPTABLE_FEED_TYPES:
            return GraphBuilder(feed)
        else:
            raise RuntimeError(f'No valid feed type selected. '
                               f'Valid feed types are {" or ".join(ACCEPTABLE_FEED_TYPES)}!')

    def save(self):
        self._save_nodes()
        self._save_routing_graph()
        self._save_spatial_index()

    def _save_nodes(self):
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)

    def _save_routing_graph(self):
        logging.debug(f'Saving graph with {len(self.graph)} nodes')
        with open(GRAPH_PATH, 'wb') as handle:
            pickle.dump(self.graph, handle)

    def _save_spatial_index(self):
        logging.debug(f'Saving spatial index')
        with open(INDEX_PATH, 'wb') as handle:
            pickle.dump(self.index, handle)

    def _build_graph(self, feed_name):
        logging.debug('building graph')
        adjacent = {}
        prefix = f'Building Graph [{feed_name}]'
        progress_bar = ProgressBar(total=self.edges.shape[0], prefix=prefix)
        for row in self.edges.sort_index().itertuples():
            progress_bar.update()
            index = row.origin
            if index not in adjacent:
                adjacent[index] = {'neighbors': {}}
            adjacent.get(index)['neighbors'][row.destination] = row.meters
        return adjacent


if __name__ == '__main__':
    logging.debug('fetching ways')
    selected_feed = Factory.feed_of(
        type='osm',
        continent='europe',
        country='germany',
        state='berlin'
    )
    builder = GraphBuilder.build(feed=selected_feed)
    builder.save()
    logging.debug('finished building and saving the graph')
