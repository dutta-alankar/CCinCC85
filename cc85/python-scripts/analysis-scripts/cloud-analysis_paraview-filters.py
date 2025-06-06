# -*- coding: utf-8 -*-
"""
Created on Sat Oct  29 23:06:48 2024

@author: alankar

Usage: time pvbatch cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-c100,m1.496,T4e4,t0.10,r35.335 1 c100,m1.496,T4e4,t0.10,r35.335
"""

import sys
import os
# state file generated using paraview version 5.11.2
import paraview

if len(sys.argv)!=4:
    print("Wrong usage!")
    sys.exit(1)
output_dir = sys.argv[1]
file_no = int(sys.argv[2])
label = sys.argv[3]
vanl = "vanl" in output_dir

print(f"Working on: output{'-vanl-' if vanl else '-'}{label}/data.{file_no:04d}.flt.xmf")

analysis_data_dir = f"paraview-cloud-analysis_data-dump{'-vanl' if vanl else ''}"
os.makedirs(f"./{analysis_data_dir}", exist_ok=True)
dump_file = f"./{analysis_data_dir}/{label}.pickle"

filter_script = f"""
import os
import numpy as np
import pickle

data_volume  = inputs[0] # same number of cells as data_cloud
data_surface = inputs[1] # same number of cells as data_normals
data_normals = inputs[2] # same number of cells as data_surface
data_cloud   = inputs[3] # same number of cells as data_volume

cloud_surface_area = np.array(data_surface.CellData.GetArray("Area"))
cloud_surface_density = np.array(data_surface.CellData.GetArray("density"))
cloud_vols = np.array(data_volume.CellData.GetArray("Volume"))

cloud_tot_vol = np.sum(cloud_vols)
cloud_tot_surface_area = np.sum(cloud_surface_area)

cloud_density  = np.array(data_cloud.CellData.GetArray("density"))
cloud_pressure = np.array(data_cloud.CellData.GetArray("pressure"))
cloud_temperature = np.array(data_cloud.CellData.GetArray("temperature"))
cloud_velocity_r  = np.array(data_cloud.CellData.GetArray("vr"))
cloud_velocity_th = np.array(data_cloud.CellData.GetArray("vth"))
cloud_velocity_ph = np.array(data_cloud.CellData.GetArray("vphi"))
cloud_distance = np.sqrt( np.array(data_cloud.CellData.GetArray("X"))**2 + np.array(data_cloud.CellData.GetArray("Y"))**2 + np.array(data_cloud.CellData.GetArray("Z"))**2 ) 
cloud_pos_x = np.array(data_cloud.CellData.GetArray("X"))
cloud_pos_y = np.array(data_cloud.CellData.GetArray("Y"))
cloud_pos_z = np.array(data_cloud.CellData.GetArray("Z"))

cloud_tot_mass = np.sum(cloud_density*cloud_vols)

# -------------- Calculate 3 velocities on the surface --------------
X = np.array(data_normals.CellData.GetArray("X"))
Y = np.array(data_normals.CellData.GetArray("Y"))
Z = np.array(data_normals.CellData.GetArray("Z"))

r = np.sqrt(X**2 + Y**2 + Z**2)
R = np.sqrt(X**2 + Y**2)
costh = Z/r
sinth = np.sqrt(1 - costh**2)
cosph = X/R
sinph = np.sqrt(1 - cosph**2)

normals = np.array(data_normals.CellData.GetArray("Normals"))
vr   = np.array(data_normals.CellData.GetArray("vr"))
vth  = np.array(data_normals.CellData.GetArray("vth"))
vphi = np.array(data_normals.CellData.GetArray("vphi"))

vx1 = vr*sinth*cosph + vth*costh*cosph - vphi*sinph
vx2 = vr*sinth*sinph + vth*costh*sinph + vphi*cosph
vx3 = vr*costh - vth*sinth

nx1 = normals[:,0]
nx2 = normals[:,1]
nx3 = normals[:,2] 

wx1 = sinth*cosph - ( nx1*nx1 * sinth*cosph + nx1*nx2 * sinth*sinph + nx1*nx3 * costh )
wx2 = sinth*sinph - ( nx1*nx2 * sinth*cosph + nx2*nx2 * sinth*sinph + nx2*nx3 * costh )
wx3 = costh       - ( nx1*nx3 * sinth*cosph + nx3*nx2 * sinth*sinph + nx3*nx3 * costh )
# normalize
norm = np.sqrt(wx1**2 + wx2**2 + wx3**2)
wx1 = wx1/norm
wx2 = wx2/norm
wx3 = wx3/norm

tx1 = nx2*wx3 - nx3*wx2
tx2 = nx3*wx1 - nx1*wx3
tx3 = nx1*wx2 - nx2*wx1

vin = vx1*nx1 + vx2*nx2 + vx3*nx3
vwi = vx1*wx1 + vx2*wx2 + vx3*wx3
vtu = vx1*tx1 + vx2*tx2 + vx3*tx3

density = np.array(data_normals.CellData.GetArray("density"))
cellvol = np.array(data_normals.CellData.GetArray("cellvol"))

vin_avg = np.sum(density*vin*cellvol)/np.sum(density*cellvol)
vwi_avg = np.sum(density*vwi*cellvol)/np.sum(density*cellvol)
vtu_avg = np.sum(density*vtu*cellvol)/np.sum(density*cellvol)

if os.path.exists("{dump_file}") and {file_no}==0:
  os.remove("{dump_file}")
mode = 'append' if os.path.isfile("{dump_file}") else 'write'

quantity = {{}}
if mode == 'append':
    with open("{dump_file}", "rb") as handle:
        quantity = pickle.load(handle)
quantity["{file_no}"] = {{
                         'cloud_tot_vol': cloud_tot_vol,
                         'cloud_tot_surface_area': cloud_tot_surface_area,
                         'cloud_surface_density': cloud_surface_density,
                         'cloud_tot_mass': cloud_tot_mass,
                         'vin_avg': vin_avg,
                         'vwi_avg': vwi_avg,
                         'vtu_avg': vtu_avg,
                         'cloud_surface_area_elems': cloud_surface_area,
                         'cloud_volume_elems': cloud_vols,
                         'cloud_surface_vin_elems': vin,
                         'cloud_surface_vwi_elems': vwi,
                         'cloud_surface_vtu_elems': vtu, 
                         'cloud_density': cloud_density,
                         'cloud_pressure': cloud_pressure,
                         'cloud_temperature': cloud_temperature,
                         'cloud_velocity_r': cloud_velocity_r,
                         'cloud_velocity_th': cloud_velocity_th,
                         'cloud_velocity_ph': cloud_velocity_ph,
                         'cloud_distance': cloud_distance,
                         'cloud_pos_x': cloud_pos_x,
                         'cloud_pos_y': cloud_pos_y,
                         'cloud_pos_z': cloud_pos_z,
                         }}
with open("{dump_file}", "wb") as handle:                         
    pickle.dump(quantity, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("Done!")
"""

paraview.compatibility.major = 5
paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# Create a new 'SpreadSheet View'
spreadSheetView2 = CreateView('SpreadSheetView')
spreadSheetView2.ColumnToSort = ''
spreadSheetView2.BlockSize = 1024
spreadSheetView2.FieldAssociation = 'Cell Data'

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, spreadSheetView2)
layout1.SetSize(400, 400)

# ----------------------------------------------------------------
# restore active view
SetActiveView(spreadSheetView2)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XDMF Reader'
data_fltxmf = XDMFReader(registrationName='data_flt.xmf', FileNames=[f'{output_dir}/data.{file_no:04d}.flt.xmf'])
data_fltxmf.CellArrayStatus = ['X', 'Y', 'Z', 'cellvol', 'delRhoByRhoWind', 'delTbyTwind', 'density', 'mach', 'ndens', 'pressure', 'temperature', 'tr1', 'vphi', 'vr', 'vth']
data_fltxmf.GridStatus = ['node_mesh']

# create a new 'Calculator'
calculator1_Twind = Calculator(registrationName='Calculator1_Twind', Input=data_fltxmf)
calculator1_Twind.AttributeType = 'Cell Data'
calculator1_Twind.ResultArrayName = 'Twind'
calculator1_Twind.Function = 'temperature/(1+delTbyTwind)'

# create a new 'Threshold'
cutoff_T_wind9e4 = Threshold(registrationName='Cutoff_T_wind>9e4', Input=calculator1_Twind)
cutoff_T_wind9e4.Scalars = ['CELLS', 'Twind']
cutoff_T_wind9e4.LowerThreshold = 428552.3125
cutoff_T_wind9e4.UpperThreshold = 90000.0
cutoff_T_wind9e4.ThresholdMethod = 'Above Upper Threshold'

# create a new 'Threshold'
cloud_material = Threshold(registrationName='cloud_material', Input=cutoff_T_wind9e4)
cloud_material.Scalars = ['CELLS', 'temperature']
cloud_material.LowerThreshold = 80000.0
cloud_material.UpperThreshold = 80000.0
cloud_material.ThresholdMethod = 'Below Lower Threshold'

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=cloud_material)

# create a new 'Cell Size'
cellSize_surface = CellSize(registrationName='CellSize_surface', Input=extractSurface1)
cellSize_surface.ComputeSum = 1

# create a new 'Generate Surface Normals'
generateSurfaceNormals1 = GenerateSurfaceNormals(registrationName='GenerateSurfaceNormals1', Input=extractSurface1)
generateSurfaceNormals1.ComputeCellNormals = 1

# create a new 'Cell Size'
cellSize_volume = CellSize(registrationName='CellSize_volume', Input=cloud_material)
cellSize_volume.ComputeSum = 1

# create a new 'Programmable Filter'
programmableFilter3 = ProgrammableFilter(registrationName='ProgrammableFilter3', Input=[cellSize_volume, cellSize_surface, generateSurfaceNormals1, cloud_material])
programmableFilter3.Script = filter_script
programmableFilter3.RequestInformationScript = ''
programmableFilter3.RequestUpdateExtentScript = ''
programmableFilter3.PythonPath = ''

# ----------------------------------------------------------------
# setup the visualization in view 'spreadSheetView2'
# ----------------------------------------------------------------

# show data from programmableFilter3
programmableFilter3Display = Show(programmableFilter3, spreadSheetView2, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
programmableFilter3Display.Assembly = ''

# ----------------------------------------------------------------
# restore active source
SetActiveSource(programmableFilter3)
# ----------------------------------------------------------------

ResetSession()
sys.exit(0)
'''
if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
'''
