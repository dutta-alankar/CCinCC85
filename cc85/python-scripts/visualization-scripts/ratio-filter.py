import numpy as np
import subprocess as sp
from scipy.interpolate import interp1d

mp = 1.67262e-24
kB = 1.3806542e-16
mu = 0.60917
X = 0.7154
gamma = 5./3
Myr = 1.0e+06 * 365*24*60*60

mach = 1.496
Tcl = 4.0e+04
chi = 100

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

select = 1
vanilla = False

root = "/freya/ptmp/mpa/adutt/CCinCC85/cc85"
cooltable = np.loadtxt(f"{root}/cooltable.dat")
directory = f"{root}/output{'-vanl' if vanilla else ''}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"

UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

LAMBDA = interp1d(cooltable[:,0],
                  cooltable[:,1],
                  fill_value="extrapolate")

input0 = inputs[0]

nH = input0.CellData["ndens"]*mu*X
Temperature = input0.CellData["temperature"]
dV = input0.CellData["cellvol"]
del_T = input0.CellData["delTbyTwind"]

x_cell = input0.CellData["X"]
y_cell = input0.CellData["Y"]
z_cell = input0.CellData["Z"]
vr   = input0.CellData["vr"]
vth  = input0.CellData["vth"]
vph  = input0.CellData["vphi"]

radius_sph = np.sqrt(x_cell**2 + y_cell**2 + z_cell**2)
radius_cyl = np.sqrt(x_cell**2 + y_cell**2)
sinth = radius_cyl/radius_sph
costh = z_cell/radius_sph
sinph = y_cell/radius_cyl
cosph = x_cell/radius_cyl

vx = vr*sinth*cosph + vth*costh*cosph - vph*sinph
vy = vr*sinth*sinph + vth*costh*sinph + vth*cosph
vz = vr*costh - vth*sinth

cs = np.sqrt(gamma*kB*Temperature/(mu*mp))
t_sc = dV**(1./3)*UNIT_LENGTH/cs

cool_rate = nH**2*LAMBDA(Temperature)
enrg_th = (1./(gamma-1))*input0.CellData["ndens"]*kB*Temperature
t_cool = enrg_th/cool_rate
output.CellData.append(t_cool/Myr, "tcoolMyr")
output.CellData.append(LAMBDA(Temperature), "LAMBDA")
# output.CellData.append(t_cool/t_sc, "tcBtcs")
# output.CellData.append(Temperature/(1. + del_T), "Twind")

output.CellData.append(vx, "VX1")
output.CellData.append(vy, "VX2")
output.CellData.append(vz, "VX3")
