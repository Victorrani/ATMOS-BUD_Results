import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter
import os

# Diretórios dos dados e das figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

ck = DIRDADO + 'Ck_pressure_level.csv'

arq = ck

labels = ['Ck']

# Nome do arquivo
nome_arquivo = arq.split('/')[-1].split('.')[0]

# Abertura dos dados em um DataFrame
df = pd.read_csv(arq, index_col=[0])
df = df.T
print(df)

# Converter nomes das colunas para objetos datetime com UTC
df.columns = pd.to_datetime(df.columns, utc=True)

# Remover o fuso horário UTC para considerar as datas como locais
df.columns = df.columns.tz_convert(None)

# Converter índice (pressões) em valores numéricos e ajustar para hPa
df.index = pd.to_numeric(df.index, errors='coerce')  # Converte para números
df.index = df.index / 100  # Ajustar escala para hPa

# Remover entradas inválidas do índice
df = df.dropna()  # Remove linhas com índices inválidos, se houver

# Verificação após a conversão
print("Índice ajustado:", df.index)

# Ajustando limites do colormap para max, min e zero
vmin = -20e-4
vmax = 9e-4
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Criando o diagrama Hovmöller
fig, ax = plt.subplots(figsize=(8, 6))

# Gerando o gráfico Hovmöller com contornos preenchidos
# Gerando o gráfico Hovmöller com contornos preenchidos
im = ax.contourf(df.columns, df.index, df.values, cmap='coolwarm', extend='both',  
                 norm=norm, levels=np.linspace(vmin, vmax, 11))

# Adicionando a barra de cores
cbar = fig.colorbar(im, pad=0.05, aspect=15)

# Ajustando a fonte e o tamanho da barra de cores
cbar.set_label('W/m²', fontsize=18) 
cbar.ax.tick_params(labelsize=14)  

# Se necessário, adicione formatação científica (já foi feito acima)
cbar.formatter = ScalarFormatter(useMathText=True)
cbar.formatter.set_scientific(True)
cbar.formatter.set_powerlimits((-3, 3))
cbar.update_ticks()

ax.invert_yaxis()
ax.set_ylim(1000, 100)
ax.set_yscale('log')
ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
ax.set_ylabel("Pressure (hPa)", fontsize=14)

# Adicionar linhas verticais em datas específicas
for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
    ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

# Formatar o eixo x como data e rotacionar os rótulos
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.tick_params(axis='x', labelrotation=45)
ax.tick_params(axis='x', labelsize=14)  # Fonte para os rótulos do eixo X
ax.tick_params(axis='y', labelsize=14)

# Configurar título e rótulos dos eixos
ax.set_title(f'Akará - Ck - EXP:track', fontsize=18, loc='left')
ax.set_ylabel('Pressure (hPa)', fontsize=18)

# Editar legenda da barra de cores
cbar.set_label('W/m²', fontsize=18)
cbar.ax.tick_params(labelsize=10)

# Adicionar formatação científica à barra de cores
cbar.formatter = ScalarFormatter(useMathText=True)
cbar.formatter.set_scientific(True)
cbar.formatter.set_powerlimits((-3, 3))
cbar.update_ticks()

# Caminho completo do arquivo a ser salvo
output_path = DIRFIGS + nome_arquivo + '_hov.png'

# Salvar o gráfico
plt.savefig(output_path, bbox_inches='tight')

# Fechar a figura
plt.close()

# Exibir onde o arquivo foi salvo
print(f"Gráfico Hovmöller salvo em: {output_path}")
