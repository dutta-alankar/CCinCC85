# -*- coding: utf-8 -*-
"""
Created on Sat May 11 11:14:42 2024

@author: alankar
Usage: time python shell-plots.py
"""
import pickle
import numpy as np
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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

## useful constants
yr     = 365*24*60**2
Myr    = 1e6*yr
MSun   = 2.e33
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

plot_freq = 1

no_profiles = True

for select in range(0, len(tcool_mix_B_tcc), 1):
    filename = f'./shell-calcs/shell_profiles-vanl_{tcool_mix_B_tcc[select]}.pickle'
    with open(filename, 'rb') as handle:
        series_vanl = pickle.load(handle)
    filename = f'./shell-calcs/shell_profiles_{tcool_mix_B_tcc[select]}.pickle'
    print(filename, end = "\r")
    with open(filename, 'rb') as handle:
        series_cc85 = pickle.load(handle)

    '''
    Cold mass total plot
    '''
    matplotlib.rcParams["figure.figsize"] = (13,10)
    time_cc85 = np.array([series_cc85[indx]["tBtccini"] for indx in range(len(series_cc85)-1)])
    cold_mass_cc85 = np.array(series_cc85[-1]["mass_cl_tot"])
    time_vanl = np.array([series_vanl[indx]["tBtccini"] for indx in range(len(series_vanl)-1)])
    cold_mass_vanl = np.array(series_vanl[-1]["mass_cl_tot"])
    line = plt.semilogy(time_cc85, cold_mass_cc85[:time_cc85.shape[0]]/cold_mass_cc85[0], label=f"{tcool_mix_B_tcc[select]:.1f}")
    line = plt.semilogy(time_vanl, cold_mass_vanl[:time_vanl.shape[0]]/cold_mass_vanl[0], 
                        color=line[-1].get_color(), linestyle="--")
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"Cold mass [$M_{\rm cold,ini}$]")
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.ylim(ymin=2.0e-01)
plt.savefig(f'./shell-calcs/cold-mass.svg', transparent=False, bbox_inches="tight")
plt.close()

if no_profiles:
    sys.exit(0)

for select in range(len(tcool_mix_B_tcc)):
    filename = f'./shell-calcs/shell_profiles-vanl_{tcool_mix_B_tcc[select]}.pickle'
    with open(filename, 'rb') as handle:
        series_vanl = pickle.load(handle)
    filename = f'./shell-calcs/shell_profiles_{tcool_mix_B_tcc[select]}.pickle'
    print(filename, end = "\r")
    with open(filename, 'rb') as handle:
        series_cc85 = pickle.load(handle)

    os.makedirs(f"./shell-calcs/{tcool_mix_B_tcc[select]}", exist_ok = True)
    # last entry is m_cold_tot
    for time_indx in range(0, min(len(series_vanl), len(series_cc85))-1, plot_freq):
        string = filename + f" {tcool_mix_B_tcc[select]} {time_indx}"
        print(string, end="\r")
        if "distanceBdini" not in list(series_cc85[time_indx].keys()) or "distanceBdini" not in list(series_vanl[time_indx].keys()):
            print(" "*len(string), end="\r")
            print(filename, end="\r")
            continue
        '''
        Rclprp plot
        '''
        matplotlib.rcParams["figure.figsize"] = (26,10)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # cloud
        ax1.plot(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["Rclprp"]/1.0, label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax2.plot(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["Rclprp"]/1.0, label=f"{series_vanl[time_indx]['tBtccini']:.1f}")

        # ax1.semilogy(series_cc85[time_indx]["distanceBdini"], np.ones_like(series_cc85[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")
        # ax2.semilogy(series_vanl[time_indx]["distanceBdini"], np.ones_like(series_vanl[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")


        ax1.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        ax2.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    
        forward = lambda arg: arg*np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])
        inverse = lambda arg: arg/np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])

        ax1.set_title("CC85 wind", size=30)
        ax2.set_title("Plane parallel constant wind (vanilla)", size=30)

        # ax1.set_xlim(xmin=1.0, xmax=9.0)
        # ax2.set_xlim(xmin=1.0, xmax=9.0)

        # ax1.set_ylim(ymin=2.0e-02, ymax=1.2e+02)
        # ax2.set_ylim(ymin=2.0e-02, ymax=1.2e+02)

        ax_top = ax1.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1.set_ylabel(r"perpendicular cloud extent [$R_{\rm cl,ini}$]")
        ax1.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2.set_ylabel(r"perpendicular cloud extent [$R_{\rm cl,ini}$]")
        ax2.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
    
        plt.savefig(f'./shell-calcs/{tcool_mix_B_tcc[select]}/Rclprp.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()
        '''
        Flux plot
        '''
        matplotlib.rcParams["figure.figsize"] = (26,10)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # cloud
        ax1.semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["flux_cl"]/(series_cc85[-1]["mass_cl_tot"][0]), label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax2.semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["flux_cl"]/(series_vanl[-1]["mass_cl_tot"][0]), label=f"{series_vanl[time_indx]['tBtccini']:.1f}")

        # ax1.semilogy(series_cc85[time_indx]["distanceBdini"], np.ones_like(series_cc85[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")
        # ax2.semilogy(series_vanl[time_indx]["distanceBdini"], np.ones_like(series_vanl[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")


        ax1.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        ax2.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
    
        forward = lambda arg: arg*np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])
        inverse = lambda arg: arg/np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])

        ax1.set_title("CC85 wind", size=30)
        ax2.set_title("Plane parallel constant wind (vanilla)", size=30)

        # ax1.set_xlim(xmin=1.0, xmax=9.0)
        # ax2.set_xlim(xmin=1.0, xmax=9.0)

        # ax1.set_ylim(ymin=2.0e-02, ymax=1.2e+02)
        # ax2.set_ylim(ymin=2.0e-02, ymax=1.2e+02)

        ax_top = ax1.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1.set_ylabel(r"$\dot{M}\ {\rm [}M_{\rm cl,ini}\ {\rm Myr^{-1}}{\rm ]}$")
        ax1.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2.set_ylabel(r"$\dot{M}\ {\rm [}M_{\rm cl,ini}\ {\rm Myr^{-1}}{\rm ]}$")
        ax2.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")

        plt.savefig(f'./shell-calcs/{tcool_mix_B_tcc[select]}/flux.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()

        '''
        Cold mass profile plot
        '''
        matplotlib.rcParams["figure.figsize"] = (26,10)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        if time_indx == 0:
            m_cl_tot_cc85_ini = series_cc85[-1]["mass_cl_tot"][0]
            m_cl_tot_vanl_ini = series_cc85[-1]["mass_cl_tot"][0]
        # cloud
        ax1.semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["m_cl"]/m_cl_tot_cc85_ini, label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax2.semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["m_cl"]/m_cl_tot_vanl_ini, label=f"{series_vanl[time_indx]['tBtccini']:.1f}")

        # ax1.semilogy(series_cc85[time_indx]["distanceBdini"], np.ones_like(series_cc85[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")
        # ax2.semilogy(series_vanl[time_indx]["distanceBdini"], np.ones_like(series_vanl[time_indx]["distanceBdini"])*10.0, 
        #          linestyle="None", marker="o", color="k")


        ax1.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
        ax2.legend(loc="upper right", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)

        forward = lambda arg: arg*np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])
        inverse = lambda arg: arg/np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])

        ax1.set_title("CC85 wind", size=30)
        ax2.set_title("Plane parallel constant wind (vanilla)", size=30)

        # ax1.set_xlim(xmin=1.0, xmax=9.0)
        # ax2.set_xlim(xmin=1.0, xmax=9.0)

        # ax1.set_ylim(ymin=2.0e-02, ymax=1.2e+02)
        # ax2.set_ylim(ymin=2.0e-02, ymax=1.2e+02)

        ax_top = ax1.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2.secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1.set_ylabel(r"Cold mass [$M_{\rm cold,ini}$]")
        ax1.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2.set_ylabel(r"Cold mass [$M_{\rm cold,ini}$]")
        ax2.set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")

        plt.savefig(f'./shell-calcs/{tcool_mix_B_tcc[select]}/cold-mass.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()

        '''
        Multiple profiles plot
        '''
        matplotlib.rcParams["figure.figsize"] = (28,50)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 2)
        # cloud
        ax1[0].semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["rho_cl"]/(mu*mp), label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax1[1].semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["rho_cl"]/(mu*mp), label=f"{series_vanl[time_indx]['tBtccini']:.1f}")
        ax2[0].plot(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["v_cl"], label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax2[1].plot(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["v_cl"], label=f"{series_vanl[time_indx]['tBtccini']:.1f}")
        ax3[0].semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["T_cl"], label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax3[1].semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["T_cl"], label=f"{series_vanl[time_indx]['tBtccini']:.1f}")
        # wind
        choose = min(len(series_vanl), len(series_cc85))-5
        x_wind = np.arange(1.0, 9.0, 0.1)
        x_val, y_val = [], []
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_cc85[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_cc85[indx]["rhowind"]/(mu*mp)) )
        y_val = np.array(y_val.flatten()[np.argsort(x_val.flatten())])
        x_val = np.array(np.sort(x_val.flatten()))
        ax1[0].semilogy(x_wind, interp1d(x_val, y_val, fill_value="extrapolate")(x_wind), linestyle='-', color="k", marker="None")

        x_val, y_val = [], []
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_vanl[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_vanl[indx]["rhowind"]/(mu*mp)) )
        y_val = np.average(np.array(y_val.flatten()[np.argsort(x_val.flatten())]))
        x_val = np.array(np.sort(x_val.flatten()))
        ax1[1].semilogy(x_wind, y_val*np.ones_like(x_wind), linestyle='-', color="k", marker="None")

        x_val = np.array(series_cc85[choose]["distanceBdini"])
        y_val = np.array(series_cc85[choose]["vwind"])
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_cc85[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_cc85[indx]["vwind"]) )
        y_val = np.array(y_val.flatten()[np.argsort(x_val.flatten())])
        x_val = np.array(np.sort(x_val.flatten()))
        ax2[0].plot(x_wind, interp1d(x_val, y_val, fill_value="extrapolate")(x_wind), linestyle='-', color="k", marker="None")

        x_val = np.array(series_vanl[choose]["distanceBdini"])
        y_val = np.array(series_vanl[choose]["vwind"])
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_vanl[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_vanl[indx]["vwind"]) )
        y_val = np.average(np.array(y_val.flatten()[np.argsort(x_val.flatten())]))
        x_val = np.array(np.sort(x_val.flatten()))
        ax2[1].plot(x_wind, y_val*np.ones_like(x_wind), linestyle='-', color="k", marker="None")

        x_val = np.array(series_cc85[choose]["distanceBdini"])
        y_val = np.array(series_cc85[choose]["Twind"])
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_cc85[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_cc85[indx]["Twind"]) )
        y_val = np.array(np.array(y_val.flatten()[np.argsort(x_val.flatten())]))
        x_val = np.array(np.sort(x_val.flatten()))
        ax3[0].semilogy(x_wind, interp1d(x_val, y_val, fill_value="extrapolate")(x_wind), linestyle='-', color="k", marker="None")

        x_val = np.array(series_vanl[choose]["distanceBdini"])
        y_val = np.array(series_vanl[choose]["Twind"])
        for indx in range(min(len(series_vanl), len(series_cc85))-1):
            x_val = np.hstack( (x_val, series_vanl[indx]["distanceBdini"]) )
            y_val = np.hstack( (y_val, series_vanl[indx]["Twind"]) )
        y_val = np.average(np.array(y_val.flatten()[np.argsort(x_val.flatten())]))
        x_val = np.array(np.sort(x_val.flatten()))
        ax3[1].semilogy(x_wind, y_val*np.ones_like(x_wind), linestyle='-', color="k", marker="None")

        ax1[0].legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 32 }, title_fontsize=32, fancybox=True)
        ax1[1].legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 32 }, title_fontsize=32, fancybox=True)
    
        forward = lambda arg: arg*np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])
        inverse = lambda arg: arg/np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])

        ax1[0].set_title("CC85 wind", size=32)
        ax1[1].set_title("plane parallel constant wind (vanilla)", size=32)

        # ax1[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax1[1].set_xlim(xmin=1.0, xmax=9.0)
        # ax2[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax2[1].set_xlim(xmin=1.0, xmax=9.0)
        # ax3[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax3[1].set_xlim(xmin=1.0, xmax=9.0)

        # ax1[0].set_ylim(ymin=5.0e-03, ymax=2.0e+02)
        # ax1[1].set_ylim(ymin=5.0e-03, ymax=2.0e+02)
        # ax2[0].set_ylim(ymin=0.05, ymax=1.62)
        # ax2[1].set_ylim(ymin=0.05, ymax=1.62)
        # ax3[0].set_ylim(ymin=2.0e+04, ymax=5.0e+06)
        # ax3[1].set_ylim(ymin=2.0e+04, ymax=5.0e+06)

        ax_top = ax1[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax1[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax3[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax3[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1[0].set_ylabel(r"number density ($\rm cm^{-3}$)")
        ax1[1].set_ylabel(r"number density ($\rm cm^{-3}$)")
        ax2[0].set_ylabel(r"velocity (code units)")
        ax2[1].set_ylabel(r"velocity (code units)")
        ax3[0].set_ylabel(r"temperature (K)")
        ax3[1].set_ylabel(r"temperature (K)")

        ax1[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax1[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax3[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax3[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")

        plt.savefig(f'./shell-calcs/{tcool_mix_B_tcc[select]}/profiles.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()

        '''
        timescale plot
        '''
        matplotlib.rcParams["figure.figsize"] = (28,50)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 2)
        # cloud
        ax1[0].semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["texp"]/series_cc85[time_indx]["tcc"], label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax1[1].semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["texp"]/series_vanl[time_indx]["tcc"], label=f"{series_vanl[time_indx]['tBtccini']:.1f}")
        ax2[0].semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["tsc"]/series_cc85[time_indx]["tcc"], label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax2[1].semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["tsc"]/series_vanl[time_indx]["tcc"], label=f"{series_vanl[time_indx]['tBtccini']:.1f}")
        ax3[0].semilogy(series_cc85[time_indx]["distanceBdini"], series_cc85[time_indx]["tcool"]/series_cc85[time_indx]["tcc"], label=f"{series_cc85[time_indx]['tBtccini']:.1f}")
        ax3[1].semilogy(series_vanl[time_indx]["distanceBdini"], series_vanl[time_indx]["tcool"]/series_vanl[time_indx]["tcc"], label=f"{series_vanl[time_indx]['tBtccini']:.1f}")

        ax1[0].legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 32 }, title_fontsize=32, fancybox=True)
        ax1[1].legend(loc="best", title=r"$t/t_{\rm cc,ini}$", ncols=1,
                   prop = { "size": 32 }, title_fontsize=32, fancybox=True)

        forward = lambda arg: arg*np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])
        inverse = lambda arg: arg/np.average(series_cc85[time_indx]["distanceBRcl"]/series_cc85[time_indx]["distanceBdini"])

        ax1[0].set_title("CC85 wind", size=32)
        ax1[1].set_title("plane parallel constant wind (vanilla)", size=32)

        # ax1[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax1[1].set_xlim(xmin=1.0, xmax=9.0)
        # ax2[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax2[1].set_xlim(xmin=1.0, xmax=9.0)
        # ax3[0].set_xlim(xmin=1.0, xmax=9.0)
        # ax3[1].set_xlim(xmin=1.0, xmax=9.0)
        '''
        ax1[0].set_ylim(ymin=5.0e-03, ymax=2.0e+02)
        ax1[1].set_ylim(ymin=5.0e-03, ymax=2.0e+02)
        ax2[0].set_ylim(ymin=0.05, ymax=1.62)
        ax2[1].set_ylim(ymin=0.05, ymax=1.62)
        ax3[0].set_ylim(ymin=2.0e+04, ymax=5.0e+06)
        ax3[1].set_ylim(ymin=2.0e+04, ymax=5.0e+06)
        '''
        ax_top = ax1[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax1[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax2[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax3[0].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")
        ax_top = ax3[1].secondary_xaxis('top', functions=(forward, inverse))
        ax_top.set_xlabel(r"$d_{\rm cl}/R_{\rm cl}$")

        ax1[0].set_ylabel(r"$t_{\rm exp}/t_{\rm cc}$")
        ax1[1].set_ylabel(r"$t_{\rm exp}/t_{\rm cc}$")
        ax2[0].set_ylabel(r"$t_{\rm sc}/t_{\rm cc}$")
        ax2[1].set_ylabel(r"$t_{\rm sc}/t_{\rm cc}$")
        ax3[0].set_ylabel(r"$t_{\rm cool}/t_{\rm cc}$")
        ax3[1].set_ylabel(r"$t_{\rm cool}/t_{\rm cc}$")

        ax1[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax1[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax2[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax3[0].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
        ax3[1].set_xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")

        plt.savefig(f'./shell-calcs/{tcool_mix_B_tcc[select]}/timescales.{time_indx:04d}.svg', 
                    transparent=False, bbox_inches="tight")
        plt.close()

        print(" "*len(string), end="\r")
        print(filename, end="\r")

    print("")

