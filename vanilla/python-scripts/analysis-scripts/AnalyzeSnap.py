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
par = []
prp = []

for snap in range(14):
    print(snap, end='\r')
    step = 20
    tcc.append(snap*step/np.sqrt(chi))
    with h5py.File(f'{dir}/data.%04d.dbl.h5'%snap, 'r') as data:
        dV = np.array(data['/Timestep_%d/vars/cellvol'%snap]).flatten()
        temperature = np.array(data['/Timestep_%d/vars/temperature'%snap]).flatten()
        ndens = np.array(data['/Timestep_%d/vars/ndens'%snap]).flatten()
        tracer = np.array(data['/Timestep_%d/vars/tr1'%snap]).flatten()

        cent = np.sum(np.array(data['/cell_coords/X']).flatten()*tracer*dV)/np.sum(tracer*dV)

        massCell = (ndens*mu*mp)*dV*Rcl**3/Msun
        condition = temperature<(3.3*Tcl)

        Mtotal = np.sum(massCell[condition])
        Vtotal = np.sum(dV[condition])*((Rcl/pc)**3)
        mass.append(Mtotal)
        vol.append(Vtotal)
        vol_all.append(np.sum(dV))
        centroid.append(cent)

        M0 = mass[0]
        V0 = vol[0]
        Vt0 = vol_all[0]

        condition = tracer>1e-4
        parmax = np.max(np.array(data['/cell_coords/X']).flatten()[condition])
        parmin = np.min(np.array(data['/cell_coords/X']).flatten()[condition])
        prpmax = (np.max(np.array(data['/cell_coords/Y']).flatten()[condition]) + \
                 np.max(np.array(data['/cell_coords/Z']).flatten()[condition]))*0.5
        prpmin = (np.min(np.array(data['/cell_coords/Y']).flatten()[condition]) + \
                 np.min(np.array(data['/cell_coords/Z']).flatten()[condition]))*0.5
        asym = (parmax-parmin)/(prpmax-prpmin)
        asymetry.append(asym)
        par.append(parmax-parmin)
        prp.append(prpmax-prpmin)

        '''
        # plt.figure(figsize=(13,10))
        # Create the 2D histogram in log space
        hist, xedges, yedges = np.histogram2d(np.log10(temperature), dV*(Rcl/pc)**3,
                                              bins=(100,101), density=True,)
        plt.imshow(hist.T, origin='lower',
                   norm=LogNorm(), extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap='viridis')
        plt.colorbar()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlim(xmin=1e-3, xmax=1.5e1)
        # plt.ylim(ymin=1e29, ymax=1e47)
        plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
        plt.ylabel(r'Volume [$pc^{3}$]', size=28, color='black')

        plt.xlabel(r'Temperature [$K$] (log)', size=28, color='black')
        # leg = plt.legend(loc='lower left', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
        plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
        plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
        plt.grid()
        plt.tight_layout()
        plt.savefig('./analysis-plots/snapVolTemp_%04d.png'%snap)
        plt.close()

        # plt.figure(figsize=(13,10))
        # Create the 2D histogram in log space
        hist, xedges, yedges = np.histogram2d(np.log10(temperature), massCell,
                                              bins=(100,101), density=True)
        plt.imshow(hist.T, origin='lower',
                   norm=LogNorm(), extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap='viridis')
        plt.colorbar()
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.xlim(xmin=1e-3, xmax=1.5e1)
        # plt.ylim(ymin=1e29, ymax=1e47)
        plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
        plt.ylabel(r'Volume [$pc^{3}$]', size=28, color='black')

        plt.xlabel(r'Temperature [$K$] (log)', size=28, color='black')
        # leg = plt.legend(loc='lower left', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
        plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
        plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
        plt.grid()
        plt.tight_layout()
        plt.savefig('./analysis-plots/snapMassTemp_%04d.png'%snap)
        plt.close()
        '''

        #Leave out the pure wind
        dV = dV[tracer>1e-4]
        temperature = temperature[tracer>1e-4]
        massCell = massCell[tracer>1e-4]
        # Compute the histogram and bin edges
        histV, edges = np.histogram(np.log10(temperature), bins=100, density=False,
                                    weights=dV*((Rcl/pc)**3) )
        histM, edges = np.histogram(np.log10(temperature), bins=100, density=False,
                                    weights=massCell)

        # Compute the bin centers
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        plt.figure(figsize=(13,10))
        plt.plot(bin_centers, histV/V0, linestyle='-', linewidth=5,
                 color='tab:red', label='volume')
        plt.plot(bin_centers, histM/M0, linestyle='-', linewidth=5,
                 color='tab:blue', label='mass')
        plt.vlines(np.log10(1.2e5), 1e-6, 1e6, colors='black', linestyles=':', linewidth=5,
                   label=r'$T=1.2\times 10^5 K$')
        # plt.xscale('log')
        plt.yscale('log')
        plt.xlim(xmin=4.4, xmax=7.1)
        plt.ylim(ymin=8e-6, ymax=2e4)
        plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
        plt.ylabel(r'Phase Distribution with respect to total initial', size=28, color='black')

        plt.xlabel(r'Temperature [$K$] (log)', size=28, color='black')
        leg = plt.legend(loc='lower right', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
        plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
        plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
        plt.grid()
        plt.tight_layout()
        plt.savefig('./analysis-plots/1DPDF_snap.%04d.png'%snap)
        plt.close()
print()
mass = np.array(mass)
vol  = np.array(vol)
tcc  = np.array(tcc)
centroid = np.array(centroid)
asymetry = np.array(asymetry)
par = np.array(par)
prp = np.array(prp)

mass = mass/M0
vol  = vol/V0
vol_all = vol_all/Vt0

plt.figure(figsize=(13,10))
plt.plot(tcc, vol, color='tab:red', linewidth=5 , label=r'volume')
plt.plot(cc85[:,0]/np.sqrt(chi), (cc85[:,1]/cc85[0,1])**2,
         color='tab:red', linestyle=':' ,linewidth=5, label='expansion')
plt.plot(tcc, (centroid/cc85[0,1])**2,
         color='tab:purple', linestyle='--' ,linewidth=5, label='volume expansion')

plt.plot(tcc, mass, 'o', color='tab:blue', linewidth=5, markersize=8)
plt.plot(cc85[:,0]/np.sqrt(chi), cc85[:,5],
         color='tab:blue', linewidth=5, label=r'Mass')
# plt.plot(tcc, vol_all, color='tab:red', linestyle=':', linewidth=5 ) #, label=r'Volume')

plt.plot(tcc, asymetry, color='tab:green', linewidth=5 , label=r'asymmetry')

# plt.xscale('log')
plt.yscale('log')
plt.xlim(xmax=25.1)
plt.ylim(ymin=0.31, ymax=210)
plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
plt.title(r'Vanilla', size=28, color='black')
plt.ylabel(r'Cold gas properties $(T<%.1f\times 10^{5} K)$'%(3.3*Tcl/1e5), size=28, color='black')
plt.xlabel(r'Time [$t_{cc}$]', size=28, color='black')
leg = plt.legend(loc='upper left', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
plt.grid()
plt.tight_layout()
plt.savefig('./analysis-plots/volMasCold.png')
plt.show()

plt.figure(figsize=(13,10))
plt.plot(tcc, prp, color='tab:red',  linewidth=5 , label=r'perpendicular')
plt.plot(tcc, par, color='tab:blue', linewidth=5,  label=r'parallel')

# plt.xscale('log')
plt.yscale('log')
plt.xlim(xmax=25.1)
# plt.ylim(ymin=0.31, ymax=210)
plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
plt.title(r'Vanilla', size=28, color='black')
plt.ylabel(r'Cold gas properties $(T<%.1f\times 10^{5} K)$'%(3.3*Tcl/1e5), size=28, color='black')
plt.xlabel(r'Time [$t_{cc}$]', size=28, color='black')
leg = plt.legend(loc='upper left', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
plt.grid()
plt.tight_layout()
# plt.savefig('./analysis-plots/volMasCold.png')
plt.show()

# -----------------------------------------------------------------------
tcc = np.sqrt(chi)

plt.figure(figsize=(13,10))
plt.plot(cc85[:,1]/cc85[0,1], np.gradient(cc85[:,5],cc85[:,0]/tcc), color='tab:blue', linewidth=5)

# plt.xscale('log')
# plt.yscale('log')
# plt.xlim(xmin=1e-3, xmax=1.5e1)
# plt.ylim(ymin=1e29, ymax=1e47)
plt.tick_params(axis='both', which='minor', labelsize=24, direction="out", pad=5, labelcolor='black')
plt.ylabel(r'$\frac{dM}{dt}(T<1.2\times 10^{5} K)\ [M_{cl,0}]$', size=28, color='black')

plt.xlabel(r'Distance [$R_{ini}$]', size=28, color='black')
# leg = plt.legend(loc='lower left', ncol=1, fancybox=True, fontsize=25, framealpha=0.5)
plt.tick_params(axis='both', which='major', length=12, width=3, labelsize=24)
plt.tick_params(axis='both', which='minor', length=8, width=2, labelsize=22)
plt.grid()
plt.tight_layout()
plt.savefig('./analysis-plots/dervCold.png')
plt.show()
