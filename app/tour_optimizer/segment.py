import pandas as pd
from ipyleaflet import LayerGroup

from app.commons.layer import Layer
from app.routing.path import Path


class Segment(Layer):

    def __init__(self, pois: tuple, distance: tuple, nodes: pd.DataFrame):
        self.pois = pois
        self.element = distance
        self.path = Path(nodes, distance[2])
        self.order = None

    @property
    def layer(self):
        layers = [poi.layer for poi in self.pois]
        layers.append(self.path.layer)
        return LayerGroup(layers=layers)

    @property
    def empty(self):
        return any([poi.empty for poi in self.pois]) or self.path.empty

    @property
    def origin(self):
        return self._poi_by(self.order[0])

    @property
    def destination(self):
        return self._poi_by(self.order[1])

    def _poi_by(self, pid):
        return self.pois[0] if pid == self.pois[0].id else self.pois[1]

    def __repr__(self):
        return f'Segment(origin={self.origin.name},destination={self.destination.name},distance={self.path.distance:.0f}m)'
