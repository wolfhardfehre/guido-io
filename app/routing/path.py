import pandas as pd
from ipyleaflet import Polyline

from app.commons.layer import Layer


class Path(Layer):

    def __init__(self, nodes: pd.DataFrame, distance: float):
        self.nodes = nodes
        self.distance = distance

    @property
    def layer(self):
        return Polyline(locations=self.coordinates, color="orange", fill=False)

    @property
    def empty(self):
        return self.nodes.empty

    @property
    def coordinates(self):
        return list(zip(self.nodes['lat'], self.nodes['lon']))

    def __repr__(self):
        return f'Path(nodes={self.nodes.shape[0]},meters={self.distance})'
