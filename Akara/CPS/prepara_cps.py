import pandas as pd


DIRCSV = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/Akara/Charts/csv_files/track_csv_formatado.csv'

arquivo = 'parameters_CPS3.xlsx'
arquivo2 = DIRCSV

cps = pd.read_excel(arquivo)
track = pd.read_csv(DIRCSV, sep=',')

print(cps.tail())

print()

print(track.tail())

df_merged = pd.concat([cps, track], axis=1)

print()
print(df_merged.tail())

# Salvar o DataFrame em um arquivo CSV
df_merged.to_csv('cps_comleto.csv', index=False, sep=',')
