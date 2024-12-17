import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.ticker import ScalarFormatter
from matplotlib.dates import DateFormatter

# Diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/'
DIRFIGS = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/AtmosBud/akara1_track/Figures/V_balanc_track/'

# Configurações dos arquivos
configs = {
    'AdvHZeta': {'label': 'Horizontal Vorticity Advection', 'vmin': -3e-9, 'vmax': 3e-9},
    'AdvVZeta': {'label': 'Vertical Vorticity Advection', 'vmin': -1.5e-9, 'vmax': 1.2e-9},
    'dZdt': {'label': 'Local Vorticity Tendency', 'vmin': -1.5e-9, 'vmax': 1.5e-9},
    'vxBeta': {'label': 'Planetary Vorticity Advection', 'vmin': -0.5e-9, 'vmax': 0.5e-9},
    'ZetaDivH': {'label': 'Stretching Term zeta', 'vmin': -1.3e-9, 'vmax': 1.3e-9},
    'fDivH': {'label': 'Stretching Term f', 'vmin': -1.5e-9, 'vmax': 1.5e-9},
    'Tilting': {'label': 'Tilting Term', 'vmin': -1e-9, 'vmax': 1e-9},
    'ResZ': {'label': 'Friction Residual', 'vmin': -2e-9, 'vmax': 2e-9},
    'tilt_advV': {'label': 'Tilting + Vertical Vorticity Advection', 'vmin': -1.5e-9, 'vmax': 1.5e-9}
}

# Datas de destaque
highlight_times = ['2024-02-14T21', '2024-02-16T09', '2024-02-19T15', '2024-02-20T06']

# Loop pelos arquivos usando configs
for arq, config in configs.items():
    # Caminho do arquivo e título
    file_path = DIRDADO + arq + '.csv'
    nome_arquivo = arq
    label = config['label']
    vmin = config['vmin']
    vmax = config['vmax']

    # Carregar dados
    df = pd.read_csv(file_path, index_col=[0])

    # Converter colunas para datetime e ajustar índice de pressão
    df.columns = pd.to_datetime(df.columns, utc=True).tz_convert(None)
    df.index = df.index / 100  # Ajuste da pressão (hPa)

    # Configuração do colormap
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(8, 6))

    # Contorno preenchido
    im = ax.contourf(df.columns, df.index, df.values, cmap='coolwarm', extend='both',
                     norm=norm, levels=np.linspace(vmin, vmax, 11))


    # Inverter o eixo y
    ax.invert_yaxis()
    ax.set_ylim(1000, 100)
    ax.set_yscale('log')
    ax.set_yticks([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_yticklabels([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100])
    ax.set_ylabel("Pressure (hPa)", fontsize=14)

    # Adicionar linhas verticais
    for time in highlight_times:
        ax.axvline(pd.to_datetime(time), color='k', linestyle='--')

    # Formatar eixo x (datas)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.tick_params(axis='x', labelrotation=45)

    # Configurar título e rótulos
    ax.set_title(f'Akará - {label} - EXP: track', fontsize=12, loc='left')
    ax.set_ylabel('Pressure (hPa)', fontsize=14)

    # Adicionar barra de cores
    cbar = fig.colorbar(im)
    cbar.set_label('[1 / s²]', fontsize=12)
    cbar.ax.tick_params(labelsize=10)

    # Formatação científica na barra de cores
    cbar.formatter = ScalarFormatter(useMathText=True)
    cbar.formatter.set_scientific(True)
    cbar.formatter.set_powerlimits((-3, 3))
    cbar.update_ticks()

    # Salvar figura
    output_file = DIRFIGS + nome_arquivo + '_hov.png'
    plt.savefig(output_file, bbox_inches='tight')
    print(f"Gráfico salvo: {output_file}")

    # Fechar figura
    plt.close()
