import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy.io.shapereader as shpreader
import metpy.calc as mpcalc
from metpy.units import units
import pandas as pd

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/geo500/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Abrir o dataset
ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_reboita1.nc')
df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

print(ds_akara_slevel)

quit()
# Extraindo latitudes, longitudes e tempos
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
times = ds_akara_slevel['valid_time'].values
n_final = len(times)

# Loop para gerar o gráfico para cada tempo
for i in range(0, n_final):
    time = str(times[i])[:13]  # Formatando a data para o título
    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']
    
    
    