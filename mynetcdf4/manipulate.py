import netCDF4 as nc
import numpy as np

logerr = False


def netcdf_extract_var(nf, var, dims=["time", "lat", "lon"]):
    ds = nc.MFDataset(nf)
    variables = ds.variables.copy()
    vardims = [variables[d][:] for d in dims]
    v = variables[var][:]
    ds.close()
    return vardims, v


def netcdf_to_dict(
    ds, kvars=None, namedims={"time": "time", "lat": "lat", "lon": "lon"}
):
    if not kvars:
        kvars = ds.variables.keys()
    dictvar = dict()
    for varname in kvars:
        if varname not in namedims.values():
            if logerr:
                print(varname)
            dictvar[varname] = ds[varname][:]
    lat = ds[namedims["lat"]][:]
    lon = ds[namedims["lon"]][:]
    time = ds[namedims["time"]][:]

    return dictvar, time, lat, lon


def netcdf_add_values_from_dict(nf, variables, time, axis=0):
    """
    
    """
    ds = nc.Dataset(nf)
    var, t, _, _ = netcdf_to_dict(ds)
    time = np.append(time, t)
    for varname in variables.keys():
        variables[varname] = np.append(variables[varname], var[varname], axis=axis)
        if variables[varname].shape[axis] != time.shape[axis]:
            print("Warning:", 
                  varname,
                  "size dimension time is major to size of time.")
    ds.close()
    return variables, time


def netcdf_extract_multi(nfs, kvars=None):
    ds = nc.Dataset(nfs[0])
    variables, time, lat, lon = netcdf_to_dict(ds, kvars=kvars)
    for nf in nfs[1:]:
        variables, time = netcdf_add_values_from_dict(nf, variables, time)
    ds.close()
    
    return variables, time, lat, lon



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
