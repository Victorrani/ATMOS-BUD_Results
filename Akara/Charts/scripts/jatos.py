import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy.io.shapereader as shpreader
import metpy.calc as mpcalc
from metpy.units import units

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/geo500/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'

# Abrir o dataset
ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_reboita.nc')

# Extraindo latitudes, longitudes e tempos
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
times = ds_akara_slevel['valid_time'].values
n_final = len(times)

# Loop para gerar o gráfico para cada tempo
for i in range(0, n_final):
    time = str(times[i])[:13]  # Formatando a data para o título
    
    # Extraindo componentes de vento para o nível de 250 hPa
    u250 = ds_akara_slevel['u'][:].isel(valid_time=i).sel(pressure_level=250)
    v250 = ds_akara_slevel['v'][:].isel(valid_time=i).sel(pressure_level=250)
    z500 = ds_akara_slevel['z'][:].isel(valid_time=i).sel(pressure_level=500)
    z500 = z500 / 100  # Convertendo de Pa para hPa
    
    # Calculando a intensidade do vento
    wind_speed = mpcalc.wind_speed(u250, v250)

    # Definindo o limite da área a ser exibida no mapa
    extent = [-60, -30, -40, -15]

    # Criando o gráfico
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # Adicionando as feições no mapa
    try:
        shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
        ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    except Exception as e:
        print(f"Erro ao carregar o shapefile: {e}")

    # Adicionando as fronteiras do mapa
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

    # Adicionando linhas de grade
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                      xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # Plotando o campo de intensidade do vento com contourf
    # Definindo o intervalo de intensidade do vento de 30 até 100
    levels_wind = np.arange(30, 95, 5)  # de 30 a 100 com incremento de 5
    contour_wind = ax.contourf(lon, lat, wind_speed, levels=levels_wind, cmap='twilight', extend='max')

    # Plotando o campo de altura geopotencial (z500) com contornos
    levels_z500 = np.arange(540, 595, 3)  # de 540 a 590 com incremento de 5
    contour_z500 = ax.contour(lon, lat, z500, levels=levels_z500, colors='red', linewidths=2)

    # Adicionando os valores dos contornos de z500
    ax.clabel(contour_z500, fmt='%d', fontsize=10, colors='black')

    # Adicionando uma barra de cores para o vento
    cbar = fig.colorbar(contour_wind, ax=ax, orientation='horizontal', pad=0.05)
    cbar.set_label('Wind Speed (m/s)')

    # Adicionando o título com a data formatada
    plt.title(f'AKARÁ reanalysis (ERA5) | {time}', loc='left')

    # Adicionando as costas do mapa
    ax.coastlines()

    # Salvando o gráfico
    try:
        plt.savefig(f'{DIRFIG}Akara_wind_speed_z500_{time}.png', dpi=300)
        plt.tight_layout()
    except Exception as e:
        print(f"Erro ao salvar a figura: {e}")
    
    # Fechando a figura
    plt.close()
