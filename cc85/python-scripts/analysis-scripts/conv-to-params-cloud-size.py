# -*- coding: utf-8 -*-
"""
Created on Mon Jul 01 13:54:56 2023

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib
import sys

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
'''
# Param set 1
Edot = 3.00e+41  # erg/s
Mdot = 2.00      # MSun/yr
Rinj = 200       # pc
'''
# Param set 2
Edot = 1.00e+42  # erg/s
Mdot = 5.00      # MSun/yr
Rinj = 300       # pc

Tcl         = 4.0e+04 # K
tcoolmbytcc = float(sys.argv[1])
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

# Rgo  = 2 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc 1.97
Rgo  = 10.378 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.29) ) * (chi/100) * (alpha**-1) # pc
Rcl  = Rgo/tcoolmbytcc # pc
# dummy = (np.sqrt(gamma)/(gamma-1))*((kB**(3/2.))/np.sqrt(mu*mp)) * 1.0 * ((1e4)**(5/2.)) / ( (1e3) * LAMBDA(np.sqrt(100)*1e4) ) * 100 * (1.0**(-1))
# print("dummy ",  dummy/pc )
# print("dummy L", np.log10(LAMBDA(np.sqrt(100)*1e4)) )

RinibyRcl = Rini/Rcl

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
print(f"(R_ini-2R_cl - R_inj)/R_cl = {((Rini-2*Rcl-Rinj)/Rcl):.1f} (thres 1.0)")
print(f"(R_ini - R_inj)/R_cl = {((Rini-Rinj)/Rcl):.1f} (thres 2.0)")

'''
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
radius = np.linspace(1,3.5, 100)*Rinj
Temperature = (prsnorm(radius/Rinj)*prs_0)/(rhonorm(radius/Rinj)*rho_0)*mu*mp/kB # K
plt.plot(radius, Temperature/1e6, color="tab:red")
secax = plt.gca().secondary_xaxis('top',
                                  functions=(
                                  interp1d(radius, radius/Rcl, fill_value='extrapolate'),
                                  interp1d(radius/Rcl, radius, fill_value='extrapolate')))
secax.set_xlabel(r"$r/R_{cl}$")
secay = plt.gca().secondary_yaxis('right',
                                  functions=(
                                  interp1d(Temperature, Temperature/(Tcl/1e6), fill_value='extrapolate'),
                                  interp1d(Temperature/(Tcl/1e6), Temperature, fill_value='extrapolate')))
secay.set_ylabel(r"$\chi$")
plt.xlabel(r"Distance (pc)")
plt.ylabel(r"Temperature $\times 10^6$ (K)")
plt.title(r"$(\mathcal{M}, \chi, T_{cl})$ = (%.1f, %d, %.1e)"%(Mach_ini, chi, Tcl))
plt.savefig("cloud-size-Temp-prof.png")
plt.close()

tcoolmbytcc = np.logspace(-2, 0, 100)
Rcl  = Rgo/tcoolmbytcc # pc
RinibyRcl = Rini/Rcl

fig = plt.figure(figsize=(13, 10))
plt.loglog(tcoolmbytcc, RinibyRcl, color="tab:red")
secay = plt.gca().secondary_yaxis('right',
                                  functions=(
                                  interp1d(RinibyRcl, Rcl, fill_value='extrapolate'),
                                  interp1d(Rcl, RinibyRcl, fill_value='extrapolate')))
secay.set_ylabel(r"$R_{cl}$")
plt.xlabel(r"$t_{cool,mix}/t_{cc}$")
plt.ylabel(r"$r_{ini}/R_{cl}$")
plt.title(r"$(\mathcal{M}, \chi, T_{cl})$ = (%.1f, %d, %.1e)"%(Mach_ini, chi, Tcl))
plt.vlines(x=0.3, ymin=np.min(RinibyRcl), ymax=np.max(RinibyRcl), color="black", linestyle=":")
# plt.hlines(y=200, xmin=np.min(tcoolmbytcc), xmax=np.max(tcoolmbytcc), color="black", linestyle=":")
plt.hlines(y=100, xmin=np.min(tcoolmbytcc), xmax=np.max(tcoolmbytcc), color="black", linestyle=":")
plt.savefig("cloud-size.png")
plt.close()
'''
