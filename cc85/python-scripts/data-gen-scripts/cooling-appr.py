# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:13:40 2022

@author: alankar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from typing import Union, Callable
import matplotlib.pyplot as plt


def cooling_appr(temperature: np.ndarray,
                 metallicity: float,
                 cooling:Callable,
                 ) -> np.ndarray:
    slope1 = -1/(np.log10(8.7e3)-np.log10(1.2e4))
    slope2 = 1/(np.log10(1.2e4)-np.log10(7e4))
    slope3 = -1/(np.log10(2e6)-np.log10(8e7))
    coolcurve = cooling(temperature)
    factor = np.piecewise(temperature,
                          [temperature<8.7e3,
                           np.logical_and(temperature>=8.7e3,temperature<=1.2e4),
                           np.logical_and(temperature>1.2e4,temperature<=7e4),
                           np.logical_and(temperature>7e4,temperature<=2e6),
                           np.logical_and(temperature>2e6,temperature<=8e7),
                           temperature>8e7,
                           ],
                          [lambda x: 0,
                           lambda x: slope1*(np.log10(x)-np.log10(8.7e3)),
                           lambda x: slope2*(np.log10(x)-np.log10(1.2e4))+1,
                           lambda x: 0,
                           lambda x: slope3*(np.log10(x)-np.log10(2e6)),
                           lambda x: 1,
                           ])
    """
    plt.semilogx(temperature, factor)
    plt.grid()
    plt.show()
    """
    coolcurve = (factor+(1-factor)*metallicity)*coolcurve

    return coolcurve

if __name__ == "__main__":
    cooling_data = np.loadtxt("cooltable.dat")
    cooling = interp1d(cooling_data[:,0], cooling_data[:,1], fill_value="extrapolate")
    temperature = np.logspace(1,9, 8000)
    np.savetxt("cooltable-appr.dat",
                np.vstack( (temperature, cooling_appr(temperature, 0.3, cooling)) ).T)
