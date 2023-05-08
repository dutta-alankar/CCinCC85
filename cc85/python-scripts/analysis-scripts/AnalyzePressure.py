# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:03:31 2023

@author: alankar
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import h5py
from scipy.interpolate import interp1d
import os

os.system('mkdir -p ./analysis-plots')

# constants
mu = 0.61
mp = 1.676e-24
Msun = 2e33
yr = 365*24*60**2
pc = 3.0857e18
kB = 1.38e-16
gamma = 5/3.
xH    = 0.76

dir = './output'

cc85 = np.loadtxt(f'{dir}/analysis.dat')

chi = 100
Rcl = 8.8*pc
Tcl = 4e4
mass = []
vol  = []
tcc = []
vol_all = []
centroid = []
asymetry = []
prp = []
par = []

for snap in range(14):
    print(snap, end='\r')
    step = 20
    tcc.append(snap*step/np.sqrt(chi))
    with h5py.File(f'{dir}/data.%04d.dbl.h5'%snap, 'r') as data:
        dV = np.array(data['/Timestep_%d/vars/cellvol'%snap]).flatten()
        temperature = np.array(data['/Timestep_%d/vars/temperature'%snap]).flatten()
        ndens = np.array(data['/Timestep_%d/vars/ndens'%snap]).flatten()
        pres = np.array(data['/Timestep_%d/vars/pressure'%snap]).flatten()

        x = np.array(data['/cell_coords/X']).flatten()
        y = np.array(data['/cell_coords/Y']).flatten()
        z = np.array(data['/cell_coords/Z']).flatten()

        distance = np.sqrt(x**2 + y**2 + z**2)

        condition = temperature<(3.3*Tcl)

        pres_all = np.copy(pres)
        distance_all = np.copy(distance)
        dV_all = np.copy(dV)

        distance = distance[condition]
        pres = pres[condition]
        dV = dV[condition]

        pres_avg_all = np.zeros_like(pres)
        pres_avg_cloud = np.zeros_like(pres)

        rad_pnts = 50
        radius = np.linspace(np.min(distance), np.max(distance), rad_pnts)
        for i, rad in enumerate(radius):
            if i==0: rad_cond = np.logical_and(distance_all>=0.95*rad, distance_all<=radius[i-1])
            elif (i==(rad_pnts-1)): rad_cond = np.logical_and(distance_all>radius[i-1], distance_all<=1.05*rad)
            else: rad_cond = np.logical_and(distance_all>radius[i-1], distance_all<=rad)

            avg = np.average(pres_all[rad_cond])

            if i==0: rad_cond = np.logical_and(distance>=0.95*rad, distance<=radius[i-1])
            elif (i==(rad_pnts-1)): rad_cond = np.logical_and(distance>radius[i-1], distance<=1.05*rad)
            else: rad_cond = np.logical_and(distance>radius[i-1], distance<=rad)

            indx = np.where(rad_cond)
            for j in indx:
                pres_avg_all[j] = avg

            avg = np.average(pres[rad_cond])
            for j in indx:
                pres_avg_cloud[j] = avg


        pres_all = pres/pres_avg_all
        pres_cloud = pres/pres_avg_cloud

        # condition = tracer>1e-4

        plt.figure(figsize=(13,10))
        # Create the histogram in log space
        plt.hist(np.log10(pres_all),   bins=100, weights=dV, density=True, color='tab:blue', label='All gas')
        plt.hist(np.log10(pres_cloud), bins=100, weights=dV, density=True, color='tab:red', alpha=0.5, label='Only cold gas')
        # plt.colorbar()
        # plt.xscale('log')
        # plt.yscale('log')
        plt.xlim(xmin=-1.0, xmax=1.0)
        plt.ylim(ymin=0., ymax=3.1)
        plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
        plt.ylabel(r'Volume filling fraction [$T<1.3\times 10^5 K$]', size=28, color='black')

        plt.xlabel(r'$P(r)/<P(r)>$ (log)', size=28, color='black')
        leg = plt.legend(loc='upper right', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
        plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
        plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
        plt.grid()
        plt.tight_layout()
        plt.savefig('./analysis-plots/presDistrb_%04d.png'%snap)
        plt.close()
