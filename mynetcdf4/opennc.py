import netCDF4 as nc
import numpy as np

logerr = False


def extract_var(nf, var, dims=["time", "lat", "lon"]):
    """
    
    """
    ds = nc.MFDataset(nf)
    variables = ds.variables.copy()
    vardims = [variables[d][:] for d in dims]
    v = variables[var][:]
    ds.close()
    return vardims, v


def as_dict(
    ds, kvars=None, namedims={"time": "time", "lat": "lat", "lon": "lon"}
):
    """
    
    """
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


def _add_values_from_dict(nf, variables, time, axis=0):
    """
    
    """
    ds = nc.Dataset(nf)
    var, t, _, _ = as_dict(ds)
    time = np.append(time, t)
    for varname in variables.keys():
        variables[varname] = np.append(variables[varname], var[varname], axis=axis)
        if variables[varname].shape[axis] != time.shape[axis]:
            print("Warning:", 
                  varname,
                  "size dimension time is major to size of time.")
    ds.close()
    return variables, time


def multiple_files(nfs, kvars=None):
    ds = nc.Dataset(nfs[0])
    variables, time, lat, lon = as_dict(ds, kvars=kvars)
    for nf in nfs[1:]:
        variables, time = _add_values_from_dict(nf, variables, time)
    ds.close()
    
    return variables, time, lat, lon
