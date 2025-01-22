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
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/cross_sections/hov/'
# Lendo o arquivo com separador por espaço(s)

df = pd.read_csv(DIRCSV+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

ds_akara = xr.open_dataset(DIRDADO+'akara_maps.nc')

lat_ = ds_akara['latitude'][:]
lon_ = ds_akara['longitude'][:]
times = ds_akara['valid_time'].values
# Lista para armazenar os resultados
zonal_deviation_results = []

import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.interpolate import cross_section

DIRSHAPE = '/home/victor/USP/sat_goes/shapefile/BR_UF_2019.shp'
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/cross_sections/hov/'

# Lendo o arquivo de dados
df = pd.read_csv(DIRCSV + 'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

# Lendo o arquivo NetCDF
ds_akara = xr.open_dataset(DIRDADO + 'akara_maps.nc')

lat_ = ds_akara['latitude'][:]
lon_ = ds_akara['longitude'][:]
times = ds_akara['valid_time'].values

# Lista para armazenar os resultados
zonal_deviation_results = []

# Iterando sobre os tempos e posições
for i in range(0,len(df),2):
    time = str(times[i])[:13]
    tempo = df.loc[i, 'time']
    lat = df.loc[i, 'Lat']
    lon = df.loc[i, 'Lon']

    # Cross-section
    ds_akara_tempo = ds_akara.isel(valid_time=i)
    data = ds_akara_tempo.metpy.parse_cf().squeeze()
    start = (lat, lon - 2)
    end = (lat, lon + 2)
    cross = cross_section(data, start, end).set_coords(('latitude', 'longitude'))
    
    # Temperatura potencial
    cross['Potential_temperature'] = mpcalc.potential_temperature(
        cross['pressure_level'], cross['t']
    )
    
    # Média zonal e desvio zonal
    cross_theta_mean = cross['Potential_temperature'].mean('index')
    theta_zonal_deviation = cross['Potential_temperature'] - cross_theta_mean

    theta_zonal_deviation_cyclone_center = theta_zonal_deviation.isel(index=50)

    
    # Salvando os resultados na lista
    zonal_deviation_results.append({
        'time': time,
        'theta_zonal_mean': theta_zonal_deviation_cyclone_center.values,  # Valores como array NumPy
        'pressure_levels': cross['pressure_level'].values,  # Níveis de pressão
    })

# Verificação de um exemplo
print(zonal_deviation_results[0])

# Criando DataFrame para os resultados de desvio zonal
df_results = pd.DataFrame([
    {
        'time': result['time'],
        'pressure_level': pressure_level,
        'theta_zonal_mean': theta_mean
    }
    for result in zonal_deviation_results
    for pressure_level, theta_mean in zip(result['pressure_levels'], result['theta_zonal_mean'])
])

# Verificar as primeiras linhas do DataFrame
print(df_results.head())

# Reformatar o DataFrame
df_pivoted = df_results.pivot(index='pressure_level', columns='time', values='theta_zonal_mean')

# Ordenar os níveis de pressão em ordem decrescente (se necessário)
df_pivoted = df_pivoted.sort_index(ascending=False)

# Exibir o resultado
print(df_pivoted.head())

# Salvar o DataFrame reformado em CSV
output_path_pivoted = DIRCSV + 'zonal_deviation_results_pivoted.csv'
df_pivoted.to_csv(output_path_pivoted)
print(f"Arquivo salvo em: {output_path_pivoted}")

fig, ax = plt.subplots(figsize=(16, 9))

im = ax.contourf(df_pivoted.columns, df_pivoted.index, df_pivoted.values,levels=np.arange(-1, 1, 0.2),
                  cmap=plt.get_cmap("coolwarm"), extend='both'
)
cbar = fig.colorbar(im, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label("Theta Zonal Deviation (units)")  # Rótulo da barra de cores
ax.invert_yaxis()



ax.tick_params(axis='x', labelrotation=90)

plt.savefig(DIRFIG+'hov', dpi=300)