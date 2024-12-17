import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.dates import DateFormatter

# Diretórios de dados e figuras
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/T_balanc_track/'

# Lista de arquivos de dados
arquivos = {
    'dTdt': DIRDADO + 'dTdt.csv',
    'AdvHTemp': DIRDADO + 'AdvHTemp.csv',
    'AdvVTemp': DIRDADO + 'AdvVTemp.csv',
    'SigmaOmega': DIRDADO + 'Sigma_omega.csv',
    'ResT': DIRDADO + 'ResT.csv'
}

# Lista de rótulos e limites para os gráficos
configs = {
    'dTdt': {'label': 'Local Temperature Tendency', 'vmin': -6, 'vmax': 6},
    'AdvHTemp': {'label': 'Horizontal Temperature Advection', 'vmin': -6, 'vmax': 6},
    'AdvVTemp': {'label': 'Vertical Temperature Advection', 'vmin': -15, 'vmax': 30},
    'SigmaOmega': {'label': 'Total Vertical Motion Effect', 'vmin': -15, 'vmax': 8},
    'ResT': {'label': 'Diabatic Heating', 'vmin': -5, 'vmax': 20}
}

# Loop para gerar os gráficos
for nome_arquivo, caminho in arquivos.items():
    label = configs[nome_arquivo]['label']
    vmin = configs[nome_arquivo]['vmin']
    vmax = configs[nome_arquivo]['vmax']

    print(f"\nGerando gráfico para: {label} ({nome_arquivo})")

    # Abertura dos dados em um DataFrame
    df = pd.read_csv(caminho, index_col=[0])
    
    # Converter nomes das colunas para objetos datetime com UTC
    df.columns = pd.to_datetime(df.columns, utc=True)
    df.columns = df.columns.tz_convert(None)  # Remover UTC

    # Ajuste do índice (presumivelmente em hPa)
    df.index = df.index / 100

    # Criando o diagrama Hovmöller
    fig, ax = plt.subplots(figsize=(8, 6))
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    # Contornos preenchidos
    im = ax.contourf(df.columns, df.index, df.values * 86400, cmap='coolwarm', extend='both', 
                     norm=norm, levels=np.linspace(vmin, vmax, 11))
    
    # Barra de cores
    cbar = fig.colorbar(im)
    cbar.set_label('[K / Day]', fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Configurar eixo y como logarítmico
    ax.invert_yaxis()
    ax.set_ylim(1000, 100)
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_ylabel("Pressure (hPa)", fontsize=14)

    # Linhas verticais em datas específicas
    for time in ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']:
        ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

    # Formatação do eixo x
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %HZ'))
    ax.tick_params(axis='x', labelrotation=45)

    # Configurar título e rótulos dos eixos
    ax.set_title(f'Akará - {label} - EXP:track', fontsize=12, loc='left')

    # Salvar o gráfico
    plt.savefig(DIRFIGS + f"{nome_arquivo}_track_hov_custom.png", bbox_inches='tight', dpi=300)
    plt.close()

print("\nTodos os gráficos foram gerados com sucesso!")
