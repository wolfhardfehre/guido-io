from app.config import logging
from app.routing.algorithm import Algorithm
from app.routing.priority_dict import PriorityDict


class Dijkstra(Algorithm):
    """ Shortest Path with Dijkstra by David Eppstein, UC Irvine, 8 Mar 2002 """

    def shortest_path(self, start, end):
        distances, predecessors = self.dijkstra(start, end)
        distance = distances[end]
        path = []
        while 1:
            path.append(end)
            if end == start:
                break
            end = predecessors[end]
        path.reverse()
        logging.debug(f'shortest path: {path}')
        path_nodes = self.nodes.loc[path, :]
        return path_nodes, distance

    def dijkstra(self, start, end=None):
        distances, predecessors = {}, {}
        priority_dict = PriorityDict()
        priority_dict[start] = 0
        for v in priority_dict:
            distances[v] = priority_dict[v]
            if v == end:
                break
            for w in self.graph[v].neighbors:
                distance = distances[v] + self.graph[v].neighbors[w]
                if w in distances:
                    if distance < distances[w]:
                        raise ValueError("Dijkstra: found better path to already-final vertex")
                elif w not in priority_dict or distance < priority_dict[w]:
                    priority_dict[w] = distance
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
