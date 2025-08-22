# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 21:20:56 2024

@author: alankar
"""
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib
import subprocess as sp
import sys
import os
from decimal import Decimal

def fexp(number):
    (sign, digits, exponent) = Decimal(number).as_tuple()
    return len(digits) + exponent - 1

def fman(number):
    return Decimal(number).scaleb(-fexp(number)).normalize()

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

# Param set 1
Edot = 3.00e+41  # erg/s
Mdot = 2.00      # MSun/yr
Rinj = 200       # pc
'''
# Param set 2
Edot = 1.00e+42  # erg/s
Mdot = 5.00      # MSun/yr
Rinj = 300       # pc
'''
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
Mw = Mach_ini

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

PinibykB = prswind_ini/kB

rhoTini = rhonorm(RinibyRinj)
prsTini = prsnorm(RinibyRinj)
velTini = velnorm(RinibyRinj)

UNIT_LENGTH   = Rcl* pc
UNIT_DENSITY  = rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2)
UNIT_VELOCITY = velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

cooling = True
vanilla = True

definitions = \
f'''
#define  PHYSICS                        HD
#define  DIMENSIONS                     3
#define  COMPONENTS                     3
#define  GEOMETRY                       SPHERICAL
#define  BODY_FORCE                     NO
#define  FORCED_TURB                    NO
#define  COOLING                        {"TABULATED" if cooling else "NO"}
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

with open("../../definitions.h", "w") as text_file:
    text_file.write(definitions)

Rclbydcell  = 8 #resolution
Npar   = 600
Nprp   = 20
Nleft  = 2.0
buf_t  = 16.0

Rbarini  = RinibyRinj
Rinj     = Rinj/Rcl # code units
Rini     = Rini/Rcl # code units
Rcl      = 1.0 # code units

tcc      = np.sqrt(chi) # code units

dr     = Rcl/Rclbydcell # code units
dth    = Rcl/(Rini*Rclbydcell)
dph    = dth

Rbeg   = Rini-Nleft*Rcl # code units
Rend   = int(np.ceil(Rbeg + Npar*Rcl)) # code units
thbeg  = np.pi/2 - Nprp*Rcl/(2*Rini)
thend  = np.pi/2 + Nprp*Rcl/(2*Rini)
phbeg  = - Nprp*Rcl/(2*Rini)
phend  =   Nprp*Rcl/(2*Rini)

Nr     = int(np.floor((Rend-Rbeg)/dr))
Nth    = int(np.ceil((thend-thbeg)/dth))
Nph    = Nth

cfl    = 0.2
tstop  = 10.0*tcc*np.sqrt(chi)
dt_ini = 1.e-8
dt_analysis = 1e-1*tcc

output_dir = './'
log_dir    = './Log_Files'

print('Resolution (%d, %d, %d)'%(Nr, Nth, Nph))
if (Rbeg/Rini*Rbarini <= 1.0 ): print('Problem! Injection region included!')

pluto_ini = f"""
[Grid]

X1-grid    1     {Rbeg:<7.6f}   {Nr:<4}        u        {Rend:<8.6f}
X2-grid    1     {thbeg:<9.6f}    {Nth:<6}      u        {thend:<9.6f}
X3-grid    1     {phbeg:<9.6f}    {Nph:<6}      u        {phend:<9.6f}

[Chombo Refinement]

Levels           4
Ref_ratio        2 2 2 2 2
Regrid_interval  2 2 2 2
Refine_thresh    0.3
Tag_buffer_size  3
Block_factor     8
Max_grid_size    64
Fill_ratio       0.75

[Time]

CFL              {cfl}
CFL_max_var      1.1
tstop            {tstop:.2e}
first_dt         {dt_ini}

[Solver]

Solver         hllc

[Boundary]

X1-beg        userdef
X1-end        userdef
X2-beg        userdef
X2-end        userdef
X3-beg        userdef
X3-end        userdef

[Static Grid Output]

uservar    6    temperature ndens mach cellvol delTbyTwind delRhoByRhoWind
output_dir {output_dir}
log_dir    {log_dir}
dbl       -1.0          -1   single_file
flt       -1.0          -1   single_file
vtk       -1.0          -1   single_file
dbl.h5    -1.0          -1   single_file
flt.h5    {1.0*tcc:<8.2e}      -1   single_file
tab       -1.0          -1
ppm       -1.0          -1
png       -1.0          -1
log        100
analysis  {dt_analysis:<8.2e}      -1

[Chombo HDF5 output]

Checkpoint_interval  -1.0  0
Plot_interval         1.0  0

[Particles]

Nparticles             0   -1
particles_dbl       -1.0   -1
particles_flt       -1.0   -1
particles_vtk       -1.0   -1
particles_tab       -1.0   -1

[Parameters]

RINI                        {Rini:.3f}
THINI                       90.0
PHIINI                      0.0
CHI                         {chi:.3f}
MACH                        {Mw:.3f}
ZMET                        1.0
BUFFER_TRACK                {buf_t:.1f}
"""
pluto_ini = pluto_ini[1:]

# if (Rbeg-5*dr<0): print("Problem!")
with open("../../pluto.ini", "w") as text_file:
    text_file.write(pluto_ini)

local_make = \
f'''
ifeq ($(strip $(PARALLEL)), TRUE)
 LDFLAGS      += -L/mpcdf/soft/SLE_15/packages/skylake/hdf5/gcc_10-10.3.0-openmpi_4-4.0.7/1.12.0/lib -lhdf5 -lz
 INCLUDE_DIRS += -I/mpcdf/soft/SLE_15/packages/skylake/hdf5/gcc_10-10.3.0-openmpi_4-4.0.7/1.12.0/include
endif

ifeq ($(strip $(PARALLEL)), FALSE)
 LDFLAGS      += -L/mpcdf/soft/SLE_15/packages/skylake/hdf5/gcc_10-10.3.0/1.12.0/lib -lhdf5 -lz
 INCLUDE_DIRS += -I/mpcdf/soft/SLE_15/packages/skylake/hdf5/gcc_10-10.3.0/1.12.0/include
endif

 CFLAGS       += -g -DUSE_HDF5 # -DH5_USE_16_API
 OBJ          += hdf5_io.o

 OBJ          += tracking.o
 OBJ          += wind.o

 HEADERS      += wind.h
 HEADERS      += local_pluto.h
 HEADERS      += local_gvars.h
 
 # CFLAGS      += -DUSE_PNG
 # LDFLAGS     += -L$(PNG_LIB)/lib -lpng
 # LDFLAGS     += -lgsl -lgslcblas

 # INCLUDE_DIRS += -I/u/adutt/comp_libs/catalyst/include/catalyst-2.0
 # LDFLAGS      += -L/u/adutt/comp_libs/catalyst/lib64 -lcatalyst
 # CFLAGS       += -DUSE_CATALYST # -DCATALYST_VERBOSE
 # CFLAGS       += -DPARAVIEW_IMPL_DIR=\"/mpcdf/soft/SLE_15/packages/x86_64/paraview/5.10.1/lib/catalyst/\"

 CFLAGS        += -DPYTHON_LOC=\\"../../.venv/bin/python\\"
 # CFLAGS        += -DCLOUDY_DATA_PATH==\"$(pwd)/c17.03/data\"
 {"# " if not(vanilla) else ""}CFLAGS        += -DVANILLA
'''
 
local_make = local_make[1:]
with open("../../local_make", "w") as text_file:
    text_file.write(local_make)

out_dir = f"output-{'vanl-' if vanilla else ''}c{chi:d},m{Mach_ini:.3f},T{round(fman(Tcl)):d}e{round(fexp(Tcl)):d},t{tcoolmbytcc:.2f},r{RinibyRcl:.3f}{'-no_cool' if not(cooling) else ''}"
print(out_dir)

compile_code = True
submit = True
force = False
if len(sys.argv)==3:
    force = True if sys.argv[2]=="T" else False

if not(os.path.isdir(f"../../{out_dir}")) or force:
    if os.path.isdir(f"../../{out_dir}"):
        old_jobs = sp.getoutput("ls ../../{out_dir}/tjob.*")
        if "No such file or directory" not in old_jobs:
            os.system("rm -f ../../{out_dir}/tjob.*")
            os.system("rm -f ../../{out_dir}/Log_Files/*")
    else:
        os.system(f"mkdir ../../{out_dir}")
    # copy a few files needed during PLUTO runs
    os.system(f"cp ../../sysconf.out ../../{out_dir}")
    os.system(f"cp ../../CC85_steady-prof_gamma_1.667.txt ../../{out_dir}")
    os.system(f"cp ../../CC85.py ../../{out_dir}")
    os.system(f"cp ../../cooltable.dat ../../{out_dir}")
    if cooling:
        os.system(f"cp ./makefile-w_cool ../../makefile")
    else:
        os.system("cp ./makefile-no_cool ../../makefile")
    if compile_code:
        environment = '''module purge && module load gcc/10 openmpi/4 hdf5-mpi/1.12.0 && export LD_LIBRARY_PATH="/mpcdf/soft/SLE_15/packages/skylake/openmpi/gcc_10-10.3.0/4.0.7/lib:/mpcdf/soft/SLE_15/packages/skylake/gsl/gcc_10-10.3.0/2.4/lib:/mpcdf/soft/SLE_15/packages/skylake/fftw/gcc_10-10.3.0-openmpi_4-4.0.7/3.3.10/lib:/mpcdf/soft/SLE_15/packages/skylake/hdf5/gcc_10-10.3.0-openmpi_4-4.0.7/1.12.0/lib:$LD_LIBRARY_PATH"'''
        os.system(f"{environment} && cd ../.. && make -j16 && make clean")
        os.system(f"cp ../../pluto ../../{out_dir}")
        os.system(f"cp ../../pluto.ini ../../{out_dir}")
        os.system(f"cp ../../definitions.h ../../{out_dir}")
        os.system(f"cp ../../local_make ../../{out_dir}")
        os.system(f"cp ../../makefile ../../{out_dir}")
        os.system(f"cp ./slurm-script ../../{out_dir}")
    if submit:
        os.system(f"cd ../../{out_dir} && sbatch slurm-script")
else:
    print("Location already exists!")
