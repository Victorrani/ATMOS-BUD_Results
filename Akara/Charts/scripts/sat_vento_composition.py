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
import matplotlib.colors as cm
from datetime import datetime
import pandas as pd

# Definindo diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/sat_vento/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRSAT = '/home/victor/USP/sat_goes/fig_dados/20240214_23/ch13/'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Paleta sem tons de cinza, ajustando as cores para temperaturas
palCO_new_adjusted = ["#FF0000", "#FFC0CB", "#ADD8E6", "#00008B", "#FFFF00", "#FFA500"]
cmapCO_new_adjusted = cm.LinearSegmentedColormap.from_list("IR_clean_adjusted", palCO_new_adjusted, N=20)

# Aplicando a paleta suave com 25 pontos (metade do original)
cmapCO_adjusted = cmapCO_new_adjusted(np.linspace(0, 1, 80))  # 25 divisões na paleta colorida

# Criando a paleta sem cinza com 120 pontos e adicionando as cores ajustadas
cmapPB_adjusted = cm.LinearSegmentedColormap.from_list("", ["white", "black"])
cmapPB_adjusted = cmapPB_adjusted(np.linspace(0, 1, 145))  # 120 divisões na paleta total
cmapPB_adjusted[:80, :] = cmapCO_adjusted  # Inserindo a paleta colorida nas primeiras 25 divisões

# Definindo o mapa de cores final sem tons de cinza
cmap_TbINPE_adjusted = cm.ListedColormap(cmapPB_adjusted)

# Carregar o arquivo NetCDF
ds_akara_slevel = xr.open_dataset(DIRDADO+'akara_reboita1.nc')
df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Lista das datas específicas
lista_datas = [2024021421, 2024021521, 2024021621, 2024021721, 2024021915, 2024022012]
letters = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']
lista_indice = [0, 8, 16, 24, 38, 45]

# Extraindo lat, lon
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
times = ds_akara_slevel['valid_time'].values
n_final = len(ds_akara_slevel['valid_time'])
X, Y = np.meshgrid(lon, lat)

# Lista dos arquivos NetCDF
arquivos_netCDF = sorted([f for f in os.listdir(DIRSAT) if f.endswith('.nc')])

# Criar a figura com 2 linhas e 3 colunas para os gráficos
fig, axs = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})
plt.subplots_adjust(hspace=0.4, wspace=0.4)

# Loop para gerar gráficos para as datas específicas
for idx, data_lista in enumerate(lista_datas):
    data_hora_formatada = str(data_lista)
    
    arquivo_encontrado = False
    
    # Verificar se o arquivo NetCDF corresponde à data
    for arquivo in arquivos_netCDF:
        data_arquivo = str(arquivo[10:20])
        if data_arquivo == data_hora_formatada:
            print(f"Arquivo correspondente encontrado: {arquivo}")
            arq_entrada = xr.open_dataset(DIRSAT + arquivo, engine='netcdf4')
            ch13 = arq_entrada.Band1
            ch13.data = ch13.data / 100 - 273.15  # Convertendo de Kelvin para Celsius

            # Identificar a posição do gráfico (2x3)
            ax = axs[idx // 3, idx % 3]

            # Configurar o gráfico
            ax.add_feature(cfeature.LAND, edgecolor='black')
            ax.add_feature(cfeature.COASTLINE, linewidth=2.0)  # Aumenta a grossura da linha de costa
            ax.add_feature(cfeature.BORDERS, linestyle=':')

            # Adicionando o shapefile dos estados
            shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
            ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

            # Plotando os dados do canal 13
            img = ch13.plot(
                ax=ax, cmap=cmap_TbINPE_adjusted, transform=ccrs.PlateCarree(), add_colorbar=False,
                  vmin=-90, vmax=55)
            u_1000 = ds_akara_slevel['u'].isel(valid_time=lista_indice[idx], pressure_level=0)
            v_1000 = ds_akara_slevel['v'].isel(valid_time=lista_indice[idx], pressure_level=0)

            sep = 6

# Plotar o campo de vento com barbelas
            ax.barbs(X[::sep,::sep], Y[::sep,::sep], u_1000[::sep,::sep], v_1000[::sep,::sep], 
            transform=ccrs.PlateCarree(), 
            barbcolor='white', flagcolor='white', flip_barb=True, length=4) 

            # Adicionar marcador de ponto
            lat_point = df2.loc[lista_indice[idx], 'Lat']
            lon_point = df2.loc[lista_indice[idx], 'Lon']
            ax.scatter(lon_point, lat_point, color='#50C878', marker='X', s=100, label="Center")

            # Ajustar limites do gráfico
            ax.set_extent([-60, -30, -40, -15], crs=ccrs.PlateCarree())

            # Linhas de grade
            gl = ax.gridlines()
            gl.bottom_labels = True
            gl.left_labels = True
            gl.xlabel_style = {'fontsize': 18}
            gl.ylabel_style = {'fontsize': 18}

            # Título
            ax.set_title(f"{letters[idx]} Akará GOES16 CH13\nWind 1000 hPa\n{data_arquivo}Z",
                          loc='left', fontsize=18)

            arquivo_encontrado = True
            break

    if not arquivo_encontrado:
        print(f"Nenhum arquivo encontrado para a data {data_hora_formatada}")

cbar_ax = fig.add_axes([0.80, 0.18, 0.02, 0.7])
cbar = fig.colorbar(img, cax=cbar_ax, orientation='vertical', shrink=0.8, aspect=20, pad=0.05)
cbar.set_label('Brightness Temperature (°C)', rotation=270, labelpad=20, fontsize=18)
ticks = np.arange(-90, 50, 15)
cbar.set_ticks(ticks)
cbar.ax.tick_params(labelsize=18)

plt.subplots_adjust(left=0.05, right=0.75, top=0.95, bottom=0.05, wspace=0.25, hspace=0.00)

# Salvar a figura final com todos os subgráficos
fig.savefig(f"{DIRFIG}composicao_2x3.png", dpi=300, bbox_inches='tight')
plt.close(fig)  # Fecha a figura após salvar

print("Composição 2x3 gerada com sucesso!")