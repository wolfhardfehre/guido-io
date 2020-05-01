import numpy as np


def meters(from_lat, from_lon, to_lat, to_lon):
    from_lat_rad = np.radians(from_lat)
    to_lat_rad = np.radians(to_lat)
    delta = np.radians(to_lon - from_lon)
    func = np.sin(from_lat_rad) * np.sin(to_lat_rad) + np.cos(from_lat_rad) * np.cos(to_lat_rad) * np.cos(delta)
    func = func.where(func <= 1.0, 1.0)
    angle = np.arccos(func)
    return angle * 6371e3


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame({
        'lat': [0.0, 0.0],
        'lon': [0.0, 0.0],
        'lat_to': [0.0, 0.0],
        'lon_to': [0.00001, 180.0],
    })
    result = meters(df['lat'], df['lon'], df['lat_to'], df['lon_to'])
    print(result)
