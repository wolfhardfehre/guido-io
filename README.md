# guido-io

Guido-Io is a prototype for route and tour optimisation. The goal is to create an API 
endpoint that returns points of interest (POI) within close proximity to each other and 
an optimal tour connecting these locations. POIs are defined by a specific topic.

Imagine you visit a new city and you are interested in historical monuments. As a user
you provide your starting point and the amount of monuments you want to visit. The endpoints 
returns a list with specified number of historical places including the shortest path/tour.

## Setup

1) Install python packages

```Bash
pipenv install
```

2) [OPTIONAL] Install jupyter lab extensions

```Bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager 
jupyter labextension install jupyter-leaflet
```

## Usage

1) Load OSM data to build the routing graph

Option A: Load data from Overpass: `python3 app/routing/graph_builder.py`

Option B: Load data from OSM-PBF: `python3 app/osm/pbf_parser.py`

>> You need to download an OSM pbf file first, e.g. from [GEOFABRIK](https://download.geofabrik.de/)

2) Run
