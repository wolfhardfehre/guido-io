class Node:
    def __init__(self, node_id, lat, lng):
        self.node_id = node_id
        self.latitude = lat
        self.longitude = lng
        self.neighbors = {}

    def add_neighbor(self, node_id, distance):
        self.neighbors[node_id] = distance

    def __repr__(self):
        return f'Node[id={self.node_id}, latLng=({self.latitude} {self.longitude}), neighbors={self.neighbors}]'
