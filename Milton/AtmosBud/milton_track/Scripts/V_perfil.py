import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os

# ======================== SETUP DE CONFIGURAÇÃO ========================
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Milton/AtmosBud/milton_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Milton/AtmosBud/milton_track/Figures/V_balanc_track/'

# Configurações específicas para cada arquivo
configs = {
    'AdvHZeta': {'label': 'Horizontal Vorticity Advection', 'vmin': -1e-8, 'vmax': 1e-8},
    'AdvVZeta': {'label': 'Vertical Vorticity Advection', 'vmin': -0.5e-8, 'vmax': 0.5e-8},
    'dZdt': {'label': 'Local Vorticity Tendency', 'vmin': -0.2e-8, 'vmax': 0.2e-8},
    'vxBeta': {'label': 'Planetary Vorticity Advection', 'vmin': -0.1e-8, 'vmax': 0.1e-8},
    'ZetaDivH': {'label': 'Stretching Term zeta', 'vmin': -1e-8, 'vmax': 1e-8},
    'fDivH': {'label': 'Stretching Term f', 'vmin': -0.3e-8, 'vmax': 0.3e-8},
    'Tilting': {'label': 'Tilting Term', 'vmin': -2e-8, 'vmax': 2e-8},
    'ResZ': {'label': 'Friction Residual', 'vmin': -0.8e-8, 'vmax': 0.5e-8},
    'tilt_advV': {'label': 'Tilting + Vertical Vorticity Advection', 'vmin': -0.5e-8, 'vmax': 0.5e-8}
}

# Intervalos de datas para as fases
date_intervals = [
    ('2024-10-04T00', '2024-10-05T00'),
    ('2024-10-05T00', '2024-10-06T00'),
    ('2024-10-06T00', '2024-10-07T00'),
    ('2024-10-07T00', '2024-10-08T00'),
    ('2024-10-08T00', '2024-10-09T00'),
    ('2024-10-09T00', '2024-10-10T00'),
    ('2024-10-10T00', '2024-10-10T18')
]

# Nomes das fases e cores associadas
curves = ['2024-10-04', '2024-10-05', '2024-10-06', '2024-10-07', '2024-10-08', 
          '2024-10-09', '2024-10-10']
colors = ['#0072B2', '#D55E00', '#F0E442', '#56B4E9', '#009E73', '#CC79A7', '#E69F00']

# ========================== LOOP PRINCIPAL ============================
for nome_arquivo, config in configs.items():
    caminho_arquivo = os.path.join(DIRDADO, nome_arquivo + '.csv')

    # Verificar se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Arquivo {caminho_arquivo} não encontrado. Pulando...")
        continue

    # Ler o arquivo CSV
    df = pd.read_csv(caminho_arquivo, index_col=[0])
    df.index = df.index / 100  # Ajustar índice (assumindo que está em decapascais)
    df.columns = pd.to_datetime(df.columns).strftime('%Y-%m-%dT%H')

    # Criar subplots
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plotar cada fase usando os intervalos de datas
    for idx, (date1, date2) in enumerate(date_intervals):
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)

        ax.plot(
            selected_data_mean, df.index, 
            label=curves[idx], color=colors[idx], 
            marker='x', markerfacecolor='white', markersize=5
        )

    # Customizações do gráfico
    ax.axvline(0, c='k', linewidth=0.75)  # Linha vertical em x=0
    ax.invert_yaxis()
    ax.set_ylim(1000, 100)
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_xlabel('[1/s²]', fontsize=11)
    ax.set_ylabel('Pressure (hPa)', fontsize=12)
    ax.set_xlim([config['vmin'], config['vmax']])
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)
    
    # Formatação do título e eixos
    ax.set_title(f"Milton - {config['label']} - EXP:track", fontsize=12, loc='left')
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Fundo do gráfico
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')

    # Legenda e layout
    plt.legend()
    plt.tight_layout()

    # Salvar a figura
    caminho_fig = os.path.join(DIRFIGS, f"{nome_arquivo}_track.png")
    plt.savefig(caminho_fig, dpi=300)
    plt.close()

    print(f"Figura salva: {caminho_fig}")
