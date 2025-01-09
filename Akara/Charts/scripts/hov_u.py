import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Definindo diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/'

arquivo = 'akara_hov.nc'

# Abrindo o arquivo NetCDF
ds = xr.open_dataset(DIRDADO + arquivo)

latitude = -30

# Selecionando o nível de pressão corretamente e a latitude mais próxima de -30
u_30 = ds['u'][:].sel(pressure_level=30, latitude=latitude)  # Usando 'nearest' para pegar a latitude mais próxima de -30
u_50 = ds['u'][:].sel(pressure_level=50, latitude=latitude)

# Extraindo longitude e time
lon = ds['longitude'][:]
time = ds['valid_time']

# Convertendo os dados para um formato 2D (longitude vs time)
u_30_values = u_30.values  # valores de 'u' para o nível de pressão 30
u_50_values = u_50.values  # valores de 'u' para o nível de pressão 50

# Criando o DataFrame com as dimensões corretas
df_u_30 = pd.DataFrame(u_30_values, index=time, columns=lon)  # Tempo no índice, Longitude nas colunas
df_u_50 = pd.DataFrame(u_50_values, index=time, columns=lon)  # Tempo no índice, Longitude nas colunas

# Invertendo a ordem das linhas (tempo)
df_u_30 = df_u_30.iloc[::-1, :]  # Invertendo a ordem das linhas (tempo)
df_u_50 = df_u_50.iloc[::-1, :]  # Invertendo a ordem das linhas (tempo)

# Exibindo os DataFrames para verificação
print(df_u_30.head())
print(df_u_50.head())

# Criando a figura com dois gráficos
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Nível de pressão 30
# Usando o colormap 'coolwarm', que já tem um centro branco
cmap = plt.cm.coolwarm

# Definindo a normalização simétrica ao redor de zero
vmin = min(df_u_30.values.min(), -df_u_30.values.max())
vmax = max(df_u_30.values.max(), -df_u_30.values.min())
norm1 = mcolors.Normalize(vmin=vmin, vmax=vmax)

# Plotando com a normalização
c1 = axes[0].contourf(df_u_30.columns, df_u_30.index, df_u_30.values, cmap='coolwarm', norm=norm1)
axes[0].set_title(f'Latitude: {latitude} U (30 hPa)', fontsize=14)
axes[0].set_xlabel('Longitude', fontsize=12)
axes[0].set_ylabel('Tempo', fontsize=12)
axes[0].set_yticks(df_u_30.index[::10])  # Exibindo um número reduzido de ticks no eixo Y
axes[0].set_yticklabels(df_u_30.index[::10].strftime('%Y-%m-%d %H:%M'), rotation=45, ha='right')  # Formatando as datas
axes[0].tick_params(axis='x', labelsize=10)
axes[0].tick_params(axis='y', labelsize=10)

# Invertendo o eixo Y
axes[0].invert_yaxis()
time_range = pd.to_datetime(df_u_30.index)
day_ticks = pd.date_range(start=time_range.min(), end=time_range.max(), freq='D')
axes[0].set_yticks(day_ticks)
axes[0].set_yticklabels(day_ticks.strftime('%Y-%m-%d'), rotation=45, ha='right')  # Formatando as datas

# Adicionando a barra de cores
fig.colorbar(c1, ax=axes[0], orientation='vertical', label='Velocidade U (m/s)')

# Nível de pressão 50
# Usando o mesmo colormap e normalização para o segundo gráfico
norm2 = mcolors.Normalize(vmin=vmin, vmax=vmax)

c2 = axes[1].contourf(df_u_50.columns, df_u_50.index, df_u_50.values, cmap=cmap, norm=norm2)
axes[1].set_title(f'Latitude: {latitude} U (50 hPa)', fontsize=14)
axes[1].set_xlabel('Longitude', fontsize=12)
axes[1].set_ylabel('Tempo', fontsize=12)
axes[1].set_yticks(df_u_50.index[::10])  # Exibindo um número reduzido de ticks no eixo Y
axes[1].set_yticklabels(df_u_50.index[::10].strftime('%Y-%m-%d %H:%M'), rotation=45, ha='right')  # Formatando as datas
axes[1].tick_params(axis='x', labelsize=10)
axes[1].tick_params(axis='y', labelsize=10)

# Invertendo o eixo Y
axes[1].invert_yaxis()

time_range = pd.to_datetime(df_u_50.index)
day_ticks = pd.date_range(start=time_range.min(), end=time_range.max(), freq='D')
axes[1].set_yticks(day_ticks)
axes[1].set_yticklabels(day_ticks.strftime('%Y-%m-%d'), rotation=45, ha='right') 

# Adicionando a barra de cores
fig.colorbar(c2, ax=axes[1], orientation='vertical', label='Velocidade U (m/s)')

# Ajustando o layout para evitar sobreposição
plt.tight_layout()

# Salvando a figura
plt.savefig(DIRFIG+'hov_u.png', dpi=300, bbox_inches='tight')

# Exibindo a figura
plt.show()
