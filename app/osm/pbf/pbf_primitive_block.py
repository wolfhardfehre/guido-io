import numpy as np
from app.osm.pbf.osm_pb2 import PrimitiveBlock
from app.osm.pbf.pbf_utils import read_blob_data, decoded_string_table

MEMBER_TYPE = {
    0: 'node',
    1: 'way',
    2: 'relation'
}


class PdfPrimitiveBlock:

    def __init__(self, filename, blob_pos, blob_size):
        self.pos = filename, blob_pos, blob_size
        data = read_blob_data(filename, blob_pos, blob_size)
        primitive_block = PrimitiveBlock()
        primitive_block.ParseFromString(data)
        self.primitive_group = primitive_block.primitivegroup
        self._decoded = decoded_string_table(primitive_block.stringtable.s)
        self._granularity = primitive_block.granularity or 100
        self._lat_offset = primitive_block.lat_offset or 0
        self._lon_offset = primitive_block.lon_offset or 0

    def parse(self):
        for group in self.primitive_group:
            if group.nodes:
                yield self.nodes(group.nodes)
            elif group.dense.id:
                yield self.dense_nodes(group.dense)
            elif group.ways:
                yield self.ways(group.ways)

    @staticmethod
    def nodes(nodes):
        for node in nodes:
            yield 0, node.id, node.lon, node.lat

    def dense_nodes(self, nodes):
        current_id, current_lon, current_lat, tag_idx = 0, 0, 0, 0
        for node_id, lon, lat in zip(nodes.id, nodes.lon, nodes.lat):
            current_id += node_id
            current_lon += lon
            current_lat += lat
            tags, tag_idx = self._dense_tags(nodes, tag_idx)
            lat, lon = self._transform(current_lat, current_lon)
            yield 0, current_id, lon, lat

    def ways(self, ways):
        for way in ways:
            tags = self._tags(way)
            if 'highway' not in tags:
                continue
            highway = tags['highway']
            swap_nodes = 'oneway' in tags and tags['oneway'] == '-1'
            oneway = tags['oneway'] == 'yes' or swap_nodes if 'oneway' in tags else False
            access = tags['access'] if 'access' in tags else 'no'
            max_speed = tags['maxspeed'] if 'maxspeed' in tags else np.nan
            ref = 0
            previous = None
            for delta in way.refs:
                ref += delta
                if previous is not None:
                    if swap_nodes:
                        yield 1, ref, previous, highway, oneway, max_speed, access
                    else:
                        yield 1, previous, ref, highway, oneway, max_speed, access
                previous = ref

    def relations(self, relations):
        for relation in relations:
            yield 2, relation.id, self._tags(relation), self._members(relation)

    def _members(self, relation):
        members = []
        member_id = 0
        for rel_type, mid, role in zip(relation.types, relation.memids, relation.roles_sid):
            member_id += mid
            members.append((member_id, MEMBER_TYPE[rel_type], self._decoded[role]))
        return members

    def _tags(self, item):
        return {self._decoded[k]: self._decoded[v] for k, v in zip(item.keys, item.vals)}

    def _dense_tags(self, nodes, tag_idx):
        tags = {}
        if tag_idx < len(nodes.keys_vals):
            while nodes.keys_vals[tag_idx] != 0:
                k = nodes.keys_vals[tag_idx]
                v = nodes.keys_vals[tag_idx + 1]
                tag_idx += 2
                tags[self._decoded[k]] = self._decoded[v]
        tag_idx += 1
        return tags, tag_idx

    def _transform(self, lat, lon):
        lat = float(lat * self._granularity + self._lat_offset) / 1000000000
        lon = float(lon * self._granularity + self._lon_offset) / 1000000000
        return lat, lon
