# -*- coding: utf-8 -*-
"""
Created on Sat Aug  21 12:03:48 2023

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

dark = True
tcool_mix_B_tcc = [0.10, 0.20, 0.50, 0.80, 2.50, 8.00,] # [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [35.335, 70.671, 176.677, 282.684, 883.387, 2826.838,] # [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
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
matplotlib.rcParams["figure.figsize"] = (14,10)
if dark:
    plt.style.use('dark_background')

def plot_colourline(x,y,c, min_val, max_val, label=None):
    col = matplotlib.cm.nipy_spectral((c-min_val)/(max_val-np.min(c)))
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
min_dist = np.inf
max_dist = -np.inf
for i in range(len(tcool_mix_B_tcc)):
    print(i, end="\r")
    root = "../../output"
    data = np.loadtxt(f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}/{filename}")
    cloud_mass.append(data[:,13])
    distance_B_rini.append(data[:,1]/rini_B_rcl[i]) 
    time_B_tcc.append(data[:,0]/tcc) 
    
    min_dist = min( min_dist, np.min(data[:,1]/rini_B_rcl[i]))
    max_dist = max( max_dist, np.max(data[:,1]/rini_B_rcl[i]))
print(min_dist, max_dist)
for i in range(len(tcool_mix_B_tcc)-1, -1, -1):
    print(i, end="\r")
    im = plot_colourline(time_B_tcc[i], cloud_mass[i], np.log10(distance_B_rini[i]), 
                    np.log10(min_dist), np.log10(max_dist),
                    label="%.2f"%tcool_mix_B_tcc[i])

cbar = plt.colorbar(im, pad=0.01)
cbar.set_label(r"$d_{\rm cl}/d_{\rm cl,ini}$") #, rotation=270)
# print(dir(cbar.ax))
cbar.ax.tick_params(direction="out", length=8, width=1.2, colors="k", which="major", right=True, zorder=10)
cbar.ax.tick_params(direction="out", length=5, width=1.0, colors="k", which="minor", right=True, zorder=10)
cbar.ax.update({"zorder": 100000,})

plt.xlim(xmin = 0., xmax = 149.6)
plt.ylim(ymin = 5.0e-02)
#plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
#           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}$")
plt.ylabel(r"$M_{\rm cl}/M_{\rm cl,ini}$")
plt.title(r"Cloud $\equiv \ [T<3.3 T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$")
print("Saving.. ")
plt.savefig(f"cc85-cool-mass{'-dark' if dark else ''}.pdf", transparent=True, bbox_inches="tight")
plt.close()

fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(13,14))
fig.suptitle(r"Cloud $\equiv \ [T<3.3 T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$")

for i in range(len(tcool_mix_B_tcc)):
    print(i, end="\r")
    line = ax1.semilogy(time_B_tcc[i], cloud_mass[i])
    ax2.semilogy(time_B_tcc[i], distance_B_rini[i], color=line[-1].get_color(),
                 label="%.2f"%tcool_mix_B_tcc[i])
    if (i==(len(tcool_mix_B_tcc)-1)): continue
    pos = np.argmax(cloud_mass[i])
    ax1.vlines(time_B_tcc[i][pos], 1.0e-02, 1.0e+02, 
               color=line[-1].get_color(), linestyle=":")
    ax2.vlines(time_B_tcc[i][pos], 1.0e-02, 1.0e+02, 
               color=line[-1].get_color(), linestyle=":")

ax2.set_xlim(xmin = 0., xmax = 149.6)
ax1.set_ylim(ymin = 5.0e-02, ymax=2.0e+01)
ax2.set_ylim(ymin = 2.0e-01, ymax=6.0e+01)
ax2.set_xlabel(r"$t/t_{\rm cc,ini}$")
ax1.set_ylabel(r"$M_{\rm cl}/M_{\rm cl,ini}$")
ax2.set_ylabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")

ax2.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 16 }, title_fontsize=16, fancybox=True)

plt.savefig(f"cc85-cool-mass-2_pan{'-dark' if dark else ''}.pdf", transparent=True, bbox_inches="tight")
plt.close()


for i in range(len(tcool_mix_B_tcc)):
    plt.semilogy(distance_B_rini[i], cloud_mass[i], label="%.2f"%tcool_mix_B_tcc[i])

plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 16 }, title_fontsize=16, fancybox=True)
 
plt.xlim(xmin=1.0, xmax=10)
plt.ylim(ymin=1.03e-03,  ymax=18)
plt.vlines(3.0, 1.0e-03, 20)
plt.ylabel(r"$M_{\rm cl}/M_{\rm cl,ini}$")
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.savefig(f"mass-dist{'-dark' if dark else ''}.pdf", transparent=True, bbox_inches="tight")
plt.close()
