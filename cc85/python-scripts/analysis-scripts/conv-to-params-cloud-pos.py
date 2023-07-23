# -*- coding: utf-8 -*-
"""
Created on Mon Jul 02 00:59:56 2023

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

rhonorm  = interp1d(rnorm, wind[:,1])
prsnorm  = interp1d(rnorm, wind[:,2])
velnorm  = interp1d(rnorm, wind[:,3])
Tempnorm = lambda rnorm:prsnorm(rnorm)/rhonorm(rnorm)

relpos = interp1d(mach, rnorm) #inverting the Mach relation

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

Edot = 2.0e+41 # 1.5e+42 # erg/s
Mdot = 1.33    # MSun/yr
Rinj = 300     # pc

Tcl         = 4.0e+4
chi         = 100
Mach_ini    = 1.5
RinibyRcl   = np.linspace(40, 200, 100)

RinibyRinj = relpos(Mach_ini)
Rini       = RinibyRinj*Rinj # pc
Rcl        = Rini/RinibyRcl[20]  # pc This is the fixed Rcl

rho_0 = ((Mdot*(MSun/yr))**1.5)  * (Edot**-0.5) * ((Rinj*pc)**-2)
prs_0 = ((Mdot*(MSun/yr))**0.5)  * (Edot**0.5)  * ((Rinj*pc)**-2)
vel_0 = ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)
'''
Twindnorm_ini = Twind_ini/((prs_0/rho_0)*mu*mp/kB)

prswind_ini = prsnorm(RinibyRinj)*prs_0
rhowind_ini = rhonorm(RinibyRinj)*rho_0
velwind_ini = velnorm(RinibyRinj)*vel_0

Rgo  = 2 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
tcoolmbytcc  = Rgo/Rcl # pc

print(f"chi = {chi:d}")
print(f"Mw  = {Mach_ini:.3f}")
print(f"tcoolmBytcc = {tcoolmbytcc:.2f}")
print(f"RinibyRcl = {RinibyRcl:.3f}")
print(f"T_cl = {Tcl:.1e} K")
print(f"PinibykB = {prswind_ini/kB:.3e} K cm^-3")
print(f"RinibyRinj = {RinibyRinj:.2f}")
print(f"R_cl = {Rcl:.1f} pc")
print(f"R_ini = {Rini:.1f} pc")
print(f"R_go  = {Rgo:.1f} pc")
print(f"Mdot = {Mdot:.2e} MSun/yr")
print(f"Edot = {Edot:.2e} erg/s'%")
'''

Rini  = RinibyRcl*Rcl # pc
RinibyRinj  = Rini/Rinj
Mach_ini    = interp1d(rnorm, mach)(RinibyRinj)
prswind_ini = prsnorm(RinibyRinj)*prs_0
rhowind_ini = rhonorm(RinibyRinj)*rho_0
velwind_ini = velnorm(RinibyRinj)*vel_0
Twind_ini   = Tempnorm(RinibyRinj)*((prs_0/rho_0)*mu*mp/kB)

chi = Twind_ini/Tcl
Rgo  = 2 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
tcoolmbytcc  = Rgo/Rcl # pc

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

fig = plt.figure(figsize=(13, 10))
plt.plot(RinibyRcl, Mach_ini, color="tab:red")
plt.xlabel(r"$r_{ini}/R_{cl}$")
plt.ylabel(r"$\mathcal{M}$")
plt.title(r"Rcl = %.1f pc"%Rcl)
plt.savefig("cloud-pos-mach.png")
plt.close()

fig = plt.figure(figsize=(13, 10))
plt.plot(RinibyRcl, chi, color="tab:red")
plt.xlabel(r"$r_{ini}/R_{cl}$")
plt.ylabel(r"$\chi$")
plt.title(r"Rcl = %.1f pc"%Rcl)
plt.savefig("cloud-pos-chi.png")
plt.close()

fig = plt.figure(figsize=(16, 12))
plt.semilogy(RinibyRcl, tcoolmbytcc, color="tab:red")
secax = plt.gca().secondary_xaxis('top',
                                  functions=(
                                  interp1d(RinibyRcl, Mach_ini, fill_value='extrapolate'),
                                  interp1d(Mach_ini,  RinibyRcl, fill_value='extrapolate')))
secax.set_xlabel(r"$\mathcal{M}$")
secay = plt.gca().secondary_yaxis('right',
                                  functions=(
                                  interp1d(tcoolmbytcc, chi, fill_value='extrapolate'),
                                  interp1d(chi,  tcoolmbytcc, fill_value='extrapolate')))
secay.set_ylabel(r"$\chi$")


plt.xlabel(r"$r_{ini}/R_{cl}$")
plt.ylabel(r"$t_{cool,mix}/t_{cc}$")
plt.title(r"Rcl = %.1f pc"%Rcl)
plt.savefig("cloud-pos-tcoolmbytcc.png")
plt.close()
