# -*- coding: utf-8 -*-
"""
Created on Sat May 11 11:14:42 2024

@author: alankar
Usage: time python shell-calc.py van T cr T
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
import logging

if len(sys.argv)<5:
    print("Wrong usage!")
    sys.exit(1)

vanilla = sys.argv[2] == "T" 

# create logger with 'shell_calc'
logger = logging.getLogger(f'shell_calc{"-vanl" if vanilla else ""}')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(f'shell_calc{"-vanl" if vanilla else ""}.log')
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

wind = np.loadtxt('../../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach_data = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]
relpos = interp1d(mach_data, rnorm) #inverting the Mach relation
diniBdinj = relpos(mach)
CC85wind = interp1d(rnorm, wind[:,3])

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

X_solar = 0.7154
Y_solar = 0.2703
Z_solar = 0.0143
fracZ   = 1.0
Xp      = X_solar*(1-fracZ*Z_solar)/(X_solar+Y_solar)
Yp      = Y_solar*(1-fracZ*Z_solar)/(X_solar+Y_solar)
Zp      = fracZ*Z_solar
mu     = 1./(2*Xp+0.75*Yp+0.5625*Zp)
mp     = 1.67262192369e-24
kB     = 1.3806505e-16

create = sys.argv[4] == "T"

root = f"../../output{'-vanl' if vanilla else ''}"

Tmix = np.sqrt(chi)*Tcl
Temperature_cold = 8.0e+04 # 3.3*Tcl
Tcutoff = 9.0e+04
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Tcold: %.2e K"%Temperature_cold)
print(f"{till+1} files analyzed for each tcool_mix_B_tcc")
logger.info(f"{till+1} files analyzed")
logger.info(f"Tmix = {Tmix:.1e} K")
logger.info(f"Tcutoff = {Tcutoff:.1e} K")

analyze_freq = 1   
if create:
    os.makedirs("./shell-calcs", exist_ok = True)
    for select in range(len(tcool_mix_B_tcc)):
        UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        quantity = None # re-initialized later
        distance_ini = None
        mass_cl_tot = np.zeros(till+1, dtype=np.float64)
        cloud_profiles = []
        for file_no in range(0, till+1, analyze_freq):
            quantities = {}
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
            del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
            temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            density   = np.array(data[f"/Timestep_{file_no}/vars/ndens"]).flatten()*mu*mp # CGS
            velocity  = np.array(data[f"/Timestep_{file_no}/vars/vr"]).flatten()
            Twind = temperature/(1 + del_T)
            rho_wind = density/(1 + del_rho)
            x_cells = np.array(data["/cell_coords/X"]).flatten()
            y_cells = np.array(data["/cell_coords/Y"]).flatten()
            z_cells = np.array(data["/cell_coords/Z"]).flatten()
            distance_cells = np.sqrt(x_cells**2 + y_cells**2 + z_cells**2)
            distance_cellthick = np.min(np.abs(distance_cells[1:]-distance_cells[:-1]))
            cutoff = Twind>Tcutoff # for vanilla this is the entire domain
            cells_cold = temperature<Temperature_cold
            cutoff = np.logical_and(cutoff, cells_cold)
            # clip the domain
            del_T = del_T[cutoff]
            temperature = temperature[cutoff]
            cell_vol  = cell_vol[cutoff]
            density   = density[cutoff]
            velocity  = velocity[cutoff]
            Twind = Twind[cutoff]
            rho_wind = rho_wind[cutoff]
            x_cells = x_cells[cutoff]
            y_cells = y_cells[cutoff]
            z_cells = z_cells[cutoff]
            distance_cells = distance_cells[cutoff]
            if Twind.shape[0] == 0: # all of the wind is colder than cutoff
                logger.info(f"Wind has become cooler than {Tcutoff:.1e} K or no clouds remain")
                data.close()
                print(" "*len(string), end="\r")
                print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                break    
            mass_cl_tot[file_no] = np.sum(density*cell_vol)*UNIT_LENGTH**3 # CGS

            # calculate cloud quantitites at fixed shells down the wind
            shells = np.arange(np.min(distance_cells)-1.0, np.max(distance_cells)+1.0, 0.5)
            string = string + f"total shells: {shells.shape[0]}"
            print(string, end="\r")
            # quantities are (distance, T_wind, rho_wind, v_wind, T_cl, rho_cl, v_cl, flux_cl, m_cl, Rcl, tcool, tcc, tsc) for every file at all distances down the wind
            # vel and Rcl and times are in code units while density is in CGS
            if (shells.shape[0] == 0 or shells.shape[0]==1):
                logger.info(f"Wind has become cooler than {Tcutoff:.1e} K or no clouds remain")
                data.close()
                print(" "*len(string), end="\r")
                print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                break
            quantities["tBtccini"] = file_no
            quantities["distanceiniBdini"] = distance_ini
            # create but not assign values
            quantities["distanceBRcl"] = np.zeros_like(shells)
            quantities["Twind"]   = np.zeros_like(shells)
            quantities["rhowind"] = np.zeros_like(shells)
            quantities["vwind"]   = np.zeros_like(shells)
            quantities["T_cl"]    = np.zeros_like(shells)
            quantities["rho_cl"]  = np.zeros_like(shells)
            quantities["v_cl"]    = np.zeros_like(shells)
            quantities["flux_cl"] = np.zeros_like(shells)
            quantities["m_cl"]    = np.zeros_like(shells)
            quantities["Rclprp"]     = np.zeros_like(shells)
            quantities["texp"]   = np.zeros_like(shells)
            quantities["tcc"]     = np.zeros_like(shells)
            quantities["tsc"]     = np.zeros_like(shells)
            quantities["tcool"]   = np.zeros_like(shells)
            
            # start loop for every shell
            for indx, shell_dist in enumerate(shells):
                string = f"shell dist: {shell_dist:.2f}"
                string = f"{output_file}: {file_no}; {string}"
                print(string, end="\r")
                logger.info(string)

                # find the shell distance in sim that is closest to shell_dist
                closest_shell_dist_in_sim = distance_cells[np.argmin( np.abs(distance_cells - shell_dist) )]
                quantities["distanceBRcl"][indx] = closest_shell_dist_in_sim

                if closest_shell_dist_in_sim<np.min(distance_cells) or closest_shell_dist_in_sim>np.max(distance_cells):
                    logger.info(f"Warning: Selected region is beyond cutoff. This is unexpected!")
                    continue

                # choose all cells in the required shell
                cells_chosen = ( (np.abs(distance_cells - closest_shell_dist_in_sim)/closest_shell_dist_in_sim) < 1.0e-06 )
                logger.info(f"number of cells chosen at this shell: {np.sum(cells_chosen)}")
                logger.info(f"distance of cells chosen (target {shell_dist:.2f}, closest {closest_shell_dist_in_sim:.2f}): ")
                logger.info(distance_cells[cells_chosen])
                if np.sum(cells_chosen) == 0:
                    logger.info(f"Warning: No cells are present in the current shell!")
                    continue
                
                # wind
                quantities["Twind"][indx]   = np.sum(rho_wind[cells_chosen]*Twind[cells_chosen]*cell_vol[cells_chosen])/np.sum(rho_wind[cells_chosen]*cell_vol[cells_chosen]) # CGS
                quantities["rhowind"][indx] = np.sum(rho_wind[cells_chosen]*cell_vol[cells_chosen])/np.sum(cell_vol[cells_chosen])
                if not(vanilla):
                    quantities["vwind"][indx]   = CC85wind(quantities["distanceBRcl"][indx]/distance_ini * diniBdinj)/CC85wind(diniBdinj) # code units
                else:
                    quantities["vwind"][indx]   = 1.0 # code units

                quantities["T_cl"][indx] = np.sum(density[cells_chosen]*temperature[cells_chosen]*cell_vol[cells_chosen])/np.sum(density[cells_chosen]*cell_vol[cells_chosen]) # K
                quantities["rho_cl"][indx] = np.sum(density[cells_chosen]*cell_vol[cells_chosen])/np.sum(cell_vol[cells_chosen]) # CGS
                quantities["v_cl"][indx] = np.sum(density[cells_chosen]*velocity[cells_chosen]*cell_vol[cells_chosen])/np.sum(density[cells_chosen]*cell_vol[cells_chosen]) # code units
                quantities["m_cl"][indx] = np.sum(density[cells_chosen]*cell_vol[cells_chosen])*UNIT_LENGTH**3 # CGS
                quantities["flux_cl"][indx] = np.sum(density[cells_chosen]*velocity[cells_chosen]*(cell_vol[cells_chosen]/distance_cellthick))*UNIT_VELOCITY*UNIT_LENGTH**2 # CGS
                quantities["Rclprp"][indx]  = np.max( np.sqrt( (x_cells[cells_chosen]-quantities["distanceBRcl"][indx])**2 + y_cells[cells_chosen]**2 + z_cells[cells_chosen]**2 ) ) # code units of R_cl (code units)
                quantities["tcc"][indx]  = 2*quantities["Rclprp"][indx]/np.abs(quantities["v_cl"][indx] - quantities["vwind"][indx]) # code units
                quantities["texp"][indx] = quantities["distanceBRcl"][indx]/(2*quantities["vwind"][indx]) # code units
                quantities["tsc"][indx]  = 2*quantities["Rclprp"][indx]/(np.sqrt(gamma * kB*quantities["T_cl"][indx]/(mu*mp))/UNIT_VELOCITY) # code units
                quantities["tcool"][indx]  = (1./(gamma-1))*(quantities["rho_cl"][indx]/(mu*mp))*kB*quantities["T_cl"][indx]/( (quantities["rho_cl"][indx]/(mu*mp)*Xp)**2 * LAMBDA(quantities["T_cl"][indx]) ) / (UNIT_LENGTH/UNIT_VELOCITY) # code units

            data.close()
            quantities["distanceBdini"] = quantities["distanceBRcl"]/distance_ini
            cloud_profiles.append(quantities)
            print(" "*len(string), end="\r")
        print(f"{directory}")
        cloud_profiles.append({"mass_cl_tot": mass_cl_tot})
        with open(f'./shell-calcs/shell_profiles{"-vanl" if vanilla else ""}_{tcool_mix_B_tcc[select]}.pickle', 'wb') as handle:
            pickle.dump(cloud_profiles, handle, protocol=pickle.HIGHEST_PROTOCOL)


