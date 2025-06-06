# -*- coding: utf-8 -*-
"""
Created on Sat Oct  28 12:11:48 2024

@author: alankar

Usage: time pvbatch area+volume_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-c100,m1.496,T4e4,t0.10,r35.335 1 c100,m1.496,T4e4,t0.10,r35.335
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

paraview.compatibility.major = 5
paraview.compatibility.minor = 11

analysis_data_dir = "area+volume-data_dump"
os.makedirs(f"./{analysis_data_dir}", exist_ok=True)
dump_file = f"./{analysis_data_dir}/{label}.txt"

area_script =f"""
import os

if os.path.exists("{dump_file}") and {file_no}==0:
  os.remove("{dump_file}")

mode = 'a' if os.path.isfile("{dump_file}") else 'w'
if mode == 'a':
    with open("{dump_file}", 'r') as txtfile:
        last_line = txtfile.readlines()[-1]
else:
    last_line = ''

data = inputs[0]
area = data.CellData.GetArray("Area")[0]

with open("{dump_file}", mode) as txtfile:
    if mode == 'w':
        txtfile.write(f"# {label}\\n")
        txtfile.write(f"# t/tcc    Area          Volume        Mass          Density\\n")
    to_write = f"  {file_no:<9d}{{area:<14.3e}}"
    if to_write != last_line:
        txtfile.write(to_write)
print(f"Area:   {{area:.3f}}")
"""
volume_script = f"""
import numpy as np

data = inputs[0]
cell_vols = np.array(data.CellData.GetArray("cellvol"))
density = np.array(data.CellData.GetArray("density"))
volume_cl = np.sum(cell_vols)
mass_cl = np.sum(density*cell_vols)

with open("{dump_file}", 'a') as txtfile:
    to_write = f"{{volume_cl:<14.3e}}{{mass_cl:<14.3e}}{{np.average(density):<14.3e}}\\n"
    txtfile.write(to_write)
print(f"Volume: {{volume_cl:.3f}}")
"""

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1514, 728]
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [176.67820739746094, -3.376218402073583e-11, -3.0442868592217565e-05]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [178.61005905003907, -3.376218402073583e-11, -3.0442868592217565e-05]
renderView1.CameraFocalPoint = [176.67820739746094, -3.376218402073583e-11, -3.0442868592217565e-05]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 0.5
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1514, 728)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

print(f'Working on: output-{label}/data.{file_no:04d}.flt.xmf')

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
cutoff_T_wind8e4 = Threshold(registrationName='Cutoff_T_wind>8e4', Input=calculator1_Twind)
cutoff_T_wind8e4.Scalars = ['CELLS', 'Twind']
cutoff_T_wind8e4.LowerThreshold = 428552.3125
cutoff_T_wind8e4.UpperThreshold = 90000.0
cutoff_T_wind8e4.ThresholdMethod = 'Above Upper Threshold'

# create a new 'Threshold'
cloud_material = Threshold(registrationName='cloud_material', Input=cutoff_T_wind8e4)
cloud_material.Scalars = ['CELLS', 'temperature']
cloud_material.LowerThreshold = 80000.0
cloud_material.UpperThreshold = 80000.0
cloud_material.ThresholdMethod = 'Below Lower Threshold'

# create a new 'Cell Size'
cloud_volume = CellSize(registrationName='cloud_volume', Input=cloud_material)
cloud_volume.ComputeSum = 1

# create a new 'Programmable Filter'
programmableFilter2 = ProgrammableFilter(registrationName='ProgrammableFilter2', Input=cloud_volume)
programmableFilter2.Script = volume_script
programmableFilter2.RequestInformationScript = ''
programmableFilter2.RequestUpdateExtentScript = ''
programmableFilter2.PythonPath = ''

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=cloud_material)

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=extractSurface1)
cellSize1.ComputeSum = 1

# create a new 'Integrate Variables'
integrateVariables_surface = IntegrateVariables(registrationName='IntegrateVariables_surface', Input=cellSize1)

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(registrationName='ProgrammableFilter1', Input=integrateVariables_surface)
programmableFilter1.Script = area_script
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.PythonPath = ''
# print('Checkpoint 1')

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from programmableFilter1
programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')
# print('Checkpoint 2')

# show data from programmableFilter2
programmableFilter2Display = Show(programmableFilter2, renderView1, 'UnstructuredGridRepresentation')
# print('Checkpoint 3')

ResetSession()
sys.exit(0)

'''
# hide data in view
Hide(programmableFilter2, renderView1)

# ----------------------------------------------------------------
# restore active source
SetActiveSource(cloud_material)
# ----------------------------------------------------------------

if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
'''
