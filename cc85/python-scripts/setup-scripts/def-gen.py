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
RinibyRcl = 40

PinibykB = 1.0e+06 # 2.5e+05 # Kcm^-3, degenerate


# New parameters
chi = 100
Mw = 1.8
tcoolmBytcc = 0.1
Tcl = 4e4 # K
RinibyRcl = 40

PinibykB = 2.5e+05 # Kcm^-3, degenerate
'''

# From dimensional parameters
chi = 100
Mw = 1.496
tcoolmBytcc = 0.80
Tcl = 4.0e+04 # K
RinibyRcl = 282.684

PinibykB = 2.020e+06 # Kcm^-3, degenerate

Tw = chi*Tcl
Pw = PinibykB*kB
rhow = (PinibykB/Tw)*(mu*mp)
vw   = Mw*np.sqrt(gamma*kB*Tw/(mu*mp))
RinibyRinj = relpos(Mw)
rhoTini = rhonorm(RinibyRinj)
prsTini = prsnorm(RinibyRinj)
velTini = velnorm(RinibyRinj)

# Rgo  = 2 * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
# Rgo  = (1.97) * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.29) ) * (chi/100) * (alpha**-1) # pc
Rgo  = 10.378 * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.29) ) * (chi/100) * (alpha**-1) # pc
Rcl  = (tcoolmBytcc**-1) * Rgo # pc
Rini = RinibyRcl*Rcl # pc
Rinj = Rini/RinibyRinj # pc

Mdot = ((Pw/prsTini)* (vw/velTini)**(-1) *(Rinj*pc)**2) / (MSun/yr)
Edot = ((Pw/prsTini) * (vw/velTini) *(Rinj*pc)**2) #erg s^-1

# Equivalent alternate expression
# Mdot = ((rhow/rhoTini)* (vw/velTini) *(Rinj*pc)**2) / (MSun/yr)
# Edot = ((rhow/rhoTini) * (vw/velTini)**3 *(Rinj*pc)**2) #erg s^-1

sanity = (rhow/rhoTini)/((Pw/prsTini)*(vw/velTini)**-2)

print('M_ini = %.3f'%Mw)
print('Mdot = %.2e MSun/yr'%Mdot)
print('Edot = %.2e erg/s'%Edot)
print('R_inj = %.2e pc'%(Rinj*pc/pc))
print('R_ini = %.2e pc'%(Rini*pc/pc))
print('R_cl = %.2e pc'%(Rcl*pc/pc))
print('R_go = %.2e pc'%Rgo)
print('T_cl = %.2e K'%Tcl)
print('R_ini/R_inj = %.2f'%(Rini/Rinj))
print('R_inj/R_cl = %.2f'%(Rinj/Rcl))

UNIT_LENGTH   = Rcl* pc
UNIT_DENSITY  = rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2)
UNIT_VELOCITY = velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

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
#define  USER_DEF_PARAMETERS            7

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
#define  WIND_TEST                      NO

/* -- user-defined parameters (labels) -- */

#define  RINI                           0
#define  THINI                          1
#define  PHIINI                         2
#define  CHI                            3
#define  MACH                           4
#define  ZMET                           5
#define  BUFFER_TRACK                   6

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

nl  = "\\n"
tab = "\\t"

info_code = f"""
void write_info (char* filename) {{
  if (prank!=0) return;
  FILE *fp;
  sprintf (filename, "%s/%s", RuntimeGet()->output_dir, filename);
  fp = fopen(filename,"w"); /* from beginning */
  fprintf (fp,"id: growth_test{nl}");
  fprintf (fp,"paths:{nl}- {{root}}/%s{nl}", RuntimeGet()->output_dir);
  fprintf (fp,"simulation attributes:{nl}");
  #if COOLING != NO
  fprintf (fp,"{tab}has_cooling: yes{nl}");
  #else
  fprintf (fp,"{tab}has_cooling: no{nl}");
  #endif
  #if GEOMETRY == SPHERICAL
  fprintf (fp,"{tab}geometry: spherical{nl}");
  #elif GEOMETRY == CARTESIAN
  fprintf (fp,"{tab}geometry: cartesian{nl}");
  #elif GEOMETRY == POLAR
  fprintf (fp,"{tab}geometry: polar{nl}");
  #else
  printLog("Unsupported Geometry!{nl}");
  QUIT_PLUTO(1);
  #endif
  fprintf (fp,"{tab}dimensioality: %d{nl}", DIMENSIONS);

  fprintf (fp,"parameters:{nl}");
  fprintf (fp,"{tab}chi: %.3f{nl}", g_inputParam[CHI]);
  fprintf (fp,"{tab}Mach_ini: %.3f{nl}", g_inputParam[MACH]);
  fprintf (fp,"{tab}coolmBytcc: %.3f{nl}", {tcoolmBytcc});
  fprintf (fp,"{tab}RinibyRcl: %.3f{nl}", g_inputParam[RINI]);
  fprintf (fp,"{tab}Tcl: %.2e{nl}", {Tcl});
  fprintf (fp,"{tab}PinibykB: %.3e{nl}", {PinibykB});

  fprintf (fp,"wind properties:{nl}");
  fprintf (fp,"{tab}Edot : %.3e{nl}", {Edot});
  fprintf (fp,"{tab}Mdot : %.3e{nl}", {Mdot});
  fprintf (fp,"{tab}Rinj : %.3f{nl}", {Rinj});
  fprintf (fp,"{tab}Rini : %.3f{nl}", {Rini});
  fprintf (fp,"{tab}Rcl  : %.3f{nl}", {Rcl});

  fprintf (fp,"code units:{nl}");
  fprintf (fp,"{tab}unit_dens: %e{nl}", UNIT_DENSITY);
  fprintf (fp,"{tab}unit_len: %e{nl}",  UNIT_LENGTH);
  fprintf (fp,"{tab}unit_vel: %e{nl}",  UNIT_VELOCITY);
"""

info_code = info_code[1:]
if __name__ != '__main__':
    with open("../../info.h", "w") as text_file:
        text_file.write(info_code)
