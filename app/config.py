import logging
import os

LOG_LEVEL = logging.INFO

SRC_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = f'{SRC_PATH}/../.data'
CACHE_PATH = f'{SRC_PATH}/../.cache'
NODES_PATH = f'{CACHE_PATH}/nodes.pkl'
EDGES_PATH = f'{CACHE_PATH}/edges.pkl'
GRAPH_PATH = f'{CACHE_PATH}/graph.pkl'
INDEX_PATH = f'{CACHE_PATH}/index.pkl'

OVERPASS_PATH = f'{CACHE_PATH}/overpass-'

FORMAT = '%(asctime)s.%(msecs)03d %(levelname)5s %(process)d ---' \
         '[%(name)22s][%(lineno)4d] %(filename)-20s : %(message)s'
logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)
