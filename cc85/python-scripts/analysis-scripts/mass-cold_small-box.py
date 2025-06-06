# -*- coding: utf-8 -*-
"""
Created on Fri Apr  26 11:33:48 2024

@author: alankar.
Usage: time python mass-cold_small-box.py cr T
"""
import numpy as np
from scipy.interpolate import interp1d
import pickle
import h5py
import sys
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt

dark = True
if len(sys.argv)<3:
    print(sys.argv)
    print("Wrong usage!")
    sys.exit(1)

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = False
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["grid.linestyle"] = ":"
matplotlib.rcParams["grid.linewidth"] = 0.8
matplotlib.rcParams["grid.color"] = "gray"
matplotlib.rcParams["grid.alpha"] = 0.3
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 1.0
matplotlib.rcParams["lines.linewidth"] = 3.5
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 1.0
matplotlib.rcParams["xtick.minor.width"] = 1.0
matplotlib.rcParams["ytick.major.size"] = 11.0
matplotlib.rcParams["xtick.major.size"] = 11.0
matplotlib.rcParams["ytick.minor.size"] = 5.0
matplotlib.rcParams["xtick.minor.size"] = 5.0
matplotlib.rcParams["xtick.major.pad"] = 10.0
matplotlib.rcParams["xtick.minor.pad"] = 10.0
matplotlib.rcParams["ytick.major.pad"] = 6.0
matplotlib.rcParams["ytick.minor.pad"] = 6.0
matplotlib.rcParams["xtick.labelsize"] = 26.0
matplotlib.rcParams["ytick.labelsize"] = 26.0
matplotlib.rcParams["axes.titlesize"] = 24.0
matplotlib.rcParams["axes.labelsize"] = 28.0
matplotlib.rcParams["axes.labelpad"] = 8.0
plt.rcParams["font.size"] = 28
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True
matplotlib.rcParams["figure.figsize"] = (13,10)
if dark:
    plt.style.use('dark_background')

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]

mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 100

wind = np.loadtxt('../../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach_data = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]
relpos = interp1d(mach_data, rnorm) #inverting the Mach relation
diniBdinj = relpos(mach)
CC85wind_density = interp1d(wind[:,0], wind[:,1])

mu = 0.60917
mp = 1.6726e-24
Myr = 1.0e+06 * 365*24*60*60
MSun = 1.99e+33

create = sys.argv[2] == "T"

root = "../../output"
root_vanl = "../../output-vanl"

Tmix = np.sqrt(chi)*Tcl
Tcutoff = 9.0e+04
Temperature_identify = 2.0*Tcl
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Temperature_identify: %.2e K"%Temperature_identify)
print(f"{till+1} files analyzed for each tcool_mix_B_tcc")

mass_evol = {}
analyze_freq = 1
if create:
    for select in range(len(tcool_mix_B_tcc)):
        quantity = np.zeros( (till+1, 4), dtype=np.float64)
        # quantities are (Mcl_CC85, Mcl_vanl) for every file
        UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        distance_ini = None
        for file_no in range(0, till+1, analyze_freq):
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
            directory_vanl = f"{root_vanl}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file_vanl = f"{directory_vanl}/data.{file_no:04d}.{file_ext}"
            string = f"{output_file}: {file_no}"
            print(string, end="\r")
            if file_no == 0:
                UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
                UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
                UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
                distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
            data = h5py.File(output_file, "r")
            data_vanl = h5py.File(output_file_vanl, "r")
            del_T = np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten()
            del_T_vanl = np.array(data_vanl[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten()
            temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            temperature_vanl = np.array(data_vanl[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            cell_vol_vanl  = np.array(data_vanl[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            ndens   = np.array(data[f"/Timestep_{file_no}/vars/ndens"]).flatten()
            ndens_vanl   = np.array(data_vanl[f"/Timestep_{file_no}/vars/ndens"]).flatten() # CGS
            tracer = np.array(data[f"/Timestep_{file_no}/vars/tr1"]).flatten()
            tracer_vanl = np.array(data_vanl[f"/Timestep_{file_no}/vars/tr1"]).flatten()

            Twind = temperature/(1 + del_T)
            Twind_vanl = temperature_vanl/(1 + del_T_vanl)

            x_cells = np.array(data["/cell_coords/X"]).flatten()
            y_cells = np.array(data["/cell_coords/Y"]).flatten()
            z_cells = np.array(data["/cell_coords/Z"]).flatten()
            distance_cells = np.sqrt(x_cells**2 + y_cells**2 + z_cells**2)
            x_cells_vanl = np.array(data_vanl["/cell_coords/X"]).flatten()
            y_cells_vanl = np.array(data_vanl["/cell_coords/Y"]).flatten()
            z_cells_vanl = np.array(data_vanl["/cell_coords/Z"]).flatten()
            distance_cells = np.sqrt(x_cells**2 + y_cells**2 + z_cells**2)
            distance_cells_vanl = np.sqrt(x_cells_vanl**2 + y_cells_vanl**2 + z_cells_vanl**2)

            distance_cellthick = np.min(np.abs(distance_cells[1:]-distance_cells[:-1]))
            distance_cellthick_vanl = np.min(np.abs(distance_cells_vanl[1:]-distance_cells_vanl[:-1]))
            cutoff = Twind>Tcutoff # for vanilla this is the entire domain
            Twind = Twind[cutoff]
            if Twind.shape[0] == 0: # all of the wind is colder than cutoff in CC85
                for rest_file_no in range(file_no, till+1):
                    for column in range(quantity.shape[-1]):
                        quantity[rest_file_no, column] = np.nan
                data.close()
                data_vanl.close()
                print(" "*len(string), end="\r")
                print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                break
            cutoff_vanl = distance_cells_vanl<=np.max(distance_cells[cutoff])
            Twind_vanl = Twind_vanl[cutoff_vanl]
            # clip the domain
            ndens = ndens[cutoff]
            ndens_vanl = ndens_vanl[cutoff_vanl]
            del_T = del_T[cutoff]
            del_T_vanl = del_T_vanl[cutoff_vanl]
            temperature = temperature[cutoff]
            temperature_vanl = temperature_vanl[cutoff_vanl]
            cell_vol  = cell_vol[cutoff]
            cell_vol_vanl  = cell_vol_vanl[cutoff_vanl]
            x_cells = x_cells[cutoff]
            x_cells_vanl = x_cells_vanl[cutoff_vanl]
            y_cells = y_cells[cutoff]
            y_cells_vanl = y_cells_vanl[cutoff_vanl]
            z_cells = z_cells[cutoff]
            z_cells_vanl = z_cells_vanl[cutoff_vanl]
            distance_cells = distance_cells[cutoff]
            distance_cells_vanl = distance_cells_vanl[cutoff_vanl]
            tracer = tracer[cutoff]
            tracer_vanl = tracer_vanl[cutoff_vanl]

            cells_chosen = temperature<Temperature_identify
            cells_chosen_vanl = temperature_vanl<Temperature_identify
            mass_cl_cc85 = np.sum(ndens[cells_chosen]*cell_vol[cells_chosen])*mu*mp*UNIT_LENGTH**3 # cgs
            mass_cl_vanl = np.sum(ndens_vanl[cells_chosen_vanl]*cell_vol_vanl[cells_chosen_vanl])*mu*mp*UNIT_LENGTH**3 # cgs

            quantity[file_no, 0] =  mass_cl_cc85/MSun # Solar mass
            quantity[file_no, 1] =  mass_cl_vanl/MSun # Solar mass
            quantity[file_no, 2] =  np.sum(tracer_vanl*ndens_vanl*cell_vol_vanl) # mixed units
            quantity[file_no, 3] =  np.sum(tracer*ndens*cell_vol) # mixed units
            data.close()
            data_vanl.close()
            print(" "*len(string), end="\r")
        mass_evol[f"{tcool_mix_B_tcc[select]}"] = quantity
        np.save(f"mass_evol_{tcool_mix_B_tcc[select]}.npy", quantity)
        print(f"{directory}")
else:
    for select in range(len(tcool_mix_B_tcc)):
        directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
        print(f"{directory}")
        quantity = np.load(f"mass_evol_{tcool_mix_B_tcc[select]}.npy")
        mass_evol[f"{tcool_mix_B_tcc[select]}"] = quantity

with open(f'mass_evol-truncated_box.pickle', 'wb') as handle:
        pickle.dump(mass_evol, handle, protocol=pickle.HIGHEST_PROTOCOL)

do_plot = True
colors = ["yellowgreen", "steelblue", "darkorchid", "plum", "goldenrod", "crimson"]
if do_plot:
    with open(f'mass_evol-truncated_box.pickle', 'rb') as handle:
        data = pickle.load(handle)
        print(data.keys())

        c_indx = 0
        for select, tcoolBtcc in enumerate(tcool_mix_B_tcc):
            if tcoolBtcc not in [0.1, 0.2, 0.5, 0.8, 2.5, 8.0]: continue
            if tcoolBtcc==0.1:
                trunc = 32
            elif tcoolBtcc==0.2:
                trunc = 62
            else:
                trunc = -1
            mass_cl_cc85 = data[f"{tcoolBtcc}"][:,0]
            mass_cl_vanl = data[f"{tcoolBtcc}"][:,1]
            directory_vanl = f"{root_vanl}-c{chi:d},m{mach:.3f},T4e4,t{tcoolBtcc:.2f},r{rini_B_rcl[select]:.3f}"
            analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
            if trunc == -1:
                line = plt.semilogy(np.arange(0, mass_cl_cc85.shape[0], 1.0), mass_cl_cc85/mass_cl_cc85[0], label=f"{tcoolBtcc:.2f}", color=colors[c_indx])
                plt.semilogy(analysis_file_vanl[:,0]/10, analysis_file_vanl[:,6], color=line[-1].get_color(), linestyle=(0, (5, 5)), linewidth=1.5, alpha=1.0)
            else:
                zorder = 100 if tcool_mix_B_tcc == 0.1 else 50
                line = plt.semilogy(np.arange(0, mass_cl_cc85.shape[0], 1.0)[:trunc+1], mass_cl_cc85[:trunc+1]/mass_cl_cc85[0], 
                                    label=f"{tcoolBtcc:.2f}", color=colors[c_indx], zorder=zorder)
                plt.semilogy(analysis_file_vanl[:,0]/10, analysis_file_vanl[:,6], 
                             color=line[-1].get_color(), linestyle=(0, (5, 5)), linewidth=1.5, alpha=1.0, zorder=zorder)
                plt.semilogy([np.arange(0, mass_cl_cc85.shape[0], 1.0)[trunc]], [mass_cl_cc85[trunc]/mass_cl_cc85[0]], 
                             color=colors[c_indx], linestyle = ":", marker="x", markersize=8, zorder=zorder)
            # plt.semilogy(np.arange(0, mass_cl_vanl.shape[0], 1.0), mass_cl_vanl/mass_cl_vanl[0], color=line[-1].get_color(), linestyle="--")
            c_indx += 1
        plt.legend(loc="upper left", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        plt.ylim(ymin=5.0e-02)
        plt.xlim(xmin=0., xmax =99.9)
        plt.xlabel(r"time [$t_{\rm cc,ini}$]")
        plt.ylabel(r"$M_{\rm cold}$ ($T<8\times 10^4$ K) [$M_{\rm cold, ini}$]")
        plt.savefig(f"mass-cold-trunc{'-dark' if dark else ''}.svg", transparent=False)
        plt.show()
        plt.close()

        c_indx = 0
        for select, tcoolBtcc in enumerate(tcool_mix_B_tcc):
            if tcoolBtcc not in [0.1, 0.2, 0.5, 0.8, 2.5, 8.0]: continue
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcoolBtcc:.2f},r{rini_B_rcl[select]:.3f}"
            analysis_file = np.loadtxt(f"{directory}/analysis.dat")

            # plt.semilogy(analysis_file[:,0]/10, analysis_file[:,1]/rini_B_rcl[select], label=f"{tcoolBtcc:.2f}")
            plt.semilogy(analysis_file[:,0]/10, 
                         CC85wind_density( (analysis_file[:,1]/rini_B_rcl[select])*diniBdinj )/CC85wind_density(diniBdinj),
                         label=f"{tcoolBtcc:.2f}", color=colors[c_indx])
            c_indx += 1
        plt.legend(loc="lower left", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        # plt.ylim(ymin=2.0e-02)
        plt.xlim(xmin=0.1, xmax =99.9)
        plt.xlabel(r"time [$t_{\rm cc,ini}$]")
        plt.ylabel(r"wind density near COM [$\rho_{\rm ini}$]")
        # plt.savefig("mass-cold-trunc.svg", transparent=False)
        plt.show()
        plt.close()
