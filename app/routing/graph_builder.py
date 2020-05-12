import logging
import pickle

from app.commons.progress_bar import progress_bar
from app.osm.pbf_parser import PbfParser
from app.overpass.location import Location
from app.overpass.ways import Ways
from app.config import NODES_PATH, GRAPH_PATH, DATA_PATH, INDEX_PATH
from app.routing.feeds.feed import Feed
from app.routing.feeds.osm_feed import OsmFeed
from app.routing.feeds.overpass_feed import OverpassFeed
from app.routing.spatial_index import SpatialIndex


class GraphBuilder:

    def __init__(self, feed: Feed):
        self.nodes = feed.nodes
        self.edges = feed.edges
        self.graph = self._build_graph()
        self.index = SpatialIndex(feed.nodes)
        logging.debug('finished building graph')

    def save(self):
        logging.debug(f'Saving {len(self.nodes)} nodes')
        self.nodes.to_pickle(NODES_PATH)
        logging.debug(f'Saving graph with {len(self.graph)} nodes')
        with open(GRAPH_PATH, 'wb') as handle:
            pickle.dump(self.graph, handle)
        logging.debug(f'Saving spatial index')
        with open(INDEX_PATH, 'wb') as handle:
            pickle.dump(self.index, handle)

    def _build_graph(self):
        logging.debug('building graph')
        adjacent = {}
        i = 0
        length = self.edges.shape[0]
        for row in self.edges.itertuples():
            i += 1
            progress_bar(i, length, prefix='building graph')
            index = row.origin
            if index not in adjacent:
                adjacent[index] = {'neighbors': {}}
            adjacent.get(index)['neighbors'][row.destination] = row.meters
        return adjacent


def feed_factory(feed_type='overpass', osm_area='berlin', use_cache=True):
    if feed_type == 'overpass':
        ways = Ways()
        ways.location = Location(13.383333, 52.516667)
        ways.radius = 10000
        ways.selection = '["highway"]'
        ways_around = ways.around()
        return OverpassFeed(ways=ways_around)
    elif feed_type == 'osm':
        # TODO: download from geofabrik if not exists
        file_name = f'{DATA_PATH}/{osm_area}-latest.osm.pbf'
        parser = PbfParser(file_name, use_cache=use_cache)
        good_highways = ['tertiary', 'primary', 'secondary', 'trunk',
                         'residential', 'living_street', 'path',
                         'unclassified', 'track', 'primary_link', 'secondary_link', 'cycleway']
        logging.debug(f'before: {parser.ways.shape[0]}')
        ways = parser.ways[parser.ways['highway'].isin(good_highways)]
        logging.debug(f'after: {ways.shape[0]}')
        return OsmFeed(ways=ways, nodes=parser.nodes)
    else:
        raise RuntimeError('no valid feed type selected. Valid feed types are "overpass" or "osm"!')


if __name__ == '__main__':
    logging.debug('fetching ways')
    graph_feed = feed_factory(
        feed_type='osm',
        osm_area='brandenburg'
    )
    builder = GraphBuilder(feed=graph_feed)
    builder.save()
    logging.debug('finished building and saving the graph')
