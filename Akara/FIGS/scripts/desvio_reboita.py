import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import scipy.ndimage
import matplotlib.dates as mdates 
import geopandas as gpd
from rasterio.features import geometry_mask
import rioxarray


DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/cross_sections/hov/'


# Abrindo os dados
df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])
ds_akara = xr.open_dataset(DIRDADO+'akara_reboita1.nc')

shapefile = gpd.read_file(DIRSHAPE)
shapefile = shapefile.to_crs("EPSG:4326")

# Pegando os tempos e os níveis de pressão
times = ds_akara['valid_time'].values
pressure_levels = ds_akara['pressure_level'].values

# Criando a máscara com o shapefile e ajustando a forma para coincidir com os dados
mask = geometry_mask(
    geometries=shapefile.geometry,
    transform=ds_akara.rio.transform(),  # Transforma o dataset para o CRS correto
    invert=True,
    out_shape=(ds_akara.sizes["latitude"], ds_akara.sizes["longitude"])
)

# Agora, para garantir que a máscara tenha a mesma forma que os dados de temperatura, podemos reamostrárla
# Ajustando a máscara para a resolução do dataset de temperatura
mask = xr.DataArray(mask, dims=["latitude", "longitude"], coords={
    "latitude": ds_akara["latitude"].values,
    "longitude": ds_akara["longitude"].values
})

# Loop para processar cada tempo
for i in range(0, len(df), 2):
    time = str(times[i])[:13]  # Exibindo até horas
    lat_center = df.loc[i, 'Lat']
    lon_center = df.loc[i, 'Lon']

    # Definindo os limites das caixas
    lat_min_grande = lat_center - 1
    lat_max_grande = lat_center + 1
    lon_min_grande = lon_center - 15
    lon_max_grande = lon_center + 15

    lat_min_peq = lat_center - 1
    lat_max_peq = lat_center + 1
    lon_min_peq = lon_center - 5
    lon_max_peq = lon_center + 5

    # Selecionando os dados dentro das caixas e para o tempo
    temp_box_grande = ds_akara['t'].sel(
        latitude=slice(lat_max_grande, lat_min_grande),
        longitude=slice(lon_min_grande, lon_max_grande),
        valid_time=times[i]
    )

    # Aplicando a máscara para excluir os dados dentro do continente
    temp_box_grande_masked = temp_box_grande.where(mask)

    # Selecionando o intervalo de dados menor
    temp_box_pequena = ds_akara['t'].sel(
        latitude=slice(lat_max_peq, lat_min_peq),
        longitude=slice(lon_min_peq, lon_max_peq),
        valid_time=times[i]
    )

    # Calculando a temperatura média (garantindo que a média é feita sobre latitude e longitude)
    mean_temp_grande = temp_box_grande_masked.mean(dim=['latitude', 'longitude']).values
    mean_temp_pequena = temp_box_pequena.mean(dim=['latitude', 'longitude']).values
    mean_temp_reboita = mean_temp_pequena - mean_temp_grande

    # Salvando os resultados na lista para cada nível de pressão
    for pressure_level, theta_mean in zip(pressure_levels, mean_temp_reboita):
        zonal_deviation_results.append({
            'time': time,
            'pressure_level': pressure_level,
            'theta_zonal_mean': theta_mean  # Salvando o valor da média de desvio zonal de temperatura
        })

# Criando DataFrame para os resultados de desvio zonal
df_results = pd.DataFrame(zonal_deviation_results)

# Pivotando o DataFrame para colocar 'time' como índice e 'pressure_level' como colunas
df_pivot = df_results.pivot(index='pressure_level', columns='time', values='theta_zonal_mean')
df_pivoted = df_pivot.sort_index(ascending=False)

# Exibindo as primeiras linhas para verificar o formato
print(df_pivoted.head())

smoothed_data = scipy.ndimage.gaussian_filter(df_pivoted.values, sigma=1.5)

fig, ax = plt.subplots(figsize=(16, 9))

# Criando o gráfico de contorno
im = ax.contourf(df_pivoted.columns, df_pivoted.index, smoothed_data, 
                  levels=np.arange(-1, 1.1, 0.2), cmap=plt.get_cmap("coolwarm"), extend='both')

# Barra de cores
cbar = fig.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label("Diferente (°C)")  # Rótulo da barra de cores

ax.invert_yaxis()
ax.set_ylim(1000, 200)

# Ajustando o eixo Y para escala logarítmica
ax.set_yscale('log')

# Definindo os valores de pressão para os rótulos
pressure_ticks = [1000, 900, 800, 700, 600, 500, 400, 300, 200]

# Definindo os rótulos visíveis no eixo Y
ax.set_yticks(pressure_ticks)  # Ticks com os valores de pressão

# Rótulos visíveis no eixo Y (eles vão aparecer como valores de pressão)
ax.set_yticklabels(pressure_ticks)  # Rótulos de pressão reais
ax.set_ylabel("Pressure (hPa)")

# Lista das datas desejadas para o eixo X
desired_dates = ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T09', '2024-02-22T21']

# Convertendo as datas para o formato de string conforme necessário
desired_dates_str = pd.to_datetime(desired_dates)

# Convertendo para strings, que o Matplotlib pode entender facilmente
desired_dates_str = [dt.strftime('%m-%d %HZ') for dt in desired_dates_str]

# Pegando os índices das colunas para as datas desejadas
desired_date_indices = df_pivoted.columns.get_indexer_for(desired_dates)

# Adicionando a data faltante manualmente no índice de colunas, se necessário

# Adicionando as linhas verticais para as outras datas desejadas
for date_index in desired_date_indices:
    ax.axvline(x=df_pivoted.columns[date_index], color='black', linestyle='--', linewidth=1)

# Definindo explicitamente os ticks do eixo X para as datas desejadas
ax.set_xticks(df_pivoted.columns[desired_date_indices])

# Ajustando os rótulos das ticks do eixo X para mostrar as datas no formato desejado
ax.set_xticklabels(desired_dates_str, rotation=90)

# Título do gráfico
plt.title('Zonal deviation of Air Temperature')

# Salvando a imagem
plt.savefig(DIRFIG+'hov_reboita_suave_mascara.png', dpi=300)
