# -*- coding: utf-8 -*-
"""
Created on Mon Jul 02 14:28:56 2023

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib

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
relpos_mach   = interp1d(mach, rnorm)

rhonorm  = interp1d(rnorm, wind[:,1])
prsnorm  = interp1d(rnorm, wind[:,2])
velnorm  = interp1d(rnorm, wind[:,3])
mach     = interp1d(rnorm, mach)
Tempnorm = lambda rnorm:prsnorm(rnorm)/rhonorm(rnorm)

relpos = interp1d(wind[:,2]/wind[:,1], rnorm) #inverting the Temperature relation

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')
'''
Edot = 2.00e+41  # erg/s
Mdot = 1.33      # MSun/yr
Rinj = 300       # pc
# previous
Edot = 2.00e+41  # erg/s
Mdot = 1.42      # MSun/yr
Rinj = 200       # pc
# Sneider
Edot = 1.50e+42  # erg/s
Mdot = 1.50      # MSun/yr
Rinj = 300       # pc
'''
Edot = 3.00e+41  # erg/s
Mdot = 2.00      # MSun/yr
Rinj = 200       # pc

Tcl         = 4.0e+4

rho_0 = ((Mdot*(MSun/yr))**1.5)  * (Edot**-0.5) * ((Rinj*pc)**-2)
prs_0 = ((Mdot*(MSun/yr))**0.5)  * (Edot**0.5)  * ((Rinj*pc)**-2)
vel_0 = ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

rbyrInj  = np.linspace(0.8, 3.0, 100)
prswind  = prsnorm(rbyrInj)*prs_0
rhowind  = rhonorm(rbyrInj)*rho_0
velwind  = velnorm(rbyrInj)*vel_0
machwind = mach(rbyrInj)
Tempwind = (prswind/rhowind)*mu*mp/kB

chi = Tempwind/Tcl
# Rgo  = 2 * (Tcl/1e4)**(5/2)*machwind/(((prswind/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
Rgo  = 10.378 * (Tcl/1e4)**(5/2)*machwind/(((prswind/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.29) ) * (chi/100) * (alpha**-1) # pc

Rcl_min = Rgo # pc from vanilla CC
Rcl_max = rbyrInj*Rinj/200 # pc not yet known
Rcl_dest = rbyrInj*Rinj/100 # pc not yet known

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

fig = plt.figure(figsize=(15, 12))
plt.semilogy(rbyrInj, Rcl_min, color="tab:blue", label=r"$R_{cl,min}$", alpha=0.7)
plt.semilogy(rbyrInj, Rcl_max, color="tab:red", label=r"$R_{cl,max}=r_{ini}/200$", alpha=0.7)
plt.semilogy(rbyrInj, Rcl_dest, color="tab:red", linestyle=":", label=r"$R_{cl,dest}=r_{ini}/100$", alpha=0.7)

secax = plt.gca().secondary_xaxis('top',
                                  functions=(
                                  interp1d(rbyrInj, mach(rbyrInj), fill_value='extrapolate'),
                                  interp1d(mach(rbyrInj), rbyrInj, fill_value='extrapolate')))
secax.set_xlabel(r"$\mathcal{M}$")
'''
secay = plt.gca().secondary_yaxis('right',
                                  functions=(
                                  interp1d(Temperature, Temperature/(Tcl/1e6), fill_value='extrapolate'),
                                  interp1d(Temperature/(Tcl/1e6), Temperature, fill_value='extrapolate')))
secay.set_ylabel(r"$\chi$")
'''
# Simulation params
Mach_ini = 1.385
Rini = relpos_mach(Mach_ini) * Rinj # pc
RinibyRcl   = np.array([23.382, 31.176, 77.941, 116.911, 202.646, 311.763, 974.260])
tcoolmBytcc = np.array([0.06,   0.08,   0.20,   0.30,    0.52,    0.80,    2.5    ])
status      =          ['P',    'D',    'P',    'D',     'G',     'P',     'D']
Rcl = Rini/RinibyRcl # pc

cond = np.logical_and(rbyrInj>=1.0, Rcl_max>=Rcl_min)
plt.fill_between(rbyrInj[cond], Rcl_min[cond], Rcl_max[cond], color="gray", alpha=0.5)

for i, txt in enumerate(tcoolmBytcc):
    color = "tab:red" if status[i]=='D' else "darkgreen"
    if status[i]=='P': color="tab:gray"
    plt.scatter([relpos_mach(Mach_ini),], Rcl[i], s=35, marker="x", color=color)
    plt.gca().annotate(f"{str(txt)}, {status[i]}",
                       ((relpos_mach(Mach_ini)+0.03)*np.ones_like(Rcl)[i], Rcl[i]),
                       size=18, weight="bold",
                       color = color)
plt.legend(loc="best")
plt.xlabel(r"$r/r_{inj}$")
plt.ylabel(r"Growing cloud size (pc)")
plt.title(r"$(\dot{E}, \dot{M}, r_{inj})$ = (%.2e, %.1f, %.1f)"%(Edot, Mdot, Rinj))
plt.savefig("growth-size.png")
plt.close()
