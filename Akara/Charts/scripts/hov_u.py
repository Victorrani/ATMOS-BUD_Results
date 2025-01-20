import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Definindo diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/hovs/'

arquivo = 'akara_hov.nc'

# Abrindo o arquivo NetCDF
ds = xr.open_dataset(DIRDADO + arquivo)

latitudes = [-24.75]  # Quatro latitudes para criar um layout 2x2

# Criando a figura e a grade de subplots
fig, ax = plt.subplots(2, 2, figsize=(12, 10))  # 2 linhas, 2 colunas

# Iterando pelas latitudes e preenchendo os subplots
for i, latitude in enumerate(latitudes):
    # Selecionando o nível de pressão e a latitude
    u_30 = ds['u'][:].sel(pressure_level=30, latitude=latitude)
    
    # Extraindo longitude e tempo
    lon = ds['longitude'][:]
    time = ds['valid_time']

    # Convertendo para DataFrame
    u_30_values = u_30.values
    df_u_30 = pd.DataFrame(u_30_values, index=time, columns=lon)
    df_u_30 = df_u_30.iloc[::-1, :]  # Invertendo o tempo
    
    # Definindo normalização para o colormap
    vmin = min(df_u_30.values.min(), -df_u_30.values.max())
    vmax = max(df_u_30.values.max(), -df_u_30.values.min())
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    
    # Determinando a posição do subplot
    row = i // 2  # Linha (0 ou 1)
    col = i % 2   # Coluna (0 ou 1)
    
    # Plotando o subplot
    c = ax[row, col].contourf(df_u_30.columns, df_u_30.index, df_u_30.values, cmap='coolwarm', norm=norm)
    ax[row, col].set_title(f'Latitude: {latitude} U (30 hPa)', fontsize=14)
    ax[row, col].set_xlabel('Longitude', fontsize=12)
    ax[row, col].set_ylabel('Tempo', fontsize=12)
    ax[row, col].tick_params(axis='x', labelsize=10)
    ax[row, col].tick_params(axis='y', labelsize=10)
    
    # Invertendo o eixo Y
    ax[row, col].invert_yaxis()
    
    # Ajustando ticks do tempo
    time_range = pd.to_datetime(df_u_30.index)
    day_ticks = pd.date_range(start=time_range.min(), end=time_range.max(), freq='D')
    ax[row, col].set_yticks(day_ticks)
    ax[row, col].set_yticklabels(day_ticks.strftime('%Y-%m-%d'), rotation=45, ha='right')
    
    # Adicionando a barra de cores para cada subplot
    fig.colorbar(c, ax=ax[row, col], orientation='vertical', label='Velocidade U (m/s)')

# Ajustando o layout
plt.tight_layout()

# Salvando e exibindo o gráfico
plt.savefig(DIRFIG + 'hov_u_2x2.png', dpi=300, bbox_inches='tight')
plt.show()
