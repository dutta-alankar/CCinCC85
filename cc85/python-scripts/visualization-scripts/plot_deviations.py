# state file generated using paraview version 5.10.1

# uncomment the following three lines to ensure this script works in future versions
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

import os
import sys

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
renderView1.ViewSize = [1103, 332]
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [325.1457862854004, 0.0, 0.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView1.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 100.87470293261362
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [1103, 332]
renderView2.InteractionMode = '2D'
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.CenterOfRotation = [325.1457862854004, 0.0, 0.0]
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView2.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 100.87470293261362
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitVertical(0, 0.500000)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)
layout1.SetSize(1103, 665)

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100

select = int(sys.argv[-2])
file_no = int(sys.argv[-1])

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView2)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'XDMF Reader'
file_ext = "flt.xmf"
root = "/freya/ptmp/mpa/adutt/CCinCC85/cc85"
filename = f"{root}/output-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/data.{file_no:04d}.{file_ext}"
gridData = XDMFReader(registrationName='gridData', FileNames=[filename,])
gridData.CellArrayStatus = ['X', 'Y', 'Z', 'cellvol', 'delRhoByRhoWind', 'delTbyTwind', 'density', 'mach', 'ndens', 'pressure', 'temperature', 'tr1', 'vphi', 'vr', 'vth']
gridData.GridStatus = ['node_mesh']

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=gridData)
clip1.ClipType = 'Cylinder'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['CELLS', 'density']
clip1.Value = 57.70016017073067

# init the 'Cylinder' selected for 'ClipType'
clip1.ClipType.Center = [334.0, 0.0, 0.0]
clip1.ClipType.Axis = [1.0, 0.0, 0.0]
clip1.ClipType.Radius = 50.0

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [325.1457862854004, 0.0, 0.00019073486328125]

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=clip1)
calculator1.AttributeType = 'Cell Data'
calculator1.ResultArrayName = ' delPrsByPrsWind'
calculator1.Function = 'delRhoByRhoWind + delTbyTwind + delRhoByRhoWind*delTbyTwind'

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=calculator1)
calculator2.AttributeType = 'Cell Data'
calculator2.ResultArrayName = 'delvBcsw'
calculator2.Function = 'abs(1.48614e+00-vr)/sqrt(5/3*pressure/density)'

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=calculator2)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [325.1457862854004, 0.0, 0.0]
slice2.SliceType.Normal = [0.0, 0.0, 1.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice2.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]

# create a new 'Text'
text1 = Text(registrationName='Text1')
text1.Text = '$t/t_{\\rm cc, ini} = $' + f'{file_no:.1f}'

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [325.1457862854004, 0.0, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from text1
# text1Display = Show(text1, renderView1, 'TextSourceRepresentation')

# trace defaults for the display properties.
# text1Display.WindowLocation = 'Lower Center'
# text1Display.FontSize = 25

# show data from gridData
gridDataDisplay = Show(gridData, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
gridDataDisplay.Representation = 'Outline'
gridDataDisplay.ColorArrayName = ['CELLS', '']
gridDataDisplay.SelectTCoordArray = 'None'
gridDataDisplay.SelectNormalArray = 'None'
gridDataDisplay.SelectTangentArray = 'None'
gridDataDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
gridDataDisplay.SelectOrientationVectors = 'None'
gridDataDisplay.ScaleFactor = 60.370842742919926
gridDataDisplay.SelectScaleArray = 'density'
gridDataDisplay.GlyphType = 'Arrow'
gridDataDisplay.GlyphTableIndexArray = 'density'
gridDataDisplay.GaussianRadius = 3.018542137145996
gridDataDisplay.SetScaleArray = [None, '']
gridDataDisplay.ScaleTransferFunction = 'PiecewiseFunction'
gridDataDisplay.OpacityArray = [None, '']
gridDataDisplay.OpacityTransferFunction = 'PiecewiseFunction'
gridDataDisplay.DataAxesGrid = 'GridAxesRepresentation'
gridDataDisplay.PolarAxes = 'PolarAxesRepresentation'
gridDataDisplay.ScalarOpacityUnitDistance = 1.7320408131091525

# show data from clip1
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Outline'
clip1Display.ColorArrayName = ['POINTS', '']
clip1Display.SelectTCoordArray = 'None'
clip1Display.SelectNormalArray = 'None'
clip1Display.SelectTangentArray = 'None'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'None'
clip1Display.ScaleFactor = 60.370842742919926
clip1Display.SelectScaleArray = 'density'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'density'
clip1Display.GaussianRadius = 3.018542137145996
clip1Display.SetScaleArray = [None, '']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = [None, '']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityUnitDistance = 1.7786614177350901
clip1Display.OpacityArrayName = ['CELLS', 'density']

# show data from calculator1
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Outline'
calculator1Display.ColorArrayName = ['POINTS', '']
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'None'
calculator1Display.ScaleFactor = 60.370842742919926
calculator1Display.SelectScaleArray = ' delPrsByPrsWind'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = ' delPrsByPrsWind'
calculator1Display.GaussianRadius = 3.018542137145996
calculator1Display.SetScaleArray = [None, '']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = [None, '']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityUnitDistance = 1.7786614177350901
calculator1Display.OpacityArrayName = ['CELLS', ' delPrsByPrsWind']

# show data from calculator2
calculator2Display = Show(calculator2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator2Display.Representation = 'Outline'
calculator2Display.ColorArrayName = ['POINTS', '']
calculator2Display.SelectTCoordArray = 'None'
calculator2Display.SelectNormalArray = 'None'
calculator2Display.SelectTangentArray = 'None'
calculator2Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator2Display.SelectOrientationVectors = 'None'
calculator2Display.ScaleFactor = 60.370842742919926
calculator2Display.SelectScaleArray = 'delvBcsw'
calculator2Display.GlyphType = 'Arrow'
calculator2Display.GlyphTableIndexArray = 'delvBcsw'
calculator2Display.GaussianRadius = 3.018542137145996
calculator2Display.SetScaleArray = [None, '']
calculator2Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator2Display.OpacityArray = [None, '']
calculator2Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator2Display.DataAxesGrid = 'GridAxesRepresentation'
calculator2Display.PolarAxes = 'PolarAxesRepresentation'
calculator2Display.ScalarOpacityUnitDistance = 1.7786614177350901
calculator2Display.OpacityArrayName = ['CELLS', 'delvBcsw']

# show data from slice1
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'delPrsByPrsWind'
delPrsByPrsWindLUT = GetColorTransferFunction('delPrsByPrsWind')
delPrsByPrsWindLUT.AutomaticRescaleRangeMode = 'Never'
delPrsByPrsWindLUT.RGBPoints = [-20.0, 0.0, 0.0, 0.34902, -18.75, 0.039216, 0.062745, 0.380392, -17.5, 0.062745, 0.117647, 0.411765, -16.25, 0.090196, 0.184314, 0.45098, -15.0, 0.12549, 0.262745, 0.501961, -13.75, 0.160784, 0.337255, 0.541176, -12.5, 0.2, 0.396078, 0.568627, -11.25, 0.239216, 0.454902, 0.6, -10.0, 0.286275, 0.521569, 0.65098, -8.75, 0.337255, 0.592157, 0.701961, -7.5, 0.388235, 0.654902, 0.74902, -6.25, 0.466667, 0.737255, 0.819608, -5.0, 0.572549, 0.819608, 0.878431, -3.75, 0.654902, 0.866667, 0.909804, -2.5, 0.752941, 0.917647, 0.941176, -1.25, 0.823529, 0.956863, 0.968627, 0.0, 0.988235, 0.960784, 0.901961, 0.0, 0.941176, 0.984314, 0.988235, 0.8000000000000007, 0.988235, 0.945098, 0.85098, 1.6000000000000014, 0.980392, 0.898039, 0.784314, 2.5, 0.968627, 0.835294, 0.698039, 3.75, 0.94902, 0.733333, 0.588235, 5.0, 0.929412, 0.65098, 0.509804, 6.25, 0.909804, 0.564706, 0.435294, 7.5, 0.878431, 0.458824, 0.352941, 8.75, 0.839216, 0.388235, 0.286275, 10.0, 0.760784, 0.294118, 0.211765, 11.25, 0.701961, 0.211765, 0.168627, 12.5, 0.65098, 0.156863, 0.129412, 13.75, 0.6, 0.094118, 0.094118, 15.0, 0.54902, 0.066667, 0.098039, 16.25, 0.501961, 0.05098, 0.12549, 17.5, 0.45098, 0.054902, 0.172549, 18.75, 0.4, 0.054902, 0.192157, 20.0, 0.34902, 0.070588, 0.211765]
delPrsByPrsWindLUT.ColorSpace = 'Lab'
delPrsByPrsWindLUT.NanColor = [0.25, 0.0, 0.0]
delPrsByPrsWindLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['CELLS', ' delPrsByPrsWind']
slice1Display.LookupTable = delPrsByPrsWindLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 60.2170955657959
slice1Display.SelectScaleArray = ' delPrsByPrsWind'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = ' delPrsByPrsWind'
slice1Display.GaussianRadius = 3.010854778289795
slice1Display.SetScaleArray = [None, '']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = [None, '']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# setup the color legend parameters for each legend in this view

# get color transfer function/color map for 'density'
densityLUT = GetColorTransferFunction('density')
densityLUT.RGBPoints = [0.0013335250550881028, 0.231373, 0.298039, 0.752941, 57.70016017073067, 0.865003, 0.865003, 0.865003, 115.39898681640625, 0.705882, 0.0156863, 0.14902]
densityLUT.ScalarRangeInitialized = 1.0

# get color legend/bar for densityLUT in view renderView1
densityLUTColorBar = GetScalarBar(densityLUT, renderView1)
densityLUTColorBar.Title = 'density'
densityLUTColorBar.ComponentTitle = ''

# set color bar visibility
densityLUTColorBar.Visibility = 0

# get color legend/bar for delPrsByPrsWindLUT in view renderView1
delPrsByPrsWindLUTColorBar = GetScalarBar(delPrsByPrsWindLUT, renderView1)
delPrsByPrsWindLUTColorBar.Orientation = 'Horizontal'
delPrsByPrsWindLUTColorBar.WindowLocation = 'Any Location'
delPrsByPrsWindLUTColorBar.Position = [0.03967361740707158, 0.7667469879518075]
delPrsByPrsWindLUTColorBar.Title = ' delPrsByPrsWind'
delPrsByPrsWindLUTColorBar.ComponentTitle = ''
delPrsByPrsWindLUTColorBar.ScalarBarLength = 0.9202085222121487

# set color bar visibility
delPrsByPrsWindLUTColorBar.Visibility = 1

# get color transfer function/color map for 'delvBcsw'
delvBcswLUT = GetColorTransferFunction('delvBcsw')
delvBcswLUT.AutomaticRescaleRangeMode = 'Never'
delvBcswLUT.RGBPoints = [-50.0, 0.0, 0.0, 0.34902, -46.875, 0.039216, 0.062745, 0.380392, -43.75, 0.062745, 0.117647, 0.411765, -40.625, 0.090196, 0.184314, 0.45098, -37.5, 0.12549, 0.262745, 0.501961, -34.375, 0.160784, 0.337255, 0.541176, -31.25, 0.2, 0.396078, 0.568627, -28.125, 0.239216, 0.454902, 0.6, -25.0, 0.286275, 0.521569, 0.65098, -21.875, 0.337255, 0.592157, 0.701961, -18.75, 0.388235, 0.654902, 0.74902, -15.625, 0.466667, 0.737255, 0.819608, -12.5, 0.572549, 0.819608, 0.878431, -9.375, 0.654902, 0.866667, 0.909804, -6.25, 0.752941, 0.917647, 0.941176, -3.125, 0.823529, 0.956863, 0.968627, 0.0, 0.988235, 0.960784, 0.901961, 0.0, 0.941176, 0.984314, 0.988235, 2.0, 0.988235, 0.945098, 0.85098, 4.0, 0.980392, 0.898039, 0.784314, 6.25, 0.968627, 0.835294, 0.698039, 9.375, 0.94902, 0.733333, 0.588235, 12.5, 0.929412, 0.65098, 0.509804, 15.625, 0.909804, 0.564706, 0.435294, 18.75, 0.878431, 0.458824, 0.352941, 21.874999999999986, 0.839216, 0.388235, 0.286275, 25.0, 0.760784, 0.294118, 0.211765, 28.125000000000014, 0.701961, 0.211765, 0.168627, 31.25, 0.65098, 0.156863, 0.129412, 34.374999999999986, 0.6, 0.094118, 0.094118, 37.5, 0.54902, 0.066667, 0.098039, 40.625000000000014, 0.501961, 0.05098, 0.12549, 43.75, 0.45098, 0.054902, 0.172549, 46.874999999999986, 0.4, 0.054902, 0.192157, 50.0, 0.34902, 0.070588, 0.211765]
delvBcswLUT.ColorSpace = 'Lab'
delvBcswLUT.NanColor = [0.25, 0.0, 0.0]
delvBcswLUT.ScalarRangeInitialized = 1.0

# get color legend/bar for delvBcswLUT in view renderView1
delvBcswLUTColorBar = GetScalarBar(delvBcswLUT, renderView1)
delvBcswLUTColorBar.Title = 'delvBcsw'
delvBcswLUTColorBar.ComponentTitle = ''

# set color bar visibility
delvBcswLUTColorBar.Visibility = 0

# hide data in view
Hide(gridData, renderView1)

# hide data in view
Hide(clip1, renderView1)

# hide data in view
Hide(calculator1, renderView1)

# show color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# reset view to fit data
renderView1.ResetCamera(True)

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from text1
text1Display_1 = Show(text1, renderView2, 'TextSourceRepresentation')

# trace defaults for the display properties.
text1Display_1.WindowLocation = 'Lower Center'
text1Display_1.FontSize = 25

# show data from gridData
gridDataDisplay_1 = Show(gridData, renderView2, 'StructuredGridRepresentation')

# trace defaults for the display properties.
gridDataDisplay_1.Representation = 'Outline'
gridDataDisplay_1.ColorArrayName = ['CELLS', '']
gridDataDisplay_1.SelectTCoordArray = 'None'
gridDataDisplay_1.SelectNormalArray = 'None'
gridDataDisplay_1.SelectTangentArray = 'None'
gridDataDisplay_1.OSPRayScaleFunction = 'PiecewiseFunction'
gridDataDisplay_1.SelectOrientationVectors = 'None'
gridDataDisplay_1.ScaleFactor = 60.370842742919926
gridDataDisplay_1.SelectScaleArray = 'density'
gridDataDisplay_1.GlyphType = 'Arrow'
gridDataDisplay_1.GlyphTableIndexArray = 'density'
gridDataDisplay_1.GaussianRadius = 3.018542137145996
gridDataDisplay_1.SetScaleArray = [None, '']
gridDataDisplay_1.ScaleTransferFunction = 'PiecewiseFunction'
gridDataDisplay_1.OpacityArray = [None, '']
gridDataDisplay_1.OpacityTransferFunction = 'PiecewiseFunction'
gridDataDisplay_1.DataAxesGrid = 'GridAxesRepresentation'
gridDataDisplay_1.PolarAxes = 'PolarAxesRepresentation'
gridDataDisplay_1.ScalarOpacityUnitDistance = 1.7320408131091525

# show data from slice2
slice2Display = Show(slice2, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
slice2Display.Representation = 'Surface'
slice2Display.ColorArrayName = ['CELLS', 'delvBcsw']
slice2Display.LookupTable = delvBcswLUT
slice2Display.SelectTCoordArray = 'None'
slice2Display.SelectNormalArray = 'None'
slice2Display.SelectTangentArray = 'None'
slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice2Display.SelectOrientationVectors = 'None'
slice2Display.ScaleFactor = 9.998966217041016
slice2Display.SelectScaleArray = 'delvBcsw'
slice2Display.GlyphType = 'Arrow'
slice2Display.GlyphTableIndexArray = 'delvBcsw'
slice2Display.GaussianRadius = 0.49994831085205077
slice2Display.SetScaleArray = [None, '']
slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
slice2Display.OpacityArray = [None, '']
slice2Display.OpacityTransferFunction = 'PiecewiseFunction'
slice2Display.DataAxesGrid = 'GridAxesRepresentation'
slice2Display.PolarAxes = 'PolarAxesRepresentation'

# show data from clip1
clip1Display_1 = Show(clip1, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display_1.Representation = 'Outline'
clip1Display_1.ColorArrayName = ['POINTS', '']
clip1Display_1.SelectTCoordArray = 'None'
clip1Display_1.SelectNormalArray = 'None'
clip1Display_1.SelectTangentArray = 'None'
clip1Display_1.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display_1.SelectOrientationVectors = 'None'
clip1Display_1.ScaleFactor = 60.370842742919926
clip1Display_1.SelectScaleArray = 'density'
clip1Display_1.GlyphType = 'Arrow'
clip1Display_1.GlyphTableIndexArray = 'density'
clip1Display_1.GaussianRadius = 3.018542137145996
clip1Display_1.SetScaleArray = [None, '']
clip1Display_1.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display_1.OpacityArray = [None, '']
clip1Display_1.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display_1.DataAxesGrid = 'GridAxesRepresentation'
clip1Display_1.PolarAxes = 'PolarAxesRepresentation'
clip1Display_1.ScalarOpacityUnitDistance = 1.7786614177350901
clip1Display_1.OpacityArrayName = ['CELLS', 'density']

# setup the color legend parameters for each legend in this view

# get color legend/bar for delvBcswLUT in view renderView2
delvBcswLUTColorBar_1 = GetScalarBar(delvBcswLUT, renderView2)
delvBcswLUTColorBar_1.Orientation = 'Horizontal'
delvBcswLUTColorBar_1.WindowLocation = 'Any Location'
delvBcswLUTColorBar_1.Position = [0.03967361740707167, 0.7757831325301207]
delvBcswLUTColorBar_1.Title = 'delvrBycsw'
delvBcswLUTColorBar_1.ComponentTitle = ''
delvBcswLUTColorBar_1.ScalarBarLength = 0.9229283771532185

# set color bar visibility
delvBcswLUTColorBar_1.Visibility = 1

# get color legend/bar for densityLUT in view renderView2
densityLUTColorBar_1 = GetScalarBar(densityLUT, renderView2)
densityLUTColorBar_1.Title = 'density'
densityLUTColorBar_1.ComponentTitle = ''

# set color bar visibility
densityLUTColorBar_1.Visibility = 0

# hide data in view
Hide(gridData, renderView2)

# show color legend
slice2Display.SetScalarBarVisibility(renderView2, True)

# reset view to fit data
renderView2.ResetCamera(True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'delPrsByPrsWind'
delPrsByPrsWindPWF = GetOpacityTransferFunction('delPrsByPrsWind')
delPrsByPrsWindPWF.Points = [-20.0, 0.0, 0.5, 0.0, 20.0, 1.0, 0.5, 0.0]
delPrsByPrsWindPWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'density'
densityPWF = GetOpacityTransferFunction('density')
densityPWF.Points = [0.0013335250550881028, 0.0, 0.5, 0.0, 115.39898681640625, 1.0, 0.5, 0.0]
densityPWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'delvBcsw'
delvBcswPWF = GetOpacityTransferFunction('delvBcsw')
delvBcswPWF.Points = [-50.0, 0.0, 0.5, 0.0, 50.0, 1.0, 0.5, 0.0]
delvBcswPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# restore active source
SetActiveSource(text1)
# ----------------------------------------------------------------

# save screenshot
screenshot_loc = f"{root}/output-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/deviations"
os.makedirs(screenshot_loc, exist_ok = True)
print(f"Saving screenshot: {screenshot_loc}/screenshot-{file_no:04d}.png", end='\n')
SaveScreenshot(f'{screenshot_loc}/screenshot-{file_no:04d}.png', layout1, SaveAllViews=1,
    ImageResolution=[1102, 664],
    FontScaling='Scale fonts proportionally',
    SeparatorWidth=1,
    SeparatorColor=[0.937, 0.922, 0.906],
    OverrideColorPalette='',
    StereoMode='No change',
    TransparentBackground=0, 
    # PNG options
    CompressionLevel='0',
    MetaData=['Application', 'ParaView'])


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
    sys.exit(0)