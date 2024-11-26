import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/milton_fixed/'

tilt_csv = 'Tilting.csv'
advV_csv = 'AdvVZeta.csv'

tilt = pd.read_csv(DIRDADO+tilt_csv, index_col=[0])
advV = pd.read_csv(DIRDADO+advV_csv, index_col=[0])


tilt_advV = 'tilt_advV.csv'
df_tilt_advV = tilt + advV
df_tilt_advV.to_csv(DIRDADO+tilt_advV,index='True')
print(df_tilt_advV.head())
