import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.colors as mcolors
import pandas as pd

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/sst/'
DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRCSV2 = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Cores para o mapa
colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", "#ab1900", "#6b0200"]
dif_sstt2m = mcolors.LinearSegmentedColormap.from_list("", colors)
dif_sstt2m.set_over('#3c0000')
dif_sstt2m.set_under('#28000a')

df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Abrindo os dados
ds_akara_slevel = xr.open_dataset(DIRDADO + 'akara_maps.nc')
lat = ds_akara_slevel['latitude'][:]
lon = ds_akara_slevel['longitude'][:]
times = ds_akara_slevel['valid_time'].values
lista_indice = [0, 8, 16, 24, 38, 45]
letters = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

# Configuração da figura com 2 linhas e 3 colunas
fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.flatten()  # Achatar a grade para facilitar iteração

extent = [-47.5, -35, -35, -17.5]

# Iteração sobre os índices
for idx, i in enumerate(lista_indice):
    ax = axes[idx]  # Seleciona o eixo correspondente
    time = str(times[i])[:13]
    lat_point = df2.loc[i, 'Lat']
    lon_point = df2.loc[i, 'Lon']

    # Dados do SST e MSL
    sst = ds_akara_slevel['sst'][:].isel(valid_time=i) - 273
    msl = ds_akara_slevel['msl'][:].isel(valid_time=i) / 100

    # Configurações do mapa
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    shapefile = list(shpreader.Reader(DIRSHAPE).geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)

    # Contorno do SST
    interval = 0.5
    img1 = ax.contourf(lon, lat, sst, levels=np.arange(22, 30, interval), cmap=dif_sstt2m, extend='both')

    # Contorno do MSL
    levels_mslp = np.arange(980, 1030, 2)
    levels2_mslp = np.arange(980, 1030, 2)
    #ct1 = ax.contour(lon, lat, msl, linewidths=1.0, levels=levels_mslp, colors='lightgrey')
    ct2 = ax.contour(lon, lat, msl, linewidths=1.5, levels=levels2_mslp, colors='lightgrey')
    ax.clabel(ct2, inline=1, inline_spacing=0, fontsize='13', fmt='%1.0f', colors='lightgrey')

    ax.scatter(lon_point, lat_point, color='black', marker='X', s=100, label="Center")
    lat_min = lat_point - 2.5
    lat_max = lat_point + 2.5
    lon_min = lon_point - 2.5
    lon_max = lon_point + 2.5

    # Criando um retângulo para a caixa
    #ax.plot([lon_min, lon_max], [lat_min, lat_min], color='black', linewidth=2)  # Linha inferior
    #ax.plot([lon_min, lon_max], [lat_max, lat_max], color='black', linewidth=2)  # Linha superior
    #ax.plot([lon_min, lon_min], [lat_min, lat_max], color='black', linewidth=2)  # Linha esquerda
    #ax.plot([lon_max, lon_max], [lat_min, lat_max], color='black', linewidth=2)  # Linha direita

    # Adicionar grade e título
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                      xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 18}
    gl.ylabel_style = {'size': 18}
    ax.set_title(f'{letters[idx]} {time[:-3]} {time[-2:]}Z', fontsize=18, loc='left')

# Adicionar barra de cores
cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])  # Ajuste o valor de 0.92 para 0.88
cbar = fig.colorbar(img1, cax=cbar_ax, extend='both')
cbar.set_label('SST (°C)', fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.subplots_adjust(left=0.05, right=0.9, top=0.95, bottom=0.1, wspace=0.0, hspace=0.2)


plt.savefig(f'{DIRFIG}Akara_mslp_sst_multiplot.png', dpi=300, bbox_inches='tight')

