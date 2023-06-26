# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:54:56 2022

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d
import h5py
import matplotlib.pyplot as plt
import sys
from matplotlib import colors

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

'''
# Max's parameters
chi = 100
Mw = 1.5
tcoolmBytcc = 0.08
Tcl = 4e4 # K
RinibyRcl = 200

PinibykB = 1.0e+06 # Kcm^-3, degenerate
'''
# New parameters
chi = 100
Mw = 1.8
tcoolmBytcc = 0.1
Tcl = 4e4 # K
RinibyRcl = 40

PinibykB = 2.5e5 # Kcm^-3, degenerate


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

data_dir = "../../output"

file_no = int(sys.argv[1])
data = h5py.File(f"{data_dir}/data.{file_no:04d}.flt.h5", "r")
x = np.array(data["/cell_coords/X"]).flatten()
y = np.array(data["/cell_coords/Y"]).flatten()
z = np.array(data["/cell_coords/Z"]).flatten()

vx = np.array(data[f"/Timestep_{file_no}/vars/vx1"]).flatten()
vy = np.array(data[f"/Timestep_{file_no}/vars/vx2"]).flatten()
vz = np.array(data[f"/Timestep_{file_no}/vars/vx3"]).flatten()

distance = (np.sqrt(x**2 +y**2 +z**2)*UNIT_LENGTH/pc)/(Rinj*pc/pc)
density  = np.array(data[f"/Timestep_{file_no}/vars/density"]).flatten()*UNIT_DENSITY/((Edot**(-1/2.))*((Mdot*(MSun/yr))**(3/2.))*((Rinj*pc)**-2))
pressure = np.array(data[f"/Timestep_{file_no}/vars/pressure"]).flatten()*(UNIT_DENSITY*UNIT_VELOCITY**2)/((Edot**(1/2.))*((Mdot*(MSun/yr))**(1/2.))*((Rinj*pc)**-2))
velocity = np.sqrt(vx**2 + vy**2 + vz**2)*UNIT_VELOCITY/((Edot**(1/2.))*((Mdot*(MSun/yr))**(-1/2.)))
cell_vol = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()

plt.hist2d(np.log10(distance), np.log10(density), bins=(100,100), weights=cell_vol, density=True, norm=colors.LogNorm()) #, range=[[np.min(np.log10(distance))]])
plt.plot(np.log10(rnorm), np.log10(wind[:,1]), color="tab:red", linewidth=2, alpha=0.6)
plt.colorbar()
plt.savefig("density.png")
plt.close()

plt.hist2d(np.log10(distance), np.log10(pressure), bins=(100,100), weights=cell_vol, density=True, norm=colors.LogNorm())
plt.plot(np.log10(rnorm), np.log10(wind[:,2]), color="tab:red", linewidth=2, alpha=0.6)
plt.colorbar()
plt.savefig("pressure.png")
plt.close()

plt.hist2d(np.log10(distance), velocity, bins=(100,100), weights=cell_vol, density=True, norm=colors.LogNorm())
plt.plot(np.log10(rnorm), wind[:,3], color="tab:red", linewidth=2, alpha=0.6)
plt.colorbar()
plt.savefig("velocity.png")
plt.close()

data.close()

