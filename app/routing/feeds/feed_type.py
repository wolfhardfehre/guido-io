from enum import Enum


class FeedType(str, Enum):
    OSM = 'osm'
    OVERPASS = 'overpass'
