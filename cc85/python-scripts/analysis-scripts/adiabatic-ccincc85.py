# -*- coding: utf-8 -*-
"""
Created on Sat Aug  19 22:45:48 2023

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100
filename = "analysis.dat"
tcc = np.sqrt(chi)
gamma = 5/3.

## Plot Styling
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
matplotlib.rcParams["figure.figsize"] = (13,10)

custom_lines = [Line2D([0], [0], color="gray", 
                       linewidth=matplotlib.rcParams["lines.linewidth"],
                       linestyle = "-",
                      ),
                Line2D([0], [0], color="gray",
                       linewidth=matplotlib.rcParams["lines.linewidth"],
                       linestyle = "--",
                      ),
               ]

for i in range(len(tcool_mix_B_tcc)):
    root = "../../output-vanl"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}-no_cool/{filename}")
    line = plt.semilogy(data[:,0]/tcc, data[:,13],
                        linestyle=":")
    root = "../../output"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}-no_cool/{filename}")
    plt.semilogy(data[:,0]/tcc, data[:,13], label="%.2f"%tcool_mix_B_tcc[i],
                 color = line[-1].get_color(), linestyle="-")

plt.xlim(xmin = 0., xmax = 12.6)
plt.ylim(ymin = 9.6e-4)
lg1 = plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
lg2 = plt.legend(custom_lines, [r"CC85", r"Vanilla"], title="Setups", loc="lower left",
           prop = { "size": 20 }, fancybox=True)
plt.gca().add_artist(lg1)
plt.xlabel(r"$t/t_{\rm cc,ini}$")
plt.ylabel(r"$M_{\rm cl}/M_{\rm cl,ini}$")
plt.title(r"Cloud $\equiv \ [T<3.3 T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$")
plt.savefig("vanilla-mass-no_scale.png", transparent=True)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    root = "../../output-vanl"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}-no_cool/{filename}")
    line = plt.semilogy(data[:,0]/tcc, data[:,13],
                        linestyle=":")
    root = "../../output"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}-no_cool/{filename}")
    scale = (data[:,1]/rini_B_rcl[i])**(1-gamma/3.)
    plt.semilogy(data[:,0]/(tcc*scale), data[:,13], label="%.2f"%tcool_mix_B_tcc[i],
                 color = line[-1].get_color(), linestyle="-")

plt.xlim(xmin = 0., xmax = 8.3)
plt.ylim(ymin = 9.6e-4)
lg1 = plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3, 
        prop = { "size": 20,}, title_fontsize=20, fancybox=True)
lg2 = plt.legend(custom_lines, [r"CC85 ($t_{\rm cc} \propto d^{4/9}$)", r"Vanilla ($t_{\rm cc} \propto d^{0}$)"], title="Setups",
           prop = { "size": 20 }, fancybox=True)
plt.gca().add_artist(lg1)
plt.xlabel(r"$t/t_{\rm cc,ini}$")
plt.ylabel(r"$M_{\rm cl}/M_{\rm cl,ini}$")
plt.title(r"Cloud $\equiv \ [T<3.3 T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$")
plt.savefig("vanilla-mass-scaled.png", transparent=True)

