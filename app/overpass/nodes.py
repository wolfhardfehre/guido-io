from app.overpass.overpass import Overpass
from app.overpass.location import Location


class Nodes(Overpass):
    TYPE = 'node'


if __name__ == '__main__':
    import pandas as pd
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    nodes = Nodes()
    nodes.location = Location(13.383333, 52.516667)
    nodes.radius = 4000
    nodes.selection = '["tourism"="attraction"]'
    nodes.sorted = True

    result = nodes.around()
    print(result)
