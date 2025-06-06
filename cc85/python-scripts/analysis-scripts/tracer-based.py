# -*- coding: utf-8 -*-
"""
Created on Fri Apr  26 11:33:48 2024

@author: alankar
"""
import numpy as np
import pickle
import h5py
import sys
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt

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

vanilla = True
tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

if vanilla:
    tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
    rini_B_rcl = rini_B_rcl[1:]

mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 100

mu = 0.61
mp = 1.6726e-24
Myr = 1.0e+06 * 365*24*60*60

create = True

root = f"../../output{'-vanl' if vanilla else ''}"

Tmix = np.sqrt(chi)*Tcl
print("Tmix: %.2e K"%Tmix )

mass_cloud = {}

if create:
    for select in range(len(tcool_mix_B_tcc)):
        cloud = np.zeros( (till+1, 1), dtype=np.float64)
        mass_cloud_ini = 0.
        # UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        for file_no in range(till+1):
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
            print(f"{output_file}: {file_no}", end="\r")
            '''
            if file_no == 0:
                UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
                UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
                UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
                distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
            '''
            data = h5py.File(output_file, "r")
            del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
            del_T   = np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten()
            temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            density   = np.array(data[f"/Timestep_{file_no}/vars/density"]).flatten()
            velocity  = np.array(data[f"/Timestep_{file_no}/vars/vr"]).flatten()
            tracer    = np.array(data[f"/Timestep_{file_no}/vars/tr1"]).flatten()
            rho_wind = density/(1 + del_rho)
            Twind    = temperature/(1 + del_T)
            x_cells = np.array(data["/cell_coords/X"]).flatten()
            y_cells = np.array(data["/cell_coords/Y"]).flatten()
            z_cells = np.array(data["/cell_coords/Z"]).flatten()
            distance_cells = np.sqrt(x_cells**2 + y_cells**2 + z_cells**2)

            cutoff = Twind>Tmix
            choose = np.logical_and(tracer>1.0e-04, temperature<=3.3*Tcl)
            choose = np.logical_and(choose, cutoff)
            mass_cloud_this_snap = np.sum(density[choose]*cell_vol[choose])
            if file_no == 0 and mass_cloud_ini == 0.:
                mass_cloud_ini = np.sum(density[density>(chi-1)]*cell_vol[density>(chi-1)])
            cloud[file_no, 0] = mass_cloud_this_snap/mass_cloud_ini
        mass_cloud[f"{tcool_mix_B_tcc[select]}"] = cloud
        print("\n", end="\r")

    with open(f'mass-tracer_cold{"-vanl" if vanilla else ""}.pickle', 'wb') as handle:
        pickle.dump(mass_cloud, handle, protocol=pickle.HIGHEST_PROTOCOL)

if not(create):
    with open(f'mass-tracer_cold{"-vanl" if vanilla else ""}.pickle', 'rb') as handle:
        mass_cloud = pickle.load(handle)

for key in list(mass_cloud.keys()):
    data = mass_cloud[key]
    condition = data[:,0]>0
    plt.loglog(np.range(data.shape[0])[condition], (data[:,0])[condition], label=f"{key}")

plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 16 }, title_fontsize=16, fancybox=True)
# plt.ylim(ymin=1.03e-03,  ymax=18)
plt.ylabel(r"$M_{\rm cold}\ [M_{\rm cl,ini}]$")
plt.xlabel(r"time [$t_{\rm cc}$]")
plt.savefig("tracer-cold.svg", transparent=False, bbox_inches="tight")
plt.close()
       
