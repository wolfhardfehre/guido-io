import logging

LOG_LEVEL = logging.INFO

CACHE_PATH = '.cache'
NODES_PATH = f'{CACHE_PATH}/nodes.pkl'
EDGES_PATH = f'{CACHE_PATH}/edges.pkl'
GRAPH_PATH = f'{CACHE_PATH}/graph.pkl'


logging.basicConfig(
    level=LOG_LEVEL,
    format='[%(levelname)5s] - %(asctime)s.%(msecs)03d - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
