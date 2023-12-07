import numpy as np

def extract_from_region(var, lat, lon, region):
    """
    extract values of a variable betweeen lat,lon coordenates.

    """
    def _order_minmax(point):
        if point[1] > point[0]:
            return point[0], point[1]
        else:
            return point[1], point[0]

    def get_index_limits(vardim, limits):
        return [np.abs(vardim - limit).argmin() for limit in limits]

    def reduce_dim(vardim, idxs):
        m, M =  _order_minmax(idxs)
        return vardim[m:M]

    def extract_var(var, lat_idxs, lon_idxs):
        lat_m, lat_M =  _order_minmax(lat_idxs)
        lon_m, lon_M =  _order_minmax(lon_idxs)
        return var[:, lat_m : lat_M, lon_m : lon_M]

    lat_idxs = get_index_limits(lat, region["lat"])
    lon_idxs = get_index_limits(lon, region["lon"])
    if type(var) == dict:
        _var = dict()
        for nvar, vvar in var.items():
            _var[nvar] = extract_var(vvar, lat_idxs, lon_idxs)
    else:
        _var = extract_var(var, lat_idxs, lon_idxs)

    return _var, reduce_dim(lat, lat_idxs), reduce_dim(lon, lon_idxs)
