import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import os

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Milton/AtmosBud/milton_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Milton/AtmosBud/milton_track/Figures/T_balanc_track/'

# Lista de arquivos de dados
dTdt = DIRDADO + 'dTdt.csv'
AdvHTemp = DIRDADO + 'AdvHTemp.csv'
AdvVTemp = DIRDADO + 'AdvVTemp.csv'
SigmaOmega = DIRDADO + 'Sigma_omega.csv'
ResT = DIRDADO + 'ResT.csv'

#lista_arquivos = [dTdt]
#lista_arquivos = [AdvHTemp]
#lista_arquivos = [AdvVTemp]
#lista_arquivos = [SigmaOmega]
lista_arquivos = [ResT]

labels = ['Local Temperature Tendency',
          'Horizontal Temperature Advection',
          'Vertical Temperature Advection',
          'Total Vertical Motion Effect',
          'Diabatic Heating'] 

# Intervalos de datas a serem usados para as fases
date_intervals = [
    ('2024-10-04T00', '2024-10-05T00'),
    ('2024-10-05T00', '2024-10-06T00'),
    ('2024-10-06T00', '2024-10-07T00'),
    ('2024-10-07T00', '2024-10-08T00'),
    ('2024-10-08T00', '2024-10-09T00'),
    ('2024-10-09T00', '2024-10-10T00'),
    ('2024-10-10T00', '2024-10-10T18')
]

# Loop para processar cada arquivo da lista
for i in lista_arquivos:
    nome_arquivo = i.rsplit('/', 1)[-1].split('.')[0]  # Extrair nome do arquivo sem extensão

    # Ler os dados em um DataFrame e ajustar o índice e as colunas
    df = pd.read_csv(i, index_col=[0])
    df.index = df.index / 100  # Ajustar o índice (supondo que esteja em decapascais)
    df.columns = pd.to_datetime(df.columns)  # Converter colunas para datetime
    df.columns = df.columns.strftime('%Y-%m-%dT%H')  # Formatar colunas como 'YYYY-MM-DDTHH'

    # Criar subplots com tamanho maior verticalmente
    fig, ax = plt.subplots(figsize=(8, 6))

    # Cores acessíveis para daltonismo
    colors = ['#0072B2', '#D55E00', '#F0E442', '#56B4E9', '#009E73', '#CC79A7', '#E69F00', '#000000']
    curves = ['2024-10-04', '2024-10-05', '2024-10-06', '2024-10-07', '2024-10-08', 
         '2024-10-09', '2024-10-10']

    # Plotar cada fase usando os intervalos de data
    for idx, date_interval in enumerate(date_intervals):
        date1, date2 = date_interval

        # Selecionar os dados do intervalo de tempo e calcular a média
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)

        # Converter a média para valores diários (86400 segundos por dia)
        dia = 86400
        ax.plot(selected_data_mean * dia, df.index, label=curves[idx], 
                color=colors[idx], marker='x', markerfacecolor='white', markersize=5)

    # Configurações do eixo Y - Escala logarítmica
    ax.set_yscale('log')
    
    ax.set_ylim(1000, 100)  # Limites do eixo Y
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])

    # Outras customizações do gráfico
    ax.axvline(0, c='k', linewidth=0.75)  # Linha vertical em x=0
    #ax.invert_yaxis()  # Inverter o eixo Y (pressão)
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)  # Linhas de grade horizontais

    # Definir título e rótulos dos eixos
    ax.set_title(f'Milton - Diabatic Heating- EXP:track', fontsize=12, loc='left')
    ax.set_xlabel('[K / day]', fontsize=11)
    ax.set_ylabel('Pressure (hPa)', fontsize=12)
    ax.set_xlim([-5, 25])

    # Formatação científica para o eixo X
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Definir fundo do gráfico como branco
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')

    # Exibir legenda e ajustar layout
    plt.legend()
    plt.tight_layout()

    # Salvar a figura
    plt.savefig(DIRFIGS + nome_arquivo + '_track.png', dpi=300)
    plt.close()  # Fechar a figura para liberar memória