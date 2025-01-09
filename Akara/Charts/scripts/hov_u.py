import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import cartopy, cartopy.crs as ccrs
import matplotlib.colors as mcolors
import matplotlib.colors
import metpy.calc as mpcalc
from metpy.calc import equivalent_potential_temperature
from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity
from metpy.interpolate import cross_section
import cartopy.io.shapereader as shpreader
import matplotlib.colors as cm
from datetime import datetime
import pandas as pd

# Definindo diretórios
DIRDADO = '/home/victor/USP/sinotica3/ATMOS-BUD/dados/'

arquivo = 'akara_hov.nc'

ds = xr.open_dataset(DIRDADO+arquivo)

u = ds['u'][:].sel[pressure_leve=30]
lon = ds['longitude'][:]
time =ds['valid_time']

