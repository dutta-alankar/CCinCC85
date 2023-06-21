# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:54:56 2022

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

wind = np.loadtxt('../CC85_steady-prof_gamma_1.667.txt', skiprows=1)
mach = wind[:,3]/np.sqrt(gamma*wind[:,2]/wind[:,1])
rnorm = wind[:,0]

relpos = interp1d(mach, rnorm) #inverting the Mach relation

rhonorm = interp1d(rnorm, wind[:,1])
prsnorm = interp1d(rnorm, wind[:,2])
velnorm = interp1d(rnorm, wind[:,3])

LAMBDA = np.loadtxt('../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

# New parameters
chi = 100
Mw = 1.5
tcoolmBytcc = 0.08
Tcl = 4e4 # K
RinibyRcl = 200

PinibykB = 1.0e+06 # Kcm^-3, degenerate

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

sanity = (rhow/rhoTini)/((Pw/prsTini)*(vw/velTini)**-2)

print('Mdot = %.2e MSun/yr'%Mdot)
print('Edot = %.2e erg/s'%Edot)
print('R_inj = %.2e pc'%(Rinj*pc/pc))
print('R_ini = %.2e pc'%(Rini*pc/pc))
print('R_cl = %.2e pc'%(Rcl*pc/pc))
print('R_go = %.2e pc'%Rgo)
print('T_cl = %.2e K'%Tcl)

UNIT_LENGTH   = Rcl* pc
UNIT_DENSITY  = rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2)
UNIT_VELOCITY = velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

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

file_no= 0
scaling_data = "../scaling-approx/output/analysis.dat"
dummy_cloud_data = f"../dummy-cloud/output/data.{file_no:04d}.tab"

scaling_data = np.loadtxt(scaling_data)
dummy_cloud_data = np.loadtxt(dummy_cloud_data)

radius_by_Rcl  = np.linspace(RinibyRcl-10, 700, 50)
radius_by_Rinj = radius_by_Rcl*Rcl/Rinj
cc85_profile_T = (prsnorm(radius_by_Rinj)/rhonorm(radius_by_Rinj))*(mu*mp/kB)*(Edot/(Mdot*MSun/yr))

plt.figure(figsize=(13,10))
plt.plot(scaling_data[:,1], scaling_data[:,17]/1e6, label="scaling setup")
plt.plot(dummy_cloud_data[:,0], dummy_cloud_data[:,8]/1e6, label="spherical setup")
plt.plot(radius_by_Rcl, cc85_profile_T/1e6, 'o', label="CC85 solution")
plt.plot(radius_by_Rcl, Tw*(RinibyRcl/radius_by_Rcl)**(2*(gamma-1))/1e6, 'o', label="asymptotic solution")

plt.xlim(xmin=RinibyRcl-15)
plt.legend(loc="best")
plt.xlabel(r"$r/R_{cl}$")
plt.ylabel(r"Temperature $(\times 10^6\ K)$")
plt.savefig("compare-setups.png")

temperature_dummy_cloud = (prsnorm(radius_by_Rinj)/rhonorm(radius_by_Rinj))*(mu*mp/kB)*(Edot/(Mdot*MSun/yr))
temperaure_scaling = (prsnorm(RinibyRinj)/rhonorm(RinibyRinj))*(mu*mp/kB)*(Edot/(Mdot*MSun/yr)) * ((radius_by_Rinj/RinibyRinj)**(-2*(gamma-1)))

ndens_dummy_cloud = rhonorm(radius_by_Rinj)* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2) / (mu*mp)
ndens_scaling =  rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2) * ((radius_by_Rinj/RinibyRinj)**-2) / (mu*mp)

tcool_dummy_cloud = (1./(gamma-1))*kB*temperature_dummy_cloud/(ndens_dummy_cloud*LAMBDA(temperature_dummy_cloud))
tcool_scaling = (1./(gamma-1))*kB*temperaure_scaling/(ndens_scaling*LAMBDA(temperaure_scaling))

tadv_dummy_cloud = radius_by_Rcl*Rcl*pc/(velnorm(radius_by_Rinj)* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5))
tadv_scaling = radius_by_Rcl*Rcl*pc/(velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5))

plt.figure(figsize=(13,10))
plt.plot(radius_by_Rcl, tcool_scaling/tadv_scaling, label="scaling setup")
plt.plot(radius_by_Rcl, tcool_dummy_cloud/tadv_dummy_cloud, label="spherical setup")

plt.xlim(xmin=RinibyRcl-15)
plt.legend(loc="best")
plt.xlabel(r"$r/R_{cl}$")
plt.ylabel(r"$t_{cool}/t_{adv}$")
plt.savefig("compare-tcoolBytadv.png")
