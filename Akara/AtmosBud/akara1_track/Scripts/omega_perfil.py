import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import os

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'


# Lista de arquivos de dados

Omega = DIRDADO + 'Omega.csv'

lista_arquivos = [Omega]


labels = ['Omega']

# Intervalos de datas a serem usados para as fases
date_intervals = [
    ('2024-02-14T21', '2024-02-16T09'),  # Incipiente
    ('2024-02-16T09', '2024-02-19T15'),  # Intensificação
    ('2024-02-19T15', '2024-02-20T06'),  # Maturação
    ('2024-02-20T06', '2024-02-22T21')   # Declínio
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
    colors = ['#65a1e6', '#f7b538', '#d62828', '#9aa981']
    curves = ['Incipient', 'Intensification', 'Maturation', 'Decay']

    # Plotar cada fase usando os intervalos de data
    for idx, date_interval in enumerate(date_intervals):
        date1, date2 = date_interval

        # Selecionar os dados do intervalo de tempo e calcular a média
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)

        # Converter a média para valores diários (86400 segundos por dia)
        #dia = 86400
        ax.plot(selected_data_mean, df.index, label=curves[idx], 
                color=colors[idx], marker='x', markerfacecolor='white', markersize=5)

    # Customizações do gráfico
    ax.axvline(0, c='k', linewidth=0.75)  # Linha vertical em x=0
    ax.invert_yaxis()
    ax.set_ylim(1000, 100)
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)  # Linhas de grade horizontais

    # Definir título e rótulos dos eixos
    ax.set_title(f'Akará - Omega - EXP:track', fontsize=18, loc='left')
    ax.set_xlabel('[Pa / s]', fontsize=18)
    ax.set_ylabel('Pressure (hPa)', fontsize=18)
    ax.set_xlim([-2e-1,0.5e-1])

    # Formatação científica para o eixo X
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax.tick_params(axis='x', labelsize=14)  # Aumentar tamanho dos valores no eixo x
    ax.tick_params(axis='y', labelsize=14)

    # Definir ticks personalizados para o eixo Y
    custom_y_ticks = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100]
    ax.set_yticks(custom_y_ticks)

    # Definir fundo do gráfico como branco
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')

    # Exibir legenda e ajustar layout
    plt.legend(fontsize=14)
    plt.tight_layout()

    # Salvar a figura
    plt.savefig(DIRFIGS + nome_arquivo + '_track.png', dpi=300)
    plt.close()  # Fechar a figura para liberar memória
