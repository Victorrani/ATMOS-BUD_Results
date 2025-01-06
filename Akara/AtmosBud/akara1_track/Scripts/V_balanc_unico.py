import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

# Lista de arquivos de dados
AdvHZeta = DIRDADO + 'AdvHZeta.csv'
AdvVZeta = DIRDADO + 'AdvVZeta.csv'
dZdt = DIRDADO + 'dZdt.csv'
vxBeta = DIRDADO + 'vxBeta.csv'
ZetaDivH = DIRDADO + 'ZetaDivH.csv'
fDivH = DIRDADO + 'fDivH.csv'
Tilting = DIRDADO + 'Tilting.csv'
ResZ = DIRDADO + 'ResZ.csv'

lista_arquivos = [AdvHZeta, AdvVZeta, dZdt, vxBeta, ZetaDivH, fDivH, Tilting, ResZ]

# Intervalos de datas
date_intervals = [
    ('2024-02-14T21', '2024-02-16T09'),
    ('2024-02-16T09', '2024-02-19T15'),
    ('2024-02-19T15', '2024-02-20T06'),
    ('2024-02-20T06', '2024-02-22T21')
]

nomes = ['(A) Incipient', '(B) Intensification', '(C) Mature', '(D) Decay']
colors = ['#0072B2', '#D55E00', '#F0E442', '#56B4E9', '#009E73', '#CC79A7', '#E69F00', '#000000']
labels = ['Horizontal Vorticity Advection', 'Vertical Vorticity Advection', 'Local Vorticity Tendency',
          'Planetary Vorticity Advection', 'Stretching Term zeta', 'Stretching Term f',
          'Tilting Term', 'Friction Residual']

# Marcadores diferentes para cada curva
markers = ['x', 'd', 'o', '^', 's', 'p', 'H', '*']

# Criar uma figura com 4 subplots (1 linha, 4 colunas)
fig, axs = plt.subplots(1, 4, figsize=(24, 10), sharey=True)

for idx, (date_interval, nome) in enumerate(zip(date_intervals, nomes)):
    ax = axs[idx]  # Selecionar o subplot correspondente
    all_data = []
    date1, date2 = date_interval

    for file_path in lista_arquivos:
        # Abrir dados
        df = pd.read_csv(file_path, index_col=[0])
        df.index = df.index / 100  # Ajuste da escala de pressão (hPa)
        df.columns = pd.to_datetime(df.columns).strftime('%Y-%m-%dT%H')

        # Selecionar intervalo de datas e calcular a média
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)
        all_data.append(selected_data_mean)

    # Plotar os dados no subplot correspondente
    for i, data in enumerate(all_data):
        ax.plot(data, df.index, label=labels[i], color=colors[i],
                linewidth=1.5, linestyle='solid', marker=markers[i], markersize=6)

    ax.axvline(0, c='black', linewidth=0.75)
    ax.invert_yaxis()
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
    ax.set_ylim(1000, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
    #ax.set_xlim(-5e-9, 5e-9)

    # Título e configurações do subplot
    ax.set_title(nome, fontsize=16, loc='center', fontweight='bold')
    ax.set_xlabel('[1/s²]', fontsize=18)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)

# Adicionar legenda comum para todos os subplots
fig.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize=18, ncol=4, frameon=True)

# Ajustar espaçamento entre os subplots
fig.tight_layout(rect=[0, 0, 1, 0.9])

# Salvar a figura
plt.savefig(DIRFIGS + 'Vorticity_Budget_Combined_1x4.png', bbox_inches='tight', dpi=300)
plt.close()

print("Gráfico 1x4 combinado gerado com sucesso!")
