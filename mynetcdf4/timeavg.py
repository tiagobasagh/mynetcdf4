import numpy as np

# WIP: Work in progress. 

def count_weeks(dts):
    """
    Funcion que devuelve el numero de semanas de mi periodo.
    Importante: Siempre el primero de enero comienza a contar las semanas, no importa como finalice diciembre.
    """
    aux_year = None
    aux_week = 0
    count_weeks = 0
    for i, t in enumerate(dts):
        if aux_year==t.year:
            if aux_week == 7:
                aux_week = 1
                count_weeks += 1
            else:
                aux_week += 1
        else:
            aux_year = t.year
            aux_week = 1
            count_weeks += 1
    return count_weeks


def daily_to_woy(var, dts):
    total_weeks = count_weeks(dts)
    
    new_var = np.zeros((total_weeks, var.shape[1], var.shape[2]))
    new_years = []
    new_weeks = []
    
    aux_year = None
    aux_month = None
    aux_days = 0

    for iw in range(total_weeks):
        aux_year = dts[aux_days].year
        aux_start_week = aux_days
        while ((aux_days < len(dts)) and (aux_year == dts[aux_days].year) and ((aux_days - aux_start_week) < 7)):
            aux_days += 1
        new_var[iw] = np.nanmean( var[aux_start_week:aux_days, :, :], axis=0)
        new_years.append(aux_year)
    return new_years, new_var


def daily_to_month(var, dts):
    total_months = (dts[-1].year - dts[0].year) * 12 + dts[-1].month
    new_var = np.zeros((total_months, var.shape[1], var.shape[2]))
    new_time = []
    
    aux_year = None
    aux_month = None
    aux_days = 0
    aux_start_month = 0
    
    for im in range(total_months):
        aux_year = dts[aux_days].year
        aux_month = dts[aux_days].month
        aux_start_month = aux_days
        while (aux_days < len(dts)) and (aux_month == dts[aux_days].month):
            aux_days += 1
        new_var[im] = np.nanmean( var[aux_start_month:aux_days, :, :], axis=0)
        new_time.append( dt.datetime(aux_year, aux_month, 1))
    return new_time, new_var