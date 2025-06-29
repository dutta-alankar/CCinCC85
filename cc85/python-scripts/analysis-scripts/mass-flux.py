# -*- coding: utf-8 -*-
"""
Created on Fri Apr  26 11:33:48 2024

@author: alankar
Usage: time python mass-flux.py van T cr T
"""
import numpy as np
import pickle
import h5py
import sys
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
import logging

if len(sys.argv)<5:
    print("Wrong usage!")
    sys.exit(1)

vanilla = sys.argv[2] == "T" 

# create logger with 'mass-flux'
logger = logging.getLogger(f'mass_flux{"-vanl" if vanilla else ""}')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(f'mass_flux{"-vanl" if vanilla else ""}.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

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
matplotlib.rcParams["figure.figsize"] = (13,10)

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

mu = 0.60917
mp = 1.6726e-24
Myr = 1.0e+06 * 365*24*60*60

create = sys.argv[4]=="T"

root = f"../../output{'-vanl' if vanilla else ''}"

contrasts = np.arange(int(chi*1.02), 4, -1)
# distance_factor = (contrasts/chi)**(-1./(2*(gamma-1)))
# checkpoint_wind_temperatures = np.array([110, 100, 80, 60, 40, 30, 20, 10, 4][::-1])*Tcl
print("Twind:", end=" [")
for contrast in contrasts:
    print(f"{(contrast*Tcl):.2e}", end=", ")
print("\b\b]")
Tmix = np.sqrt(chi)*Tcl
Tcutoff = 1.4e+05
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print(f"{till+1} files analyzed for each tcool_mix_B_tcc")
logger.info(f"{till+1} files analyzed")
logger.info(f"Tmix = {Tmix:.1e} K")
logger.info(f"Tcutoff = {Tcutoff:.1e} K")

flux_data = {}
analyze_freq = 1   
if create:
    for select in range(len(tcool_mix_B_tcc)):
        quantity = np.zeros( (till+1, contrasts.shape[0], 3), dtype=np.float64)
        # quantities are (distance, flux, Twind) for every file at all distances down the wind
        UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        distance_ini = None
        for file_no in range(0, till+1, analyze_freq):
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
            string = f"{output_file}: {file_no}"
            print(string, end="\r")
            logger.info(string)
            if file_no == 0:
                UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
                UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
                UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
                distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
            data = h5py.File(output_file, "r")
            del_T = np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten()
            temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            density   = np.array(data[f"/Timestep_{file_no}/vars/ndens"]).flatten()*mu*mp
            velocity  = np.array(data[f"/Timestep_{file_no}/vars/vr"]).flatten()
            Twind = temperature/(1 + del_T)
            x_cells = np.array(data["/cell_coords/X"]).flatten()
            y_cells = np.array(data["/cell_coords/Y"]).flatten()
            z_cells = np.array(data["/cell_coords/Z"]).flatten()
            distance_cells = np.sqrt(x_cells**2 + y_cells**2 + z_cells**2)
            distance_cellthick = np.min(np.abs(distance_cells[1:]-distance_cells[:-1]))
            cutoff = Twind>Tcutoff # for vanilla this is the entire domain
            # clip the domain
            del_T = del_T[cutoff]
            temperature = temperature[cutoff]
            cell_vol  = cell_vol[cutoff]
            density   = density[cutoff]
            velocity  = velocity[cutoff]
            Twind = Twind[cutoff]
            x_cells = x_cells[cutoff]
            y_cells = y_cells[cutoff]
            z_cells = z_cells[cutoff]
            distance_cells = distance_cells[cutoff]
            if Twind.shape[0] == 0: # all of the wind is colder than cutoff
                logger.info(f"Wind has become cooler than {Tcutoff:.1e} K")
                for rest_file_no in range(file_no, till+1):
                    for column in range(quantity.shape[-1]):
                        quantity[rest_file_no, :, column] = np.nan * np.ones_like(contrasts)
                data.close()
                print(" "*len(string), end="\r")
                print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                break
            if not(vanilla):
                temperature_checkpoints_indx = [np.argmin(np.abs(contrast*Tcl - Twind)) for contrast in contrasts]
                # print("Test:", [Twind[indx] for indx in temperature_checkpoints_indx])
                # print("sim dist:", [distance_cells[indx] for indx in temperature_checkpoints_indx])
                # print("req dist:", distance_ini*distance_factor)
                quantity[file_no, :, 0] = np.array( [distance_cells[indx] for indx in temperature_checkpoints_indx] )
                quantity[file_no, :, 2] = np.array( [Twind[indx] for indx in temperature_checkpoints_indx] )
                # All action has moved past the region of interest and clipped off by tracking
                if (quantity[file_no, :, 0][0] == quantity[file_no, :, 0][-1]):
                    for rest_file_no in range(file_no, till+1):
                        for column in range(quantity.shape[-1]):
                            quantity[rest_file_no, :, column] = np.nan * np.ones_like(contrasts)
                    data.close()
                    print(" "*len(string), end="\r")
                    print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                    break
            else: # load the distances from cc85 sims
                series_cc85 = np.load(f"mass-flux_{tcool_mix_B_tcc[select]}.npy")
                quantity[file_no, :, 0] = series_cc85[file_no, :, 0]*distance_ini
                quantity[file_no, :, 2] = np.ones_like(contrasts)*np.average(Twind)
                if np.sum(np.isnan(series_cc85[file_no, :, 0])) == contrasts.shape[0]:
                    data.close()
                    for rest_file_no in range(file_no, till+1):
                        for column in range(quantity.shape[-1]):
                            quantity[rest_file_no, :, column] = np.nan * np.ones_like(contrasts)
                    print(" "*len(string), end="\r")
                    print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                    break
            for indx, shell_dist in enumerate(quantity[file_no, :, 0]):
                string = f"shell dist: {shell_dist:.2f}"
                string = f"{output_file}: {file_no}; {string}"
                print(string, end="\r")
                logger.info(string)
                if indx > 0:
                    if (quantity[file_no, :, 0][indx-1] == shell_dist):
                        for fill in range(1, quantity.shape[-1]):
                            quantity[file_no, indx, fill] = quantity[file_no, indx-1, fill]
                        continue

                if shell_dist<np.min(distance_cells) or shell_dist>np.max(distance_cells):
                    # Since initial distances are chosen for vanilla, 
                    # tracking can remove a part of the smaller distances considered at some later time
                    logger.info(f"Problem: selected region is beyond cutoff. {'This is unexpected!' if not(vanilla) else ''}")
                    continue
                # print(f"d/d_ini = {checkpoint_distance/distance_ini:.2f}, T = {checkpoint_wind_temperatures[indx_checkpoint]:.1e} K")
                # find the shell distance in sim that is closest to current shell_dist
                closest_shell_dist_in_sim = distance_cells[np.argmin( np.abs(distance_cells - shell_dist) )]
                # print("Test:", shell_dist, closest_shell_dist_in_sim)

                cells_chosen = ( (np.abs(distance_cells - closest_shell_dist_in_sim)/closest_shell_dist_in_sim) < 1.0e-06 )
                logger.info(f"number of cells chosen at this shell: {np.sum(cells_chosen)}")
                logger.info(f"distance of cells chosen (target {shell_dist:.2f}): ")
                logger.info(distance_cells[cells_chosen])
                # print("Test:", (distance_cells[cells_chosen])[0])
                # cells_chosen = np.logical_and(distance >= (shell_dist-0.5*distance_cellthick), distance <= (shell_dist+0.5*distance_cellthick) )
                if np.sum(cells_chosen) == 0:
                    quantity[file_no, indx, 1] =  0.
                    continue
                Temperature_identify = 3.3*Tcl
                cells_chosen = np.logical_and(cells_chosen, temperature<Temperature_identify )
                if np.sum(cells_chosen) == 0:
                    quantity[file_no, indx, 1] =  0.
                    continue
                flux = np.sum(density[cells_chosen]*velocity[cells_chosen]*(cell_vol[cells_chosen]/distance_cellthick))*UNIT_VELOCITY*UNIT_LENGTH**2 # CGS
                mass_cloud_ini = chi*(4*np.pi/3)*UNIT_DENSITY*UNIT_LENGTH**3
                flux = flux/(mass_cloud_ini/Myr)
                # print(f"Flux = {flux:.2e} M_cl/Myr")
                quantity[file_no, indx, 1] =  flux
            data.close()
            # XXX: normalization of distance change here to d_ini from R_cl
            quantity[file_no, :, 0] = quantity[file_no, :, 0]/distance_ini
            print(" "*len(string), end="\r")
        flux_data[f"{tcool_mix_B_tcc[select]}"] = quantity
        np.save(f"mass-flux{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}.npy", quantity)
        print(f"{directory}")
    with open(f'mass-flux{"-vanl" if vanilla else ""}.pickle', 'wb') as handle:
        pickle.dump(flux_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''
if not(create):
    with open(f'mass-flux{"-vanl" if vanilla else ""}.pickle', 'rb') as handle:
        flux_data = pickle.load(handle)

print(flux_data[list(flux_data.keys())[0]].shape)
os.makedirs('./flux-figs', exist_ok = True)
plot_freq = 2
for select in range( 2 ): # min(len(flux_data.keys()),len(tcool_mix_B_tcc))
    series = np.load(f"mass-flux{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}.npy") # flux_data[f"{tcool_mix_B_tcc[select]}"]
    if tcool_mix_B_tcc[select] != 0.1:
        continue
    # print(flux.shape)
    # if select != 1:
    #     continue
    for time_indx in range(0, min(till+1, series.shape[0])-65, plot_freq):
        # if time_indx == 20:
        #     print(flux[time_indx, :, 0], flux[time_indx, :, 1])
        # print(time_indx)
        plt.plot(series[time_indx, :, 0], series[time_indx, :, 1], label=f"{(time_indx):.1f}")
        if time_indx == 0:
            xold = series[time_indx, :, 0]
            xnew = xold*rini_B_rcl[select] # units of R_cl

    ax1 = plt.gca()
    plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
               prop = { "size": 16 }, title_fontsize=16, fancybox=True)
    # plt.ylim(ymin=1.03e-03,  ymax=18)
    
    forward = lambda arg: arg*rini_B_rcl[select]
    inverse = lambda arg: arg/rini_B_rcl[select]
    # ax2 = plt.gca().twiny()
    ax1.set_xlim(xmin=1.0, xmax=7.6)
    # ax2.grid()

    ax2 = plt.gca().secondary_xaxis('top', functions=(forward, inverse))
    ax1.set_ylabel(r"$\dot{M}\ {\rm [}M_{\rm cl,ini}\ {\rm Myr^{-1}}{\rm ]}$")
    ax1.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
    ax2.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
    plt.savefig(f"./flux-figs/flux-dist-{tcool_mix_B_tcc[select]}{'-vanl' if vanilla else ''}.svg", transparent=False, bbox_inches="tight")
    plt.close()

matplotlib.rcParams["xtick.top"] = True
for select in range( min(len(flux_data.keys()),len(tcool_mix_B_tcc)) ): 
    series = np.load(f"mass-flux{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}.npy") # flux_data[f"{tcool_mix_B_tcc[select]}"]
    # print(flux.shape)
    for time_indx in range(0, min(till+1, series.shape[0]), plot_freq):
        if time_indx != 2:
            continue
        #     print(flux[time_indx, :, 0], flux[time_indx, :, 1])
        # print(time_indx)
        plt.loglog(series[time_indx, :, 0], series[time_indx, :, 2], label=f"{tcool_mix_B_tcc[select]}")

plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 16 }, title_fontsize=16, fancybox=True)
# plt.ylim(ymin=1.03e-03,  ymax=18)
plt.ylabel(r"Wind temperature [$\rm K$]")
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.savefig("flux-Twind.svg", transparent=False, bbox_inches="tight")
plt.close()
'''
