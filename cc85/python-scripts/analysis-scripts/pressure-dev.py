# -*- coding: utf-8 -*-
"""
Created on Sat Aug  20 22:45:48 2023

@author: alankar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import h5py
import pickle

kB = 1.38e-16
mu = 0.609
mp = 1.67e-24

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100
file_ext = "flt.h5"
tcc = np.sqrt(chi)
gamma = 5/3.
create = False

cool = True
extra = '-no_cool' if not(cool) else ''
transparent = False
till = 30 if not(cool) else 100
directory = "./figures"
image_extension = "svg"

## Plot Styling
## Plot Styling
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
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
matplotlib.rcParams["lines.linewidth"] = 4.0
matplotlib.rcParams["ytick.major.width"] = 3.0
matplotlib.rcParams["xtick.major.width"] = 3.0
matplotlib.rcParams["ytick.minor.width"] = 1.5
matplotlib.rcParams["xtick.minor.width"] = 1.5
matplotlib.rcParams["ytick.major.size"] = 12.0
matplotlib.rcParams["xtick.major.size"] = 12.0
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
matplotlib.pyplot.rcParams["font.size"] = 28
matplotlib.rcParams["legend.handlelength"] = 2
# matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["axes.axisbelow"] = True
# plt.style.use('dark_background')
matplotlib.rcParams["figure.figsize"] = (13,10)

Rclbydcell  = 8 
contrast = np.sqrt(chi)
cloud_data = []
plot_title = r"Cloud $\equiv \ [T<%.1f T_{\rm cl} \ \mathcal{and}\ \rho (d)>10 \rho _{\rm wind}(d)]$"%(contrast/3.)

def weighted_quantile(values, quantiles, sample_weight=None, 
                      values_sorted=False, old_style=False):
    # taken from https://stackoverflow.com/questions/21844024/weighted-percentile-using-numpy
    """ Very close to numpy.percentile, but supports weights.
    NOTE: quantiles should be in [0, 1]!
    :param values: numpy.array with data
    :param quantiles: array-like with many quantiles needed
    :param sample_weight: array-like of the same length as `array`
    :param values_sorted: bool, if True, then will avoid sorting of
        initial array
    :param old_style: if True, will correct output to be consistent
        with numpy.percentile.
    :return: numpy.array with computed quantiles.
    """
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), \
        'quantiles should be in [0, 1]'

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)

if create:
    for i in range(len(tcool_mix_B_tcc)):
        root = "../../output"
        t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64)
        del_P = np.zeros_like(t_by_tcc, dtype=np.float64) # deviation wrt to analytic wind pressure
        avg_P = np.zeros_like(t_by_tcc, dtype=np.float64)
        std_P = np.zeros_like(t_by_tcc, dtype=np.float64)
        avg_T = np.zeros_like(t_by_tcc, dtype=np.float64)
        std_T = np.zeros_like(t_by_tcc, dtype=np.float64)
        avg_n = np.zeros_like(t_by_tcc, dtype=np.float64)
        std_n = np.zeros_like(t_by_tcc, dtype=np.float64)
        avg_vel = np.zeros_like(t_by_tcc, dtype=np.float64)
        std_vel = np.zeros_like(t_by_tcc, dtype=np.float64)
        distance = np.zeros_like(t_by_tcc, dtype=np.float64)
        mass_cld = np.zeros_like(t_by_tcc, dtype=np.float64)
        vel_rad_COM = np.zeros_like(t_by_tcc, dtype=np.float64)
        cloud_extent = np.zeros((t_by_tcc.shape[0], 3), dtype=np.float64)

        print(tcool_mix_B_tcc[i])
        for file_no in range(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101):

            special = "long_run/" if (tcool_mix_B_tcc[i]==0.08 and not(cool)) else ""
            filename = f"{root}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[i]:.2f},r{rini_B_rcl[i]:.3f}{extra}/{special}data.{file_no:04d}.{file_ext}"
            print(filename, end="\r")
            data = h5py.File(filename, 'r')
            temperature  = np.array(data[f"/Timestep_{file_no}/vars/temperature"]).flatten()
            vel_rad = np.array(data[f"/Timestep_{file_no}/vars/vr"]).flatten()
            del_rho = np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"]).flatten()
            rad_pos = np.sqrt( np.array(data[f"/cell_coords/X"])**2 + np.array(data[f"/cell_coords/Y"])**2 + np.array(data[f"/cell_coords/Z"])**2 ).flatten()
            condition =  np.logical_and(del_rho>=(contrast-1), temperature<=(contrast/3.)*Tcl)

            tracer = np.array(data[f"/Timestep_{file_no}/vars/tr1"]).flatten()
            density = np.array(data[f"/Timestep_{file_no}/vars/density"]).flatten()
            pressure = np.array(data[f"/Timestep_{file_no}/vars/pressure"]).flatten()
            cellvol = np.array(data[f"/Timestep_{file_no}/vars/cellvol"]).flatten()

            X_pos = np.array(data["/cell_coords/X"]).flatten()
            Y_pos = np.array(data["/cell_coords/Y"]).flatten()
            Z_pos = np.array(data["/cell_coords/Z"]).flatten()

            vel_rad_COM[file_no] = np.sum(density*tracer*cellvol*vel_rad)/np.sum(density*tracer*cellvol)

            delP_by_Pwind = (np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"])+np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"]) + \
                             np.array(data[f"/Timestep_{file_no}/vars/delRhoByRhoWind"])*np.array(data[f"/Timestep_{file_no}/vars/delTbyTwind"])).flatten()

            delP_by_Pwind = delP_by_Pwind[condition]
            density = density[condition]
            pressure = pressure[condition]
            temperature = temperature[condition]
            vel_rad = vel_rad[condition]
            cellvol = cellvol[condition]
            rad_pos = rad_pos[condition]
            X_pos = X_pos[condition]
            Y_pos = Y_pos[condition]
            Z_pos = Z_pos[condition]
            # mass wieghted
            del_P[file_no] = np.sum(delP_by_Pwind*density*cellvol)/np.sum(density*cellvol)
            avg_P[file_no] = np.sum(pressure*cellvol)/np.sum(cellvol)
            std_P[file_no] = np.sqrt(np.sum( (pressure-avg_P[file_no])**2*cellvol)/np.sum(cellvol))
            avg_T[file_no] = np.sum(temperature*density*cellvol)/np.sum(density*cellvol)
            std_T[file_no] = np.sqrt(np.sum( (temperature-avg_T[file_no])**2*density*cellvol)/np.sum(density*cellvol))
            avg_n[file_no] = np.sum(density*cellvol)/np.sum(cellvol)
            std_n[file_no] = np.sqrt(np.sum( (density-avg_n[file_no])**2*cellvol)/np.sum(cellvol))
            avg_vel[file_no] = np.sum(np.abs(vel_rad)*density*cellvol)/np.sum(density*cellvol)
            std_vel[file_no] = np.sqrt(np.sum( (np.abs(vel_rad)-avg_vel[file_no])**2*density*cellvol)/np.sum(density*cellvol))
            distance[file_no] = np.sum(density*cellvol*rad_pos)/np.sum(density*cellvol)/rini_B_rcl[i] # in terms of Rini
            mass_cld[file_no] = np.sum(density*cellvol)

            com_rad = distance[file_no] * rini_B_rcl[i] # in terms of Rcl
            shell_select = np.logical_and( rad_pos>=(com_rad-4.0*1./Rclbydcell), rad_pos<=(com_rad+4.*1./Rclbydcell) )
            distance_from_com = np.sqrt( (X_pos-com_rad)**2 + Y_pos**2 + Z_pos**2 )
            # print("Test:", com_rad, distance_from_com[shell_select])
            if distance_from_com[shell_select].shape[0] != 0:
                cloud_extent[file_no,:] = weighted_quantile(distance_from_com[shell_select], [0.16, 0.50, 0.84], sample_weight=cellvol[shell_select])

            data.close()
        cloud_data.append([del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent])
        print()
    with open(f'./dump/cloud-props-c{chi:d},m{mach:.3f}{extra}.pickle', 'wb') as pic_file:
        pickle.dump(cloud_data, pic_file)

with open(f'./dump/cloud-props-c{chi:d},m{mach:.3f}{extra}.pickle', 'rb') as pic_file:
    cloud_data = pickle.load(pic_file)



# plot with time starts here
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64)
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(t_by_tcc, distance, label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.xlim(xmax = 100)
# plt.ylim(ymin= -0.8, ymax = 5.0)
plt.legend(loc="upper left", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"$d_{\rm cl}/ d_{\rm cl,ini}$")
plt.title(plot_title)
plt.savefig(f"{directory}/cloud-pos{extra}.{image_extension}", transparent=transparent)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(t_by_tcc, np.abs(del_P), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.xlim(xmax = 100)
# plt.ylim(ymin= -0.8, ymax = 5.0)
plt.legend(loc="upper left", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"$\tilde {\Delta p}  (d)/ p_{\rm wind} (d) $")
plt.title(plot_title)
plt.savefig(f"{directory}/pressure-diff_prs{extra}.{image_extension}", transparent=transparent)
plt.close()

exponent = -2*gamma
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.semilogy(t_by_tcc, avg_P/avg_P[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.loglog(t_by_tcc, 0.1*((t_by_tcc-1)/20)**exponent, color="k", linestyle=":", label="-10/3")

plt.xlim(xmax = 100)
plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Average pressure [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantP{extra}.{image_extension}", transparent=transparent)
plt.close()

exponent = -2*(gamma-1)
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.semilogx(t_by_tcc+1, avg_T/avg_T[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Average temperature [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantT{extra}.{image_extension}", transparent=transparent)
plt.close()

exponent = [-2, -2*(gamma-1)]
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(t_by_tcc, avg_n/avg_n[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.loglog(t_by_tcc, 1.0e-02*((t_by_tcc-1)/20)**exponent[0], color="tab:gray", linestyle=":", label="-2")
plt.loglog(t_by_tcc, 8.0e-03*((t_by_tcc-1)/20)**exponent[1], color="k", linestyle=":", label="-10/3")

plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Average density [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantrho{extra}.{image_extension}", transparent=transparent)
plt.close()

vasymp = 1.48614e+00 # code

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    # plt.loglog(t_by_tcc, (vasymp-avg_vel)/(np.sqrt(gamma*kB*chi*Tcl*(distance**(-2*(gamma-1)))/(mu*mp))/4.4963e+07), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    plt.semilogx(t_by_tcc+1, avg_vel/vasymp, label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

plt.xlim(xmax = 100)
plt.ylim(ymax=0.98)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Average rad velocity [asymp]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantv{extra}.{image_extension}", transparent=transparent)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    # plt.loglog(t_by_tcc, (vasymp-avg_vel)/(np.sqrt(gamma*kB*chi*Tcl*(distance**(-2*(gamma-1)))/(mu*mp))/4.4963e+07), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    plt.semilogx(t_by_tcc+1, vel_rad_COM/vasymp, label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

plt.xlim(xmax = 100)
# plt.ylim(ymax=0.98)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Average rad velocity COM [asymp]")
plt.title(r"Tracer marked region")
plt.savefig(f"{directory}/avg_quantvCOM{extra}.{image_extension}", transparent=transparent)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    # plt.loglog(distance, (vasymp-avg_vel)/(np.sqrt(gamma*kB*chi*Tcl*(distance**(-2*(gamma-1)))/(mu*mp))/4.4963e+07), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    p =  plt.semilogx(t_by_tcc+1,  cloud_extent[:,1], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    # plt.fill_between(distance, cloud_extent[:,0], cloud_extent[:,2], color=p[-1].get_color(), alpha=0.7)

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

plt.xlim(xmax = 100)
# plt.ylim(ymax = 0.98)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$t/t_{\rm cc,ini}+1$")
plt.ylabel(r"Transverse cloud extent [$R_{\rm cl}$]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantcloudR{extra}.{image_extension}", transparent=transparent)
plt.close()

# plot with distance starts here
travel = None
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(distance, np.abs(del_P), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    if (i==1):
        travel = np.copy(distance)

plt.loglog(travel, np.abs(6.0*(travel/10)**(2*(gamma-1))-1.0), color="k", linestyle=":", label=f"4/3")

# plt.xlim(xmax = 100)
# plt.ylim(ymin= -0.8, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"$\tilde {\Delta p}  (d)/ p_{\rm wind} (d) $")
plt.title(plot_title)
plt.savefig(f"{directory}/pressure-diff_prsDist{extra}.{image_extension}", transparent=transparent)
plt.close()

exponent = -2
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(distance, avg_P/avg_P[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.loglog(travel, 1.0e-03*(travel/10)**exponent, color="k", linestyle=":", label=f"{exponent}")
plt.loglog(travel, 1.3e-02*(travel/3)**(-2*gamma), color="tab:gray", linestyle=":", label=f"-10/3")

# plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Average pressure [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistP{extra}.{image_extension}", transparent=transparent)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.semilogx(distance, avg_T/avg_T[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

# plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Average temperature [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistT{extra}.{image_extension}", transparent=transparent)
plt.close()

exponent = -2 
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(distance, avg_n/avg_n[0], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

plt.loglog(travel, 4.0e-03*(travel/5)**exponent, color="k", linestyle=":", label=f"{exponent}")
plt.loglog(travel, 5.0e-02*(travel/2)**(-2*gamma), color="tab:gray", linestyle=":", label="-10/3")

# plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Average density [initial]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistrho{extra}.{image_extension}", transparent=transparent)
plt.close()

xponent = -2 
for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    plt.loglog(distance, avg_n/((avg_n[0]/chi)*distance**-2), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(travel, 4.0e-03*(travel/5)**exponent, color="k", linestyle=":", label=f"{exponent}")
# plt.loglog(travel, 5.0e-02*(travel/2)**(-2*gamma), color="tab:gray", linestyle=":", label="-10/3")

# plt.xlim(xmax = 100)
# plt.ylim(ymin= 1.2e-03, ymax = 5.0)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Average $\chi$")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistchi{extra}.{image_extension}", transparent=transparent)
plt.close()

vasymp = 1.48614e+00 # code

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    # plt.loglog(distance, (vasymp-avg_vel)/(np.sqrt(gamma*kB*chi*Tcl*(distance**(-2*(gamma-1)))/(mu*mp))/4.4963e+07), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    plt.semilogx(distance, avg_vel/vasymp, label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")

# plt.loglog(t_by_tcc, 0.1*(t_by_tcc/20)**exponent, color="k", linestyle=":")

plt.xlim(xmax = 27)
plt.ylim(ymax = 0.98)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Average rad velocity [asymp]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistv{extra}.{image_extension}", transparent=transparent)
plt.close()

for i in range(len(tcool_mix_B_tcc)):
    t_by_tcc = np.arange(till+1 if (tcool_mix_B_tcc[i]!=0.08 and not(cool)) else 101, dtype=np.float64) + 1
    # del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance = cloud_data[i]
    del_P, avg_P, std_P, avg_T, std_T, avg_n, std_n, avg_vel, std_vel, distance, mass_cld, vel_rad_COM, cloud_extent = cloud_data[i]
    if tcool_mix_B_tcc[i]!=0.2: continue
    # plt.loglog(distance, (vasymp-avg_vel)/(np.sqrt(gamma*kB*chi*Tcl*(distance**(-2*(gamma-1)))/(mu*mp))/4.4963e+07), label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    p =  plt.loglog(distance, cloud_extent[:,1], label="%.2f"%tcool_mix_B_tcc[i], linestyle="-")
    plt.fill_between(distance, cloud_extent[:,0], cloud_extent[:,2], color=p[-1].get_color(), alpha=0.5)

plt.loglog(travel, (travel/1)**(1.0), color="tab:gray", linestyle=":", label="1")

plt.xlim(xmax = 27)
# plt.ylim(ymax = 0.98)
plt.legend(loc="best", title=r"$t_{\rm cool,mix}/t_{\rm cc,ini}$", ncols=3,
           prop = { "size": 20 }, title_fontsize=20, fancybox=True)
plt.xlabel(r"$d_{\rm cl}/d_{\rm cl,ini}$")
plt.ylabel(r"Transverse cloud extent [$R_{\rm cl}$]")
plt.title(plot_title)
plt.savefig(f"{directory}/avg_quantDistcloudR{extra}.{image_extension}", transparent=transparent)
plt.close()
