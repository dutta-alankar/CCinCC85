# -*- coding: utf-8 -*-
"""
Created on Sun Jan  07 12:58:48 2024

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

gamma = 5/3.

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

rhonorm   = interp1d(rnorm, wind[:,1])
prsnorm   = interp1d(rnorm, wind[:,2])
velnorm   = interp1d(rnorm, wind[:,3])
mach_cc85 = interp1d(rnorm, mach)
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
chi = 100 # all chi maynot be possible for a wind as it is too cold due to adiabatic expansion

Twind_ini = chi*Tcl

rho_0 = ((Mdot*(MSun/yr))**1.5)  * (Edot**-0.5) * ((Rinj*pc)**-2)
prs_0 = ((Mdot*(MSun/yr))**0.5)  * (Edot**0.5)  * ((Rinj*pc)**-2)
vel_0 = ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

Twindnorm_ini = Twind_ini/((prs_0/rho_0)*mu*mp/kB)

RinibyRinj = relpos(Twindnorm_ini)
Mach_ini   = mach_cc85(RinibyRinj)

Rini = RinibyRinj*Rinj # pc

prswind_ini = prsnorm(RinibyRinj)*prs_0
rhowind_ini = rhonorm(RinibyRinj)*rho_0
velwind_ini = velnorm(RinibyRinj)*vel_0

# Rgo  = 2 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc 1.97
Rgo  = 10.378 * (Tcl/1e4)**(5/2)*Mach_ini/(((prswind_ini/kB)/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.29) ) * (chi/100) * (alpha**-1) # pc

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.30, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 106.006, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
rclBrthres = 1/np.array(tcool_mix_B_tcc)

select = [True, True, True, True, True, True, True, True, True, True, ]
# select = [False, False, False, False, True, False, False, False, False, ]
tcool_mix_B_tcc = np.array(tcool_mix_B_tcc)[np.where(select)]
rini_B_rcl = np.array(rini_B_rcl)[np.where(select)]

rho_cl = chi*rho_0
mass_cl_ini = 4*np.pi/3*(Rini/rini_B_rcl*pc)**3*rho_cl/MSun

mach = 1.496
Tcl = 4.0e+04
chi = 100
filename = "analysis.dat"
tcc = np.sqrt(chi)

## Plot Styling
#plt.style.use("dark_background") # dark mode
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = True
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["grid.linestyle"] = ":"
matplotlib.rcParams["grid.linewidth"] = 2.0
matplotlib.rcParams["grid.color"] = "gray"
matplotlib.rcParams["grid.alpha"] = 0.5
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 1.0
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 1.0
matplotlib.rcParams["xtick.minor.width"] = 1.0
matplotlib.rcParams["ytick.major.size"] = 8.0
matplotlib.rcParams["xtick.major.size"] = 8.0
matplotlib.rcParams["ytick.minor.size"] = 5.0
matplotlib.rcParams["xtick.minor.size"] = 5.0
matplotlib.rcParams["xtick.major.pad"] = 10.0
matplotlib.rcParams["xtick.minor.pad"] = 10.0
matplotlib.rcParams["ytick.major.pad"] = 6.0
matplotlib.rcParams["ytick.minor.pad"] = 6.0
matplotlib.rcParams["xtick.labelsize"] = 24.0
matplotlib.rcParams["ytick.labelsize"] = 24.0
matplotlib.rcParams["axes.titlesize"] = 24.0
matplotlib.rcParams["axes.labelsize"] = 28.0
matplotlib.rcParams["axes.labelpad"] = 8.0
plt.rcParams["font.size"] = 28
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True
matplotlib.rcParams["figure.figsize"] = (16,14)

def plot_colourline(x,y,c, min_val, max_val, label=None):
    col = matplotlib.cm.cubehelix((c-min_val)/(max_val-np.min(c)))
    ax = plt.gca()
    for i in np.arange(len(x)-1):
        ax.semilogy([x[i],x[i+1]], [y[i],y[i+1]], c=col[i])
    im = ax.scatter(x, y, c=10.**c, s=0,
                    cmap=matplotlib.cm.cubehelix, 
                    norm=matplotlib.colors.LogNorm(vmin=10.**min_val, vmax=10.**max_val)) #, label=label)
    return im

cloud_mass = []
distance_B_rini = []
time_B_tcc = []

for i in range(len(tcool_mix_B_tcc)):
    root = "../../output"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}/{filename}")
    cloud_mass.append(data[:,13])
    distance_B_rini.append(data[:,1]/rini_B_rcl[i]) 
    time_B_tcc.append(data[:,0]/tcc) 

colors = plt.cm.winter(tcool_mix_B_tcc)

for i in range(len(tcool_mix_B_tcc)):
    print(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}/{filename}")
    plt.plot(distance_B_rini[i]*Rini/1.0e+03, cloud_mass[i]*mass_cl_ini[i], 
             color = colors[i], label=f"{tcool_mix_B_tcc[i]:.2f}")

chi_dynamic = Twind_ini*(distance_B_rini[0])**(-2*(gamma-1))/Tcl
prswind_dynamic = prswind_ini*(distance_B_rini[0])**(-2*gamma)
rhowind_dynamic = rhowind_ini*(distance_B_rini[0])**(-2)
Rgo_dynamic  = 10.378 * (Tcl/1e4)**(5/2)*mach_cc85(distance_B_rini[0]/RinibyRinj)/(((prswind_dynamic/kB)/1e3)*(LAMBDA(np.sqrt(chi_dynamic)*Tcl)/10**-21.29) ) * (chi_dynamic/100) * (alpha**-1) # pc
Mgo_dynamic = (4*np.pi/3)*(rhowind_dynamic*chi_dynamic)*(Rgo_dynamic*pc)**3/MSun

plt.plot(distance_B_rini[0]*Rini/1.0e+03, Mgo_dynamic, color="k", linestyle="--")

print(Rini, Rgo)
print(Rini/rini_B_rcl)
# im = plt.scatter(Rini/rini_B_rcl, np.array(cloud_mass_at)*mass_cl_ini, color="k") #, c=rclBrthres, cmap="winter")
# im = plt.scatter(Rini/rini_B_rcl, mass_cl_ini, color="tab:blue") #, c=rclBrthres, cmap="winter")

'''
cbar = plt.colorbar(im, pad=0.01)
cbar.set_label(r"$R_{\rm cl}/R_{\rm thres}$") #, rotation=270)
# print(dir(cbar.ax))
cbar.ax.tick_params(direction="out", length=8, width=1.2, which="major", right=True, zorder=10)
cbar.ax.tick_params(direction="out", length=5, width=1.0, which="minor", right=True, zorder=10)
cbar.ax.update({"zorder": 100000,})
'''
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 15 }, title_fontsize=18, fancybox=True)
# plt.xlim(xmin = 0., xmax = 149.6)
# plt.ylim(ymin = 5.0e-02)
'''
plt.annotate(f"{rclBrthres[0]:.1f}", xy=[30,0.3], fontsize=22)
plt.annotate(f"{rclBrthres[-1]:.1f}", xy=[16,0.1], fontsize=22)
plt.annotate(f"{rclBrthres[5]:.1f}", xy=[120,2.0], fontsize=22)
plt.annotate(f"{rclBrthres[3]:.1f}", xy=[66,1.0], fontsize=22)
'''
#plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncol=3,
#           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.vlines([Rini*(chi/10)**(1/(2*gamma-1))/1.0e+03], ymin=1.0e-05, ymax=1.0e+07, colors='tab:red', linestyles='--')

plt.yscale("log")
plt.xscale("log")
plt.ylabel(r"Cloud mass ($M_\odot$)")
plt.xlabel(r"Distance travelled (kpc)")
# plt.title(r"Cloud $\equiv \ [T<3.3 T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$")
print("Saving.. ")
plt.savefig(f"cloud-mass_dist-m{mach:.3f}.png", transparent=True, bbox_inches='tight')
plt.close()