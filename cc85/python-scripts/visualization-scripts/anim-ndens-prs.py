# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10
import sys
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]
mach = 1.496
Tcl = 4.0e+04
chi = 100

select = 0 # int(sys.argv[-2])
file_no = 0 # int(sys.argv[-1])

# create a new 'XDMF Reader'
file_ext = "flt.h5"
root = "/freya/ptmp/mpa/adutt/CCinCC85/cc85"
filename = f"{root}/output-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}-no_cool/data.{file_no:04d}.{file_ext}"
data0000fltxmf = XDMFReader(registrationName=f'data.{int(sys.argv[-1]):04d}.flt.xmf', FileNames=[filename,])
data0000fltxmf.PointArrayStatus = []
data0000fltxmf.CellArrayStatus = ['X', 'Y', 'Z', 'cellvol', 'delRhoByRhoWind', 'delTbyTwind', 'density', 'mach', 'ndens', 'pressure', 'temperature', 'tr1', 'vphi', 'vr', 'vth']
data0000fltxmf.SetStatus = []
data0000fltxmf.GridStatus = ['node_mesh']
data0000fltxmf.Stride = [1, 1, 1]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
data0000fltxmfDisplay = Show(data0000fltxmf, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
data0000fltxmfDisplay.Selection = None
data0000fltxmfDisplay.Representation = 'Outline'
data0000fltxmfDisplay.ColorArrayName = ['CELLS', '']
data0000fltxmfDisplay.LookupTable = None
data0000fltxmfDisplay.MapScalars = 1
data0000fltxmfDisplay.MultiComponentsMapping = 0
data0000fltxmfDisplay.InterpolateScalarsBeforeMapping = 1
data0000fltxmfDisplay.Opacity = 1.0
data0000fltxmfDisplay.PointSize = 2.0
data0000fltxmfDisplay.LineWidth = 1.0
data0000fltxmfDisplay.RenderLinesAsTubes = 0
data0000fltxmfDisplay.RenderPointsAsSpheres = 0
data0000fltxmfDisplay.Interpolation = 'Gouraud'
data0000fltxmfDisplay.Specular = 0.0
data0000fltxmfDisplay.SpecularColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.SpecularPower = 100.0
data0000fltxmfDisplay.Luminosity = 0.0
data0000fltxmfDisplay.Ambient = 0.0
data0000fltxmfDisplay.Diffuse = 1.0
data0000fltxmfDisplay.Roughness = 0.3
data0000fltxmfDisplay.Metallic = 0.0
data0000fltxmfDisplay.EdgeTint = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.Anisotropy = 0.0
data0000fltxmfDisplay.AnisotropyRotation = 0.0
data0000fltxmfDisplay.BaseIOR = 1.5
data0000fltxmfDisplay.CoatStrength = 0.0
data0000fltxmfDisplay.CoatIOR = 2.0
data0000fltxmfDisplay.CoatRoughness = 0.0
data0000fltxmfDisplay.CoatColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.SelectTCoordArray = 'None'
data0000fltxmfDisplay.SelectNormalArray = 'None'
data0000fltxmfDisplay.SelectTangentArray = 'None'
data0000fltxmfDisplay.Texture = None
data0000fltxmfDisplay.RepeatTextures = 1
data0000fltxmfDisplay.InterpolateTextures = 0
data0000fltxmfDisplay.SeamlessU = 0
data0000fltxmfDisplay.SeamlessV = 0
data0000fltxmfDisplay.UseMipmapTextures = 0
data0000fltxmfDisplay.ShowTexturesOnBackface = 1
data0000fltxmfDisplay.BaseColorTexture = None
data0000fltxmfDisplay.NormalTexture = None
data0000fltxmfDisplay.NormalScale = 1.0
data0000fltxmfDisplay.CoatNormalTexture = None
data0000fltxmfDisplay.CoatNormalScale = 1.0
data0000fltxmfDisplay.MaterialTexture = None
data0000fltxmfDisplay.OcclusionStrength = 1.0
data0000fltxmfDisplay.AnisotropyTexture = None
data0000fltxmfDisplay.EmissiveTexture = None
data0000fltxmfDisplay.EmissiveFactor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.FlipTextures = 0
data0000fltxmfDisplay.BackfaceRepresentation = 'Follow Frontface'
data0000fltxmfDisplay.BackfaceAmbientColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.BackfaceOpacity = 1.0
data0000fltxmfDisplay.Position = [0.0, 0.0, 0.0]
data0000fltxmfDisplay.Scale = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.Orientation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay.Origin = [0.0, 0.0, 0.0]
data0000fltxmfDisplay.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
data0000fltxmfDisplay.Pickable = 1
data0000fltxmfDisplay.Triangulate = 0
data0000fltxmfDisplay.UseShaderReplacements = 0
data0000fltxmfDisplay.ShaderReplacements = ''
data0000fltxmfDisplay.NonlinearSubdivisionLevel = 1
data0000fltxmfDisplay.UseDataPartitions = 0
data0000fltxmfDisplay.OSPRayUseScaleArray = 'All Approximate'
data0000fltxmfDisplay.OSPRayScaleArray = ''
data0000fltxmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
data0000fltxmfDisplay.OSPRayMaterial = 'None'
data0000fltxmfDisplay.BlockSelectors = ['/']
data0000fltxmfDisplay.BlockColors = []
data0000fltxmfDisplay.BlockOpacities = []
data0000fltxmfDisplay.Orient = 0
data0000fltxmfDisplay.OrientationMode = 'Direction'
data0000fltxmfDisplay.SelectOrientationVectors = 'None'
data0000fltxmfDisplay.Scaling = 0
data0000fltxmfDisplay.ScaleMode = 'No Data Scaling Off'
data0000fltxmfDisplay.ScaleFactor = 60.370842742919926
data0000fltxmfDisplay.SelectScaleArray = 'density'
data0000fltxmfDisplay.GlyphType = 'Arrow'
data0000fltxmfDisplay.UseGlyphTable = 0
data0000fltxmfDisplay.GlyphTableIndexArray = 'density'
data0000fltxmfDisplay.UseCompositeGlyphTable = 0
data0000fltxmfDisplay.UseGlyphCullingAndLOD = 0
data0000fltxmfDisplay.LODValues = []
data0000fltxmfDisplay.ColorByLODIndex = 0
data0000fltxmfDisplay.GaussianRadius = 3.018542137145996
data0000fltxmfDisplay.ShaderPreset = 'Sphere'
data0000fltxmfDisplay.CustomTriangleScale = 3
data0000fltxmfDisplay.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
data0000fltxmfDisplay.Emissive = 0
data0000fltxmfDisplay.ScaleByArray = 0
data0000fltxmfDisplay.SetScaleArray = [None, '']
data0000fltxmfDisplay.ScaleArrayComponent = 0
data0000fltxmfDisplay.UseScaleFunction = 1
data0000fltxmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
data0000fltxmfDisplay.OpacityByArray = 0
data0000fltxmfDisplay.OpacityArray = [None, '']
data0000fltxmfDisplay.OpacityArrayComponent = 0
data0000fltxmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
data0000fltxmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
data0000fltxmfDisplay.SelectionCellLabelBold = 0
data0000fltxmfDisplay.SelectionCellLabelColor = [0.0, 1.0, 0.0]
data0000fltxmfDisplay.SelectionCellLabelFontFamily = 'Arial'
data0000fltxmfDisplay.SelectionCellLabelFontFile = ''
data0000fltxmfDisplay.SelectionCellLabelFontSize = 18
data0000fltxmfDisplay.SelectionCellLabelItalic = 0
data0000fltxmfDisplay.SelectionCellLabelJustification = 'Left'
data0000fltxmfDisplay.SelectionCellLabelOpacity = 1.0
data0000fltxmfDisplay.SelectionCellLabelShadow = 0
data0000fltxmfDisplay.SelectionPointLabelBold = 0
data0000fltxmfDisplay.SelectionPointLabelColor = [1.0, 1.0, 0.0]
data0000fltxmfDisplay.SelectionPointLabelFontFamily = 'Arial'
data0000fltxmfDisplay.SelectionPointLabelFontFile = ''
data0000fltxmfDisplay.SelectionPointLabelFontSize = 18
data0000fltxmfDisplay.SelectionPointLabelItalic = 0
data0000fltxmfDisplay.SelectionPointLabelJustification = 'Left'
data0000fltxmfDisplay.SelectionPointLabelOpacity = 1.0
data0000fltxmfDisplay.SelectionPointLabelShadow = 0
data0000fltxmfDisplay.PolarAxes = 'PolarAxesRepresentation'
data0000fltxmfDisplay.ScalarOpacityFunction = None
data0000fltxmfDisplay.ScalarOpacityUnitDistance = 1.7320408131091525
data0000fltxmfDisplay.SelectMapper = 'Projected tetra'
data0000fltxmfDisplay.SamplingDimensions = [128, 128, 128]

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
data0000fltxmfDisplay.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
data0000fltxmfDisplay.GlyphType.TipResolution = 6
data0000fltxmfDisplay.GlyphType.TipRadius = 0.1
data0000fltxmfDisplay.GlyphType.TipLength = 0.35
data0000fltxmfDisplay.GlyphType.ShaftResolution = 6
data0000fltxmfDisplay.GlyphType.ShaftRadius = 0.03
data0000fltxmfDisplay.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
data0000fltxmfDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
data0000fltxmfDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
data0000fltxmfDisplay.DataAxesGrid.XTitle = 'X Axis'
data0000fltxmfDisplay.DataAxesGrid.YTitle = 'Y Axis'
data0000fltxmfDisplay.DataAxesGrid.ZTitle = 'Z Axis'
data0000fltxmfDisplay.DataAxesGrid.XTitleFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.XTitleFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.XTitleBold = 0
data0000fltxmfDisplay.DataAxesGrid.XTitleItalic = 0
data0000fltxmfDisplay.DataAxesGrid.XTitleFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.XTitleShadow = 0
data0000fltxmfDisplay.DataAxesGrid.XTitleOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.YTitleFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.YTitleFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.YTitleBold = 0
data0000fltxmfDisplay.DataAxesGrid.YTitleItalic = 0
data0000fltxmfDisplay.DataAxesGrid.YTitleFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.YTitleShadow = 0
data0000fltxmfDisplay.DataAxesGrid.YTitleOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.ZTitleFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.ZTitleFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.ZTitleBold = 0
data0000fltxmfDisplay.DataAxesGrid.ZTitleItalic = 0
data0000fltxmfDisplay.DataAxesGrid.ZTitleFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.ZTitleShadow = 0
data0000fltxmfDisplay.DataAxesGrid.ZTitleOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.FacesToRender = 63
data0000fltxmfDisplay.DataAxesGrid.CullBackface = 0
data0000fltxmfDisplay.DataAxesGrid.CullFrontface = 1
data0000fltxmfDisplay.DataAxesGrid.ShowGrid = 0
data0000fltxmfDisplay.DataAxesGrid.ShowEdges = 1
data0000fltxmfDisplay.DataAxesGrid.ShowTicks = 1
data0000fltxmfDisplay.DataAxesGrid.LabelUniqueEdgesOnly = 1
data0000fltxmfDisplay.DataAxesGrid.AxesToLabel = 63
data0000fltxmfDisplay.DataAxesGrid.XLabelFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.XLabelFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.XLabelBold = 0
data0000fltxmfDisplay.DataAxesGrid.XLabelItalic = 0
data0000fltxmfDisplay.DataAxesGrid.XLabelFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.XLabelShadow = 0
data0000fltxmfDisplay.DataAxesGrid.XLabelOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.YLabelFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.YLabelFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.YLabelBold = 0
data0000fltxmfDisplay.DataAxesGrid.YLabelItalic = 0
data0000fltxmfDisplay.DataAxesGrid.YLabelFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.YLabelShadow = 0
data0000fltxmfDisplay.DataAxesGrid.YLabelOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.ZLabelFontFamily = 'Arial'
data0000fltxmfDisplay.DataAxesGrid.ZLabelFontFile = ''
data0000fltxmfDisplay.DataAxesGrid.ZLabelBold = 0
data0000fltxmfDisplay.DataAxesGrid.ZLabelItalic = 0
data0000fltxmfDisplay.DataAxesGrid.ZLabelFontSize = 12
data0000fltxmfDisplay.DataAxesGrid.ZLabelShadow = 0
data0000fltxmfDisplay.DataAxesGrid.ZLabelOpacity = 1.0
data0000fltxmfDisplay.DataAxesGrid.XAxisNotation = 'Mixed'
data0000fltxmfDisplay.DataAxesGrid.XAxisPrecision = 2
data0000fltxmfDisplay.DataAxesGrid.XAxisUseCustomLabels = 0
data0000fltxmfDisplay.DataAxesGrid.XAxisLabels = []
data0000fltxmfDisplay.DataAxesGrid.YAxisNotation = 'Mixed'
data0000fltxmfDisplay.DataAxesGrid.YAxisPrecision = 2
data0000fltxmfDisplay.DataAxesGrid.YAxisUseCustomLabels = 0
data0000fltxmfDisplay.DataAxesGrid.YAxisLabels = []
data0000fltxmfDisplay.DataAxesGrid.ZAxisNotation = 'Mixed'
data0000fltxmfDisplay.DataAxesGrid.ZAxisPrecision = 2
data0000fltxmfDisplay.DataAxesGrid.ZAxisUseCustomLabels = 0
data0000fltxmfDisplay.DataAxesGrid.ZAxisLabels = []
data0000fltxmfDisplay.DataAxesGrid.UseCustomBounds = 0
data0000fltxmfDisplay.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
data0000fltxmfDisplay.PolarAxes.Visibility = 0
data0000fltxmfDisplay.PolarAxes.Translation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay.PolarAxes.Scale = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.Orientation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay.PolarAxes.EnableCustomBounds = [0, 0, 0]
data0000fltxmfDisplay.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
data0000fltxmfDisplay.PolarAxes.EnableCustomRange = 0
data0000fltxmfDisplay.PolarAxes.CustomRange = [0.0, 1.0]
data0000fltxmfDisplay.PolarAxes.PolarAxisVisibility = 1
data0000fltxmfDisplay.PolarAxes.RadialAxesVisibility = 1
data0000fltxmfDisplay.PolarAxes.DrawRadialGridlines = 1
data0000fltxmfDisplay.PolarAxes.PolarArcsVisibility = 1
data0000fltxmfDisplay.PolarAxes.DrawPolarArcsGridlines = 1
data0000fltxmfDisplay.PolarAxes.NumberOfRadialAxes = 0
data0000fltxmfDisplay.PolarAxes.AutoSubdividePolarAxis = 1
data0000fltxmfDisplay.PolarAxes.NumberOfPolarAxis = 0
data0000fltxmfDisplay.PolarAxes.MinimumRadius = 0.0
data0000fltxmfDisplay.PolarAxes.MinimumAngle = 0.0
data0000fltxmfDisplay.PolarAxes.MaximumAngle = 90.0
data0000fltxmfDisplay.PolarAxes.RadialAxesOriginToPolarAxis = 1
data0000fltxmfDisplay.PolarAxes.Ratio = 1.0
data0000fltxmfDisplay.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleVisibility = 1
data0000fltxmfDisplay.PolarAxes.PolarAxisTitle = 'Radial Distance'
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleLocation = 'Bottom'
data0000fltxmfDisplay.PolarAxes.PolarLabelVisibility = 1
data0000fltxmfDisplay.PolarAxes.PolarLabelFormat = '%-#6.3g'
data0000fltxmfDisplay.PolarAxes.PolarLabelExponentLocation = 'Labels'
data0000fltxmfDisplay.PolarAxes.RadialLabelVisibility = 1
data0000fltxmfDisplay.PolarAxes.RadialLabelFormat = '%-#3.1f'
data0000fltxmfDisplay.PolarAxes.RadialLabelLocation = 'Bottom'
data0000fltxmfDisplay.PolarAxes.RadialUnitsVisibility = 1
data0000fltxmfDisplay.PolarAxes.ScreenSize = 10.0
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleOpacity = 1.0
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleBold = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleItalic = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleShadow = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisTitleFontSize = 12
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelOpacity = 1.0
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelBold = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelItalic = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelShadow = 0
data0000fltxmfDisplay.PolarAxes.PolarAxisLabelFontSize = 12
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextOpacity = 1.0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextBold = 0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextItalic = 0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextShadow = 0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTextFontSize = 12
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextBold = 0
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextItalic = 0
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextShadow = 0
data0000fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontSize = 12
data0000fltxmfDisplay.PolarAxes.EnableDistanceLOD = 1
data0000fltxmfDisplay.PolarAxes.DistanceLODThreshold = 0.7
data0000fltxmfDisplay.PolarAxes.EnableViewAngleLOD = 1
data0000fltxmfDisplay.PolarAxes.ViewAngleLODThreshold = 0.7
data0000fltxmfDisplay.PolarAxes.SmallestVisiblePolarAngle = 0.5
data0000fltxmfDisplay.PolarAxes.PolarTicksVisibility = 1
data0000fltxmfDisplay.PolarAxes.ArcTicksOriginToPolarAxis = 1
data0000fltxmfDisplay.PolarAxes.TickLocation = 'Both'
data0000fltxmfDisplay.PolarAxes.AxisTickVisibility = 1
data0000fltxmfDisplay.PolarAxes.AxisMinorTickVisibility = 0
data0000fltxmfDisplay.PolarAxes.ArcTickVisibility = 1
data0000fltxmfDisplay.PolarAxes.ArcMinorTickVisibility = 0
data0000fltxmfDisplay.PolarAxes.DeltaAngleMajor = 10.0
data0000fltxmfDisplay.PolarAxes.DeltaAngleMinor = 5.0
data0000fltxmfDisplay.PolarAxes.PolarAxisMajorTickSize = 0.0
data0000fltxmfDisplay.PolarAxes.PolarAxisTickRatioSize = 0.3
data0000fltxmfDisplay.PolarAxes.PolarAxisMajorTickThickness = 1.0
data0000fltxmfDisplay.PolarAxes.PolarAxisTickRatioThickness = 0.5
data0000fltxmfDisplay.PolarAxes.LastRadialAxisMajorTickSize = 0.0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTickRatioSize = 0.3
data0000fltxmfDisplay.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
data0000fltxmfDisplay.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
data0000fltxmfDisplay.PolarAxes.ArcMajorTickSize = 0.0
data0000fltxmfDisplay.PolarAxes.ArcTickRatioSize = 0.3
data0000fltxmfDisplay.PolarAxes.ArcMajorTickThickness = 1.0
data0000fltxmfDisplay.PolarAxes.ArcTickRatioThickness = 0.5
data0000fltxmfDisplay.PolarAxes.Use2DMode = 0
data0000fltxmfDisplay.PolarAxes.UseLogAxis = 0

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=data0000fltxmf)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = ['CELLS', 'density']
clip1.Value = 57.70016017073067
clip1.Invert = 1
clip1.Crinkleclip = 0
clip1.Exact = 0

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [325.1457862854004, 0.0, 0.00019073486328125]
clip1.ClipType.Normal = [1.0, 0.0, 0.0]
clip1.ClipType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [325.1457862854004, 0.0, 0.00019073486328125]
clip1.HyperTreeGridClipper.Normal = [1.0, 0.0, 0.0]
clip1.HyperTreeGridClipper.Offset = 0.0

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=clip1.ClipType)

# Properties modified on clip1
clip1.ClipType = 'Cylinder'

# Properties modified on clip1.ClipType
clip1.ClipType.Center = [334.0, 0.0, 0.0]
clip1.ClipType.Axis = [1.0, 0.0, 0.0]
clip1.ClipType.Radius = 50.0

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'density'
densityLUT = GetColorTransferFunction('density')
densityLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
densityLUT.InterpretValuesAsCategories = 0
densityLUT.AnnotationsInitialized = 0
densityLUT.ShowCategoricalColorsinDataRangeOnly = 0
densityLUT.RescaleOnVisibilityChange = 0
densityLUT.EnableOpacityMapping = 0
densityLUT.RGBPoints = [0.0013335250550881028, 0.231373, 0.298039, 0.752941, 57.70016017073067, 0.865003, 0.865003, 0.865003, 115.39898681640625, 0.705882, 0.0156863, 0.14902]
densityLUT.UseLogScale = 0
densityLUT.UseOpacityControlPointsFreehandDrawing = 0
densityLUT.ShowDataHistogram = 0
densityLUT.AutomaticDataHistogramComputation = 0
densityLUT.DataHistogramNumberOfBins = 10
densityLUT.ColorSpace = 'Diverging'
densityLUT.UseBelowRangeColor = 0
densityLUT.BelowRangeColor = [0.0, 0.0, 0.0]
densityLUT.UseAboveRangeColor = 0
densityLUT.AboveRangeColor = [0.5, 0.5, 0.5]
densityLUT.NanColor = [1.0, 1.0, 0.0]
densityLUT.NanOpacity = 1.0
densityLUT.Discretize = 1
densityLUT.NumberOfTableValues = 256
densityLUT.ScalarRangeInitialized = 1.0
densityLUT.HSVWrap = 0
densityLUT.VectorComponent = 0
densityLUT.VectorMode = 'Magnitude'
densityLUT.AllowDuplicateScalars = 1
densityLUT.Annotations = []
densityLUT.ActiveAnnotatedValues = []
densityLUT.IndexedColors = []
densityLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'density'
densityPWF = GetOpacityTransferFunction('density')
densityPWF.Points = [0.0013335250550881028, 0.0, 0.5, 0.0, 115.39898681640625, 1.0, 0.5, 0.0]
densityPWF.AllowDuplicateScalars = 1
densityPWF.UseLogScale = 0
densityPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
clip1Display.Selection = None
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['CELLS', 'density']
clip1Display.LookupTable = densityLUT
clip1Display.MapScalars = 1
clip1Display.MultiComponentsMapping = 0
clip1Display.InterpolateScalarsBeforeMapping = 1
clip1Display.Opacity = 1.0
clip1Display.PointSize = 2.0
clip1Display.LineWidth = 1.0
clip1Display.RenderLinesAsTubes = 0
clip1Display.RenderPointsAsSpheres = 0
clip1Display.Interpolation = 'Gouraud'
clip1Display.Specular = 0.0
clip1Display.SpecularColor = [1.0, 1.0, 1.0]
clip1Display.SpecularPower = 100.0
clip1Display.Luminosity = 0.0
clip1Display.Ambient = 0.0
clip1Display.Diffuse = 1.0
clip1Display.Roughness = 0.3
clip1Display.Metallic = 0.0
clip1Display.EdgeTint = [1.0, 1.0, 1.0]
clip1Display.Anisotropy = 0.0
clip1Display.AnisotropyRotation = 0.0
clip1Display.BaseIOR = 1.5
clip1Display.CoatStrength = 0.0
clip1Display.CoatIOR = 2.0
clip1Display.CoatRoughness = 0.0
clip1Display.CoatColor = [1.0, 1.0, 1.0]
clip1Display.SelectTCoordArray = 'None'
clip1Display.SelectNormalArray = 'None'
clip1Display.SelectTangentArray = 'None'
clip1Display.Texture = None
clip1Display.RepeatTextures = 1
clip1Display.InterpolateTextures = 0
clip1Display.SeamlessU = 0
clip1Display.SeamlessV = 0
clip1Display.UseMipmapTextures = 0
clip1Display.ShowTexturesOnBackface = 1
clip1Display.BaseColorTexture = None
clip1Display.NormalTexture = None
clip1Display.NormalScale = 1.0
clip1Display.CoatNormalTexture = None
clip1Display.CoatNormalScale = 1.0
clip1Display.MaterialTexture = None
clip1Display.OcclusionStrength = 1.0
clip1Display.AnisotropyTexture = None
clip1Display.EmissiveTexture = None
clip1Display.EmissiveFactor = [1.0, 1.0, 1.0]
clip1Display.FlipTextures = 0
clip1Display.BackfaceRepresentation = 'Follow Frontface'
clip1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
clip1Display.BackfaceOpacity = 1.0
clip1Display.Position = [0.0, 0.0, 0.0]
clip1Display.Scale = [1.0, 1.0, 1.0]
clip1Display.Orientation = [0.0, 0.0, 0.0]
clip1Display.Origin = [0.0, 0.0, 0.0]
clip1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
clip1Display.Pickable = 1
clip1Display.Triangulate = 0
clip1Display.UseShaderReplacements = 0
clip1Display.ShaderReplacements = ''
clip1Display.NonlinearSubdivisionLevel = 1
clip1Display.UseDataPartitions = 0
clip1Display.OSPRayUseScaleArray = 'All Approximate'
clip1Display.OSPRayScaleArray = ''
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.OSPRayMaterial = 'None'
clip1Display.BlockSelectors = ['/']
clip1Display.BlockColors = []
clip1Display.BlockOpacities = []
clip1Display.Orient = 0
clip1Display.OrientationMode = 'Direction'
clip1Display.SelectOrientationVectors = 'None'
clip1Display.Scaling = 0
clip1Display.ScaleMode = 'No Data Scaling Off'
clip1Display.ScaleFactor = 60.370842742919926
clip1Display.SelectScaleArray = 'density'
clip1Display.GlyphType = 'Arrow'
clip1Display.UseGlyphTable = 0
clip1Display.GlyphTableIndexArray = 'density'
clip1Display.UseCompositeGlyphTable = 0
clip1Display.UseGlyphCullingAndLOD = 0
clip1Display.LODValues = []
clip1Display.ColorByLODIndex = 0
clip1Display.GaussianRadius = 3.018542137145996
clip1Display.ShaderPreset = 'Sphere'
clip1Display.CustomTriangleScale = 3
clip1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
clip1Display.Emissive = 0
clip1Display.ScaleByArray = 0
clip1Display.SetScaleArray = [None, '']
clip1Display.ScaleArrayComponent = 0
clip1Display.UseScaleFunction = 1
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityByArray = 0
clip1Display.OpacityArray = [None, '']
clip1Display.OpacityArrayComponent = 0
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.SelectionCellLabelBold = 0
clip1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
clip1Display.SelectionCellLabelFontFamily = 'Arial'
clip1Display.SelectionCellLabelFontFile = ''
clip1Display.SelectionCellLabelFontSize = 18
clip1Display.SelectionCellLabelItalic = 0
clip1Display.SelectionCellLabelJustification = 'Left'
clip1Display.SelectionCellLabelOpacity = 1.0
clip1Display.SelectionCellLabelShadow = 0
clip1Display.SelectionPointLabelBold = 0
clip1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
clip1Display.SelectionPointLabelFontFamily = 'Arial'
clip1Display.SelectionPointLabelFontFile = ''
clip1Display.SelectionPointLabelFontSize = 18
clip1Display.SelectionPointLabelItalic = 0
clip1Display.SelectionPointLabelJustification = 'Left'
clip1Display.SelectionPointLabelOpacity = 1.0
clip1Display.SelectionPointLabelShadow = 0
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = densityPWF
clip1Display.ScalarOpacityUnitDistance = 1.7786614177350901
clip1Display.UseSeparateOpacityArray = 0
clip1Display.OpacityArrayName = ['CELLS', 'density']
clip1Display.OpacityComponent = ''
clip1Display.SelectMapper = 'Projected tetra'
clip1Display.SamplingDimensions = [128, 128, 128]
clip1Display.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
clip1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
clip1Display.GlyphType.TipResolution = 6
clip1Display.GlyphType.TipRadius = 0.1
clip1Display.GlyphType.TipLength = 0.35
clip1Display.GlyphType.ShaftResolution = 6
clip1Display.GlyphType.ShaftRadius = 0.03
clip1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip1Display.DataAxesGrid.XTitle = 'X Axis'
clip1Display.DataAxesGrid.YTitle = 'Y Axis'
clip1Display.DataAxesGrid.ZTitle = 'Z Axis'
clip1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.XTitleFontFile = ''
clip1Display.DataAxesGrid.XTitleBold = 0
clip1Display.DataAxesGrid.XTitleItalic = 0
clip1Display.DataAxesGrid.XTitleFontSize = 12
clip1Display.DataAxesGrid.XTitleShadow = 0
clip1Display.DataAxesGrid.XTitleOpacity = 1.0
clip1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.YTitleFontFile = ''
clip1Display.DataAxesGrid.YTitleBold = 0
clip1Display.DataAxesGrid.YTitleItalic = 0
clip1Display.DataAxesGrid.YTitleFontSize = 12
clip1Display.DataAxesGrid.YTitleShadow = 0
clip1Display.DataAxesGrid.YTitleOpacity = 1.0
clip1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
clip1Display.DataAxesGrid.ZTitleFontFile = ''
clip1Display.DataAxesGrid.ZTitleBold = 0
clip1Display.DataAxesGrid.ZTitleItalic = 0
clip1Display.DataAxesGrid.ZTitleFontSize = 12
clip1Display.DataAxesGrid.ZTitleShadow = 0
clip1Display.DataAxesGrid.ZTitleOpacity = 1.0
clip1Display.DataAxesGrid.FacesToRender = 63
clip1Display.DataAxesGrid.CullBackface = 0
clip1Display.DataAxesGrid.CullFrontface = 1
clip1Display.DataAxesGrid.ShowGrid = 0
clip1Display.DataAxesGrid.ShowEdges = 1
clip1Display.DataAxesGrid.ShowTicks = 1
clip1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
clip1Display.DataAxesGrid.AxesToLabel = 63
clip1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.XLabelFontFile = ''
clip1Display.DataAxesGrid.XLabelBold = 0
clip1Display.DataAxesGrid.XLabelItalic = 0
clip1Display.DataAxesGrid.XLabelFontSize = 12
clip1Display.DataAxesGrid.XLabelShadow = 0
clip1Display.DataAxesGrid.XLabelOpacity = 1.0
clip1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.YLabelFontFile = ''
clip1Display.DataAxesGrid.YLabelBold = 0
clip1Display.DataAxesGrid.YLabelItalic = 0
clip1Display.DataAxesGrid.YLabelFontSize = 12
clip1Display.DataAxesGrid.YLabelShadow = 0
clip1Display.DataAxesGrid.YLabelOpacity = 1.0
clip1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
clip1Display.DataAxesGrid.ZLabelFontFile = ''
clip1Display.DataAxesGrid.ZLabelBold = 0
clip1Display.DataAxesGrid.ZLabelItalic = 0
clip1Display.DataAxesGrid.ZLabelFontSize = 12
clip1Display.DataAxesGrid.ZLabelShadow = 0
clip1Display.DataAxesGrid.ZLabelOpacity = 1.0
clip1Display.DataAxesGrid.XAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.XAxisPrecision = 2
clip1Display.DataAxesGrid.XAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.XAxisLabels = []
clip1Display.DataAxesGrid.YAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.YAxisPrecision = 2
clip1Display.DataAxesGrid.YAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.YAxisLabels = []
clip1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
clip1Display.DataAxesGrid.ZAxisPrecision = 2
clip1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
clip1Display.DataAxesGrid.ZAxisLabels = []
clip1Display.DataAxesGrid.UseCustomBounds = 0
clip1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip1Display.PolarAxes.Visibility = 0
clip1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
clip1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
clip1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
clip1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
clip1Display.PolarAxes.EnableCustomRange = 0
clip1Display.PolarAxes.CustomRange = [0.0, 1.0]
clip1Display.PolarAxes.PolarAxisVisibility = 1
clip1Display.PolarAxes.RadialAxesVisibility = 1
clip1Display.PolarAxes.DrawRadialGridlines = 1
clip1Display.PolarAxes.PolarArcsVisibility = 1
clip1Display.PolarAxes.DrawPolarArcsGridlines = 1
clip1Display.PolarAxes.NumberOfRadialAxes = 0
clip1Display.PolarAxes.AutoSubdividePolarAxis = 1
clip1Display.PolarAxes.NumberOfPolarAxis = 0
clip1Display.PolarAxes.MinimumRadius = 0.0
clip1Display.PolarAxes.MinimumAngle = 0.0
clip1Display.PolarAxes.MaximumAngle = 90.0
clip1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
clip1Display.PolarAxes.Ratio = 1.0
clip1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
clip1Display.PolarAxes.PolarAxisTitleVisibility = 1
clip1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
clip1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
clip1Display.PolarAxes.PolarLabelVisibility = 1
clip1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
clip1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
clip1Display.PolarAxes.RadialLabelVisibility = 1
clip1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
clip1Display.PolarAxes.RadialLabelLocation = 'Bottom'
clip1Display.PolarAxes.RadialUnitsVisibility = 1
clip1Display.PolarAxes.ScreenSize = 10.0
clip1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
clip1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
clip1Display.PolarAxes.PolarAxisTitleFontFile = ''
clip1Display.PolarAxes.PolarAxisTitleBold = 0
clip1Display.PolarAxes.PolarAxisTitleItalic = 0
clip1Display.PolarAxes.PolarAxisTitleShadow = 0
clip1Display.PolarAxes.PolarAxisTitleFontSize = 12
clip1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
clip1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
clip1Display.PolarAxes.PolarAxisLabelFontFile = ''
clip1Display.PolarAxes.PolarAxisLabelBold = 0
clip1Display.PolarAxes.PolarAxisLabelItalic = 0
clip1Display.PolarAxes.PolarAxisLabelShadow = 0
clip1Display.PolarAxes.PolarAxisLabelFontSize = 12
clip1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
clip1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
clip1Display.PolarAxes.LastRadialAxisTextFontFile = ''
clip1Display.PolarAxes.LastRadialAxisTextBold = 0
clip1Display.PolarAxes.LastRadialAxisTextItalic = 0
clip1Display.PolarAxes.LastRadialAxisTextShadow = 0
clip1Display.PolarAxes.LastRadialAxisTextFontSize = 12
clip1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
clip1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
clip1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
clip1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
clip1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
clip1Display.PolarAxes.EnableDistanceLOD = 1
clip1Display.PolarAxes.DistanceLODThreshold = 0.7
clip1Display.PolarAxes.EnableViewAngleLOD = 1
clip1Display.PolarAxes.ViewAngleLODThreshold = 0.7
clip1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
clip1Display.PolarAxes.PolarTicksVisibility = 1
clip1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
clip1Display.PolarAxes.TickLocation = 'Both'
clip1Display.PolarAxes.AxisTickVisibility = 1
clip1Display.PolarAxes.AxisMinorTickVisibility = 0
clip1Display.PolarAxes.ArcTickVisibility = 1
clip1Display.PolarAxes.ArcMinorTickVisibility = 0
clip1Display.PolarAxes.DeltaAngleMajor = 10.0
clip1Display.PolarAxes.DeltaAngleMinor = 5.0
clip1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
clip1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
clip1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
clip1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
clip1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
clip1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
clip1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
clip1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
clip1Display.PolarAxes.ArcMajorTickSize = 0.0
clip1Display.PolarAxes.ArcTickRatioSize = 0.3
clip1Display.PolarAxes.ArcMajorTickThickness = 1.0
clip1Display.PolarAxes.ArcTickRatioThickness = 0.5
clip1Display.PolarAxes.Use2DMode = 0
clip1Display.PolarAxes.UseLogAxis = 0

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# turn off scalar coloring
ColorBy(clip1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(densityLUT, renderView1)

# change representation type
clip1Display.SetRepresentationType('Outline')

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=clip1)
calculator1.AttributeType = 'Cell Data'
calculator1.CoordinateResults = 0
calculator1.ResultNormals = 0
calculator1.ResultTCoords = 0
calculator1.ResultArrayName = 'Result'
calculator1.Function = ''
calculator1.ReplaceInvalidResults = 1
calculator1.ReplacementValue = 0.0
calculator1.ResultArrayType = 'Double'

# Properties modified on calculator1
calculator1.ResultArrayName = 'delvBcs'
calculator1.Function = """(1.48614e+00-vr)/sqrt(5/3*pressure/density)\r
"""

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'delvBcs'
delvBcsLUT = GetColorTransferFunction('delvBcs')
delvBcsLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
delvBcsLUT.InterpretValuesAsCategories = 0
delvBcsLUT.AnnotationsInitialized = 0
delvBcsLUT.ShowCategoricalColorsinDataRangeOnly = 0
delvBcsLUT.RescaleOnVisibilityChange = 0
delvBcsLUT.EnableOpacityMapping = 0
delvBcsLUT.RGBPoints = [-0.5219647675040819, 0.231373, 0.298039, 0.752941, 11.252601736802436, 0.865003, 0.865003, 0.865003, 23.027168241108956, 0.705882, 0.0156863, 0.14902]
delvBcsLUT.UseLogScale = 0
delvBcsLUT.UseOpacityControlPointsFreehandDrawing = 0
delvBcsLUT.ShowDataHistogram = 0
delvBcsLUT.AutomaticDataHistogramComputation = 0
delvBcsLUT.DataHistogramNumberOfBins = 10
delvBcsLUT.ColorSpace = 'Diverging'
delvBcsLUT.UseBelowRangeColor = 0
delvBcsLUT.BelowRangeColor = [0.0, 0.0, 0.0]
delvBcsLUT.UseAboveRangeColor = 0
delvBcsLUT.AboveRangeColor = [0.5, 0.5, 0.5]
delvBcsLUT.NanColor = [1.0, 1.0, 0.0]
delvBcsLUT.NanOpacity = 1.0
delvBcsLUT.Discretize = 1
delvBcsLUT.NumberOfTableValues = 256
delvBcsLUT.ScalarRangeInitialized = 1.0
delvBcsLUT.HSVWrap = 0
delvBcsLUT.VectorComponent = 0
delvBcsLUT.VectorMode = 'Magnitude'
delvBcsLUT.AllowDuplicateScalars = 1
delvBcsLUT.Annotations = []
delvBcsLUT.ActiveAnnotatedValues = []
delvBcsLUT.IndexedColors = []
delvBcsLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'delvBcs'
delvBcsPWF = GetOpacityTransferFunction('delvBcs')
delvBcsPWF.Points = [-0.5219647675040819, 0.0, 0.5, 0.0, 23.027168241108956, 1.0, 0.5, 0.0]
delvBcsPWF.AllowDuplicateScalars = 1
delvBcsPWF.UseLogScale = 0
delvBcsPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
calculator1Display.Selection = None
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = ['CELLS', 'delvBcs']
calculator1Display.LookupTable = delvBcsLUT
calculator1Display.MapScalars = 1
calculator1Display.MultiComponentsMapping = 0
calculator1Display.InterpolateScalarsBeforeMapping = 1
calculator1Display.Opacity = 1.0
calculator1Display.PointSize = 2.0
calculator1Display.LineWidth = 1.0
calculator1Display.RenderLinesAsTubes = 0
calculator1Display.RenderPointsAsSpheres = 0
calculator1Display.Interpolation = 'Gouraud'
calculator1Display.Specular = 0.0
calculator1Display.SpecularColor = [1.0, 1.0, 1.0]
calculator1Display.SpecularPower = 100.0
calculator1Display.Luminosity = 0.0
calculator1Display.Ambient = 0.0
calculator1Display.Diffuse = 1.0
calculator1Display.Roughness = 0.3
calculator1Display.Metallic = 0.0
calculator1Display.EdgeTint = [1.0, 1.0, 1.0]
calculator1Display.Anisotropy = 0.0
calculator1Display.AnisotropyRotation = 0.0
calculator1Display.BaseIOR = 1.5
calculator1Display.CoatStrength = 0.0
calculator1Display.CoatIOR = 2.0
calculator1Display.CoatRoughness = 0.0
calculator1Display.CoatColor = [1.0, 1.0, 1.0]
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.Texture = None
calculator1Display.RepeatTextures = 1
calculator1Display.InterpolateTextures = 0
calculator1Display.SeamlessU = 0
calculator1Display.SeamlessV = 0
calculator1Display.UseMipmapTextures = 0
calculator1Display.ShowTexturesOnBackface = 1
calculator1Display.BaseColorTexture = None
calculator1Display.NormalTexture = None
calculator1Display.NormalScale = 1.0
calculator1Display.CoatNormalTexture = None
calculator1Display.CoatNormalScale = 1.0
calculator1Display.MaterialTexture = None
calculator1Display.OcclusionStrength = 1.0
calculator1Display.AnisotropyTexture = None
calculator1Display.EmissiveTexture = None
calculator1Display.EmissiveFactor = [1.0, 1.0, 1.0]
calculator1Display.FlipTextures = 0
calculator1Display.BackfaceRepresentation = 'Follow Frontface'
calculator1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
calculator1Display.BackfaceOpacity = 1.0
calculator1Display.Position = [0.0, 0.0, 0.0]
calculator1Display.Scale = [1.0, 1.0, 1.0]
calculator1Display.Orientation = [0.0, 0.0, 0.0]
calculator1Display.Origin = [0.0, 0.0, 0.0]
calculator1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
calculator1Display.Pickable = 1
calculator1Display.Triangulate = 0
calculator1Display.UseShaderReplacements = 0
calculator1Display.ShaderReplacements = ''
calculator1Display.NonlinearSubdivisionLevel = 1
calculator1Display.UseDataPartitions = 0
calculator1Display.OSPRayUseScaleArray = 'All Approximate'
calculator1Display.OSPRayScaleArray = ''
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.OSPRayMaterial = 'None'
calculator1Display.BlockSelectors = ['/']
calculator1Display.BlockColors = []
calculator1Display.BlockOpacities = []
calculator1Display.Orient = 0
calculator1Display.OrientationMode = 'Direction'
calculator1Display.SelectOrientationVectors = 'None'
calculator1Display.Scaling = 0
calculator1Display.ScaleMode = 'No Data Scaling Off'
calculator1Display.ScaleFactor = 60.370842742919926
calculator1Display.SelectScaleArray = 'delvBcs'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.UseGlyphTable = 0
calculator1Display.GlyphTableIndexArray = 'delvBcs'
calculator1Display.UseCompositeGlyphTable = 0
calculator1Display.UseGlyphCullingAndLOD = 0
calculator1Display.LODValues = []
calculator1Display.ColorByLODIndex = 0
calculator1Display.GaussianRadius = 3.018542137145996
calculator1Display.ShaderPreset = 'Sphere'
calculator1Display.CustomTriangleScale = 3
calculator1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
calculator1Display.Emissive = 0
calculator1Display.ScaleByArray = 0
calculator1Display.SetScaleArray = [None, '']
calculator1Display.ScaleArrayComponent = 0
calculator1Display.UseScaleFunction = 1
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityByArray = 0
calculator1Display.OpacityArray = [None, '']
calculator1Display.OpacityArrayComponent = 0
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.SelectionCellLabelBold = 0
calculator1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
calculator1Display.SelectionCellLabelFontFamily = 'Arial'
calculator1Display.SelectionCellLabelFontFile = ''
calculator1Display.SelectionCellLabelFontSize = 18
calculator1Display.SelectionCellLabelItalic = 0
calculator1Display.SelectionCellLabelJustification = 'Left'
calculator1Display.SelectionCellLabelOpacity = 1.0
calculator1Display.SelectionCellLabelShadow = 0
calculator1Display.SelectionPointLabelBold = 0
calculator1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
calculator1Display.SelectionPointLabelFontFamily = 'Arial'
calculator1Display.SelectionPointLabelFontFile = ''
calculator1Display.SelectionPointLabelFontSize = 18
calculator1Display.SelectionPointLabelItalic = 0
calculator1Display.SelectionPointLabelJustification = 'Left'
calculator1Display.SelectionPointLabelOpacity = 1.0
calculator1Display.SelectionPointLabelShadow = 0
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityFunction = delvBcsPWF
calculator1Display.ScalarOpacityUnitDistance = 1.7786614177350901
calculator1Display.UseSeparateOpacityArray = 0
calculator1Display.OpacityArrayName = ['CELLS', 'delvBcs']
calculator1Display.OpacityComponent = ''
calculator1Display.SelectMapper = 'Projected tetra'
calculator1Display.SamplingDimensions = [128, 128, 128]
calculator1Display.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
calculator1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
calculator1Display.GlyphType.TipResolution = 6
calculator1Display.GlyphType.TipRadius = 0.1
calculator1Display.GlyphType.TipLength = 0.35
calculator1Display.GlyphType.ShaftResolution = 6
calculator1Display.GlyphType.ShaftRadius = 0.03
calculator1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
calculator1Display.DataAxesGrid.XTitle = 'X Axis'
calculator1Display.DataAxesGrid.YTitle = 'Y Axis'
calculator1Display.DataAxesGrid.ZTitle = 'Z Axis'
calculator1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
calculator1Display.DataAxesGrid.XTitleFontFile = ''
calculator1Display.DataAxesGrid.XTitleBold = 0
calculator1Display.DataAxesGrid.XTitleItalic = 0
calculator1Display.DataAxesGrid.XTitleFontSize = 12
calculator1Display.DataAxesGrid.XTitleShadow = 0
calculator1Display.DataAxesGrid.XTitleOpacity = 1.0
calculator1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
calculator1Display.DataAxesGrid.YTitleFontFile = ''
calculator1Display.DataAxesGrid.YTitleBold = 0
calculator1Display.DataAxesGrid.YTitleItalic = 0
calculator1Display.DataAxesGrid.YTitleFontSize = 12
calculator1Display.DataAxesGrid.YTitleShadow = 0
calculator1Display.DataAxesGrid.YTitleOpacity = 1.0
calculator1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
calculator1Display.DataAxesGrid.ZTitleFontFile = ''
calculator1Display.DataAxesGrid.ZTitleBold = 0
calculator1Display.DataAxesGrid.ZTitleItalic = 0
calculator1Display.DataAxesGrid.ZTitleFontSize = 12
calculator1Display.DataAxesGrid.ZTitleShadow = 0
calculator1Display.DataAxesGrid.ZTitleOpacity = 1.0
calculator1Display.DataAxesGrid.FacesToRender = 63
calculator1Display.DataAxesGrid.CullBackface = 0
calculator1Display.DataAxesGrid.CullFrontface = 1
calculator1Display.DataAxesGrid.ShowGrid = 0
calculator1Display.DataAxesGrid.ShowEdges = 1
calculator1Display.DataAxesGrid.ShowTicks = 1
calculator1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
calculator1Display.DataAxesGrid.AxesToLabel = 63
calculator1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
calculator1Display.DataAxesGrid.XLabelFontFile = ''
calculator1Display.DataAxesGrid.XLabelBold = 0
calculator1Display.DataAxesGrid.XLabelItalic = 0
calculator1Display.DataAxesGrid.XLabelFontSize = 12
calculator1Display.DataAxesGrid.XLabelShadow = 0
calculator1Display.DataAxesGrid.XLabelOpacity = 1.0
calculator1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
calculator1Display.DataAxesGrid.YLabelFontFile = ''
calculator1Display.DataAxesGrid.YLabelBold = 0
calculator1Display.DataAxesGrid.YLabelItalic = 0
calculator1Display.DataAxesGrid.YLabelFontSize = 12
calculator1Display.DataAxesGrid.YLabelShadow = 0
calculator1Display.DataAxesGrid.YLabelOpacity = 1.0
calculator1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
calculator1Display.DataAxesGrid.ZLabelFontFile = ''
calculator1Display.DataAxesGrid.ZLabelBold = 0
calculator1Display.DataAxesGrid.ZLabelItalic = 0
calculator1Display.DataAxesGrid.ZLabelFontSize = 12
calculator1Display.DataAxesGrid.ZLabelShadow = 0
calculator1Display.DataAxesGrid.ZLabelOpacity = 1.0
calculator1Display.DataAxesGrid.XAxisNotation = 'Mixed'
calculator1Display.DataAxesGrid.XAxisPrecision = 2
calculator1Display.DataAxesGrid.XAxisUseCustomLabels = 0
calculator1Display.DataAxesGrid.XAxisLabels = []
calculator1Display.DataAxesGrid.YAxisNotation = 'Mixed'
calculator1Display.DataAxesGrid.YAxisPrecision = 2
calculator1Display.DataAxesGrid.YAxisUseCustomLabels = 0
calculator1Display.DataAxesGrid.YAxisLabels = []
calculator1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
calculator1Display.DataAxesGrid.ZAxisPrecision = 2
calculator1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
calculator1Display.DataAxesGrid.ZAxisLabels = []
calculator1Display.DataAxesGrid.UseCustomBounds = 0
calculator1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
calculator1Display.PolarAxes.Visibility = 0
calculator1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
calculator1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
calculator1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
calculator1Display.PolarAxes.EnableCustomRange = 0
calculator1Display.PolarAxes.CustomRange = [0.0, 1.0]
calculator1Display.PolarAxes.PolarAxisVisibility = 1
calculator1Display.PolarAxes.RadialAxesVisibility = 1
calculator1Display.PolarAxes.DrawRadialGridlines = 1
calculator1Display.PolarAxes.PolarArcsVisibility = 1
calculator1Display.PolarAxes.DrawPolarArcsGridlines = 1
calculator1Display.PolarAxes.NumberOfRadialAxes = 0
calculator1Display.PolarAxes.AutoSubdividePolarAxis = 1
calculator1Display.PolarAxes.NumberOfPolarAxis = 0
calculator1Display.PolarAxes.MinimumRadius = 0.0
calculator1Display.PolarAxes.MinimumAngle = 0.0
calculator1Display.PolarAxes.MaximumAngle = 90.0
calculator1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
calculator1Display.PolarAxes.Ratio = 1.0
calculator1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
calculator1Display.PolarAxes.PolarAxisTitleVisibility = 1
calculator1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
calculator1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
calculator1Display.PolarAxes.PolarLabelVisibility = 1
calculator1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
calculator1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
calculator1Display.PolarAxes.RadialLabelVisibility = 1
calculator1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
calculator1Display.PolarAxes.RadialLabelLocation = 'Bottom'
calculator1Display.PolarAxes.RadialUnitsVisibility = 1
calculator1Display.PolarAxes.ScreenSize = 10.0
calculator1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
calculator1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
calculator1Display.PolarAxes.PolarAxisTitleFontFile = ''
calculator1Display.PolarAxes.PolarAxisTitleBold = 0
calculator1Display.PolarAxes.PolarAxisTitleItalic = 0
calculator1Display.PolarAxes.PolarAxisTitleShadow = 0
calculator1Display.PolarAxes.PolarAxisTitleFontSize = 12
calculator1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
calculator1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
calculator1Display.PolarAxes.PolarAxisLabelFontFile = ''
calculator1Display.PolarAxes.PolarAxisLabelBold = 0
calculator1Display.PolarAxes.PolarAxisLabelItalic = 0
calculator1Display.PolarAxes.PolarAxisLabelShadow = 0
calculator1Display.PolarAxes.PolarAxisLabelFontSize = 12
calculator1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
calculator1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
calculator1Display.PolarAxes.LastRadialAxisTextFontFile = ''
calculator1Display.PolarAxes.LastRadialAxisTextBold = 0
calculator1Display.PolarAxes.LastRadialAxisTextItalic = 0
calculator1Display.PolarAxes.LastRadialAxisTextShadow = 0
calculator1Display.PolarAxes.LastRadialAxisTextFontSize = 12
calculator1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
calculator1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
calculator1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
calculator1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
calculator1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
calculator1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
calculator1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
calculator1Display.PolarAxes.EnableDistanceLOD = 1
calculator1Display.PolarAxes.DistanceLODThreshold = 0.7
calculator1Display.PolarAxes.EnableViewAngleLOD = 1
calculator1Display.PolarAxes.ViewAngleLODThreshold = 0.7
calculator1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
calculator1Display.PolarAxes.PolarTicksVisibility = 1
calculator1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
calculator1Display.PolarAxes.TickLocation = 'Both'
calculator1Display.PolarAxes.AxisTickVisibility = 1
calculator1Display.PolarAxes.AxisMinorTickVisibility = 0
calculator1Display.PolarAxes.ArcTickVisibility = 1
calculator1Display.PolarAxes.ArcMinorTickVisibility = 0
calculator1Display.PolarAxes.DeltaAngleMajor = 10.0
calculator1Display.PolarAxes.DeltaAngleMinor = 5.0
calculator1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
calculator1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
calculator1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
calculator1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
calculator1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
calculator1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
calculator1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
calculator1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
calculator1Display.PolarAxes.ArcMajorTickSize = 0.0
calculator1Display.PolarAxes.ArcTickRatioSize = 0.3
calculator1Display.PolarAxes.ArcMajorTickThickness = 1.0
calculator1Display.PolarAxes.ArcTickRatioThickness = 0.5
calculator1Display.PolarAxes.Use2DMode = 0
calculator1Display.PolarAxes.UseLogAxis = 0

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(clip1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=clip1.ClipType)

# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=clip1)
calculator2.AttributeType = 'Cell Data'
calculator2.CoordinateResults = 0
calculator2.ResultNormals = 0
calculator2.ResultTCoords = 0
calculator2.ResultArrayName = 'Result'
calculator2.Function = ''
calculator2.ReplaceInvalidResults = 1
calculator2.ReplacementValue = 0.0
calculator2.ResultArrayType = 'Double'

# Properties modified on calculator2
calculator2.ResultArrayName = 'delPrsByPrsWind'
calculator2.Function = 'delRhoByRhoWind + delTbyTwind + delRhoByRhoWind*delTbyTwind'

# show data in view
calculator2Display = Show(calculator2, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'delPrsByPrsWind'
delPrsByPrsWindLUT = GetColorTransferFunction('delPrsByPrsWind')
delPrsByPrsWindLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
delPrsByPrsWindLUT.InterpretValuesAsCategories = 0
delPrsByPrsWindLUT.AnnotationsInitialized = 0
delPrsByPrsWindLUT.ShowCategoricalColorsinDataRangeOnly = 0
delPrsByPrsWindLUT.RescaleOnVisibilityChange = 0
delPrsByPrsWindLUT.EnableOpacityMapping = 0
delPrsByPrsWindLUT.RGBPoints = [-9.5367431640625e-07, 0.231373, 0.298039, 0.752941, -4.76837158203125e-07, 0.865003, 0.865003, 0.865003, 0.0, 0.705882, 0.0156863, 0.14902]
delPrsByPrsWindLUT.UseLogScale = 0
delPrsByPrsWindLUT.UseOpacityControlPointsFreehandDrawing = 0
delPrsByPrsWindLUT.ShowDataHistogram = 0
delPrsByPrsWindLUT.AutomaticDataHistogramComputation = 0
delPrsByPrsWindLUT.DataHistogramNumberOfBins = 10
delPrsByPrsWindLUT.ColorSpace = 'Diverging'
delPrsByPrsWindLUT.UseBelowRangeColor = 0
delPrsByPrsWindLUT.BelowRangeColor = [0.0, 0.0, 0.0]
delPrsByPrsWindLUT.UseAboveRangeColor = 0
delPrsByPrsWindLUT.AboveRangeColor = [0.5, 0.5, 0.5]
delPrsByPrsWindLUT.NanColor = [1.0, 1.0, 0.0]
delPrsByPrsWindLUT.NanOpacity = 1.0
delPrsByPrsWindLUT.Discretize = 1
delPrsByPrsWindLUT.NumberOfTableValues = 256
delPrsByPrsWindLUT.ScalarRangeInitialized = 1.0
delPrsByPrsWindLUT.HSVWrap = 0
delPrsByPrsWindLUT.VectorComponent = 0
delPrsByPrsWindLUT.VectorMode = 'Magnitude'
delPrsByPrsWindLUT.AllowDuplicateScalars = 1
delPrsByPrsWindLUT.Annotations = []
delPrsByPrsWindLUT.ActiveAnnotatedValues = []
delPrsByPrsWindLUT.IndexedColors = []
delPrsByPrsWindLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'delPrsByPrsWind'
delPrsByPrsWindPWF = GetOpacityTransferFunction('delPrsByPrsWind')
delPrsByPrsWindPWF.Points = [-9.5367431640625e-07, 0.0, 0.5, 0.0, 0.0, 1.0, 0.5, 0.0]
delPrsByPrsWindPWF.AllowDuplicateScalars = 1
delPrsByPrsWindPWF.UseLogScale = 0
delPrsByPrsWindPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
calculator2Display.Selection = None
calculator2Display.Representation = 'Surface'
calculator2Display.ColorArrayName = ['CELLS', 'delPrsByPrsWind']
calculator2Display.LookupTable = delPrsByPrsWindLUT
calculator2Display.MapScalars = 1
calculator2Display.MultiComponentsMapping = 0
calculator2Display.InterpolateScalarsBeforeMapping = 1
calculator2Display.Opacity = 1.0
calculator2Display.PointSize = 2.0
calculator2Display.LineWidth = 1.0
calculator2Display.RenderLinesAsTubes = 0
calculator2Display.RenderPointsAsSpheres = 0
calculator2Display.Interpolation = 'Gouraud'
calculator2Display.Specular = 0.0
calculator2Display.SpecularColor = [1.0, 1.0, 1.0]
calculator2Display.SpecularPower = 100.0
calculator2Display.Luminosity = 0.0
calculator2Display.Ambient = 0.0
calculator2Display.Diffuse = 1.0
calculator2Display.Roughness = 0.3
calculator2Display.Metallic = 0.0
calculator2Display.EdgeTint = [1.0, 1.0, 1.0]
calculator2Display.Anisotropy = 0.0
calculator2Display.AnisotropyRotation = 0.0
calculator2Display.BaseIOR = 1.5
calculator2Display.CoatStrength = 0.0
calculator2Display.CoatIOR = 2.0
calculator2Display.CoatRoughness = 0.0
calculator2Display.CoatColor = [1.0, 1.0, 1.0]
calculator2Display.SelectTCoordArray = 'None'
calculator2Display.SelectNormalArray = 'None'
calculator2Display.SelectTangentArray = 'None'
calculator2Display.Texture = None
calculator2Display.RepeatTextures = 1
calculator2Display.InterpolateTextures = 0
calculator2Display.SeamlessU = 0
calculator2Display.SeamlessV = 0
calculator2Display.UseMipmapTextures = 0
calculator2Display.ShowTexturesOnBackface = 1
calculator2Display.BaseColorTexture = None
calculator2Display.NormalTexture = None
calculator2Display.NormalScale = 1.0
calculator2Display.CoatNormalTexture = None
calculator2Display.CoatNormalScale = 1.0
calculator2Display.MaterialTexture = None
calculator2Display.OcclusionStrength = 1.0
calculator2Display.AnisotropyTexture = None
calculator2Display.EmissiveTexture = None
calculator2Display.EmissiveFactor = [1.0, 1.0, 1.0]
calculator2Display.FlipTextures = 0
calculator2Display.BackfaceRepresentation = 'Follow Frontface'
calculator2Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
calculator2Display.BackfaceOpacity = 1.0
calculator2Display.Position = [0.0, 0.0, 0.0]
calculator2Display.Scale = [1.0, 1.0, 1.0]
calculator2Display.Orientation = [0.0, 0.0, 0.0]
calculator2Display.Origin = [0.0, 0.0, 0.0]
calculator2Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
calculator2Display.Pickable = 1
calculator2Display.Triangulate = 0
calculator2Display.UseShaderReplacements = 0
calculator2Display.ShaderReplacements = ''
calculator2Display.NonlinearSubdivisionLevel = 1
calculator2Display.UseDataPartitions = 0
calculator2Display.OSPRayUseScaleArray = 'All Approximate'
calculator2Display.OSPRayScaleArray = ''
calculator2Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator2Display.OSPRayMaterial = 'None'
calculator2Display.BlockSelectors = ['/']
calculator2Display.BlockColors = []
calculator2Display.BlockOpacities = []
calculator2Display.Orient = 0
calculator2Display.OrientationMode = 'Direction'
calculator2Display.SelectOrientationVectors = 'None'
calculator2Display.Scaling = 0
calculator2Display.ScaleMode = 'No Data Scaling Off'
calculator2Display.ScaleFactor = 60.370842742919926
calculator2Display.SelectScaleArray = 'delPrsByPrsWind'
calculator2Display.GlyphType = 'Arrow'
calculator2Display.UseGlyphTable = 0
calculator2Display.GlyphTableIndexArray = 'delPrsByPrsWind'
calculator2Display.UseCompositeGlyphTable = 0
calculator2Display.UseGlyphCullingAndLOD = 0
calculator2Display.LODValues = []
calculator2Display.ColorByLODIndex = 0
calculator2Display.GaussianRadius = 3.018542137145996
calculator2Display.ShaderPreset = 'Sphere'
calculator2Display.CustomTriangleScale = 3
calculator2Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
calculator2Display.Emissive = 0
calculator2Display.ScaleByArray = 0
calculator2Display.SetScaleArray = [None, '']
calculator2Display.ScaleArrayComponent = 0
calculator2Display.UseScaleFunction = 1
calculator2Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator2Display.OpacityByArray = 0
calculator2Display.OpacityArray = [None, '']
calculator2Display.OpacityArrayComponent = 0
calculator2Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator2Display.DataAxesGrid = 'GridAxesRepresentation'
calculator2Display.SelectionCellLabelBold = 0
calculator2Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
calculator2Display.SelectionCellLabelFontFamily = 'Arial'
calculator2Display.SelectionCellLabelFontFile = ''
calculator2Display.SelectionCellLabelFontSize = 18
calculator2Display.SelectionCellLabelItalic = 0
calculator2Display.SelectionCellLabelJustification = 'Left'
calculator2Display.SelectionCellLabelOpacity = 1.0
calculator2Display.SelectionCellLabelShadow = 0
calculator2Display.SelectionPointLabelBold = 0
calculator2Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
calculator2Display.SelectionPointLabelFontFamily = 'Arial'
calculator2Display.SelectionPointLabelFontFile = ''
calculator2Display.SelectionPointLabelFontSize = 18
calculator2Display.SelectionPointLabelItalic = 0
calculator2Display.SelectionPointLabelJustification = 'Left'
calculator2Display.SelectionPointLabelOpacity = 1.0
calculator2Display.SelectionPointLabelShadow = 0
calculator2Display.PolarAxes = 'PolarAxesRepresentation'
calculator2Display.ScalarOpacityFunction = delPrsByPrsWindPWF
calculator2Display.ScalarOpacityUnitDistance = 1.7786614177350901
calculator2Display.UseSeparateOpacityArray = 0
calculator2Display.OpacityArrayName = ['CELLS', 'delPrsByPrsWind']
calculator2Display.OpacityComponent = ''
calculator2Display.SelectMapper = 'Projected tetra'
calculator2Display.SamplingDimensions = [128, 128, 128]
calculator2Display.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
calculator2Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator2Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
calculator2Display.GlyphType.TipResolution = 6
calculator2Display.GlyphType.TipRadius = 0.1
calculator2Display.GlyphType.TipLength = 0.35
calculator2Display.GlyphType.ShaftResolution = 6
calculator2Display.GlyphType.ShaftRadius = 0.03
calculator2Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator2Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
calculator2Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
calculator2Display.DataAxesGrid.XTitle = 'X Axis'
calculator2Display.DataAxesGrid.YTitle = 'Y Axis'
calculator2Display.DataAxesGrid.ZTitle = 'Z Axis'
calculator2Display.DataAxesGrid.XTitleFontFamily = 'Arial'
calculator2Display.DataAxesGrid.XTitleFontFile = ''
calculator2Display.DataAxesGrid.XTitleBold = 0
calculator2Display.DataAxesGrid.XTitleItalic = 0
calculator2Display.DataAxesGrid.XTitleFontSize = 12
calculator2Display.DataAxesGrid.XTitleShadow = 0
calculator2Display.DataAxesGrid.XTitleOpacity = 1.0
calculator2Display.DataAxesGrid.YTitleFontFamily = 'Arial'
calculator2Display.DataAxesGrid.YTitleFontFile = ''
calculator2Display.DataAxesGrid.YTitleBold = 0
calculator2Display.DataAxesGrid.YTitleItalic = 0
calculator2Display.DataAxesGrid.YTitleFontSize = 12
calculator2Display.DataAxesGrid.YTitleShadow = 0
calculator2Display.DataAxesGrid.YTitleOpacity = 1.0
calculator2Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
calculator2Display.DataAxesGrid.ZTitleFontFile = ''
calculator2Display.DataAxesGrid.ZTitleBold = 0
calculator2Display.DataAxesGrid.ZTitleItalic = 0
calculator2Display.DataAxesGrid.ZTitleFontSize = 12
calculator2Display.DataAxesGrid.ZTitleShadow = 0
calculator2Display.DataAxesGrid.ZTitleOpacity = 1.0
calculator2Display.DataAxesGrid.FacesToRender = 63
calculator2Display.DataAxesGrid.CullBackface = 0
calculator2Display.DataAxesGrid.CullFrontface = 1
calculator2Display.DataAxesGrid.ShowGrid = 0
calculator2Display.DataAxesGrid.ShowEdges = 1
calculator2Display.DataAxesGrid.ShowTicks = 1
calculator2Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
calculator2Display.DataAxesGrid.AxesToLabel = 63
calculator2Display.DataAxesGrid.XLabelFontFamily = 'Arial'
calculator2Display.DataAxesGrid.XLabelFontFile = ''
calculator2Display.DataAxesGrid.XLabelBold = 0
calculator2Display.DataAxesGrid.XLabelItalic = 0
calculator2Display.DataAxesGrid.XLabelFontSize = 12
calculator2Display.DataAxesGrid.XLabelShadow = 0
calculator2Display.DataAxesGrid.XLabelOpacity = 1.0
calculator2Display.DataAxesGrid.YLabelFontFamily = 'Arial'
calculator2Display.DataAxesGrid.YLabelFontFile = ''
calculator2Display.DataAxesGrid.YLabelBold = 0
calculator2Display.DataAxesGrid.YLabelItalic = 0
calculator2Display.DataAxesGrid.YLabelFontSize = 12
calculator2Display.DataAxesGrid.YLabelShadow = 0
calculator2Display.DataAxesGrid.YLabelOpacity = 1.0
calculator2Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
calculator2Display.DataAxesGrid.ZLabelFontFile = ''
calculator2Display.DataAxesGrid.ZLabelBold = 0
calculator2Display.DataAxesGrid.ZLabelItalic = 0
calculator2Display.DataAxesGrid.ZLabelFontSize = 12
calculator2Display.DataAxesGrid.ZLabelShadow = 0
calculator2Display.DataAxesGrid.ZLabelOpacity = 1.0
calculator2Display.DataAxesGrid.XAxisNotation = 'Mixed'
calculator2Display.DataAxesGrid.XAxisPrecision = 2
calculator2Display.DataAxesGrid.XAxisUseCustomLabels = 0
calculator2Display.DataAxesGrid.XAxisLabels = []
calculator2Display.DataAxesGrid.YAxisNotation = 'Mixed'
calculator2Display.DataAxesGrid.YAxisPrecision = 2
calculator2Display.DataAxesGrid.YAxisUseCustomLabels = 0
calculator2Display.DataAxesGrid.YAxisLabels = []
calculator2Display.DataAxesGrid.ZAxisNotation = 'Mixed'
calculator2Display.DataAxesGrid.ZAxisPrecision = 2
calculator2Display.DataAxesGrid.ZAxisUseCustomLabels = 0
calculator2Display.DataAxesGrid.ZAxisLabels = []
calculator2Display.DataAxesGrid.UseCustomBounds = 0
calculator2Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
calculator2Display.PolarAxes.Visibility = 0
calculator2Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
calculator2Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
calculator2Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
calculator2Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
calculator2Display.PolarAxes.EnableCustomRange = 0
calculator2Display.PolarAxes.CustomRange = [0.0, 1.0]
calculator2Display.PolarAxes.PolarAxisVisibility = 1
calculator2Display.PolarAxes.RadialAxesVisibility = 1
calculator2Display.PolarAxes.DrawRadialGridlines = 1
calculator2Display.PolarAxes.PolarArcsVisibility = 1
calculator2Display.PolarAxes.DrawPolarArcsGridlines = 1
calculator2Display.PolarAxes.NumberOfRadialAxes = 0
calculator2Display.PolarAxes.AutoSubdividePolarAxis = 1
calculator2Display.PolarAxes.NumberOfPolarAxis = 0
calculator2Display.PolarAxes.MinimumRadius = 0.0
calculator2Display.PolarAxes.MinimumAngle = 0.0
calculator2Display.PolarAxes.MaximumAngle = 90.0
calculator2Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
calculator2Display.PolarAxes.Ratio = 1.0
calculator2Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
calculator2Display.PolarAxes.PolarAxisTitleVisibility = 1
calculator2Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
calculator2Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
calculator2Display.PolarAxes.PolarLabelVisibility = 1
calculator2Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
calculator2Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
calculator2Display.PolarAxes.RadialLabelVisibility = 1
calculator2Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
calculator2Display.PolarAxes.RadialLabelLocation = 'Bottom'
calculator2Display.PolarAxes.RadialUnitsVisibility = 1
calculator2Display.PolarAxes.ScreenSize = 10.0
calculator2Display.PolarAxes.PolarAxisTitleOpacity = 1.0
calculator2Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
calculator2Display.PolarAxes.PolarAxisTitleFontFile = ''
calculator2Display.PolarAxes.PolarAxisTitleBold = 0
calculator2Display.PolarAxes.PolarAxisTitleItalic = 0
calculator2Display.PolarAxes.PolarAxisTitleShadow = 0
calculator2Display.PolarAxes.PolarAxisTitleFontSize = 12
calculator2Display.PolarAxes.PolarAxisLabelOpacity = 1.0
calculator2Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
calculator2Display.PolarAxes.PolarAxisLabelFontFile = ''
calculator2Display.PolarAxes.PolarAxisLabelBold = 0
calculator2Display.PolarAxes.PolarAxisLabelItalic = 0
calculator2Display.PolarAxes.PolarAxisLabelShadow = 0
calculator2Display.PolarAxes.PolarAxisLabelFontSize = 12
calculator2Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
calculator2Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
calculator2Display.PolarAxes.LastRadialAxisTextFontFile = ''
calculator2Display.PolarAxes.LastRadialAxisTextBold = 0
calculator2Display.PolarAxes.LastRadialAxisTextItalic = 0
calculator2Display.PolarAxes.LastRadialAxisTextShadow = 0
calculator2Display.PolarAxes.LastRadialAxisTextFontSize = 12
calculator2Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
calculator2Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
calculator2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
calculator2Display.PolarAxes.SecondaryRadialAxesTextBold = 0
calculator2Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
calculator2Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
calculator2Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
calculator2Display.PolarAxes.EnableDistanceLOD = 1
calculator2Display.PolarAxes.DistanceLODThreshold = 0.7
calculator2Display.PolarAxes.EnableViewAngleLOD = 1
calculator2Display.PolarAxes.ViewAngleLODThreshold = 0.7
calculator2Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
calculator2Display.PolarAxes.PolarTicksVisibility = 1
calculator2Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
calculator2Display.PolarAxes.TickLocation = 'Both'
calculator2Display.PolarAxes.AxisTickVisibility = 1
calculator2Display.PolarAxes.AxisMinorTickVisibility = 0
calculator2Display.PolarAxes.ArcTickVisibility = 1
calculator2Display.PolarAxes.ArcMinorTickVisibility = 0
calculator2Display.PolarAxes.DeltaAngleMajor = 10.0
calculator2Display.PolarAxes.DeltaAngleMinor = 5.0
calculator2Display.PolarAxes.PolarAxisMajorTickSize = 0.0
calculator2Display.PolarAxes.PolarAxisTickRatioSize = 0.3
calculator2Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
calculator2Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
calculator2Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
calculator2Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
calculator2Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
calculator2Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
calculator2Display.PolarAxes.ArcMajorTickSize = 0.0
calculator2Display.PolarAxes.ArcTickRatioSize = 0.3
calculator2Display.PolarAxes.ArcMajorTickThickness = 1.0
calculator2Display.PolarAxes.ArcTickRatioThickness = 0.5
calculator2Display.PolarAxes.Use2DMode = 0
calculator2Display.PolarAxes.UseLogAxis = 0

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
calculator2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(calculator1)

# set scalar coloring
ColorBy(calculator1Display, ('CELLS', 'cellvol'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(delvBcsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'cellvol'
cellvolLUT = GetColorTransferFunction('cellvol')
cellvolLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
cellvolLUT.InterpretValuesAsCategories = 0
cellvolLUT.AnnotationsInitialized = 0
cellvolLUT.ShowCategoricalColorsinDataRangeOnly = 0
cellvolLUT.RescaleOnVisibilityChange = 0
cellvolLUT.EnableOpacityMapping = 0
cellvolLUT.RGBPoints = [0.0016152765601873398, 0.231373, 0.298039, 0.752941, 0.4811825705692172, 0.865003, 0.865003, 0.865003, 0.9607498645782471, 0.705882, 0.0156863, 0.14902]
cellvolLUT.UseLogScale = 0
cellvolLUT.UseOpacityControlPointsFreehandDrawing = 0
cellvolLUT.ShowDataHistogram = 0
cellvolLUT.AutomaticDataHistogramComputation = 0
cellvolLUT.DataHistogramNumberOfBins = 10
cellvolLUT.ColorSpace = 'Diverging'
cellvolLUT.UseBelowRangeColor = 0
cellvolLUT.BelowRangeColor = [0.0, 0.0, 0.0]
cellvolLUT.UseAboveRangeColor = 0
cellvolLUT.AboveRangeColor = [0.5, 0.5, 0.5]
cellvolLUT.NanColor = [1.0, 1.0, 0.0]
cellvolLUT.NanOpacity = 1.0
cellvolLUT.Discretize = 1
cellvolLUT.NumberOfTableValues = 256
cellvolLUT.ScalarRangeInitialized = 1.0
cellvolLUT.HSVWrap = 0
cellvolLUT.VectorComponent = 0
cellvolLUT.VectorMode = 'Magnitude'
cellvolLUT.AllowDuplicateScalars = 1
cellvolLUT.Annotations = []
cellvolLUT.ActiveAnnotatedValues = []
cellvolLUT.IndexedColors = []
cellvolLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'cellvol'
cellvolPWF = GetOpacityTransferFunction('cellvol')
cellvolPWF.Points = [0.0016152765601873398, 0.0, 0.5, 0.0, 0.9607498645782471, 1.0, 0.5, 0.0]
cellvolPWF.AllowDuplicateScalars = 1
cellvolPWF.UseLogScale = 0
cellvolPWF.ScalarRangeInitialized = 1

# turn off scalar coloring
ColorBy(calculator1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(cellvolLUT, renderView1)

# change representation type
calculator1Display.SetRepresentationType('Outline')

# set active source
SetActiveSource(calculator2)

# turn off scalar coloring
ColorBy(calculator2Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(delPrsByPrsWindLUT, renderView1)

# change representation type
calculator2Display.SetRepresentationType('Outline')

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitVertical(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.UseCache = 0
renderView2.ViewSize = [400, 400]
renderView2.UseInteractiveRenderingForScreenshots = 0
renderView2.InteractionMode = '3D'
renderView2.CollectGeometryThreshold = 100.0
renderView2.SuppressRendering = 0
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.CenterAxesVisibility = 0
renderView2.OrientationAxesVisibility = 1
renderView2.OrientationAxesInteractivity = 0
renderView2.CenterOfRotation = [0.0, 0.0, 0.0]
renderView2.RotationFactor = 1.0
renderView2.EnableRenderOnInteraction = 1
renderView2.UseLight = 1
renderView2.KeyLightWarmth = 0.6
renderView2.KeyLightIntensity = 0.75
renderView2.KeyLightElevation = 50.0
renderView2.KeyLightAzimuth = 10.0
renderView2.FillLightWarmth = 0.4
renderView2.FillLightKFRatio = 3.0
renderView2.FillLightElevation = -75.0
renderView2.FillLightAzimuth = -10.0
renderView2.BackLightWarmth = 0.5
renderView2.BackLightKBRatio = 3.5
renderView2.BackLightElevation = 0.0
renderView2.BackLightAzimuth = 110.0
renderView2.HeadLightWarmth = 0.5
renderView2.HeadLightKHRatio = 3.0
renderView2.MaintainLuminance = 0
renderView2.HiddenLineRemoval = 0
renderView2.UseToneMapping = 0
renderView2.Exposure = 1.0
renderView2.UseAmbientOcclusion = 0
renderView2.StereoRender = 0
renderView2.StereoType = 'Crystal Eyes'
renderView2.ServerStereoType = 'Same As Client'
renderView2.MultiSamples = 0
renderView2.AlphaBitPlanes = 1
renderView2.StencilCapable = 1
renderView2.CameraPosition = [0.0, 0.0, 6.69]
renderView2.CameraFocalPoint = [0.0, 0.0, 0.0]
renderView2.CameraViewUp = [0.0, 1.0, 0.0]
renderView2.CameraViewAngle = 30.0
renderView2.CameraFocalDisk = 1.0
renderView2.CameraFocalDistance = 0.0
renderView2.CameraParallelScale = 1.73
renderView2.EyeAngle = 2.0
renderView2.CameraParallelProjection = 0
renderView2.UseColorPaletteForBackground = 1
renderView2.BackgroundColorMode = 'Single Color'
renderView2.BackgroundTexture = None
renderView2.Background2 = [0.0, 0.0, 0.165]
renderView2.Background = [0.329, 0.349, 0.427]
renderView2.UseEnvironmentLighting = 0
renderView2.MaxClipBounds = [0.0, -1.0, 0.0, -1.0, 0.0, -1.0]
renderView2.LockBounds = 0
renderView2.EnableRayTracing = 0
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.Shadows = 0
renderView2.AmbientSamples = 0
renderView2.SamplesPerPixel = 1
renderView2.ProgressivePasses = 1
renderView2.RouletteDepth = 5
renderView2.VolumeAnisotropy = 0.0
renderView2.Denoise = 1
renderView2.LightScale = 1.0
renderView2.TemporalCacheSize = 0
renderView2.Backgroundmode = 'Environment'
renderView2.EnvironmentNorth = [0.0, 1.0, 0.0]
renderView2.EnvironmentEast = [1.0, 0.0, 0.0]
renderView2.EnvironmentalBG = [0.329, 0.349, 0.427]
renderView2.EnvironmentalBG2 = [0.0, 0.0, 0.165]
renderView2.UseGradientEnvironmentalBG = 0
renderView2.UseTexturedEnvironmentalBG = 0
renderView2.EnvironmentalBGTexture = None
renderView2.AdditionalLights = None
renderView2.OSPRayMaterialLibrary = materialLibrary1

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView2.AxesGrid.Visibility = 0
renderView2.AxesGrid.XTitle = 'X Axis'
renderView2.AxesGrid.YTitle = 'Y Axis'
renderView2.AxesGrid.ZTitle = 'Z Axis'
renderView2.AxesGrid.XTitleOpacity = 1.0
renderView2.AxesGrid.XTitleFontFamily = 'Arial'
renderView2.AxesGrid.XTitleFontFile = ''
renderView2.AxesGrid.XTitleBold = 0
renderView2.AxesGrid.XTitleItalic = 0
renderView2.AxesGrid.XTitleShadow = 0
renderView2.AxesGrid.XTitleFontSize = 12
renderView2.AxesGrid.YTitleOpacity = 1.0
renderView2.AxesGrid.YTitleFontFamily = 'Arial'
renderView2.AxesGrid.YTitleFontFile = ''
renderView2.AxesGrid.YTitleBold = 0
renderView2.AxesGrid.YTitleItalic = 0
renderView2.AxesGrid.YTitleShadow = 0
renderView2.AxesGrid.YTitleFontSize = 12
renderView2.AxesGrid.ZTitleOpacity = 1.0
renderView2.AxesGrid.ZTitleFontFamily = 'Arial'
renderView2.AxesGrid.ZTitleFontFile = ''
renderView2.AxesGrid.ZTitleBold = 0
renderView2.AxesGrid.ZTitleItalic = 0
renderView2.AxesGrid.ZTitleShadow = 0
renderView2.AxesGrid.ZTitleFontSize = 12
renderView2.AxesGrid.FacesToRender = 63
renderView2.AxesGrid.CullBackface = 0
renderView2.AxesGrid.CullFrontface = 1
renderView2.AxesGrid.ShowGrid = 0
renderView2.AxesGrid.ShowEdges = 1
renderView2.AxesGrid.ShowTicks = 1
renderView2.AxesGrid.AxesToLabel = 63
renderView2.AxesGrid.LabelUniqueEdgesOnly = 1
renderView2.AxesGrid.XLabelOpacity = 1.0
renderView2.AxesGrid.XLabelFontFamily = 'Arial'
renderView2.AxesGrid.XLabelFontFile = ''
renderView2.AxesGrid.XLabelBold = 0
renderView2.AxesGrid.XLabelItalic = 0
renderView2.AxesGrid.XLabelShadow = 0
renderView2.AxesGrid.XLabelFontSize = 12
renderView2.AxesGrid.YLabelOpacity = 1.0
renderView2.AxesGrid.YLabelFontFamily = 'Arial'
renderView2.AxesGrid.YLabelFontFile = ''
renderView2.AxesGrid.YLabelBold = 0
renderView2.AxesGrid.YLabelItalic = 0
renderView2.AxesGrid.YLabelShadow = 0
renderView2.AxesGrid.YLabelFontSize = 12
renderView2.AxesGrid.ZLabelOpacity = 1.0
renderView2.AxesGrid.ZLabelFontFamily = 'Arial'
renderView2.AxesGrid.ZLabelFontFile = ''
renderView2.AxesGrid.ZLabelBold = 0
renderView2.AxesGrid.ZLabelItalic = 0
renderView2.AxesGrid.ZLabelShadow = 0
renderView2.AxesGrid.ZLabelFontSize = 12
renderView2.AxesGrid.XAxisNotation = 'Mixed'
renderView2.AxesGrid.XAxisPrecision = 2
renderView2.AxesGrid.XAxisUseCustomLabels = 0
renderView2.AxesGrid.XAxisLabels = []
renderView2.AxesGrid.YAxisNotation = 'Mixed'
renderView2.AxesGrid.YAxisPrecision = 2
renderView2.AxesGrid.YAxisUseCustomLabels = 0
renderView2.AxesGrid.YAxisLabels = []
renderView2.AxesGrid.ZAxisNotation = 'Mixed'
renderView2.AxesGrid.ZAxisPrecision = 2
renderView2.AxesGrid.ZAxisUseCustomLabels = 0
renderView2.AxesGrid.ZAxisLabels = []
renderView2.AxesGrid.UseCustomBounds = 0
renderView2.AxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
renderView2.AxesGrid.DataScale = [1.0, 1.0, 1.0]
renderView2.AxesGrid.DataPosition = [0.0, 0.0, 0.0]
renderView2.AxesGrid.DataBoundsScaleFactor = 1.0008
renderView2.AxesGrid.ModelTransformMatrix = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
renderView2.AxesGrid.ModelBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
renderView2.AxesGrid.UseModelTransform = 0

# assign view to a particular cell in the layout
AssignViewToLayout(view=renderView2, layout=layout1, hint=2)

# set active source
SetActiveSource(calculator1)

# set active source
SetActiveSource(calculator2)

# set active view
SetActiveView(renderView1)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator2)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.UseDual = 0
slice1.Crinkleslice = 0
slice1.Triangulatetheslice = 1
slice1.Mergeduplicatedpointsintheslice = 1
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [325.1457862854004, 0.0, 0.0]
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]
slice1.HyperTreeGridSlicer.Normal = [1.0, 0.0, 0.0]
slice1.HyperTreeGridSlicer.Offset = 0.0

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [334.0, 0.0, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Selection = None
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['CELLS', 'delPrsByPrsWind']
slice1Display.LookupTable = delPrsByPrsWindLUT
slice1Display.MapScalars = 1
slice1Display.MultiComponentsMapping = 0
slice1Display.InterpolateScalarsBeforeMapping = 1
slice1Display.Opacity = 1.0
slice1Display.PointSize = 2.0
slice1Display.LineWidth = 1.0
slice1Display.RenderLinesAsTubes = 0
slice1Display.RenderPointsAsSpheres = 0
slice1Display.Interpolation = 'Gouraud'
slice1Display.Specular = 0.0
slice1Display.SpecularColor = [1.0, 1.0, 1.0]
slice1Display.SpecularPower = 100.0
slice1Display.Luminosity = 0.0
slice1Display.Ambient = 0.0
slice1Display.Diffuse = 1.0
slice1Display.Roughness = 0.3
slice1Display.Metallic = 0.0
slice1Display.EdgeTint = [1.0, 1.0, 1.0]
slice1Display.Anisotropy = 0.0
slice1Display.AnisotropyRotation = 0.0
slice1Display.BaseIOR = 1.5
slice1Display.CoatStrength = 0.0
slice1Display.CoatIOR = 2.0
slice1Display.CoatRoughness = 0.0
slice1Display.CoatColor = [1.0, 1.0, 1.0]
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.Texture = None
slice1Display.RepeatTextures = 1
slice1Display.InterpolateTextures = 0
slice1Display.SeamlessU = 0
slice1Display.SeamlessV = 0
slice1Display.UseMipmapTextures = 0
slice1Display.ShowTexturesOnBackface = 1
slice1Display.BaseColorTexture = None
slice1Display.NormalTexture = None
slice1Display.NormalScale = 1.0
slice1Display.CoatNormalTexture = None
slice1Display.CoatNormalScale = 1.0
slice1Display.MaterialTexture = None
slice1Display.OcclusionStrength = 1.0
slice1Display.AnisotropyTexture = None
slice1Display.EmissiveTexture = None
slice1Display.EmissiveFactor = [1.0, 1.0, 1.0]
slice1Display.FlipTextures = 0
slice1Display.BackfaceRepresentation = 'Follow Frontface'
slice1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
slice1Display.BackfaceOpacity = 1.0
slice1Display.Position = [0.0, 0.0, 0.0]
slice1Display.Scale = [1.0, 1.0, 1.0]
slice1Display.Orientation = [0.0, 0.0, 0.0]
slice1Display.Origin = [0.0, 0.0, 0.0]
slice1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
slice1Display.Pickable = 1
slice1Display.Triangulate = 0
slice1Display.UseShaderReplacements = 0
slice1Display.ShaderReplacements = ''
slice1Display.NonlinearSubdivisionLevel = 1
slice1Display.UseDataPartitions = 0
slice1Display.OSPRayUseScaleArray = 'All Approximate'
slice1Display.OSPRayScaleArray = ''
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.OSPRayMaterial = 'None'
slice1Display.BlockSelectors = ['/']
slice1Display.BlockColors = []
slice1Display.BlockOpacities = []
slice1Display.Orient = 0
slice1Display.OrientationMode = 'Direction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.Scaling = 0
slice1Display.ScaleMode = 'No Data Scaling Off'
slice1Display.ScaleFactor = 60.2170955657959
slice1Display.SelectScaleArray = 'delPrsByPrsWind'
slice1Display.GlyphType = 'Arrow'
slice1Display.UseGlyphTable = 0
slice1Display.GlyphTableIndexArray = 'delPrsByPrsWind'
slice1Display.UseCompositeGlyphTable = 0
slice1Display.UseGlyphCullingAndLOD = 0
slice1Display.LODValues = []
slice1Display.ColorByLODIndex = 0
slice1Display.GaussianRadius = 3.010854778289795
slice1Display.ShaderPreset = 'Sphere'
slice1Display.CustomTriangleScale = 3
slice1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
slice1Display.Emissive = 0
slice1Display.ScaleByArray = 0
slice1Display.SetScaleArray = [None, '']
slice1Display.ScaleArrayComponent = 0
slice1Display.UseScaleFunction = 1
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityByArray = 0
slice1Display.OpacityArray = [None, '']
slice1Display.OpacityArrayComponent = 0
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.SelectionCellLabelBold = 0
slice1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
slice1Display.SelectionCellLabelFontFamily = 'Arial'
slice1Display.SelectionCellLabelFontFile = ''
slice1Display.SelectionCellLabelFontSize = 18
slice1Display.SelectionCellLabelItalic = 0
slice1Display.SelectionCellLabelJustification = 'Left'
slice1Display.SelectionCellLabelOpacity = 1.0
slice1Display.SelectionCellLabelShadow = 0
slice1Display.SelectionPointLabelBold = 0
slice1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
slice1Display.SelectionPointLabelFontFamily = 'Arial'
slice1Display.SelectionPointLabelFontFile = ''
slice1Display.SelectionPointLabelFontSize = 18
slice1Display.SelectionPointLabelItalic = 0
slice1Display.SelectionPointLabelJustification = 'Left'
slice1Display.SelectionPointLabelOpacity = 1.0
slice1Display.SelectionPointLabelShadow = 0
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
slice1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
slice1Display.GlyphType.TipResolution = 6
slice1Display.GlyphType.TipRadius = 0.1
slice1Display.GlyphType.TipLength = 0.35
slice1Display.GlyphType.ShaftResolution = 6
slice1Display.GlyphType.ShaftRadius = 0.03
slice1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
slice1Display.DataAxesGrid.XTitle = 'X Axis'
slice1Display.DataAxesGrid.YTitle = 'Y Axis'
slice1Display.DataAxesGrid.ZTitle = 'Z Axis'
slice1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
slice1Display.DataAxesGrid.XTitleFontFile = ''
slice1Display.DataAxesGrid.XTitleBold = 0
slice1Display.DataAxesGrid.XTitleItalic = 0
slice1Display.DataAxesGrid.XTitleFontSize = 12
slice1Display.DataAxesGrid.XTitleShadow = 0
slice1Display.DataAxesGrid.XTitleOpacity = 1.0
slice1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
slice1Display.DataAxesGrid.YTitleFontFile = ''
slice1Display.DataAxesGrid.YTitleBold = 0
slice1Display.DataAxesGrid.YTitleItalic = 0
slice1Display.DataAxesGrid.YTitleFontSize = 12
slice1Display.DataAxesGrid.YTitleShadow = 0
slice1Display.DataAxesGrid.YTitleOpacity = 1.0
slice1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
slice1Display.DataAxesGrid.ZTitleFontFile = ''
slice1Display.DataAxesGrid.ZTitleBold = 0
slice1Display.DataAxesGrid.ZTitleItalic = 0
slice1Display.DataAxesGrid.ZTitleFontSize = 12
slice1Display.DataAxesGrid.ZTitleShadow = 0
slice1Display.DataAxesGrid.ZTitleOpacity = 1.0
slice1Display.DataAxesGrid.FacesToRender = 63
slice1Display.DataAxesGrid.CullBackface = 0
slice1Display.DataAxesGrid.CullFrontface = 1
slice1Display.DataAxesGrid.ShowGrid = 0
slice1Display.DataAxesGrid.ShowEdges = 1
slice1Display.DataAxesGrid.ShowTicks = 1
slice1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
slice1Display.DataAxesGrid.AxesToLabel = 63
slice1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
slice1Display.DataAxesGrid.XLabelFontFile = ''
slice1Display.DataAxesGrid.XLabelBold = 0
slice1Display.DataAxesGrid.XLabelItalic = 0
slice1Display.DataAxesGrid.XLabelFontSize = 12
slice1Display.DataAxesGrid.XLabelShadow = 0
slice1Display.DataAxesGrid.XLabelOpacity = 1.0
slice1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
slice1Display.DataAxesGrid.YLabelFontFile = ''
slice1Display.DataAxesGrid.YLabelBold = 0
slice1Display.DataAxesGrid.YLabelItalic = 0
slice1Display.DataAxesGrid.YLabelFontSize = 12
slice1Display.DataAxesGrid.YLabelShadow = 0
slice1Display.DataAxesGrid.YLabelOpacity = 1.0
slice1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
slice1Display.DataAxesGrid.ZLabelFontFile = ''
slice1Display.DataAxesGrid.ZLabelBold = 0
slice1Display.DataAxesGrid.ZLabelItalic = 0
slice1Display.DataAxesGrid.ZLabelFontSize = 12
slice1Display.DataAxesGrid.ZLabelShadow = 0
slice1Display.DataAxesGrid.ZLabelOpacity = 1.0
slice1Display.DataAxesGrid.XAxisNotation = 'Mixed'
slice1Display.DataAxesGrid.XAxisPrecision = 2
slice1Display.DataAxesGrid.XAxisUseCustomLabels = 0
slice1Display.DataAxesGrid.XAxisLabels = []
slice1Display.DataAxesGrid.YAxisNotation = 'Mixed'
slice1Display.DataAxesGrid.YAxisPrecision = 2
slice1Display.DataAxesGrid.YAxisUseCustomLabels = 0
slice1Display.DataAxesGrid.YAxisLabels = []
slice1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
slice1Display.DataAxesGrid.ZAxisPrecision = 2
slice1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
slice1Display.DataAxesGrid.ZAxisLabels = []
slice1Display.DataAxesGrid.UseCustomBounds = 0
slice1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
slice1Display.PolarAxes.Visibility = 0
slice1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
slice1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
slice1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
slice1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
slice1Display.PolarAxes.EnableCustomRange = 0
slice1Display.PolarAxes.CustomRange = [0.0, 1.0]
slice1Display.PolarAxes.PolarAxisVisibility = 1
slice1Display.PolarAxes.RadialAxesVisibility = 1
slice1Display.PolarAxes.DrawRadialGridlines = 1
slice1Display.PolarAxes.PolarArcsVisibility = 1
slice1Display.PolarAxes.DrawPolarArcsGridlines = 1
slice1Display.PolarAxes.NumberOfRadialAxes = 0
slice1Display.PolarAxes.AutoSubdividePolarAxis = 1
slice1Display.PolarAxes.NumberOfPolarAxis = 0
slice1Display.PolarAxes.MinimumRadius = 0.0
slice1Display.PolarAxes.MinimumAngle = 0.0
slice1Display.PolarAxes.MaximumAngle = 90.0
slice1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
slice1Display.PolarAxes.Ratio = 1.0
slice1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
slice1Display.PolarAxes.PolarAxisTitleVisibility = 1
slice1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
slice1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
slice1Display.PolarAxes.PolarLabelVisibility = 1
slice1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
slice1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
slice1Display.PolarAxes.RadialLabelVisibility = 1
slice1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
slice1Display.PolarAxes.RadialLabelLocation = 'Bottom'
slice1Display.PolarAxes.RadialUnitsVisibility = 1
slice1Display.PolarAxes.ScreenSize = 10.0
slice1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
slice1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
slice1Display.PolarAxes.PolarAxisTitleFontFile = ''
slice1Display.PolarAxes.PolarAxisTitleBold = 0
slice1Display.PolarAxes.PolarAxisTitleItalic = 0
slice1Display.PolarAxes.PolarAxisTitleShadow = 0
slice1Display.PolarAxes.PolarAxisTitleFontSize = 12
slice1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
slice1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
slice1Display.PolarAxes.PolarAxisLabelFontFile = ''
slice1Display.PolarAxes.PolarAxisLabelBold = 0
slice1Display.PolarAxes.PolarAxisLabelItalic = 0
slice1Display.PolarAxes.PolarAxisLabelShadow = 0
slice1Display.PolarAxes.PolarAxisLabelFontSize = 12
slice1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
slice1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
slice1Display.PolarAxes.LastRadialAxisTextFontFile = ''
slice1Display.PolarAxes.LastRadialAxisTextBold = 0
slice1Display.PolarAxes.LastRadialAxisTextItalic = 0
slice1Display.PolarAxes.LastRadialAxisTextShadow = 0
slice1Display.PolarAxes.LastRadialAxisTextFontSize = 12
slice1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
slice1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
slice1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
slice1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
slice1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
slice1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
slice1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
slice1Display.PolarAxes.EnableDistanceLOD = 1
slice1Display.PolarAxes.DistanceLODThreshold = 0.7
slice1Display.PolarAxes.EnableViewAngleLOD = 1
slice1Display.PolarAxes.ViewAngleLODThreshold = 0.7
slice1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
slice1Display.PolarAxes.PolarTicksVisibility = 1
slice1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
slice1Display.PolarAxes.TickLocation = 'Both'
slice1Display.PolarAxes.AxisTickVisibility = 1
slice1Display.PolarAxes.AxisMinorTickVisibility = 0
slice1Display.PolarAxes.ArcTickVisibility = 1
slice1Display.PolarAxes.ArcMinorTickVisibility = 0
slice1Display.PolarAxes.DeltaAngleMajor = 10.0
slice1Display.PolarAxes.DeltaAngleMinor = 5.0
slice1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
slice1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
slice1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
slice1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
slice1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
slice1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
slice1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
slice1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
slice1Display.PolarAxes.ArcMajorTickSize = 0.0
slice1Display.PolarAxes.ArcTickRatioSize = 0.3
slice1Display.PolarAxes.ArcMajorTickThickness = 1.0
slice1Display.PolarAxes.ArcTickRatioThickness = 0.5
slice1Display.PolarAxes.Use2DMode = 0
slice1Display.PolarAxes.UseLogAxis = 0

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
renderView2.Update()

# set scalar coloring
ColorBy(slice1Display, ('CELLS', 'ndens'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(delPrsByPrsWindLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'ndens'
ndensLUT = GetColorTransferFunction('ndens')
ndensLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
ndensLUT.InterpretValuesAsCategories = 0
ndensLUT.AnnotationsInitialized = 0
ndensLUT.ShowCategoricalColorsinDataRangeOnly = 0
ndensLUT.RescaleOnVisibilityChange = 0
ndensLUT.EnableOpacityMapping = 0
ndensLUT.RGBPoints = [0.0006734263151884079, 0.231373, 0.298039, 0.752941, 29.13841540273279, 0.865003, 0.865003, 0.865003, 58.27615737915039, 0.705882, 0.0156863, 0.14902]
ndensLUT.UseLogScale = 0
ndensLUT.UseOpacityControlPointsFreehandDrawing = 0
ndensLUT.ShowDataHistogram = 0
ndensLUT.AutomaticDataHistogramComputation = 0
ndensLUT.DataHistogramNumberOfBins = 10
ndensLUT.ColorSpace = 'Diverging'
ndensLUT.UseBelowRangeColor = 0
ndensLUT.BelowRangeColor = [0.0, 0.0, 0.0]
ndensLUT.UseAboveRangeColor = 0
ndensLUT.AboveRangeColor = [0.5, 0.5, 0.5]
ndensLUT.NanColor = [1.0, 1.0, 0.0]
ndensLUT.NanOpacity = 1.0
ndensLUT.Discretize = 1
ndensLUT.NumberOfTableValues = 256
ndensLUT.ScalarRangeInitialized = 1.0
ndensLUT.HSVWrap = 0
ndensLUT.VectorComponent = 0
ndensLUT.VectorMode = 'Magnitude'
ndensLUT.AllowDuplicateScalars = 1
ndensLUT.Annotations = []
ndensLUT.ActiveAnnotatedValues = []
ndensLUT.IndexedColors = []
ndensLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'ndens'
ndensPWF = GetOpacityTransferFunction('ndens')
ndensPWF.Points = [0.0006734263151884079, 0.0, 0.5, 0.0, 58.27615737915039, 1.0, 0.5, 0.0]
ndensPWF.AllowDuplicateScalars = 1
ndensPWF.UseLogScale = 0
ndensPWF.ScalarRangeInitialized = 1

# get color legend/bar for ndensLUT in view renderView1
ndensLUTColorBar = GetScalarBar(ndensLUT, renderView1)
ndensLUTColorBar.AutoOrient = 1
ndensLUTColorBar.Orientation = 'Vertical'
ndensLUTColorBar.WindowLocation = 'Lower Right Corner'
ndensLUTColorBar.Position = [0.89, 0.02]
ndensLUTColorBar.Title = 'ndens'
ndensLUTColorBar.ComponentTitle = ''
ndensLUTColorBar.TitleJustification = 'Centered'
ndensLUTColorBar.HorizontalTitle = 0
ndensLUTColorBar.TitleOpacity = 1.0
ndensLUTColorBar.TitleFontFamily = 'Arial'
ndensLUTColorBar.TitleFontFile = ''
ndensLUTColorBar.TitleBold = 0
ndensLUTColorBar.TitleItalic = 0
ndensLUTColorBar.TitleShadow = 0
ndensLUTColorBar.TitleFontSize = 16
ndensLUTColorBar.LabelOpacity = 1.0
ndensLUTColorBar.LabelFontFamily = 'Arial'
ndensLUTColorBar.LabelFontFile = ''
ndensLUTColorBar.LabelBold = 0
ndensLUTColorBar.LabelItalic = 0
ndensLUTColorBar.LabelShadow = 0
ndensLUTColorBar.LabelFontSize = 16
ndensLUTColorBar.AutomaticLabelFormat = 1
ndensLUTColorBar.LabelFormat = '%-#6.3g'
ndensLUTColorBar.DrawTickMarks = 1
ndensLUTColorBar.DrawTickLabels = 1
ndensLUTColorBar.UseCustomLabels = 0
ndensLUTColorBar.CustomLabels = []
ndensLUTColorBar.AddRangeLabels = 1
ndensLUTColorBar.RangeLabelFormat = '%-#6.1e'
ndensLUTColorBar.DrawAnnotations = 1
ndensLUTColorBar.AddRangeAnnotations = 0
ndensLUTColorBar.AutomaticAnnotations = 0
ndensLUTColorBar.DrawNanAnnotation = 0
ndensLUTColorBar.NanAnnotation = 'NaN'
ndensLUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
ndensLUTColorBar.ReverseLegend = 0
ndensLUTColorBar.ScalarBarThickness = 16
ndensLUTColorBar.ScalarBarLength = 0.33

# change scalar bar placement
ndensLUTColorBar.Orientation = 'Horizontal'
ndensLUTColorBar.WindowLocation = 'Any Location'
ndensLUTColorBar.Position = [0.3306980961015411, 0.7727710843373493]
ndensLUTColorBar.ScalarBarLength = 0.3299999999999996

# set active source
SetActiveSource(calculator1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# set active view
SetActiveView(renderView2)

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=calculator1)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.UseDual = 0
slice2.Crinkleslice = 0
slice2.Triangulatetheslice = 1
slice2.Mergeduplicatedpointsintheslice = 1
slice2.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [325.1457862854004, 0.0, 0.0]
slice2.SliceType.Normal = [1.0, 0.0, 0.0]
slice2.SliceType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice2.HyperTreeGridSlicer.Origin = [325.1457862854004, 0.0, 0.0]
slice2.HyperTreeGridSlicer.Normal = [1.0, 0.0, 0.0]
slice2.HyperTreeGridSlicer.Offset = 0.0

# Properties modified on slice2.SliceType
slice2.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice2Display = Show(slice2, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
slice2Display.Selection = None
slice2Display.Representation = 'Surface'
slice2Display.ColorArrayName = ['CELLS', 'delvBcs']
slice2Display.LookupTable = delvBcsLUT
slice2Display.MapScalars = 1
slice2Display.MultiComponentsMapping = 0
slice2Display.InterpolateScalarsBeforeMapping = 1
slice2Display.Opacity = 1.0
slice2Display.PointSize = 2.0
slice2Display.LineWidth = 1.0
slice2Display.RenderLinesAsTubes = 0
slice2Display.RenderPointsAsSpheres = 0
slice2Display.Interpolation = 'Gouraud'
slice2Display.Specular = 0.0
slice2Display.SpecularColor = [1.0, 1.0, 1.0]
slice2Display.SpecularPower = 100.0
slice2Display.Luminosity = 0.0
slice2Display.Ambient = 0.0
slice2Display.Diffuse = 1.0
slice2Display.Roughness = 0.3
slice2Display.Metallic = 0.0
slice2Display.EdgeTint = [1.0, 1.0, 1.0]
slice2Display.Anisotropy = 0.0
slice2Display.AnisotropyRotation = 0.0
slice2Display.BaseIOR = 1.5
slice2Display.CoatStrength = 0.0
slice2Display.CoatIOR = 2.0
slice2Display.CoatRoughness = 0.0
slice2Display.CoatColor = [1.0, 1.0, 1.0]
slice2Display.SelectTCoordArray = 'None'
slice2Display.SelectNormalArray = 'None'
slice2Display.SelectTangentArray = 'None'
slice2Display.Texture = None
slice2Display.RepeatTextures = 1
slice2Display.InterpolateTextures = 0
slice2Display.SeamlessU = 0
slice2Display.SeamlessV = 0
slice2Display.UseMipmapTextures = 0
slice2Display.ShowTexturesOnBackface = 1
slice2Display.BaseColorTexture = None
slice2Display.NormalTexture = None
slice2Display.NormalScale = 1.0
slice2Display.CoatNormalTexture = None
slice2Display.CoatNormalScale = 1.0
slice2Display.MaterialTexture = None
slice2Display.OcclusionStrength = 1.0
slice2Display.AnisotropyTexture = None
slice2Display.EmissiveTexture = None
slice2Display.EmissiveFactor = [1.0, 1.0, 1.0]
slice2Display.FlipTextures = 0
slice2Display.BackfaceRepresentation = 'Follow Frontface'
slice2Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
slice2Display.BackfaceOpacity = 1.0
slice2Display.Position = [0.0, 0.0, 0.0]
slice2Display.Scale = [1.0, 1.0, 1.0]
slice2Display.Orientation = [0.0, 0.0, 0.0]
slice2Display.Origin = [0.0, 0.0, 0.0]
slice2Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
slice2Display.Pickable = 1
slice2Display.Triangulate = 0
slice2Display.UseShaderReplacements = 0
slice2Display.ShaderReplacements = ''
slice2Display.NonlinearSubdivisionLevel = 1
slice2Display.UseDataPartitions = 0
slice2Display.OSPRayUseScaleArray = 'All Approximate'
slice2Display.OSPRayScaleArray = ''
slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice2Display.OSPRayMaterial = 'None'
slice2Display.BlockSelectors = ['/']
slice2Display.BlockColors = []
slice2Display.BlockOpacities = []
slice2Display.Orient = 0
slice2Display.OrientationMode = 'Direction'
slice2Display.SelectOrientationVectors = 'None'
slice2Display.Scaling = 0
slice2Display.ScaleMode = 'No Data Scaling Off'
slice2Display.ScaleFactor = 60.2170955657959
slice2Display.SelectScaleArray = 'delvBcs'
slice2Display.GlyphType = 'Arrow'
slice2Display.UseGlyphTable = 0
slice2Display.GlyphTableIndexArray = 'delvBcs'
slice2Display.UseCompositeGlyphTable = 0
slice2Display.UseGlyphCullingAndLOD = 0
slice2Display.LODValues = []
slice2Display.ColorByLODIndex = 0
slice2Display.GaussianRadius = 3.010854778289795
slice2Display.ShaderPreset = 'Sphere'
slice2Display.CustomTriangleScale = 3
slice2Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
slice2Display.Emissive = 0
slice2Display.ScaleByArray = 0
slice2Display.SetScaleArray = [None, '']
slice2Display.ScaleArrayComponent = 0
slice2Display.UseScaleFunction = 1
slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
slice2Display.OpacityByArray = 0
slice2Display.OpacityArray = [None, '']
slice2Display.OpacityArrayComponent = 0
slice2Display.OpacityTransferFunction = 'PiecewiseFunction'
slice2Display.DataAxesGrid = 'GridAxesRepresentation'
slice2Display.SelectionCellLabelBold = 0
slice2Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
slice2Display.SelectionCellLabelFontFamily = 'Arial'
slice2Display.SelectionCellLabelFontFile = ''
slice2Display.SelectionCellLabelFontSize = 18
slice2Display.SelectionCellLabelItalic = 0
slice2Display.SelectionCellLabelJustification = 'Left'
slice2Display.SelectionCellLabelOpacity = 1.0
slice2Display.SelectionCellLabelShadow = 0
slice2Display.SelectionPointLabelBold = 0
slice2Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
slice2Display.SelectionPointLabelFontFamily = 'Arial'
slice2Display.SelectionPointLabelFontFile = ''
slice2Display.SelectionPointLabelFontSize = 18
slice2Display.SelectionPointLabelItalic = 0
slice2Display.SelectionPointLabelJustification = 'Left'
slice2Display.SelectionPointLabelOpacity = 1.0
slice2Display.SelectionPointLabelShadow = 0
slice2Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
slice2Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice2Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
slice2Display.GlyphType.TipResolution = 6
slice2Display.GlyphType.TipRadius = 0.1
slice2Display.GlyphType.TipLength = 0.35
slice2Display.GlyphType.ShaftResolution = 6
slice2Display.GlyphType.ShaftRadius = 0.03
slice2Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice2Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
slice2Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
slice2Display.DataAxesGrid.XTitle = 'X Axis'
slice2Display.DataAxesGrid.YTitle = 'Y Axis'
slice2Display.DataAxesGrid.ZTitle = 'Z Axis'
slice2Display.DataAxesGrid.XTitleFontFamily = 'Arial'
slice2Display.DataAxesGrid.XTitleFontFile = ''
slice2Display.DataAxesGrid.XTitleBold = 0
slice2Display.DataAxesGrid.XTitleItalic = 0
slice2Display.DataAxesGrid.XTitleFontSize = 12
slice2Display.DataAxesGrid.XTitleShadow = 0
slice2Display.DataAxesGrid.XTitleOpacity = 1.0
slice2Display.DataAxesGrid.YTitleFontFamily = 'Arial'
slice2Display.DataAxesGrid.YTitleFontFile = ''
slice2Display.DataAxesGrid.YTitleBold = 0
slice2Display.DataAxesGrid.YTitleItalic = 0
slice2Display.DataAxesGrid.YTitleFontSize = 12
slice2Display.DataAxesGrid.YTitleShadow = 0
slice2Display.DataAxesGrid.YTitleOpacity = 1.0
slice2Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
slice2Display.DataAxesGrid.ZTitleFontFile = ''
slice2Display.DataAxesGrid.ZTitleBold = 0
slice2Display.DataAxesGrid.ZTitleItalic = 0
slice2Display.DataAxesGrid.ZTitleFontSize = 12
slice2Display.DataAxesGrid.ZTitleShadow = 0
slice2Display.DataAxesGrid.ZTitleOpacity = 1.0
slice2Display.DataAxesGrid.FacesToRender = 63
slice2Display.DataAxesGrid.CullBackface = 0
slice2Display.DataAxesGrid.CullFrontface = 1
slice2Display.DataAxesGrid.ShowGrid = 0
slice2Display.DataAxesGrid.ShowEdges = 1
slice2Display.DataAxesGrid.ShowTicks = 1
slice2Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
slice2Display.DataAxesGrid.AxesToLabel = 63
slice2Display.DataAxesGrid.XLabelFontFamily = 'Arial'
slice2Display.DataAxesGrid.XLabelFontFile = ''
slice2Display.DataAxesGrid.XLabelBold = 0
slice2Display.DataAxesGrid.XLabelItalic = 0
slice2Display.DataAxesGrid.XLabelFontSize = 12
slice2Display.DataAxesGrid.XLabelShadow = 0
slice2Display.DataAxesGrid.XLabelOpacity = 1.0
slice2Display.DataAxesGrid.YLabelFontFamily = 'Arial'
slice2Display.DataAxesGrid.YLabelFontFile = ''
slice2Display.DataAxesGrid.YLabelBold = 0
slice2Display.DataAxesGrid.YLabelItalic = 0
slice2Display.DataAxesGrid.YLabelFontSize = 12
slice2Display.DataAxesGrid.YLabelShadow = 0
slice2Display.DataAxesGrid.YLabelOpacity = 1.0
slice2Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
slice2Display.DataAxesGrid.ZLabelFontFile = ''
slice2Display.DataAxesGrid.ZLabelBold = 0
slice2Display.DataAxesGrid.ZLabelItalic = 0
slice2Display.DataAxesGrid.ZLabelFontSize = 12
slice2Display.DataAxesGrid.ZLabelShadow = 0
slice2Display.DataAxesGrid.ZLabelOpacity = 1.0
slice2Display.DataAxesGrid.XAxisNotation = 'Mixed'
slice2Display.DataAxesGrid.XAxisPrecision = 2
slice2Display.DataAxesGrid.XAxisUseCustomLabels = 0
slice2Display.DataAxesGrid.XAxisLabels = []
slice2Display.DataAxesGrid.YAxisNotation = 'Mixed'
slice2Display.DataAxesGrid.YAxisPrecision = 2
slice2Display.DataAxesGrid.YAxisUseCustomLabels = 0
slice2Display.DataAxesGrid.YAxisLabels = []
slice2Display.DataAxesGrid.ZAxisNotation = 'Mixed'
slice2Display.DataAxesGrid.ZAxisPrecision = 2
slice2Display.DataAxesGrid.ZAxisUseCustomLabels = 0
slice2Display.DataAxesGrid.ZAxisLabels = []
slice2Display.DataAxesGrid.UseCustomBounds = 0
slice2Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
slice2Display.PolarAxes.Visibility = 0
slice2Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
slice2Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
slice2Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
slice2Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
slice2Display.PolarAxes.EnableCustomRange = 0
slice2Display.PolarAxes.CustomRange = [0.0, 1.0]
slice2Display.PolarAxes.PolarAxisVisibility = 1
slice2Display.PolarAxes.RadialAxesVisibility = 1
slice2Display.PolarAxes.DrawRadialGridlines = 1
slice2Display.PolarAxes.PolarArcsVisibility = 1
slice2Display.PolarAxes.DrawPolarArcsGridlines = 1
slice2Display.PolarAxes.NumberOfRadialAxes = 0
slice2Display.PolarAxes.AutoSubdividePolarAxis = 1
slice2Display.PolarAxes.NumberOfPolarAxis = 0
slice2Display.PolarAxes.MinimumRadius = 0.0
slice2Display.PolarAxes.MinimumAngle = 0.0
slice2Display.PolarAxes.MaximumAngle = 90.0
slice2Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
slice2Display.PolarAxes.Ratio = 1.0
slice2Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
slice2Display.PolarAxes.PolarAxisTitleVisibility = 1
slice2Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
slice2Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
slice2Display.PolarAxes.PolarLabelVisibility = 1
slice2Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
slice2Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
slice2Display.PolarAxes.RadialLabelVisibility = 1
slice2Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
slice2Display.PolarAxes.RadialLabelLocation = 'Bottom'
slice2Display.PolarAxes.RadialUnitsVisibility = 1
slice2Display.PolarAxes.ScreenSize = 10.0
slice2Display.PolarAxes.PolarAxisTitleOpacity = 1.0
slice2Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
slice2Display.PolarAxes.PolarAxisTitleFontFile = ''
slice2Display.PolarAxes.PolarAxisTitleBold = 0
slice2Display.PolarAxes.PolarAxisTitleItalic = 0
slice2Display.PolarAxes.PolarAxisTitleShadow = 0
slice2Display.PolarAxes.PolarAxisTitleFontSize = 12
slice2Display.PolarAxes.PolarAxisLabelOpacity = 1.0
slice2Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
slice2Display.PolarAxes.PolarAxisLabelFontFile = ''
slice2Display.PolarAxes.PolarAxisLabelBold = 0
slice2Display.PolarAxes.PolarAxisLabelItalic = 0
slice2Display.PolarAxes.PolarAxisLabelShadow = 0
slice2Display.PolarAxes.PolarAxisLabelFontSize = 12
slice2Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
slice2Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
slice2Display.PolarAxes.LastRadialAxisTextFontFile = ''
slice2Display.PolarAxes.LastRadialAxisTextBold = 0
slice2Display.PolarAxes.LastRadialAxisTextItalic = 0
slice2Display.PolarAxes.LastRadialAxisTextShadow = 0
slice2Display.PolarAxes.LastRadialAxisTextFontSize = 12
slice2Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
slice2Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
slice2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
slice2Display.PolarAxes.SecondaryRadialAxesTextBold = 0
slice2Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
slice2Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
slice2Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
slice2Display.PolarAxes.EnableDistanceLOD = 1
slice2Display.PolarAxes.DistanceLODThreshold = 0.7
slice2Display.PolarAxes.EnableViewAngleLOD = 1
slice2Display.PolarAxes.ViewAngleLODThreshold = 0.7
slice2Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
slice2Display.PolarAxes.PolarTicksVisibility = 1
slice2Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
slice2Display.PolarAxes.TickLocation = 'Both'
slice2Display.PolarAxes.AxisTickVisibility = 1
slice2Display.PolarAxes.AxisMinorTickVisibility = 0
slice2Display.PolarAxes.ArcTickVisibility = 1
slice2Display.PolarAxes.ArcMinorTickVisibility = 0
slice2Display.PolarAxes.DeltaAngleMajor = 10.0
slice2Display.PolarAxes.DeltaAngleMinor = 5.0
slice2Display.PolarAxes.PolarAxisMajorTickSize = 0.0
slice2Display.PolarAxes.PolarAxisTickRatioSize = 0.3
slice2Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
slice2Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
slice2Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
slice2Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
slice2Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
slice2Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
slice2Display.PolarAxes.ArcMajorTickSize = 0.0
slice2Display.PolarAxes.ArcTickRatioSize = 0.3
slice2Display.PolarAxes.ArcMajorTickThickness = 1.0
slice2Display.PolarAxes.ArcTickRatioThickness = 0.5
slice2Display.PolarAxes.Use2DMode = 0
slice2Display.PolarAxes.UseLogAxis = 0

# reset view to fit data
renderView2.ResetCamera(False)

#changing interaction mode based on data extents
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [325.9145221710205, 0.0, 10000.0]
renderView2.CameraFocalPoint = [325.9145221710205, 0.0, 0.0]

# show color bar/color legend
slice2Display.SetScalarBarVisibility(renderView2, True)

# update the view to ensure updated data information
renderView2.Update()

# set scalar coloring
ColorBy(slice2Display, ('CELLS', 'pressure'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(delvBcsLUT, renderView2)

# rescale color and/or opacity maps used to include current data range
slice2Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice2Display.SetScalarBarVisibility(renderView2, True)

# get color transfer function/color map for 'pressure'
pressureLUT = GetColorTransferFunction('pressure')
pressureLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
pressureLUT.InterpretValuesAsCategories = 0
pressureLUT.AnnotationsInitialized = 0
pressureLUT.ShowCategoricalColorsinDataRangeOnly = 0
pressureLUT.RescaleOnVisibilityChange = 0
pressureLUT.EnableOpacityMapping = 0
pressureLUT.RGBPoints = [4.331347099650884e-06, 0.231373, 0.298039, 0.752941, 0.2261738380177576, 0.865003, 0.865003, 0.865003, 0.4523433446884155, 0.705882, 0.0156863, 0.14902]
pressureLUT.UseLogScale = 0
pressureLUT.UseOpacityControlPointsFreehandDrawing = 0
pressureLUT.ShowDataHistogram = 0
pressureLUT.AutomaticDataHistogramComputation = 0
pressureLUT.DataHistogramNumberOfBins = 10
pressureLUT.ColorSpace = 'Diverging'
pressureLUT.UseBelowRangeColor = 0
pressureLUT.BelowRangeColor = [0.0, 0.0, 0.0]
pressureLUT.UseAboveRangeColor = 0
pressureLUT.AboveRangeColor = [0.5, 0.5, 0.5]
pressureLUT.NanColor = [1.0, 1.0, 0.0]
pressureLUT.NanOpacity = 1.0
pressureLUT.Discretize = 1
pressureLUT.NumberOfTableValues = 256
pressureLUT.ScalarRangeInitialized = 1.0
pressureLUT.HSVWrap = 0
pressureLUT.VectorComponent = 0
pressureLUT.VectorMode = 'Magnitude'
pressureLUT.AllowDuplicateScalars = 1
pressureLUT.Annotations = []
pressureLUT.ActiveAnnotatedValues = []
pressureLUT.IndexedColors = []
pressureLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'pressure'
pressurePWF = GetOpacityTransferFunction('pressure')
pressurePWF.Points = [4.331347099650884e-06, 0.0, 0.5, 0.0, 0.4523433446884155, 1.0, 0.5, 0.0]
pressurePWF.AllowDuplicateScalars = 1
pressurePWF.UseLogScale = 0
pressurePWF.ScalarRangeInitialized = 1

# get color legend/bar for pressureLUT in view renderView2
pressureLUTColorBar = GetScalarBar(pressureLUT, renderView2)
pressureLUTColorBar.AutoOrient = 1
pressureLUTColorBar.Orientation = 'Vertical'
pressureLUTColorBar.WindowLocation = 'Lower Right Corner'
pressureLUTColorBar.Position = [0.89, 0.02]
pressureLUTColorBar.Title = 'pressure'
pressureLUTColorBar.ComponentTitle = ''
pressureLUTColorBar.TitleJustification = 'Centered'
pressureLUTColorBar.HorizontalTitle = 0
pressureLUTColorBar.TitleOpacity = 1.0
pressureLUTColorBar.TitleFontFamily = 'Arial'
pressureLUTColorBar.TitleFontFile = ''
pressureLUTColorBar.TitleBold = 0
pressureLUTColorBar.TitleItalic = 0
pressureLUTColorBar.TitleShadow = 0
pressureLUTColorBar.TitleFontSize = 16
pressureLUTColorBar.LabelOpacity = 1.0
pressureLUTColorBar.LabelFontFamily = 'Arial'
pressureLUTColorBar.LabelFontFile = ''
pressureLUTColorBar.LabelBold = 0
pressureLUTColorBar.LabelItalic = 0
pressureLUTColorBar.LabelShadow = 0
pressureLUTColorBar.LabelFontSize = 16
pressureLUTColorBar.AutomaticLabelFormat = 1
pressureLUTColorBar.LabelFormat = '%-#6.3g'
pressureLUTColorBar.DrawTickMarks = 1
pressureLUTColorBar.DrawTickLabels = 1
pressureLUTColorBar.UseCustomLabels = 0
pressureLUTColorBar.CustomLabels = []
pressureLUTColorBar.AddRangeLabels = 1
pressureLUTColorBar.RangeLabelFormat = '%-#6.1e'
pressureLUTColorBar.DrawAnnotations = 1
pressureLUTColorBar.AddRangeAnnotations = 0
pressureLUTColorBar.AutomaticAnnotations = 0
pressureLUTColorBar.DrawNanAnnotation = 0
pressureLUTColorBar.NanAnnotation = 'NaN'
pressureLUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
pressureLUTColorBar.ReverseLegend = 0
pressureLUTColorBar.ScalarBarThickness = 16
pressureLUTColorBar.ScalarBarLength = 0.33

# change scalar bar placement
pressureLUTColorBar.Orientation = 'Horizontal'
pressureLUTColorBar.WindowLocation = 'Any Location'
pressureLUTColorBar.Position = [0.3515503173164098, 0.7546987951807228]
pressureLUTColorBar.ScalarBarLength = 0.33000000000000035

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
pressureLUT.ApplyPreset('Viridis (matplotlib)', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
pressureLUT.ApplyPreset('Viridis (matplotlib)', True)

# rescale color and/or opacity maps used to exactly fit the current data range
slice2Display.RescaleTransferFunctionToDataRange(False, True)

# convert to log space
pressureLUT.MapControlPointsToLogSpace()

# Properties modified on pressureLUT
pressureLUT.UseLogScale = 1

#change interaction mode for render view
renderView2.InteractionMode = '3D'

#change interaction mode for render view
renderView2.InteractionMode = '2D'

# reset view to fit data bounds
renderView2.ResetCamera(24.829044342041016, 627.0, -50.0, 50.0, 0.0, 0.0, False)

# reset view to fit data
renderView2.ResetCamera(True)

# change scalar bar placement
pressureLUTColorBar.Position = [0.34339075249320034, 0.8028915662650601]
pressureLUTColorBar.ScalarBarLength = 0.33000000000000046

# change scalar bar placement
pressureLUTColorBar.ScalarBarLength = 0.5901994560290116

# change scalar bar placement
pressureLUTColorBar.Position = [0.037860380779691706, 0.8028915662650601]
pressureLUTColorBar.ScalarBarLength = 0.8957298277425202

# set active view
SetActiveView(renderView1)

# hide data in view
Hide(calculator2, renderView1)

# hide data in view
Hide(calculator1, renderView1)

# set active source
SetActiveSource(clip1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice2.SliceType)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=clip1.ClipType)

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(data0000fltxmf, renderView1)

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip1.ClipType)

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# reset view to fit data
renderView1.ResetCamera(True)

# change scalar bar placement
ndensLUTColorBar.Position = [0.08228467815049849, 0.7727710843373493]
ndensLUTColorBar.ScalarBarLength = 0.5784134179510423

# change scalar bar placement
ndensLUTColorBar.Position = [0.037860380779691616, 0.7757831325301204]

# change scalar bar placement
ndensLUTColorBar.ScalarBarLength = 0.9229283771532131

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=slice1.SliceType)

# convert to log space
ndensLUT.MapControlPointsToLogSpace()

# Properties modified on ndensLUT
ndensLUT.UseLogScale = 1

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=slice1.SliceType)

# Rescale transfer function
ndensLUT.RescaleTransferFunction(0.0005, 80.0)

# Rescale transfer function
ndensPWF.RescaleTransferFunction(0.0005, 80.0)

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# set active view
SetActiveView(renderView2)

# set active source
SetActiveSource(data0000fltxmf)

# show data in view
data0000fltxmfDisplay_1 = Show(data0000fltxmf, renderView2, 'StructuredGridRepresentation')

# trace defaults for the display properties.
data0000fltxmfDisplay_1.Selection = None
data0000fltxmfDisplay_1.Representation = 'Outline'
data0000fltxmfDisplay_1.ColorArrayName = ['CELLS', '']
data0000fltxmfDisplay_1.LookupTable = None
data0000fltxmfDisplay_1.MapScalars = 1
data0000fltxmfDisplay_1.MultiComponentsMapping = 0
data0000fltxmfDisplay_1.InterpolateScalarsBeforeMapping = 1
data0000fltxmfDisplay_1.Opacity = 1.0
data0000fltxmfDisplay_1.PointSize = 2.0
data0000fltxmfDisplay_1.LineWidth = 1.0
data0000fltxmfDisplay_1.RenderLinesAsTubes = 0
data0000fltxmfDisplay_1.RenderPointsAsSpheres = 0
data0000fltxmfDisplay_1.Interpolation = 'Gouraud'
data0000fltxmfDisplay_1.Specular = 0.0
data0000fltxmfDisplay_1.SpecularColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.SpecularPower = 100.0
data0000fltxmfDisplay_1.Luminosity = 0.0
data0000fltxmfDisplay_1.Ambient = 0.0
data0000fltxmfDisplay_1.Diffuse = 1.0
data0000fltxmfDisplay_1.Roughness = 0.3
data0000fltxmfDisplay_1.Metallic = 0.0
data0000fltxmfDisplay_1.EdgeTint = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.Anisotropy = 0.0
data0000fltxmfDisplay_1.AnisotropyRotation = 0.0
data0000fltxmfDisplay_1.BaseIOR = 1.5
data0000fltxmfDisplay_1.CoatStrength = 0.0
data0000fltxmfDisplay_1.CoatIOR = 2.0
data0000fltxmfDisplay_1.CoatRoughness = 0.0
data0000fltxmfDisplay_1.CoatColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.SelectTCoordArray = 'None'
data0000fltxmfDisplay_1.SelectNormalArray = 'None'
data0000fltxmfDisplay_1.SelectTangentArray = 'None'
data0000fltxmfDisplay_1.Texture = None
data0000fltxmfDisplay_1.RepeatTextures = 1
data0000fltxmfDisplay_1.InterpolateTextures = 0
data0000fltxmfDisplay_1.SeamlessU = 0
data0000fltxmfDisplay_1.SeamlessV = 0
data0000fltxmfDisplay_1.UseMipmapTextures = 0
data0000fltxmfDisplay_1.ShowTexturesOnBackface = 1
data0000fltxmfDisplay_1.BaseColorTexture = None
data0000fltxmfDisplay_1.NormalTexture = None
data0000fltxmfDisplay_1.NormalScale = 1.0
data0000fltxmfDisplay_1.CoatNormalTexture = None
data0000fltxmfDisplay_1.CoatNormalScale = 1.0
data0000fltxmfDisplay_1.MaterialTexture = None
data0000fltxmfDisplay_1.OcclusionStrength = 1.0
data0000fltxmfDisplay_1.AnisotropyTexture = None
data0000fltxmfDisplay_1.EmissiveTexture = None
data0000fltxmfDisplay_1.EmissiveFactor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.FlipTextures = 0
data0000fltxmfDisplay_1.BackfaceRepresentation = 'Follow Frontface'
data0000fltxmfDisplay_1.BackfaceAmbientColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.BackfaceOpacity = 1.0
data0000fltxmfDisplay_1.Position = [0.0, 0.0, 0.0]
data0000fltxmfDisplay_1.Scale = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.Orientation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay_1.Origin = [0.0, 0.0, 0.0]
data0000fltxmfDisplay_1.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
data0000fltxmfDisplay_1.Pickable = 1
data0000fltxmfDisplay_1.Triangulate = 0
data0000fltxmfDisplay_1.UseShaderReplacements = 0
data0000fltxmfDisplay_1.ShaderReplacements = ''
data0000fltxmfDisplay_1.NonlinearSubdivisionLevel = 1
data0000fltxmfDisplay_1.UseDataPartitions = 0
data0000fltxmfDisplay_1.OSPRayUseScaleArray = 'All Approximate'
data0000fltxmfDisplay_1.OSPRayScaleArray = ''
data0000fltxmfDisplay_1.OSPRayScaleFunction = 'PiecewiseFunction'
data0000fltxmfDisplay_1.OSPRayMaterial = 'None'
data0000fltxmfDisplay_1.BlockSelectors = ['/']
data0000fltxmfDisplay_1.BlockColors = []
data0000fltxmfDisplay_1.BlockOpacities = []
data0000fltxmfDisplay_1.Orient = 0
data0000fltxmfDisplay_1.OrientationMode = 'Direction'
data0000fltxmfDisplay_1.SelectOrientationVectors = 'None'
data0000fltxmfDisplay_1.Scaling = 0
data0000fltxmfDisplay_1.ScaleMode = 'No Data Scaling Off'
data0000fltxmfDisplay_1.ScaleFactor = 60.370842742919926
data0000fltxmfDisplay_1.SelectScaleArray = 'density'
data0000fltxmfDisplay_1.GlyphType = 'Arrow'
data0000fltxmfDisplay_1.UseGlyphTable = 0
data0000fltxmfDisplay_1.GlyphTableIndexArray = 'density'
data0000fltxmfDisplay_1.UseCompositeGlyphTable = 0
data0000fltxmfDisplay_1.UseGlyphCullingAndLOD = 0
data0000fltxmfDisplay_1.LODValues = []
data0000fltxmfDisplay_1.ColorByLODIndex = 0
data0000fltxmfDisplay_1.GaussianRadius = 3.018542137145996
data0000fltxmfDisplay_1.ShaderPreset = 'Sphere'
data0000fltxmfDisplay_1.CustomTriangleScale = 3
data0000fltxmfDisplay_1.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
data0000fltxmfDisplay_1.Emissive = 0
data0000fltxmfDisplay_1.ScaleByArray = 0
data0000fltxmfDisplay_1.SetScaleArray = [None, '']
data0000fltxmfDisplay_1.ScaleArrayComponent = 0
data0000fltxmfDisplay_1.UseScaleFunction = 1
data0000fltxmfDisplay_1.ScaleTransferFunction = 'PiecewiseFunction'
data0000fltxmfDisplay_1.OpacityByArray = 0
data0000fltxmfDisplay_1.OpacityArray = [None, '']
data0000fltxmfDisplay_1.OpacityArrayComponent = 0
data0000fltxmfDisplay_1.OpacityTransferFunction = 'PiecewiseFunction'
data0000fltxmfDisplay_1.DataAxesGrid = 'GridAxesRepresentation'
data0000fltxmfDisplay_1.SelectionCellLabelBold = 0
data0000fltxmfDisplay_1.SelectionCellLabelColor = [0.0, 1.0, 0.0]
data0000fltxmfDisplay_1.SelectionCellLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.SelectionCellLabelFontFile = ''
data0000fltxmfDisplay_1.SelectionCellLabelFontSize = 18
data0000fltxmfDisplay_1.SelectionCellLabelItalic = 0
data0000fltxmfDisplay_1.SelectionCellLabelJustification = 'Left'
data0000fltxmfDisplay_1.SelectionCellLabelOpacity = 1.0
data0000fltxmfDisplay_1.SelectionCellLabelShadow = 0
data0000fltxmfDisplay_1.SelectionPointLabelBold = 0
data0000fltxmfDisplay_1.SelectionPointLabelColor = [1.0, 1.0, 0.0]
data0000fltxmfDisplay_1.SelectionPointLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.SelectionPointLabelFontFile = ''
data0000fltxmfDisplay_1.SelectionPointLabelFontSize = 18
data0000fltxmfDisplay_1.SelectionPointLabelItalic = 0
data0000fltxmfDisplay_1.SelectionPointLabelJustification = 'Left'
data0000fltxmfDisplay_1.SelectionPointLabelOpacity = 1.0
data0000fltxmfDisplay_1.SelectionPointLabelShadow = 0
data0000fltxmfDisplay_1.PolarAxes = 'PolarAxesRepresentation'
data0000fltxmfDisplay_1.ScalarOpacityFunction = None
data0000fltxmfDisplay_1.ScalarOpacityUnitDistance = 1.7320408131091525
data0000fltxmfDisplay_1.SelectMapper = 'Projected tetra'
data0000fltxmfDisplay_1.SamplingDimensions = [128, 128, 128]

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
data0000fltxmfDisplay_1.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay_1.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
data0000fltxmfDisplay_1.GlyphType.TipResolution = 6
data0000fltxmfDisplay_1.GlyphType.TipRadius = 0.1
data0000fltxmfDisplay_1.GlyphType.TipLength = 0.35
data0000fltxmfDisplay_1.GlyphType.ShaftResolution = 6
data0000fltxmfDisplay_1.GlyphType.ShaftRadius = 0.03
data0000fltxmfDisplay_1.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
data0000fltxmfDisplay_1.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay_1.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
data0000fltxmfDisplay_1.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0000fltxmfDisplay_1.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
data0000fltxmfDisplay_1.DataAxesGrid.XTitle = 'X Axis'
data0000fltxmfDisplay_1.DataAxesGrid.YTitle = 'Y Axis'
data0000fltxmfDisplay_1.DataAxesGrid.ZTitle = 'Z Axis'
data0000fltxmfDisplay_1.DataAxesGrid.XTitleFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.XTitleFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.XTitleBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.XTitleItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.XTitleFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.XTitleShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.XTitleOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.YTitleFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.YTitleFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.YTitleBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.YTitleItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.YTitleFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.YTitleShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.YTitleOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZTitleOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.FacesToRender = 63
data0000fltxmfDisplay_1.DataAxesGrid.CullBackface = 0
data0000fltxmfDisplay_1.DataAxesGrid.CullFrontface = 1
data0000fltxmfDisplay_1.DataAxesGrid.ShowGrid = 0
data0000fltxmfDisplay_1.DataAxesGrid.ShowEdges = 1
data0000fltxmfDisplay_1.DataAxesGrid.ShowTicks = 1
data0000fltxmfDisplay_1.DataAxesGrid.LabelUniqueEdgesOnly = 1
data0000fltxmfDisplay_1.DataAxesGrid.AxesToLabel = 63
data0000fltxmfDisplay_1.DataAxesGrid.XLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.XLabelFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.XLabelBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.XLabelItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.XLabelFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.XLabelShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.XLabelOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.YLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.YLabelFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.YLabelBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.YLabelItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.YLabelFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.YLabelShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.YLabelOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelFontFile = ''
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelBold = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelItalic = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelFontSize = 12
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelShadow = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZLabelOpacity = 1.0
data0000fltxmfDisplay_1.DataAxesGrid.XAxisNotation = 'Mixed'
data0000fltxmfDisplay_1.DataAxesGrid.XAxisPrecision = 2
data0000fltxmfDisplay_1.DataAxesGrid.XAxisUseCustomLabels = 0
data0000fltxmfDisplay_1.DataAxesGrid.XAxisLabels = []
data0000fltxmfDisplay_1.DataAxesGrid.YAxisNotation = 'Mixed'
data0000fltxmfDisplay_1.DataAxesGrid.YAxisPrecision = 2
data0000fltxmfDisplay_1.DataAxesGrid.YAxisUseCustomLabels = 0
data0000fltxmfDisplay_1.DataAxesGrid.YAxisLabels = []
data0000fltxmfDisplay_1.DataAxesGrid.ZAxisNotation = 'Mixed'
data0000fltxmfDisplay_1.DataAxesGrid.ZAxisPrecision = 2
data0000fltxmfDisplay_1.DataAxesGrid.ZAxisUseCustomLabels = 0
data0000fltxmfDisplay_1.DataAxesGrid.ZAxisLabels = []
data0000fltxmfDisplay_1.DataAxesGrid.UseCustomBounds = 0
data0000fltxmfDisplay_1.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
data0000fltxmfDisplay_1.PolarAxes.Visibility = 0
data0000fltxmfDisplay_1.PolarAxes.Translation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay_1.PolarAxes.Scale = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.Orientation = [0.0, 0.0, 0.0]
data0000fltxmfDisplay_1.PolarAxes.EnableCustomBounds = [0, 0, 0]
data0000fltxmfDisplay_1.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.EnableCustomRange = 0
data0000fltxmfDisplay_1.PolarAxes.CustomRange = [0.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.PolarAxisVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.RadialAxesVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.DrawRadialGridlines = 1
data0000fltxmfDisplay_1.PolarAxes.PolarArcsVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.DrawPolarArcsGridlines = 1
data0000fltxmfDisplay_1.PolarAxes.NumberOfRadialAxes = 0
data0000fltxmfDisplay_1.PolarAxes.AutoSubdividePolarAxis = 1
data0000fltxmfDisplay_1.PolarAxes.NumberOfPolarAxis = 0
data0000fltxmfDisplay_1.PolarAxes.MinimumRadius = 0.0
data0000fltxmfDisplay_1.PolarAxes.MinimumAngle = 0.0
data0000fltxmfDisplay_1.PolarAxes.MaximumAngle = 90.0
data0000fltxmfDisplay_1.PolarAxes.RadialAxesOriginToPolarAxis = 1
data0000fltxmfDisplay_1.PolarAxes.Ratio = 1.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitle = 'Radial Distance'
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleLocation = 'Bottom'
data0000fltxmfDisplay_1.PolarAxes.PolarLabelVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.PolarLabelFormat = '%-#6.3g'
data0000fltxmfDisplay_1.PolarAxes.PolarLabelExponentLocation = 'Labels'
data0000fltxmfDisplay_1.PolarAxes.RadialLabelVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.RadialLabelFormat = '%-#3.1f'
data0000fltxmfDisplay_1.PolarAxes.RadialLabelLocation = 'Bottom'
data0000fltxmfDisplay_1.PolarAxes.RadialUnitsVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.ScreenSize = 10.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleOpacity = 1.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleFontFile = ''
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleBold = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleItalic = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleShadow = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTitleFontSize = 12
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelOpacity = 1.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelFontFile = ''
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelBold = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelItalic = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelShadow = 0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisLabelFontSize = 12
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextOpacity = 1.0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextFontFile = ''
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextBold = 0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextItalic = 0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextShadow = 0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTextFontSize = 12
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextFontFile = ''
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextBold = 0
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextItalic = 0
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextShadow = 0
data0000fltxmfDisplay_1.PolarAxes.SecondaryRadialAxesTextFontSize = 12
data0000fltxmfDisplay_1.PolarAxes.EnableDistanceLOD = 1
data0000fltxmfDisplay_1.PolarAxes.DistanceLODThreshold = 0.7
data0000fltxmfDisplay_1.PolarAxes.EnableViewAngleLOD = 1
data0000fltxmfDisplay_1.PolarAxes.ViewAngleLODThreshold = 0.7
data0000fltxmfDisplay_1.PolarAxes.SmallestVisiblePolarAngle = 0.5
data0000fltxmfDisplay_1.PolarAxes.PolarTicksVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.ArcTicksOriginToPolarAxis = 1
data0000fltxmfDisplay_1.PolarAxes.TickLocation = 'Both'
data0000fltxmfDisplay_1.PolarAxes.AxisTickVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.AxisMinorTickVisibility = 0
data0000fltxmfDisplay_1.PolarAxes.ArcTickVisibility = 1
data0000fltxmfDisplay_1.PolarAxes.ArcMinorTickVisibility = 0
data0000fltxmfDisplay_1.PolarAxes.DeltaAngleMajor = 10.0
data0000fltxmfDisplay_1.PolarAxes.DeltaAngleMinor = 5.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisMajorTickSize = 0.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTickRatioSize = 0.3
data0000fltxmfDisplay_1.PolarAxes.PolarAxisMajorTickThickness = 1.0
data0000fltxmfDisplay_1.PolarAxes.PolarAxisTickRatioThickness = 0.5
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisMajorTickSize = 0.0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTickRatioSize = 0.3
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
data0000fltxmfDisplay_1.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
data0000fltxmfDisplay_1.PolarAxes.ArcMajorTickSize = 0.0
data0000fltxmfDisplay_1.PolarAxes.ArcTickRatioSize = 0.3
data0000fltxmfDisplay_1.PolarAxes.ArcMajorTickThickness = 1.0
data0000fltxmfDisplay_1.PolarAxes.ArcTickRatioThickness = 0.5
data0000fltxmfDisplay_1.PolarAxes.Use2DMode = 0
data0000fltxmfDisplay_1.PolarAxes.UseLogAxis = 0

# hide data in view
Hide(data0000fltxmf, renderView2)

# set active source
SetActiveSource(clip1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=clip1.ClipType)

# show data in view
clip1Display_1 = Show(clip1, renderView2, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display_1.Selection = None
clip1Display_1.Representation = 'Surface'
clip1Display_1.ColorArrayName = ['CELLS', 'density']
clip1Display_1.LookupTable = densityLUT
clip1Display_1.MapScalars = 1
clip1Display_1.MultiComponentsMapping = 0
clip1Display_1.InterpolateScalarsBeforeMapping = 1
clip1Display_1.Opacity = 1.0
clip1Display_1.PointSize = 2.0
clip1Display_1.LineWidth = 1.0
clip1Display_1.RenderLinesAsTubes = 0
clip1Display_1.RenderPointsAsSpheres = 0
clip1Display_1.Interpolation = 'Gouraud'
clip1Display_1.Specular = 0.0
clip1Display_1.SpecularColor = [1.0, 1.0, 1.0]
clip1Display_1.SpecularPower = 100.0
clip1Display_1.Luminosity = 0.0
clip1Display_1.Ambient = 0.0
clip1Display_1.Diffuse = 1.0
clip1Display_1.Roughness = 0.3
clip1Display_1.Metallic = 0.0
clip1Display_1.EdgeTint = [1.0, 1.0, 1.0]
clip1Display_1.Anisotropy = 0.0
clip1Display_1.AnisotropyRotation = 0.0
clip1Display_1.BaseIOR = 1.5
clip1Display_1.CoatStrength = 0.0
clip1Display_1.CoatIOR = 2.0
clip1Display_1.CoatRoughness = 0.0
clip1Display_1.CoatColor = [1.0, 1.0, 1.0]
clip1Display_1.SelectTCoordArray = 'None'
clip1Display_1.SelectNormalArray = 'None'
clip1Display_1.SelectTangentArray = 'None'
clip1Display_1.Texture = None
clip1Display_1.RepeatTextures = 1
clip1Display_1.InterpolateTextures = 0
clip1Display_1.SeamlessU = 0
clip1Display_1.SeamlessV = 0
clip1Display_1.UseMipmapTextures = 0
clip1Display_1.ShowTexturesOnBackface = 1
clip1Display_1.BaseColorTexture = None
clip1Display_1.NormalTexture = None
clip1Display_1.NormalScale = 1.0
clip1Display_1.CoatNormalTexture = None
clip1Display_1.CoatNormalScale = 1.0
clip1Display_1.MaterialTexture = None
clip1Display_1.OcclusionStrength = 1.0
clip1Display_1.AnisotropyTexture = None
clip1Display_1.EmissiveTexture = None
clip1Display_1.EmissiveFactor = [1.0, 1.0, 1.0]
clip1Display_1.FlipTextures = 0
clip1Display_1.BackfaceRepresentation = 'Follow Frontface'
clip1Display_1.BackfaceAmbientColor = [1.0, 1.0, 1.0]
clip1Display_1.BackfaceOpacity = 1.0
clip1Display_1.Position = [0.0, 0.0, 0.0]
clip1Display_1.Scale = [1.0, 1.0, 1.0]
clip1Display_1.Orientation = [0.0, 0.0, 0.0]
clip1Display_1.Origin = [0.0, 0.0, 0.0]
clip1Display_1.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
clip1Display_1.Pickable = 1
clip1Display_1.Triangulate = 0
clip1Display_1.UseShaderReplacements = 0
clip1Display_1.ShaderReplacements = ''
clip1Display_1.NonlinearSubdivisionLevel = 1
clip1Display_1.UseDataPartitions = 0
clip1Display_1.OSPRayUseScaleArray = 'All Approximate'
clip1Display_1.OSPRayScaleArray = ''
clip1Display_1.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display_1.OSPRayMaterial = 'None'
clip1Display_1.BlockSelectors = ['/']
clip1Display_1.BlockColors = []
clip1Display_1.BlockOpacities = []
clip1Display_1.Orient = 0
clip1Display_1.OrientationMode = 'Direction'
clip1Display_1.SelectOrientationVectors = 'None'
clip1Display_1.Scaling = 0
clip1Display_1.ScaleMode = 'No Data Scaling Off'
clip1Display_1.ScaleFactor = 60.370842742919926
clip1Display_1.SelectScaleArray = 'density'
clip1Display_1.GlyphType = 'Arrow'
clip1Display_1.UseGlyphTable = 0
clip1Display_1.GlyphTableIndexArray = 'density'
clip1Display_1.UseCompositeGlyphTable = 0
clip1Display_1.UseGlyphCullingAndLOD = 0
clip1Display_1.LODValues = []
clip1Display_1.ColorByLODIndex = 0
clip1Display_1.GaussianRadius = 3.018542137145996
clip1Display_1.ShaderPreset = 'Sphere'
clip1Display_1.CustomTriangleScale = 3
clip1Display_1.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
clip1Display_1.Emissive = 0
clip1Display_1.ScaleByArray = 0
clip1Display_1.SetScaleArray = [None, '']
clip1Display_1.ScaleArrayComponent = 0
clip1Display_1.UseScaleFunction = 1
clip1Display_1.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display_1.OpacityByArray = 0
clip1Display_1.OpacityArray = [None, '']
clip1Display_1.OpacityArrayComponent = 0
clip1Display_1.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display_1.DataAxesGrid = 'GridAxesRepresentation'
clip1Display_1.SelectionCellLabelBold = 0
clip1Display_1.SelectionCellLabelColor = [0.0, 1.0, 0.0]
clip1Display_1.SelectionCellLabelFontFamily = 'Arial'
clip1Display_1.SelectionCellLabelFontFile = ''
clip1Display_1.SelectionCellLabelFontSize = 18
clip1Display_1.SelectionCellLabelItalic = 0
clip1Display_1.SelectionCellLabelJustification = 'Left'
clip1Display_1.SelectionCellLabelOpacity = 1.0
clip1Display_1.SelectionCellLabelShadow = 0
clip1Display_1.SelectionPointLabelBold = 0
clip1Display_1.SelectionPointLabelColor = [1.0, 1.0, 0.0]
clip1Display_1.SelectionPointLabelFontFamily = 'Arial'
clip1Display_1.SelectionPointLabelFontFile = ''
clip1Display_1.SelectionPointLabelFontSize = 18
clip1Display_1.SelectionPointLabelItalic = 0
clip1Display_1.SelectionPointLabelJustification = 'Left'
clip1Display_1.SelectionPointLabelOpacity = 1.0
clip1Display_1.SelectionPointLabelShadow = 0
clip1Display_1.PolarAxes = 'PolarAxesRepresentation'
clip1Display_1.ScalarOpacityFunction = densityPWF
clip1Display_1.ScalarOpacityUnitDistance = 1.7786614177350901
clip1Display_1.UseSeparateOpacityArray = 0
clip1Display_1.OpacityArrayName = ['CELLS', 'density']
clip1Display_1.OpacityComponent = ''
clip1Display_1.SelectMapper = 'Projected tetra'
clip1Display_1.SamplingDimensions = [128, 128, 128]
clip1Display_1.UseFloatingPointFrameBuffer = 1

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
clip1Display_1.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display_1.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
clip1Display_1.GlyphType.TipResolution = 6
clip1Display_1.GlyphType.TipRadius = 0.1
clip1Display_1.GlyphType.TipLength = 0.35
clip1Display_1.GlyphType.ShaftResolution = 6
clip1Display_1.GlyphType.ShaftRadius = 0.03
clip1Display_1.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
clip1Display_1.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display_1.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
clip1Display_1.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
clip1Display_1.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
clip1Display_1.DataAxesGrid.XTitle = 'X Axis'
clip1Display_1.DataAxesGrid.YTitle = 'Y Axis'
clip1Display_1.DataAxesGrid.ZTitle = 'Z Axis'
clip1Display_1.DataAxesGrid.XTitleFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.XTitleFontFile = ''
clip1Display_1.DataAxesGrid.XTitleBold = 0
clip1Display_1.DataAxesGrid.XTitleItalic = 0
clip1Display_1.DataAxesGrid.XTitleFontSize = 12
clip1Display_1.DataAxesGrid.XTitleShadow = 0
clip1Display_1.DataAxesGrid.XTitleOpacity = 1.0
clip1Display_1.DataAxesGrid.YTitleFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.YTitleFontFile = ''
clip1Display_1.DataAxesGrid.YTitleBold = 0
clip1Display_1.DataAxesGrid.YTitleItalic = 0
clip1Display_1.DataAxesGrid.YTitleFontSize = 12
clip1Display_1.DataAxesGrid.YTitleShadow = 0
clip1Display_1.DataAxesGrid.YTitleOpacity = 1.0
clip1Display_1.DataAxesGrid.ZTitleFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.ZTitleFontFile = ''
clip1Display_1.DataAxesGrid.ZTitleBold = 0
clip1Display_1.DataAxesGrid.ZTitleItalic = 0
clip1Display_1.DataAxesGrid.ZTitleFontSize = 12
clip1Display_1.DataAxesGrid.ZTitleShadow = 0
clip1Display_1.DataAxesGrid.ZTitleOpacity = 1.0
clip1Display_1.DataAxesGrid.FacesToRender = 63
clip1Display_1.DataAxesGrid.CullBackface = 0
clip1Display_1.DataAxesGrid.CullFrontface = 1
clip1Display_1.DataAxesGrid.ShowGrid = 0
clip1Display_1.DataAxesGrid.ShowEdges = 1
clip1Display_1.DataAxesGrid.ShowTicks = 1
clip1Display_1.DataAxesGrid.LabelUniqueEdgesOnly = 1
clip1Display_1.DataAxesGrid.AxesToLabel = 63
clip1Display_1.DataAxesGrid.XLabelFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.XLabelFontFile = ''
clip1Display_1.DataAxesGrid.XLabelBold = 0
clip1Display_1.DataAxesGrid.XLabelItalic = 0
clip1Display_1.DataAxesGrid.XLabelFontSize = 12
clip1Display_1.DataAxesGrid.XLabelShadow = 0
clip1Display_1.DataAxesGrid.XLabelOpacity = 1.0
clip1Display_1.DataAxesGrid.YLabelFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.YLabelFontFile = ''
clip1Display_1.DataAxesGrid.YLabelBold = 0
clip1Display_1.DataAxesGrid.YLabelItalic = 0
clip1Display_1.DataAxesGrid.YLabelFontSize = 12
clip1Display_1.DataAxesGrid.YLabelShadow = 0
clip1Display_1.DataAxesGrid.YLabelOpacity = 1.0
clip1Display_1.DataAxesGrid.ZLabelFontFamily = 'Arial'
clip1Display_1.DataAxesGrid.ZLabelFontFile = ''
clip1Display_1.DataAxesGrid.ZLabelBold = 0
clip1Display_1.DataAxesGrid.ZLabelItalic = 0
clip1Display_1.DataAxesGrid.ZLabelFontSize = 12
clip1Display_1.DataAxesGrid.ZLabelShadow = 0
clip1Display_1.DataAxesGrid.ZLabelOpacity = 1.0
clip1Display_1.DataAxesGrid.XAxisNotation = 'Mixed'
clip1Display_1.DataAxesGrid.XAxisPrecision = 2
clip1Display_1.DataAxesGrid.XAxisUseCustomLabels = 0
clip1Display_1.DataAxesGrid.XAxisLabels = []
clip1Display_1.DataAxesGrid.YAxisNotation = 'Mixed'
clip1Display_1.DataAxesGrid.YAxisPrecision = 2
clip1Display_1.DataAxesGrid.YAxisUseCustomLabels = 0
clip1Display_1.DataAxesGrid.YAxisLabels = []
clip1Display_1.DataAxesGrid.ZAxisNotation = 'Mixed'
clip1Display_1.DataAxesGrid.ZAxisPrecision = 2
clip1Display_1.DataAxesGrid.ZAxisUseCustomLabels = 0
clip1Display_1.DataAxesGrid.ZAxisLabels = []
clip1Display_1.DataAxesGrid.UseCustomBounds = 0
clip1Display_1.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
clip1Display_1.PolarAxes.Visibility = 0
clip1Display_1.PolarAxes.Translation = [0.0, 0.0, 0.0]
clip1Display_1.PolarAxes.Scale = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.Orientation = [0.0, 0.0, 0.0]
clip1Display_1.PolarAxes.EnableCustomBounds = [0, 0, 0]
clip1Display_1.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
clip1Display_1.PolarAxes.EnableCustomRange = 0
clip1Display_1.PolarAxes.CustomRange = [0.0, 1.0]
clip1Display_1.PolarAxes.PolarAxisVisibility = 1
clip1Display_1.PolarAxes.RadialAxesVisibility = 1
clip1Display_1.PolarAxes.DrawRadialGridlines = 1
clip1Display_1.PolarAxes.PolarArcsVisibility = 1
clip1Display_1.PolarAxes.DrawPolarArcsGridlines = 1
clip1Display_1.PolarAxes.NumberOfRadialAxes = 0
clip1Display_1.PolarAxes.AutoSubdividePolarAxis = 1
clip1Display_1.PolarAxes.NumberOfPolarAxis = 0
clip1Display_1.PolarAxes.MinimumRadius = 0.0
clip1Display_1.PolarAxes.MinimumAngle = 0.0
clip1Display_1.PolarAxes.MaximumAngle = 90.0
clip1Display_1.PolarAxes.RadialAxesOriginToPolarAxis = 1
clip1Display_1.PolarAxes.Ratio = 1.0
clip1Display_1.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
clip1Display_1.PolarAxes.PolarAxisTitleVisibility = 1
clip1Display_1.PolarAxes.PolarAxisTitle = 'Radial Distance'
clip1Display_1.PolarAxes.PolarAxisTitleLocation = 'Bottom'
clip1Display_1.PolarAxes.PolarLabelVisibility = 1
clip1Display_1.PolarAxes.PolarLabelFormat = '%-#6.3g'
clip1Display_1.PolarAxes.PolarLabelExponentLocation = 'Labels'
clip1Display_1.PolarAxes.RadialLabelVisibility = 1
clip1Display_1.PolarAxes.RadialLabelFormat = '%-#3.1f'
clip1Display_1.PolarAxes.RadialLabelLocation = 'Bottom'
clip1Display_1.PolarAxes.RadialUnitsVisibility = 1
clip1Display_1.PolarAxes.ScreenSize = 10.0
clip1Display_1.PolarAxes.PolarAxisTitleOpacity = 1.0
clip1Display_1.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
clip1Display_1.PolarAxes.PolarAxisTitleFontFile = ''
clip1Display_1.PolarAxes.PolarAxisTitleBold = 0
clip1Display_1.PolarAxes.PolarAxisTitleItalic = 0
clip1Display_1.PolarAxes.PolarAxisTitleShadow = 0
clip1Display_1.PolarAxes.PolarAxisTitleFontSize = 12
clip1Display_1.PolarAxes.PolarAxisLabelOpacity = 1.0
clip1Display_1.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
clip1Display_1.PolarAxes.PolarAxisLabelFontFile = ''
clip1Display_1.PolarAxes.PolarAxisLabelBold = 0
clip1Display_1.PolarAxes.PolarAxisLabelItalic = 0
clip1Display_1.PolarAxes.PolarAxisLabelShadow = 0
clip1Display_1.PolarAxes.PolarAxisLabelFontSize = 12
clip1Display_1.PolarAxes.LastRadialAxisTextOpacity = 1.0
clip1Display_1.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
clip1Display_1.PolarAxes.LastRadialAxisTextFontFile = ''
clip1Display_1.PolarAxes.LastRadialAxisTextBold = 0
clip1Display_1.PolarAxes.LastRadialAxisTextItalic = 0
clip1Display_1.PolarAxes.LastRadialAxisTextShadow = 0
clip1Display_1.PolarAxes.LastRadialAxisTextFontSize = 12
clip1Display_1.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
clip1Display_1.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
clip1Display_1.PolarAxes.SecondaryRadialAxesTextFontFile = ''
clip1Display_1.PolarAxes.SecondaryRadialAxesTextBold = 0
clip1Display_1.PolarAxes.SecondaryRadialAxesTextItalic = 0
clip1Display_1.PolarAxes.SecondaryRadialAxesTextShadow = 0
clip1Display_1.PolarAxes.SecondaryRadialAxesTextFontSize = 12
clip1Display_1.PolarAxes.EnableDistanceLOD = 1
clip1Display_1.PolarAxes.DistanceLODThreshold = 0.7
clip1Display_1.PolarAxes.EnableViewAngleLOD = 1
clip1Display_1.PolarAxes.ViewAngleLODThreshold = 0.7
clip1Display_1.PolarAxes.SmallestVisiblePolarAngle = 0.5
clip1Display_1.PolarAxes.PolarTicksVisibility = 1
clip1Display_1.PolarAxes.ArcTicksOriginToPolarAxis = 1
clip1Display_1.PolarAxes.TickLocation = 'Both'
clip1Display_1.PolarAxes.AxisTickVisibility = 1
clip1Display_1.PolarAxes.AxisMinorTickVisibility = 0
clip1Display_1.PolarAxes.ArcTickVisibility = 1
clip1Display_1.PolarAxes.ArcMinorTickVisibility = 0
clip1Display_1.PolarAxes.DeltaAngleMajor = 10.0
clip1Display_1.PolarAxes.DeltaAngleMinor = 5.0
clip1Display_1.PolarAxes.PolarAxisMajorTickSize = 0.0
clip1Display_1.PolarAxes.PolarAxisTickRatioSize = 0.3
clip1Display_1.PolarAxes.PolarAxisMajorTickThickness = 1.0
clip1Display_1.PolarAxes.PolarAxisTickRatioThickness = 0.5
clip1Display_1.PolarAxes.LastRadialAxisMajorTickSize = 0.0
clip1Display_1.PolarAxes.LastRadialAxisTickRatioSize = 0.3
clip1Display_1.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
clip1Display_1.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
clip1Display_1.PolarAxes.ArcMajorTickSize = 0.0
clip1Display_1.PolarAxes.ArcTickRatioSize = 0.3
clip1Display_1.PolarAxes.ArcMajorTickThickness = 1.0
clip1Display_1.PolarAxes.ArcTickRatioThickness = 0.5
clip1Display_1.PolarAxes.Use2DMode = 0
clip1Display_1.PolarAxes.UseLogAxis = 0

# show color bar/color legend
clip1Display_1.SetScalarBarVisibility(renderView2, True)

# turn off scalar coloring
ColorBy(clip1Display_1, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(densityLUT, renderView2)

# change representation type
clip1Display_1.SetRepresentationType('Outline')

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip1.ClipType)

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=slice1.SliceType)

# set active source
SetActiveSource(slice2)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=slice2.SliceType)

# reset view to fit data
renderView2.ResetCamera(True)

# reset view to fit data
renderView2.ResetCamera(True)

# reset view to fit data
renderView2.ResetCamera(True)

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice2.SliceType)

# reset view to fit data
renderView2.ResetCamera(True)

# create a new 'Text'
text1 = Text(registrationName='Text1')
text1.Text = 'Text'

# Properties modified on text1
text1.Text = '$t/t_{\\rm cc, ini} = $'+f'{file_no:.1f}'

# show data in view
text1Display = Show(text1, renderView2, 'TextSourceRepresentation')

# trace defaults for the display properties.
text1Display.TextPropMode = '2D Text Widget'
text1Display.Interactivity = 1
text1Display.WindowLocation = 'Upper Left Corner'
text1Display.Position = [0.05, 0.05]
text1Display.Opacity = 1.0
text1Display.FontFamily = 'Arial'
text1Display.FontFile = ''
text1Display.Bold = 0
text1Display.Italic = 0
text1Display.Shadow = 0
text1Display.FontSize = 18
text1Display.Justification = 'Center'
text1Display.VerticalJustification = 'Center'
text1Display.ShowBorder = 'Only on hover'
text1Display.BackgroundColor = [1.0, 1.0, 1.0, 0.2]
text1Display.BorderThickness = 0.0
text1Display.CornerRadius = 0.0
text1Display.Padding = 1
text1Display.BasePosition = [0.0, 0.0, 0.0]
text1Display.TopPosition = [0.0, 1.0, 0.0]
text1Display.FlagSize = 1.0
text1Display.BillboardPosition = [0.0, 0.0, 0.0]
text1Display.DisplayOffset = [0, 0]

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on text1
text1.Text = '$t/t_{\\rm cc, ini} = $'+f'{file_no:.1f}'

# update the view to ensure updated data information
renderView2.Update()

# Properties modified on text1Display
text1Display.WindowLocation = 'Lower Center'

# Properties modified on text1Display
text1Display.FontSize = 19

# Properties modified on text1Display
text1Display.FontSize = 20

# Properties modified on text1Display
text1Display.FontSize = 21

# Properties modified on text1Display
text1Display.FontSize = 22

# Properties modified on text1Display
text1Display.FontSize = 23

# Properties modified on text1Display
text1Display.FontSize = 24

# Properties modified on text1Display
text1Display.FontSize = 25

# Properties modified on text1Display
text1Display.FontSize = 26

# Properties modified on text1Display
text1Display.FontSize = 27

# Properties modified on text1Display
text1Display.FontSize = 28

# Properties modified on text1Display
text1Display.FontSize = 29

# Properties modified on text1Display
text1Display.FontSize = 30

# Properties modified on text1Display
text1Display.FontSize = 31

# Properties modified on text1Display
text1Display.FontSize = 32

# Properties modified on text1Display
text1Display.FontSize = 33

# Properties modified on text1Display
text1Display.FontSize = 34

# Properties modified on text1Display
text1Display.FontSize = 35

# Properties modified on text1Display
text1Display.FontSize = 34

# Properties modified on text1Display
text1Display.FontSize = 33

# Properties modified on text1Display
text1Display.FontSize = 32

# Properties modified on text1Display
text1Display.FontSize = 31

# Properties modified on text1Display
text1Display.FontSize = 30

# Properties modified on text1Display
text1Display.FontSize = 29

# Properties modified on text1Display
text1Display.FontSize = 28

# Properties modified on text1Display
text1Display.FontSize = 27

# Properties modified on text1Display
text1Display.FontSize = 26

# Properties modified on text1Display
text1Display.FontSize = 25

# set active source
SetActiveSource(data0000fltxmf)

# layout/tab size in pixels
layout1.SetSize(1103, 665)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView1.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView1.CameraParallelScale = 100.87470293261362

# current camera placement for renderView2
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView2.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView2.CameraParallelScale = 100.87470293261362

'''
# save screenshot
SaveScreenshot('/freya/ptmp/mpa/adutt/CCinCC85/cc85/python-scripts/vis-scripts/test-00.png', layout1, SaveAllViews=1,
    ImageResolution=[1102, 665],
    FontScaling='Scale fonts proportionally',
    SeparatorWidth=1,
    SeparatorColor=[0.937, 0.922, 0.906],
    OverrideColorPalette='',
    StereoMode='No change',
    TransparentBackground=0, 
    # PNG options
    CompressionLevel='0',
    MetaData=['Application', 'ParaView'])
'''

# set active view
SetActiveView(renderView1)

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Show3DWidgets(proxy=slice1.SliceType)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
ndensLUT.ApplyPreset('Inferno (matplotlib)', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
ndensLUT.ApplyPreset('Inferno (matplotlib)', True)

# set active view
SetActiveView(renderView2)

# set active source
SetActiveSource(data0000fltxmf)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# layout/tab size in pixels
layout1.SetSize(1103, 665)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView1.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView1.CameraParallelScale = 100.87470293261362

# current camera placement for renderView2
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView2.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView2.CameraParallelScale = 100.87470293261362

# save screenshot
SaveScreenshot(f'{root}/python-scripts/vis-scripts/ndens_prs-{int(sys.argv[-1]):04d}.png', layout1, SaveAllViews=1,
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

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1103, 665)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView1.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView1.CameraParallelScale = 100.87470293261362

# current camera placement for renderView2
renderView2.InteractionMode = '2D'
renderView2.CameraPosition = [325.1457862854004, 0.0, 1197.8475191596485]
renderView2.CameraFocalPoint = [325.1457862854004, 0.0, 0.0]
renderView2.CameraParallelScale = 100.87470293261362

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).