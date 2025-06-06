# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:21:48 2023

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

tcool_mix_B_tcc = [2.50, 5.00, 6.00, 7.00, 8.00, 10.00,]
rini_B_rcl = [883.387, 1766.774, 2120.128, 2473.483, 2826.838, 3533.547]
mach = 1.496
Tcl = 4.0e+04
chi = 100
root = "../../output-vanl"
filename = "analysis.dat"
tcc = np.sqrt(chi)

## Plot Styling
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
matplotlib.rcParams["xtick.top"] = False
matplotlib.rcParams["ytick.right"] = True
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["grid.linestyle"] = ":"
matplotlib.rcParams["grid.linewidth"] = 0.8
matplotlib.rcParams["grid.color"] = "gray"
matplotlib.rcParams["grid.alpha"] = 0.3
matplotlib.rcParams["lines.dash_capstyle"] = "round"
matplotlib.rcParams["lines.solid_capstyle"] = "round"
matplotlib.rcParams["legend.handletextpad"] = 0.4
matplotlib.rcParams["axes.linewidth"] = 1.0
matplotlib.rcParams["lines.linewidth"] = 3.5
matplotlib.rcParams["ytick.major.width"] = 1.2
matplotlib.rcParams["xtick.major.width"] = 1.2
matplotlib.rcParams["ytick.minor.width"] = 1.0
matplotlib.rcParams["xtick.minor.width"] = 1.0
matplotlib.rcParams["ytick.major.size"] = 11.0
matplotlib.rcParams["xtick.major.size"] = 11.0
matplotlib.rcParams["ytick.minor.size"] = 5.0
matplotlib.rcParams["xtick.minor.size"] = 5.0
matplotlib.rcParams["xtick.major.pad"] = 10.0
matplotlib.rcParams["xtick.minor.pad"] = 10.0
matplotlib.rcParams["ytick.major.pad"] = 6.0
matplotlib.rcParams["ytick.minor.pad"] = 6.0
matplotlib.rcParams["xtick.labelsize"] = 26.0
matplotlib.rcParams["ytick.labelsize"] = 26.0
matplotlib.rcParams["axes.titlesize"] = 24.0
matplotlib.rcParams["axes.labelsize"] = 28.0
matplotlib.rcParams["axes.labelpad"] = 8.0
plt.rcParams["font.size"] = 28
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True
matplotlib.rcParams["figure.figsize"] = (13,10)

colors = sns.color_palette("Paired", n_colors=len(tcool_mix_B_tcc))  # a list of RGB tuples

for i in range(len(tcool_mix_B_tcc)):
    analysis_file = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}/{filename}"
    data = np.loadtxt(analysis_file)
    print(analysis_file)
    plt.semilogy(data[:,0]/tcc, data[:,13], label=r"%.1f"%tcool_mix_B_tcc[i], color=colors[i])

plt.legend(loc="lower right", title=r"$t_{\rm cool, mix}/t_{\rm cc}|_{\rm ini}$", ncols=3,
                   prop = { "size": 20 }, title_fontsize=22, fancybox=True)
plt.xlim(xmin=0., xmax=149.)
plt.ylim(ymin=6.0e-04, ymax=80)
plt.xlabel(r"time [$t_{\rm cc,ini}$]")
plt.ylabel(r"$M_{\rm cold}$ ($T<8.0\times 10^4$ K) [$M_{\rm cold, ini}$]")
#plt.title(r"Cloud $\equiv \ [T<3.3 T_{\rm cl}]$")
plt.savefig("vanilla-thres-turnover.svg", transparent=False, bbox_inches="tight")
