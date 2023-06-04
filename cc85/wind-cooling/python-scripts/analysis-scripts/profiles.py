"""
Created on Fri May 26 00:08:30 2023

@author: alankar
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib
import os
import sys
from scipy.interpolate import interp1d

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

out_dir = "profile-plots"
os.makedirs(f"./{out_dir}/", exist_ok=True)

UNIT_DENSITY = 6.3682e-26
UNIT_LENGTH = 2.7198e+20
UNIT_VELOCITY = 5.4100e+07

kpc = 3.086e+21
rini = 40

all_files = [0, 5, 8, 15]

chi = 100
analysis = np.loadtxt("../../../threshold/output-tcoolmBytcc_0.01/analysis.dat")
pos_cloud = interp1d(analysis[:,0]/np.sqrt(chi), analysis[:,0]) 

with plt.style.context('dark_background'):
    plt.figure(figsize=(13,10))
    for i,file_no in enumerate(all_files):
        hdf = h5py.File(f"../../output/data.{file_no:04d}.flt.h5", "r")

        # print(list(hdf.keys()))
        # print(list(hdf[f"/Timestep_{file_no}/vars"].keys()))
        rad = np.array(hdf[f"/cell_coords/X"])
        ndens = np.array(hdf[f"/Timestep_{file_no}/vars/ndens"])
        temp  = np.array(hdf[f"/Timestep_{file_no}/vars/temperature"])
        vel   = np.array(hdf[f"/Timestep_{file_no}/vars/vr"])
        prs   = np.array(hdf[f"/Timestep_{file_no}/vars/pressure"])
        mach  = np.array(hdf[f"/Timestep_{file_no}/vars/mach"])
        hdf.close()
        
        if (i+1)==len(all_files):
            cloud = pos_cloud(file_no) if (i+1)>1 else rini
            plt.axvline(x = cloud*UNIT_LENGTH/kpc, color = 'lightsalmon', linestyle=":")
        # plt.loglog(rad/rini, ndens)
        # plt.loglog(rad/rini, prs)
        plt.semilogy(rad*UNIT_LENGTH/kpc, temp, linestyle="--" if (i+1)<len(all_files) else "-", color="turquoise")
    plt.xlabel(r"Distance [kpc]")
    plt.ylabel(r"Temperature [K]")
    plt.ylim(2e4, 8e6)
plt.savefig(f"{out_dir}/profile_{len(all_files)}.png", transparent=True)

