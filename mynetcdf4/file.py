import netCDF4 as nc
import numpy as np

from manipulate import extract_from_region, netcdf_to_dict

logerr = False

def netcdf_del_attrs(ds):
    """
    Funcion que elimina los atributos de un dado Objet.netCDF4.Dataset
    """
    attrs = ds.__dict__.keys()
    for attr in attrs:
        delattr(ds, attr)
    return ds


def netcdf_copy_attr(ds, newds, tocattr=None):
    """
    Funcion qeu copia los attributos de un dado 
    Objet.netCDDF4.Dataser a otro objeto similar.
    """
    newds = netcdf_del_attrs(newds)
    if not tocattr:
        for attr, value in ds.__dict__.items():
            newds.setncattr(attr, value)
    else:
        for attr in tocattr:
            newds.setncattr(attr, ds.getncattr(attr))
    return newds


def netcdf_reshape_dims(newds, ds, newshapes):
    """
    Funcion que copia las dimensiones de otro netCDF4 modificando las dimensiones.
    [Esta funcion deberia cambiarse seguramente]
    """
    for dim, info in ds.dimensions.items():
        if info.isunlimited():
            newds.createDimension(dim)
        else:
            newds.createDimension(dim, newshapes[dim])
    return newds


def netcdf_new_variables_from_dict(newds, variables, dims):
    """
    Funcion que crea variables para un .nc dado un diccionarioa
    """
    ds_var = dict()
    for varname, info in variables.items():
        if logerr:
            print(varname)
        if varname in dims:
            mytype = type(info["data"].data[0])
            ds_var[varname] = newds.createVariable(
                varname, mytype, (varname,)
            )
        else:
            mytype = type(info["data"].data[0,0, 0])
            ds_var[varname] = newds.createVariable(
                varname, mytype, dims
            )
            ds_var[varname].setncatts({"_FillValue": mytype(info["_FillValue"])})
        ds_var[varname][:] = info["data"]
        for ninfo in info.keys():
            if ninfo not in ["data", "datatype", "_FillValue"]:
                ds_var[varname].setncatts({ninfo: info[ninfo]})
    return newds


def new_netcdf(filedir, metadata, variables, dimensiones):
    pass

def netcdf_reduct_to_a_region(
    ds,
    newds,
    region,
    namedims={"time": "time", "lat": "lat", "lon": "lon"},
    tocattr=None,
    kvars=None,
):
    """
    
    """
    def _add_info_variables(ds, newdictvar, kvars):
        variables = dict()
        for varname in kvars:
            if logerr:
                print(varname)
            cats = ds.variables[varname].ncattrs()
            _dict = {cat: ds.variables[varname].getncattr(cat) for cat in cats}
            _dict["datatype"] = ds.variables[varname].datatype.type
            _dict["data"] = newdictvar[varname]
            variables[varname] = _dict
        return variables

    if not kvars:
        kvars = ds.variables.keys()
    # cargo ds original
    dictvar, time, lat, lon = netcdf_to_dict(ds, kvars, namedims=namedims)

    # extraigo la region
    newdictvar, newlat, newlon = extract_from_region(dictvar, lat, lon, region)
    newdictvar[namedims["lat"]] = newlat
    newdictvar[namedims["lon"]] = newlon
    newdictvar[namedims["time"]] = time

    # copio atributos
    newds = netcdf_copy_attr(ds, newds, tocattr=tocattr)

    # copio y redefino tamano dimensioens 
    newshapes = {namedims["lat"]: newlat.shape[0],
                 namedims["lon"]: newlon.shape[0]}
    
    newds = netcdf_reshape_dims(newds, ds, newshapes)

    # creo nuevas  variables
    dims = tuple(ds.dimensions.keys())
    variables = _add_info_variables(ds, newdictvar, kvars)
    newds = netcdf_new_variables_from_dict(newds, variables, dims)

    return newds

