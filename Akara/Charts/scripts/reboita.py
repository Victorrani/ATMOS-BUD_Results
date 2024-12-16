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
import matplotlib.patches as mpatches


DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/reboita_caixas/'

df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

print(df.head())

ds_akara = xr.open_dataset(DIRDADO+'akara_reboita1.nc')

lon = ds_akara['longitude'][:]
lat = ds_akara['latitude'][:]

times = ds_akara['valid_time'].values
n_final = len(ds_akara['valid_time'])
extent = [-60, -20, -40, -15]


box_lat_size_grande = 2.0  # 1 grau para cima e para baixo (total 2 graus na latitude)
box_lon_size_grande = 30.0  # 15 graus para leste e oeste (total 30 graus na longitude)
box_lat_size_pequeno = 2.0  # 1 grau para cima e para baixo (total 2 graus na latitude)
box_lon_size_pequeno = 10  # 15 graus para leste e oeste (total 10 graus na longitude)

for i in range(0, n_final):
    # Definindo string de data
    time = str(times[i])[:13]
    
    # Pegando informações do DataFrame
    tempo = df.loc[i, 'time']
    lat = df.loc[i, 'Lat']
    lon = df.loc[i, 'Lon']

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

    # Coordenadas do canto inferior esquerdo da caixa
    lower_left_lon_grande = lon - box_lon_size_grande / 2
    lower_left_lat_grande = lat - box_lat_size_grande / 2

    lower_left_lon_pequeno = lon - box_lon_size_pequeno / 2
    lower_left_lat_pequeno = lat - box_lat_size_pequeno / 2

    # Adicionando a caixa ao mapa
    rect1 = mpatches.Rectangle(
        (lower_left_lon_grande, lower_left_lat_grande),  # Coordenadas do canto inferior esquerdo
        box_lon_size_grande,  # Largura da caixa (longitude)
        box_lat_size_grande,  # Altura da caixa (latitude)
        linewidth=1.5,
        edgecolor='red',
        facecolor='none',
        transform=ccrs.PlateCarree()  # Transforma para coordenadas geográficas
    )
    ax.add_patch(rect1)
    rect2 = mpatches.Rectangle(
        (lower_left_lon_pequeno, lower_left_lat_pequeno),  # Coordenadas do canto inferior esquerdo
        box_lon_size_pequeno,  # Largura da caixa (longitude)
        box_lat_size_pequeno,  # Altura da caixa (latitude)
        linewidth=1.5,
        edgecolor='blue',
        facecolor='none',
        transform=ccrs.PlateCarree()  # Transforma para coordenadas geográficas
    )
    ax.add_patch(rect2)

    # Adicionando um 'x' no ponto central (lat, lon)
    ax.plot(lon, lat, marker='x', color='red', markersize=10, linewidth=2, transform=ccrs.PlateCarree())

    # Configuração das linhas de grade
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black',
                      alpha=1.0, linestyle='--', linewidth=0.25,
                      xlocs=np.arange(-180, 180, 5),
                      ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # Adicionando título para verificar o tempo
    ax.set_title(f"Tempo: {time} - Lat: {lat:.2f}, Lon: {lon:.2f}")
    
    # Salvando figura ou exibindo
    plt.savefig(f"{DIRFIG}akara_caixas__{i:03d}.png", dpi=300)
    plt.close(fig)
