import math


def meters(from_lat, from_lon, to_lat, to_lon):
    from_lat_rad = math.radians(from_lat)
    to_lat_rad = math.radians(to_lat)
    delta = math.radians(to_lon - from_lon)
    return math.acos(math.sin(from_lat_rad) * math.sin(to_lat_rad) +
                     math.cos(from_lat_rad) * math.cos(to_lat_rad) *
                     math.cos(delta)) * 6371e3


def centroid(bounding_box):
    south, west, north, east = bounding_box
    lon = west + abs(east - west) / 2.0
    lat = south + abs(north - south) / 2.0
    return lon, lat
