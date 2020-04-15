import pandas as pd
from ipyleaflet import basemap_to_tiles, basemaps, FullScreenControl, Map, Polyline, TileLayer

from app.commons.layer import Layer
from app.utils.maputils import center


class LeafletMap:

    def __init__(self, bounds: tuple):
        self.layer = None
        self._leaflet_map = Map(
            layers=(basemap_to_tiles(basemaps.OpenStreetMap.BlackAndWhite),),
            name="Leaflet Map",
            center=center(bounds),
            zoom=12,
            scroll_wheel_zoom=True
        )
        self._leaflet_map.add_control(FullScreenControl())

    @property
    def map(self):
        return self._leaflet_map

    def update(self, layer: Layer):
        self.layer = layer
        self._remove_layers()
        self._update_layers()

    def _remove_layers(self):
        for layer in self._leaflet_map.layers:
            if isinstance(layer, TileLayer):
                continue
            self._leaflet_map.remove_layer(layer)

    def _update_layers(self):
        if self.layer.empty:
            return
        self._leaflet_map.add_layer(self.layer.layer)
