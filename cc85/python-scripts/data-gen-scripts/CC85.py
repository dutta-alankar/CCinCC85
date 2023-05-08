# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:14:50 2021

@author: alankar

Usage: python ./CC85.py <alpha> <Edot(erg/s)> <beta> <Mdot(Msun/yr)> <Rinj(pc)> <gamma> <True/False(make plot)>
"""
import sys
import numpy as np
from scipy.optimize import root

def Mach_CC85(M, rbyR, gamma):
    if rbyR<0: sys.exit('rbyR cannot be negative: %.3f'%rbyR)
    elif rbyR<1:
        return ((3*gamma+(1/M**2))/(3*gamma+1))**(-(3*gamma+1)/(5*gamma+1))*\
            ((gamma-1+(2/M**2))/(gamma+1))**((gamma+1)/(2*(5*gamma+1))) - rbyR
    else:
        return (M**(2/(gamma-1)))*\
            ((gamma-1+(2/M**2))/(gamma+1))**((gamma+1)/(2*(gamma-1))) - rbyR**2

Msun = 2e33
yr   = 365*24*60**2
pc   = 3.086e18

gamma = float(sys.argv[6])
distance = np.linspace(10**-0.5,10**2,100000)
Mach = [root(Mach_CC85, 0.2*rbyR if rbyR<1 else 1.2*rbyR , args=(rbyR, gamma)).x[0] for rbyR in distance]
Mach = np.array(Mach)

alpha = float(sys.argv[1])
beta  = float(sys.argv[3])
Edot  = float(sys.argv[2])*alpha #1e43*alpha #erg/s
Mdot  = float(sys.argv[4])*beta*(Msun/yr)  #1*Msun/yr*beta
Rinj  = float(sys.argv[5])*pc #200*pc

rhodot  = Mdot/(4/3.*np.pi*Rinj**3)
q       = Edot/(4/3.*np.pi*Rinj**3)

vel = Mach*np.sqrt((q/rhodot)/(0.5*Mach**2+(1./(gamma-1))))
prs = (1/(3*gamma))*rhodot*(Mach**(-1))*np.sqrt((q/rhodot)/(0.5*Mach**2+(1./(gamma-1))))
rho = (1/3.)*rhodot*(Mach**(-1))/np.sqrt((q/rhodot)/(0.5*Mach**2+(1./(gamma-1))))

radius = distance*Rinj
factor = np.array([r if (r/Rinj)<1 else (Rinj**3/r**2) for r in radius])
prs *= factor
rho *= factor

vel_norm = Mdot**(-1/2)*Edot**(1./2)
prs_norm = Mdot**(1/2)*Edot**(1./2)*Rinj**(-2)
rho_norm = Mdot**(3/2)*Edot**(-1./2)*Rinj**(-2)

data = np.vstack((distance, rho/rho_norm, prs/prs_norm, vel/vel_norm)).T
np.savetxt('CC85_steady-prof_gamma_%.3f.txt'%gamma, data,
           header='r/R\trho/(Mdot**(3/2)*Edot**(-1./2)*R**(-2))\tP/(Mdot**(1/2)*Edot**(1./2)*R**(-2))\tu/(Mdot**(-1/2)*Edot**(1./2))',
           comments='# ')

plotit = sys.argv[7]
if (plotit=="True"):
    print(rho_norm, prs_norm, vel_norm)
    import matplotlib.pyplot as plt
    plt.plot(np.log10(distance), Mach, label=r'$\rm \mathcal{M}$')
    plt.plot(np.log10(distance), vel/vel_norm, label=r'velocity')
    plt.plot(np.log10(distance), prs/prs_norm, label=r'pressure')
    plt.plot(np.log10(distance), rho/rho_norm, label=r'density')

    plt.legend(loc='best')
    plt.xlabel(r'$\rm r/R$')
    plt.ylabel(r'Gas fields')
    plt.grid()
    plt.yscale('log')
    #plt.xscale('log')
    plt.xlim(-0.5,0.5)
    plt.ylim(1e-4,1.2e2)
    plt.show()
