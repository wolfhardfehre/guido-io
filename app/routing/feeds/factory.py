from typing import Any

from app.routing.feeds.feed import Feed
from app.routing.feeds.feed_type import FeedType
from app.routing.feeds.osm_feed import OsmFeed
from app.routing.feeds.overpass_feed import OverpassFeed


class Factory:

    @classmethod
    def feed_of(cls, feed_type: FeedType, **kwargs: Any) -> Feed:
        if feed_type == FeedType.OSM:
            return OsmFeed.area(**kwargs)
        elif feed_type == FeedType.OVERPASS:
            return OverpassFeed.around(**kwargs)
        raise ValueError(f'Unknown feed type: {feed_type}! Please choose one of: {FeedType}')
