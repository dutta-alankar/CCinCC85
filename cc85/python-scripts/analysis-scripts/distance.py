import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

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
location_vanl = "../../../vanilla/threshold/output-tcoolmBytcc_"

chi = 100
thresholds = [1.0, 0.5, 0.1, 0.01]
kpc = 3.086e+21
UNIT_LENGTH = [2.7198e+18, 5.4395e+18, 2.7198e+19, 2.7198e+20]

plt.figure(figsize=(13,10))
for i, threshold in enumerate(thresholds):
    with plt.style.context('dark_background'):
        data = np.loadtxt(f"{location_cc85}{threshold:.2f}/analysis.dat")
        p = plt.semilogy(data[:,0]/np.sqrt(chi), (data[:,1]-data[0,1])*UNIT_LENGTH[i]/kpc, label=r"$t_{cool,mix}/t_{cc} = %.2f$"%threshold)
        data = np.loadtxt(f"{location_vanl}{threshold:.2f}/analysis.dat")
        plt.semilogy(data[:,0]/np.sqrt(chi), (data[:,1]-data[0,1])*UNIT_LENGTH[i]/kpc, linestyle="--", color=p[-1].get_color())

# plt.legend(loc="best", fancybox=True)
plt.xlim(xmin=0, xmax=40)
plt.ylim(ymin=1e-4, ymax=35)
plt.ylabel(r"Distance travelled by cloud [kpc]")
plt.xlabel(r"$t/t_{cc}$")
plt.savefig(f"{out_dir}/distance_{len(thresholds)}.png", transparent=True)
plt.show()
