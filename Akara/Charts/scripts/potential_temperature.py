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
import pandas as pd

DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/cross_sections/potential_temperature/'
# Lendo o arquivo com separador por espaço(s)

df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

ds_akara = xr.open_dataset(DIRDADO+'akara_maps.nc')

lat_ = ds_akara['latitude'][:]
lon_ = ds_akara['longitude'][:]

times = ds_akara['valid_time'].values
for i in range(len(df)):
    time = str(times[i])[:13]
    tempo = df.loc[i, 'time']
    lat = df.loc[i, 'Lat']
    lon = df.loc[i, 'Lon']

    mslp = ds_akara['msl'].isel(valid_time=i) / 100  # Converte para hPa

    # Cross-section
    ds_akara_tempo = ds_akara.isel(valid_time=i)
    data = ds_akara_tempo.metpy.parse_cf().squeeze()
    start = (lat, lon - 2)
    end = (lat, lon + 2)
    cross = cross_section(data, start, end).set_coords(('latitude', 'longitude'))
    cross['Potential_temperature'] = mpcalc.potential_temperature(
        cross['pressure_level'], cross['t'])

    # Criação da figura
    fig, ax = plt.subplots(figsize=(16, 9))
    extent = [-47.5, -35, -35, -17.5]

    # Minimap
    minimapa = fig.add_axes([0.037, 0.58, 0.3, 0.3], projection=ccrs.PlateCarree())
    minimapa.set_extent(extent, crs=ccrs.PlateCarree())
    minimapa.set_xticks([])
    minimapa.set_yticks([])
    minimapa.add_feature(cfeature.COASTLINE)
    minimapa.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
    minimapa.add_feature(cfeature.LAND, facecolor="lightgrey", zorder=2)
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    minimapa.add_geometries(
        shapefile, ccrs.PlateCarree(), edgecolor="black", facecolor="none", linewidth=0.3, zorder=3
    )

    # Contorno no minimapa
    contour = minimapa.contour(
        lon_, lat_, mslp, levels=np.arange(980, 1020, 2), colors="black", linewidths=2, zorder=1
    )
    ax.clabel(contour, inline=1, inline_spacing=0, fontsize="10", fmt="%1.0f", colors="black", zorder=1)

    # Pontos do cross-section
    transform = ccrs.Geodetic()._as_mpl_transform(minimapa)
    endpoints = transform.transform(np.vstack([start, end]))
    minimapa.scatter(endpoints[:, 0], endpoints[:, 1], c="black", zorder=2)
    minimapa.plot([start[1], end[1]], [start[0], end[0]], c="black", zorder=2)

    # Contornos de temperatura potencial
    theta_contour = ax.contour(
        cross["longitude"], cross["pressure_level"], cross["Potential_temperature"],
        levels=np.arange(300, 358, 5), colors="black", linewidths=0.5
    )
    ax.clabel(theta_contour, fmt="%1.0f", inline=True, fontsize=8)

    # Configuração dos eixos
    ax.set_title(
        f"Akara Cross Section {time} Latitude:{lat:.2f} Central Longitude:{lon:.2f}\nPotential Temperature (K)",
        loc="left",
    )
    ax.set_ylabel("Pressure (hPa)")
    ax.set_xlabel("Longitude (degrees east)")
    ax.set_yscale("symlog")
    ax.set_ylim(1000, 200)
    ax.set_yticks(np.arange(1000, 250, -100))
    ax.set_yticklabels(np.arange(1000, 250, -100))


    # Salva e fecha a figura
    plt.savefig(f"{DIRFIG}Akara_cross_{time}.png", dpi=300)
    plt.close(fig)  # Fecha a figura no final de cada iteração
