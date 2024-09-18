import xarray as xr

def expand_dims(ds, dim="time", var="SSS", extravars=["eSSS"], dropvars=["timebounds"]):
    expanded = dict()
    expanded[var] = ds[var].expand_dims(dim) # create_index_for_new_dim=create_index_for_new_dim)
    if extravars:
        exp = {}
        for evar in extravars:
            expanded[evar] = ds[evar].expand_dims(dim)
            ds = ds.drop(evar)

    if dropvars:
        for dv in dropvars:
            ds = ds.drop(dv)

    ds = ds.drop(var)
    nds = ds.assign(expanded)
    return nds