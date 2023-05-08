# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:54:56 2022

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d

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

LAMBDA = np.loadtxt('../../cooltable.dat')
LAMBDA = interp1d(LAMBDA[:,0], LAMBDA[:,1], fill_value='extrapolate')

'''
# Max's parameters
chi = 100
Mw = 1.5
tcoolmBytcc = 0.08
RinibyRcl = 200
Tcl = 4e4 #K

PinibykB = 1e3 #Kcm^-3, degenerate

# Our model params
chi = 1143
Mw = 4.993191399557429
tcoolmBytcc = 0.003304105670882433
RinibyRcl = 625/75
Tcl = 1e4 #K
PinibykB = 419955.6141084651 #Kcm^-3
'''
# New parameters
chi = 100
Mw = 1.8
tcoolmBytcc = 0.1
Tcl = 4e4 # K
RinibyRcl = 40

PinibykB = 2.5e5 # Kcm^-3, degenerate

Rgo  = 2 * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) #pc
Rcl  = (tcoolmBytcc**-1) *Rgo # pc
Rini = RinibyRcl*Rcl # pc

UNIT_LENGTH   = Rcl*pc
UNIT_DENSITY  = (PinibykB/(chi*Tcl))*mu*mp
UNIT_VELOCITY = Mw*np.sqrt(gamma*chi*kB*Tcl/(mu*mp))

definitions = \
f'''
#define  PHYSICS                        HD
#define  DIMENSIONS                     3
#define  COMPONENTS                     3
#define  GEOMETRY                       SPHERICAL
#define  BODY_FORCE                     NO
#define  FORCED_TURB                    NO
#define  COOLING                        TABULATED
#define  RECONSTRUCTION                 LINEAR
#define  TIME_STEPPING                  RK2
#define  DIMENSIONAL_SPLITTING          NO
#define  NTRACER                        1
#define  USER_DEF_PARAMETERS            6

/* -- physics dependent declarations -- */

#define  EOS                            IDEAL
#define  ENTROPY_SWITCH                 NO
#define  THERMAL_CONDUCTION             NO
#define  VISCOSITY                      NO
#define  ROTATING_FRAME                 NO
#define  PARTICLES                      NO
#define  INTERNAL_BOUNDARY              YES
#define  SHOW_TIMING                    NO
#define  SHOW_TIME_STEPS                YES
#define  TRACKING                       YES

/* -- user-defined parameters (labels) -- */

#define  RINI                           0
#define  THINI                          1
#define  PHIINI                         2
#define  CHI                            3
#define  MACH                           4
#define  ZMET                           5

/* [Beg] user-defined constants (do not change this line) */

#define  UNIT_DENSITY                   {UNIT_DENSITY:<10.4e}
#define  UNIT_LENGTH                    {UNIT_LENGTH:<10.4e}
#define  UNIT_VELOCITY                  {UNIT_VELOCITY:<10.4e}

/* [End] user-defined constants (do not change this line) */
#define  MULTIPLE_LOG_FILES             YES
#define  VERBOSE                        NO
#define  CUTOFF                         NO
'''

definitions = definitions[1:]

if __name__ == '__main__':
    with open("../../definitions.h", "w") as text_file:
        text_file.write(definitions)
    print('Rcl = %.1f pc'%Rcl)
