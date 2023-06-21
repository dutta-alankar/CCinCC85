# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:54:56 2022

@author: alankar
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

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

scaling_data = "../scaling-approx/output/analysis.dat"
dummy_cloud_data = "../dummy-cloud/output/analysis.dat"

scaling_data = np.loadtxt(scaling_data)
dummy_cloud_data = np.loadtxt(dummy_cloud_data)

rInibyRcl = 200

plt.figure(figsize=(13,10))
plt.plot(scaling_data[:,0], scaling_data[:,1], label="scaling setup")
plt.plot(dummy_cloud_data[:,0], dummy_cloud_data[:,1], label="spherical setup")

plt.xlabel(r"time ($t_{cross}$)")
plt.ylabel(r"Cloud position ($R_{cl}$)")
plt.legend(loc="best")
plt.xlim(xmin=0, xmax=400)
plt.ylim(ymin=rInibyRcl)
plt.savefig("compare-positions.png")
