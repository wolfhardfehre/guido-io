import logging

from app.routing.routing import Routing
from app.tour_optimizer.poi import Poi
from app.tour_optimizer.segment import Segment


class Bucket:

    def __init__(self, routing: Routing):
        self.routing = routing
        self._segments = {}

    def add(self, origin: Poi, destination: Poi):
        if self._redundant(origin, destination):
            return
        path = self.routing.path(origin=origin.location, destination=destination.location)
        logging.info(
            f'meters: {path.distance:.2f} from: {origin.name} [{origin.id}], to: {destination.name} [{destination.id}]'
        )
        key = frozenset({origin.id, destination.id})
        segment = Segment(
            pois=(origin, destination),
            distance=(origin.id, destination.id, path.distance),
            nodes=path.nodes
        )
        self._segments.update({key: segment})

    @property
    def distances(self):
        return [segment.element for segment in self._segments.values()]

    def segments(self, keys):
        return [self.segment_by(key) for key in keys]

    def segment_by(self, key: set):
        segment = self._segments[frozenset(key)]
        segment.order = key
        return segment

    def _redundant(self, origin, destination):
        has_key = {origin.id, destination.id} in list(self._segments.keys())
        return origin.id == destination.id or has_key
