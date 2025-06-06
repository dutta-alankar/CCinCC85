import numpy as np
from scipy.interpolate import interp1d

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

cool = np.loadtxt("../../cooltable.dat")
gamma = 5./3
PiniBkB = 1.0e+03
Tcl = 1.0e+04
chi = 100
mach = 1.0
LAMBDA = interp1d(cool[:,0], cool[:,1])

Rthres = (kB*Tcl**2/(gamma-1))/PiniBkB*chi*mach/(mu*Xp)**2*np.sqrt(gamma*kB*Tcl/(mu*mp))/pc/LAMBDA(np.sqrt(chi)*Tcl)
print("R_thres = %.3f pc"%Rthres)
