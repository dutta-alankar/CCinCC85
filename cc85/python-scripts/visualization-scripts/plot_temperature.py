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
renderView1.ViewSize = [1103, 700]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraFocalDisk = 1.0
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [1103, 332]
renderView2.InteractionMode = '2D'
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.CenterOfRotation = [325.14579010009766, 0.0, 0.0]
renderView2.StereoType = 'Crystal Eyes'
renderView2.CameraPosition = [325.14579010009766, 0.0, 1714.1147742013559]
renderView2.CameraFocalPoint = [325.14579010009766, 0.0, 0.0]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 122.00587779993208
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.OSPRayMaterialLibrary = materialLibrary1

# Create a new 'Render View'
renderView3 = CreateView('RenderView')
renderView3.ViewSize = [1103, 332]
renderView3.InteractionMode = '2D'
renderView3.AxesGrid = 'GridAxes3DActor'
renderView3.CenterOfRotation = [325.1457862854004, 0.0, 0.0]
renderView3.StereoType = 'Crystal Eyes'
renderView3.CameraPosition = [325.1457862854004, 0.0, 1211.4787353740596]
renderView3.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView3.CameraFocalDisk = 1.0
renderView3.CameraParallelScale = 100.75919457543668
renderView3.BackEnd = 'OSPRay raycaster'
renderView3.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(1103, 700)

# create new layout object 'Layout #1'
layout1_1 = CreateLayout(name='Layout #1')
layout1_1.SplitVertical(0, 0.500000)
layout1_1.AssignView(1, renderView3)
layout1_1.AssignView(2, renderView2)
layout1_1.SetSize(1103, 665)

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100

select = int(sys.argv[-2])
file_no = int(sys.argv[-1])

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView3)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'Text'
text1 = Text(registrationName='Text1')
text1.Text = '$t/t_{\\rm cc, ini} = $' + f'{file_no:.1f}'

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
clip1.ClipType.Radius = 60.0

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [325.1457862854004, 0.0, 0.00019073486328125]

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=clip1)
calculator2.AttributeType = 'Cell Data'
calculator2.ResultArrayName = 'delPrsByPrsWind'
calculator2.Function = 'delRhoByRhoWind + delTbyTwind + delRhoByRhoWind*delTbyTwind'

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator2)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [334.0, 0.0, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=clip1)
calculator1.AttributeType = 'Cell Data'
calculator1.ResultArrayName = 'delvBcs'
calculator1.Function = """(1.48614e+00-vr)/sqrt(5/3*pressure/density)\r
"""

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=calculator1)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [325.1457862854004, 0.0, 0.0]
slice2.SliceType.Normal = [0.0, 0.0, 1.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice2.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView2'
# ----------------------------------------------------------------

# show data from slice1
slice1Display = Show(slice1, renderView2, 'GeometryRepresentation')

# get color transfer function/color map for 'delPrsByPrsWind'
delPrsByPrsWindLUT = GetColorTransferFunction('delPrsByPrsWind')
delPrsByPrsWindLUT.RGBPoints = [-0.9090826184044829, 0.231373, 0.298039, 0.752941, 0.8067498655415051, 0.865003, 0.865003, 0.865003, 2.522582349487493, 0.705882, 0.0156863, 0.14902]
delPrsByPrsWindLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['CELLS', 'delPrsByPrsWind']
slice1Display.LookupTable = delPrsByPrsWindLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 60.2170955657959
slice1Display.SelectScaleArray = 'delPrsByPrsWind'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'delPrsByPrsWind'
slice1Display.GaussianRadius = 3.010854778289795
slice1Display.SetScaleArray = [None, '']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = [None, '']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# setup the color legend parameters for each legend in this view

# get color legend/bar for delPrsByPrsWindLUT in view renderView2
delPrsByPrsWindLUTColorBar = GetScalarBar(delPrsByPrsWindLUT, renderView2)
delPrsByPrsWindLUTColorBar.Orientation = 'Horizontal'
delPrsByPrsWindLUTColorBar.WindowLocation = 'Any Location'
delPrsByPrsWindLUTColorBar.Position = [0.34067089755213037, 0.7697590361445784]
delPrsByPrsWindLUTColorBar.Title = 'delPrsByPrsWind'
delPrsByPrsWindLUTColorBar.ComponentTitle = ''
delPrsByPrsWindLUTColorBar.ScalarBarLength = 0.3300000000000008

# set color bar visibility
delPrsByPrsWindLUTColorBar.Visibility = 1

# show color legend
slice1Display.SetScalarBarVisibility(renderView2, True)

# ----------------------------------------------------------------
# setup the visualization in view 'renderView3'
# ----------------------------------------------------------------

# show data from slice2
slice2Display = Show(slice2, renderView3, 'GeometryRepresentation')

# get color transfer function/color map for 'temperature'
temperatureLUT = GetColorTransferFunction('temperature')
temperatureLUT.AutomaticRescaleRangeMode = 'Never'
temperatureLUT.RGBPoints = [40000.00000000001, 0.0, 0.0, 0.34902, 47006.176868037255, 0.039216, 0.062745, 0.380392, 55239.51659373012, 0.062745, 0.117647, 0.411765, 64914.96217774377, 0.090196, 0.184314, 0.45098, 76285.10483772444, 0.12549, 0.262745, 0.501961, 89646.77825997098, 0.160784, 0.337255, 0.541176, 105348.807863448, 0.2, 0.396078, 0.568627, 123801.11738165274, 0.239216, 0.454902, 0.6, 145485.43050256523, 0.286275, 0.521569, 0.65098, 170967.84694815305, 0.337255, 0.592157, 0.701961, 200913.6213098105, 0.388235, 0.654902, 0.74902, 236104.5304621702, 0.466667, 0.737255, 0.819608, 277459.2829562415, 0.572549, 0.819608, 0.878431, 326057.50320799695, 0.654902, 0.866667, 0.909804, 383167.91662364395, 0.752941, 0.917647, 0.941176, 450281.47147420887, 0.823529, 0.956863, 0.968627, 529150.2622129183, 0.988235, 0.960784, 0.901961, 529150.2622129183, 0.941176, 0.984314, 0.988235, 586732.0022026984, 0.988235, 0.945098, 0.85098, 650579.7445306143, 0.980392, 0.898039, 0.784314, 730750.1172521784, 0.968627, 0.835294, 0.698039, 858744.2314473712, 0.94902, 0.733333, 0.588235, 1009157.080695546, 0.929412, 0.65098, 0.509804, 1185915.4055701767, 0.909804, 0.564706, 0.435294, 1393633.7326190432, 0.878431, 0.458824, 0.352941, 1637734.843118845, 0.839216, 0.388235, 0.286275, 1924591.3424647916, 0.760784, 0.294118, 0.211765, 2261692.026064831, 0.701961, 0.211765, 0.168627, 2657837.3849558234, 0.65098, 0.156863, 0.129412, 3123369.3550928817, 0.6, 0.094118, 0.094118, 3670441.3082425855, 0.54902, 0.066667, 0.098039, 4313335.332975016, 0.501961, 0.05098, 0.12549, 5068835.088824469, 0.45098, 0.054902, 0.172549, 5956663.967504906, 0.4, 0.054902, 0.192157, 7000000.000000002, 0.34902, 0.070588, 0.211765]
temperatureLUT.UseLogScale = 1
temperatureLUT.ColorSpace = 'Lab'
temperatureLUT.NanColor = [0.25, 0.0, 0.0]
temperatureLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice2Display.Representation = 'Surface'
slice2Display.ColorArrayName = ['CELLS', 'temperature']
slice2Display.LookupTable = temperatureLUT
slice2Display.SelectTCoordArray = 'None'
slice2Display.SelectNormalArray = 'None'
slice2Display.SelectTangentArray = 'None'
slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice2Display.SelectOrientationVectors = 'None'
slice2Display.ScaleFactor = 60.2170955657959
slice2Display.SelectScaleArray = 'delvBcs'
slice2Display.GlyphType = 'Arrow'
slice2Display.GlyphTableIndexArray = 'delvBcs'
slice2Display.GaussianRadius = 3.010854778289795
slice2Display.SetScaleArray = ['POINTS', '']
slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
slice2Display.OpacityArray = ['POINTS', '']
slice2Display.OpacityTransferFunction = 'PiecewiseFunction'
slice2Display.DataAxesGrid = 'GridAxesRepresentation'
slice2Display.PolarAxes = 'PolarAxesRepresentation'

# show data from gridData
gridDataDisplay = Show(gridData, renderView3, 'StructuredGridRepresentation')

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
gridDataDisplay.SetScaleArray = ['POINTS', '']
gridDataDisplay.ScaleTransferFunction = 'PiecewiseFunction'
gridDataDisplay.OpacityArray = ['POINTS', '']
gridDataDisplay.OpacityTransferFunction = 'PiecewiseFunction'
gridDataDisplay.DataAxesGrid = 'GridAxesRepresentation'
gridDataDisplay.PolarAxes = 'PolarAxesRepresentation'
gridDataDisplay.ScalarOpacityUnitDistance = 1.7320408131091525

# show data from clip1
clip1Display = Show(clip1, renderView3, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'density'
densityLUT = GetColorTransferFunction('density')
densityLUT.RGBPoints = [0.0013335250550881028, 0.231373, 0.298039, 0.752941, 205.3405715476838, 0.865003, 0.865003, 0.865003, 410.6798095703125, 0.705882, 0.0156863, 0.14902]
densityLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'density'
densityPWF = GetOpacityTransferFunction('density')
densityPWF.Points = [0.0013335250550881028, 0.0, 0.5, 0.0, 115.39898681640625, 1.0, 0.5, 0.0]
densityPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
clip1Display.Representation = 'Outline'
clip1Display.ColorArrayName = ['POINTS', '']
clip1Display.LookupTable = densityLUT
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
clip1Display.SetScaleArray = ['POINTS', '']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = ['POINTS', '']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = densityPWF
clip1Display.ScalarOpacityUnitDistance = 1.7786614177350901
clip1Display.OpacityArrayName = ['CELLS', 'density']

# show data from text1
text1Display = Show(text1, renderView3, 'TextSourceRepresentation')

# trace defaults for the display properties.
text1Display.WindowLocation = 'Lower Center'
text1Display.FontSize = 25

# setup the color legend parameters for each legend in this view

# get color transfer function/color map for 'delvBcs'
delvBcsLUT = GetColorTransferFunction('delvBcs')
delvBcsLUT.AutomaticRescaleRangeMode = 'Never'
delvBcsLUT.RGBPoints = [-50.0, 0.0, 0.0, 0.34902, -46.875, 0.039216, 0.062745, 0.380392, -43.75, 0.062745, 0.117647, 0.411765, -40.625, 0.090196, 0.184314, 0.45098, -37.5, 0.12549, 0.262745, 0.501961, -34.375, 0.160784, 0.337255, 0.541176, -31.25, 0.2, 0.396078, 0.568627, -28.125, 0.239216, 0.454902, 0.6, -25.0, 0.286275, 0.521569, 0.65098, -21.875, 0.337255, 0.592157, 0.701961, -18.75, 0.388235, 0.654902, 0.74902, -15.625, 0.466667, 0.737255, 0.819608, -12.5, 0.572549, 0.819608, 0.878431, -9.375, 0.654902, 0.866667, 0.909804, -6.25, 0.752941, 0.917647, 0.941176, -3.125000000000007, 0.823529, 0.956863, 0.968627, 0.0, 0.988235, 0.960784, 0.901961, 0.0, 0.941176, 0.984314, 0.988235, 2.0, 0.988235, 0.945098, 0.85098, 4.0, 0.980392, 0.898039, 0.784314, 6.25, 0.968627, 0.835294, 0.698039, 9.375, 0.94902, 0.733333, 0.588235, 12.5, 0.929412, 0.65098, 0.509804, 15.625, 0.909804, 0.564706, 0.435294, 18.75, 0.878431, 0.458824, 0.352941, 21.875, 0.839216, 0.388235, 0.286275, 25.0, 0.760784, 0.294118, 0.211765, 28.125000000000014, 0.701961, 0.211765, 0.168627, 31.25, 0.65098, 0.156863, 0.129412, 34.375, 0.6, 0.094118, 0.094118, 37.5, 0.54902, 0.066667, 0.098039, 40.625, 0.501961, 0.05098, 0.12549, 43.749999999999986, 0.45098, 0.054902, 0.172549, 46.875, 0.4, 0.054902, 0.192157, 50.0, 0.34902, 0.070588, 0.211765]
delvBcsLUT.ColorSpace = 'Lab'
delvBcsLUT.NanColor = [0.25, 0.0, 0.0]
delvBcsLUT.ScalarRangeInitialized = 1.0

# get color legend/bar for delvBcsLUT in view renderView3
delvBcsLUTColorBar = GetScalarBar(delvBcsLUT, renderView3)
delvBcsLUTColorBar.Orientation = 'Horizontal'
delvBcsLUTColorBar.WindowLocation = 'Any Location'
delvBcsLUTColorBar.Position = [0.033327289211242034, 0.8080966767371603]
delvBcsLUTColorBar.Title = 'delvBcs'
delvBcsLUTColorBar.ComponentTitle = ''
delvBcsLUTColorBar.ScalarBarLength = 0.9274614687216712

# set color bar visibility
delvBcsLUTColorBar.Visibility = 0

# get color transfer function/color map for 'pressure'
pressureLUT = GetColorTransferFunction('pressure')
pressureLUT.RGBPoints = [4.331347099650881e-06, 0.267004, 0.004874, 0.329415, 4.546205236806739e-06, 0.26851, 0.009605, 0.335427, 4.771662591307253e-06, 0.269944, 0.014625, 0.341379, 5.008362747613648e-06, 0.271305, 0.019942, 0.347269, 5.256739615053322e-06, 0.272594, 0.025563, 0.353093, 5.517502203508735e-06, 0.273809, 0.031497, 0.358853, 5.7911285326023904e-06, 0.274952, 0.037752, 0.364543, 6.0783996886465435e-06, 0.276022, 0.044167, 0.370164, 6.3799210407673684e-06, 0.277018, 0.050344, 0.375715, 6.696316813692021e-06, 0.277941, 0.056324, 0.381191, 7.028490182229328e-06, 0.278791, 0.062145, 0.386592, 7.377050073408217e-06, 0.279566, 0.067836, 0.391917, 7.742991476858845e-06, 0.280267, 0.073417, 0.397163, 8.126985221830818e-06, 0.280894, 0.078907, 0.402329, 8.530127446474182e-06, 0.281446, 0.08432, 0.407414, 8.953267696074413e-06, 0.281924, 0.089666, 0.412415, 9.39728197694082e-06, 0.282327, 0.094955, 0.417331, 9.863437760220499e-06, 0.282656, 0.100196, 0.42216, 1.0352589584184735e-05, 0.28291, 0.105393, 0.426902, 1.0866133768389316e-05, 0.283091, 0.110553, 0.431554, 1.1405011721640392e-05, 0.283197, 0.11568, 0.436115, 1.1970761710356377e-05, 0.283229, 0.120777, 0.440584, 1.2564575944646506e-05, 0.283187, 0.125848, 0.44496, 1.3187683768720576e-05, 0.283072, 0.130895, 0.449241, 1.3841863889306213e-05, 0.282884, 0.13592, 0.453427, 1.4528315523423665e-05, 0.282623, 0.140926, 0.457517, 1.5248998197325961e-05, 0.28229, 0.145912, 0.46151, 1.600523303787334e-05, 0.281887, 0.150881, 0.465405, 1.6799178772570996e-05, 0.281412, 0.155834, 0.469201, 1.763229083121298e-05, 0.280868, 0.160771, 0.472899, 1.85069473929303e-05, 0.280255, 0.165693, 0.476498, 1.9424991629469817e-05, 0.279574, 0.170599, 0.479997, 2.0388324122362517e-05, 0.278826, 0.17549, 0.483397, 2.1399694774466054e-05, 0.278012, 0.180367, 0.486697, 2.2460957590299344e-05, 0.277134, 0.185228, 0.489898, 2.357514202196903e-05, 0.276194, 0.190074, 0.493001, 2.4744290548132014e-05, 0.275191, 0.194905, 0.496005, 2.5971740588523256e-05, 0.274128, 0.199721, 0.498911, 2.7260078759803814e-05, 0.273006, 0.20452, 0.501721, 2.861197224470457e-05, 0.271828, 0.209303, 0.504434, 3.0031280121773207e-05, 0.270595, 0.214069, 0.507052, 3.1520604209850314e-05, 0.269308, 0.218818, 0.509577, 3.3084195893163273e-05, 0.267968, 0.223549, 0.512008, 3.47249214858971e-05, 0.26658, 0.228262, 0.514349, 3.6447464558915884e-05, 0.265145, 0.232956, 0.516599, 3.8255455042941985e-05, 0.263663, 0.237631, 0.518762, 4.0152635931161894e-05, 0.262138, 0.242286, 0.520837, 4.214442286478405e-05, 0.260571, 0.246922, 0.522828, 4.423446710852348e-05, 0.258965, 0.251537, 0.524736, 4.642873484610229e-05, 0.257322, 0.25613, 0.526563, 4.8731248522004996e-05, 0.255645, 0.260703, 0.528312, 5.1148580829443744e-05, 0.253935, 0.265254, 0.529983, 5.368582583482924e-05, 0.252194, 0.269783, 0.531579, 5.6348236270878584e-05, 0.250425, 0.27429, 0.533103, 5.91434121823531e-05, 0.248629, 0.278775, 0.534556, 6.207647757474019e-05, 0.246811, 0.283237, 0.535941, 6.515580509711348e-05, 0.244972, 0.287675, 0.53726, 6.838703965040958e-05, 0.243113, 0.292092, 0.538516, 7.17794050293181e-05, 0.241237, 0.296485, 0.539709, 7.534004999633054e-05, 0.239346, 0.300855, 0.540844, 7.907634597843629e-05, 0.237441, 0.305202, 0.541921, 8.29989585050078e-05, 0.235526, 0.309527, 0.542944, 8.711507835356526e-05, 0.233603, 0.313828, 0.543914, 9.143645528840921e-05, 0.231674, 0.318106, 0.544834, 9.59710110861385e-05, 0.229739, 0.322361, 0.545706, 0.00010073168996698701, 0.227802, 0.326594, 0.546532, 0.00010572852415296433, 0.225863, 0.330805, 0.547314, 0.00011097185834249486, 0.223925, 0.334994, 0.548053, 0.00011647666001542339, 0.221989, 0.339161, 0.548752, 0.00012225302035558667, 0.220057, 0.343307, 0.549413, 0.00012831742840485057, 0.21813, 0.347432, 0.550038, 0.0001346810011952394, 0.21621, 0.351535, 0.550627, 0.00014136190400938442, 0.214298, 0.355619, 0.551184, 0.00014837421557469655, 0.212395, 0.359683, 0.55171, 0.00015573245313263296, 0.210503, 0.363727, 0.552206, 0.0001634576213089465, 0.208623, 0.367752, 0.552675, 0.0001715638815751786, 0.206756, 0.371758, 0.553117, 0.0001800743738424557, 0.204903, 0.375746, 0.553533, 0.00018900469920725893, 0.203063, 0.379716, 0.553925, 0.00019838034993463867, 0.201239, 0.38367, 0.554294, 0.00020821851309521007, 0.19943, 0.387607, 0.554642, 0.00021854727244322158, 0.197636, 0.391528, 0.554969, 0.00022938839386741554, 0.19586, 0.395433, 0.555276, 0.00024076432120473797, 0.1941, 0.399323, 0.555565, 0.0002527075278694305, 0.192357, 0.403199, 0.555836, 0.0002652399076736968, 0.190631, 0.407061, 0.556089, 0.00027839723520968636, 0.188923, 0.41091, 0.556326, 0.00029220362996777233, 0.187231, 0.414746, 0.556547, 0.0003066985033087059, 0.185556, 0.41857, 0.556753, 0.00032191240041122863, 0.183898, 0.422383, 0.556944, 0.00033787681785328057, 0.182256, 0.426184, 0.55712, 0.0003546373272287491, 0.180629, 0.429975, 0.557282, 0.0003722246532378774, 0.179019, 0.433756, 0.55743, 0.0003906890001854176, 0.177423, 0.437527, 0.557565, 0.00041006421617899357, 0.175841, 0.44129, 0.557685, 0.00043040560918571, 0.174274, 0.445044, 0.557792, 0.00045175604480850504, 0.172719, 0.448791, 0.557885, 0.00047415972379719924, 0.171176, 0.45253, 0.557965, 0.0004976805990873876, 0.169646, 0.456262, 0.55803, 0.000522361788213659, 0.168126, 0.459988, 0.558082, 0.0005482737454303963, 0.166617, 0.463708, 0.558119, 0.00057546397150863, 0.165117, 0.467423, 0.558141, 0.0006040100829317077, 0.163625, 0.471133, 0.558148, 0.000633972235180491, 0.162142, 0.474838, 0.55814, 0.0006654124574153691, 0.160665, 0.47854, 0.558115, 0.0006984204980436751, 0.159194, 0.482237, 0.558073, 0.000733056866094771, 0.157729, 0.485932, 0.558013, 0.0007694204336073199, 0.15627, 0.489624, 0.557936, 0.0008075778608293242, 0.154815, 0.493313, 0.55784, 0.0008476380709196427, 0.153364, 0.497, 0.557724, 0.0008896854831242355, 0.151918, 0.500685, 0.557587, 0.0009338071461188408, 0.150476, 0.504369, 0.55743, 0.0009801290084083117, 0.149039, 0.508051, 0.55725, 0.0010287359853912007, 0.147607, 0.511733, 0.557049, 0.0010797668292282523, 0.14618, 0.515413, 0.556823, 0.0011333150876360056, 0.144759, 0.519093, 0.556572, 0.0011895336180234059, 0.143343, 0.522773, 0.556295, 0.0012485408902120963, 0.141935, 0.526453, 0.555991, 0.0013104590640362628, 0.140536, 0.530132, 0.555659, 0.0013754648894388347, 0.139147, 0.533812, 0.555298, 0.0014436775325176255, 0.13777, 0.537492, 0.554906, 0.001515291711237108, 0.136408, 0.541173, 0.554483, 0.0015904387058659803, 0.135066, 0.544853, 0.554029, 0.0016693330289809522, 0.133743, 0.548535, 0.553541, 0.0017521409353084116, 0.132444, 0.552216, 0.553018, 0.0018390338579570514, 0.131172, 0.555899, 0.552459, 0.0019302598391117507, 0.129933, 0.559582, 0.551864, 0.0020259861106186683, 0.128729, 0.563265, 0.551229, 0.002126485930101216, 0.127568, 0.566949, 0.550556, 0.0022319435298377268, 0.126453, 0.570633, 0.549841, 0.0023426599462377583, 0.125394, 0.574318, 0.549086, 0.0024588381402394148, 0.124395, 0.578002, 0.548287, 0.002580809750970453, 0.123463, 0.581687, 0.547445, 0.0027088318103181976, 0.122606, 0.585371, 0.546557, 0.0028431693560138174, 0.121831, 0.589055, 0.545623, 0.0029842058643788486, 0.121148, 0.592739, 0.544641, 0.003132199877940004, 0.120565, 0.596422, 0.543611, 0.003287573856402333, 0.120092, 0.600104, 0.54253, 0.0034506126251733905, 0.119738, 0.603785, 0.5414, 0.003621781590309206, 0.119512, 0.607464, 0.540218, 0.0038014414577305818, 0.119423, 0.611141, 0.538982, 0.003989964168366178, 0.119483, 0.614817, 0.537692, 0.004187887874042613, 0.119699, 0.61849, 0.536347, 0.004395575400637784, 0.120081, 0.622161, 0.534946, 0.004613619607343208, 0.120638, 0.625828, 0.533488, 0.004842420204140262, 0.12138, 0.629492, 0.531973, 0.005082630319019153, 0.122312, 0.633153, 0.530398, 0.005334756148944996, 0.123444, 0.636809, 0.528763, 0.005599319657540866, 0.12478, 0.640461, 0.527068, 0.005877076060636899, 0.126326, 0.644107, 0.525311, 0.006168534530241791, 0.128087, 0.647749, 0.523491, 0.006474527055813391, 0.130067, 0.651384, 0.521608, 0.006795614570698883, 0.132268, 0.655014, 0.519661, 0.007132713642626712, 0.134692, 0.658636, 0.517649, 0.007486534643544536, 0.137339, 0.662252, 0.515571, 0.007857810071553055, 0.14021, 0.665859, 0.513427, 0.008247599759438968, 0.143303, 0.669459, 0.511215, 0.00865661825417994, 0.146616, 0.67305, 0.508936, 0.009086033128899277, 0.150148, 0.676631, 0.506589, 0.009536631569893669, 0.153894, 0.680203, 0.504172, 0.010009699843275467, 0.157851, 0.683765, 0.501686, 0.01050623485013023, 0.162016, 0.687316, 0.499129, 0.01102726454229945, 0.166383, 0.690856, 0.496502, 0.011574276237038562, 0.170948, 0.694384, 0.493803, 0.012148272694465062, 0.175707, 0.6979, 0.491033, 0.01275089242932876, 0.180653, 0.701402, 0.488189, 0.013383240140198116, 0.185783, 0.704891, 0.485273, 0.01404712090973153, 0.19109, 0.708366, 0.482284, 0.014743933739927328, 0.196571, 0.711827, 0.479221, 0.01547512120788903, 0.202219, 0.715272, 0.476084, 0.016242770541570053, 0.20803, 0.718701, 0.472873, 0.01704828896524628, 0.214, 0.722114, 0.469588, 0.017893975890005343, 0.220124, 0.725509, 0.466226, 0.018781381595536165, 0.226397, 0.728888, 0.462789, 0.019713039246144603, 0.232815, 0.732247, 0.459277, 0.020690912132491773, 0.239374, 0.735588, 0.455688, 0.021717024696400352, 0.24607, 0.73891, 0.452024, 0.02279430605101921, 0.252899, 0.742211, 0.448284, 0.023924731025749886, 0.259857, 0.745492, 0.444467, 0.025111526501125674, 0.266941, 0.748751, 0.440573, 0.026356868063485528, 0.274149, 0.751988, 0.436601, 0.027664310631143017, 0.281477, 0.755203, 0.432552, 0.029036250955895907, 0.288921, 0.758394, 0.428426, 0.030476605341458036, 0.296479, 0.761561, 0.424223, 0.0319884090597581, 0.304148, 0.764704, 0.419943, 0.03357479192318526, 0.311925, 0.767822, 0.415586, 0.035240282377319666, 0.319809, 0.770914, 0.411152, 0.03698793353312676, 0.327796, 0.77398, 0.40664, 0.038822734188288535, 0.335885, 0.777018, 0.402049, 0.04074804782650779, 0.344074, 0.780029, 0.397381, 0.04276937039597994, 0.35236, 0.783011, 0.392636, 0.04489096144818401, 0.360741, 0.785964, 0.387814, 0.047117213208036614, 0.369214, 0.788888, 0.382914, 0.049454480673548705, 0.377779, 0.791781, 0.377939, 0.05190704843062762, 0.386433, 0.794644, 0.372886, 0.05448191751280359, 0.395174, 0.797475, 0.367757, 0.05718380806783267, 0.404001, 0.800275, 0.362552, 0.06002043283935549, 0.412913, 0.803041, 0.357269, 0.06299776947261486, 0.421908, 0.805774, 0.35191, 0.06612198180023633, 0.430983, 0.808473, 0.346476, 0.06940198811416073, 0.440137, 0.811138, 0.340967, 0.07284380119171667, 0.449368, 0.813768, 0.335384, 0.07645724593934854, 0.458674, 0.816363, 0.329727, 0.0802489463804814, 0.468053, 0.818921, 0.323998, 0.08422972620055658, 0.477504, 0.821444, 0.318195, 0.08840797413318223, 0.487026, 0.823929, 0.312321, 0.09279234019819002, 0.496615, 0.826376, 0.306377, 0.09739533988826882, 0.506271, 0.828786, 0.300362, 0.10222541123966937, 0.515992, 0.831158, 0.294279, 0.10729634204332587, 0.525776, 0.833491, 0.288127, 0.11261742812822534, 0.535621, 0.835785, 0.281908, 0.11820385892266957, 0.545524, 0.838039, 0.275626, 0.12406740676320302, 0.555484, 0.840254, 0.269281, 0.1302202106626192, 0.565498, 0.84243, 0.262877, 0.13667983424837826, 0.575563, 0.844566, 0.256415, 0.14345811904593267, 0.585678, 0.846661, 0.249897, 0.15057441416358225, 0.595839, 0.848717, 0.243329, 0.15804176491095656, 0.606045, 0.850733, 0.236712, 0.16588148738536465, 0.616293, 0.852709, 0.230052, 0.17411010230545157, 0.626579, 0.854645, 0.223353, 0.1827446449652927, 0.636902, 0.856542, 0.21662, 0.19180976329663502, 0.647257, 0.8584, 0.209861, 0.20132207511443717, 0.657642, 0.860219, 0.203082, 0.21130873400652372, 0.668054, 0.861999, 0.196293, 0.22178804711941447, 0.678489, 0.863742, 0.189503, 0.23278992841665713, 0.688944, 0.865448, 0.182725, 0.24433756226301462, 0.699415, 0.867117, 0.175971, 0.2564548551531212, 0.709898, 0.868751, 0.169257, 0.2691763967832567, 0.720391, 0.87035, 0.162603, 0.2825255077783777, 0.730889, 0.871916, 0.156029, 0.29654029414938304, 0.741388, 0.873449, 0.149561, 0.3112464472461312, 0.751884, 0.874951, 0.143228, 0.32668594685517277, 0.762373, 0.876424, 0.137064, 0.3428870960541034, 0.772852, 0.877868, 0.131109, 0.3598961422048736, 0.783315, 0.879285, 0.125405, 0.3777489286255137, 0.79376, 0.880678, 0.120005, 0.39648241505586507, 0.804182, 0.882046, 0.114965, 0.4161500775991938, 0.814576, 0.883393, 0.110347, 0.4367879702334911, 0.82494, 0.88472, 0.106217, 0.45845500532842054, 0.83527, 0.886029, 0.102646, 0.48119090203234294, 0.845561, 0.887322, 0.099702, 0.5050605616205458, 0.85581, 0.888601, 0.097452, 0.5301142848443055, 0.866013, 0.889868, 0.095953, 0.5564039391864142, 0.876168, 0.891125, 0.09525, 0.5840045703825173, 0.886271, 0.892374, 0.095374, 0.612966774813731, 0.89632, 0.893616, 0.096335, 0.6433732272048424, 0.906311, 0.894855, 0.098125, 0.6752796674569651, 0.916242, 0.896091, 0.100717, 0.7087771748307625, 0.926106, 0.89733, 0.104071, 0.7439363389289291, 0.935904, 0.89857, 0.108131, 0.7808299480281781, 0.945636, 0.899815, 0.112838, 0.819563317626373, 0.9553, 0.901065, 0.118128, 0.8602074521985934, 0.964894, 0.902323, 0.123941, 0.9028783733911865, 0.974417, 0.90359, 0.130215, 0.9476543038424704, 0.983868, 0.904867, 0.136897, 0.9946630597114555, 0.993248, 0.906157, 0.143936]
pressureLUT.UseLogScale = 1
pressureLUT.NanColor = [1.0, 0.0, 0.0]
pressureLUT.ScalarRangeInitialized = 1.0

# get color legend/bar for pressureLUT in view renderView3
pressureLUTColorBar = GetScalarBar(pressureLUT, renderView3)
pressureLUTColorBar.Orientation = 'Horizontal'
pressureLUTColorBar.WindowLocation = 'Any Location'
pressureLUTColorBar.Position = [0.037860380779691706, 0.8059127143013138]
pressureLUTColorBar.Title = 'pressure'
pressureLUTColorBar.ComponentTitle = ''
pressureLUTColorBar.ScalarBarLength = 0.927461468721668

# set color bar visibility
pressureLUTColorBar.Visibility = 0

# get color legend/bar for densityLUT in view renderView3
densityLUTColorBar = GetScalarBar(densityLUT, renderView3)
densityLUTColorBar.Title = 'density'
densityLUTColorBar.ComponentTitle = ''

# set color bar visibility
densityLUTColorBar.Visibility = 0

# get color legend/bar for temperatureLUT in view renderView3
temperatureLUTColorBar = GetScalarBar(temperatureLUT, renderView3)
temperatureLUTColorBar.Orientation = 'Horizontal'
temperatureLUTColorBar.WindowLocation = 'Any Location'
temperatureLUTColorBar.Position = [0.030607434270172332, 0.8069535283993113]
temperatureLUTColorBar.Title = 'temperature'
temperatureLUTColorBar.ComponentTitle = ''
temperatureLUTColorBar.AutomaticLabelFormat = 0
temperatureLUTColorBar.LabelFormat = '%-#6.1e'
temperatureLUTColorBar.ScalarBarLength = 0.932901178603806

# set color bar visibility
temperatureLUTColorBar.Visibility = 1

# show color legend
slice2Display.SetScalarBarVisibility(renderView3, True)

# hide data in view
Hide(gridData, renderView3)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'delPrsByPrsWind'
delPrsByPrsWindPWF = GetOpacityTransferFunction('delPrsByPrsWind')
delPrsByPrsWindPWF.Points = [-0.9090826184044829, 0.0, 0.5, 0.0, 2.522582349487493, 1.0, 0.5, 0.0]
delPrsByPrsWindPWF.ScalarRangeInitialized = 1

# get color transfer function/color map for 'delRhoByRhoWind'
delRhoByRhoWindLUT = GetColorTransferFunction('delRhoByRhoWind')
delRhoByRhoWindLUT.AutomaticRescaleRangeMode = 'Never'
delRhoByRhoWindLUT.RGBPoints = [-20.0, 0.0, 0.0, 0.34902, -18.75, 0.039216, 0.062745, 0.380392, -17.5, 0.062745, 0.117647, 0.411765, -16.25, 0.090196, 0.184314, 0.45098, -15.0, 0.12549, 0.262745, 0.501961, -13.75, 0.160784, 0.337255, 0.541176, -12.5, 0.2, 0.396078, 0.568627, -11.25, 0.239216, 0.454902, 0.6, -10.0, 0.286275, 0.521569, 0.65098, -8.75, 0.337255, 0.592157, 0.701961, -7.5, 0.388235, 0.654902, 0.74902, -6.25, 0.466667, 0.737255, 0.819608, -5.0, 0.572549, 0.819608, 0.878431, -3.75, 0.654902, 0.866667, 0.909804, -2.5, 0.752941, 0.917647, 0.941176, -1.25, 0.823529, 0.956863, 0.968627, 0.0, 0.941176, 0.984314, 0.988235, 0.0, 0.988235, 0.960784, 0.901961, 0.8000000000000007, 0.988235, 0.945098, 0.85098, 1.6000000000000014, 0.980392, 0.898039, 0.784314, 2.5, 0.968627, 0.835294, 0.698039, 3.75, 0.94902, 0.733333, 0.588235, 5.0, 0.929412, 0.65098, 0.509804, 6.25, 0.909804, 0.564706, 0.435294, 7.5, 0.878431, 0.458824, 0.352941, 8.75, 0.839216, 0.388235, 0.286275, 10.0, 0.760784, 0.294118, 0.211765, 11.25, 0.701961, 0.211765, 0.168627, 12.5, 0.65098, 0.156863, 0.129412, 13.75, 0.6, 0.094118, 0.094118, 15.0, 0.54902, 0.066667, 0.098039, 16.25, 0.501961, 0.05098, 0.12549, 17.5, 0.45098, 0.054902, 0.172549, 18.75, 0.4, 0.054902, 0.192157, 20.0, 0.34902, 0.070588, 0.211765]
delRhoByRhoWindLUT.ColorSpace = 'Lab'
delRhoByRhoWindLUT.NanColor = [0.25, 0.0, 0.0]
delRhoByRhoWindLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'delRhoByRhoWind'
delRhoByRhoWindPWF = GetOpacityTransferFunction('delRhoByRhoWind')
delRhoByRhoWindPWF.Points = [-20.0, 0.0, 0.5, 0.0, 20.0, 1.0, 0.5, 0.0]
delRhoByRhoWindPWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'temperature'
temperaturePWF = GetOpacityTransferFunction('temperature')
temperaturePWF.Points = [40000.0, 0.0, 0.5, 0.0, 7000000.0, 1.0, 0.5, 0.0]
temperaturePWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'delvBcs'
delvBcsPWF = GetOpacityTransferFunction('delvBcs')
delvBcsPWF.Points = [-50.0, 0.0, 0.5, 0.0, 50.0, 1.0, 0.5, 0.0]
delvBcsPWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'pressure'
pressurePWF = GetOpacityTransferFunction('pressure')
pressurePWF.Points = [4.331347099650884e-06, 0.0, 0.5, 0.0, 0.9946630597114563, 1.0, 0.5, 0.0]
pressurePWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# restore active source
SetActiveSource(text1)
# ----------------------------------------------------------------

# reset view to fit data
renderView3.ResetCamera(True)

# save screenshot
screenshot_loc = f"{root}/output-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}/temperature"
os.makedirs(screenshot_loc, exist_ok = True)
print(f"Saving screenshot: {screenshot_loc}/screenshot-{file_no:04d}.png", end='\n')
SaveScreenshot(f'{screenshot_loc}/screenshot-{file_no:04d}.png', renderView3,
    ImageResolution=[1102, 332],
    FontScaling='Scale fonts proportionally',
    OverrideColorPalette='',
    StereoMode='No change',
    TransparentBackground=0, 
    # PNG options
    CompressionLevel='0',
    MetaData=['Application', 'ParaView'])

if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')