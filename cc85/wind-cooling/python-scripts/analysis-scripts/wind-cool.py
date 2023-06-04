"""
Created on Fri May 26 00:08:30 2023

@author: alankar
"""

import numpy as np
import h5py
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

UNIT_DENSITY = 6.3682e-26
UNIT_LENGTH = 2.7198e+20
UNIT_VELOCITY = 5.4100e+07

file_no = 0
hdf = h5py.File(f"../../output/data.{file_no:04d}.flt.h5", "r")

print(list(hdf.keys()))
print(list(hdf[f"/Timestep_{file_no}/vars"].keys()))
rad = np.array(hdf[f"/cell_coords/X"])
ndens = np.array(hdf[f"/Timestep_{file_no}/vars/ndens"])
temp  = np.array(hdf[f"/Timestep_{file_no}/vars/temperature"])
vel   = np.array(hdf[f"/Timestep_{file_no}/vars/vr"])

cooltable = np.loadtxt("../../cooltable.dat")
lam = interp1d(cooltable[:,0], cooltable[:,1], fill_value="extrapolate")

tcool = 1.38e-16*temp/(ndens*lam(temp))
tadv  = (rad*UNIT_LENGTH)/(vel*UNIT_VELOCITY)

plt.semilogx(rad/40, tcool/tadv)
plt.grid()
plt.show()
