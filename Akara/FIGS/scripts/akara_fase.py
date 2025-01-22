import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
import scipy.ndimage
import matplotlib.dates as mdates
import matplotlib.patches as mpatches


DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRCSV2 =  '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/CSV_FILES/'
DIRFIG = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/FIGS/Specific_Figures/serie/'

df = pd.read_csv(DIRCSV+'akara1_track_track.csv', sep=';')
df2 = pd.read_csv(DIRCSV2+'trackfile.v3.txt', sep='\s+', header=None, names=["time", "Lat", "Lon", "mslp", "vort850"])

df_plot = df[['time', 'min_max_zeta_850', 'min_hgt_850']]

df_plot['time'] = pd.to_datetime(df_plot['time'])
df2['time'] = pd.to_datetime(df2['time'])


# Plotar os dados com eixos duplos
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotar no primeiro eixo y
ax1.plot(df_plot['time'], df2['mslp'], label='MSLP', marker='o', color='black')
ax1.set_xlabel('Data')
ax1.tick_params(axis='y', labelcolor='black')
#ax1.legend(loc='lower left', bbox_to_anchor=(0.01, 0))  # Ajuste da posição da legenda do eixo 1

# Criar um segundo eixo y (eixo secundário) com escala diferente
ax2 = ax1.twinx()
ax2.plot(df_plot['time'], df_plot['min_max_zeta_850'], label=r'$\zeta_{850}$', marker='o', color='blue')  # Usando LaTeX para zeta com subscrito
ax2.tick_params(axis='y', labelcolor='blue')
#ax2.legend(loc='lower left', bbox_to_anchor=(0.01, 0.06))  # Ajuste da posição da legenda

patches = [
    mpatches.Patch(color='black', label='MSLP'),
    mpatches.Patch(color='blue', label=r'$\zeta_{850}$')
]

# Adicione a legenda ao gráfico
plt.legend(handles=patches, loc='lower left')

  # Substitua com o tempo desejado
time0 = pd.to_datetime('2024-02-14T21')
time1 = pd.to_datetime('2024-02-16T09')
time2 = pd.to_datetime('2024-02-19T15')
time3 = pd.to_datetime('2024-02-20T09')
time4 = pd.to_datetime('2024-02-22T21')

time5 = pd.to_datetime('2024-02-17T12')
time6 = pd.to_datetime('2024-02-21T09')



ax1.axvline(time0, color='black', linewidth=1.5)
ax1.axvline(time1, color='black', linewidth=1.5)
ax1.axvline(time2, color='black', linewidth=1.5)
ax1.axvline(time3, color='black', linewidth=1.5)
ax1.axvline(time4, color='black', linewidth=1.5)

#ax1.axvline(time5, color='black', linewidth=1.5, linestyle='--')
#ax1.axvline(time6, color='black', linewidth=1.5, linestyle='--')

colors_phases = {'Incipient': '#65a1e6', 'Intensification': '#f7b538',
                 'Mature': '#d62828', 'Decay': '#9aa981'}

ax1.axvspan(time0, time1, color='#65a1e6', alpha=0.3)
ax1.axvspan(time1, time2, color='#f7b538', alpha=0.3)
ax1.axvspan(time2, time3, color='#d62828', alpha=0.3)
ax1.axvspan(time3, time4, color='#9aa981', alpha=0.3)


ax1.text(df_plot['time'][1], df2['mslp'][1] ,'             Subtropical Phase                ', bbox=dict(boxstyle="darrow,pad=0.1",
                                                                                                          facecolor='lightcoral', edgecolor='lightcoral'))
ax1.text(df_plot['time'][22], df2['mslp'][1] ,'                                  Tropical Phase                                ', bbox=dict(boxstyle="darrow,pad=0.1", facecolor='lightcoral', edgecolor='lightcoral'))
ax1.text(df_plot['time'][53], df2['mslp'][1] ,' Subtropical Phase ', bbox=dict(boxstyle="darrow,pad=0.1", facecolor='lightcoral', edgecolor='lightcoral'))


# Definir os ticks do eixo X para datas específicas, espaçando a cada 2 valores
time_ticks = df_plot['time'][::2]
ax1.set_xticks(time_ticks)  # Configurar os ticks no eixo X
ax1.set_xticklabels([t.strftime('%Y-%m-%d %HZ')[5:] for t in time_ticks], rotation=90)  # Formatando as datas


plt.xlim(df_plot['time'][0], df_plot['time'][64])



# Crie legendas apenas para as fases que você deseja mostrar
patches = [mpatches.Patch(color=color, label=phase) for phase, color in colors_phases.items()]

# Adicione a legenda ao gráfico
plt.legend(handles=patches, loc=(0.82, 0.01))

handles, labels = [], []
handles.append(ax1.lines[0])
handles.append(ax2.lines[0])
handles.extend(patches)
labels = ['MSLP', r'$\zeta_{850}$'] + list(colors_phases.keys())

# Adicione a legenda ao gráfico
plt.legend(handles=handles, labels=labels, loc='lower right', ncol=1)

# Mostrar o gráfico
plt.tight_layout()
plt.savefig(DIRFIG+'serie.png')