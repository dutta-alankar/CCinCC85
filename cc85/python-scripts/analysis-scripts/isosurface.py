# -*- coding: utf-8 -*-
"""
Created on Sat Oct  26 18:30:48 2024

@author: alankar
Usage: time python isosurface.py van T
"""
import numpy as np
import h5py
import sys
import os
import subprocess as sp

from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
# from skimage.measure import marching_cubes

if len(sys.argv)<3:
    print("Wrong usage!")
    sys.exit(1)

vanilla = sys.argv[-1] == "T"

root = f"../../output{'-vanl' if vanilla else ''}"

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

if vanilla:
    tcool_mix_B_tcc = tcool_mix_B_tcc[1:]
    rini_B_rcl = rini_B_rcl[1:]

mach = 1.496
Tcl = 4.0e+04
chi = 100

Tmix = np.sqrt(chi)*Tcl
Tcutoff = 8.0e+04

file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
till = 0

mu = 0.60917
mp = 1.6726e-24
Myr = 1.0e+06 * 365*24*60*60

analyze_freq = 1
for select in range(len(tcool_mix_B_tcc[:1])):
    quantity = np.zeros( (till+1, ), dtype=np.float64)
    UNIT_LENGTH, UNIT_DENSITY, UNIT_VELOCITY = None, None, None
    distance_ini = None
    for file_no in range(0, till+1, analyze_freq):
        directory = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"
        output_file = f"{directory}/data.{file_no:04d}.{file_ext}"
        string = f"{output_file}: {file_no}"
        print(string, end="\r")
        if file_no == 0:
            UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
            UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
            UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
            distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])
        data = h5py.File(output_file, "r")
        temperature = np.array(data[f"/Timestep_{file_no}/vars/temperature"])
        del_T = np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"])
        cell_vol  = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]) # code units
        x_cells = np.array(data["/cell_coords/X"])
        y_cells = np.array(data["/cell_coords/Y"])
        z_cells = np.array(data["/cell_coords/Z"])
        Twind = temperature/(1 + del_T)

        cutoff = Twind>Tcutoff # for vanilla this is the entire domain
        # clip the domain
        temperature = np.piecewise(temperature, [cutoff, ], [lambda x:x, 1.0e+10])

        
        # Create a Delaunay tessellation
        delaunay = Delaunay(np.vstack([x_cells.flatten(), y_cells.flatten(), z_cells.flatten()]).T)

        # Interpolate data onto a regular grid
        # grid_x, grid_y, grid_z = np.mgrid[0:1:100j, 0:1:100j, 0:1:100j]  # Adjust range and resolution as needed
        # interpolator = LinearNDInterpolator(delaunay, values)
        # grid_values = interpolator(grid_x, grid_y, grid_z)
        '''
        # Extract isosurface
        verts, faces, _, _ = marching_cubes(grid_values, level=isovalue)
        '''
        print("\n", "Done!")
        data.close()


