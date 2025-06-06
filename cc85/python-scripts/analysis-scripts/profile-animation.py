# -*- coding: utf-8 -*-
"""
Created on Sat Nov  23 10:50:48 2024

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
colors = ["yellowgreen", "steelblue", "darkorchid", "plum", "goldenrod", "crimson"]

'''
tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]
del tcool_mix_B_tcc[5]
del rini_B_rcl[5]
del tcool_mix_B_tcc[4]
del rini_B_rcl[4]
'''
tcool_mix_B_tcc = [0.08, 0.10, 0.20,]# 0.50, 0.80, 1.00, 1.40,]#  2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671,]# 176.677, 282.684, 353.355, 494.697,]# 883.387, 2826.838,]

tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]
del tcool_mix_B_tcc[0]
del rini_B_rcl[0]

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

Tmix = np.sqrt(chi)*Tcl
Tcutoff = 9.0e+04
Temperature_identify = 2.0*Tcl
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Temperature_identify: %.2e K"%Temperature_identify)

root = "../../output"
root_vanl = "../../output-vanl"
till = 100 # tcc
ext = "png"

# adapted from https://stackoverflow.com/questions/36505587/color-line-by-third-variable-python
def plot_colourline(x,y,c, min_val, max_val, label=None, axis=None, zorder=None):
    colormap = matplotlib.cm.nipy_spectral
    log_map = False
    if log_map:
        col = colormap((c-min_val)/(max_val-min_val))
    else:
        col = colormap((10.**c-10.**min_val)/(10.**max_val-10.**min_val))

    ax = plt.gca() if axis is None else axis
    for i in np.arange(len(x)-1):
        if zorder is None:
            ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=col[i], linestyle="-")
        else:
            ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=col[i], linestyle="-", zorder=zorder)
    im = ax.scatter(x, y, c=10.**c, s=0,
                    cmap=colormap, 
                    norm=matplotlib.colors.LogNorm(vmin=10.**min_val, vmax=10.**max_val) if \
                         log_map else \
                         matplotlib.colors.Normalize(vmin=10.**min_val, vmax=10.**max_val)
                    ) #, label=label)
    return im

# plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))
os.makedirs(f"profiles-anim", exist_ok = True)
print("density")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp)
    ndens_cl_ini = chi * ndens_w_ini # cgs
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs
    os.makedirs(f"profiles-anim/{label}", exist_ok = True)

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    distance_min, distance_max = None, None
    for key in list(cloud_data.keys()):
        # cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini

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

    mass_data = []
    for key in list(cloud_data.keys()):
        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs

        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        condition =  cloud_ndens > (10. * ndens_w)
        cloud_mass = np.sum(cloud_ndens[condition]*cloud_volume[condition])*(mu*mp)

        mass_data.append([float(key), cloud_mass, cloud_com])
        print(f"{label}: {int(key)}", end="\r")
        min_dist, max_dist = 0.8, 1.01*distance_max
    
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(28,10))
        line, = ax1.plot(cloud_distance, cloud_density, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True)
        ax1.plot([], [], color=line.get_color(), label=f"{key}")
        
        im = plot_colourline(np.array(mass_data)[:,0], np.array(mass_data)[:,1]/np.array(mass_data)[0,1], np.log10(np.array(mass_data)[:,2]), 
                            np.log10(min_dist), np.log10(10.7), # np.log10(max_dist),
                            label=f'{tcool_mix_B_tcc[select]:.2f}',
                            axis = ax2,
                            zorder = -int(50*(select+1)))
        
        if (int(key)>=10):
            # Calculate the bin width using the Freedman-Diaconis rule 
            q25, q75 = np.percentile(cloud_distance, [25, 75]) 
            iqr = q75 - q25 
            # Interquartile range 
            bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
            num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

            # Calculate the median y trend as a function of x 
            bin_means, bin_edges, _ = binned_statistic(cloud_distance, cloud_density, 
                                                       statistic='median', bins=num_bins) 
            # Plot the median y trend 
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
            # Calculate bin centers for plotting 
            ax1.plot(bin_centers, bin_means, color="sandybrown")

        '''
        if distance_min<0.5*diniBdinj:
            distance_min = 0.5*diniBdinj
        if distance_max<1.5*diniBdinj:
            distance_max = 1.5*diniBdinj
        '''    
        ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

        ax1.plot(distance_w, ndens_w/ndens_w_ini, linestyle="--", color="black" if not(dark) else "peachpuff", linewidth=2.0)
        ax1.plot(distance_w, prs_w/prs_w_ini*chi, linestyle=":", color="gray" if not(dark) else "beige", linewidth=2.0)
        ax1.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        contrast_highlight = 10.0
        ax1.plot(distance_w, contrast_highlight*ndens_w/ndens_w_ini, color="black" if not(dark) else "peachpuff", linestyle=(0, (5, 5)))
        # plt.hlines(contrast_highlight, xmin=0.8, xmax=1.01*distance_max, colors='black', linestyles=(0, (5, 5)))
        ax1.set_xlim(xmin=0.8, xmax=1.01*distance_max)
        ax1.set_ylim(ymin=3.1e-03, ymax=1.10e+02)
        # plt.xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel(r"Distance [$d_{\rm ini}$]")
        ax1.set_ylabel(r"Density [initial wind density]")
        fig.suptitle(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
        
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = plt.colorbar(im, cax=cax, pad=0.01, extend='max')
        cbar.set_label(r"$d_{\rm cl}/d_{\rm cl,ini}$") #, rotation=270)
        # print(dir(cbar.ax))
        cbar.ax.tick_params(direction="out", length=8, width=1.2, colors="black" if not(dark) else "white", which="major", right=True, zorder=10)
        cbar.ax.tick_params(direction="out", length=5, width=1.0, colors="black" if not(dark) else "white", which="minor", right=True, zorder=10)
        cbar.ax.update({"zorder": 100000,})
        
        ax2.set_ylim(ymin=0.2, ymax=3.0)
        ax2.set_xlim(xmin=0., xmax = till)
        ax2.set_yscale('log')
        ax2.set_xlabel(r"time [$t_{\rm cc,ini}$]")
        ax2.set_ylabel(r"$M_{\rm cold}$ ($T<8\times 10^4$ K, $\rho > 10 \rho _{\rm wind}$) [$M_{\rm cold, ini}$]")

        plt.savefig(f"profiles-anim/{label}/density{'-dark' if dark else ''}.{int(key):04d}.{ext}", transparent=False, bbox_inches="tight")
        # plt.show()
        plt.close()
    print(len(f"{label}: {int(key)}")*" ", end="\r")
    print(label)

print("pressure")
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

    for key in list(cloud_data.keys()):
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        print(f"{label}: {int(key)}", end="\r")
        plt.figure()
        line, = plt.plot(cloud_distance, cloud_pressure, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
        
        if (int(key)>=10):
            # Calculate the bin width using the Freedman-Diaconis rule 
            q25, q75 = np.percentile(cloud_distance, [25, 75]) 
            iqr = q75 - q25 
            # Interquartile range 
            bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
            num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

            # Calculate the median y trend as a function of x 
            bin_means, bin_edges, _ = binned_statistic(cloud_distance, cloud_pressure, 
                                                       statistic='median', bins=num_bins) 
            # Plot the median y trend 
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
            # Calculate bin centers for plotting 
            plt.plot(bin_centers, bin_means, color="sandybrown")

        '''
        if distance_min<0.5*diniBdinj:
            distance_min = 0.5*diniBdinj
        if distance_max<1.5*diniBdinj:
            distance_max = 1.5*diniBdinj
        '''    
        ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

        plt.plot(distance_w, prs_w/prs_w_ini, linestyle="--", color="black" if not(dark) else "peachpuff", linewidth=2.0)
        plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        plt.ylim(ymin=8.0e-05, ymax=6.0)
        plt.xlim(xmin=0.8, xmax=1.01*distance_max)
        # plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(r"Distance [$d_{\rm ini}$]")
        plt.ylabel(r"Pressure [initial wind pressure]")
        plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
        plt.savefig(f"profiles-anim/{label}/pressure{'-dark' if dark else ''}.{int(key):04d}.{ext}", transparent=False, bbox_inches="tight")
        # plt.show()
        plt.close()
    print(len(f"{label}: {int(key)}")*" ", end="\r")
    print(label)

print("velocity")
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

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    distance_min, distance_max = None, None
    for key in list(cloud_data.keys()):
        cloud_velocity  = np.sqrt(cloud_data[key]['cloud_velocity_r']**2 + cloud_data[key]['cloud_velocity_th']**2 + cloud_data[key]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        cloud_distance  = cloud_data[key]['cloud_distance']/distance_ini

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

    for key in list(cloud_data.keys()):
        cloud_velocity  = np.sqrt(cloud_data[key]['cloud_velocity_r']**2 + cloud_data[key]['cloud_velocity_th']**2 + cloud_data[key]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        cloud_distance  = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        print(f"{label}: {int(key)}", end="\r")
        plt.figure()
        line, = plt.plot(cloud_distance, cloud_velocity/v_w_ini, marker='.', markersize=0.5, 
                         linestyle='None', alpha=0.5, rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
        
        if (int(key)>=10):
            # Calculate the bin width using the Freedman-Diaconis rule 
            q25, q75 = np.percentile(cloud_distance, [25, 75]) 
            iqr = q75 - q25 
            # Interquartile range 
            bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
            num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

            # Calculate the median y trend as a function of x 
            bin_means, bin_edges, _ = binned_statistic(cloud_distance, cloud_velocity/v_w_ini, 
                                                       statistic='median', bins=num_bins) 
            # Plot the median y trend 
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
            # Calculate bin centers for plotting 
            plt.plot(bin_centers, bin_means, color="sandybrown")
        '''
        if distance_min<0.5*diniBdinj:
            distance_min = 0.5*diniBdinj
        if distance_max<1.5*diniBdinj:
            distance_max = 1.5*diniBdinj
        '''    
        v_w     = (CC85windvel(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000)*diniBdinj)/CC85windvel(diniBdinj)) * v_w_ini

        plt.plot(distance_w, v_w/v_w_ini, linestyle="--", color="black" if not(dark) else "peachpuff", linewidth=2.0)
        plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
                prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        plt.ylim(ymin=0.12, ymax=1.58)
        plt.xlim(xmin=0.8, xmax=1.01*distance_max)
        # plt.xscale('log')
        # plt.yscale('log')
        plt.xlabel(r"Distance [$d_{\rm ini}$]")
        plt.ylabel(r"Velocity [initial wind velocity]")
        plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
        plt.savefig(f"profiles-anim/{label}/velocity{'-dark' if dark else ''}.{int(key):04d}.{ext}", transparent=False, bbox_inches="tight")
        # plt.show()
        plt.close()
    print(len(f"{label}: {int(key)}")*" ", end="\r")
    print(label)
