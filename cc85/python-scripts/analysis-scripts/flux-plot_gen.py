# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:23:08 2024

@author: alankar
"""

import numpy as np
import pickle
import sys
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt


## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = False
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["grid.linestyle"] = ":"
matplotlib.rcParams["grid.linewidth"] = 2.0
matplotlib.rcParams["grid.color"] = "gray"
matplotlib.rcParams["grid.alpha"] = 0.5
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 1.0
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 1.0
matplotlib.rcParams["xtick.minor.width"] = 1.0
matplotlib.rcParams["ytick.major.size"] = 8.0
matplotlib.rcParams["xtick.major.size"] = 8.0
matplotlib.rcParams["ytick.minor.size"] = 5.0
matplotlib.rcParams["xtick.minor.size"] = 5.0
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
matplotlib.rcParams["figure.figsize"] = (28,12)

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

# get rid of the one where vanilaa is missing
tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]

mach = 1.496
Tcl = 4.0e+04
chi = 100
tcc = np.sqrt(chi)
gamma = 5/3.
till = 100

mu = 0.60917
mp = 1.6726e-24
kB = 1.380649e-16
Myr = 1.0e+06 * 365*24*60*60


os.makedirs('./flux-plots', exist_ok = True)
plot_freq = 1
for select in range( len(tcool_mix_B_tcc) ):
    os.makedirs(f'./flux-plots/tcmBtcc_{tcool_mix_B_tcc[select]}', exist_ok = True)
    series_cc85 = np.load(f"mass-flux_{tcool_mix_B_tcc[select]}.npy")
    series_vanl = np.load(f"mass-flux-vanl_{tcool_mix_B_tcc[select]}.npy")
    print(f"Reading flux_{tcool_mix_B_tcc[select]}: CC85:{series_cc85.shape} Vanilla:{series_vanl.shape}")
    assert(series_cc85.shape == series_vanl.shape)
    for time_indx in range(0, min(till+1, series_cc85.shape[0]), plot_freq):
        print(time_indx, end="\r")
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # cloud
        ax1.plot(series_cc85[time_indx, :, 0], series_cc85[time_indx, :, 1], label=f"{(time_indx):.1f}")
        ax2.plot(series_vanl[time_indx, :, 0], series_vanl[time_indx, :, 1], label=f"{(time_indx):.1f}")

        ax1.plot(series_cc85[time_indx, :, 0], np.ones_like(series_cc85[time_indx, :, 0])*10.0, 
                 linestyle="None", marker="D", color="k", markersize=10)

        if time_indx == 0:
            xold = series_cc85[time_indx, :, 0]
            xnew = xold*rini_B_rcl[select] # units of R_cl

        ax1.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        ax2.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    
        forward = lambda arg: arg*rini_B_rcl[select]
        inverse = lambda arg: arg/rini_B_rcl[select]

        ax1.set_title("CC85 wind", size=20)
        ax2.set_title("plane parallel constant wind (vanilla)", size=20)

        ax1.set_xlim(xmin=1.0, xmax=7.6)
        ax2.set_xlim(xmin=1.0, xmax=7.6)
        
        ax1.set_ylim(ymin=0.02, ymax=6.2e+01)
        ax2.set_ylim(ymin=0.02, ymax=6.2e+01)

        ax_top = ax1.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1.set_ylabel(r"$\dot{M}\ {\rm [}M_{\rm cl,ini}\ {\rm Myr^{-1}}{\rm ]}$")
        ax1.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2.set_ylabel(r"$\dot{M}\ {\rm [}M_{\rm cl,ini}\ {\rm Myr^{-1}}{\rm ]}$")
        ax2.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
    
        plt.savefig(f'./flux-plots/tcmBtcc_{tcool_mix_B_tcc[select]}/t.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()
    print(" ", end="\r")

