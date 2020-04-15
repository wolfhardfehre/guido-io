def center(bounds: tuple):
    west, south, east, north = bounds
    latitude = south + ((north - south) / 2)
    longitude = west + ((east - west) / 2)
    return latitude, longitude
