import xarray as xr
import os
import pandas as pd
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import metpy.calc as mpcalc
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Diretórios de dados
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/'


# Caminho para o arquivo de saída
file_path = DIRCSV + 'trackfile.v3.txt'

# Inicializando o arquivo
ds_akara = xr.open_dataset(DIRDADO + 'akara_maps.nc')

arquivo_csv = pd.read_csv(DIRCSV + 'track_mslp_vort_inicial.csv', sep=',')
arquivo_csv['Time'] = pd.to_datetime(arquivo_csv['Time'])
arquivo_csv['Lat'] = pd.to_numeric(arquivo_csv['Lat'], errors='coerce')
arquivo_csv['Lon'] = pd.to_numeric(arquivo_csv['Lon'], errors='coerce')

linhas = len(arquivo_csv['Time'])

# Abrindo o arquivo no modo de adição
with open(file_path, 'a') as file:
    for t_index in range(0, linhas):  # Índices de tempo de 0 até (linhas - 1)
        row = arquivo_csv.iloc[t_index]  # Pegando a linha correspondente no CSV
        lat = row['Lat']
        lon = row['Lon']
        
        # Verificando se Lat ou Lon são NaN
        if pd.isna(lat) or pd.isna(lon):
            continue  # Pula para a próxima iteração se houver NaN
        
        msl = row['MSL']
        vort = row['vort']
        
        # Seleciona o tempo no arquivo .nc com base no índice t_index
        data_nc = ds_akara.isel(valid_time=t_index)
        tempo_atual = data_nc['valid_time'].values
        tempo_atual = str(tempo_atual)[0:13]

        u850 = data_nc['u'].sel(pressure_level=850)
        v850 = data_nc['v'].sel(pressure_level=850)
        
        # Cálculo da vorticidade em 850 hPa
        vort850_tot = mpcalc.vorticity(u850, v850).values
        lati = data_nc['latitude'].values
        long = data_nc['longitude'].values
        msl = data_nc['msl'] / 100

        delta = 1
        # Seleciona os dados de latitude e longitude no arquivo .nc
        data_nc_latlon = data_nc.sel(latitude=slice(lat + delta, lat - delta), longitude=slice(lon - delta, lon + delta), pressure_level=850)

        longitudes = data_nc_latlon.longitude
        latitudes = data_nc_latlon.latitude

        msl_nc = data_nc_latlon['msl'] / 100  # Convertendo de Pa para hPa
        vort850 = mpcalc.vorticity(data_nc_latlon['u'], data_nc_latlon['v'])  # Cálculo da vorticidade para a área selecionada

        # Encontrar a posição da MSL mínima
        min_msl_index = np.unravel_index(np.argmin(msl_nc.values), msl_nc.shape)
        min_msl_latitude = latitudes[min_msl_index[0]].item()  # Obter o valor escalar
        min_msl_longitude = longitudes[min_msl_index[1]].item()  # Obter o valor escalar
        msl_value = msl_nc[min_msl_index].item()  # Obter o valor escalar

        # Encontrar a posição da vorticidade mínima
        min_vort_index = np.unravel_index(np.argmin(vort850.values), vort850.shape)
        min_vort_latitude = latitudes[min_vort_index[0]].item()  # Obter o valor escalar
        min_vort_longitude = longitudes[min_vort_index[1]].item()  # Obter o valor escalar
        vort_min_value = vort850[min_vort_index].item().magnitude * 1e5  # Multiplicando por 10^5

        tempo = datetime.fromisoformat(tempo_atual)
        data_formatada = tempo.strftime('%Y%m%d%H')

        # Escreve os dados no arquivo
        file.write(f'{data_formatada+"00"} {min_msl_latitude} {min_msl_longitude} {msl_value:.3f} {vort_min_value}\n')

        # Imprime os valores para verificação
        print(f'{data_formatada+"00"} MSL Min: {min_msl_latitude}, {min_msl_longitude}, {msl_value:.3f} | Vort Min: {min_vort_latitude}, {min_vort_longitude}, {vort_min_value}')
