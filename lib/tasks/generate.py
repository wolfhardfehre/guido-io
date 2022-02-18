from invoke import task


@task
def osm_pb2(c):
    """Generates a new osm_pb2.py file to parse the osm protocol buffer format"""
    c.run('protoc --python_out="./app/osm/pbf" osm.proto')
