#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:44:05 2024

@author: alankar and ritali
"""

import numpy as np
import cmasher as cm
import matplotlib as mpl

with open('cmasher-presets.xml', 'w') as xml:
    xml.write('<ColorMaps>')
    for cmap in mpl.colormaps:
        if 'cmr.' in cmap and '_r' not in cmap:
            cm_name = f'cmasher_{cmap.split(".")[-1]}'
            xml.write(f'  <ColorMap name="{cm_name}" space="RGB">')
            print(cm_name)
            cm_data = mpl.colormaps.get_cmap(cmap).colors
            for indx, val in enumerate(np.linspace(0, 1, len(cm_data))):
                xml.write(f'    <Point x="{val:.6f}" o="{val:.6f}" r="{cm_data[indx][0]:.6f}" g="{cm_data[indx][1]:.6f}" b="{cm_data[indx][2]:.6f}"/>\n')
            xml.write('  </ColorMap>')
    xml.write('</ColorMaps>')
    