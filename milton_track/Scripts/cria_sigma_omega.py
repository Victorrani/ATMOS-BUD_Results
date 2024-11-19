import xarray as xr
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd

DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD_Results/milton_track/'

omega_csv = 'Omega.csv'
sigma_csv = 'Sigma.csv'

omega = pd.read_csv(DIRDADO+omega_csv, index_col=[0])
print(omega.head())
print('')
sigma = pd.read_csv(DIRDADO+sigma_csv, index_col=[0])
print(sigma.head())

sigma_omega_csv = 'Sigma_omega.csv'
df_sigma_omega = sigma * omega
df_sigma_omega.to_csv(DIRDADO+sigma_omega_csv,index='True')
print(df_sigma_omega.head())