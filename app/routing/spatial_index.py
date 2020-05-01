import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from app.overpass.location import Location
from app.routing.feeds.feed import LATITUDE, LONGITUDE
from app.config import logging, NODES_PATH


class SpatialIndex:

    def __init__(self, nodes: pd.DataFrame):
        logging.debug('building spatial index')
        geometries = nodes[[LONGITUDE, LATITUDE]].to_numpy()
        self._nodes = nodes
        self._algorithm = cKDTree(geometries)
        self.bounds = self._bounds()

    def closest_to(self, location: Location):
        logging.debug(f'fetching closest point to {location}')
        distance, index = self._algorithm.query(np.array(location))
        closest = self._nodes.iloc[index]
        logging.debug(f'closest: {closest.name}, dist: {distance}°, loc: ({closest["lat"]}, {closest["lon"]})')
        return closest, distance

    def _bounds(self):
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

    print(f'node: {node.name}, distance: {degrees}')
