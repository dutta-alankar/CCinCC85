# -*- coding: utf-8 -*-
"""
Created on Sat Nov  23 10:50:48 2024

@author: alankar.
Usage: time python 2d-pdfs_cloud.py
"""
import numpy as np
import scipy
import subprocess as sp
from scipy.interpolate import interp1d
from scipy.stats import binned_statistic
import sys
import os
import pickle
import h5py
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
from tueplots import cycler
from tueplots.constants import markers
from tueplots.constants.color import palettes
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

tcool_mix_B_tcc = [0.08, 0.10, 0.20,]# 0.50, 0.80, 1.00, 1.40,]#  2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671,]# 176.677, 282.684, 353.355, 494.697,]# 883.387, 2826.838,]

tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
rini_B_rcl = rini_B_rcl[1:]
del tcool_mix_B_tcc[0]
del rini_B_rcl[0]
'''
del tcool_mix_B_tcc[5]
del rini_B_rcl[5]
del tcool_mix_B_tcc[4]
del rini_B_rcl[4]
'''
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
Twind_ini = chi*Tcl
print("Tmix: %.2e K"%Tmix)
print("Tcutoff: %.2e K"%Tcutoff)
print("Temperature_identify: %.2e K"%Temperature_identify)

root = "../../output"
root_vanl = "../../output-vanl"
till = 100 # tcc
ext = "png"

def fd_bins(arr):
    # Calculate the bin width using the Freedman-Diaconis rule 
    q25, q75 = np.percentile(arr, [25, 75]) 
    iqr = q75 - q25 
    # Interquartile range 
    bin_width = 2 * iqr * len(arr) ** (-1./3) 
    num_bins = int((arr.max() - arr.min()) / bin_width)
    return num_bins

# plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))
os.makedirs(f"profiles-anim", exist_ok = True)
make_anim = True # XXX: set this to false to get the plots in paper

def make_wind_contours(file_no, ax):
    if not(make_anim):
        axins = inset_axes(ax, width="100%", height="100%", bbox_to_anchor=(.64, .14, .36, .36),
                           bbox_transform=ax.transAxes)
    else:
        axins = inset_axes(ax, width="100%", height="100%", bbox_to_anchor=(.18, .52, .36, .36),
                           bbox_transform=ax.transAxes)
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
    with h5py.File(f"{directory}/data.{file_no:04d}.flt.h5", "r") as hdf:
        gas_density  = np.array(hdf[f"/Timestep_{file_no}/vars/density"]).flatten() * UNIT_DENSITY/(mu*mp)/ndens_w_ini
        gas_pressure = np.array(hdf[f"/Timestep_{file_no}/vars/pressure"]).flatten()* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        gas_temperature = np.array(hdf[f"/Timestep_{file_no}/vars/temperature"]).flatten() # K
        gas_volume = np.array(hdf[f"/Timestep_{file_no}/vars/cellvol"]).flatten() # code units
        wind_temperature = gas_temperature/(1+np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten())
        wind_density = gas_density/(1+np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten())
        condition = np.logical_and(wind_temperature>Tcutoff, gas_temperature<=(2*Tcl))
        delP_Pwind = np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten() + np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten() + \
                     np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten() * np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten() 
        hist_nbins  = np.min([fd_bins(delP_Pwind[condition]), 128])
        hist, bin_edges = np.histogram(delP_Pwind[condition], bins=hist_nbins, density=True, 
                                       weights=(gas_density[condition]*gas_volume[condition]))
        axins.plot(np.hstack([bin_edges[0], 0.5*(bin_edges[1:]+bin_edges[:-1]), bin_edges[-1]]) , np.hstack([0,hist,0]) )
        axins.set_yscale("log")
        # axins.set_xlabel(r"$\frac{\Delta p}{p_{\rm wind}}$", fontsize=35)
        axins.set_xlabel(r"$\Delta \mathcal{P}$", fontsize=30)
        # axins.set_ylabel(r"$\frac{1}{M_0} \frac{dM}{d(\Delta p/p_{\rm wind})}$", fontsize=20)
        axins.set_ylabel(r"PDF", fontsize=30)
        axins.tick_params(axis='both', which='major', labelsize=16)
        axins.tick_params(axis='both', which='minor', labelsize=14)
        '''
        density_nbins  = np.min([fd_bins(gas_density[condition]), 128])
        pressure_nbins = np.min([fd_bins(gas_pressure[condition]), 128])
        # print("debug: ", (density_nbins,pressure_nbins))
        hist, x_edges, y_edges = np.histogram2d(np.log10(gas_density[condition]), np.log10(gas_pressure[condition]), 
                                                bins=(density_nbins,pressure_nbins), density=True,
                                                weights=(gas_density[condition]*gas_volume[condition]))
        hist = hist.T
        '''
        '''
        X, Y = np.meshgrid(0.5*(x_edges[1:]+x_edges[:-1]), 0.5*(y_edges[1:]+y_edges[:-1]))
        ax.contour(X, Y, hist)
        '''
        '''
        X, Y = np.meshgrid(x_edges, y_edges)
        pc = axins.pcolormesh(X, Y, hist, 
                              norm=matplotlib.colors.LogNorm(vmin=5.0e-02, vmax=5.0e+00),
                              cmap="viridis", rasterized=True)
        '''

def make_wind_panels(file_no, ax):
    if not(make_anim):
        axins = inset_axes(ax, width="100%", height="100%", bbox_to_anchor=(.64, .14, .36, .36),
                           bbox_transform=ax.transAxes)
    else:
        axins = inset_axes(ax, width="100%", height="100%", bbox_to_anchor=(.18, .52, .36, .36),
                           bbox_transform=ax.transAxes)
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
    with h5py.File(f"{directory}/data.{file_no:04d}.flt.h5", "r") as hdf:
        gas_density  = np.array(hdf[f"/Timestep_{file_no}/vars/density"]).flatten() * UNIT_DENSITY/(mu*mp)/ndens_w_ini
        gas_pressure = np.array(hdf[f"/Timestep_{file_no}/vars/pressure"]).flatten()* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        gas_temperature = np.array(hdf[f"/Timestep_{file_no}/vars/temperature"]).flatten() # K
        gas_volume = np.array(hdf[f"/Timestep_{file_no}/vars/cellvol"]).flatten() # code units
        wind_temperature = gas_temperature/(1+np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten())
        wind_density = gas_density/(1+np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten())
        condition = np.logical_and(wind_temperature>Tcutoff, gas_temperature<=(2*Tcl))
        delP_Pwind = np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten() + np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten() + \
                     np.array(hdf[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten() * np.array(hdf[f"/Timestep_{file_no}/vars/delTbyTwind"]).flatten() 
        hist_nbins  = np.min([fd_bins(delP_Pwind[condition]), 128])
        hist, bin_edges = np.histogram(delP_Pwind[condition], bins=hist_nbins, density=True, 
                                       weights=(gas_density[condition]*gas_volume[condition]))
        axins.plot(np.hstack([bin_edges[0], 0.5*(bin_edges[1:]+bin_edges[:-1]), bin_edges[-1]]) , np.hstack([0,hist,0]) )
        axins.set_yscale("log")
        # axins.set_xlabel(r"$\frac{\Delta p}{p_{\rm wind}}$", fontsize=35)
        axins.set_xlabel(r"$\Delta \mathcal{P}$", fontsize=30)
        # axins.set_ylabel(r"$\frac{1}{M_0} \frac{dM}{d(\Delta p/p_{\rm wind})}$", fontsize=20)
        axins.set_ylabel(r"PDF", fontsize=30)
        axins.tick_params(axis='both', which='major', labelsize=16)
        axins.tick_params(axis='both', which='minor', labelsize=14)
        '''
        density_nbins  = np.min([fd_bins(gas_density[condition]), 128])
        pressure_nbins = np.min([fd_bins(gas_pressure[condition]), 128])
        # print("debug: ", (density_nbins,pressure_nbins))
        hist, x_edges, y_edges = np.histogram2d(np.log10(gas_density[condition]), np.log10(gas_pressure[condition]), 
                                                bins=(density_nbins,pressure_nbins), density=True,
                                                weights=(gas_density[condition]*gas_volume[condition]))
        hist = hist.T
        '''
        '''
        X, Y = np.meshgrid(0.5*(x_edges[1:]+x_edges[:-1]), 0.5*(y_edges[1:]+y_edges[:-1]))
        ax.contour(X, Y, hist)
        '''
        '''
        X, Y = np.meshgrid(x_edges, y_edges)
        pc = axins.pcolormesh(X, Y, hist, 
                              norm=matplotlib.colors.LogNorm(vmin=5.0e-02, vmax=5.0e+00),
                              cmap="viridis", rasterized=True)
        '''

print("density-pressure")
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
    os.makedirs(f"profiles-anim/{label}/hist2d", exist_ok = True)

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    density_min, density_max = None, None
    pressure_min, pressure_max = None, None
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
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
            density_min = np.min(cloud_density)
            density_max = np.max(cloud_density)
            pressure_min = np.min(cloud_pressure)
            pressure_max = np.max(cloud_pressure)
        else:
            density_min = density_min if (_tmp:=np.min(cloud_density))>density_min else _tmp
            density_max = density_max if (_tmp:=np.max(cloud_density))<density_max else _tmp
            pressure_min = density_min if (_tmp:=np.min(cloud_pressure))>density_min else _tmp
            pressure_max = density_max if (_tmp:=np.max(cloud_pressure))<density_max else _tmp
        count += 1

    for key in list(cloud_data.keys()):
        if int(key) not in [10, 20, 40, 50] and not(make_anim): continue
        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        print(f"{label}: {int(key)}", end="\r")
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
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
        
        pcl_pred = (pwind_com/kB)/prs_w_ini
        ndens_cl_pred = (pwind_com/(kB*Tcl))/ndens_w_ini

        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        contrast = False
        if contrast:
            contrast_highlight = 10.0
            condition =  cloud_ndens > (contrast_highlight * ndens_w)
            cloud_density  = cloud_density[condition]
            cloud_pressure  = cloud_pressure[condition]
        
        density_nbins  = fd_bins(cloud_density)
        pressure_nbins = fd_bins(cloud_pressure)
        
        hist, x_edges, y_edges = np.histogram2d(np.log10(cloud_density), np.log10(cloud_pressure), 
                                                bins=(density_nbins,pressure_nbins), density=True,
                                                weights=(cloud_density*cloud_volume))
        hist = hist.T

        fig = plt.figure(figsize=(13,10))
        ax  = plt.gca()
        X, Y = np.meshgrid(x_edges, y_edges)
        pc = ax.pcolormesh(X, Y, hist, 
                           norm=matplotlib.colors.LogNorm(vmin=5.0e-02, vmax=5.0e+00),
                           cmap="viridis", rasterized=True)
        '''
        im = NonUniformImage(ax, interpolation='bilinear', cmap="viridis")
        x_centers = (x_edges[:-1] + x_edges[1:]) / 2
        y_centers = (y_edges[:-1] + y_edges[1:]) / 2
        im.set_data(x_centers, y_centers, hist)
        ax.add_image(im)
        '''
        cbar = plt.colorbar(pc, extend="both", pad=0.02) #, norm=matplotlib.colors.LogNorm(vmin=hist.min(), vmax=hist.max()))
        cbar.ax.tick_params(axis="y", which="major", direction="in", color='tab:red') #, width=16, length=20, zorder=111)
        cbar.ax.tick_params(axis="y", which="minor", direction="in", color='tab:red') #, width=12, length=18, zorder=111)
        cbar.ax.set_axisbelow(False)
        
        # Calculate the bin width using the Freedman-Diaconis rule 
        q25, q75 = np.percentile(cloud_distance, [25, 75]) 
        iqr = q75 - q25 
        # Interquartile range 
        bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
        num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

        # Calculate the median y trend as a function of x 
        bin_means, bin_edges, _ = binned_statistic(cloud_distance, np.log10(cloud_density), 
                                                   statistic='median', bins=num_bins) 
        # Calculate bin centers for plotting 
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
        
        ndens_cl_pred = 10.**bin_means[np.argmin(np.abs(bin_centers-cloud_com))]
        
        # Calculate the bin width using the Freedman-Diaconis rule 
        q25, q75 = np.percentile(cloud_distance, [25, 75]) 
        iqr = q75 - q25 
        # Interquartile range 
        bin_width = 2 * iqr * len(cloud_distance) ** (-1./3) 
        num_bins = int((cloud_distance.max() - cloud_distance.min()) / bin_width)

        # Calculate the median y trend as a function of x 
        bin_means, bin_edges, _ = binned_statistic(cloud_distance, np.log10(cloud_pressure), 
                                                   statistic='median', bins=num_bins) 
        # Calculate bin centers for plotting 
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.
        
        pcl_pred = 10.**bin_means[np.argmin(np.abs(bin_centers-cloud_com))]

        # ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        # prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini
        
        x = np.linspace(np.log10(density_min), np.log10(density_max), 100)
        plt.plot(x, x + np.log10(Temperature_identify/Twind_ini), linestyle=":", label=r"$2T_{\rm cl}$", alpha=0.6,
                                 color = "gray" if not(dark) else "white")
        plt.plot(x, x + np.log10(Tcl/Twind_ini), linestyle="--", label=r"$T_{\rm cl}$", alpha=0.9,
                                 color = "gray" if not(dark) else "white")
        plt.legend(loc="upper right", ncols=1,
                   prop = { "size": 32 }, title_fontsize=34, fancybox=True)
        
        plt.scatter(np.log10(chi), np.log10(1), s=270, color="tab:orange", marker="D", alpha=0.9, zorder=150)

        ax.set_xlim(xmin=np.log10(density_min), xmax=np.log10(density_max))
        ax.set_ylim(ymin=np.log10(pressure_min), ymax=np.log10(pressure_max))
        if int(key) in [10, 20, 40, 50] and not(make_anim):
            make_wind_contours(int(key), plt.gca())
        elif int(key)!=0:
            make_wind_panels(int(key), plt.gca())
        if not(make_anim):
            if (tcool_mix_B_tcc[select]==0.2 and int(key)==40):
                ax.set_xlim(xmin=-1.9, xmax=0.1)
                ax.set_ylim(ymin=-3.8, ymax=-1.9)
            if (tcool_mix_B_tcc[select]==0.2 and int(key)==10):
                ax.set_xlim(xmin=0.3, xmax=2.2)
                ax.set_ylim(ymin=-1.6, ymax=0.4)
            if (tcool_mix_B_tcc[select]==0.2 and int(key)==20):
                ax.set_xlim(xmin=-0.8, xmax=1.4)
                ax.set_ylim(ymin=-2.6, ymax=-0.8)
            if (tcool_mix_B_tcc[select]==0.2 and int(key)==50):
                ax.set_xlim(xmin=np.log10(density_min), xmax=-0.4)
                ax.set_ylim(ymin=np.log10(pressure_min), ymax=-2.4)
        # ax.set_yscale('log')
        # ax.set_xscale('log')
        
        # plt.axvline(np.log10(ndens_cl_pred), np.log10(pressure_min), np.log10(pressure_max), linestyle=":", color="tab:orange", alpha=0.8)
        # plt.axhline(np.log10(pcl_pred), np.log10(density_min), np.log10(density_max), linestyle=":", color="tab:orange", alpha=0.8)
        ax.scatter(np.log10(ndens_cl_pred), np.log10(pcl_pred), s=270, color="tab:red", marker="X", alpha=0.9, zorder=150)
        
        ax.text(ax.get_xlim()[0] + 0.08*(ax.get_xlim()[1]-ax.get_xlim()[0]),
                ax.get_ylim()[1] - 0.08*(ax.get_ylim()[1]-ax.get_ylim()[0]),
                r"$t/t_{\rm cc,ini}$ = "+f'{key}')
        
        ax.set_xlabel(r"$\log _{\rm 10}($density [initial wind density]$)$")
        ax.set_ylabel(r"$\log _{\rm 10}($pressure [initial wind pressure]$)$")
        fig.suptitle(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}', x=0.45)

        plt.savefig(f"profiles-anim/{label}/hist2d/density-pressure{'-dark' if dark else ''}.{int(key):04d}.{ext}", transparent=False, bbox_inches="tight")
        # plt.show()
        plt.close()
    print(len(f"{label}: {int(key)}")*" ", end="\r")
    print(label)
'''
print("temperature-velocity")
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
    os.makedirs(f"profiles-anim/{label}/hist2d", exist_ok = True)

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    temperature_min, temperature_max = None, None
    velocity_min, velocity_max = None, None
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_volume   = cloud_data[key]['cloud_volume_elems']
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_velocity  = cloud_data[key]['cloud_velocity_r']* UNIT_VELOCITY
        cloud_temperature  = cloud_data[key]['cloud_temperature']/1.0e+04
        v_w_ini = UNIT_VELOCITY # cgs
        cloud_velocity = cloud_velocity/v_w_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        if count==0:
            temperature_min = np.min(cloud_temperature)
            temperature_max = np.max(cloud_temperature)
            velocity_min = np.min(cloud_velocity)
            velocity_max = np.max(cloud_velocity)
        else:
            temperature_min = temperature_min if (_tmp:=np.min(cloud_temperature))>temperature_min else _tmp
            temperature_max = temperature_max if (_tmp:=np.max(cloud_temperature))<temperature_max else _tmp
            velocity_min = velocity_min if (_tmp:=np.min(cloud_velocity))>velocity_min else _tmp
            velocity_max = velocity_max if (_tmp:=np.max(cloud_velocity))<velocity_max else _tmp
        count += 1

    for key in list(cloud_data.keys()):
        if tcool_mix_B_tcc[select]==0.1:
            till = 25
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 80
        if float(key)>till:
            continue

        print(f"{label}: {int(key)}", end="\r")
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        cloud_volume   = cloud_data[key]['cloud_volume_elems']
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_velocity  = cloud_data[key]['cloud_velocity_r']* UNIT_VELOCITY
        cloud_temperature  = cloud_data[key]['cloud_temperature']/1.0e+04
        v_w_ini = UNIT_VELOCITY # cgs
        cloud_velocity = cloud_velocity/v_w_ini

        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        contrast = False
        if contrast:
            contrast_highlight = 10.0
            condition =  cloud_ndens > (contrast_highlight * ndens_w)
            cloud_density  = cloud_density[condition]
            cloud_pressure  = cloud_pressure[condition]
        
        try:
            velocity_nbins  = fd_bins(cloud_velocity) if int(key)>0 else 50
            temperature_nbins = fd_bins(cloud_temperature) if int(key)>0 else 50
        except:
            velocity_nbins  = 100
            temperature_nbins = 100
            
        hist, x_edges, y_edges = np.histogram2d(cloud_velocity, cloud_temperature, 
                                                weights=np.log10(cloud_density*cloud_volume),
                                                bins=(velocity_nbins,temperature_nbins), density=True)
        hist = hist.T

        fig = plt.figure(figsize=(13,10))
        ax  = plt.gca()
        X, Y = np.meshgrid(x_edges, y_edges)
        pc = ax.pcolormesh(X, Y, hist, 
                           norm=matplotlib.colors.LogNorm(vmin=1.0e-01, vmax=5.0e+00),
                           cmap="viridis", rasterized=True)
        \'\'\'
        im = NonUniformImage(ax, interpolation='bilinear', cmap="viridis")
        x_centers = (x_edges[:-1] + x_edges[1:]) / 2
        y_centers = (y_edges[:-1] + y_edges[1:]) / 2
        im.set_data(x_centers, y_centers, hist)
        ax.add_image(im)
        \'\'\'
        plt.colorbar(pc) #, norm=matplotlib.colors.LogNorm(vmin=hist.min(), vmax=hist.max()))

        # ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        # prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

        ax.set_xlim(xmin=velocity_min, xmax=velocity_max)
        ax.set_ylim(ymin=temperature_min, ymax=temperature_max)
        # ax.set_yscale('log')
        # ax.set_xscale('log')
        ax.set_xlabel(r"velocity [initial wind velocity]")
        ax.set_ylabel(r"temperature $\times 10^4$ [K]")
        fig.suptitle(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')

        plt.savefig(f"profiles-anim/{label}/hist2d/velocity-temperature{'-dark' if dark else ''}.{int(key):04d}.{ext}", transparent=False, bbox_inches="tight")
        # plt.show()
        plt.close()
    print(len(f"{label}: {int(key)}")*" ", end="\r")
    print(label)
'''
