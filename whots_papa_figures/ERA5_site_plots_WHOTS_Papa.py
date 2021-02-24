# -*- coding: utf-8 -*-
"""
Make plots of ERA5 surface conditions at Papa, WHOTS, NTAS, Stratus

Created on Fri Jan 22 19:38:04 2021

@author: jtomfarrar
jfarrar@whoi.edu
"""
import glob
import xarray as xr
import nc_time_axis
import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os
# I need this to make basemap work
os.environ['PROJ_LIB'] = r'C:\Users\jtomf\anaconda3\pkgs\cartopy-0.18.0-py38h2a8b5ed_8\Lib\site-packages\cartopy'
# import proplot as plot

site_name = 'WHOTS-Papa'  # can be 'NTAS', 'WHOTS', 'Stratus', or 'Papa'
lon_ptW = -158  # WHOTS=-158
lat_ptW = 22.67  # WHOTS=22.67
lon_ptP = -145  # Papa
lat_ptP = 50  # Papa

__figdir__ = site_name
savefig_args = {'bbox_inches': 'tight', 'pad_inches': 0}

# Define path using the r prefix (which means raw string so that special character / should not be evaluated)
path = r"C:\Users\jtomf\Documents\Python\ERA5_plots"

# Get a list of all relevant .nc files
filenamesW = glob.glob(path+'/ERA5_surface_WHOTS_*.nc')
ERAW = xr.open_mfdataset(filenamesW, combine='nested', concat_dim='time')
timeW = ERAW.time  # 'days since 1950-01-01 00:00:00'

filenamesP = glob.glob(path+'/ERA5_surface_Papa_*.nc')
ERAP = xr.open_mfdataset(filenamesP, combine='nested', concat_dim='time')
timeP = ERAP.time  # 'days since 1950-01-01 00:00:00'

tind = 0
sstW = ERAW.sst[tind, :, :]-273.15
atmpW = ERAW.t2m[tind, :, :]-273.15
swhW = ERAW.swh[tind, :, :]
UW = ERAW.u10[tind, :, :]
VW = ERAW.v10[tind, :, :]
lonW = ERAW.longitude
latW = ERAW.latitude
lonmeshW, latmeshW = np.meshgrid(lonW, latW)
# There is something off with SWH-- it seems the resolution is half as fine and
#   and the data have been padded to have the same shape as SST, etc
ny, nx = np.shape(swhW)
swhW = swhW[0:round(ny/2)+1, 0:round(nx/2)+1]
lonWw = lonW[0:nx:2]
latWw = latW[0:ny:2]
lonmeshWw, latmeshWw = np.meshgrid(lonWw, latWw)

ffxW = np.where(np.abs(lonW[:].data-lon_ptW) ==
                np.min(np.abs(lonW[:].data-lon_ptW)))
ffyW = np.where(np.abs(latW[:].data-lat_ptW) ==
                np.min(np.abs(latW[:].data-lat_ptW)))
ffxW = np.squeeze(ffxW)
ffyW = np.squeeze(ffyW)
sst0W = ERAW.sst[:, ffyW, ffxW]-273.15
atmp0W = ERAW.t2m[:, ffyW, ffxW]-273.15
u0W = ERAW.u10[:, ffyW, ffxW]
v0W = ERAW.v10[:, ffyW, ffxW]

# Wave parameters are on a lower-res lat/lon grid:
ffxWw = np.where(np.abs(lonWw[:].data-lon_ptW) ==
                 np.min(np.abs(lonWw[:].data-lon_ptW)))
ffyWw = np.where(np.abs(latWw[:].data-lat_ptW) ==
                 np.min(np.abs(latWw[:].data-lat_ptW)))
ffxWw = np.squeeze(ffxWw)
ffyWw = np.squeeze(ffyWw)
swh0W = ERAW.swh[:, ffyWw, ffxWw]


sstP = ERAP.sst[tind, :, :]-273.15
atmpP = ERAP.t2m[tind, :, :]-273.15
swhP = ERAP.swh[tind, :, :]
UP = ERAP.u10[tind, :, :]
VP = ERAP.v10[tind, :, :]
lonP = ERAP.longitude
latP = ERAP.latitude
lonmeshP, latmeshP = np.meshgrid(lonP, latP)
# There is something off with SWH-- it seems the resolution is half as fine and
#   and the data have been padded to have the same shape as SST, etc
ny, nx = np.shape(swhP)
swhP = swhP[0:round(ny/2)+1, 0:round(nx/2)+1]
lonPw = lonP[0:nx:2]
latPw = latP[0:ny:2]
lonmeshPw, latmeshPw = np.meshgrid(lonPw, latPw)

ffxP = np.where(np.abs(lonP[:].data-lon_ptP) ==
                np.min(np.abs(lonP[:].data-lon_ptP)))
ffyP = np.where(np.abs(latP[:].data-lat_ptP) ==
                np.min(np.abs(latP[:].data-lat_ptP)))
ffxP = np.squeeze(ffxP)
ffyP = np.squeeze(ffyP)
sst0P = ERAP.sst[:, ffyP, ffxP]-273.15
atmp0P = ERAP.t2m[:, ffyP, ffxP]-273.15
u0P = ERAP.u10[:, ffyP, ffxP]
v0P = ERAP.v10[:, ffyP, ffxP]

# Wave parameters are on a lower-res lat/lon grid:
ffxPw = np.where(np.abs(lonPw[:].data-lon_ptP) ==
                 np.min(np.abs(lonPw[:].data-lon_ptP)))
ffyPw = np.where(np.abs(latPw[:].data-lat_ptP) ==
                 np.min(np.abs(latPw[:].data-lat_ptP)))
ffxPw = np.squeeze(ffxPw)
ffyPw = np.squeeze(ffyPw)
swh0P = ERAP.swh[:, ffyPw, ffxPw]


plt.close('all')
#############################


##############################
# Try doing plot with matplotlib API approach:
fig, axs = plt.subplots(4, 1, sharex=True)
axs[0].plot(timeW, sst0W, lw=2)
axs[0].set(ylabel='[$^\circ$C]')
axs[0].legend(['SST'])
axs[1].plot(timeW, swh0W)
axs[1].set(ylabel='[m]')
axs[1].legend('Signif. Wave Height')
axs[2].plot(timeW, atmp0W)
axs[2].set(ylabel='[m]')
axs[2].legend('Air temp')
axs[3].plot(timeW, np.sqrt(u0W**2+v0W**2))
axs[3].set(ylabel='[m/s]')
axs[3].legend('Wind speed')


#############################
fig, axs = plt.subplots(1, 2,figsize=(7,3.5))
axs[0,].hist(np.sqrt(u0W**2+v0W**2), 30, density=True, edgecolor='k',alpha=1)
axs[0,].hist(np.sqrt(u0P**2+v0P**2), 30, density=True, edgecolor='k',alpha=0.65)
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Probablility density')
axs[0,].set(xlabel='Wind speed (m/s)', ylabel='Probablility density')
axs[0,].legend(['WHOTS','Stn. Papa'])

axs[1,].hist(swh0W, 30, density=True, edgecolor='k',alpha=1)
axs[1,].hist(swh0P, 30, density=True, edgecolor='k',alpha=0.65)
plt.xlabel('Wave height (m)')
plt.ylabel('Probablility density')
axs[1,].set(xlabel='Wave height (m)', ylabel='Probablility density')
axs[1,].legend(['WHOTS','Stn. Papa'])
plt.tight_layout()
plt.savefig(__figdir__+'_stats', **savefig_args)

fhfhgf


#############################
# Wind/wave statistics
fig=plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
n, bins, patches=plt.hist(np.sqrt(u0**2+v0**2), 30,
                          density=True, edgecolor='k')
plt.title('ERA5 ' + site_name + '(' + str(round(float(
    lat[ffy]), 4)) + '$^\circ$N, ' + str(round(float(lon[ffx]), 4)) + '$^\circ$E)')
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Probablility density')

plt.subplot(1, 2, 2)
n, bins, patches=plt.hist(swh0, 30, density=True, edgecolor='k')
# plt.title('ERA5 ' + site_name + '('+ str(round(float(lat[ffy]),4)) + '$^\circ$N, ' + str(round(float(lon[ffx]),4)) + '$^\circ$E)' + ' SWH PDF')
plt.xlabel('Signif. Wave Height (m)')
plt.ylabel('Probablility density')
plt.savefig(__figdir__+'_stats', **savefig_args)

# Air temp statistics
fig=plt.figure(figsize=(8, 4))
n, bins, patches=plt.hist(atmp0, 30, density=True, edgecolor='k')
plt.title('ERA5 ' + site_name + '(' + str(round(float(
    lat[ffy]), 4)) + '$^\circ$N, ' + str(round(float(lon[ffx]), 4)) + '$^\circ$E)')
plt.xlabel('Air temp ($^\circ$C)')
plt.ylabel('Probablility density')
plt.savefig(__figdir__+'_atmp_stats', **savefig_args)
