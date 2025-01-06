import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os

# ======================== SETUP DE CONFIGURAÇÃO ========================
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

# Configurações específicas para cada arquivo
configs = {
    'AdvHZeta': {'label': 'Horizontal Vorticity Advection', 'vmin': -1.5e-9, 'vmax': 5e-9},
    'AdvVZeta': {'label': 'Vertical Vorticity Advection', 'vmin': -1e-9, 'vmax': 2e-9},
    'dZdt': {'label': 'Local Vorticity Tendency', 'vmin': -1.5e-9, 'vmax': 1.5e-9},
    'vxBeta': {'label': 'Planetary Vorticity Advection', 'vmin': -1e-9, 'vmax': 1e-9},
    'ZetaDivH': {'label': 'Stretching Term zeta', 'vmin': -5.5e-9, 'vmax': 1e-9},
    'fDivH': {'label': 'Stretching Term f', 'vmin': -2e-9, 'vmax': 1e-9},
    'Tilting': {'label': 'Tilting Term', 'vmin': -1e-9, 'vmax': 2e-9},
    'ResZ': {'label': 'Friction Residual', 'vmin': -1.2e-9, 'vmax': 3e-9},
    'tilt_advV': {'label': 'Tilting + Vertical Vorticity Advection', 'vmin': -1e-9, 'vmax': 2e-9}
}

# Intervalos de datas para as fases
date_intervals = [
    ('2024-02-14T21', '2024-02-16T09'),  # Incipiente
    ('2024-02-16T09', '2024-02-19T15'),  # Intensificação
    ('2024-02-19T15', '2024-02-20T06'),  # Maturação
    ('2024-02-20T06', '2024-02-22T21')   # Declínio
]

# Nomes das fases e cores associadas
curves = ['Incipient', 'Intensification', 'Maturation', 'Decay']
colors = ['#65a1e6', '#f7b538', '#d62828', '#9aa981']  # Cores acessíveis para daltonismo

# Lista de marcadores diferentes
markers = ['x', 'o', '^', 's', 'd', 'p', 'H', '*']

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
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plotar cada fase usando os intervalos de datas
    for idx, (date1, date2) in enumerate(date_intervals):
        selected_data = df.loc[:, date1:date2]
        selected_data_mean = selected_data.mean(axis=1)

        # Usar marcadores diferentes para cada curva
        ax.plot(
            selected_data_mean, df.index, 
            label=curves[idx], color=colors[idx], 
            marker=markers[idx], markerfacecolor='white', markersize=7
        )

    # Customizações do gráfico
    ax.axvline(0, c='k', linewidth=0.75)  # Linha vertical em x=0
    ax.invert_yaxis()
    ax.set_ylim(1000, 100)
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_xlabel('[1/s²]', fontsize=18)
    ax.set_ylabel('Pressure (hPa)', fontsize=18)
    ax.set_xlim([config['vmin'], config['vmax']])
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.7, linewidth=0.5)
    
    # Formatação do título e eixos
    ax.set_title(f"Akará - {config['label']} - EXP:track", fontsize=18, loc='left')
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax.tick_params(axis='x', labelsize=18)  # Aumentar tamanho dos valores no eixo x
    ax.tick_params(axis='y', labelsize=18)

    # Fundo do gráfico
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')

    # Legenda e layout
    plt.legend(fontsize=14)
    plt.tight_layout()

    # Salvar a figura
    caminho_fig = os.path.join(DIRFIGS, f"{nome_arquivo}_track.png")
    plt.savefig(caminho_fig, dpi=300)
    plt.close()

    print(f"Figura salva: {caminho_fig}")
