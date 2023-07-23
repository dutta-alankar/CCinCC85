# -*- coding: utf-8 -*-
"""
Created on Mon Jun 01 00:58:56 2022

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

relpos = interp1d(mach, rnorm) #inverting the Mach relation

rhonorm = interp1d(rnorm, wind[:,1])
prsnorm = interp1d(rnorm, wind[:,2])
velnorm = interp1d(rnorm, wind[:,3])

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

# Max's parameters
chi = 100
Mw = 1.5
tcoolmBytcc = 0.08
Tcl = 4e4 # K
RinibyRcl = np.arange(40, 230, 30)

PinibykB = np.logspace(2.8, 6.2, 100) # Kcm^-3, degenerate

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
Rini = np.array([RinibyRcl[i]*Rcl for i in range(RinibyRcl.shape[0])]) # pc
Rinj = np.array([Rini[i,:]/RinibyRinj for i in range(RinibyRcl.shape[0])])  # pc

Mdot = np.array([((Pw/prsTini) * (vw/velTini)**(-1) *(Rinj[i,:]*pc)**2) / (MSun/yr) for i in range(RinibyRcl.shape[0])])
Edot = np.array([((Pw/prsTini) * (vw/velTini) *(Rinj[i,:]*pc)**2) for i in range(RinibyRcl.shape[0])])  #erg s^-1

# Equivalent alternate expression
# Mdot = ((rhow/rhoTini)* (vw/velTini) *(Rinj*pc)**2) / (MSun/yr)
# Edot = ((rhow/rhoTini) * (vw/velTini)**3 *(Rinj*pc)**2) #erg s^-1

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

fig = plt.figure(figsize=(13, 10))
plt.loglog(PinibykB, Rcl, color="tab:red") # idependent of RinibyRcl
plt.xlabel(r"$P_{ini}/k_B\ (K cm^{-3})$")
plt.ylabel(r"$R_{cl}$ (pc)")
plt.title(r"$(\mathcal{M}, \chi, t_{cool,mix}/t_{cc}, T_{cl})$ = (%.1f, %d, %.2f, %.1e)"%(Mw, chi, tcoolmBytcc, Tcl))
plt.savefig("prs-Rcl.png")
plt.close()

colors = plt.cm.magma(RinibyRcl)

fig = plt.figure(figsize=(14, 12))
for i in range(RinibyRcl.shape[0]):
    plt.loglog(PinibykB, Rini[i,:],
             label=r"$r_{ini}/R_{cl}$=%d"%RinibyRcl[i],
             color=colors[i])
secax = plt.gca().secondary_xaxis('top',
                                  functions=(
                                  interp1d(PinibykB, Rcl, fill_value='extrapolate'),
                                  interp1d(Rcl, PinibykB, fill_value='extrapolate')))
secax.set_xlabel(r"$R_{cl}$ (pc)")

secay = plt.gca().secondary_yaxis('right',
                                  functions=(
                                  interp1d(Rini[0,:], Rini[0,:]/RinibyRinj, fill_value='extrapolate'),
                                  interp1d(Rini[0,:]/RinibyRinj, Rini[0,:], fill_value='extrapolate')))
secay.set_ylabel(r"$R_{inj}$ (pc)")

plt.xlabel(r"$P_{ini}/k_B\ (K cm^{-3})$")
plt.ylabel(r"$R_{ini}$ (pc)")
plt.title(r"$(\mathcal{M}, \chi, t_{cool,mix}/t_{cc}, T_{cl})$ = (%.1f, %d, %.2f, %.1e)"%(Mw, chi, tcoolmBytcc, Tcl))
plt.legend(loc="best")
plt.savefig("prs-Rini-Rinj.png")
plt.close()

fig = plt.figure(figsize=(13, 10))
for i in range(RinibyRcl.shape[0]):
    plt.loglog(PinibykB, Edot[i,:],
               label=r"$r_{ini}/R_{cl}$=%d"%RinibyRcl[i],
               color=colors[i])
plt.xlabel(r"$P_{ini}/k_B\ (K cm^{-3})$")
plt.ylabel(r"Edot ($erg s ^{-1}$)")
plt.title(r"$(\mathcal{M}, \chi, t_{cool,mix}/t_{cc}, T_{cl})$ = (%.1f, %d, %.2f, %.1e)"%(Mw, chi, tcoolmBytcc, Tcl))
plt.legend(loc="best")
plt.savefig("prs-Edot.png")
plt.close()

fig = plt.figure(figsize=(13, 10))
for i in range(RinibyRcl.shape[0]):
    plt.loglog(PinibykB, Mdot[i,:],
               label=r"$r_{ini}/R_{cl}$=%d"%RinibyRcl[i],
               color=colors[i])
plt.xlabel(r"$P_{ini}/k_B\ (K cm^{-3})$")
plt.ylabel(r"Mdot ($M_{\odot} yr ^{-1}$)")
plt.title(r"$(\mathcal{M}, \chi, t_{cool,mix}/t_{cc}, T_{cl})$ = (%.1f, %d, %.2f, %.1e)"%(Mw, chi, tcoolmBytcc, Tcl))
plt.legend(loc="best")
plt.savefig("prs-Mdot.png")
plt.close()
