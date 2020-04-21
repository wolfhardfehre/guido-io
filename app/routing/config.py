import logging

LOG_LEVEL = logging.DEBUG

DATA_PATH = '.data'
CACHE_PATH = '.cache'
NODES_PATH = f'{CACHE_PATH}/nodes.pkl'
EDGES_PATH = f'{CACHE_PATH}/edges.pkl'
GRAPH_PATH = f'{CACHE_PATH}/graph.pkl'

FORMAT = '%(asctime)s.%(msecs)03d %(levelname)5s %(process)d --- [%(name)22s][%(lineno)d] %(filename)-20s : %(message)s'
logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)
