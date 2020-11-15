from app.routing.feeds.feed import Feed
from app.routing.feeds.osm_feed import OsmFeed
from app.routing.feeds.overpass_feed import OverpassFeed

ACCEPTABLE_FEED_TYPES = ['osm', 'overpass']


class Factory:

    @classmethod
    def feed_of(cls, type, **kwargs) -> Feed:
        if type == 'osm':
            return OsmFeed.area(**kwargs)
        elif type == 'overpass':
            return OverpassFeed.around(**kwargs)
        else:
            raise ValueError(f'Unknown feed type: {type}! '
                             f'Please choose one of these -> {ACCEPTABLE_FEED_TYPES}.')
