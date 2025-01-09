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

ds_akara_slevel = xr.open_dataset(DIRDADO+'akara_reboita1.nc')

df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

## extraindo lat, lon
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]

times = ds_akara_slevel['valid_time'].values
n_final = len(ds_akara_slevel['valid_time'])
X, Y = np.meshgrid(lon, lat)

pressure_levels = ds_akara_slevel['pressure_level'].values


arquivos_netCDF = sorted([f for f in os.listdir(DIRSAT) if f.endswith('.nc')])
for i in range(0, n_final):
    ## definindo string de data
    time_ds = str(times[i])[:13]
    
    print('Data do ds: '+time_ds)
    data_hora = datetime.strptime(time_ds, "%Y-%m-%dT%H")

    data_hora_formatada = str(data_hora.strftime("%Y%m%d%H"))

    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']
    data_point = df2.loc[i, 'time']

    print('Data formatada do ds: '+data_hora_formatada)
    for arquivo in arquivos_netCDF:
        data_arquivo = str(arquivo[10:20])
        if data_arquivo == data_hora_formatada:
            print(f'arquivo {data_arquivo} encontrad: {arquivo}')

            arq_entrada = xr.open_dataset(DIRSAT+arquivo, engine='netcdf4')
            
            print(f'Criando a imagem da data {data_arquivo}')

            print(f'data_point: {data_point}')

            ch13 = arq_entrada.Band1
            ch13.data = ch13.data / 100 - 273.15  # Convertendo de Kelvin para Celsius

            fig, ax = plt.subplots(figsize=(8, 7), subplot_kw={'projection': ccrs.PlateCarree()})
            
            ax.add_feature(cfeature.LAND, edgecolor='black')
            ax.add_feature(cfeature.COASTLINE, linewidth=2.0)  # Aumenta a grossura da linha de costa
            ax.add_feature(cfeature.BORDERS, linestyle=':')

            # Adicionando o shapefile dos estados
            shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
            ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)

            # Plotando os dados do canal 13
            img = ch13.plot(
    ax=ax, cmap=cmap_TbINPE_adjusted, transform=ccrs.PlateCarree(), vmin=-90, vmax=55,
    cbar_kwargs={
        "label": "Brightness Temperature (°C)", 
        "orientation": "vertical",  # Barra de cores vertical
        "pad": 0.05,                # Distância da barra para o gráfico
        "aspect": 20,               # Aumenta a espessura da barra de cores
        "shrink": 0.8,              # Aumenta a altura total da barra de cores
        "ticks": np.arange(-90, 60, 15),  # Personalizar os ticks
        "extend": 'neither'             # Aumenta o tamanho da fonte dos ticks
    }
)
            cbar = img.colorbar
            cbar.set_label("Brightness Temperature (°C)", fontsize=16)  # Aumenta o tamanho do rótulo principal
            cbar.ax.tick_params(labelsize=13)
            
            u_1000 = ds_akara_slevel['u'].isel(valid_time=i, pressure_level=0)
            v_1000 = ds_akara_slevel['v'].isel(valid_time=i, pressure_level=0)

            sep = 5

# Plotar o campo de vento com barbelas
            ax.barbs(X[::sep,::sep], Y[::sep,::sep], u_1000[::sep,::sep], v_1000[::sep,::sep], 
            transform=ccrs.PlateCarree(), 
            barbcolor='white', flagcolor='white', flip_barb=True, length=4) 

            ax.scatter(lon_point, lat_point, color='#50C878', marker='X', s=100, label="Center")

            # Ajustando os limites do gráfico para o intervalo desejado
            ax.set_extent([-60, -30, -40, -15], crs=ccrs.PlateCarree())
    
            # Linhas de grade
            gl = ax.gridlines()
            gl.bottom_labels = True
            gl.left_labels = True
            gl.xlabel_style = {'fontsize': 18}  # Ajuste o tamanho da fonte no eixo X (longitude)
            gl.ylabel_style = {'fontsize': 18}

            

            # Título
            plt.title(
    f"Akará GOES16 CH13\nWind 1000 hPa - {data_arquivo}Z", 
    loc='left', 
    fontsize=18  # Altere para o tamanho desejado
) 
            file_name = f"ch13_AKARA_vento{data_arquivo}.png"
            plt.savefig(os.path.join(DIRFIG, file_name), dpi=300, bbox_inches='tight')
            plt.close(fig)

            break

        else:
            print('')