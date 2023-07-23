# -*- coding: utf-8 -*-
"""
Created on Mon Jul 01 13:54:56 2023

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

## useful constants
yr     = 365*24*60**2
Myr    = 1e6*yr
pi     = np.pi
pc     = 3.0856775807e18
kpc    = 1e3*pc
Mpc    = 1e3*kpc
s      = 1
cm     = 1
K      = 1
km     = 1e5*cm
mp     = 1.67262192369e-24
kB     = 1.3806505e-16
G      = 6.6726e-8
H0     = 67.4
H0cgs  = H0*((km/s)/Mpc)
dcrit0 = 3*H0cgs**2/(8.*pi*G)
MSun   = 2.e33
X_solar = 0.7154
Y_solar = 0.2703
Z_solar = 0.0143
fracZ   = 1.0
Xp      = X_solar*(1-fracZ*Z_solar)/(X_solar+Y_solar)
Yp      = Y_solar*(1-fracZ*Z_solar)/(X_solar+Y_solar)
Zp      = fracZ*Z_solar
mu     = 1./(2*Xp+0.75*Yp+0.5625*Zp)
mup    = 1./(2*Xp+0.75*Yp+(9./16.)*Zp)
muHp   = 1./Xp
mue    = 2./(1+Xp)
mui    = 1./(1/mu-1/mue)

# Program starts here
gamma = 5/3
alpha = 1.0

wind = np.loadtxt('../../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]

rhonorm  = interp1d(rnorm, wind[:,1])
prsnorm  = interp1d(rnorm, wind[:,2])
velnorm  = interp1d(rnorm, wind[:,3])
mach     = interp1d(rnorm, mach)
Tempnorm = lambda rnorm:prsnorm(rnorm)/rhonorm(rnorm)

relpos = interp1d(wind[:,2]/wind[:,1], rnorm) #inverting the Temperature relation

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

def wind_condition(tcoolmbytcc = 0.10):
    Edot = 2.00e+41  # erg/s
    Mdot = 1.42      # MSun/yr
    Rinj = 200       # pc

    Tcl         = 4.0e+4
    chi = 100 # all chi maynot be possible for a wind as it is too cold due to adiabatic expansion

    Twind_ini = chi*Tcl

    rho_0 = ((Mdot*(MSun/yr))**1.5)  * (Edot**-0.5) * ((Rinj*pc)**-2)
    prs_0 = ((Mdot*(MSun/yr))**0.5)  * (Edot**0.5)  * ((Rinj*pc)**-2)
    vel_0 = ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

    Twindnorm_ini = Twind_ini/((prs_0/rho_0)*mu*mp/kB)

    RinibyRinj = relpos(Twindnorm_ini)
    Mach_ini   = mach(RinibyRinj)

    Rini = RinibyRinj*Rinj # pc

    prswind_ini = prsnorm(RinibyRinj)*prs_0
    rhowind_ini = rhonorm(RinibyRinj)*rho_0
    velwind_ini = velnorm(RinibyRinj)*vel_0

    Rgo  = 2 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
    Rcl  = Rgo/tcoolmbytcc # pc
    # print("dummy: ", 2./(LAMBDA(np.sqrt(chi)*1e4)/10**-21.4) )

    RinibyRcl = Rini/Rcl

    UNIT_LENGTH   = Rcl * pc
    UNIT_DENSITY  = rhowind_ini
    UNIT_VELOCITY = velwind_ini

    print(f"chi = {chi:d}")
    print(f"Mw  = {Mach_ini:.3f}")
    print(f"tcoolmBytcc = {tcoolmbytcc:.2f}")
    print(f"RinibyRcl = {RinibyRcl:.3f}")
    print(f"T_cl = {Tcl:.1e} K")
    print(f"PinibykB = {prswind_ini/kB:.3e} K cm^-3")
    print(f"RinibyRinj = {RinibyRinj:.2f}")
    print(f"R_cl = {Rcl:.1f} pc")
    print(f"R_ini = {Rini:.1f} pc")
    print(f"R_go  = {Rgo:.2f} pc")
    print(f"Mdot = {Mdot:.2e} MSun/yr")
    print(f"Edot = {Edot:.2e} erg/s")
    print(f"R_inj = {Rinj:.1f} pc")

    analysis = f"../../output-c{chi:d},m{Mach_ini:.3f},T4e4,t{tcoolmbytcc:.2f},r{RinibyRcl:.3f}/analysis.dat"
    analysis = np.loadtxt(analysis)

    Tw_cloud_pos = (prsnorm(analysis[:,1]*Rcl/Rinj)*prs_0)/(rhonorm(analysis[:,1]*Rcl/Rinj)*rho_0)*(mu*mp/kB)
    nw_cloud_pos = (rhonorm(analysis[:,1]*Rcl/Rinj)*rho_0)/(mu*mp)
    vw_cloud_pos = (velnorm(analysis[:,1]*Rcl/Rinj)*vel_0)

    tcool_mix = (1/(gamma-1)) * kB*Tcl/(nw_cloud_pos*LAMBDA(np.sqrt(Tcl*Tw_cloud_pos))) * ((mu*Xp)**(-2))
    texp  = analysis[:,1]*UNIT_LENGTH/vw_cloud_pos

    Rcl = Rcl*( analysis[:,14]*((Tw_cloud_pos/(chi*Tcl))**(-1)) * ((nw_cloud_pos/(rhowind_ini/(mu*mp)))**(-1)) )**(1./3) 
    tcc = np.sqrt(Tw_cloud_pos/Tcl) * Rcl * pc / np.abs(analysis[:,2]*UNIT_VELOCITY-vw_cloud_pos)
    tsccl = Rcl*pc/np.sqrt(gamma*kB*Tcl/(mu*mp))

    t_factor_x = tcool_mix/tcc #/((tcool_mix/tcc)[0])*tcoolmbytcc
    t_factor_y = tsccl/texp

    time = analysis[:,0]/np.sqrt(chi)
    time = 0.5*(time[1:]+time[:-1])
    '''
    if (tcoolmbytcc==0.10):
        fig = plt.figure(figsize=(13,10))
        plt.plot(analysis[:,1]*UNIT_LENGTH/pc, (vw_cloud_pos-analysis[:,2]*UNIT_VELOCITY)/vw_cloud_pos)
        plt.show()
    '''

    return (t_factor_x, t_factor_y, time)

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = False
matplotlib.rcParams["ytick.right"] = False
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 0.8
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 0.6
matplotlib.rcParams["xtick.minor.width"] = 0.6
matplotlib.rcParams["ytick.major.size"] = 12.0
matplotlib.rcParams["xtick.major.size"] = 12.0
matplotlib.rcParams["ytick.minor.size"] = 6.0
matplotlib.rcParams["xtick.minor.size"] = 6.0
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

fig = plt.figure(figsize=(15,10))
first = 0
norm = plt.Normalize(0, 30)

def make_plot(tcoolmbytcc = 0.10):
    global first
    t_factor_x, t_factor_y, time = wind_condition(tcoolmbytcc)
    points = np.array([t_factor_x, t_factor_y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    # Set the values used for colormapping
    lc.set_array(time)
    lc.set_linewidth(3)
    line = plt.gca().add_collection(lc)

    if (first==0):
        fig.colorbar(line, ax=plt.gca())
    first += 1

tcoolmbytcc = [0.10, 0.08, 0.06, 0.04]

for ratio in tcoolmbytcc:
    make_plot(tcoolmbytcc = ratio)

plt.xlabel(r"$t_{cool,mix}/t_{cc}$")
plt.ylabel(r"$t_{sc,cl}/t_{exp}$")
plt.yscale("log")
plt.xscale("log")
# plt.gca().set_ylim(1/30, 1/3)
# plt.gca().set_xlim(0.2, 1.2)
plt.tight_layout()
plt.savefig("phase-space.png")
