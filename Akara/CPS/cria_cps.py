import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Carregar os dados do arquivo CSV
cps = pd.read_csv('cps_completo.csv', sep=',')

# Criar a coluna B, que é a diferença entre B_left e B_right
cps['B'] = cps['B_left'] - cps['B_right']

# Calcular médias móveis
for col in ["B", "VTL", "VTU"]:
    nova_coluna = f"{col}_media_movel"
    cps[nova_coluna] = cps[col].rolling(window=5, center=True).mean()

cps_filtered = cps.dropna(subset=['B_media_movel', 'VTL_media_movel', 'VTU_media_movel'])
cps_filtered['time'] = cps_filtered['time'].astype(str)

# Criar uma figura com 2 subgráficos (1 linha e 2 colunas)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Criar um conjunto para rastrear itens únicos da legenda
legend_items = {}

# Gráfico 1: VTL vs B
axes[0].fill_betweenx([-20, 10], 0, 100, color='#d62828', alpha=0.2)  # Tropical
axes[0].fill_betweenx([-25, 25], -50, 100, color='#a7c957', alpha=0.2)  # Subtropical
#axes[0].fill_betweenx([10, 20], -20, 0, color='#0077b6', alpha=0.2)  # Extratropical


# Adicionar linhas conectando os pontos
axes[0].plot(cps_filtered['VTL_media_movel'], cps_filtered['B_media_movel'], color='black', alpha=0.5, linewidth=1)



# Adicionar pontos com símbolos e cores
# Loop para plotar pontos e adicionar rótulos de 2 em 2
for idx, row in enumerate(cps_filtered.iterrows()):
    _, row = row  # Extrai a linha atual do iterador
    # Plotar os pontos
    axes[0].scatter(row['VTL_media_movel'], row['B_media_movel'],
                    color=row['color'], marker=row['symbol'], s=30,
                    linewidth=2)
    # Criar itens únicos para a legenda
    if row['phase'] not in legend_items:
        legend_items[row['phase']] = mlines.Line2D([], [], color=row['color'],
                                                   marker=row['symbol'], linestyle='None',
                                                   markersize=8, label=row['phase'])
    # Adicionar rótulos de 2 em 2 a partir do quarto ponto
    if idx >= 3 and (idx - 3) % 8 == 0:  # Começa no quarto ponto e segue a lógica de 4 em 4
        axes[0].annotate(row['time'][6:-2], (row['VTL_media_movel'], row['B_media_movel']),
                         fontsize=8, color='black', alpha=0.7,
                         xytext=(-10, -10), textcoords='offset points')
        
datas_destaque = ["202402142100", "202402152100", "202402162100",
                   "202402172100", "202402191500", "202402201200"]


# Filtre os dados de destaque
destaques = cps_filtered[cps_filtered['time'].isin(datas_destaque)]

print(destaques['symbol'])

axes[0].scatter(destaques['VTL_media_movel'].iloc[0], destaques['B_media_movel'].iloc[0],
            color=destaques['color'].iloc[0], marker=destaques['symbol'].iloc[0], s=150,
            linewidth=2, edgecolor='black')
axes[0].scatter(destaques['VTL_media_movel'].iloc[1], destaques['B_media_movel'].iloc[1],
            color=destaques['color'].iloc[1], marker=destaques['symbol'].iloc[1], s=150,
            linewidth=2, edgecolor='black')
axes[0].scatter(destaques['VTL_media_movel'].iloc[2], destaques['B_media_movel'].iloc[2],
            color=destaques['color'].iloc[2], marker=destaques['symbol'].iloc[2], s=150,
            linewidth=2, edgecolor='black')
axes[0].scatter(destaques['VTL_media_movel'].iloc[3], destaques['B_media_movel'].iloc[3],
            color=destaques['color'].iloc[3], marker=destaques['symbol'].iloc[3], s=150,
            linewidth=2, edgecolor='black')
axes[0].scatter(destaques['VTL_media_movel'].iloc[4], destaques['B_media_movel'].iloc[4],
            color=destaques['color'].iloc[4], marker=destaques['symbol'].iloc[4], s=150,
            linewidth=2, edgecolor='black')
#
#print(destaques['symbol'].unique())
axes[0].axhline(10, color='black', linewidth=2, linestyle='--')  # Linha horizontal
axes[0].axvline(0, color='black', linewidth=2, linestyle='--')  # Linha vertical
axes[0].set_title('Akará 20240214 21Z - 20240222 21Z', fontsize=18, loc='left')
axes[0].set_xlabel('-V$_{T}$$^{L}$ [Low Level Thermal Wind]', fontsize=18)
axes[0].set_ylabel(r'B [Low Level Thickness asymmetry]', fontsize=18)
axes[0].grid(False)
axes[0].set_xlim(-20, 100)
axes[0].set_ylim(-20, 20)
axes[0].tick_params(axis='x', labelsize=16)
axes[0].tick_params(axis='y', labelsize=16)

# Gráfico 2: VTL vs VTU
axes[1].fill_betweenx([0, 100], 0, 100, color='#d62828', alpha=0.2)  # Tropical
axes[1].fill_betweenx([-120, -10], -50, 100, color='#a7c957', alpha=0.2)  # Subtropical
#axes[1].fill_betweenx([-120, 0], -20, 0, color='#0077b6', alpha=0.2)  # Extratropical

# Adicionar linhas conectando os pontos
axes[1].plot(cps_filtered['VTL_media_movel'], cps_filtered['VTU_media_movel'], color='black', alpha=1, linewidth=1)

for idx, row in enumerate(cps_filtered.iterrows()):
    _, row = row  # Extrai a linha atual do iterador
    # Plotar os pontos
    axes[1].scatter(row['VTL_media_movel'], row['VTU_media_movel'],
                    color=row['color'], marker=row['symbol'], s=30,
                    linewidth=2)
    # Criar itens únicos para a legenda
    if row['phase'] not in legend_items:
        legend_items[row['phase']] = mlines.Line2D([], [], color=row['color'],
                                                   marker=row['symbol'], linestyle='None',
                                                   markersize=8, label=row['phase'])
    # Adicionar rótulos de 2 em 2 a partir do quarto ponto
    if idx >= 3 and (idx - 3) % 8 == 0:  # Começa no quarto ponto e segue a lógica de 4 em 4
        axes[1].annotate(row['time'][6:-2], (row['VTL_media_movel'], row['VTU_media_movel']),
                         fontsize=8, color='black', alpha=0.7,
                         xytext=(-10, -10), textcoords='offset points')

datas_destaque = ["202402142100", "202402152100", "202402162100",
                   "202402172100", "202402191500", "202402201200"]


# Filtre os dados de destaque
destaques = cps_filtered[cps_filtered['time'].isin(datas_destaque)]

print(destaques['symbol'])

axes[1].scatter(destaques['VTL_media_movel'].iloc[0], destaques['VTU_media_movel'].iloc[0],
            color=destaques['color'].iloc[0], marker=destaques['symbol'].iloc[0], s=150,
            linewidth=2, edgecolor='black')
axes[1].scatter(destaques['VTL_media_movel'].iloc[1], destaques['VTU_media_movel'].iloc[1],
            color=destaques['color'].iloc[1], marker=destaques['symbol'].iloc[1], s=150,
            linewidth=2, edgecolor='black')
axes[1].scatter(destaques['VTL_media_movel'].iloc[2], destaques['VTU_media_movel'].iloc[2],
            color=destaques['color'].iloc[2], marker=destaques['symbol'].iloc[2], s=150,
            linewidth=2, edgecolor='black')
axes[1].scatter(destaques['VTL_media_movel'].iloc[3], destaques['VTU_media_movel'].iloc[3],
            color=destaques['color'].iloc[3], marker=destaques['symbol'].iloc[3], s=150,
            linewidth=2, edgecolor='black')
axes[1].scatter(destaques['VTL_media_movel'].iloc[4], destaques['VTU_media_movel'].iloc[4],
            color=destaques['color'].iloc[4], marker=destaques['symbol'].iloc[4], s=150,
            linewidth=2, edgecolor='black')

axes[1].axhline(0, color='black', linewidth=2, linestyle='--')  # Linha horizontal
axes[1].axvline(0, color='black', linewidth=2, linestyle='--')  # Linha vertical
axes[1].set_title(r'Akará 20240214 21Z - 20240222 21Z', fontsize=18, loc='left')
axes[1].set_xlabel('-V$_{T}$$^{L}$ [Low Level Thermal Wind]', fontsize=18)
axes[1].set_ylabel('-V$_{T}$$^{U}$ [High Level Thermal Wind]', fontsize=18)
axes[1].grid(False)
axes[1].set_xlim(-20, 100)
axes[1].set_ylim(-120, 100)
axes[1].tick_params(axis='x', labelsize=16)
axes[1].tick_params(axis='y', labelsize=16)

# Adicionar a mesma legenda em ambos os gráficos
handles = list(legend_items.values())
axes[0].legend(handles=handles, loc='upper left', fontsize=12)
axes[1].legend(handles=handles, loc='upper left', fontsize=12)



# Ajustar o layout para evitar sobreposição
plt.tight_layout()

# Salvar o gráfico
plt.savefig('cps_total_master.png', dpi=300, bbox_inches='tight')

