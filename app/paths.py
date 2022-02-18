from pathlib import Path

ROOT = Path(__file__).parent.parent

CACHE_PATH = ROOT / '.cache'
NODES_PATH = CACHE_PATH / 'nodes.pkl'
EDGES_PATH = CACHE_PATH / 'edges.pkl'
GRAPH_PATH = CACHE_PATH / 'graph.pkl'
INDEX_PATH = CACHE_PATH / 'index.pkl'
