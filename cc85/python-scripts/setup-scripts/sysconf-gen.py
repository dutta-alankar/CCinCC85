# -*- coding: utf-8 -*-
"""
Created on Mon Jun 07 07:02:56 2024

@author: alankar
"""

import os
import re
import subprocess as sp

pluto_loc = "/freya/ptmp/mpa/adutt/CCinCC85/PLUTO"
details = os.uname()
year = sp.getoutput('date +"%Y"')
user = sp.getoutput("echo $USER")
# work_dir = sp.getoutput("cd .. && pwd")
sys_name = details[0]
node_name = details[1]
release = details[2]
arch = details[-1]
byte = sp.getoutput('lscpu | grep Endian').split()[-2].lower()
version = details[-2]
compiler_details = sp.getoutput('cat ../../makefile | grep "ARCH" | grep "="').split()[-1]
mpi_compiler = sp.getoutput(f'cat {pluto_loc}/Config/Linux.mpicc.defs | grep "CC"').split()[-1]
c_compiler = 'gcc' # re.sub('[\W_]+', '', sp.getoutput(f"{mpi_compiler} --version").split()[0])
pluto_ver = sp.getoutput(f'grep -r "PLUTO_VERSION" {pluto_loc}/Src/* | grep "define"').split()[-1][1:-1]

root = "/freya/ptmp/mpa/adutt/CCinCC85/cc85/output"
mach = 1.496
Tcl = 4.0e+04
chi = 100
tcool_mix_B_tcc = 0.2
rini_B_rcl = 70.671
Rclbydcell = 16

work_dir = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc:.2f},r{rini_B_rcl:.3f}_res{Rclbydcell}"

sysconf = f"""
USER           = {user}
WORKING_DIR    = {work_dir}
SYSTEM_NAME    = {sys_name}
NODE_NAME      = {node_name}
RELEASE        = {release}
ARCH           = {arch}
BYTE_ORDER     = {byte}
VERSION        = {version}
PLUTO_DIR      = {pluto_loc}
PLUTO_VERSION  = "{pluto_ver}"
C_COMPILER     = {c_compiler}
MPI_C_COMPILER = {mpi_compiler}
"""

with open("../../sysconf.out", "w") as ascii:
    ascii.write(sysconf[1:])

print(sysconf[1:])
