from app.overpass.overpass import Overpass
from app.overpass.location import Location


class Relations(Overpass):
    TYPE = 'rel'


if __name__ == '__main__':
    import pandas as pd
    pd.options.display.max_columns = None
    pd.options.display.width = 800

    relations = Relations()
    relations.location = Location(13.425034, 52.480689)
    relations.radius = 100
    relations.selection = '[type=route]'
    relations.sorted = True

    result = relations.around()
    print(result)
