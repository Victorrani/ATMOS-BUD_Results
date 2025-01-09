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
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/geo500_jatos/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Abrir o dataset
ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_reboita1.nc')
df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Extraindo latitudes, longitudes e tempos
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
times = ds_akara_slevel['valid_time'].values
n_final = len(times)
lista_indice = [0, 8, 16, 24, 38, 45]
letters = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

# Definindo o limite da área a ser exibida no mapa
extent = [-60, -30, -40, -15]

# Criando a figura para a composição de gráficos (2 linhas, 3 colunas)
fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.flatten()  # Achatar a grade para facilitar iteração

# Iteração sobre os índices
for idx, i in enumerate(lista_indice):
    time = str(times[i])[:13]  # Formatando a data para o título
    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']

    # Extraindo componentes de vento para o nível de 250 hPa
    u250 = ds_akara_slevel['u'][:].isel(valid_time=i).sel(pressure_level=250)
    v250 = ds_akara_slevel['v'][:].isel(valid_time=i).sel(pressure_level=250)
    z500 = ds_akara_slevel['z'][:].isel(valid_time=i).sel(pressure_level=500)
    z500 = z500 / 100  # Convertendo de Pa para hPa
    
    # Calculando a intensidade do vento
    wind_speed = mpcalc.wind_speed(u250, v250)

    # Selecionando o eixo correspondente para o gráfico atual
    ax = axes[idx]

    # Adicionando as feições no mapa
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

    # Adicionando linhas de grade
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                      xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'fontsize': 18}  # Ajuste o tamanho da fonte no eixo X (longitude)
    gl.ylabel_style = {'fontsize': 18}

    # Plotando o campo de intensidade do vento com contourf
    levels_wind = np.arange(30, 95, 5)  # de 30 a 100 com incremento de 5
    contour_wind = ax.contourf(lon, lat, wind_speed, levels=levels_wind, cmap='twilight', extend='max')

    # Plotando o campo de altura geopotencial (z500) com contornos
    levels_z500 = np.arange(540, 595, 3)  # de 540 a 590 com incremento de 3
    contour_z500 = ax.contour(lon, lat, z500, levels=levels_z500, colors='red', linewidths=2)

    # Adicionando os valores dos contornos de z500
    ax.clabel(contour_z500, fmt='%d', fontsize=15, colors='black')

    # Adicionando a caixa com o 'X' no centro
    ax.scatter(lon_point, lat_point, color='black', marker='X', s=100, label="Center")
    lat_min = lat_point - 2.5
    lat_max = lat_point + 2.5
    lon_min = lon_point - 2.5
    lon_max = lon_point + 2.5

    # Criando um retângulo para a caixa
    ax.plot([lon_min, lon_max], [lat_min, lat_min], color='black', linewidth=2)  # Linha inferior
    ax.plot([lon_min, lon_max], [lat_max, lat_max], color='black', linewidth=2)  # Linha superior
    ax.plot([lon_min, lon_min], [lat_min, lat_max], color='black', linewidth=2)  # Linha esquerda
    ax.plot([lon_max, lon_max], [lat_min, lat_max], color='black', linewidth=2)  # Linha direita

    cbar_ax = fig.add_axes([0.95, 0.2, 0.02, 0.7])  # Ajuste o valor de 0.92 para 0.88
    cbar = fig.colorbar(contour_wind, cax=cbar_ax, extend='both')
    cbar.set_label('Wind Speed (m/s)', fontsize=18)
    cbar.ax.tick_params(labelsize=18)
    plt.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.1, wspace=0.2, hspace=-0.1)

    # Adicionando o título com a data formatada
    ax.set_title(f'{letters[idx]} {time[:-3]} {time[-2:]}Z', loc='left', fontsize=18)

    # Adicionando as costas do mapa
    ax.coastlines()

# Salvando a composição de gráficos
try:
  
    plt.savefig(f'{DIRFIG}Akara_wind_speed_z500_composition.png', dpi=300, bbox_inches='tight')
    print(f"Composição de figuras salva com sucesso em {DIRFIG}Akara_wind_speed_z500_composition.png")
except Exception as e:
    print(f"Erro ao salvar a composição de figuras: {e}")

# Fechando a figura
plt.close()
