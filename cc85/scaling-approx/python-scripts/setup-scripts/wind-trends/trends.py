# -*- coding: utf-8 -*-
"""
Created on Fri May 26 00:08:30 2023

@author: alankar
"""

import numpy as np
from scipy.interpolate import interp1d
from typing import Tuple
import matplotlib
import matplotlib.pyplot as plt
import os

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = True
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 0.8
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 0.6
matplotlib.rcParams["xtick.major.width"] = 0.6
matplotlib.rcParams["ytick.minor.width"] = 0.45
matplotlib.rcParams["xtick.minor.width"] = 0.45
matplotlib.rcParams["ytick.major.size"] = 4.0
matplotlib.rcParams["xtick.major.size"] = 4.0
matplotlib.rcParams["ytick.minor.size"] = 2.0
matplotlib.rcParams["xtick.minor.size"] = 2.0
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


gamma = 5/3
alpha = 1.0

wind = np.loadtxt('../../../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]

rhonorm = interp1d(rnorm, wind[:,1])
prsnorm = interp1d(rnorm, wind[:,2])
velnorm = interp1d(rnorm, wind[:,3])

LAMBDA = np.loadtxt('../../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

def generate_wind_props( chi: float,
                         Mw: float,
                         tcoolmBytcc: float,
                         Tcl: float,
                         RinibyRcl: float,
                         PinibykB: float ) -> Tuple[float]:
    relpos = interp1d(mach, rnorm) #inverting the Mach relation
    Tw = chi*Tcl
    Pw = PinibykB*kB
    rhow = (PinibykB/Tw)*(mu*mp)
    vw   = Mw*np.sqrt(gamma*kB*Tw/(mu*mp))
    RinibyRinj = relpos(Mw)
    rhoTini = rhonorm(RinibyRinj)
    prsTini = prsnorm(RinibyRinj)
    velTini = velnorm(RinibyRinj)

    Rgo  = 2 * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
    Rcl  = (tcoolmBytcc**-1) * Rgo # pc
    Rini = RinibyRcl*Rcl # pc
    Rinj = Rini/RinibyRinj # pc

    Mdot = ((Pw/prsTini)* (vw/velTini)**(-1) *(Rinj*pc)**2) / (MSun/yr)
    Edot = ((Pw/prsTini) * (vw/velTini) *(Rinj*pc)**2) #erg s^-1

    # Equivalent alternate expression
    # Mdot = ((rhow/rhoTini)* (vw/velTini) *(Rinj*pc)**2) / (MSun/yr)
    # Edot = ((rhow/rhoTini) * (vw/velTini)**3 *(Rinj*pc)**2) #erg s^-1

    # sanity = (rhow/rhoTini)/((Pw/prsTini)*(vw/velTini)**-2)

    print('Mdot = %.2e MSun/yr'%Mdot)
    print('Edot = %.2e erg/s'%Edot)
    print('R_inj = %.2e pc'%(Rinj*pc/pc))
    print('R_ini = %.2e pc'%(Rini*pc/pc))
    print('R_cl = %.2e pc'%(Rcl*pc/pc))
    print('R_go = %.2e pc'%Rgo)
    print('T_cl = %.2e K'%Tcl)

    if (Rini-Rcl)<Rinj:
        print("Problem!")
    else:
        print("Left room = %.1f R_cl"%((Rini-Rinj)/Rcl))

    return (Mdot, Edot, Rinj, Rini, Rcl, Rgo)

# Free parameters
chi = 1000
Mw = 1.5
tcoolmBytcc = 0.08
Tcl = 4e4 # K
RinibyRcl = 2000

PinibykB = np.array([1.0e+03, 1.0e+04, 1.0e+05, 1.0e+06, 1.0e+07, 1.0e+08,]) # Kcm^-3, degenerate

Mdot = np.zeros_like(PinibykB)
Edot = np.zeros_like(PinibykB)
Rinj = np.zeros_like(PinibykB)
Rini = np.zeros_like(PinibykB)
Rcl  = np.zeros_like(PinibykB)
Rgo  = np.zeros_like(PinibykB)

directory = f"chi{chi:d}_M{Mw:.1f}_tcmtcc{tcoolmBytcc:.2f}_RiniRcl{RinibyRcl:d}_Tcl{Tcl:.1e}"
os.makedirs(directory, exist_ok=True)

for indx, prs in enumerate(PinibykB):
    Mdot[indx], Edot[indx], Rinj[indx], Rini[indx], Rcl[indx], Rgo[indx] = generate_wind_props( chi, Mw, tcoolmBytcc, Tcl, RinibyRcl, prs )

plt.figure(figsize=(13,10))
with plt.style.context('dark_background'):
    plt.title(r"$\chi = %d,\ \mathcal{M} = %.1f,\ t_{cool,mix}/t_{cc}=%.2f,\ R_{ini}/R_{cl}=%d,\ T_{cl}=%.1e K$"
              %(chi, Mw, tcoolmBytcc, RinibyRcl, Tcl))
    plt.loglog(PinibykB, Mdot)

plt.ylabel(r"$\dot{M}\ (M_{\odot} yr ^{-1})$")
plt.xlabel(r"$P/k_B\ (K cm ^{-3})$")
plt.savefig(f"{directory}/trends-mass.png", transparent=True)

plt.figure(figsize=(13,10))
with plt.style.context('dark_background'):
    plt.title(r"$\chi = %d,\ \mathcal{M} = %.1f,\ t_{cool,mix}/t_{cc}=%.2f,\ R_{ini}/R_{cl}=%d,\ T_{cl}=%.1e K$"
              %(chi, Mw, tcoolmBytcc, RinibyRcl, Tcl))
    plt.loglog(PinibykB, Edot)

plt.ylabel(r"$\dot{E}\ (erg s ^{-1})$")
plt.xlabel(r"$P/k_B\ (K cm ^{-3})$")
plt.savefig(f"{directory}/trends-energy.png", transparent=True)

plt.figure(figsize=(13,10))
with plt.style.context('dark_background'):
    plt.title(r"$\chi = %d,\ \mathcal{M} = %.1f,\ t_{cool,mix}/t_{cc}=%.2f,\ R_{ini}/R_{cl}=%d,\ T_{cl}=%.1e K$"
              %(chi, Mw, tcoolmBytcc, RinibyRcl, Tcl))
    plt.loglog(PinibykB, Rinj)

plt.ylabel(r"$R_{inj}\ (pc)$")
plt.xlabel(r"$P/k_B\ (K cm ^{-3})$")
plt.savefig(f"{directory}/trends-inj.png", transparent=True)

plt.figure(figsize=(13,10))
with plt.style.context('dark_background'):
    plt.title(r"$\chi = %d,\ \mathcal{M} = %.1f,\ t_{cool,mix}/t_{cc}=%.2f,\ R_{ini}/R_{cl}=%d,\ T_{cl}=%.1e K$"
              %(chi, Mw, tcoolmBytcc, RinibyRcl, Tcl))
    plt.loglog(PinibykB, Rcl)

plt.ylabel(r"$R_{cl}\ (pc)$")
plt.xlabel(r"$P/k_B\ (K cm ^{-3})$")
plt.savefig(f"{directory}/trends-cloud.png", transparent=True)

'''
UNIT_LENGTH   = Rcl* pc
UNIT_DENSITY  = rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2)
UNIT_VELOCITY = velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)
'''
