# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:54:56 2022

@author: alankar
"""
import numpy as np
import importlib
constants_add_misc = importlib.import_module("def-gen")
globals().update(vars(constants_add_misc)) #imported variables

Rclbydcell  = 8 #resolution
Npar   = 230
Nprp   = 40
Nleft  = 100

Rbarini  = Rini/Rinj
Rinj     = Rinj/Rcl # code units
Rini     = Rini/Rcl # code units
Rcl      = 1.0 # code units

tcc      = np.sqrt(chi) # code units

dr     = Rcl/Rclbydcell # code units

Rbeg    = Rini-Nleft*Rcl # code units
Rend    =  int(np.ceil(Rbeg + Npar*Rcl)) # code units
prpbeg  = -int(np.ceil(0.5*Nprp*Rcl)) # code units
prpend  =  int(np.ceil(0.5*Nprp*Rcl)) # code units

Nr      = int(np.ceil((Rend-Rbeg)/dr))
Nprp    = int(np.ceil((prpend-prpbeg)/dr))

cfl    = 0.2
tstop  = 4.0*tcc*np.sqrt(chi)
dt_ini = 1.e-8
dt_analysis = 1e-1*tcc

output_dir = './output'
log_dir    = './output/Log_Files'

print('Resolution (%d, %d, %d)'%(Nr, Nprp, Nprp))

pluto_ini = f"""
[Grid]

X1-grid    1     {Rbeg:<8.2f}     {Nr:<5}       u        {Rend:.2f}
X2-grid    1     {prpbeg:<9.2f}    {Nprp:<6}      u        {prpend:.2f}
X3-grid    1     {prpbeg:<9.2f}    {Nprp:<6}      u        {prpend:.2f}

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

X1-beg        outflow
X1-end        outflow
X2-beg        outflow
X2-end        outflow
X3-beg        outflow
X3-end        outflow

[Static Grid Output]

uservar    4    temperature ndens mach cellvol
output_dir {output_dir}
log_dir    {log_dir}
dbl       -1.0          -1   single_file
flt       -1.0          -1   single_file
vtk       -1.0          -1   single_file
dbl.h5    {10.*tcc:<8.2e}      -1   single_file
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

RINI                        {Rini:.2f}
CHI                         {chi:.2f}
MACH                        {Mw:.2f}
ZMET                        1.0
"""
pluto_ini = pluto_ini[1:]

# if (Rbeg-5*dr<0): print("Problem!")
with open("../../pluto.ini", "w") as text_file:
    text_file.write(pluto_ini)
