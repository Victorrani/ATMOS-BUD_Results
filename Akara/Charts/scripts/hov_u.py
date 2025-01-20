import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm


# Definindo diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/hovs/'

arquivo = 'akara_hov.nc'

# Abrindo o arquivo NetCDF
ds = xr.open_dataset(DIRDADO + arquivo)

latitudes = [-24.75, -24.0, -31.0] 
longitudes = [-43.75, -39.75, -42.0]
cmap = 'terrain'

vmin, vmax, vcenter = -30, 30, 0

# Normalizando para garantir que 0 seja branco
norm0 = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
norm1 = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
norm2 = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)

fig, ax = plt.subplots(2, 2, figsize=(12, 10))  # Adicionado sharey=True

# Selecionando o nível de pressão e a latitude
u_30_0 = ds['u'][:].sel(pressure_level=30, latitude=latitudes[0])
u_30_1 = ds['u'][:].sel(pressure_level=30, latitude=latitudes[1])
u_30_2 = ds['u'][:].sel(pressure_level=30, latitude=latitudes[2])

# Extraindo longitude e tempo
lon = ds['longitude'][:]
time = ds['valid_time']

# Convertendo para DataFrame
u_30_0_values = u_30_0.values
df_u_30_0 = pd.DataFrame(u_30_0_values, index=time, columns=lon)
df_u_30_0 = df_u_30_0.iloc[::-1, :]  # Invertendo o tempo
# Definindo normalização para o colormap




# Criando o gráfico
d = ax[0, 0].contourf(df_u_30_0.columns,
                       df_u_30_0.index,
                       df_u_30_0.values,
                       cmap=cmap,
                       norm=norm0,
                       extend='both', 
                       levels=np.arange(-30, 3, 3))

ax[0, 0].set_title(f'A) Latitude: {latitudes[0]} u zonal (m/s) (30 hPa)', fontsize=12)
ax[0, 0].set_xlabel('Longitude', fontsize=12)
ax[0, 0].tick_params(axis='x', labelsize=10)
ax[0, 0].tick_params(axis='y', labelsize=10)
ax[0, 0].invert_yaxis()

# Ajustando os ticks do tempo
time_range = pd.to_datetime(df_u_30_0.index)
day_ticks = pd.date_range(start=time_range.min(), end=time_range.max(), freq='D')
ax[0, 0].set_yticks(day_ticks)
ax[0, 0].set_yticklabels(day_ticks.strftime('%m-%d'), ha='right')

cbar = fig.colorbar(d, ax=ax[0, 0], label='Velocidade (m/s)',
              orientation='vertical', extend='both', 
              ticks=np.arange(-30, 3, 3)) 

u_30_1_values = u_30_1.values
df_u_30_1 = pd.DataFrame(u_30_1_values, index=time, columns=lon)
df_u_30_1 = df_u_30_1.iloc[::-1, :]  # Invertendo o tempo
# Definindo normalização para o colormap



c = ax[0, 1].contourf(df_u_30_1.columns, df_u_30_1.index,
                       df_u_30_1.values, cmap=cmap, norm=norm1,
                         extend='both', levels=np.arange(-30, 3, 3))
ax[0, 1].set_title(f'B) Latitude: {latitudes[1]} U (30 hPa)', fontsize=14)
ax[0, 1].set_xlabel('Longitude', fontsize=12)
ax[0, 1].tick_params(axis='x', labelsize=10)
ax[0, 1].tick_params(axis='y', labelsize=10)
ax[0, 1].set_yticks(day_ticks)
ax[0, 1].set_yticklabels(day_ticks.strftime('%m-%d'), ha='right')
ax[0, 1].invert_yaxis()

# Barra de cores para o segundo subplot
fig.colorbar(c, ax=ax[0, 1], orientation='vertical',
              label='Velocidade (m/s)', extend='both', ticks=np.arange(-30, 3, 3))

u_30_2_values = u_30_2.values
df_u_30_2 = pd.DataFrame(u_30_2_values, index=time, columns=lon)
df_u_30_2 = df_u_30_2.iloc[::-1, :]  # Invertendo o tempo



# Plotando o terceiro subplot
e = ax[1, 0].contourf(df_u_30_2.columns, df_u_30_2.index, df_u_30_2.values,
                       cmap=cmap, norm=norm2, extend='both', levels=np.arange(-30, 3, 3))
ax[1, 0].set_title(f'C) Latitude: {latitudes[2]} U (30 hPa)', fontsize=14)
ax[1, 0].set_xlabel('Longitude', fontsize=12)
ax[1, 0].tick_params(axis='x', labelsize=10)
ax[1, 0].tick_params(axis='y', labelsize=10)
ax[1, 0].set_yticks(day_ticks)
ax[1, 0].set_yticklabels(day_ticks.strftime('%m-%d'), ha='right')
ax[1, 0].invert_yaxis()

# Barra de cores para o terceiro subplot
fig.colorbar(e, ax=ax[1, 0], orientation='vertical',
              label='Velocidade (m/s)', extend='both', ticks=np.arange(-30, 3, 3))



# Definindo o eixo com projeção Cartopy diretamente
projection = ccrs.PlateCarree()

ax[1, 1].set_xticks([])  # Remove os ticks do eixo X
ax[1, 1].set_yticks([])

# Use o ax[1, 1] diretamente, sem o `fig.add_subplot()`
ax[1, 1] = fig.add_subplot(2, 2, 4, projection=projection)  # Eixo com projeção Cartopy
ax[1, 1].set_extent([-100, -10, -60, 15], crs=ccrs.PlateCarree())

# Adicionando features ao mapa
ax[1, 1].add_feature(cfeature.BORDERS, linestyle=':', edgecolor='black')
ax[1, 1].add_feature(cfeature.COASTLINE)
ax[1, 1].add_feature(cfeature.STATES, edgecolor='gray', linestyle='-', linewidth=0.5)

gl = ax[1,1].gridlines(crs=ccrs.PlateCarree(), color='black', alpha=1.0, linestyle='--', linewidth=0.25,
                  xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-90, 90, 10), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'fontsize': 14}  # Ajuste o tamanho da fonte no eixo X (longitude)
gl.ylabel_style = {'fontsize': 14}

ax[1, 1].scatter(longitudes[0], latitudes[0], color='red', s=50, marker='x')
ax[1, 1].scatter(longitudes[1], latitudes[1], color='blue', s=50, marker='x')
ax[1, 1].scatter(longitudes[2], latitudes[2], color='green', s=50, marker='x')

ax[1, 1].plot([-80, -20], [latitudes[0], latitudes[0]], color='red', lw=2, label='A) Incipient')
ax[1, 1].plot([-80, -20], [latitudes[1], latitudes[1]], color='blue', lw=2, label='B) Intensification')
ax[1, 1].plot([-80, -20], [latitudes[2], latitudes[2]], color='green', lw=2, label='C) Mature')
ax[1, 1].legend(loc='lower right', fontsize=12)

# Salvando o gráfico
plt.savefig(DIRFIG + 'hov_u_2x2_30.png', dpi=300, bbox_inches='tight')

# Exibindo o gráfico
