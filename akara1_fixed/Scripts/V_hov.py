import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter

# Diretórios dos dados e das figuras
DIRDADO = '/p1-chima/victor/ATMOS-BUD_Results/akara1_fixed/'
DIRFIGS = '/p1-chima/victor/ATMOS-BUD_Results/akara1_fixed/Figures/V_balanc/'

AdvHZeta = DIRDADO + 'AdvHZeta.csv'
AdvVZeta = DIRDADO + 'AdvVZeta.csv'
dZdt = DIRDADO + 'dZdt.csv'
vxBeta = DIRDADO + 'vxBeta.csv'
ZetaDivH = DIRDADO + 'ZetaDivH.csv'
fDivH = DIRDADO + 'fDivH.csv'
Tilting = DIRDADO + 'Tilting.csv'
ResZ = DIRDADO + 'ResZ.csv'

#arq = AdvHZeta
#arq = AdvVZeta
#arq = dZdt
#arq = vxBeta
#arq = ZetaDivH
#arq = fDivH
#arq = Tilting
arq = ResZ



labels = ['Horizontal Vorticity Advection',
          'Vertical Vorticity Advection',
          'Local Vorticity Tendency',
          'Planetary Vorticity Advection',
          'Stretching Term zeta',
          'Stretching Term f',
          'Tilting Term',
          'Friction Residual']


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
vmin = df.min().min()   # Multiplicando para ajustar a escala (valores em K/dia)
vmax = df.max().max()
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Criando o diagrama Hovmöller
fig, ax = plt.subplots(figsize=(8, 6))

# Gerando o gráfico Hovmöller com contornos preenchidos
im = ax.contourf(df.columns, df.index, df.values, cmap='RdBu_r', 
                 norm=norm, levels=np.linspace(vmin, vmax, 31))

# Adicionando a barra de cores
cbar = fig.colorbar(im)

# Inverter o eixo y
ax.invert_yaxis()

# Adicionar linhas verticais em datas específicas
for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
    ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

# Formatar o eixo x como data e rotacionar os rótulos
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.tick_params(axis='x', labelrotation=45)

# Configurar título e rótulos dos eixos
ax.set_title(f'Friction Residual - EXP:fixed', fontsize=12, loc='left')
ax.set_ylabel('Pressure (hPa)', fontsize=14)

# Editar legenda da barra de cores
cbar.set_label('[1 / s²]', fontsize=12)
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