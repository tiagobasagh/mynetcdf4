import os
import subprocess

from oceanpy.mydatasets import exist_or_create

#  cdo mergetime *.nc MARARG2001.nc

def cmd_reduce_netcdf4(nf1, nf2, lon1, lon2, lat1, lat2):
    return f"cdo sellonlatbox,{lon1},{lon2},{lat1},{lat2} {nf1} {nf2}"


def cmd_mergetime(dirncs, name_new_nc):
    return f"cdo mergetime {dirncs} {name_new_nc}"


def reduce_netcdf4(nf1, region, nf2=None):
    if nf2:
        cmd = cmd_reduce_netcdf4(nf1, nf2, min(region["lon"]), max(region["lon"]), min(region["lat"]), max(region["lat"]))
        subprocess.run(cmd, shell=True, check=True, text=True)
    else:
        pass


def multiple_reduce_netcdf4(region, ipath, npath=None, join=True,ignore_folders=[]):
    for nf in os.listdir(ipath):
        auxpath = os.path.join(ipath, nf)
        auxnewpath = os.path.join(npath, nf) if npath else auxpath
        if os.path.isfile(auxpath):
            reduce_netcdf4(auxpath, region, nf2=auxnewpath)
        elif os.path.isdir(auxpath) and nf not in ignore_folders:
            exist_or_create(auxnewpath)
            multiple_reduce_netcdf4(
                region, 
                auxpath, 
                npath=auxnewpath, 
                ignore_folders=ignore_folders
            )
            if join:
                pass