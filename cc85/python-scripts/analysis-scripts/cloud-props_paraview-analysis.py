# -*- coding: utf-8 -*-
"""
Created on Mon Oct  28 17:39:48 2024

@author: alankar.
Usage: time python area-analysis.py
"""
import numpy as np
import scipy
import subprocess as sp
from scipy.interpolate import interp1d
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
'''
del tcool_mix_B_tcc[5]
del rini_B_rcl[5]
del tcool_mix_B_tcc[4]
del rini_B_rcl[4]
'''
print(tcool_mix_B_tcc)

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

print("area-time")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Area
    area_data = []
    for key in list(cloud_data.keys()):
        area_data.append([float(key), cloud_data[key]['cloud_tot_surface_area']])
    area_data = np.array(area_data)

    line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))
    # plt.plot(area_data[:till+1,0], (area_data[:till+1,2]/area_data[0,2])**0.845, linestyle ='--', color = line.get_color())


plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0., xmax = till)
plt.yscale('log')
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"Surface area $A_{\rm cl}$ ($T<8\times 10^4$ K) [$A_{\rm cl, ini}$]")
plt.savefig(f"area-cold-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")

"""
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
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        condition =  cloud_ndens > (10. * ndens_w)
        cloud_mass = np.sum(cloud_ndens[condition]*cloud_volume[condition])*(mu*mp)
        mass_data.append([float(key), cloud_mass, cloud_com])
    mass_data = np.array(mass_data)

    line, = plt.plot(mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(mass_data[:till+1,0], (mass_data[:till+1,2]/mass_data[0,2])**0.845, linestyle ='--', color = line.get_color())

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0., xmax = till)
plt.yscale('log')
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"$M_{\rm cl}$ ($T<8\times 10^4$ K, $\rho > 10 \rho _{\rm wind}$) [$M_{\rm cl, ini}$]")
plt.savefig(f"mass-cold+dense-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()


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
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        condition =  cloud_ndens > (10. * ndens_w)
        cloud_mass = np.sum(cloud_ndens[condition]*cloud_volume[condition])*(mu*mp)
        mass_data.append([float(key), cloud_mass, cloud_com])
    mass_data = np.array(mass_data)

    line, = plt.plot(mass_data[:till+1,2], 
                     np.gradient(mass_data[:till+1,1]/mass_data[0,1], mass_data[:till+1,0]), 
                     label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(mass_data[:till+1,0], (mass_data[:till+1,2]/mass_data[0,2])**0.845, linestyle ='--', color = line.get_color())

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
# plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0.98, xmax=11.2)
plt.yscale('symlog', linthresh=0.01)
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"$\dot{M}_{\rm cl}$ ($T<8\times 10^4$ K, $\rho > 10 \rho _{\rm wind}$) [$M_{\rm cl, ini}$]")
plt.savefig(f"mass_dot-cold+dense-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    directory_vanl = f"{root_vanl}-{label}"
    analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp) # cgs
    ndens_cl_ini = chi * ndens_w_ini
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        cloud_mass = np.sum(cloud_ndens*cloud_volume)*(mu*mp)
        mass_data.append([float(key), cloud_mass, cloud_com])
    mass_data = np.array(mass_data)

    line, = plt.plot(mass_data[:till+1,2], 
                     np.gradient(mass_data[:till+1,1]/mass_data[0,1], mass_data[:till+1,0]), 
                     label=f'{tcool_mix_B_tcc[select]:.2f}')
    plt.plot(analysis_file_vanl[:,1][::int(tcc)]/distance_ini, 
             np.gradient(analysis_file_vanl[:,6][::int(tcc)], analysis_file_vanl[:,0][::int(tcc)]/tcc), 
             color=line.get_color(), 
             linestyle=(0, (5, 5)), 
             linewidth=1.5, alpha=1.0,
             zorder=-int(50*(select+1)))

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
# plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0.98, xmax=11.2)
plt.yscale('symlog', linthresh=0.01)
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"$\dot{M}_{\rm cl}$ ($T<8\times 10^4$ K) [$M_{\rm cl, ini}$]")
plt.savefig(f"mass_dot-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()


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
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        condition =  cloud_ndens > (10. * ndens_w)
        cloud_mass = np.sum(cloud_ndens[condition]*cloud_volume[condition])*(mu*mp)
        mass_data.append([float(key), cloud_mass, cloud_com])
    mass_data = np.array(mass_data)

    line, = plt.plot(mass_data[:till+1,0], 
                     np.gradient(mass_data[:till+1,1]/mass_data[0,1], mass_data[:till+1,0]), 
                     label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(mass_data[:till+1,0], (mass_data[:till+1,2]/mass_data[0,2])**0.845, linestyle ='--', color = line.get_color())

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
# plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0., xmax = till)
plt.yscale('symlog', linthresh=0.01)
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"$\dot{M}_{\rm cl}$ ($T<8\times 10^4$ K, $\rho > 10 \rho _{\rm wind}$) [$M_{\rm cl,ini}/t_{\rm cc,ini}$]")
plt.savefig(f"mass_dot-cold+dense-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
"""

print("cold and dense gas")

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

ax = None
fig = None
sub_ax = None
lines = None
make_inset = False

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
    if tcool_mix_B_tcc[select]==1.4 or tcool_mix_B_tcc[select]==1.0:
        continue
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini
        ndens_w   = (CC85windrho(cloud_distance * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
        cloud_ndens = cloud_data[key]['cloud_density'] * UNIT_DENSITY/(mu*mp) # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs
        cloud_com = np.sum(cloud_ndens*cloud_volume*cloud_distance)/np.sum(cloud_ndens*cloud_volume)

        condition =  cloud_ndens > (10. * ndens_w)
        cloud_mass = np.sum(cloud_ndens[condition]*cloud_volume[condition])*(mu*mp)
        mass_data.append([float(key), cloud_mass, cloud_com])
    mass_data = np.array(mass_data)

    min_dist, max_dist = 0.8, 10.7
    im = plot_colourline(mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1], np.log10(mass_data[:till+1,2]), 
                         np.log10(min_dist), np.log10(max_dist),
                         label=f'{tcool_mix_B_tcc[select]:.2f}',
                         axis = ax,
                         zorder = -int(50*(select+1)))
    if ax is None:
        ax = plt.gca()
    if fig is None:
        fig = plt.gcf()
    if sub_ax is None and make_inset:
        sub_ax = inset_axes(
        parent_axes=ax,
        loc='upper left',
        width=0.20*fig.get_size_inches()[0],
        height=0.18*fig.get_size_inches()[1],
        bbox_to_anchor=(0.03, 1.15),
        bbox_transform=ax.transAxes,
        borderpad=1  # padding between parent and inset axes
        )
    if make_inset:
        line = sub_ax.plot(mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1], linewidth=2,
                           label=f'{tcool_mix_B_tcc[select]:.2f}',
                           zorder=-int(50*(select+1)) )
        if lines is None:
            lines = line
        else:
            lines += line
    else:
        position_ann = { 0.1: (32.0, 0.428), 0.2: (52.5, 0.247), 0.5: (78.0, 0.473), 0.8: (52.0, 6.035), 2.5: (81.9, 3.031), 8.0: (7.1, 0.328) }
        for line_text in list(position_ann.keys()):
            if line_text!=tcool_mix_B_tcc[select]:
                continue
            text_pos = position_ann[line_text]
            # print(text_pos)
            ax.annotate(f'{tcool_mix_B_tcc[select]:.1f}',
                xy=text_pos, xycoords='data',
                # xytext=(-10, 90), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='center', verticalalignment='bottom')
        
    # plt.plot(mass_data[:till+1,0], (mass_data[:till+1,2]/mass_data[0,2])**0.845, linestyle ='--', color = line.get_color())

ax.annotate(r'$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini} = $',
                xy=(32.0, 6.035), xycoords='data',
                # xytext=(-10, 90), textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='center', verticalalignment='bottom')
cbar = fig.colorbar(im, pad=0.01, extend='max')
cbar.set_label(r"$d_{\rm cl}/d_{\rm cl,ini}$") #, rotation=270)
# print(dir(cbar.ax))
cbar.ax.tick_params(direction="out", length=8, width=1.2, colors="k", which="major", right=True, zorder=10)
cbar.ax.tick_params(direction="out", length=5, width=1.0, colors="k", which="minor", right=True, zorder=10)
cbar.ax.update({"zorder": 100000,})

if make_inset:
    line_labels = [l.get_label() for l in lines]
    ax.legend(lines, line_labels, loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
              prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    sub_ax.set_ylim(ymin=2.0e-01)
    sub_ax.set_xlim(xmin=0., xmax = till)
    sub_ax.set_yscale('log')
    sub_ax.tick_params(axis='both', labelsize=13)

ax.set_ylim(ymin=2.0e-01)
ax.set_xlim(xmin=0., xmax = till)
ax.set_yscale('log')
ax.set_xlabel(r"time [$t_{\rm cc,ini}$]")
ax.set_ylabel(r"$M_{\rm cl}$ ($T<8\times 10^4$ K, $\rho > 10 \rho _{\rm wind}$) [$M_{\rm cl, ini}$]")
plt.savefig(f"mass-cold+dense-w_dist-trunc_time{'-dark' if dark else ''}.svg", transparent=True, bbox_inches="tight")
# plt.show()
plt.close()
print("Done!")

"""
print("Absolute mass")
fig = plt.figure(figsize=(28,10))
axs = fig.subplots(1,2)

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory_vanl = f"{root_vanl}-{label}"
    directory = f"{root}-{label}"
    # print(label)
    analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory_vanl}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory_vanl}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory_vanl}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    # print(UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY)
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    # print(UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY)
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp) # cgs
    ndens_cl_ini = chi * ndens_w_ini
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs

    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_density = cloud_data[key]['cloud_density']
        cloud_volume = cloud_data[key]['cloud_volume_elems']

        cloud_mass = np.sum(cloud_density * cloud_volume)
        mass_data.append([float(key), cloud_mass])
    mass_data = np.array(mass_data)
    mass_data[:,1] = mass_data[:,1]*UNIT_DENSITY*UNIT_LENGTH**3/MSun
    tcc_to_Myr = tcc*(UNIT_LENGTH/UNIT_VELOCITY)/Myr

    mcl_ini = (4*np.pi/3.)*chi*UNIT_DENSITY*UNIT_LENGTH**3/MSun
    # print(mass_data[0,1], mcl_ini, analysis_file_vanl[0,6]*mcl_ini)
    # donot normalize by mass_data[0,1]
    line, = axs[0].plot(mass_data[:till+1,0]*tcc_to_Myr, 
                     mass_data[:till+1,1], label=f'{tcool_mix_B_tcc[select]:.2f}, {(UNIT_LENGTH/pc):.2f}')
    axs[0].plot(analysis_file_vanl[:,0]/tcc*tcc_to_Myr, 
             analysis_file_vanl[:,6]*mcl_ini, color=line.get_color(), 
             linestyle=(0, (5, 5)), linewidth=1.5, alpha=1.0)
    np.savetxt(f"./paraview-cloud-analysis_data-dump/{label}.cold-mass-time.txt", np.vstack( [mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1]] ).T)
    # plt.plot(mass_data[:till+1,0], (mass_data[:till+1,2]/mass_data[0,2])**0.845, linestyle ='--', color = line.get_color())

axs[0].legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$, $R_{\rm cl}$ [pc]", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
axs[0].set_ylim(ymin=2.0e-06) #, ymax=8.0e+03)
axs[0].set_xlim(xmin=0, xmax = 6.0)
axs[0].set_yscale('log')
axs[0].set_xlabel(r"time [Myr]")
axs[0].set_ylabel(r"$M_{\rm cl}$ ($T<8\times 10^4$ K) [$M_{\odot}$]")
# plt.savefig(f"mass-cold_to_CGM-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
# plt.close()

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    directory_vanl = f"{root_vanl}-{label}"
    analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp) # cgs
    ndens_cl_ini = chi * ndens_w_ini
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs

    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_density = cloud_data[key]['cloud_density'] * UNIT_DENSITY # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs

        cloud_mass = np.sum(cloud_density * cloud_volume)/MSun
        mass_data.append([float(key), cloud_mass])
    mass_data = np.array(mass_data)

    # normalize by mass_data[0,1]
    line, = axs[1].plot(mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1], 
                     label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=-int(50*(select+1)))
    axs[1].plot(analysis_file_vanl[:,0]/tcc, 
             analysis_file_vanl[:,6], color=line.get_color(), 
             linestyle=(0, (5, 5)), linewidth=1.5, alpha=1.0)
    np.savetxt(f"mass-cold-trunc_time-{label}.txt", np.vstack( [ mass_data[:till+1,0], mass_data[:till+1,1]/mass_data[0,1] ]).T)

axs[1].legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
axs[1].set_ylim(ymin=5.0e-02)
axs[1].set_xlim(xmin=0., xmax = till)
axs[1].set_yscale('log')
axs[1].set_xlabel(r"time [$t_{\rm cc,ini}$]")
axs[1].set_ylabel(r"$M_{\rm cl}$ ($T<8\times 10^4$ K) [$M_{\rm cl,ini}$]")
plt.savefig(f"mass-cold-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    directory_vanl = f"{root_vanl}-{label}"
    analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
    ndens_w_ini  = UNIT_DENSITY/(mu*mp) # cgs
    ndens_cl_ini = chi * ndens_w_ini
    prs_w_ini = ndens_w_ini*chi*Tcl # p/kB
    v_w_ini = UNIT_VELOCITY # cgs

    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    mass_data = []
    for key in list(cloud_data.keys()):
        cloud_density = cloud_data[key]['cloud_density'] * UNIT_DENSITY # cgs
        cloud_volume = cloud_data[key]['cloud_volume_elems'] * UNIT_LENGTH**3 # cgs

        cloud_mass = np.sum(cloud_density * cloud_volume)/MSun
        mass_data.append([float(key), cloud_mass])
    mass_data = np.array(mass_data)

    # normalize by mass_data[0,1]
    line, = plt.plot(mass_data[:till+1,0], 
                     np.gradient(mass_data[:till+1,1]/mass_data[0,1], mass_data[:till+1,0]), 
                     label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=-int(50*(select+1)))
    plt.plot(analysis_file_vanl[:,0][::int(tcc)]/tcc, 
             np.gradient(analysis_file_vanl[:,6][::int(tcc)], analysis_file_vanl[:,0][::int(tcc)]/tcc), 
             color=line.get_color(), 
             linestyle=(0, (5, 5)), 
             linewidth=1.5, alpha=1.0,
             zorder=-int(50*(select+1)))

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
# plt.ylim(ymin=5.0e-02)
plt.xlim(xmin=0., xmax = till)
plt.yscale('symlog', linthresh=0.01)
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"$\dot{M}_{\rm cl}$ ($T<8\times 10^4$ K) [$M_{\rm cl,ini}/t_{\rm cc,ini}$]")
plt.savefig(f"mass_dot-cold-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
"""

print("area-volume")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Area          Volume
    
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        wind_vel = CC85windvel(cloud_com/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
        delta_v = (wind_vel - cloud_velocity_r)/wind_vel 
        area_data.append([float(key), 
                          cloud_data[key]['cloud_tot_surface_area'], 
                          cloud_data[key]['cloud_tot_vol'],
                          cloud_data[key]['cloud_tot_mass'],
                          delta_v,
                          ])
    area_data = np.array(area_data)
    
    line, = plt.plot(area_data[:till+1,2]/area_data[0,2], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))

    where = interp1d(area_data[:till+1,4], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(0.2)
    if where<=np.max(area_data[:till+1,2]/area_data[0,2]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,2]/area_data[0,2], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(where), 
                    s=180, marker="*", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("vel", tcool_mix_B_tcc[select], where)
    
    where = interp1d(area_data[:till+1,3]/area_data[0,3], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(2)
    if where<=np.max(area_data[:till+1,2]/area_data[0,2]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,2]/area_data[0,2], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(where), 
                    s=120, marker="D", color=line.get_color(), zorder=100+int(8%(select+1)))
    
    if tcool_mix_B_tcc[select] == 0.2:
        index = 2/3.
        K1, K2 = 6./10.**index, 80./10.**index
        plt.fill_between(area_data[:till+1,2]/area_data[0,2], K1*(area_data[:till+1,2]/area_data[0,2])**index, K2*(area_data[:till+1,2]/area_data[0,2])**index, 
                         color="lemonchiffon", alpha=0.8, zorder=-100)
        '''
        K1, K2 = 6./10.**(2/3.), 40./10.**(2/3.)
        plt.fill_between(area_data[:till+1,2]/area_data[0,2], K1*(area_data[:till+1,2]/area_data[0,2])**(2/3.), K2*(area_data[:till+1,2]/area_data[0,2])**(2/3.), 
                         color="gray", alpha=0.3, zorder=-100)
        '''

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.7)
plt.xlim(xmin=0.7)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"Volume $V_{\rm cl}$ ($T<8\times 10^4$ K) [$V_{\rm cl, ini}$]")
plt.ylabel(r"Surface area $A_{\rm cl}$ ($T<8\times 10^4$ K) [$A_{\rm cl, ini}$]")
plt.savefig(f"area-cold-trunc_volume{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")
        
print("area-distance")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_mass = cloud_data[key]['cloud_tot_mass']
        cloud_pos_y = np.array(cloud_data[key]['cloud_pos_y'])
        cloud_pos_z = np.array(cloud_data[key]['cloud_pos_z'])
        cloud_area  = cloud_data[key]['cloud_tot_surface_area']

        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        wind_vel = CC85windvel(cloud_com/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
        delta_v = (wind_vel - cloud_velocity_r)/wind_vel 
        
        area_data.append([float(key),
                          cloud_com,
                          cloud_area,
                          cloud_mdot,
                          delta_v,
                          cloud_mass,
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    if tcool_mix_B_tcc[select] == 0.2:
        a_pow = 3*gamma-2 # 2/3*(7/6) + 4*gamma/3.
        K1, K2 = 20/2**a_pow, 600/3**a_pow
        plt.fill_between(area_data[:till+1,1]/area_data[0,1], K1*(area_data[:till+1,1]/area_data[0,1])**a_pow, K2*(area_data[:till+1,1]/area_data[0,1])**a_pow, 
                         color="lemonchiffon", alpha=0.8, zorder=-100)
        a_pow = 3*(gamma-1/2.) # 2/3*(23/12) + 4*gamma/3.
        K1, K2 = 80/2**a_pow, 300/2**a_pow
        plt.fill_between(area_data[:till+1,1]/area_data[0,1], K1*(area_data[:till+1,1]/area_data[0,1])**a_pow, K2*(area_data[:till+1,1]/area_data[0,1])**a_pow, 
                         color="gray", alpha=0.3, zorder=-100)
    # print(tcool_mix_B_tcc[select], area_data[:till+1,2])

    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    # plt.plot(area_data[:till+1,4]/area_data[0,4], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}') # del_v
    
    # area-distance
    line, = plt.plot(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))
    
    where = interp1d(area_data[:till+1,4], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(0.2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=180, marker="*", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("vel", tcool_mix_B_tcc[select], where)
    
    where = interp1d(area_data[:till+1,5]/area_data[0,5], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=120, marker="D", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("mass", tcool_mix_B_tcc[select], where)

    np.savetxt(f"./paraview-cloud-analysis_data-dump/{label}.cold-area-distance.txt", np.vstack( [area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2]] ).T)

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.2, ymax=8.0e+03)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Surface area $A_{\rm cl}$ ($T<8\times 10^4$ K) [$A_{\rm cl, ini}$]")
plt.savefig(f"area-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")  

print("spread-distance")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_mass = cloud_data[key]['cloud_tot_mass']
        cloud_pos_y = np.array(cloud_data[key]['cloud_pos_y'])
        cloud_pos_z = np.array(cloud_data[key]['cloud_pos_z'])
        cloud_prp   = np.sqrt(cloud_pos_y**2 + cloud_pos_z**2)
        cloud_sprd  = np.percentile(cloud_prp, 95) - np.percentile(cloud_prp, 5)

        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        wind_vel = CC85windvel(cloud_com/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
        delta_v = (wind_vel - cloud_velocity_r)/wind_vel 
        
        area_data.append([float(key),
                          cloud_com,
                          cloud_sprd,
                          cloud_mdot,
                          delta_v,
                          cloud_mass,
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    
    if tcool_mix_B_tcc[select] == 0.2:
        K1, K2 = 5/3, 15/2
        plt.fill_between(area_data[:till+1,1]/area_data[0,1], K1*(area_data[:till+1,1]/area_data[0,1]), K2*(area_data[:till+1,1]/area_data[0,1]), 
                         color="lemonchiffon", alpha=0.8, zorder=-100)
    # print(tcool_mix_B_tcc[select], area_data[:till+1,2])

    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    # plt.plot(area_data[:till+1,4]/area_data[0,4], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}') # del_v
    
    # spread-distance
    line, = plt.plot(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))
    
    where = interp1d(area_data[:till+1,4], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(0.2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=180, marker="*", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("vel", tcool_mix_B_tcc[select], where)
    
    where = interp1d(area_data[:till+1,5]/area_data[0,5], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=120, marker="D", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("mass", tcool_mix_B_tcc[select], where)

    np.savetxt(f"./paraview-cloud-analysis_data-dump/{label}.cold-spread-distance.txt", np.vstack( [area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2]] ).T)

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.6, ymax=35.0)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Cloud spread $R_{\rm cl,\perp}$ [$R_{\rm cl, ini}$]")
plt.savefig(f"spread-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!") 


print("length-distance")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_mass = cloud_data[key]['cloud_tot_mass']
        cloud_pos_x = np.array(cloud_data[key]['cloud_pos_x'])
        cloud_prl   = cloud_pos_x
        cloud_len   = np.percentile(cloud_prl, 95) - np.percentile(cloud_prl, 5)

        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        wind_vel = CC85windvel(cloud_com/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
        delta_v = (wind_vel - cloud_velocity_r)/wind_vel 
        
        area_data.append([float(key),
                          cloud_com,
                          cloud_len,
                          cloud_mdot,
                          delta_v,
                          cloud_mass,
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    
    if tcool_mix_B_tcc[select] == 0.2:
        K1, K2 = 20/2, 115/2
        plt.fill_between(area_data[:till+1,1]/area_data[0,1], K1*(area_data[:till+1,1]/area_data[0,1]), K2*(area_data[:till+1,1]/area_data[0,1]), 
                         color="lemonchiffon", alpha=0.8, zorder=-100)
    
    # print(tcool_mix_B_tcc[select], area_data[:till+1,2])

    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    # plt.plot(area_data[:till+1,4]/area_data[0,4], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}') # del_v
    
    # length-distance
    line, = plt.plot(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))
    
    where = interp1d(area_data[:till+1,4], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(0.2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=180, marker="*", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("vel", tcool_mix_B_tcc[select], where)
    
    where = interp1d(area_data[:till+1,5]/area_data[0,5], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(2)
    if where<=np.max(area_data[:till+1,1]/area_data[0,1]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2], fill_value="extrapolate")(where), 
                    s=120, marker="D", color=line.get_color(), zorder=100+int(8%(select+1)))
    # print("mass", tcool_mix_B_tcc[select], where)

    np.savetxt(f"./paraview-cloud-analysis_data-dump/{label}.cold-length-distance.txt", np.vstack( [area_data[:till+1,1]/area_data[0,1], area_data[:till+1,2]/area_data[0,2]] ).T)

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.9, ymax=222.0)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Cloud length $R_{\rm cl,\parallel}$ [$R_{\rm cl, ini}$]")
plt.savefig(f"length-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!") 

print("mass-distance")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_velocity = np.sqrt( cloud_velocity_r**2 + cloud_velocity_th**2 + cloud_velocity_ph**2 )
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        wind_vel = CC85windvel(cloud_com/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
        delta_v = (wind_vel - cloud_velocity_r)/wind_vel 
        
        area_data.append([float(key),
                          cloud_data[key]['cloud_tot_mass'],
                          cloud_data[key]['cloud_tot_surface_area'],
                          cloud_velocity,
                          cloud_com,
                          np.abs(cloud_mdot),
                          np.average(cloud_data[key]['cloud_surface_vin_elems']),
                          np.average(cloud_data[key]['cloud_surface_density']),
                          delta_v,
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    wind_vel = CC85windvel(area_data[:till+1,4]/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
    
    mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    mass_smoothed = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=0)
    mdot_from_mass = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=1)/area_data[0,1]
    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    # plt.plot(area_data[:till+1,4]/area_data[0,4], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}') # del_v
    
    # mass-distance
    line, = plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}', zorder=100+int(8%(select+1)))
    where = interp1d(area_data[:till+1,8], area_data[:till+1,4]/area_data[0,4], fill_value="extrapolate")(0.2)
    if where<=np.max(area_data[:till+1,4]/area_data[0,4]):
        plt.scatter(where, 
                    interp1d(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1], fill_value="extrapolate")(where), 
                    s=180, marker="*", color=line.get_color(), zorder=100+int(8%(select+1)))
    
    np.savetxt(f"./paraview-cloud-analysis_data-dump/{label}.cold-mass-distance.txt", np.vstack( [area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1]] ).T)
    # plt.plot(area_data[:till+1,4]/area_data[0,4], K0*(area_data[:till+1,4]/area_data[0,4]), color='k', linestyle="--")
    if tcool_mix_B_tcc[select] == 0.2:
        m_pow = 7/6
        K0, K1, K2 = 1.71/1.46**m_pow, 1.5/3**m_pow, 3./2**m_pow
        plt.fill_between(area_data[:till+1,4]/area_data[0,4], K1*(area_data[:till+1,4]/area_data[0,4])**m_pow, K2*(area_data[:till+1,4]/area_data[0,4])**m_pow, 
                         color="lemonchiffon", alpha=0.8, zorder=-100)
        '''
        K0, K1, K2 = 1.71/1.46**m_pow, 1.51/1.46**m_pow, 1.71/1.14**m_pow
        plt.fill_between(area_data[:till+1,4]/area_data[0,4], K1*(area_data[:till+1,4]/area_data[0,4])**m_pow, K2*(area_data[:till+1,4]/area_data[0,4])**m_pow, 
                         color="gray", alpha=0.3, zorder=-100)
        '''
        m_pow = 23/12
        K0, K1, K2 = 1.71/1.46**m_pow, 2.5/2**m_pow, 10.3/3**m_pow
        plt.fill_between(area_data[:till+1,4]/area_data[0,4], K1*(area_data[:till+1,4]/area_data[0,4])**m_pow, K2*(area_data[:till+1,4]/area_data[0,4])**m_pow, 
                         color="gray", alpha=0.3, zorder=-100)

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.6, ymax=22.0)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Cold mass $M_{\rm cl}$ ($T<8\times 10^4$ K) [$M_{\rm cl, ini}$]")
plt.savefig(f"mass-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")
"""
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_velocity = np.sqrt( cloud_velocity_r**2 + cloud_velocity_th**2 + cloud_velocity_ph**2 )
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        area_data.append([float(key),
                          cloud_data[key]['cloud_tot_mass'],
                          cloud_data[key]['cloud_tot_surface_area'],
                          cloud_velocity,
                          cloud_com,
                          np.abs(cloud_mdot),
                          np.average(cloud_data[key]['cloud_surface_vin_elems']),
                          np.average(cloud_data[key]['cloud_surface_density']),
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    wind_vel = CC85windvel(area_data[:till+1,4]/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
    
    mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    mass_smoothed = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=0)
    mdot_from_mass = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=1)/area_data[0,1]
    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    plt.plot(area_data[:till+1,4]/area_data[0,4], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}',
             zorder=100+int(8%(select+1))) # del_v
    
    # mass-distance
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], K0*(area_data[:till+1,4]/area_data[0,4]), color='k', linestyle="--")

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.06)#, ymax=22.0)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Cold mass velocity $|v_{\rm cl}-v_{\rm wind}|$ ($T<8\times 10^4$ K) [$v_{\rm wind}$]")
plt.savefig(f"vel_diff-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    directory_vanl = f"{root_vanl}-{label}"
    # print(label)
    analysis_file_vanl = np.loadtxt(f"{directory_vanl}/analysis.dat")
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_velocity = np.sqrt( cloud_velocity_r**2 + cloud_velocity_th**2 + cloud_velocity_ph**2 )
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        area_data.append([float(key),
                          cloud_data[key]['cloud_tot_mass'],
                          cloud_data[key]['cloud_tot_surface_area'],
                          cloud_velocity,
                          cloud_com,
                          np.abs(cloud_mdot),
                          np.average(cloud_data[key]['cloud_surface_vin_elems']),
                          np.average(cloud_data[key]['cloud_surface_density']),
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    wind_vel = CC85windvel(area_data[:till+1,4]/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
    
    mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    mass_smoothed = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=0)
    mdot_from_mass = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=1)/area_data[0,1]
    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    line, = plt.plot(area_data[:till+1,0], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}',
                     zorder=-int(50*(select+1)) ) # del_v
    plt.plot(analysis_file_vanl[:,0]/tcc, np.abs(analysis_file_vanl[:,2]-1.0)/1.0, color=line.get_color(),
             linestyle=(0, (5, 5)), linewidth=1.5, alpha=1.0, zorder=-int(50*(select+1)) ) # del_v
    
    # mass-distance
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], K0*(area_data[:till+1,4]/area_data[0,4]), color='k', linestyle="--")

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.06)#, ymax=22.0)
plt.xlim(xmin=0., xmax = till)
plt.yscale('log')
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"$|v_{\rm cl}-v_{\rm wind}|$ ($T<8\times 10^4$ K) [$v_{\rm wind}$]")
plt.savefig(f"vel_diff-cold-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()

for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    Mass          Area       Velocity    Position      Mdot
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_velocity_r = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_r'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_th = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_th'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_velocity_ph = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_velocity_ph'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        
        cloud_velocity = np.sqrt( cloud_velocity_r**2 + cloud_velocity_th**2 + cloud_velocity_ph**2 )
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        cloud_mdot = np.sum(-cloud_data[key]['cloud_surface_density']*cloud_data[key]['cloud_tot_surface_area']*cloud_data[key]['cloud_surface_vin_elems'])
        area_data.append([float(key)*(UNIT_LENGTH/UNIT_VELOCITY)*tcc/Myr,
                          cloud_data[key]['cloud_tot_mass'],
                          cloud_data[key]['cloud_tot_surface_area'],
                          cloud_velocity,
                          cloud_com,
                          np.abs(cloud_mdot),
                          np.average(cloud_data[key]['cloud_surface_vin_elems']),
                          np.average(cloud_data[key]['cloud_surface_density']),
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    wind_vel = CC85windvel(area_data[:till+1,4]/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units
    
    mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    mass_smoothed = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=0)
    mdot_from_mass = scipy.signal.savgol_filter(area_data[:till+1,1], window_length=6, polyorder=4, deriv=1)/area_data[0,1]
    # smooth mass test
    # line, = plt.plot(area_data[:till+1,0], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,0], mass_smoothed/mass_smoothed[0], color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,0], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}') # dM/dt [M0/tcc]
    # mdot_from_mass = np.gradient(area_data[:till+1,0]*tcc, area_data[:till+1,1])/(area_data[0,1]/tcc)
    # plt.plot(area_data[:till+1,0], mdot_from_mass, color=line.get_color(), linestyle="--")

    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], mdot_from_mass, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,5]/(area_data[0,1]/tcc), color=line.get_color(), linestyle="--")
    
    # line, = plt.plot(area_data[:till+1,4]/area_data[0,4], -mdot_from_mass/(area_data[:till+1,7]*area_data[:till+1,2]), label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,6], color=line.get_color(), linestyle="--")
    
    # velocity
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,3]/cs, label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], wind_vel/cs, color='k', linestyle="--")
    plt.plot(area_data[:till+1,0], np.abs(area_data[:till+1,3]-wind_vel)/wind_vel, 
             label=f'{tcool_mix_B_tcc[select]:.2f}, {(UNIT_LENGTH/pc):.2f}',
             zorder=100+int(8%(select+1))) # del_v
    
    # mass-distance
    # plt.plot(area_data[:till+1,4]/area_data[0,4], area_data[:till+1,1]/area_data[0,1], label=f'{tcool_mix_B_tcc[select]:.2f}')
    # plt.plot(area_data[:till+1,4]/area_data[0,4], K0*(area_data[:till+1,4]/area_data[0,4]), color='k', linestyle="--")

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$, $R_{\rm cl}$ [pc]", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=0.06)#, ymax=22.0)
plt.xlim(xmin=0.) #, xmax = till)
plt.yscale('log')
plt.xlabel(r"time [Myr]")
plt.ylabel(r"$|v_{\rm cl}-v_{\rm wind}|$ ($T<8\times 10^4$ K) [$v_{\rm wind}$]")
plt.savefig(f"vel_diff-cold-Myr-trunc_time{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
"""

print("vin-distance")
for select in range(len(tcool_mix_B_tcc)):
    label = f"c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
    directory = f"{root}-{label}"
    UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
    UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
    UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
    distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # t/tcc    vin      distance
    area_data = []
    for key in list(cloud_data.keys()):
        cloud_com = np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems']*cloud_data[key]['cloud_distance'])/np.sum(cloud_data[key]['cloud_density']*cloud_data[key]['cloud_volume_elems'])
        area_data.append([float(key),
                         -cloud_data[key]['vin_avg'],
                          cloud_com,
                          ])
    area_data = np.array(area_data)
    
    if tcool_mix_B_tcc[select]==0.1:
        till = 42
    elif tcool_mix_B_tcc[select]==0.2:
        till = 62
    else:
        till = 100
    wind_vel = CC85windvel(area_data[:till+1,2]/distance_ini * diniBdinj)/CC85windvel(diniBdinj) # code units

    line, = plt.plot(area_data[:till+1,2]/area_data[0,2], np.abs(area_data[:till+1,1])/wind_vel, label=f'{tcool_mix_B_tcc[select]:.2f}',
                     zorder=100+int(8%(select+1))) # v_in
    
    if tcool_mix_B_tcc[select] == 0.2:
        index = -gamma/2
        K1, K2 = 1.0e-02/2.0**index, 7.0e-03/1.0**index
        plt.fill_between(area_data[:till+1,2]/area_data[0,2], K1*(area_data[:till+1,2]/area_data[0,2])**index, K2*(area_data[:till+1,2]/area_data[0,2])**index, 
                         color="lemonchiffon", alpha=0.8, zorder=-100)

plt.legend(loc="best", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
            prop = { "size": 20 }, title_fontsize=22, fancybox=True)
# plt.ylim(ymin=0.06)#, ymax=22.0)
plt.xlim(xmin=0.98, xmax=11.2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
plt.ylabel(r"Inflow velocity $v_{\rm in}$ ($T<8\times 10^4$ K) [$v_{\rm wind}$]")
plt.savefig(f"vel_inf-cold-trunc_distance{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
# plt.show()
plt.close()
print("Done!")

"""
plt.rcParams.update(cycler.cycler(color=palettes.paultol_muted))
os.makedirs(f"profiles-paraview", exist_ok = True)
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

    with open(f"./paraview-cloud-analysis_data-dump/{label}.pickle", "rb") as handle:
        cloud_data = pickle.load(handle)
    # print(f"./paraview-cloud-analysis_data-dump/{label}.pickle")
    # print(list(cloud_data.keys()))
    count = 0
    distance_min, distance_max = None, None
    for key in list(cloud_data.keys()):
        if int(key)%8 > 1.0e-06:
            continue
        cloud_density  = cloud_data[key]['cloud_density']* UNIT_DENSITY/(mu*mp)/ndens_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 42
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 64
        if float(key)>till:
            continue

        if count==0:
            distance_min = np.min(cloud_distance)
            distance_max = np.max(cloud_distance)
        else:
            distance_min = distance_min if (_tmp:=np.min(cloud_distance))>distance_min else _tmp
            distance_max = distance_max if (_tmp:=np.max(cloud_distance))<distance_max else _tmp
        count += 1

        line, = plt.plot(cloud_distance, cloud_density, marker='.', markersize=4, linestyle='None', rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
    '''
    if distance_min<0.5*diniBdinj:
        distance_min = 0.5*diniBdinj
    if distance_max<1.5*diniBdinj:
        distance_max = 1.5*diniBdinj
    '''    
    ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
    prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

    plt.plot(distance_w, ndens_w/ndens_w_ini, linestyle="--", color="black", linewidth=2.0)
    plt.plot(distance_w, prs_w/prs_w_ini*chi, linestyle=":", color="gray", linewidth=2.0)
    plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
               prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    # plt.ylim(ymin=0.06)#, ymax=22.0)
    # plt.xlim(xmin=distance_min, xmax=distance_max)
    contrast_highlight = 10.0
    plt.plot(distance_w, contrast_highlight*ndens_w/ndens_w_ini, color='black', linestyle=(0, (5, 5)))
    # plt.hlines(contrast_highlight, xmin=0.8, xmax=1.01*distance_max, colors='black', linestyles=(0, (5, 5)))
    plt.xlim(xmin=0.8, xmax=1.01*distance_max)
    # plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
    plt.ylabel(r"Density [initial wind density]")
    plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
    plt.savefig(f"profiles-paraview/density-profile_{tcool_mix_B_tcc[select]:.2f}{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
    # plt.show()
    plt.close()

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
        if int(key)%8 > 1.0e-06:
            continue
        cloud_pressure  = cloud_data[key]['cloud_pressure']* UNIT_DENSITY*UNIT_VELOCITY**2/kB/prs_w_ini
        cloud_distance = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 42
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 64
        if float(key)>till:
            continue

        if count==0:
            distance_min = np.min(cloud_distance)
            distance_max = np.max(cloud_distance)
        else:
            distance_min = distance_min if (_tmp:=np.min(cloud_distance))>distance_min else _tmp
            distance_max = distance_max if (_tmp:=np.max(cloud_distance))<distance_max else _tmp
        count += 1

        line, = plt.plot(cloud_distance, cloud_pressure, marker='.', markersize=4, linestyle='None', rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
    '''
    if distance_min<0.5*diniBdinj:
        distance_min = 0.5*diniBdinj
    if distance_max<1.5*diniBdinj:
        distance_max = 1.5*diniBdinj
    '''    
    ndens_w   = (CC85windrho(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000) * diniBdinj)/CC85windrho(diniBdinj)) * UNIT_DENSITY/(mu*mp) # cgs
    prs_w     = (CC85windprs(distance_w*diniBdinj)/CC85windprs(diniBdinj)) * prs_w_ini

    plt.plot(distance_w, prs_w/prs_w_ini, linestyle="--", color="black", linewidth=2.0)
    plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
               prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    # plt.ylim(ymin=0.06)#, ymax=22.0)
    # plt.xlim(xmin=distance_min, xmax=distance_max)
    plt.xlim(xmin=0.8, xmax=1.01*distance_max)
    # plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
    plt.ylabel(r"Pressure [initial wind pressure]")
    plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
    plt.savefig(f"profiles-paraview/pressure-profile_{tcool_mix_B_tcc[select]:.2f}{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
    # plt.show()
    plt.close()

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
        if int(key)%8 > 1.0e-06:
            continue
        cloud_velocity  = np.sqrt(cloud_data[key]['cloud_velocity_r']**2 + cloud_data[key]['cloud_velocity_th']**2 + cloud_data[key]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        cloud_distance  = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 42
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 64
        if float(key)>till:
            continue

        if count==0:
            distance_min = np.min(cloud_distance)
            distance_max = np.max(cloud_distance)
        else:
            distance_min = distance_min if (_tmp:=np.min(cloud_distance))>distance_min else _tmp
            distance_max = distance_max if (_tmp:=np.max(cloud_distance))<distance_max else _tmp
        count += 1

        line, = plt.plot(cloud_distance, cloud_velocity/v_w_ini, marker='.', markersize=4, linestyle='None', rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
    '''
    if distance_min<0.5*diniBdinj:
        distance_min = 0.5*diniBdinj
    if distance_max<1.5*diniBdinj:
        distance_max = 1.5*diniBdinj
    '''
    v_w     = (CC85windvel(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000)*diniBdinj)/CC85windvel(diniBdinj)) * v_w_ini

    plt.plot(distance_w, v_w/v_w_ini, linestyle="--", color="black", linewidth=2.0)
    plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
               prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    # plt.ylim(ymin=0.06)#, ymax=22.0)
    # plt.xlim(xmin=distance_min, xmax=distance_max)
    plt.xlim(xmin=0.98, xmax=1.01*distance_max)
    # plt.xscale('log')
    # plt.yscale('log')
    plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
    plt.ylabel(r"Velocity [initial wind velocity]")
    plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
    plt.savefig(f"profiles-paraview/velocity-profile_{tcool_mix_B_tcc[select]:.2f}{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
    # plt.show()
    plt.close()

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
        if int(key)%8 > 1.0e-06:
            continue
        cloud_velocity  = np.sqrt(cloud_data[key]['cloud_velocity_r']**2 + cloud_data[key]['cloud_velocity_th']**2 + cloud_data[key]['cloud_velocity_ph']**2) * UNIT_VELOCITY
        cloud_distance  = cloud_data[key]['cloud_distance']/distance_ini

        if tcool_mix_B_tcc[select]==0.1:
            till = 42
        elif tcool_mix_B_tcc[select]==0.2:
            till = 62
        else:
            till = 64
        if float(key)>till:
            continue

        if count==0:
            distance_min = np.min(cloud_distance)
            distance_max = np.max(cloud_distance)
        else:
            distance_min = distance_min if (_tmp:=np.min(cloud_distance))>distance_min else _tmp
            distance_max = distance_max if (_tmp:=np.max(cloud_distance))<distance_max else _tmp
        count += 1

        v_w     = (CC85windvel(cloud_distance*diniBdinj)/CC85windvel(diniBdinj)) * v_w_ini
        line, = plt.plot(cloud_distance, (cloud_velocity-v_w)/v_w, marker='.', markersize=4, linestyle='None', rasterized=True)
        plt.plot([], [], color=line.get_color(), label=f"{key}")
    '''
    if distance_min<0.5*diniBdinj:
        distance_min = 0.5*diniBdinj
    if distance_max<1.5*diniBdinj:
        distance_max = 1.5*diniBdinj
    '''
    v_w     = (CC85windvel(distance_w:=np.linspace(0.98*distance_min, distance_max, 1000)*diniBdinj)/CC85windvel(diniBdinj)) * v_w_ini

    # plt.plot(distance_w, v_w/v_w_ini, linestyle="--", color="black", linewidth=2.0)
    plt.legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=3,
               prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    # plt.ylim(ymin=0.06)#, ymax=22.0)
    # plt.xlim(xmin=distance_min, xmax=distance_max)
    plt.xlim(xmin=0.98, xmax=1.01*distance_max)
    # plt.xscale('log')
    # plt.yscale('log')
    plt.xlabel(r"distance $d_{\rm cl}$ [$d_{\rm ini}$]")
    plt.ylabel(r"$\Delta v = v_{\rm cl} - v_{\rm wind}$ [wind velocity]")
    plt.title(r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$ = "+f'{tcool_mix_B_tcc[select]:.2f}')
    plt.savefig(f"profiles-paraview/velocity_delta-profile_{tcool_mix_B_tcc[select]:.2f}{'-dark' if dark else ''}.svg", bbox_inches='tight', transparent=True)
    # plt.show()
    plt.close()
"""
