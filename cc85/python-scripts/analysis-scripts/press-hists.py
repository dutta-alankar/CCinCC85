# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:15:58 2023

@author: alankar
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import h5py
import os
from itertools import chain

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

os.makedirs('./pres-hists/', exist_ok=True)
output_dir = "../../prs-degen/output-prs_2.5e5"

tot_snap = 30
chi = 100
tcc = np.zeros(tot_snap)
Tcl  = 4e4

for snap in range(tot_snap):
    print(snap, end='\r')
    step = 10*snap
    tcc[snap] = step/np.sqrt(chi)
    with h5py.File(f'{output_dir}/data.{snap:04d}.flt.h5', 'r') as data:
        dV = np.array(data[f'/Timestep_{snap}/vars/cellvol']).flatten()
        temperature = np.array(data[f'/Timestep_{snap}/vars/temperature']).flatten()
        ndens = np.array(data[f'/Timestep_{snap}/vars/ndens']).flatten()
        pres = np.array(data[f'/Timestep_{snap}/vars/pressure']).flatten()
        tracer = np.array(data[f'/Timestep_{snap}/vars/tr1']).flatten()

        x = np.array(data['/cell_coords/X']).flatten()
        y = np.array(data['/cell_coords/Y']).flatten()
        z = np.array(data['/cell_coords/Z']).flatten()
        
        distance = np.sqrt(x**2 + y**2 + z**2)
        rad_pnts = 100
        radius = np.linspace(0.98*np.min(distance), 1.02*np.max(distance), rad_pnts+1)

        cond_cold_gas = temperature<(3.3*Tcl)
        
        cold_gas_prs_by_prs_cold_avg = []
        hot_gas_prs_by_prs_hot_avg = []
        
        cold_gas_prs_by_prs_all_avg = []
        hot_gas_prs_by_prs_all_avg = []
        
        dV_cold = [] 
        dV_hot  = []
        
        prs_hot_avg  = np.zeros(radius.shape[0]-1)
        prs_cold_avg = np.zeros_like(prs_hot_avg)
        prs_all_avg  = np.zeros_like(prs_hot_avg)
        
        for indx, rad in enumerate(radius[:-1]):
            select = np.logical_and(distance>rad, distance<radius[indx+1])
            select_hot  = np.logical_and(np.logical_not(cond_cold_gas),select)
            select_cold = np.logical_and(np.logical_and(cond_cold_gas, select), tracer>1e-4)
            hot_gas_prs  = pres[select_hot]
            cold_gas_prs = pres[select_cold]
            
            if (np.count_nonzero(select)>0):
                prs_all_avg[indx] = np.average(pres[select], weights=dV[select])
                
            if (np.count_nonzero(select_hot) > 0):
                prs_hot_avg[indx] = np.average(hot_gas_prs, weights=dV[select_hot])
                
                hot_gas_prs_by_prs_hot_avg.append( hot_gas_prs  / prs_hot_avg[indx] )
                hot_gas_prs_by_prs_all_avg.append( hot_gas_prs /  prs_all_avg[indx] )
                
                dV_hot.append(dV[select_hot])
                
            if (np.count_nonzero(select_cold) > 0) :
                prs_cold_avg[indx] = np.average(cold_gas_prs, weights=dV[select_cold])
                
                cold_gas_prs_by_prs_cold_avg.append( cold_gas_prs / prs_cold_avg[indx] )
                cold_gas_prs_by_prs_all_avg.append( cold_gas_prs / prs_all_avg[indx] )
                
                dV_cold.append(dV[select_cold])
        
        cold_gas_prs_by_prs_cold_avg = np.array(list(chain.from_iterable(cold_gas_prs_by_prs_cold_avg)))
        hot_gas_prs_by_prs_hot_avg = np.array(list(chain.from_iterable(hot_gas_prs_by_prs_hot_avg)))
        
        cold_gas_prs_by_prs_all_avg = np.array(list(chain.from_iterable(cold_gas_prs_by_prs_all_avg)))
        hot_gas_prs_by_prs_all_avg = np.array(list(chain.from_iterable(hot_gas_prs_by_prs_all_avg)))
        
        dV_hot  = np.array(list(chain.from_iterable(dV_hot)))
        dV_cold = np.array(list(chain.from_iterable(dV_cold)))
        
        plt.figure(figsize=(13,10))
        plt.hist(hot_gas_prs_by_prs_hot_avg, 
                 bins=100, 
                 weights=dV_hot, 
                 density=True, 
                 color='tab:red', label='Hot gas')
        
        plt.hist(cold_gas_prs_by_prs_cold_avg, 
                bins=100, 
                weights=dV_cold, 
                density=True, 
                color='tab:blue', alpha=0.5, label='Cold gas') 
        plt.title(r"$t/t_{cc} \approx %d$"%tcc[snap])
        plt.legend(loc="best")
        plt.yscale('log')
        plt.savefig(f"./pres-hists/local_{snap:04d}.png", transparent=False)
        plt.close()
        
        plt.figure(figsize=(13,10))
        plt.hist(hot_gas_prs_by_prs_all_avg, 
                 bins=100, 
                 weights=dV_hot, 
                 density=True, 
                 color='tab:red', label='Hot gas')
        
        plt.hist(cold_gas_prs_by_prs_all_avg, 
                bins=100, 
                weights=dV_cold, 
                density=True, 
                color='tab:blue', alpha=0.5, label='Cold gas') 
        plt.title(r"$t/t_{cc} \approx %d$"%tcc[snap])
        plt.legend(loc="best")
        plt.yscale('log')
        plt.savefig(f"./pres-hists/global_{snap:04d}.png", transparent=False)
        plt.close()
        
        plt.figure(figsize=(13,10))
        plt.plot(radius[:-1], prs_hot_avg/prs_all_avg, label="Hot gas")
        plt.plot(radius[:-1], prs_cold_avg/prs_all_avg, label="Cold gas")
        plt.title(r"$t/t_{cc} \approx %d$ (Average pressure)"%tcc[snap])
        plt.xlabel("Distance")
        plt.ylabel("Average Pressure [All average]")
        plt.legend(loc="best")
        plt.savefig(f"./pres-hists/pres-prof_{snap:04d}.png", transparent=False)
        plt.close()
        
        plt.figure(figsize=(13,10))
        plt.semilogy(radius[:-1], prs_hot_avg, label="Hot gas")
        plt.semilogy(radius[:-1], prs_cold_avg, label="Cold gas")
        plt.title(r"$t/t_{cc} \approx %d$ (Average pressure)"%tcc[snap])
        plt.xlabel("Distance")
        plt.ylabel("Average Pressure [All average]")
        plt.legend(loc="best")
        plt.savefig(f"./pres-hists/pres-prof_{snap:04d}.png", transparent=False)
        plt.close()

        