import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Carregar os dados do arquivo CSV
cps = pd.read_csv('cps_completo.csv', sep=',')

# Exibir as primeiras linhas e as colunas do DataFrame para verificação
print(cps.head())
print()
print(cps.columns)
cps['time.1'] = cps['time.1'].astype(str)
# Selecionar os dados pulando um de cada vez (passo 2)
cps = cps.iloc[::2]

print(cps['time.1'].head())
print()
print(cps['time.1'].tail())

# Criar a coluna B, que é a diferença entre B_left e B_right
cps['B'] = cps['B_left'] - cps['B_right']

# Ordenar os dados pela coluna 'time.1' (sequência temporal)
#cps = cps.sort_values(by='time.1')

# Criar uma figura com 2 subgráficos (1 linha e 2 colunas)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

#tropical
axes[0].fill_betweenx([-20, 10], 0, 100, color='red', alpha=0.2)
#subtropical
axes[0].fill_betweenx([-25, 25], -50, 100, color='green', alpha=0.2)

# Gráfico 1: VTL vs B
axes[0].scatter(cps['VTL'], cps['B'], alpha=0.7)
axes[0].plot(cps['VTL'], cps['B'], alpha=0.7)
axes[0].axhline(10, color='black', linewidth=2, linestyle='--')  # Linha horizontal no eixo y = 0
axes[0].axvline(0, color='black', linewidth=2, linestyle='--')  # Linha vertical no eixo x = 0
axes[0].set_title('V$_{T}$$^{L}$ vs B', fontsize=18)
axes[0].set_xlabel('-V$_{T}$$^{L}$ [Low Level Thermal Wind]', fontsize=18)
axes[0].set_ylabel(r'B [Low Level Thickness asymmetry]', fontsize=18)
axes[0].grid(False)
axes[0].set_xlim(-30, 100)  # Definir limite do eixo x de -100 a 100
axes[0].set_ylim(-20, 20)  # Definir limite do eixo y de -100 a 100
axes[0].tick_params(axis='x', labelsize=16)  # Tamanho da fonte do eixo X
axes[0].tick_params(axis='y', labelsize=16)  # Tamanho da fonte do eixo Y
# Adicionar os índices no gráfico
for i, txt in enumerate(cps['time.1'][::].str[-6:-2]):
    axes[0].annotate(txt, (cps['VTL'].iloc[i], cps['B'].iloc[i]), fontsize=8, color='red')

#tropical
axes[1].fill_betweenx([0, 100], 0, 100, color='red', alpha=0.2)
axes[1].fill_betweenx([-120, -10], -50, 100, color='green', alpha=0.2)

# Gráfico 2: VTL vs VTU
axes[1].scatter(cps['VTL'], cps['VTU'], alpha=0.7)
axes[1].plot(cps['VTL'], cps['VTU'], alpha=0.7)  # Conectar os pontos com uma linha
axes[1].axhline(0, color='black', linewidth=2, linestyle='--')  # Linha horizontal no eixo y = 0
axes[1].axvline(0, color='black', linewidth=2, linestyle='--')  # Linha vertical no eixo x = 0
axes[1].set_title(r'V$_{T}$$^{L}$ vs V$_{T}$$^{U}$', fontsize=18)
axes[1].set_xlabel('-V$_{T}$$^{L}$ [Low Level Thermal Wind]', fontsize=18)
axes[1].set_ylabel('-V$_{T}$$^{U}$ [High Level Thermal Wind]', fontsize=18)
axes[1].grid(False)
axes[1].set_xlim(-50, 100)  # Definir limite do eixo x de -100 a 100
axes[1].set_ylim(-120, 100)  # Definir limite do eixo y de -100 a 100
axes[1].tick_params(axis='x', labelsize=16)  # Tamanho da fonte do eixo X
axes[1].tick_params(axis='y', labelsize=16)  # Tamanho da fonte do eixo Y

# Adicionar os índices no gráfico
for i, txt in enumerate(cps['time.1'][::].str[-6:-2]):
    axes[1].annotate(txt, (cps['VTL'].iloc[i], cps['VTU'].iloc[i]), fontsize=8, color='red')


# Ajustar o layout para evitar sobreposição
plt.tight_layout()

# Mostrar o gráfico
plt.savefig('teste.png', dpi=300)

