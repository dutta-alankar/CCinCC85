import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib
import os

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
RinibyRcl = 200
Tcl = 4e4 #K

PinibykB = 1e3 #Kcm^-3, degenerate

# Our model params
chi = 1143
Mw = 4.993191399557429
tcoolmBytcc = 0.003304105670882433
RinibyRcl = 625/75
Tcl = 1e4 #K
PinibykB = 419955.6141084651 #Kcm^-3
'''
# New parameters
chi = 100
Mw = 1.8
tcoolmBytcc = np.array([1.0, 0.5, 0.1, 0.01])
Tcl = 4e4 # K
RinibyRcl = 40

PinibykB = 2.5e5 # Kcm^-3, degenerate

Tw = chi*Tcl
Pw = PinibykB*kB
rhow = (PinibykB/Tw)*(mu*mp)
vw   = Mw*np.sqrt(gamma*kB*Tw/(mu*mp))
RinibyRinj = relpos(Mw)
rhoTini = rhonorm(RinibyRinj)
prsTini = prsnorm(RinibyRinj)
velTini = velnorm(RinibyRinj)

Rgo  = 2 * (Tcl/1e4)**(5/2)*Mw/((PinibykB/1e3)*(LAMBDA(np.sqrt(chi)*Tcl)/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
Rcl  = (tcoolmBytcc**-1) * Rgo # pc
Rini = RinibyRcl*Rcl # pc
Rinj = Rini/RinibyRinj # pc

Mdot = ((Pw/prsTini)* (vw/velTini)**(-1) *(Rinj*pc)**2) / (MSun/yr)
Edot = ((Pw/prsTini) * (vw/velTini) *(Rinj*pc)**2) #erg s^-1

UNIT_LENGTH   = Rcl* pc
UNIT_DENSITY  = rhoTini* ((Mdot*(MSun/yr))**1.5) * (Edot**-0.5) * ((Rinj*pc)**-2)
UNIT_VELOCITY = velTini* ((Mdot*(MSun/yr))**-0.5) * (Edot**0.5)

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = True
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 0.8
matplotlib.rcParams["lines.linewidth"] = 3.0
matplotlib.rcParams["ytick.major.width"] = 0.6
matplotlib.rcParams["xtick.major.width"] = 0.6
matplotlib.rcParams["ytick.minor.width"] = 0.45
matplotlib.rcParams["xtick.minor.width"] = 0.45
matplotlib.rcParams["ytick.major.size"] = 4.0
matplotlib.rcParams["xtick.major.size"] = 4.0
matplotlib.rcParams["ytick.minor.size"] = 2.0
matplotlib.rcParams["xtick.minor.size"] = 2.0
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

out_dir = "cloud-analysis"
os.makedirs(f"./{out_dir}/", exist_ok=True)

location_cc85 = "../../threshold/output-tcoolmBytcc_"

plt.figure(figsize=(13,10))
for i, threshold in enumerate(tcoolmBytcc):
    with plt.style.context('dark_background'):
        data = np.loadtxt(f"{location_cc85}{threshold:.2f}/analysis.dat")
        pos_cloud = data[:,1]*UNIT_LENGTH[i]
        vel_cloud = data[:,2]*UNIT_VELOCITY[i]
        vel_wind = velnorm(pos_cloud/(Rinj[i]*pc))*((Mdot[i]*(MSun/yr))**-0.5) * (Edot[i]**0.5)
        Mach = np.abs(vel_cloud-vel_wind)/np.sqrt(gamma*kB*np.sqrt(chi)*Tcl/(mu*mp))
        rho_cloud_ini = chi *rhoTini* ((Mdot[i]*(MSun/yr))**1.5) * (Edot[i]**-0.5) * ((Rinj[i]*pc)**-2) # CGS
        M_cloud_ini = (4*np.pi/3)*rho_cloud_ini*(Rcl[i]*pc)**3
        rho_cloud = 15.0 * rhonorm(pos_cloud/(Rinj[i]*pc))* ((Mdot[i]*(MSun/yr))**1.5) * (Edot[i]**-0.5) * ((Rinj[i]*pc)**-2) # CGS
        prs_wind = prsnorm(pos_cloud/(Rinj[i]*pc)) * ((Mdot[i]*(MSun/yr))**0.5) * (Edot[i]**0.5) * ((Rinj[i]*pc)**-2) # CGS
        rho_wind = rhonorm(pos_cloud/(Rinj[i]*pc))* ((Mdot[i]*(MSun/yr))**1.5) * (Edot[i]**-0.5) * ((Rinj[i]*pc)**-2) # CGS
        T_wind = np.sqrt(gamma*prs_wind/rho_wind) # CGS
        Rgo_dyn = 2 * (Tcl/1e4)**(5/2)*Mach/((PinibykB/1e3)*(LAMBDA(T_wind/np.sqrt(chi))/10**-21.4) ) *(chi/100) * (alpha**-1) # pc
        Rcl_dyn = (3*(data[:,14]*M_cloud_ini)/(4*np.pi*rho_cloud))**(1/3)/pc
        p = plt.semilogy(data[:,0]/np.sqrt(chi), (Rcl_dyn/Rgo_dyn)/(Rcl[i]/Rgo), label=r"$t_{cool,mix}/t_{cc} = %.2f$"%threshold)


# plt.legend(loc="best", fancybox=True)
plt.xlim(xmin=0, xmax=40)
# plt.ylim(ymin=1e-4, ymax=35)
plt.ylabel(r"$\frac{R_{cl}/R_{thres}}{R_{cl}/R_{thres,\ ini}}$")
plt.xlabel(r"$t/t_{cc}$")
plt.savefig(f"{out_dir}/ratio_{len(tcoolmBytcc)}.png", transparent=True)
plt.show()
