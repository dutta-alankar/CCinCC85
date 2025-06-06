# -*- coding: utf-8 -*-
"""
Created on Mon Nov  22 12:42:48 2024

@author: alankar.
Usage: time python area-analysis.py
"""
import numpy as np
import scipy
import subprocess as sp
import seaborn as sns
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull
import hdbscan
import sys
import os
import pickle
import matplotlib
import matplotlib.pyplot as plt
from tueplots import cycler
from tueplots.constants import markers
from tueplots.constants.color import palettes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]
del tcool_mix_B_tcc[5]
del rini_B_rcl[5]
del tcool_mix_B_tcc[4]
del rini_B_rcl[4]

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
print(f"Tmix: {Tmix:.2e} K")
print(f"Tcutoff: {Tcutoff:.2e} K")
print(f"Temperature_identify: {Temperature_identify:.2e} K")

root = "../../output"
root_vanl = "../../output-vanl"
till = 100 # tcc

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    proj_area_data = []
    for key in list(cloud_data.keys()):
        cloud_pos_x = cloud_data[key]['cloud_pos_x']
        cloud_pos_y = cloud_data[key]['cloud_pos_y']
        cloud_pos_z = cloud_data[key]['cloud_pos_z']
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        proj_data = np.vstack( (cloud_pos_x, cloud_pos_y) ).T

        clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit( proj_data )
        proj_area = 0
        for group in set(clusterer.labels_):
            if group < 0:
                continue
            # print(proj_data[clusterer.labels_==group].shape)
            hull = ConvexHull( proj_data[clusterer.labels_==group] )
            proj_area += hull.volume
        proj_area_data.append([float(key),
                              proj_area,
                              cloud_com,
                              ])
        if float(key) < 5.0:
            hull = ConvexHull( proj_data )
            print(proj_area, hull.volume)
            if select == 0:
                plt.figure(figsize=(8,8))
                plt.plot(proj_data[:,0], proj_data[:,1], 'o')
                plt.plot(proj_data[hull.vertices,0], proj_data[hull.vertices,1], color='red')
                plt.gca().set_aspect('equal', 'box')
                plt.show()
                plt.close() 
                clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit( proj_data )
                plt.figure(figsize=(8,8))
                # plt.plot(proj_data[:,0], proj_data[:,1], 'o')
                color_palette = sns.color_palette('deep', int(np.max(np.array(set(clusterer.labels_)))))
                cluster_colors = [color_palette[x] if x >= 0
                                  else (0.5, 0.5, 0.5)
                                  for x in clusterer.labels_]
                cluster_member_colors = [sns.desaturate(x, p) for x, p in
                                         zip(cluster_colors, clusterer.probabilities_)]
                for group in set(clusterer.labels_):
                    if group < 0:
                        continue
                    print(proj_data[clusterer.labels_==group].shape)
                    hull = ConvexHull( proj_data[clusterer.labels_==group] )
                    plt.plot(proj_data[hull.vertices,0], proj_data[hull.vertices,1], color='red')
                plt.gca().set_aspect('equal', 'box')
                plt.show()
                plt.close() 
    proj_area_data = np.array(proj_area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 25
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100

    plt.plot(proj_area_data[:till+1,0], proj_area_data[:till+1,1]/proj_area_data[0,1], 
             label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=-int(50*(select+1)) )

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=2.0e-02) #, ymax=8.0e+03)
plt.xlim(xmin=0., xmax = till)
plt.yscale('log')
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"Projected area $A_{\rm proj, cold}$ ($T<8\times 10^4$ K) [$A_{\rm proj, cold, ini}$]")
plt.savefig(f"cloud-area_proj-trunc_time{'-dark' if dark else ''}.svg", transparent=False)
# plt.show()
plt.close()

till = 100
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    proj_area_data = []
    for key in list(cloud_data.keys()):
        cloud_pos_x = cloud_data[key]['cloud_pos_x']
        cloud_pos_y = cloud_data[key]['cloud_pos_y']
        cloud_pos_z = cloud_data[key]['cloud_pos_z']
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        hull = ConvexHull( np.vstack( (cloud_pos_x, cloud_pos_y) ).T )
        proj_area_data.append([float(key),
                              hull.volume,
                              cloud_com,
                              ])
    proj_area_data = np.array(proj_area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 25
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100

    plt.plot(proj_area_data[:till+1,2]/proj_area_data[0,2], proj_area_data[:till+1,1]/proj_area_data[0,1], 
             label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=-int(50*(select+1)) )

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=2.0e-01) #, ymax=8.0e+03)
plt.xlim(xmin=0.98, xmax=9.9)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"Distance [$d_{\rm ini}$]")
plt.ylabel(r"Projected area $A_{\rm proj, cold}$ ($T<8\times 10^4$ K) [$A_{\rm proj, cold, ini}$]")
plt.savefig(f"cloud-area_proj-trunc_distance{'-dark' if dark else ''}.svg", transparent=False)
# plt.show()
plt.close()
