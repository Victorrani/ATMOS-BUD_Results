import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/T_balanc_track/'

# Lista de arquivos de dados
dTdt = DIRDADO + 'dTdt.csv'
AdvHTemp = DIRDADO + 'AdvHTemp.csv'
SigmaOmega = DIRDADO + 'Sigma_omega.csv'
ResT = DIRDADO + 'ResT.csv'

lista_arquivos = [dTdt, AdvHTemp, SigmaOmega, ResT]

# Intervalos de datas
date_intervals = [
    ('2024-02-14T21', '2024-02-16T09'),
    ('2024-02-16T09', '2024-02-19T15'),
    ('2024-02-19T15', '2024-02-20T06'),
    ('2024-02-20T06', '2024-02-22T21')
]

nomes = ['(A) Incipient', '(B) Intensification', '(C) Mature', '(D) Decay']

colors = ['#0072B2', '#D55E00', '#F0E442', '#56B4E9', '#009E73']
labels = ['Local Temperature Tendency', 'Horizontal Temperature Advection', 
          'Total Vertical Motion Effect', 'Diabatic Heating']
markers = ['x', 'd', 'o', '^']  # Marcadores diferentes para cada curva

hora = 86400

# Criar uma figura com 4 subplots (2 linhas, 2 colunas)
fig, axs = plt.subplots(2, 2, figsize=(20, 15), sharey=True)  # 2 linhas, 2 colunas
axs = axs.flatten()  # Achatar a grade para facilitar a iteração

for idx, (date_interval, nome) in enumerate(zip(date_intervals, nomes)):
    ax = axs[idx]  # Selecionar o subplot correspondente
    all_data = []
    date1, date2 = date_interval

    for file_path in lista_arquivos:
        # Abrir dados em um DataFrame
        df = pd.read_csv(file_path, index_col=[0])
        df.index = df.index / 100  # Ajuste da escala de pressão (hPa)
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
                label=labels[i], color=colors[i], linewidth=2, linestyle='solid', 
                marker=markers[i], markerfacecolor='white', markersize=5)

    ax.axvline(0, c='black', linewidth=0.75)  # Adicionar linha vertical em x=0
    ax.invert_yaxis()  # Inverter o eixo y

    # Definir eixo y logarítmico e os ticks
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())  # Remover notação científica no log
    ax.set_ylim(1000, 100)
    
    # Configurações do título e eixos
    ax.set_title(nome, fontsize=18, loc='center', fontweight='bold')
    ax.set_xlabel('[K / Day]', fontsize=18)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)

    # Grid
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)

# Adicionar legenda comum para todos os subplots, abaixo dos gráficos
fig.legend(labels, loc='lower center', bbox_to_anchor=(0.5, -0.07), fontsize=18, ncol=4, 
           frameon=True, framealpha=1, edgecolor='black')

# Ajustar espaçamento entre subplots
fig.tight_layout(rect=[0, 0, 1, 0.95])

# Adicionar um título geral
fig.suptitle('Heat Budget Analysis - Akará Track', fontsize=20, fontweight='bold', y=0.95)

# Salvar a figura
plt.savefig(DIRFIGS + 'Heat_Budget_Combined_2x2.png', bbox_inches='tight', dpi=300)
plt.close()

print("Gráfico combinado 2x2 com título e legenda gerado com sucesso!")
