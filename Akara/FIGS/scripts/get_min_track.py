import xarray as xr
import os
import pandas as pd
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import metpy.calc as mpcalc

# Diretórios de dados e figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'

# Inicializando o arquivo
ds_akara = xr.open_dataset(DIRDADO + 'akara_maps.nc')

# Lendo o arquivo CSV
arquivo_csv = pd.read_csv(DIRCSV + 'first_track_akara.csv', sep=',')

# Convertendo as colunas 'time', 'lat' e 'lon'
tempos_csv = pd.to_datetime(arquivo_csv['time'])
arquivo_csv['lat'] = pd.to_numeric(arquivo_csv['lat'], errors='coerce')
arquivo_csv['lon'] = pd.to_numeric(arquivo_csv['lon'], errors='coerce')


# Lista para armazenar os resultados
dados = []

# Iterando sobre os dados
for time, lat, lon in zip(tempos_csv, arquivo_csv['lat'], arquivo_csv['lon']):
    # Selecionando a pressão ao nível do mar
    msl = ds_akara['msl'].sel(valid_time=time, latitude=lat, longitude=lon, method="nearest") / 100  # Converte para hPa
    u850 = ds_akara['u'].sel(valid_time=time, pressure_level=850)
    v850 = ds_akara['v'].sel(valid_time=time, pressure_level=850)
    vort850 = mpcalc.vorticity(u850, v850).sel(latitude=lat, longitude=lon, method='nearest')
    
    # Armazenando os resultados na lista
    dados.append([time, lat, lon, msl.values.item(), vort850.values])  

# Convertendo a lista em um DataFrame
df_resultados = pd.DataFrame(dados, columns=['Time', 'Lat', 'Lon', 'MSL', 'vort'])

# Salvando o DataFrame em um arquivo CSV
df_resultados.to_csv(DIRCSV + 'track_mslp_vort_inicial.csv', index=False, sep=',')

print("Arquivo track_mslp_vort.csv criado com sucesso!")
