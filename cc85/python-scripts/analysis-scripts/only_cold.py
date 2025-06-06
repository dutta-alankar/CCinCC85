# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:54:56 2022

@author: alankar
"""
import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib

till_file = 100
data_loc = "output-c100,m1.496,T4e4,t0.80,r282.684-100_tcc"
mass_just_cold = np.zeros(till_file+1, dtype=np.float64)
t_int = 1.0
time_tcc = np.arange(till_file+1)

for i in range(till_file+1):
    print(i, end="\r")
    data = h5py.File(f"../../{data_loc}/data.{i:04d}.flt.h5", "r")
    Temperature = np.array(data[f"/Timestep_{i}/vars/temperature"]).flatten()
    tracer = np.array(data[f"/Timestep_{i}/vars/tr1"]).flatten()
    condition = np.logical_and(Temperature <= 6.0e+04, tracer>=1e-4)
    rho = np.array(data[f"/Timestep_{i}/vars/density"]).flatten()[condition]
    dV  = np.array(data[f"/Timestep_{i}/vars/cellvol"]).flatten()[condition]
    mass_just_cold[i] = np.sum(rho*dV)
    data.close()
mass_just_cold = mass_just_cold/mass_just_cold[0]
print()
## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = False
matplotlib.rcParams["ytick.right"] = False
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 0.8
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 0.6
matplotlib.rcParams["xtick.minor.width"] = 0.6
matplotlib.rcParams["ytick.major.size"] = 12.0
matplotlib.rcParams["xtick.major.size"] = 12.0
matplotlib.rcParams["ytick.minor.size"] = 6.0
matplotlib.rcParams["xtick.minor.size"] = 6.0
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

fig = plt.figure(figsize=(13, 10))

plt.plot(time_tcc, mass_just_cold)
plt.savefig("mass_just_cold.png")
