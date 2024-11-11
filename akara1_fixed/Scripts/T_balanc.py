import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/akara1_fixed/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/akara1_fixed/Figures/T_balanc_fixed/'

# Lista de arquivos de dados
dTdt = DIRDADO + 'dTdt.csv'
AdvHTemp = DIRDADO + 'AdvHTemp.csv'
AdvVTemp = DIRDADO + 'AdvVTemp.csv'
SigmaOmega = DIRDADO + 'Sigma_omega.csv'
ResT = DIRDADO + 'ResT.csv'

lista_arquivos = [dTdt, AdvHTemp, AdvVTemp, SigmaOmega, ResT]

# Intervalos de datas
date_intervals = [
    ('2024-02-14T21', '2024-02-16T09'),
    ('2024-02-16T09', '2024-02-19T15'),
    ('2024-02-19T15', '2024-02-20T06'),
    ('2024-02-20T06', '2024-02-22T21')
]

nomes = ['Incipient', 'Intensification', 'Mature', 'Decay']

colors = ['#0072B2', '#D55E00', '#F0E442', '#56B4E9', '#009E73']

labels = ['Local Temperature Tendency',
          'Horizontal Temperature Advection',
          'Vertical Temperature Advection',
          'Total Vertical Motion Effect',
          'Diabatic Heating']  # Rótulos para cada curva
hora = 86400

for idx, (date_interval, nome) in enumerate(zip(date_intervals, nomes)):
    fig, ax = plt.subplots(figsize=(8, 6))  # Cria uma nova figura para cada fase
    all_data = []
    date1, date2 = date_interval
    
    for file_path in lista_arquivos:
        # Abrir dados em um DataFrame
        df = pd.read_csv(file_path, index_col=[0])
        df.to_numpy()
        df.index = df.index / 100
        df.columns = pd.to_datetime(df.columns)
        df.columns = df.columns.strftime('%Y-%m-%dT%H')

        # Selecionar dados para um intervalo específico e calcular a média
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)

        # Adicionar dados à lista
        all_data.append(selected_data_mean)

    # Plotar as curvas para a fase específica
    for i, data in enumerate(all_data):
        ax.plot(data * hora, df.index,
                label=labels[i], color=colors[i], linewidth=2, linestyle='solid', marker='x', markerfacecolor='white', markersize=5)

    ax.axvline(0, c='black', linewidth=0.75)  # Adicionar linha vertical em x=0
    ax.invert_yaxis()
    ax.set_ylim(1000, 10)  # Definir limites do eixo y
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)  # Adicionar linhas de grade horizontais
    ax.set_xlim(-8, 22)  # Definir limites do eixo x
    ax.set_title(f'Akará Heat Budget - {nome} - EXP:fixed', fontsize=12, loc='left')  # Definir título
    ax.set_xlabel('[K / Day]', fontsize=10)  # Definir rótulo do eixo x
    ax.set_ylabel('Pressure (hPa)', fontsize=10)  # Definir rótulo do eixo y
    ax.set_facecolor('white')  # Cor de fundo do eixo

    # Definir notação científica para o eixo x
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Definir ticks personalizados para o eixo y
    custom_y_ticks = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 10]
    ax.set_yticks(custom_y_ticks)

    # Remover bordas dos subplots
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    fig.legend(labels, loc='lower right', bbox_to_anchor=(0.95, 0.2), fontsize=10, frameon=True, framealpha=1, edgecolor='black')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    # Salvar a figura com o nome correspondente à fase
    plt.savefig(DIRFIGS + f'Heat_Budget_{nome}.png', bbox_inches='tight', dpi=300)
    
    # Fechar a figura
    plt.close()
