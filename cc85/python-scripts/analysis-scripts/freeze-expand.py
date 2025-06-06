# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 14:08:14 2025

@author: alankar
"""

import numpy as np
import h5py
import sys
from scipy.interpolate import interp1d

gamma = 5/3.
chi = 100
mach = 1.496
tcoolBtcc = 0.2
diniBdinj = 70.671
Tcl = 4.0e+04
start = 0
till = 150
res = 16

tcc = np.sqrt(chi)

extra = "."
label = f"c{chi},m{mach:.3f},T4e4,t{tcoolBtcc:.2f},r{diniBdinj:.3f}" # -res{res}"
print(label)
location = f"../../output-{label}/{extra}/"

initial_cell_coords = 0
initial_node_coords = 0

file_nos = list(range(start, till+1))
for i in file_nos if 0 in file_nos else np.hstack([0,file_nos]):
    print(i, end='\r' if i<till else '\n')
    cell_coords = []
    node_coords = []
    with h5py.File(f"{location}/data.{i:04d}.flt.h5", 'r') as hdf:
        cell_coords.append( np.array(hdf["/cell_coords/X"]) )
        cell_coords.append( np.array(hdf["/cell_coords/Y"]) )
        cell_coords.append( np.array(hdf["/cell_coords/Z"]) )

        node_coords.append( np.array(hdf["/node_coords/X"]) )
        node_coords.append( np.array(hdf["/node_coords/Y"]) )
        node_coords.append( np.array(hdf["/node_coords/Z"]) )
        if (i==0):
            initial_cell_coords = np.min(cell_coords[0].flatten())
            initial_node_coords = np.min(node_coords[0].flatten())
    offset_cell = np.min(cell_coords[0].flatten())
    offset_node = np.min(node_coords[0].flatten())
    with h5py.File(f"{location}/data.freeze.{i:04d}.flt.h5", 'w') as hdf:
        for j, dim in enumerate(["X", "Y", "Z"]):
            hdf.create_dataset(f"/node_coords/{dim}", data=node_coords[j]-
                                                      (offset_node if dim=="X" else 0.) )
            hdf.create_dataset(f"/cell_coords/{dim}", data=cell_coords[j]-
                                                      (offset_cell if dim=="X" else 0.) )
    with open(f"{location}/data.{i:04d}.flt.xmf", 'r') as xmf_orig:
        content = xmf_orig.readlines()
        with open(f"{location}/data.freeze.{i:04d}.flt.xmf", 'w') as xmf_freeze:
            for line in content:
                if "node_coords" in line:
                 line = line.replace(f"./data.{i:04d}.flt.h5:/node_coords", f"./data.freeze.{i:04d}.flt.h5:/node_coords")
                if "cell_coords" in line:
                    line = line.replace(f"./data.{i:04d}.flt.h5:/cell_coords", f"./data.freeze.{i:04d}.flt.h5:/cell_coords")
                xmf_freeze.write(line)
sys.exit(0)
