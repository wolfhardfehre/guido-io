from typing import Tuple

import pandas as pd
import numpy as np
from scipy.spatial import KDTree
from app.overpass.location import Location
from app.routing.feeds.feed import LATITUDE, LONGITUDE
from app.config import logging, NODES_PATH


class SpatialIndex:

    def __init__(self, nodes: pd.DataFrame):
        logging.debug('building spatial index')
        geometries = nodes[[LONGITUDE, LATITUDE]].to_numpy()
        self._nodes = nodes
        self._algorithm = KDTree(geometries)
        self.bounds = self._bounds()

    def closest_to(self, location: Location) -> Tuple[pd.Series, float]:
        logging.debug('fetching closest point to %s', location)
        distance, index = self._algorithm.query(np.array(location))
        closest = self._nodes.iloc[index]
        logging.debug(
            'closest: %s, dist: %.7f°, loc: (%.7f, %.7f)', closest.name, distance, closest['lat'], closest['lon']
        )
        return closest, distance

    def _bounds(self) -> Tuple[float, float, float, float]:
        west = min(self._nodes[LONGITUDE])
        east = max(self._nodes[LONGITUDE])
        south = min(self._nodes[LATITUDE])
        north = max(self._nodes[LATITUDE])
        return west, south, east, north


if __name__ == '__main__':
    nds = pd.read_pickle(NODES_PATH)
    spatial_index = SpatialIndex(nds)

    loc = Location(longitude=13.412003, latitude=52.522625)
    node, degrees = spatial_index.closest_to(loc)

    print(f'node: {node.name}, distance: {degrees:.7f}°')
