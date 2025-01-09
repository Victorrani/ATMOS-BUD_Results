import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy, cartopy.crs as ccrs
import matplotlib.colors as mcolors
import matplotlib.colors
import metpy.calc as mpcalc
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import cartopy.io.shapereader as shpreader
import numpy as np


DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/sst/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'


colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", "#ab1900", "#6b0200"]
dif_sstt2m = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
dif_sstt2m.set_over('#3c0000')
dif_sstt2m.set_under('#28000a')


ds_akara_slevel = xr.open_dataset(DIRDADO+'akara_maps.nc')
## extraindo lat, lon
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
sst = ds_akara_slevel['sst'][:]
sst = sst - 273
media_sst = sst.mean().values

## extraindo tempo
times = ds_akara_slevel['valid_time'].values
n_final = len(ds_akara_slevel['valid_time'])

for i in range(0, n_final):
    ## definindo string de data
    time = str(times[i])[:13]
    ## extraindo msl
    msl = ds_akara_slevel['msl'][:].isel(valid_time=i)
    msl = msl / 100
    ## sst e t2m
    sst = ds_akara_slevel['sst'][:].isel(valid_time=i)
    sst = sst - 273
    
    extent = [-47.5, -35, -35, -17.5]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)
    interval=0.5
    ## plot dfi_temp
    img1 = ax.contourf(lon, lat, sst,np.arange(22, 30, interval), cmap=dif_sstt2m, extend='both')
    cbar = plt.colorbar(img1, ax=ax, aspect=15, extend='both')
    cbar.set_label('SST (°C)', rotation=270, labelpad=20, fontsize=18)
    ticks = np.arange(22, 30, interval)
    cbar.set_ticks(ticks)
    cbar.ax.tick_params(labelsize=18)
  
    ticks = np.arange(22, 30, 1)
    cbar.set_ticks(ticks)
    ### plot mslp
    data_min_mslp = 980
    data_max_mslp = 1030
    interval_mslp = 2
    levels_mslp = np.arange(data_min_mslp, data_max_mslp, interval_mslp)
    levels2_mslp = np.arange(data_min_mslp ,data_max_mslp, 3)

    ct1 = ax.contour(lon, lat, msl, linewidths=1, levels=levels_mslp, colors='lightgrey')
    ct2 = ax.contour(lon, lat, msl, linewidths=1, levels=levels2_mslp, colors='lightgrey')
    ax.clabel(ct2, inline=1, inline_spacing=0, fontsize='12',fmt = '%1.0f', colors= 'lightgrey')
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black',
                 alpha=1.0, linestyle='--', linewidth=0.25,
                xlocs=np.arange(-180, 180, 5),
                  ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 18}  # Aumenta o tamanho da fonte dos rótulos do eixo X
    gl.ylabel_style = {'size': 18}
    plt.title(f'{time}', loc='left', fontsize=18)
    ax.coastlines()
    plt.savefig(f'{DIRFIG}Akara_mslp_sst_{time}.png', bbox_inches='tight', dpi=300)

    plt.tight_layout()
    plt.close()