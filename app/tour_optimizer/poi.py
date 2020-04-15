from ipyleaflet import Marker, AwesomeIcon

from app.commons.layer import Layer
from app.overpass.location import Location


class Poi(Layer):

    def __init__(self, pid: int, name: str, location: Location):
        self.id = pid
        self.name = name
        self.location = location

    @property
    def layer(self):
        icon = AwesomeIcon(
            name='camera',
            marker_color='blue',
            icon_color='white'
        )
        return Marker(icon=icon, location=(self.location.latitude, self.location.longitude), draggable=False)

    @property
    def empty(self):
        return self.location is None or len(self.location) < 2

    def __repr__(self):
        return f'Poi(id={self.id},name={self.name},location={self.location})'
