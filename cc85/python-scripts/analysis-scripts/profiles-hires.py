# -*- coding: utf-8 -*-
"""
Created on Fri Apr  26 11:33:48 2024

@author: alankar.
Usage: time python profiles-hires.py van F cr T
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
combine = False

# create logger with 'profiles'
logger = logging.getLogger(f'profiles{"-vanl" if vanilla else ""}')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(f'profiles{"-vanl" if vanilla else ""}.log')
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
matplotlib.rcParams["grid.linestyle"] = "-."
matplotlib.rcParams["grid.linewidth"] = 0.8
matplotlib.rcParams["grid.color"] = "gray"
matplotlib.rcParams["grid.alpha"] = 0.4
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
else:
    tcool_mix_B_tcc = tcool_mix_B_tcc[2:4]
    rini_B_rcl = rini_B_rcl[2:4]
    
mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 66
analyze_freq = 8

wind = np.loadtxt('../../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach_data = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]
relpos = interp1d(mach_data, rnorm) #inverting the Mach relation
diniBdinj = relpos(mach)
CC85windrho = interp1d(rnorm, wind[:,1])
CC85windprs = interp1d(rnorm, wind[:,2])
CC85windvel = interp1d(rnorm, wind[:,3])

mu = 0.60917
mp = 1.6726e-24
Myr = 1.0e+06 * 365*24*60*60

create = sys.argv[4] == "T"

root = f"../../output{'-vanl' if vanilla else ''}"
dump_directory = "profile-hires_selected"
os.makedirs(f'./{dump_directory}', exist_ok = True)

grid_space = 0.25
Tmix = np.sqrt(chi)*Tcl
Tcutoff = 9.0e+04
Temperature_identify = 8.0e+04 # 3.3*Tcl
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Temperature_identify: %.2e K"%Temperature_identify)
print(f"{(till+1)//analyze_freq} files analyzed for each tcool_mix_B_tcc")
logger.info(f"{till+1} files analyzed")
logger.info(f"Tmix = {Tmix:.1e} K")
logger.info(f"Tcutoff = {Tcutoff:.1e} K")
logger.info(f"Temperature_identify = {Temperature_identify:.1e} K")

profiles = {}
 
if create:
    for select in range(len(tcool_mix_B_tcc)):
        # vel is in code units while density is in CGS
        UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        distance_ini = None
        files_analyze = np.arange(0, till+1, analyze_freq)
        count = 0
        for file_no in files_analyze[::-1]: #range(0, till+1, analyze_freq):
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
            string = f"{output_file}: {file_no}"
            print(string, end="\r")
            logger.info(string)
            if count == 0:
                UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
                UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
                UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
                distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
            count += 1
            data = h5py.File(output_file, "r")
            del_T = np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten()
            del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
            temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()
            density   = np.array(data[f"/Timestep_{file_no}/vars/ndens"]).flatten()*mu*mp # CGS
            velocity  = np.array(data[f"/Timestep_{file_no}/vars/vr"]).flatten()
            # tracer    = np.array(data[f"/Timestep_{file_no}/vars/tr1"]).flatten()
            Twind = temperature/(1 + del_T)
            rho_wind = density/(1 + del_rho)
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
            rho_wind = rho_wind[cutoff]
            x_cells = x_cells[cutoff]
            y_cells = y_cells[cutoff]
            z_cells = z_cells[cutoff]
            distance_cells = distance_cells[cutoff]
            # tracer = tracer[cutoff]

            cloud_marker = temperature<=Temperature_identify
            cloud_grid = np.arange(np.min(distance_cells[cloud_marker]), np.max(distance_cells[cloud_marker])+grid_space, grid_space)
            grid_points = cloud_grid.shape[0]
            quantity = np.zeros( (grid_points, 8), dtype=np.float64)
            # quantities are (distance, T_wind, rho_wind, v_wind, T_cl, rho_cl, v_cl, flux_cl) for every file at all distances down the wind
            string = f"{output_file}: {file_no} ({cloud_grid[0]:.2f}, {cloud_grid[-1]:.2f}, {grid_points})"
            print(string, end="\r")
            logger.info(string)
            # string = string + f"; cloud extent: ({np.min(distance_cells[cloud_tracer]):.1f}, {np.max(distance_cells[cloud_tracer]):.1f}) R_cl"
            # print(string, end="\r")
            logger.info(f"cloud extent: ({np.min(distance_cells[cloud_marker]):.1f}, {np.max(distance_cells[cloud_marker]):.1f}) R_cl")

            if Twind.shape[0] == 0: # all of the wind is colder than cutoff
                logger.info(f"Wind has become cooler than {Tcutoff:.1e} K")
                quantity[:, :] = np.nan * np.ones((grid_points,7))
                '''
                for rest_file_no in range(file_no, till+1):
                    for column in range(quantity.shape[-1]):
                        quantity[rest_file_no, :, column] = np.nan * np.ones(grid_points)
                '''
                data.close()
                print(" "*len(string), end="\r")
                print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                break
            if not(vanilla):
                cloud_checkpoints_indx = [np.argmin(np.abs(grid_pos - distance_cells)) for grid_pos in cloud_grid]
                # print("Test:", [Twind[indx] for indx in cloud_checkpoints_indx])
                # print("sim dist:", [distance_cells[indx] for indx in cloud_checkpoints_indx])
                # print("req dist:", distance_ini*distance_factor)
                quantity[:, 0] = np.array( [distance_cells[indx] for indx in cloud_checkpoints_indx] ) # code units R_cl
                quantity[:, 1] = np.array( [Twind[indx] for indx in cloud_checkpoints_indx] ) # K
                quantity[:, 2] = np.array( [rho_wind[indx] for indx in cloud_checkpoints_indx] ) # cgs
                # All action has moved past the region of interest and clipped off by tracking
                if (quantity[0, 0] == quantity[-1, 0]):
                    quantity[:, :] = np.nan * np.ones((grid_points,7))
                    '''
                    for rest_file_no in range(file_no, till+1, analyze_freq):
                        for column in range(quantity.shape[-1]):
                            quantity[rest_file_no, :, column] = np.nan * np.ones(grid_points)
                    '''
                    data.close()
                    print(" "*len(string), end="\r")
                    print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                    break
            else: # load the distances from cc85 sims
                series_cc85 = np.load(f"profiles_{tcool_mix_B_tcc[select]}.npy")
                quantity[:, 0] = series_cc85[file_no, :, 0]*distance_ini # code units R_cl
                quantity[:, 1] = np.ones(grid_points)*np.average(Twind) # K
                quantity[:, 2] = np.ones(grid_points)*UNIT_DENSITY # cgs
                if np.sum(np.isnan(series_cc85[file_no, :, 0])) == grid_points:
                    data.close()
                    '''
                    for rest_file_no in range(file_no, till+1):
                        for column in range(quantity.shape[-1]):
                            quantity[rest_file_no, :, column] = np.nan * np.ones(grid_points)
                    '''
                    print(" "*len(string), end="\r")
                    print(f"{directory}", end="; cold wind!\n" if file_no == till else "\r")
                    break
            # start loop for every shell
            closest_shell_dist_in_sim_old = np.inf
            # string_orig = string[:] # copy
            for indx, shell_dist in enumerate(quantity[:, 0]):
                # string = string_orig  + f"; {shell_dist:.2f}"
                # string = f"{output_file}: {file_no}; {string}"
                logger.info(f"analysis shell dist: {shell_dist:.2f}")
                # wind
                if indx > 0:
                    if (quantity[indx-1, 0] == shell_dist):
                        quantity[indx, 3:] = quantity[indx-1, 3:]
                        continue
                if not(vanilla):
                    quantity[indx, 3] =  CC85windvel(shell_dist/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
                else:
                    quantity[indx, 3] = 1.0 # code units

                if shell_dist<np.min(distance_cells) or shell_dist>np.max(distance_cells):
                    # Since initial distances are chosen for vanilla, 
                    # tracking can remove a part of the smaller distances considered at some later time
                    logger.info(f"{'Problem: ' if not(vanilla) else ''}Selected region is beyond cutoff. {'This is unexpected!' if not(vanilla) else ''}")
                    if not(vanilla):
                        continue
                    else:
                        if shell_dist>np.max(distance_cells):
                            logger.info("Problem: Selected region is beyond upper cutoff. This is unexpected!")
                            continue
                        logger.info("This can be due to cells dropped from left by tracking")
                        continue

                # find the shell distance in sim that is closest to current shell_dist
                closest_shell_dist_in_sim = distance_cells[np.argmin( np.abs(distance_cells - shell_dist) )]
                # string = string  + f" ({closest_shell_dist_in_sim:.2f} old: {closest_shell_dist_in_sim_old:.2f})"
                # print(string, end="\r")
                logger.info(f"{closest_shell_dist_in_sim} in sim")
                # print("Test:", shell_dist, closest_shell_dist_in_sim)

                if closest_shell_dist_in_sim_old != closest_shell_dist_in_sim:
                    closest_shell_dist_in_sim_old = closest_shell_dist_in_sim
                    cells_chosen = ( (np.abs(distance_cells - closest_shell_dist_in_sim)/closest_shell_dist_in_sim) < 1.0e-06 )
                    logger.info(f"number of cells chosen at this shell: {np.sum(cells_chosen)}")
                    logger.info(f"distance of cells chosen (target {shell_dist:.2f}): ")
                    logger.info(distance_cells[cells_chosen])
                    # print("Test:", (distance_cells[cells_chosen])[0])
                    # cells_chosen = np.logical_and(distance >= (shell_dist-0.5*distance_cellthick), distance <= (shell_dist+0.5*distance_cellthick) )
                    if np.sum(cells_chosen) == 0:
                        # quantity[indx, 1] =  0. # resets Twind; not desired
                        continue
                    cells_chosen = np.logical_and(cells_chosen, temperature<=Temperature_identify)
                    if np.sum(cells_chosen) == 0:
                        # quantity[indx, 1] =  0. # resets Twind; not desired
                        continue
                    temperature_cl = np.sum(density[cells_chosen]*temperature[cells_chosen]*cell_vol[cells_chosen])/np.sum(density[cells_chosen]*cell_vol[cells_chosen]) # K
                    density_cl = np.sum(density[cells_chosen]*cell_vol[cells_chosen])/np.sum(cell_vol[cells_chosen]) # cgs
                    velocity_cl = np.sum(density[cells_chosen]*velocity[cells_chosen]*cell_vol[cells_chosen])/np.sum(density[cells_chosen]*cell_vol[cells_chosen]) # code units

                    quantity[indx, 4] =  temperature_cl # K
                    quantity[indx, 5] =  density_cl # cgs
                    quantity[indx, 6] =  velocity_cl # code units
                    quantity[indx, 7] =  np.sum((4*np.pi*(closest_shell_dist_in_sim*UNIT_LENGTH)**2 * density[cells_chosen] * velocity[cells_chosen] * UNIT_VELOCITY) * cell_vol[cells_chosen]) / np.sum(cell_vol[cells_chosen]) # cgs
                else:
                    quantity[indx, 4:] =  quantity[ indx-1, 4:]
            data.close()
            # XXX: normalization of distance change here to d_ini from R_cl
            quantity[:, 0] = quantity[:, 0]/distance_ini
            np.save(f"{dump_directory}/profiles{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}_{file_no:04d}.npy", quantity)
            print(" "*len(string), end="\r")
        # profiles[f"{tcool_mix_B_tcc[select]}"] = quantity
        # np.save(f"{dump_directory}/profiles{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}.npy", quantity)
        print(f"{directory}")
    # with open(f'{dump_directory}/profiles{"-vanl" if vanilla else ""}.pickle', 'wb') as handle:
    #     pickle.dump(profiles, handle, protocol=pickle.HIGHEST_PROTOCOL)
# if combine:
#     for select in range(len(tcool_mix_B_tcc)):
#         profiles[f"{tcool_mix_B_tcc[select]}"] = np.load(f"{dump_directory}/profiles{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}.npy")
#     with open(f'{dump_directory}/profiles{"-vanl" if vanilla else ""}.pickle', 'wb') as handle:
#         pickle.dump(profiles, handle, protocol=pickle.HIGHEST_PROTOCOL)

'''
if not(create):
    with open(f'profiles{"-vanl" if vanilla else ""}.pickle', 'rb') as handle:
        profiles = pickle.load(handle)
'''
# print(profiles[list(profiles.keys())[0]].shape)

os.makedirs(f"{dump_directory}/plots", exist_ok = True)
plot_type = "rho"
for select in range(len(tcool_mix_B_tcc)):
        UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
        distance_ini, distance_min, distance_max = None, None, None
        files_analyze = np.arange(0, till+1, analyze_freq)
        count = 0
        # colors = plt.cm.jet(matplotlib.colors.LogNorm( vmin=np.min(nH), vmax=np.max(nH) )(nH))
        colors = plt.cm.Paired(matplotlib.colors.Normalize( vmin=0, vmax=files_analyze.shape[0])(np.arange(0, files_analyze.shape[0]+1, 1)))
        for file_no in files_analyze: #range(0, till+1, analyze_freq):
            directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
            output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
            string = f"{output_file}: {file_no}"
            print(string, end="\r")
            if count == 0:
                UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
                UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
                UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
                distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
                ndens_w_ini  = UNIT_DENSITY/(mu*mp)
                ndens_cl_ini = chi * ndens_w_ini
                prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
            quantity = np.load(f"{dump_directory}/profiles{'-vanl' if vanilla else ''}_{tcool_mix_B_tcc[select]}_{file_no:04d}.npy")

            distance  = quantity[:,0] # units of d_ini
            temp_cl   = quantity[:,4] # K
            ndens_cl  = quantity[:,5]/(mu*mp) # cgs
            
            prs_cl    = ndens_cl*temp_cl/prs_w_ini
            ndens_cl  = ndens_cl/ndens_w_ini
            
            if plot_type=="rho":
                plt.semilogy(distance[ndens_cl>0], ndens_cl[ndens_cl>0], label = f"{file_no}", color=colors[count] if count<(files_analyze.shape[0]-1) else colors[count+1])
            else:
                plt.semilogy(distance[ndens_cl>0], prs_cl[ndens_cl>0], label = f"{file_no}", color=colors[count] if count<(files_analyze.shape[0]-1) else colors[count+1])
            if count==0:
                distance_min = np.min(distance)
                distance_max = np.max(distance)
            else:
                distance_min = distance_min if (_tmp:=np.min(distance))>distance_min else _tmp
                distance_max = distance_max if (_tmp:=np.max(distance))<distance_max else _tmp
            count += 1

        ndens_w   = (CC85windrho(distance_w:=np.linspace(distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini
        
        if plot_type=="rho":
            plt.semilogy(distance_w, ndens_w/ndens_w_ini, linestyle="--", color="black")
            plt.semilogy(distance_w, prs_w/prs_w_ini*chi, linestyle=":", color="gray")
            # plt.semilogy(distance_w, (ndens_cl_ini/ndens_w_ini)*distance_w**(-2*gamma), linestyle=":", color="black")
        else:
            plt.semilogy(distance_w, prs_w/prs_w_ini, linestyle=":", color="black")

        plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
                   prop = { "size": 24 }, title_fontsize=26, fancybox=True)
        
        if plot_type=="rho":
            plt.ylabel("Density (initial wind density)")
        else:
            plt.ylabel("Pressure (initial wind pressure)")
        plt.xlabel("Distance (initial cloud position)")
        
        plt.xlim(xmin=0.7, xmax=np.max(distance_max))
        if plot_type=="rho":
            plt.ylim(ymin=2.0e-03, ymax=2.0e+02)
        else:
            plt.ylim(ymin=3.8e-05, ymax=1.6+00)
        
        plt.title(r"$t_{\rm cool,mix}/t_{\rm cc}|_{\rm ini}$ = %.1f"%tcool_mix_B_tcc[select], size=28, pad=20)

        if plot_type=="rho":
            plt.savefig(f'{dump_directory}/plots/tcmBtcc_{tcool_mix_B_tcc[select]}_rho.svg', 
                        transparent=False, bbox_inches="tight")
        else:
            plt.savefig(f'{dump_directory}/plots/tcmBtcc_{tcool_mix_B_tcc[select]}_prs.svg', 
                        transparent=False, bbox_inches="tight")
        plt.close()
        
        print(" "*len(string), end="\r")
        print(f"{output_file}")

