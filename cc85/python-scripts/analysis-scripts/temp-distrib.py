# -*- coding: utf-8 -*-
"""
Created on Sat Jan  05 11:07:48 2024

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import h5py
import pickle

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 100

select = 3
create = False

root = "../../output"
temperature_distrib = []

if create:
    for file_no in range(till+1):
        print(file_no, end="\r")
        data = h5py.File(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/data.{file_no:04d}.{file_ext}", 'r')
        temperature  = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
        del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
        condition = del_rho>=10 # np.logical_and(del_rho>=10, temperature<=3.3*Tcl)

        dense_temperature = temperature[condition]
        dense_density = np.array(data[f"/Timestep_{file_no}/vars/density"]).flatten()[condition]
        dense_cellvol = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()[condition]

        temperature_distrib.append(np.vstack( (dense_temperature, dense_density, dense_cellvol) ).T)

        data.close()

    with open(f"./dump/temperature_distrib-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}.pickle", 'wb') as pic_file:
        pickle.dump(temperature_distrib, pic_file)

with open(f"./dump/temperature_distrib-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}.pickle", 'rb') as pic_file:
        temperature_distrib = pickle.load(pic_file)

stacked = False
till = 1 if stacked else len(temperature_distrib)

for i in range(till):
    ## Plot Styling
    matplotlib.rcParams["xtick.direction"] = "in"
    matplotlib.rcParams["ytick.direction"] = "in"
    matplotlib.rcParams["xtick.top"] = True
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
    matplotlib.rcParams["figure.figsize"] = (13,10)
    
    if stacked:
        snaps = [10, 50, 100]
        x = [np.log10(temperature_distrib[snap][:,0]) for snap in snaps]
        weights = [temperature_distrib[snap][:,1]*temperature_distrib[snap][:,2] for snap in snaps]
        plt.hist(x, bins=50,
                 weights = weights,
                 log = True,
                 density = True,
                 range = (4.5, 6.0),
                 stacked = stacked,
                 )
    else:
        plt.hist(np.log10(temperature_distrib[i][:,0]), bins=50,
                 weights = temperature_distrib[i][:,1]*temperature_distrib[i][:,2],
                 log = True,
                 density = True,
                 range = (4.5, 6.0),
                 stacked = stacked,
                 )
    if stacked:
        plt.savefig(f"./dump/temperature_distrib-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}_stacked.png")
    else:
        plt.savefig(f"./dump/series/temperature_distrib-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}_{i:03d}.png")
    plt.ylim(ymin=9.0e-04, ymax=6.0e+01)
    plt.close()

