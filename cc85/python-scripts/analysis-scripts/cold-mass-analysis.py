# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:40:43 2023

@author: alankar
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import h5py
import os

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = True
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 0.8
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 0.6
matplotlib.rcParams["xtick.major.width"] = 0.6
matplotlib.rcParams["ytick.minor.width"] = 0.45
matplotlib.rcParams["xtick.minor.width"] = 0.45
matplotlib.rcParams["ytick.major.size"] = 4.0
matplotlib.rcParams["xtick.major.size"] = 4.0
matplotlib.rcParams["ytick.minor.size"] = 2.0
matplotlib.rcParams["xtick.minor.size"] = 2.0
matplotlib.rcParams["xtick.major.pad"] = 10.0
matplotlib.rcParams["xtick.minor.pad"] = 10.0
matplotlib.rcParams["ytick.major.pad"] = 6.0
matplotlib.rcParams["ytick.minor.pad"] = 6.0
matplotlib.rcParams["xtick.labelsize"] = 24.0
matplotlib.rcParams["ytick.labelsize"] = 24.0
matplotlib.rcParams["axes.titlesize"] = 24.0
matplotlib.rcParams["axes.labelsize"] = 28.0
matplotlib.rcParams["axes.labelpad"] = 8.0
plt.rcParams["font.size"] = 28
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True

out_dir = "mass-analysis"
os.makedirs(f"./{out_dir}/", exist_ok=True)
snap_dir = "../../prs-degen/output-prs_2.5e5"

tot_snap = 41
chi = 100
tcc = np.zeros(tot_snap)
Tcl  = 4e4
tracer_cut = 1.0e-04

Mass_cloud = np.zeros((tot_snap,), dtype=np.float64)
for snap in range(tot_snap):
    print(snap, end='\r')
    step = 10*snap
    tcc[snap] = step/np.sqrt(chi)
    with h5py.File(f'{snap_dir}/data.{snap:04d}.flt.h5', 'r') as data:
        dV = np.array(data[f'/Timestep_{snap}/vars/cellvol']).flatten()
        temperature = np.array(data[f'/Timestep_{snap}/vars/temperature']).flatten()
        ndens = np.array(data[f'/Timestep_{snap}/vars/ndens']).flatten()
        tracer = np.array(data[f'/Timestep_{snap}/vars/tr1']).flatten()
        
        mass = ndens*dV

        cond_cold_gas = temperature<(3.3*Tcl)
        std_trc = np.std(tracer)
        med_trc = np.median(tracer)
        max_trc = np.max(tracer)
        print(med_trc, std_trc, max_trc)
        select_cold_cloud = np.logical_and(cond_cold_gas, tracer>=0.6*max_trc) #np.abs(tracer-med_trc)>=2*std_trc)
        
        cold_gas_mass = np.sum(ndens[select_cold_cloud]*dV[select_cold_cloud])
        
        Mass_cloud[snap] = cold_gas_mass
        
        print(Mass_cloud[snap])
        
np.savetxt(f"{out_dir}/mass-cold-cloud.txt", 
           np.vstack( (tcc, Mass_cloud/Mass_cloud[0]) ).T, 
           fmt="%.6e", header="# tcc\tM_cold_cloud/M0")  

plt.figure(figsize=(13,10))
plt.semilogy(tcc, Mass_cloud/Mass_cloud[0])
plt.xlabel(r"time [$t_{cc}$]")
plt.ylabel(r"Mass_cloud [$M_0$]")
plt.savefig(f"./{out_dir}/cold-cloud-mass.png", transparent=False)
plt.close()      
        