import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter

# Diretórios dos dados e das figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

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

vmin = -0.2
vmax = 0.1
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Criando o diagrama Hovmöller
fig, ax = plt.subplots(figsize=(8, 6))

# Gerando o gráfico Hovmöller com contornos preenchidos
im = ax.contourf(df.columns, df.index, df.values, cmap='coolwarm', extend='both',  
                 norm=norm, levels=np.linspace(vmin, vmax, 11))

# Adicionando a barra de cores
cbar = fig.colorbar(im)



ax.invert_yaxis()
ax.set_ylim(1000, 100)
ax.set_yscale('log')
ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax.set_ylabel("Pressure (hPa)", fontsize=18)

# Adicionar linhas verticais em datas específicas
for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
    ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

# Formatar o eixo x como data e rotacionar os rótulos
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.tick_params(axis='x', labelrotation=45)

# Configurar título e rótulos dos eixos
ax.set_title(f'Akará - Omega - EXP:track', fontsize=18, loc='left')
ax.set_ylabel('Pressure (hPa)', fontsize=18)
ax.tick_params(axis='x', labelsize=18)  # Aumentar tamanho dos valores no eixo x
ax.tick_params(axis='y', labelsize=18)
# Editar legenda da barra de cores
cbar.set_label('[Pa / s]', fontsize=18)
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
