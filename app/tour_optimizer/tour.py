from ipyleaflet import LayerGroup

from app.commons.layer import Layer


class Tour(Layer):

    def __init__(self, segments: list, meters: float):
        self.segments = segments
        self.meters = meters

    @property
    def layer(self):
        return LayerGroup(layers=[segment.layer for segment in self.segments])

    @property
    def empty(self):
        return len(self.segments) == 0
