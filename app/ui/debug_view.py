from IPython.core.display import display
from app.overpass.location import Location
from app.routing.routing import Routing
from app.tour_optimizer.tour_optimizer import TourOptimizer
from app.ui.leaflet_map import LeafletMap


class DebugView:

    def __init__(self, routing=Routing()):
        self.routing = routing
        self.tour = TourOptimizer(routing)
        self._map = LeafletMap(routing.bounds)
        display(self._map.map)

    def display_path(self, origin, destination):
        path = self.routing.path(origin, destination)
        self._map.update(path)

    def display_tour(self, pois: list, **kwargs):
        tour = self.tour.find_best(pois, **kwargs)
        self._map.update(tour)


if __name__ == '__main__':
    from app.tour_optimizer.poi import Poi
    view = DebugView()
    a = Location(longitude=13.3587658, latitude=52.4857809)
    b = Location(longitude=13.412003, latitude=52.522625)
    view.display_path(a, b)

    neukoelln = Poi(0, 'Neukölln', Location(13.434469, 52.481374))
    schlesi = Poi(1, 'Schlesi', Location(13.441840, 52.500931))
    alex = Poi(2, 'Alex', Location(13.412937, 52.521811))
    charlie = Poi(3, 'Charlie', Location(13.390779, 52.507484))
    kotti = Poi(4, 'Kotti', Location(13.418210, 52.499224))
    points_of_interest = [neukoelln, schlesi, alex, charlie, kotti]
    view.display_tour(points_of_interest)
