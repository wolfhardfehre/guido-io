import mlrose_hiive as mlrose

from app.overpass.location import Location
from app.routing.routing import Routing
from app.config import logging
from app.tour_optimizer.bucket import Bucket
from app.tour_optimizer.poi import Poi
from app.tour_optimizer.tour import Tour


class TourOptimizer:

    def __init__(self, routing=Routing()):
        self.routing = routing

    def find_best(self, pois: list, **kwargs):
        logging.debug('init bucket')
        bucket = Bucket(self.routing)
        logging.debug('compute distance matrix')
        self.compute_distances(pois, bucket)
        logging.debug('define fitness function')
        fitness_dists = mlrose.TravellingSales(distances=bucket.distances)
        logging.debug('define optimization problem')
        problem_fit = mlrose.TSPOpt(
            length=len(pois),
            fitness_fn=fitness_dists,
            maximize=False
        )
        logging.debug('run randomized optimization algorithm')
        best_state, best_fitness, fitness_curve = mlrose.genetic_alg(problem_fit, random_state=2, **kwargs)
        segments = bucket.segments(self._generate_keys(best_state))
        meters = sum([segment.path.distance for segment in segments])
        return Tour(segments, meters)

    @staticmethod
    def compute_distances(pois, bucket):
        for origin in pois:
            for destination in pois:
                bucket.add(origin, destination)

    @staticmethod
    def _generate_keys(array):
        return list(zip(array[:-1], array[1:]))


if __name__ == '__main__':
    neukoelln = Poi(0, 'Neukölln', Location(13.434469, 52.481374))
    schlesi = Poi(1, 'Schlesi', Location(13.441840, 52.500931))
    alex = Poi(2, 'Alex', Location(13.412937, 52.521811))
    charlie = Poi(3, 'Charlie', Location(13.390779, 52.507484))
    kotti = Poi(4, 'Kotti', Location(13.418210, 52.499224))

    optimizer = TourOptimizer()
    tour = optimizer.find_best([neukoelln, schlesi, alex, charlie, kotti])

    print(f'::: BEST TOUR [{tour.meters:.0f}m]:::')
    for leg in tour.segments:
        print(leg)
