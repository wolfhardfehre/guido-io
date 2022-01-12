from queue import PriorityQueue
from typing import Tuple

import pandas as pd

from app.config import logging
from app.routing.algorithms.algorithm import Algorithm


class Dijkstra(Algorithm):

    def shortest_path(self, start: int, end: int) -> Tuple[pd.DataFrame, float]:
        logging.debug('running dijkstra')
        distances, predecessors = self._dijkstra(start, end)
        distance = distances[end]
        node_id_sequence = []
        while True:
            node_id_sequence.append(end)
            if end == start:
                break
            end = predecessors[end]
        node_id_sequence.reverse()
        logging.debug('shortest path: %s', node_id_sequence)
        path_nodes = self._graph.path_of(node_id_sequence)
        return path_nodes, distance

    def _dijkstra(self, start: int, end: int) -> Tuple[dict, dict]:
        distances, predecessors = {}, {}
        queue = PriorityQueue()
        queue.put((0, start))
        while not queue.empty():
            d, v = queue.get()
            if v == end:
                break
            if v not in self.graph:
                continue
            neighbors = self.graph[v]['neighbors']
            for w in neighbors:
                distance = d + neighbors[w]
                if w not in distances or distance < distances[w]:
                    distances[w] = distance
                    queue.put((distance, w))
                    predecessors[w] = v
        return distances, predecessors


if __name__ == '__main__':
    dijkstra = Dijkstra()
    shortest_path, path_distance = dijkstra.shortest_path(
        start=27785378,
        end=2493824077
    )
    print(f'distance={path_distance}')
    print(shortest_path)
