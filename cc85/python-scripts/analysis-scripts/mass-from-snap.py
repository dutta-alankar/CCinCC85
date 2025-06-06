# -*- coding: utf-8 -*-
"""
Created on Sat Jan  05 16:45:48 2024

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

create = False

root = "../../output"
mass_dense = []

if create:
    for select in range(len(tcool_mix_B_tcc)):
        mass = np.zeros(till+1, dtype=np.float64)
        for file_no in range(till+1):
            print(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/data.{file_no:04d}.{file_ext}: {file_no}", end="\r")
            data = h5py.File(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/data.{file_no:04d}.{file_ext}", 'r')
            del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
            condition = del_rho>=10 # np.logical_and(del_rho>=10, temperature<=3.3*Tcl)

            dense_density = np.array(data[f"/Timestep_{file_no}/vars/density"]).flatten()[condition]
            dense_cellvol = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()[condition]

            mass[file_no] = np.sum( dense_density*dense_cellvol )

            data.close()
        print()
        mass_dense.append(mass)

    with open(f"./dump/mass-dense-from-snaps.pickle", 'wb') as pic_file:
        pickle.dump(mass_dense, pic_file)

with open(f"./dump/mass-dense-from-snaps.pickle", 'rb') as pic_file:
    mass_dense = pickle.load(pic_file)

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
matplotlib.rcParams["figure.figsize"] = (16,14)

for i in range(len(tcool_mix_B_tcc)):
    print(i, end=": ")
    root = "../../output"
    print(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}")
    data = mass_dense[i]
    plt.plot(np.arange(data.shape[0]), data/data[0], label="%.2f"%tcool_mix_B_tcc[i]) # tcc gap between each point


plt.xlim(xmin = 0., xmax = 100.)
plt.ylim(ymin= 5.0e-02, ymax = 15)
plt.legend(loc="upper left", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 15 }, title_fontsize=18, fancybox=True)
plt.yscale("log")
plt.xlabel(r"$t/t_{\rm cc,ini}$")
plt.ylabel(r"Dense mass $M_{\rm dense}/M_{\rm dense,ini}$")
plt.title(r"Dense mass $\equiv \ [\rho (d)>10 \rho _{\rm wind}(d)]$")
plt.savefig("mass-dense-snaps.png", transparent=True, bbox_inches='tight')
plt.close()
