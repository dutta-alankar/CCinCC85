# -*- coding: utf-8 -*-
"""
Created on Sat Apr  17 17:45:48 2025

@author: alankar.
Usage: time python profile-animation.py
"""
import numpy as np
import scipy
import subprocess as sp
from scipy.interpolate import interp1d
from scipy.stats import binned_statistic
import sys
import os
import pickle
import matplotlib
import matplotlib.pyplot as plt
from tueplots import cycler
from tueplots.constants import markers
from tueplots.constants.color import palettes
import matplotlib.patheffects as pe
from mpl_toolkits.axes_grid1 import make_axes_locatable

dark = False

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
matplotlib.rcParams["xtick.labelsize"] = 34.0
matplotlib.rcParams["ytick.labelsize"] = 34.0
matplotlib.rcParams["axes.titlesize"] = 36.0
matplotlib.rcParams["axes.labelsize"] = 36.0
matplotlib.rcParams["axes.labelpad"] = 8.0
plt.rcParams["font.size"] = 36.0
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True
matplotlib.rcParams["figure.figsize"] = (39,13)
matplotlib.rcParams["figure.constrained_layout.use"] = True

if dark:
    plt.style.use("dark_background")
colors = ["plum", "goldenrod", "steelblue", "darkorchid", "yellowgreen", "crimson"]

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

# choose the one needed
tcool_mix_B_tcc = [tcool_mix_B_tcc[2],]
rini_B_rcl = [rini_B_rcl[2],]

mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 100

cs = 1.0/mach # in unit velocity

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
kB = 1.3807e-16
Myr = 1.0e+06 * 365*24*60*60
MSun = 1.99e+33
pc   = 3.086e+18
kpc  = 1.0e+03*pc

Tmix = np.sqrt(chi)*Tcl
Tcutoff = 9.0e+04
Temperature_identify = 2.0*Tcl
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Temperature_identify: %.2e K"%Temperature_identify)

root = "../../output"
root_vanl = "../../output-vanl"
till = 100 # tcc
ext = "svg"

fig = plt.figure()
gs = fig.add_gridspec(1, 3, wspace=0)
[axP, axR, axV] = gs.subplots(sharex=True)
# axs = fig.subplots(3,3, sharex=True)

select_snap = [15, 45]
'''
if len(select_snap)!=3:
    print("Only three figs in one snap please!")
    sys.exit(0)
'''
median_snap = 8

'''
print(axs)
print(axP, axR, axV)
'''

# plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))
os.makedirs(f"profiles-anim", exist_ok = True)
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp) # cgs
    ndens_cl_ini = chi * ndens_w_ini
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs
    plot_filename = f"snap-profile-{label}"

    def tick_function(X):
        V = X * distance_ini * UNIT_LENGTH/kpc
        return [f"{z:.1f}" for z in V]

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    distance_min, distance_max = None, None
    for key in list(cloud_data.keys()):
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_temperature = cloud_data[key]['cloud_temperature']

        fix = cloud_temperature<Tcl
        cloud_pressure[fix] = (Tcl/cloud_temperature[fix])*cloud_pressure[fix]

        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        if count==0:
            distance_min = np.min(cloud_distance)
            distance_max = np.max(cloud_distance)
        else:
            distance_min = distance_min if (_tmp:=np.min(cloud_distance))>distance_min else _tmp
            distance_max = distance_max if (_tmp:=np.max(cloud_distance))<distance_max else _tmp
        count += 1

    print(distance_min, distance_max)
    count = 0
    ax2 = None
    for key in list(cloud_data.keys()):
        if int(key) not in select_snap:
            continue
        ini_cloud_pressure  = cloud_data[list(cloud_data.keys())[0]]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        ini_cloud_density  = cloud_data[list(cloud_data.keys())[0]]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        ini_cloud_velocity  = np.sqrt(cloud_data[list(cloud_data.keys())[0]]['cloud_velocity_r']**2 + cloud_data[list(cloud_data.keys())[0]]['cloud_velocity_th']**2 + cloud_data[list(cloud_data.keys())[0]]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        ini_cloud_volume = cloud_data[list(cloud_data.keys())[0]]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        ini_cloud_distance = cloud_data[list(cloud_data.keys())[0]]['cloud_distance']/distance_ini
        
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_velocity  = np.sqrt(cloud_data[key]['cloud_velocity_r']**2 + cloud_data[key]['cloud_velocity_th']**2 + cloud_data[key]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_temperature = cloud_data[key]['cloud_temperature']
        
        fix = cloud_temperature<Tcl
        cloud_pressure[fix] = (Tcl/cloud_temperature[fix])*cloud_pressure[fix]

        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)
        
        ndens_w_com = (CC85windrho(cloud_com * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        pwind_com = (CC85windprs(cloud_com * diniBdinj)/CC85windprs(diniBdinj)) * UNIT_DENSITY * UNIT_VELOCITY**2 # cgs
        Twind_com = pwind_com/(ndens_w_com*kB)

        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        # plot the entire cloud profile
        # initial profile
        if count==0:
            line, = axP.plot(ini_cloud_distance, ini_cloud_pressure, marker='.', markersize=0.5, 
                             linestyle='None', alpha=0.5, rasterized=True, color=colors[-1])
            axP.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{list(cloud_data.keys())[0]}")
            line, = axR.plot(ini_cloud_distance, ini_cloud_density, marker='.', markersize=0.5, 
                             linestyle='None', alpha=0.5, rasterized=True, color=colors[-1])
            # axR.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{list(cloud_data.keys())[0]}")
            line, = axV.plot(ini_cloud_distance, ini_cloud_velocity/v_w_ini, marker='.', markersize=0.5, 
                             linestyle='None', alpha=0.5, rasterized=True)
            # axV.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{list(cloud_data.keys())[0]}")

        print("pressure")
        line, = axP.plot(cloud_distance, cloud_pressure, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True, color=colors[count])
        axP.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{key}")
        print("density")
        line, = axR.plot(cloud_distance, cloud_density, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True, color=colors[count])
        # axR.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{key}")
        print("velocity")
        line, = axV.plot(cloud_distance, cloud_velocity/v_w_ini, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True, color=colors[count])
        # axV.plot([], [], color=line.get_color(), label=r"$t/t_{\rm cc,ini}$ = "+f"{key}")
        
        # plot the median profile
        if (int(key)>=median_snap):
            def plot_stat(quan, axis):
                # Calculate the bin width using the Freedman-Diaconis rule 
                q25, q75 = np.percentile(cloud_distance, [25, 75]) 
                iqr = q75 - q25 
                # Interquartile range 
                bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
                num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

                # Calculate the median y trend as a function of x 
                bin_means, bin_edges, _ = binned_statistic(cloud_distance, quan, 
                                                           statistic='median', bins=num_bins) 
                # Plot the median y trend 
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
                # Calculate bin centers for plotting 
                axis.plot(bin_centers, bin_means, color=colors[count], 
                         path_effects=[pe.Stroke(linewidth=5, foreground='black'), pe.Normal()])
            
            plot_stat(cloud_pressure, axP)
            plot_stat(cloud_density,  axR)
            plot_stat(cloud_velocity/v_w_ini, axV)
            

        '''
        if distance_min<0.5*diniBdinj:
            distance_min = 0.5*diniBdinj
        if distance_max<1.5*diniBdinj:
            distance_max = 1.5*diniBdinj
        '''    
        ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

        if count==0:
            axP.plot(distance_w, prs_w/prs_w_ini, linestyle="--", 
                     color="black" if not(dark) else "peachpuff", 
                     linewidth=2.0, label=r"$p_{\rm w}/p_{\rm w, ini}$")
            axR.plot(distance_w, ndens_w/ndens_w_ini, linestyle="--", 
                     color="black" if not(dark) else "peachpuff", 
                     linewidth=2.0, label=r"$\rho_{\rm w}/\rho_{\rm w, ini}$")
            axR.plot(distance_w, prs_w/prs_w_ini*chi, linestyle=":", 
                     color="gray" if not(dark) else "beige", linewidth=2.0, 
                     label=r"$\chi_{\rm ini} p_{\rm w}/p_{\rm w, ini}$")
            contrast_highlight = 10
            axR.plot(distance_w, contrast_highlight*ndens_w/ndens_w_ini, 
                     color="black" if not(dark) else "peachpuff", 
                     linestyle=(0, (5, 5)), label=f"{contrast_highlight}"+r"$\rho_{\rm w}/\rho_{\rm w, ini}$")
            v_w = (CC85windvel(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000)*diniBdinj)/CC85windvel(diniBdinj)) * v_w_ini
            axV.plot(distance_w, v_w/v_w_ini, linestyle="--", 
                     color="black" if not(dark) else "peachpuff", 
                     linewidth=2.0, label=r"$v_{\rm w}/v_{\rm w, ini}$")

        for axis in [axP, axR, axV]:
            handles, labels = axis.get_legend_handles_labels()
            if axis == axP: 
                last_one = (handles[0], labels[0])
                handles_rarr, labels_rarr = [], []
                for move, label in enumerate(labels):
                    if '$t/t_{\\rm cc,ini}$ =' not in label:
                        last_one = (handles[move], labels[move])
                    else:
                        handles_rarr.append(handles[move])
                        labels_rarr.append(labels[move])
                handles_rarr.append(last_one[0])
                labels_rarr.append(last_one[1])
                handles = handles_rarr
                labels = labels_rarr
                
            axis.legend(handles, labels, 
                       loc="upper right" if axis!=axV else "lower right", ncols=1,
                       prop = { "size": 34 }, title_fontsize=34, fancybox=True, framealpha=0.5)
        
        axP.set_ylim(ymin=6e-05, ymax=6.0)
        axR.set_ylim(ymin=3.1e-03, ymax=1.30e+02)
        axV.set_ylim(ymin=0.3, ymax=1.58)
        for axis in [axP, axR, axV]:
            axis.set_xlim(xmin=0.8, xmax=0.8*distance_max)
        
        for axis in [axP, axR, axV]:
            axis.axvline(cloud_com, axis.get_ylim()[0] if axis!=axV else 0., axis.get_ylim()[1], 
                         linestyle=":", color=colors[count], alpha=0.8)
            if axis != axV:
                axis.set_yscale('log')

        for axis in [axP, axR, axV]:
            axis.set_xlabel(r"distance [$d_{\rm ini}$]", fontsize=36)
        axP.set_ylabel(r"pressure [initial wind pressure $p_{\rm w, ini}$]", fontsize=36)
        axR.set_ylabel(r"density $\rho$ [initial wind density $\rho_{\rm w, ini}$]", fontsize=36)
        axV.set_ylabel(r"velocity [initial wind velocity]", fontsize=36)

        def set_phys_len(axis):
            x_tick_locs = axis.get_xticks()
            ax2 = axis.twiny()
    
            ax2.set_xlim(axis.get_xlim())
            ax2.set_xticks(x_tick_locs)
            ax2.set_xticklabels(tick_function(x_tick_locs))
            ax2.set_xlabel(r"distance [kpc]", fontsize=36)
            ax2.grid(False)
        for axis in [axP, axR, axV]:
            set_phys_len(axis)
        # axP.set_title("Pressure")
        count+=1

    print("Done!")
    fig.suptitle(r"Cloud profile for $t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}', fontsize=40)
    print(f"Saving {plot_filename}.{ext}")
    plt.savefig(f"{plot_filename}.{ext}")
