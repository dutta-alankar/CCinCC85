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
Npar   = 600
Nprp   = 20
Nleft  = 2
buf_t  = 16.0

Rbarini  = Rini/Rinj
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

output_dir = './output'
log_dir    = './output/Log_Files'

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

nl  = "\\n"
tab = "\\t"

info_code = f"""

  fprintf (fp,"additional info:{nl}");
  fprintf (fp,"{tab}Rclbydcell: {Rclbydcell}{nl}");
  fprintf (fp,"{tab}Rcl_buffer: {Nleft}{nl}");
  fprintf (fp,"{tab}ncells: {[Nr, Nth, Nph]}{nl}");

  fclose(fp);
}}
"""

info_code = info_code[1:]
with open("../../info.h", "a") as text_file:
    text_file.write(info_code)
