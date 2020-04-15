from app.overpass.overpass import Overpass
from app.overpass.location import Location


class Ways(Overpass):
    TYPE = 'way'


if __name__ == '__main__':
    import pandas as pd
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    ways = Ways()
    ways.location = Location(13.383333, 52.516667)
    ways.selection = '["highway"]'
    ways.sorted = True

    result = ways.around()
    print(result)
