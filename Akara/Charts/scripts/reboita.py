import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors
import metpy.calc as mpcalc
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
import cartopy.io.shapereader as shpreader
import pandas as pd
import matplotlib.patches as mpatches
from shapely.geometry import box
import geopandas as gpd
from rasterio.features import geometry_mask

# Diretórios
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/World_Continents.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/reboita_caixas/'

# Leitura do arquivo de rastreamento
df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Imprime as primeiras linhas do DataFrame
print(df.head())

# Carregando o dataset Akara
ds_akara = xr.open_dataset(DIRDADO+'akara_reboita1.nc')
shapefile = gpd.read_file(DIRSHAPE)
shapefile = shapefile.to_crs("EPSG:4326")  # Converte o shapefile para o CRS correto
lon_ = ds_akara['longitude'][:]
lat_ = ds_akara['latitude'][:]

# Exibe o tempo do dataset
print(ds_akara['valid_time'].values)

# Obtenção dos tempos e definição do extent do gráfico
times = ds_akara['valid_time'].values
n_final = len(ds_akara['valid_time'])
extent = [-60, -20, -40, -15]  # Extensão do mapa (lon_min, lon_max, lat_min, lat_max)

# Definição do tamanho das caixas
box_lat_size_grande = 2.0  # 1 grau para cima e para baixo (total 2 graus na latitude)
box_lon_size_grande = 30.0  # 15 graus para leste e oeste (total 30 graus na longitude)

# Máscara do shapefile (continentes)
mask = geometry_mask(
    geometries=shapefile.geometry,
    transform=ds_akara.rio.transform(),  # Transforma o dataset para o CRS correto
    invert=True,
    out_shape=(ds_akara.sizes["latitude"], ds_akara.sizes["longitude"])
)

mask = xr.DataArray(mask, dims=["latitude", "longitude"], coords={
    "latitude": ds_akara["latitude"].values,
    "longitude": ds_akara["longitude"].values
})

# Loop para cada tempo no dataset
for i in range(0, n_final):
    # Definindo string de data
    time = str(times[i])[:13]
    
    # Pegando informações do DataFrame
    tempo = df.loc[i, 'time']
    lat = df.loc[i, 'Lat']
    lon = df.loc[i, 'Lon']

    # Pegando a temperatura do dataset
    temp = ds_akara['t'][:].sel(valid_time=times[i], pressure_level=1000)

    # Calculando as coordenadas das caixas
    lower_left_lon_grande = lon - box_lon_size_grande / 2
    lower_left_lat_grande = lat - box_lat_size_grande / 2
    upper_right_lon_grande = lon + box_lon_size_grande / 2
    upper_right_lat_grande = lat + box_lat_size_grande / 2

    # Máscara para dentro da caixa maior
    mask_caixa_maior = (lon_ >= lower_left_lon_grande) & (lon_ <= upper_right_lon_grande) & \
                       (lat_ >= lower_left_lat_grande) & (lat_ <= upper_right_lat_grande)

    # Aplicando a máscara da caixa maior para os dados de temperatura
    temp_caixa_maior = temp.where(mask_caixa_maior)

    # **Filtro para pegar apenas os dados sobre o oceano**
    temp_caixa_maior_somente_oceano = temp_caixa_maior.where(mask == 0)  # 1 significa oceano (invertido)

    # Criação do gráfico
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

    # Adicionando a caixa maior ao mapa
    rect1 = mpatches.Rectangle(
        (lower_left_lon_grande, lower_left_lat_grande), 
        box_lon_size_grande, 
        box_lat_size_grande, 
        linewidth=1.5,
        edgecolor='red',
        facecolor='none',
        transform=ccrs.PlateCarree()
    )
    ax.add_patch(rect1)

    # Adicionando o ponto central (lat, lon)
    ax.plot(lon, lat, marker='x', color='red', markersize=10, linewidth=2, transform=ccrs.PlateCarree())

    # Configuração das linhas de grade
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black',
                      alpha=1.0, linestyle='--', linewidth=0.25,
                      xlocs=np.arange(-180, 180, 5),
                      ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # Plotando os dados filtrados sobre o oceano
    contour = ax.contourf(lon_, lat_, temp_caixa_maior_somente_oceano, cmap='coolwarm', transform=ccrs.PlateCarree())

    # Adicionando título para verificar o tempo
    ax.set_title(f"Tempo: {time} - Lat: {lat:.2f}, Lon: {lon:.2f}")
    
    # Adicionando barra de cores
    plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.7)

    # Salvando figura ou exibindo
    plt.savefig(f"{DIRFIG}akara_caixas_oceano_{i:03d}.png", dpi=300)
    plt.close(fig)
