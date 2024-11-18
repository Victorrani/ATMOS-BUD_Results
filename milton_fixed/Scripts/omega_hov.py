import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter

# Diretórios dos dados e das figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/milton_fixed/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/milton_fixed/Figures/V_balanc_fixed/'

Omega = DIRDADO + 'Omega.csv'

arq = Omega



labels = ['Omega']


# Nome do arquivo
nome_arquivo = arq.split('/')[-1].split('.')[0]

# Abertura dos dados em um DataFrame
df = pd.read_csv(arq, index_col=[0])

# Converter nomes das colunas para objetos datetime com UTC
df.columns = pd.to_datetime(df.columns, utc=True)

# Remover o fuso horário UTC para considerar as datas como locais
df.columns = df.columns.tz_convert(None)

# Ajuste do índice (presumivelmente em hPa)
df.index = df.index / 100

# Ajustando limites do colormap para max, min e zero
max_abs = max(abs(df.values.min()), abs(df.values.max()))
vmin = -max_abs
vmax = max_abs
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Criando o diagrama Hovmöller
fig, ax = plt.subplots(figsize=(8, 6))

# Gerando o gráfico Hovmöller com contornos preenchidos
im = ax.contourf(df.columns, df.index, df.values, cmap='RdBu_r', extend='both',  
                 norm=norm, levels=np.linspace(vmin, vmax, 11))

# Adicionando a barra de cores
cbar = fig.colorbar(im)

contours = ax.contour(df.columns, df.index, df.values, colors='black', 
                       levels=np.linspace(vmin, vmax, 11), linewidths=1)

# Adicionando os valores dos contornos com formatação científica
#ax.clabel(contours, inline=True, fontsize=8, fmt='%1.1e')
# Inverter o eixo y
ax.invert_yaxis()

# Adicionar linhas verticais em datas específicas
for time in ['2024-10-04T00', '2024-10-05T00', '2024-10-06T00', '2024-10-07T00',
             '2024-10-08T00', '2024-10-09T00', '2024-10-10T00', '2024-10-10T18']:
    ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

# Formatar o eixo x como data e rotacionar os rótulos
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.tick_params(axis='x', labelrotation=45)

# Configurar título e rótulos dos eixos
ax.set_title(f'Milton - Omega - EXP:fixed', fontsize=12, loc='left')
ax.set_ylabel('Pressure (hPa)', fontsize=14)

# Editar legenda da barra de cores
cbar.set_label('[Pa / s]', fontsize=12)
cbar.ax.tick_params(labelsize=10)

# Adicionar formatação científica à barra de cores
cbar.formatter = ScalarFormatter(useMathText=True)
cbar.formatter.set_scientific(True)
cbar.formatter.set_powerlimits((-3, 3))
cbar.update_ticks()

# Salvar o gráfico
plt.savefig(DIRFIGS + nome_arquivo + '_hov.png', bbox_inches='tight')

# Fechar a figura
plt.close()
