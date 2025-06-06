# trace generated using paraview version 5.11.2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

file_no = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# get layout
layout1 = GetLayout()

#Enter preview mode
layout1.PreviewMode = [1280, 720]
# Adjust camera

# create a new 'XDMF Reader'
data0025fltxmf = XDMFReader(registrationName='data.0025.flt.xmf', FileNames=['/freya/ptmp/mpa/adutt/CCinCC85/cc85/output-c100,m1.496,T4e4,t0.20,r70.671/data.%04d.flt.xmf'%file_no])
data0025fltxmf.PointArrayStatus = []
data0025fltxmf.CellArrayStatus = ['X', 'Y', 'Z', 'cellvol', 'delRhoByRhoWind', 'delTbyTwind', 'density', 'mach', 'ndens', 'pressure', 'temperature', 'tr1', 'vphi', 'vr', 'vth']
data0025fltxmf.SetStatus = []
data0025fltxmf.GridStatus = ['node_mesh']
data0025fltxmf.Stride = [1, 1, 1]
# Adjust camera

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# rename source object
RenameSource('grid', data0025fltxmf)

# show data in view
data0025fltxmfDisplay = Show(data0025fltxmf, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
data0025fltxmfDisplay.Selection = None
data0025fltxmfDisplay.Representation = 'Outline'
data0025fltxmfDisplay.ColorArrayName = ['CELLS', '']
data0025fltxmfDisplay.LookupTable = None
data0025fltxmfDisplay.MapScalars = 1
data0025fltxmfDisplay.MultiComponentsMapping = 0
data0025fltxmfDisplay.InterpolateScalarsBeforeMapping = 1
data0025fltxmfDisplay.Opacity = 1.0
data0025fltxmfDisplay.PointSize = 2.0
data0025fltxmfDisplay.LineWidth = 1.0
data0025fltxmfDisplay.RenderLinesAsTubes = 0
data0025fltxmfDisplay.RenderPointsAsSpheres = 0
data0025fltxmfDisplay.Interpolation = 'Gouraud'
data0025fltxmfDisplay.Specular = 0.0
data0025fltxmfDisplay.SpecularColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.SpecularPower = 100.0
data0025fltxmfDisplay.Luminosity = 0.0
data0025fltxmfDisplay.Ambient = 0.0
data0025fltxmfDisplay.Diffuse = 1.0
data0025fltxmfDisplay.Roughness = 0.3
data0025fltxmfDisplay.Metallic = 0.0
data0025fltxmfDisplay.EdgeTint = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.Anisotropy = 0.0
data0025fltxmfDisplay.AnisotropyRotation = 0.0
data0025fltxmfDisplay.BaseIOR = 1.5
data0025fltxmfDisplay.CoatStrength = 0.0
data0025fltxmfDisplay.CoatIOR = 2.0
data0025fltxmfDisplay.CoatRoughness = 0.0
data0025fltxmfDisplay.CoatColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.SelectTCoordArray = 'None'
data0025fltxmfDisplay.SelectNormalArray = 'None'
data0025fltxmfDisplay.SelectTangentArray = 'None'
data0025fltxmfDisplay.Texture = None
data0025fltxmfDisplay.RepeatTextures = 1
data0025fltxmfDisplay.InterpolateTextures = 0
data0025fltxmfDisplay.SeamlessU = 0
data0025fltxmfDisplay.SeamlessV = 0
data0025fltxmfDisplay.UseMipmapTextures = 0
data0025fltxmfDisplay.ShowTexturesOnBackface = 1
data0025fltxmfDisplay.BaseColorTexture = None
data0025fltxmfDisplay.NormalTexture = None
data0025fltxmfDisplay.NormalScale = 1.0
data0025fltxmfDisplay.CoatNormalTexture = None
data0025fltxmfDisplay.CoatNormalScale = 1.0
data0025fltxmfDisplay.MaterialTexture = None
data0025fltxmfDisplay.OcclusionStrength = 1.0
data0025fltxmfDisplay.AnisotropyTexture = None
data0025fltxmfDisplay.EmissiveTexture = None
data0025fltxmfDisplay.EmissiveFactor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.FlipTextures = 0
data0025fltxmfDisplay.BackfaceRepresentation = 'Follow Frontface'
data0025fltxmfDisplay.BackfaceAmbientColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.BackfaceOpacity = 1.0
data0025fltxmfDisplay.Position = [0.0, 0.0, 0.0]
data0025fltxmfDisplay.Scale = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.Orientation = [0.0, 0.0, 0.0]
data0025fltxmfDisplay.Origin = [0.0, 0.0, 0.0]
data0025fltxmfDisplay.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
data0025fltxmfDisplay.Pickable = 1
data0025fltxmfDisplay.Triangulate = 0
data0025fltxmfDisplay.UseShaderReplacements = 0
data0025fltxmfDisplay.ShaderReplacements = ''
data0025fltxmfDisplay.NonlinearSubdivisionLevel = 1
data0025fltxmfDisplay.UseDataPartitions = 0
data0025fltxmfDisplay.OSPRayUseScaleArray = 'All Approximate'
data0025fltxmfDisplay.OSPRayScaleArray = ''
data0025fltxmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
data0025fltxmfDisplay.OSPRayMaterial = 'None'
data0025fltxmfDisplay.BlockSelectors = ['/']
data0025fltxmfDisplay.BlockColors = []
data0025fltxmfDisplay.BlockOpacities = []
data0025fltxmfDisplay.Orient = 0
data0025fltxmfDisplay.OrientationMode = 'Direction'
data0025fltxmfDisplay.SelectOrientationVectors = 'None'
data0025fltxmfDisplay.Scaling = 0
data0025fltxmfDisplay.ScaleMode = 'No Data Scaling Off'
data0025fltxmfDisplay.ScaleFactor = 60.3514892578125
data0025fltxmfDisplay.SelectScaleArray = 'density'
data0025fltxmfDisplay.GlyphType = 'Arrow'
data0025fltxmfDisplay.UseGlyphTable = 0
data0025fltxmfDisplay.GlyphTableIndexArray = 'density'
data0025fltxmfDisplay.UseCompositeGlyphTable = 0
data0025fltxmfDisplay.UseGlyphCullingAndLOD = 0
data0025fltxmfDisplay.LODValues = []
data0025fltxmfDisplay.ColorByLODIndex = 0
data0025fltxmfDisplay.GaussianRadius = 3.017574462890625
data0025fltxmfDisplay.ShaderPreset = 'Sphere'
data0025fltxmfDisplay.CustomTriangleScale = 3
data0025fltxmfDisplay.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
data0025fltxmfDisplay.Emissive = 0
data0025fltxmfDisplay.ScaleByArray = 0
data0025fltxmfDisplay.SetScaleArray = [None, '']
data0025fltxmfDisplay.ScaleArrayComponent = 0
data0025fltxmfDisplay.UseScaleFunction = 1
data0025fltxmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
data0025fltxmfDisplay.OpacityByArray = 0
data0025fltxmfDisplay.OpacityArray = [None, '']
data0025fltxmfDisplay.OpacityArrayComponent = 0
data0025fltxmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
data0025fltxmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
data0025fltxmfDisplay.SelectionCellLabelBold = 0
data0025fltxmfDisplay.SelectionCellLabelColor = [0.0, 1.0, 0.0]
data0025fltxmfDisplay.SelectionCellLabelFontFamily = 'Arial'
data0025fltxmfDisplay.SelectionCellLabelFontFile = ''
data0025fltxmfDisplay.SelectionCellLabelFontSize = 18
data0025fltxmfDisplay.SelectionCellLabelItalic = 0
data0025fltxmfDisplay.SelectionCellLabelJustification = 'Left'
data0025fltxmfDisplay.SelectionCellLabelOpacity = 1.0
data0025fltxmfDisplay.SelectionCellLabelShadow = 0
data0025fltxmfDisplay.SelectionPointLabelBold = 0
data0025fltxmfDisplay.SelectionPointLabelColor = [1.0, 1.0, 0.0]
data0025fltxmfDisplay.SelectionPointLabelFontFamily = 'Arial'
data0025fltxmfDisplay.SelectionPointLabelFontFile = ''
data0025fltxmfDisplay.SelectionPointLabelFontSize = 18
data0025fltxmfDisplay.SelectionPointLabelItalic = 0
data0025fltxmfDisplay.SelectionPointLabelJustification = 'Left'
data0025fltxmfDisplay.SelectionPointLabelOpacity = 1.0
data0025fltxmfDisplay.SelectionPointLabelShadow = 0
data0025fltxmfDisplay.PolarAxes = 'PolarAxesRepresentation'
data0025fltxmfDisplay.ScalarOpacityFunction = None
data0025fltxmfDisplay.ScalarOpacityUnitDistance = 1.3584736846424879
data0025fltxmfDisplay.SelectMapper = 'Projected tetra'
data0025fltxmfDisplay.SamplingDimensions = [128, 128, 128]
data0025fltxmfDisplay.SelectInputVectors = [None, '']
data0025fltxmfDisplay.NumberOfSteps = 40
data0025fltxmfDisplay.StepSize = 0.25
data0025fltxmfDisplay.NormalizeVectors = 1
data0025fltxmfDisplay.EnhancedLIC = 1
data0025fltxmfDisplay.ColorMode = 'Blend'
data0025fltxmfDisplay.LICIntensity = 0.8
data0025fltxmfDisplay.MapModeBias = 0.0
data0025fltxmfDisplay.EnhanceContrast = 'Off'
data0025fltxmfDisplay.LowLICContrastEnhancementFactor = 0.0
data0025fltxmfDisplay.HighLICContrastEnhancementFactor = 0.0
data0025fltxmfDisplay.LowColorContrastEnhancementFactor = 0.0
data0025fltxmfDisplay.HighColorContrastEnhancementFactor = 0.0
data0025fltxmfDisplay.AntiAlias = 0
data0025fltxmfDisplay.MaskOnSurface = 1
data0025fltxmfDisplay.MaskThreshold = 0.0
data0025fltxmfDisplay.MaskIntensity = 0.0
data0025fltxmfDisplay.MaskColor = [0.5, 0.5, 0.5]
data0025fltxmfDisplay.GenerateNoiseTexture = 0
data0025fltxmfDisplay.NoiseType = 'Gaussian'
data0025fltxmfDisplay.NoiseTextureSize = 128
data0025fltxmfDisplay.NoiseGrainSize = 2
data0025fltxmfDisplay.MinNoiseValue = 0.0
data0025fltxmfDisplay.MaxNoiseValue = 0.8
data0025fltxmfDisplay.NumberOfNoiseLevels = 1024
data0025fltxmfDisplay.ImpulseNoiseProbability = 1.0
data0025fltxmfDisplay.ImpulseNoiseBackgroundValue = 0.0
data0025fltxmfDisplay.NoiseGeneratorSeed = 1
data0025fltxmfDisplay.CompositeStrategy = 'AUTO'
data0025fltxmfDisplay.UseLICForLOD = 0
data0025fltxmfDisplay.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
data0025fltxmfDisplay.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0025fltxmfDisplay.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
data0025fltxmfDisplay.GlyphType.TipResolution = 6
data0025fltxmfDisplay.GlyphType.TipRadius = 0.1
data0025fltxmfDisplay.GlyphType.TipLength = 0.35
data0025fltxmfDisplay.GlyphType.ShaftResolution = 6
data0025fltxmfDisplay.GlyphType.ShaftRadius = 0.03
data0025fltxmfDisplay.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
data0025fltxmfDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0025fltxmfDisplay.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
data0025fltxmfDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
data0025fltxmfDisplay.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
data0025fltxmfDisplay.DataAxesGrid.XTitle = 'X Axis'
data0025fltxmfDisplay.DataAxesGrid.YTitle = 'Y Axis'
data0025fltxmfDisplay.DataAxesGrid.ZTitle = 'Z Axis'
data0025fltxmfDisplay.DataAxesGrid.XTitleFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.XTitleFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.XTitleBold = 0
data0025fltxmfDisplay.DataAxesGrid.XTitleItalic = 0
data0025fltxmfDisplay.DataAxesGrid.XTitleFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.XTitleShadow = 0
data0025fltxmfDisplay.DataAxesGrid.XTitleOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.YTitleFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.YTitleFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.YTitleBold = 0
data0025fltxmfDisplay.DataAxesGrid.YTitleItalic = 0
data0025fltxmfDisplay.DataAxesGrid.YTitleFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.YTitleShadow = 0
data0025fltxmfDisplay.DataAxesGrid.YTitleOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.ZTitleFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.ZTitleFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.ZTitleBold = 0
data0025fltxmfDisplay.DataAxesGrid.ZTitleItalic = 0
data0025fltxmfDisplay.DataAxesGrid.ZTitleFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.ZTitleShadow = 0
data0025fltxmfDisplay.DataAxesGrid.ZTitleOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.FacesToRender = 63
data0025fltxmfDisplay.DataAxesGrid.CullBackface = 0
data0025fltxmfDisplay.DataAxesGrid.CullFrontface = 1
data0025fltxmfDisplay.DataAxesGrid.ShowGrid = 0
data0025fltxmfDisplay.DataAxesGrid.ShowEdges = 1
data0025fltxmfDisplay.DataAxesGrid.ShowTicks = 1
data0025fltxmfDisplay.DataAxesGrid.LabelUniqueEdgesOnly = 1
data0025fltxmfDisplay.DataAxesGrid.AxesToLabel = 63
data0025fltxmfDisplay.DataAxesGrid.XLabelFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.XLabelFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.XLabelBold = 0
data0025fltxmfDisplay.DataAxesGrid.XLabelItalic = 0
data0025fltxmfDisplay.DataAxesGrid.XLabelFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.XLabelShadow = 0
data0025fltxmfDisplay.DataAxesGrid.XLabelOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.YLabelFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.YLabelFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.YLabelBold = 0
data0025fltxmfDisplay.DataAxesGrid.YLabelItalic = 0
data0025fltxmfDisplay.DataAxesGrid.YLabelFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.YLabelShadow = 0
data0025fltxmfDisplay.DataAxesGrid.YLabelOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.ZLabelFontFamily = 'Arial'
data0025fltxmfDisplay.DataAxesGrid.ZLabelFontFile = ''
data0025fltxmfDisplay.DataAxesGrid.ZLabelBold = 0
data0025fltxmfDisplay.DataAxesGrid.ZLabelItalic = 0
data0025fltxmfDisplay.DataAxesGrid.ZLabelFontSize = 12
data0025fltxmfDisplay.DataAxesGrid.ZLabelShadow = 0
data0025fltxmfDisplay.DataAxesGrid.ZLabelOpacity = 1.0
data0025fltxmfDisplay.DataAxesGrid.XAxisNotation = 'Mixed'
data0025fltxmfDisplay.DataAxesGrid.XAxisPrecision = 2
data0025fltxmfDisplay.DataAxesGrid.XAxisUseCustomLabels = 0
data0025fltxmfDisplay.DataAxesGrid.XAxisLabels = []
data0025fltxmfDisplay.DataAxesGrid.YAxisNotation = 'Mixed'
data0025fltxmfDisplay.DataAxesGrid.YAxisPrecision = 2
data0025fltxmfDisplay.DataAxesGrid.YAxisUseCustomLabels = 0
data0025fltxmfDisplay.DataAxesGrid.YAxisLabels = []
data0025fltxmfDisplay.DataAxesGrid.ZAxisNotation = 'Mixed'
data0025fltxmfDisplay.DataAxesGrid.ZAxisPrecision = 2
data0025fltxmfDisplay.DataAxesGrid.ZAxisUseCustomLabels = 0
data0025fltxmfDisplay.DataAxesGrid.ZAxisLabels = []
data0025fltxmfDisplay.DataAxesGrid.UseCustomBounds = 0
data0025fltxmfDisplay.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
data0025fltxmfDisplay.PolarAxes.Visibility = 0
data0025fltxmfDisplay.PolarAxes.Translation = [0.0, 0.0, 0.0]
data0025fltxmfDisplay.PolarAxes.Scale = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.Orientation = [0.0, 0.0, 0.0]
data0025fltxmfDisplay.PolarAxes.EnableCustomBounds = [0, 0, 0]
data0025fltxmfDisplay.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
data0025fltxmfDisplay.PolarAxes.EnableCustomRange = 0
data0025fltxmfDisplay.PolarAxes.CustomRange = [0.0, 1.0]
data0025fltxmfDisplay.PolarAxes.PolarAxisVisibility = 1
data0025fltxmfDisplay.PolarAxes.RadialAxesVisibility = 1
data0025fltxmfDisplay.PolarAxes.DrawRadialGridlines = 1
data0025fltxmfDisplay.PolarAxes.PolarArcsVisibility = 1
data0025fltxmfDisplay.PolarAxes.DrawPolarArcsGridlines = 1
data0025fltxmfDisplay.PolarAxes.NumberOfRadialAxes = 0
data0025fltxmfDisplay.PolarAxes.AutoSubdividePolarAxis = 1
data0025fltxmfDisplay.PolarAxes.NumberOfPolarAxis = 0
data0025fltxmfDisplay.PolarAxes.MinimumRadius = 0.0
data0025fltxmfDisplay.PolarAxes.MinimumAngle = 0.0
data0025fltxmfDisplay.PolarAxes.MaximumAngle = 90.0
data0025fltxmfDisplay.PolarAxes.RadialAxesOriginToPolarAxis = 1
data0025fltxmfDisplay.PolarAxes.Ratio = 1.0
data0025fltxmfDisplay.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleVisibility = 1
data0025fltxmfDisplay.PolarAxes.PolarAxisTitle = 'Radial Distance'
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleLocation = 'Bottom'
data0025fltxmfDisplay.PolarAxes.PolarLabelVisibility = 1
data0025fltxmfDisplay.PolarAxes.PolarLabelFormat = '%-#6.3g'
data0025fltxmfDisplay.PolarAxes.PolarLabelExponentLocation = 'Labels'
data0025fltxmfDisplay.PolarAxes.RadialLabelVisibility = 1
data0025fltxmfDisplay.PolarAxes.RadialLabelFormat = '%-#3.1f'
data0025fltxmfDisplay.PolarAxes.RadialLabelLocation = 'Bottom'
data0025fltxmfDisplay.PolarAxes.RadialUnitsVisibility = 1
data0025fltxmfDisplay.PolarAxes.ScreenSize = 10.0
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleOpacity = 1.0
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleBold = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleItalic = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleShadow = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisTitleFontSize = 12
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelOpacity = 1.0
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelBold = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelItalic = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelShadow = 0
data0025fltxmfDisplay.PolarAxes.PolarAxisLabelFontSize = 12
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextOpacity = 1.0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextBold = 0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextItalic = 0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextShadow = 0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTextFontSize = 12
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextBold = 0
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextItalic = 0
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextShadow = 0
data0025fltxmfDisplay.PolarAxes.SecondaryRadialAxesTextFontSize = 12
data0025fltxmfDisplay.PolarAxes.EnableDistanceLOD = 1
data0025fltxmfDisplay.PolarAxes.DistanceLODThreshold = 0.7
data0025fltxmfDisplay.PolarAxes.EnableViewAngleLOD = 1
data0025fltxmfDisplay.PolarAxes.ViewAngleLODThreshold = 0.7
data0025fltxmfDisplay.PolarAxes.SmallestVisiblePolarAngle = 0.5
data0025fltxmfDisplay.PolarAxes.PolarTicksVisibility = 1
data0025fltxmfDisplay.PolarAxes.ArcTicksOriginToPolarAxis = 1
data0025fltxmfDisplay.PolarAxes.TickLocation = 'Both'
data0025fltxmfDisplay.PolarAxes.AxisTickVisibility = 1
data0025fltxmfDisplay.PolarAxes.AxisMinorTickVisibility = 0
data0025fltxmfDisplay.PolarAxes.ArcTickVisibility = 1
data0025fltxmfDisplay.PolarAxes.ArcMinorTickVisibility = 0
data0025fltxmfDisplay.PolarAxes.DeltaAngleMajor = 10.0
data0025fltxmfDisplay.PolarAxes.DeltaAngleMinor = 5.0
data0025fltxmfDisplay.PolarAxes.PolarAxisMajorTickSize = 0.0
data0025fltxmfDisplay.PolarAxes.PolarAxisTickRatioSize = 0.3
data0025fltxmfDisplay.PolarAxes.PolarAxisMajorTickThickness = 1.0
data0025fltxmfDisplay.PolarAxes.PolarAxisTickRatioThickness = 0.5
data0025fltxmfDisplay.PolarAxes.LastRadialAxisMajorTickSize = 0.0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTickRatioSize = 0.3
data0025fltxmfDisplay.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
data0025fltxmfDisplay.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
data0025fltxmfDisplay.PolarAxes.ArcMajorTickSize = 0.0
data0025fltxmfDisplay.PolarAxes.ArcTickRatioSize = 0.3
data0025fltxmfDisplay.PolarAxes.ArcMajorTickThickness = 1.0
data0025fltxmfDisplay.PolarAxes.ArcTickRatioThickness = 0.5
data0025fltxmfDisplay.PolarAxes.Use2DMode = 0
data0025fltxmfDisplay.PolarAxes.UseLogAxis = 0

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=data0025fltxmf)
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
calculator1.ResultArrayName = 'Twind'
calculator1.Function = 'temperature/(1.+delTbyTwind)'

# show data in view
calculator1Display = Show(calculator1, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Selection = None
calculator1Display.Representation = 'Outline'
calculator1Display.ColorArrayName = ['CELLS', '']
calculator1Display.LookupTable = None
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
calculator1Display.ScaleFactor = 60.3514892578125
calculator1Display.SelectScaleArray = 'Twind'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.UseGlyphTable = 0
calculator1Display.GlyphTableIndexArray = 'Twind'
calculator1Display.UseCompositeGlyphTable = 0
calculator1Display.UseGlyphCullingAndLOD = 0
calculator1Display.LODValues = []
calculator1Display.ColorByLODIndex = 0
calculator1Display.GaussianRadius = 3.017574462890625
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
calculator1Display.ScalarOpacityFunction = None
calculator1Display.ScalarOpacityUnitDistance = 1.3584736846424879
calculator1Display.SelectMapper = 'Projected tetra'
calculator1Display.SamplingDimensions = [128, 128, 128]
calculator1Display.SelectInputVectors = [None, '']
calculator1Display.NumberOfSteps = 40
calculator1Display.StepSize = 0.25
calculator1Display.NormalizeVectors = 1
calculator1Display.EnhancedLIC = 1
calculator1Display.ColorMode = 'Blend'
calculator1Display.LICIntensity = 0.8
calculator1Display.MapModeBias = 0.0
calculator1Display.EnhanceContrast = 'Off'
calculator1Display.LowLICContrastEnhancementFactor = 0.0
calculator1Display.HighLICContrastEnhancementFactor = 0.0
calculator1Display.LowColorContrastEnhancementFactor = 0.0
calculator1Display.HighColorContrastEnhancementFactor = 0.0
calculator1Display.AntiAlias = 0
calculator1Display.MaskOnSurface = 1
calculator1Display.MaskThreshold = 0.0
calculator1Display.MaskIntensity = 0.0
calculator1Display.MaskColor = [0.5, 0.5, 0.5]
calculator1Display.GenerateNoiseTexture = 0
calculator1Display.NoiseType = 'Gaussian'
calculator1Display.NoiseTextureSize = 128
calculator1Display.NoiseGrainSize = 2
calculator1Display.MinNoiseValue = 0.0
calculator1Display.MaxNoiseValue = 0.8
calculator1Display.NumberOfNoiseLevels = 1024
calculator1Display.ImpulseNoiseProbability = 1.0
calculator1Display.ImpulseNoiseBackgroundValue = 0.0
calculator1Display.NoiseGeneratorSeed = 1
calculator1Display.CompositeStrategy = 'AUTO'
calculator1Display.UseLICForLOD = 0
calculator1Display.WriteLog = ''

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
Hide(data0025fltxmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=calculator1)
threshold1.Scalars = ['CELLS', 'Twind']
threshold1.LowerThreshold = 127599.4663748503
threshold1.UpperThreshold = 1068908.2460241134
threshold1.ThresholdMethod = 'Between'
threshold1.AllScalars = 1
threshold1.UseContinuousCellRange = 0
threshold1.Invert = 0

# Properties modified on threshold1
threshold1.UpperThreshold = 90000.0
threshold1.ThresholdMethod = 'Above Upper Threshold'

# show data in view
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')

# get 2D transfer function for 'Twind'
twindTF2D = GetTransferFunction2D('Twind')
twindTF2D.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
twindTF2D.Boxes = []
twindTF2D.ScalarRangeInitialized = 0
twindTF2D.Range = [0.0, 1.0, 0.0, 1.0]
twindTF2D.OutputDimensions = [10, 10]

# get color transfer function/color map for 'Twind'
twindLUT = GetColorTransferFunction('Twind')
twindLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
twindLUT.InterpretValuesAsCategories = 0
twindLUT.AnnotationsInitialized = 0
twindLUT.ShowCategoricalColorsinDataRangeOnly = 0
twindLUT.RescaleOnVisibilityChange = 0
twindLUT.EnableOpacityMapping = 0
twindLUT.TransferFunction2D = twindTF2D
twindLUT.Use2DTransferFunction = 0
twindLUT.RGBPoints = [127599.4663748503, 0.231373, 0.298039, 0.752941, 598253.8561994819, 0.865003, 0.865003, 0.865003, 1068908.2460241134, 0.705882, 0.0156863, 0.14902]
twindLUT.UseLogScale = 0
twindLUT.UseOpacityControlPointsFreehandDrawing = 0
twindLUT.ShowDataHistogram = 0
twindLUT.AutomaticDataHistogramComputation = 0
twindLUT.DataHistogramNumberOfBins = 10
twindLUT.ColorSpace = 'Diverging'
twindLUT.UseBelowRangeColor = 0
twindLUT.BelowRangeColor = [0.0, 0.0, 0.0]
twindLUT.UseAboveRangeColor = 0
twindLUT.AboveRangeColor = [0.5, 0.5, 0.5]
twindLUT.NanColor = [1.0, 1.0, 0.0]
twindLUT.NanOpacity = 1.0
twindLUT.Discretize = 1
twindLUT.NumberOfTableValues = 256
twindLUT.ScalarRangeInitialized = 1.0
twindLUT.HSVWrap = 0
twindLUT.VectorComponent = 0
twindLUT.VectorMode = 'Magnitude'
twindLUT.AllowDuplicateScalars = 1
twindLUT.Annotations = []
twindLUT.ActiveAnnotatedValues = []
twindLUT.IndexedColors = []
twindLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'Twind'
twindPWF = GetOpacityTransferFunction('Twind')
twindPWF.Points = [127599.4663748503, 0.0, 0.5, 0.0, 1068908.2460241134, 1.0, 0.5, 0.0]
twindPWF.AllowDuplicateScalars = 1
twindPWF.UseLogScale = 0
twindPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
threshold1Display.Selection = None
threshold1Display.Representation = 'Surface'
threshold1Display.ColorArrayName = ['CELLS', 'Twind']
threshold1Display.LookupTable = twindLUT
threshold1Display.MapScalars = 1
threshold1Display.MultiComponentsMapping = 0
threshold1Display.InterpolateScalarsBeforeMapping = 1
threshold1Display.Opacity = 1.0
threshold1Display.PointSize = 2.0
threshold1Display.LineWidth = 1.0
threshold1Display.RenderLinesAsTubes = 0
threshold1Display.RenderPointsAsSpheres = 0
threshold1Display.Interpolation = 'Gouraud'
threshold1Display.Specular = 0.0
threshold1Display.SpecularColor = [1.0, 1.0, 1.0]
threshold1Display.SpecularPower = 100.0
threshold1Display.Luminosity = 0.0
threshold1Display.Ambient = 0.0
threshold1Display.Diffuse = 1.0
threshold1Display.Roughness = 0.3
threshold1Display.Metallic = 0.0
threshold1Display.EdgeTint = [1.0, 1.0, 1.0]
threshold1Display.Anisotropy = 0.0
threshold1Display.AnisotropyRotation = 0.0
threshold1Display.BaseIOR = 1.5
threshold1Display.CoatStrength = 0.0
threshold1Display.CoatIOR = 2.0
threshold1Display.CoatRoughness = 0.0
threshold1Display.CoatColor = [1.0, 1.0, 1.0]
threshold1Display.SelectTCoordArray = 'None'
threshold1Display.SelectNormalArray = 'None'
threshold1Display.SelectTangentArray = 'None'
threshold1Display.Texture = None
threshold1Display.RepeatTextures = 1
threshold1Display.InterpolateTextures = 0
threshold1Display.SeamlessU = 0
threshold1Display.SeamlessV = 0
threshold1Display.UseMipmapTextures = 0
threshold1Display.ShowTexturesOnBackface = 1
threshold1Display.BaseColorTexture = None
threshold1Display.NormalTexture = None
threshold1Display.NormalScale = 1.0
threshold1Display.CoatNormalTexture = None
threshold1Display.CoatNormalScale = 1.0
threshold1Display.MaterialTexture = None
threshold1Display.OcclusionStrength = 1.0
threshold1Display.AnisotropyTexture = None
threshold1Display.EmissiveTexture = None
threshold1Display.EmissiveFactor = [1.0, 1.0, 1.0]
threshold1Display.FlipTextures = 0
threshold1Display.BackfaceRepresentation = 'Follow Frontface'
threshold1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
threshold1Display.BackfaceOpacity = 1.0
threshold1Display.Position = [0.0, 0.0, 0.0]
threshold1Display.Scale = [1.0, 1.0, 1.0]
threshold1Display.Orientation = [0.0, 0.0, 0.0]
threshold1Display.Origin = [0.0, 0.0, 0.0]
threshold1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
threshold1Display.Pickable = 1
threshold1Display.Triangulate = 0
threshold1Display.UseShaderReplacements = 0
threshold1Display.ShaderReplacements = ''
threshold1Display.NonlinearSubdivisionLevel = 1
threshold1Display.UseDataPartitions = 0
threshold1Display.OSPRayUseScaleArray = 'All Approximate'
threshold1Display.OSPRayScaleArray = ''
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.OSPRayMaterial = 'None'
threshold1Display.BlockSelectors = ['/']
threshold1Display.BlockColors = []
threshold1Display.BlockOpacities = []
threshold1Display.Orient = 0
threshold1Display.OrientationMode = 'Direction'
threshold1Display.SelectOrientationVectors = 'None'
threshold1Display.Scaling = 0
threshold1Display.ScaleMode = 'No Data Scaling Off'
threshold1Display.ScaleFactor = 60.3514892578125
threshold1Display.SelectScaleArray = 'Twind'
threshold1Display.GlyphType = 'Arrow'
threshold1Display.UseGlyphTable = 0
threshold1Display.GlyphTableIndexArray = 'Twind'
threshold1Display.UseCompositeGlyphTable = 0
threshold1Display.UseGlyphCullingAndLOD = 0
threshold1Display.LODValues = []
threshold1Display.ColorByLODIndex = 0
threshold1Display.GaussianRadius = 3.017574462890625
threshold1Display.ShaderPreset = 'Sphere'
threshold1Display.CustomTriangleScale = 3
threshold1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
threshold1Display.Emissive = 0
threshold1Display.ScaleByArray = 0
threshold1Display.SetScaleArray = [None, '']
threshold1Display.ScaleArrayComponent = 0
threshold1Display.UseScaleFunction = 1
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityByArray = 0
threshold1Display.OpacityArray = [None, '']
threshold1Display.OpacityArrayComponent = 0
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1Display.SelectionCellLabelBold = 0
threshold1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
threshold1Display.SelectionCellLabelFontFamily = 'Arial'
threshold1Display.SelectionCellLabelFontFile = ''
threshold1Display.SelectionCellLabelFontSize = 18
threshold1Display.SelectionCellLabelItalic = 0
threshold1Display.SelectionCellLabelJustification = 'Left'
threshold1Display.SelectionCellLabelOpacity = 1.0
threshold1Display.SelectionCellLabelShadow = 0
threshold1Display.SelectionPointLabelBold = 0
threshold1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
threshold1Display.SelectionPointLabelFontFamily = 'Arial'
threshold1Display.SelectionPointLabelFontFile = ''
threshold1Display.SelectionPointLabelFontSize = 18
threshold1Display.SelectionPointLabelItalic = 0
threshold1Display.SelectionPointLabelJustification = 'Left'
threshold1Display.SelectionPointLabelOpacity = 1.0
threshold1Display.SelectionPointLabelShadow = 0
threshold1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1Display.ScalarOpacityFunction = twindPWF
threshold1Display.ScalarOpacityUnitDistance = 1.3584736846424879
threshold1Display.UseSeparateOpacityArray = 0
threshold1Display.OpacityArrayName = ['CELLS', 'Twind']
threshold1Display.OpacityComponent = ''
threshold1Display.SelectMapper = 'Projected tetra'
threshold1Display.SamplingDimensions = [128, 128, 128]
threshold1Display.UseFloatingPointFrameBuffer = 1
threshold1Display.SelectInputVectors = [None, '']
threshold1Display.NumberOfSteps = 40
threshold1Display.StepSize = 0.25
threshold1Display.NormalizeVectors = 1
threshold1Display.EnhancedLIC = 1
threshold1Display.ColorMode = 'Blend'
threshold1Display.LICIntensity = 0.8
threshold1Display.MapModeBias = 0.0
threshold1Display.EnhanceContrast = 'Off'
threshold1Display.LowLICContrastEnhancementFactor = 0.0
threshold1Display.HighLICContrastEnhancementFactor = 0.0
threshold1Display.LowColorContrastEnhancementFactor = 0.0
threshold1Display.HighColorContrastEnhancementFactor = 0.0
threshold1Display.AntiAlias = 0
threshold1Display.MaskOnSurface = 1
threshold1Display.MaskThreshold = 0.0
threshold1Display.MaskIntensity = 0.0
threshold1Display.MaskColor = [0.5, 0.5, 0.5]
threshold1Display.GenerateNoiseTexture = 0
threshold1Display.NoiseType = 'Gaussian'
threshold1Display.NoiseTextureSize = 128
threshold1Display.NoiseGrainSize = 2
threshold1Display.MinNoiseValue = 0.0
threshold1Display.MaxNoiseValue = 0.8
threshold1Display.NumberOfNoiseLevels = 1024
threshold1Display.ImpulseNoiseProbability = 1.0
threshold1Display.ImpulseNoiseBackgroundValue = 0.0
threshold1Display.NoiseGeneratorSeed = 1
threshold1Display.CompositeStrategy = 'AUTO'
threshold1Display.UseLICForLOD = 0
threshold1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
threshold1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
threshold1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
threshold1Display.GlyphType.TipResolution = 6
threshold1Display.GlyphType.TipRadius = 0.1
threshold1Display.GlyphType.TipLength = 0.35
threshold1Display.GlyphType.ShaftResolution = 6
threshold1Display.GlyphType.ShaftRadius = 0.03
threshold1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
threshold1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
threshold1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
threshold1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
threshold1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
threshold1Display.DataAxesGrid.XTitle = 'X Axis'
threshold1Display.DataAxesGrid.YTitle = 'Y Axis'
threshold1Display.DataAxesGrid.ZTitle = 'Z Axis'
threshold1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
threshold1Display.DataAxesGrid.XTitleFontFile = ''
threshold1Display.DataAxesGrid.XTitleBold = 0
threshold1Display.DataAxesGrid.XTitleItalic = 0
threshold1Display.DataAxesGrid.XTitleFontSize = 12
threshold1Display.DataAxesGrid.XTitleShadow = 0
threshold1Display.DataAxesGrid.XTitleOpacity = 1.0
threshold1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
threshold1Display.DataAxesGrid.YTitleFontFile = ''
threshold1Display.DataAxesGrid.YTitleBold = 0
threshold1Display.DataAxesGrid.YTitleItalic = 0
threshold1Display.DataAxesGrid.YTitleFontSize = 12
threshold1Display.DataAxesGrid.YTitleShadow = 0
threshold1Display.DataAxesGrid.YTitleOpacity = 1.0
threshold1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
threshold1Display.DataAxesGrid.ZTitleFontFile = ''
threshold1Display.DataAxesGrid.ZTitleBold = 0
threshold1Display.DataAxesGrid.ZTitleItalic = 0
threshold1Display.DataAxesGrid.ZTitleFontSize = 12
threshold1Display.DataAxesGrid.ZTitleShadow = 0
threshold1Display.DataAxesGrid.ZTitleOpacity = 1.0
threshold1Display.DataAxesGrid.FacesToRender = 63
threshold1Display.DataAxesGrid.CullBackface = 0
threshold1Display.DataAxesGrid.CullFrontface = 1
threshold1Display.DataAxesGrid.ShowGrid = 0
threshold1Display.DataAxesGrid.ShowEdges = 1
threshold1Display.DataAxesGrid.ShowTicks = 1
threshold1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
threshold1Display.DataAxesGrid.AxesToLabel = 63
threshold1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
threshold1Display.DataAxesGrid.XLabelFontFile = ''
threshold1Display.DataAxesGrid.XLabelBold = 0
threshold1Display.DataAxesGrid.XLabelItalic = 0
threshold1Display.DataAxesGrid.XLabelFontSize = 12
threshold1Display.DataAxesGrid.XLabelShadow = 0
threshold1Display.DataAxesGrid.XLabelOpacity = 1.0
threshold1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
threshold1Display.DataAxesGrid.YLabelFontFile = ''
threshold1Display.DataAxesGrid.YLabelBold = 0
threshold1Display.DataAxesGrid.YLabelItalic = 0
threshold1Display.DataAxesGrid.YLabelFontSize = 12
threshold1Display.DataAxesGrid.YLabelShadow = 0
threshold1Display.DataAxesGrid.YLabelOpacity = 1.0
threshold1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
threshold1Display.DataAxesGrid.ZLabelFontFile = ''
threshold1Display.DataAxesGrid.ZLabelBold = 0
threshold1Display.DataAxesGrid.ZLabelItalic = 0
threshold1Display.DataAxesGrid.ZLabelFontSize = 12
threshold1Display.DataAxesGrid.ZLabelShadow = 0
threshold1Display.DataAxesGrid.ZLabelOpacity = 1.0
threshold1Display.DataAxesGrid.XAxisNotation = 'Mixed'
threshold1Display.DataAxesGrid.XAxisPrecision = 2
threshold1Display.DataAxesGrid.XAxisUseCustomLabels = 0
threshold1Display.DataAxesGrid.XAxisLabels = []
threshold1Display.DataAxesGrid.YAxisNotation = 'Mixed'
threshold1Display.DataAxesGrid.YAxisPrecision = 2
threshold1Display.DataAxesGrid.YAxisUseCustomLabels = 0
threshold1Display.DataAxesGrid.YAxisLabels = []
threshold1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
threshold1Display.DataAxesGrid.ZAxisPrecision = 2
threshold1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
threshold1Display.DataAxesGrid.ZAxisLabels = []
threshold1Display.DataAxesGrid.UseCustomBounds = 0
threshold1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
threshold1Display.PolarAxes.Visibility = 0
threshold1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
threshold1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
threshold1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
threshold1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
threshold1Display.PolarAxes.EnableCustomRange = 0
threshold1Display.PolarAxes.CustomRange = [0.0, 1.0]
threshold1Display.PolarAxes.PolarAxisVisibility = 1
threshold1Display.PolarAxes.RadialAxesVisibility = 1
threshold1Display.PolarAxes.DrawRadialGridlines = 1
threshold1Display.PolarAxes.PolarArcsVisibility = 1
threshold1Display.PolarAxes.DrawPolarArcsGridlines = 1
threshold1Display.PolarAxes.NumberOfRadialAxes = 0
threshold1Display.PolarAxes.AutoSubdividePolarAxis = 1
threshold1Display.PolarAxes.NumberOfPolarAxis = 0
threshold1Display.PolarAxes.MinimumRadius = 0.0
threshold1Display.PolarAxes.MinimumAngle = 0.0
threshold1Display.PolarAxes.MaximumAngle = 90.0
threshold1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
threshold1Display.PolarAxes.Ratio = 1.0
threshold1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
threshold1Display.PolarAxes.PolarAxisTitleVisibility = 1
threshold1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
threshold1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
threshold1Display.PolarAxes.PolarLabelVisibility = 1
threshold1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
threshold1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
threshold1Display.PolarAxes.RadialLabelVisibility = 1
threshold1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
threshold1Display.PolarAxes.RadialLabelLocation = 'Bottom'
threshold1Display.PolarAxes.RadialUnitsVisibility = 1
threshold1Display.PolarAxes.ScreenSize = 10.0
threshold1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
threshold1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
threshold1Display.PolarAxes.PolarAxisTitleFontFile = ''
threshold1Display.PolarAxes.PolarAxisTitleBold = 0
threshold1Display.PolarAxes.PolarAxisTitleItalic = 0
threshold1Display.PolarAxes.PolarAxisTitleShadow = 0
threshold1Display.PolarAxes.PolarAxisTitleFontSize = 12
threshold1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
threshold1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
threshold1Display.PolarAxes.PolarAxisLabelFontFile = ''
threshold1Display.PolarAxes.PolarAxisLabelBold = 0
threshold1Display.PolarAxes.PolarAxisLabelItalic = 0
threshold1Display.PolarAxes.PolarAxisLabelShadow = 0
threshold1Display.PolarAxes.PolarAxisLabelFontSize = 12
threshold1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
threshold1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
threshold1Display.PolarAxes.LastRadialAxisTextFontFile = ''
threshold1Display.PolarAxes.LastRadialAxisTextBold = 0
threshold1Display.PolarAxes.LastRadialAxisTextItalic = 0
threshold1Display.PolarAxes.LastRadialAxisTextShadow = 0
threshold1Display.PolarAxes.LastRadialAxisTextFontSize = 12
threshold1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
threshold1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
threshold1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
threshold1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
threshold1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
threshold1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
threshold1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
threshold1Display.PolarAxes.EnableDistanceLOD = 1
threshold1Display.PolarAxes.DistanceLODThreshold = 0.7
threshold1Display.PolarAxes.EnableViewAngleLOD = 1
threshold1Display.PolarAxes.ViewAngleLODThreshold = 0.7
threshold1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
threshold1Display.PolarAxes.PolarTicksVisibility = 1
threshold1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
threshold1Display.PolarAxes.TickLocation = 'Both'
threshold1Display.PolarAxes.AxisTickVisibility = 1
threshold1Display.PolarAxes.AxisMinorTickVisibility = 0
threshold1Display.PolarAxes.ArcTickVisibility = 1
threshold1Display.PolarAxes.ArcMinorTickVisibility = 0
threshold1Display.PolarAxes.DeltaAngleMajor = 10.0
threshold1Display.PolarAxes.DeltaAngleMinor = 5.0
threshold1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
threshold1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
threshold1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
threshold1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
threshold1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
threshold1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
threshold1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
threshold1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
threshold1Display.PolarAxes.ArcMajorTickSize = 0.0
threshold1Display.PolarAxes.ArcTickRatioSize = 0.3
threshold1Display.PolarAxes.ArcMajorTickThickness = 1.0
threshold1Display.PolarAxes.ArcTickRatioThickness = 0.5
threshold1Display.PolarAxes.Use2DMode = 0
threshold1Display.PolarAxes.UseLogAxis = 0

# show color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# turn off scalar coloring
ColorBy(threshold1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(twindLUT, renderView1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# change representation type
threshold1Display.SetRepresentationType('Outline')
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# hide data in view
Hide(threshold1, renderView1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# hide data in view
Hide(calculator1, renderView1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [454.9541320800781, 0.0, 1291.8025382533183]
renderView1.CameraFocalPoint = [454.9541320800781, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 334.3431329804907

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(registrationName='ProgrammableFilter1', Input=threshold1)
programmableFilter1.OutputDataSetType = 'Same as Input'
programmableFilter1.Script = ''
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.CopyArrays = 0
programmableFilter1.PythonPath = ''

# Properties modified on programmableFilter1
programmableFilter1.Script = """import numpy as np
import subprocess as sp
from scipy.interpolate import interp1d

mp = 1.67262e-24
kB = 1.3806542e-16
mu = 0.60917
X = 0.7154
gamma = 5./3
Myr = 1.0e+06 * 365*24*60*60

mach = 1.496
Tcl = 4.0e+04
chi = 100

tcool_mix_B_tcc = [0.08, 0.10, 0.20, 0.50, 0.80, 1.00, 1.40, 2.50, 8.00,]
rini_B_rcl = [28.268, 35.335, 70.671, 176.677, 282.684, 353.355, 494.697, 883.387, 2826.838,]

select = 1
vanilla = False

root = "/freya/ptmp/mpa/adutt/CCinCC85/cc85"
cooltable = np.loadtxt(f"{root}/cooltable.dat")
directory = f"{root}/output{\'-vanl\' if vanilla else \'\'}-c{chi:d},m{mach:.3f},T4e4,t{tcool_mix_B_tcc[select]:.2f},r{rini_B_rcl[select]:.3f}"

UNIT_LENGTH = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_LENGTH").split()[-1])
UNIT_DENSITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_DENSITY").split()[-1])
UNIT_VELOCITY = float(sp.getoutput(f"cat {directory}/definitions.h | grep UNIT_VELOCITY").split()[-1])
distance_ini = float(sp.getoutput(f"cat {directory}/pluto.ini | grep RINI").split()[-1])

LAMBDA = interp1d(cooltable[:,0],
                  cooltable[:,1],
                  fill_value="extrapolate")

input0 = inputs[0]"""
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.CopyArrays = 1
programmableFilter1.PythonPath = ''

# show data in view
programmableFilter1Display = Show(programmableFilter1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
programmableFilter1Display.Selection = None
programmableFilter1Display.Representation = 'Surface'
programmableFilter1Display.ColorArrayName = ['CELLS', 'Twind']
programmableFilter1Display.LookupTable = twindLUT
programmableFilter1Display.MapScalars = 1
programmableFilter1Display.MultiComponentsMapping = 0
programmableFilter1Display.InterpolateScalarsBeforeMapping = 1
programmableFilter1Display.Opacity = 1.0
programmableFilter1Display.PointSize = 2.0
programmableFilter1Display.LineWidth = 1.0
programmableFilter1Display.RenderLinesAsTubes = 0
programmableFilter1Display.RenderPointsAsSpheres = 0
programmableFilter1Display.Interpolation = 'Gouraud'
programmableFilter1Display.Specular = 0.0
programmableFilter1Display.SpecularColor = [1.0, 1.0, 1.0]
programmableFilter1Display.SpecularPower = 100.0
programmableFilter1Display.Luminosity = 0.0
programmableFilter1Display.Ambient = 0.0
programmableFilter1Display.Diffuse = 1.0
programmableFilter1Display.Roughness = 0.3
programmableFilter1Display.Metallic = 0.0
programmableFilter1Display.EdgeTint = [1.0, 1.0, 1.0]
programmableFilter1Display.Anisotropy = 0.0
programmableFilter1Display.AnisotropyRotation = 0.0
programmableFilter1Display.BaseIOR = 1.5
programmableFilter1Display.CoatStrength = 0.0
programmableFilter1Display.CoatIOR = 2.0
programmableFilter1Display.CoatRoughness = 0.0
programmableFilter1Display.CoatColor = [1.0, 1.0, 1.0]
programmableFilter1Display.SelectTCoordArray = 'None'
programmableFilter1Display.SelectNormalArray = 'None'
programmableFilter1Display.SelectTangentArray = 'None'
programmableFilter1Display.Texture = None
programmableFilter1Display.RepeatTextures = 1
programmableFilter1Display.InterpolateTextures = 0
programmableFilter1Display.SeamlessU = 0
programmableFilter1Display.SeamlessV = 0
programmableFilter1Display.UseMipmapTextures = 0
programmableFilter1Display.ShowTexturesOnBackface = 1
programmableFilter1Display.BaseColorTexture = None
programmableFilter1Display.NormalTexture = None
programmableFilter1Display.NormalScale = 1.0
programmableFilter1Display.CoatNormalTexture = None
programmableFilter1Display.CoatNormalScale = 1.0
programmableFilter1Display.MaterialTexture = None
programmableFilter1Display.OcclusionStrength = 1.0
programmableFilter1Display.AnisotropyTexture = None
programmableFilter1Display.EmissiveTexture = None
programmableFilter1Display.EmissiveFactor = [1.0, 1.0, 1.0]
programmableFilter1Display.FlipTextures = 0
programmableFilter1Display.BackfaceRepresentation = 'Follow Frontface'
programmableFilter1Display.BackfaceAmbientColor = [1.0, 1.0, 1.0]
programmableFilter1Display.BackfaceOpacity = 1.0
programmableFilter1Display.Position = [0.0, 0.0, 0.0]
programmableFilter1Display.Scale = [1.0, 1.0, 1.0]
programmableFilter1Display.Orientation = [0.0, 0.0, 0.0]
programmableFilter1Display.Origin = [0.0, 0.0, 0.0]
programmableFilter1Display.CoordinateShiftScaleMethod = 'Always Auto Shift Scale'
programmableFilter1Display.Pickable = 1
programmableFilter1Display.Triangulate = 0
programmableFilter1Display.UseShaderReplacements = 0
programmableFilter1Display.ShaderReplacements = ''
programmableFilter1Display.NonlinearSubdivisionLevel = 1
programmableFilter1Display.UseDataPartitions = 0
programmableFilter1Display.OSPRayUseScaleArray = 'All Approximate'
programmableFilter1Display.OSPRayScaleArray = ''
programmableFilter1Display.OSPRayScaleFunction = 'PiecewiseFunction'
programmableFilter1Display.OSPRayMaterial = 'None'
programmableFilter1Display.BlockSelectors = ['/']
programmableFilter1Display.BlockColors = []
programmableFilter1Display.BlockOpacities = []
programmableFilter1Display.Orient = 0
programmableFilter1Display.OrientationMode = 'Direction'
programmableFilter1Display.SelectOrientationVectors = 'None'
programmableFilter1Display.Scaling = 0
programmableFilter1Display.ScaleMode = 'No Data Scaling Off'
programmableFilter1Display.ScaleFactor = 60.3514892578125
programmableFilter1Display.SelectScaleArray = 'Twind'
programmableFilter1Display.GlyphType = 'Arrow'
programmableFilter1Display.UseGlyphTable = 0
programmableFilter1Display.GlyphTableIndexArray = 'Twind'
programmableFilter1Display.UseCompositeGlyphTable = 0
programmableFilter1Display.UseGlyphCullingAndLOD = 0
programmableFilter1Display.LODValues = []
programmableFilter1Display.ColorByLODIndex = 0
programmableFilter1Display.GaussianRadius = 3.017574462890625
programmableFilter1Display.ShaderPreset = 'Sphere'
programmableFilter1Display.CustomTriangleScale = 3
programmableFilter1Display.CustomShader = """ // This custom shader code define a gaussian blur
 // Please take a look into vtkSMPointGaussianRepresentation.cxx
 // for other custom shader examples
 //VTK::Color::Impl
   float dist2 = dot(offsetVCVSOutput.xy,offsetVCVSOutput.xy);
   float gaussian = exp(-0.5*dist2);
   opacity = opacity*gaussian;
"""
programmableFilter1Display.Emissive = 0
programmableFilter1Display.ScaleByArray = 0
programmableFilter1Display.SetScaleArray = [None, '']
programmableFilter1Display.ScaleArrayComponent = 0
programmableFilter1Display.UseScaleFunction = 1
programmableFilter1Display.ScaleTransferFunction = 'PiecewiseFunction'
programmableFilter1Display.OpacityByArray = 0
programmableFilter1Display.OpacityArray = [None, '']
programmableFilter1Display.OpacityArrayComponent = 0
programmableFilter1Display.OpacityTransferFunction = 'PiecewiseFunction'
programmableFilter1Display.DataAxesGrid = 'GridAxesRepresentation'
programmableFilter1Display.SelectionCellLabelBold = 0
programmableFilter1Display.SelectionCellLabelColor = [0.0, 1.0, 0.0]
programmableFilter1Display.SelectionCellLabelFontFamily = 'Arial'
programmableFilter1Display.SelectionCellLabelFontFile = ''
programmableFilter1Display.SelectionCellLabelFontSize = 18
programmableFilter1Display.SelectionCellLabelItalic = 0
programmableFilter1Display.SelectionCellLabelJustification = 'Left'
programmableFilter1Display.SelectionCellLabelOpacity = 1.0
programmableFilter1Display.SelectionCellLabelShadow = 0
programmableFilter1Display.SelectionPointLabelBold = 0
programmableFilter1Display.SelectionPointLabelColor = [1.0, 1.0, 0.0]
programmableFilter1Display.SelectionPointLabelFontFamily = 'Arial'
programmableFilter1Display.SelectionPointLabelFontFile = ''
programmableFilter1Display.SelectionPointLabelFontSize = 18
programmableFilter1Display.SelectionPointLabelItalic = 0
programmableFilter1Display.SelectionPointLabelJustification = 'Left'
programmableFilter1Display.SelectionPointLabelOpacity = 1.0
programmableFilter1Display.SelectionPointLabelShadow = 0
programmableFilter1Display.PolarAxes = 'PolarAxesRepresentation'
programmableFilter1Display.ScalarOpacityFunction = twindPWF
programmableFilter1Display.ScalarOpacityUnitDistance = 1.3584736846424879
programmableFilter1Display.UseSeparateOpacityArray = 0
programmableFilter1Display.OpacityArrayName = ['CELLS', 'Twind']
programmableFilter1Display.OpacityComponent = ''
programmableFilter1Display.SelectMapper = 'Projected tetra'
programmableFilter1Display.SamplingDimensions = [128, 128, 128]
programmableFilter1Display.UseFloatingPointFrameBuffer = 1
programmableFilter1Display.SelectInputVectors = [None, '']
programmableFilter1Display.NumberOfSteps = 40
programmableFilter1Display.StepSize = 0.25
programmableFilter1Display.NormalizeVectors = 1
programmableFilter1Display.EnhancedLIC = 1
programmableFilter1Display.ColorMode = 'Blend'
programmableFilter1Display.LICIntensity = 0.8
programmableFilter1Display.MapModeBias = 0.0
programmableFilter1Display.EnhanceContrast = 'Off'
programmableFilter1Display.LowLICContrastEnhancementFactor = 0.0
programmableFilter1Display.HighLICContrastEnhancementFactor = 0.0
programmableFilter1Display.LowColorContrastEnhancementFactor = 0.0
programmableFilter1Display.HighColorContrastEnhancementFactor = 0.0
programmableFilter1Display.AntiAlias = 0
programmableFilter1Display.MaskOnSurface = 1
programmableFilter1Display.MaskThreshold = 0.0
programmableFilter1Display.MaskIntensity = 0.0
programmableFilter1Display.MaskColor = [0.5, 0.5, 0.5]
programmableFilter1Display.GenerateNoiseTexture = 0
programmableFilter1Display.NoiseType = 'Gaussian'
programmableFilter1Display.NoiseTextureSize = 128
programmableFilter1Display.NoiseGrainSize = 2
programmableFilter1Display.MinNoiseValue = 0.0
programmableFilter1Display.MaxNoiseValue = 0.8
programmableFilter1Display.NumberOfNoiseLevels = 1024
programmableFilter1Display.ImpulseNoiseProbability = 1.0
programmableFilter1Display.ImpulseNoiseBackgroundValue = 0.0
programmableFilter1Display.NoiseGeneratorSeed = 1
programmableFilter1Display.CompositeStrategy = 'AUTO'
programmableFilter1Display.UseLICForLOD = 0
programmableFilter1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
programmableFilter1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
programmableFilter1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
programmableFilter1Display.GlyphType.TipResolution = 6
programmableFilter1Display.GlyphType.TipRadius = 0.1
programmableFilter1Display.GlyphType.TipLength = 0.35
programmableFilter1Display.GlyphType.ShaftResolution = 6
programmableFilter1Display.GlyphType.ShaftRadius = 0.03
programmableFilter1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
programmableFilter1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
programmableFilter1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
programmableFilter1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
programmableFilter1Display.OpacityTransferFunction.UseLogScale = 0

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
programmableFilter1Display.DataAxesGrid.XTitle = 'X Axis'
programmableFilter1Display.DataAxesGrid.YTitle = 'Y Axis'
programmableFilter1Display.DataAxesGrid.ZTitle = 'Z Axis'
programmableFilter1Display.DataAxesGrid.XTitleFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.XTitleFontFile = ''
programmableFilter1Display.DataAxesGrid.XTitleBold = 0
programmableFilter1Display.DataAxesGrid.XTitleItalic = 0
programmableFilter1Display.DataAxesGrid.XTitleFontSize = 12
programmableFilter1Display.DataAxesGrid.XTitleShadow = 0
programmableFilter1Display.DataAxesGrid.XTitleOpacity = 1.0
programmableFilter1Display.DataAxesGrid.YTitleFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.YTitleFontFile = ''
programmableFilter1Display.DataAxesGrid.YTitleBold = 0
programmableFilter1Display.DataAxesGrid.YTitleItalic = 0
programmableFilter1Display.DataAxesGrid.YTitleFontSize = 12
programmableFilter1Display.DataAxesGrid.YTitleShadow = 0
programmableFilter1Display.DataAxesGrid.YTitleOpacity = 1.0
programmableFilter1Display.DataAxesGrid.ZTitleFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.ZTitleFontFile = ''
programmableFilter1Display.DataAxesGrid.ZTitleBold = 0
programmableFilter1Display.DataAxesGrid.ZTitleItalic = 0
programmableFilter1Display.DataAxesGrid.ZTitleFontSize = 12
programmableFilter1Display.DataAxesGrid.ZTitleShadow = 0
programmableFilter1Display.DataAxesGrid.ZTitleOpacity = 1.0
programmableFilter1Display.DataAxesGrid.FacesToRender = 63
programmableFilter1Display.DataAxesGrid.CullBackface = 0
programmableFilter1Display.DataAxesGrid.CullFrontface = 1
programmableFilter1Display.DataAxesGrid.ShowGrid = 0
programmableFilter1Display.DataAxesGrid.ShowEdges = 1
programmableFilter1Display.DataAxesGrid.ShowTicks = 1
programmableFilter1Display.DataAxesGrid.LabelUniqueEdgesOnly = 1
programmableFilter1Display.DataAxesGrid.AxesToLabel = 63
programmableFilter1Display.DataAxesGrid.XLabelFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.XLabelFontFile = ''
programmableFilter1Display.DataAxesGrid.XLabelBold = 0
programmableFilter1Display.DataAxesGrid.XLabelItalic = 0
programmableFilter1Display.DataAxesGrid.XLabelFontSize = 12
programmableFilter1Display.DataAxesGrid.XLabelShadow = 0
programmableFilter1Display.DataAxesGrid.XLabelOpacity = 1.0
programmableFilter1Display.DataAxesGrid.YLabelFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.YLabelFontFile = ''
programmableFilter1Display.DataAxesGrid.YLabelBold = 0
programmableFilter1Display.DataAxesGrid.YLabelItalic = 0
programmableFilter1Display.DataAxesGrid.YLabelFontSize = 12
programmableFilter1Display.DataAxesGrid.YLabelShadow = 0
programmableFilter1Display.DataAxesGrid.YLabelOpacity = 1.0
programmableFilter1Display.DataAxesGrid.ZLabelFontFamily = 'Arial'
programmableFilter1Display.DataAxesGrid.ZLabelFontFile = ''
programmableFilter1Display.DataAxesGrid.ZLabelBold = 0
programmableFilter1Display.DataAxesGrid.ZLabelItalic = 0
programmableFilter1Display.DataAxesGrid.ZLabelFontSize = 12
programmableFilter1Display.DataAxesGrid.ZLabelShadow = 0
programmableFilter1Display.DataAxesGrid.ZLabelOpacity = 1.0
programmableFilter1Display.DataAxesGrid.XAxisNotation = 'Mixed'
programmableFilter1Display.DataAxesGrid.XAxisPrecision = 2
programmableFilter1Display.DataAxesGrid.XAxisUseCustomLabels = 0
programmableFilter1Display.DataAxesGrid.XAxisLabels = []
programmableFilter1Display.DataAxesGrid.YAxisNotation = 'Mixed'
programmableFilter1Display.DataAxesGrid.YAxisPrecision = 2
programmableFilter1Display.DataAxesGrid.YAxisUseCustomLabels = 0
programmableFilter1Display.DataAxesGrid.YAxisLabels = []
programmableFilter1Display.DataAxesGrid.ZAxisNotation = 'Mixed'
programmableFilter1Display.DataAxesGrid.ZAxisPrecision = 2
programmableFilter1Display.DataAxesGrid.ZAxisUseCustomLabels = 0
programmableFilter1Display.DataAxesGrid.ZAxisLabels = []
programmableFilter1Display.DataAxesGrid.UseCustomBounds = 0
programmableFilter1Display.DataAxesGrid.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
programmableFilter1Display.PolarAxes.Visibility = 0
programmableFilter1Display.PolarAxes.Translation = [0.0, 0.0, 0.0]
programmableFilter1Display.PolarAxes.Scale = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.Orientation = [0.0, 0.0, 0.0]
programmableFilter1Display.PolarAxes.EnableCustomBounds = [0, 0, 0]
programmableFilter1Display.PolarAxes.CustomBounds = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
programmableFilter1Display.PolarAxes.EnableCustomRange = 0
programmableFilter1Display.PolarAxes.CustomRange = [0.0, 1.0]
programmableFilter1Display.PolarAxes.PolarAxisVisibility = 1
programmableFilter1Display.PolarAxes.RadialAxesVisibility = 1
programmableFilter1Display.PolarAxes.DrawRadialGridlines = 1
programmableFilter1Display.PolarAxes.PolarArcsVisibility = 1
programmableFilter1Display.PolarAxes.DrawPolarArcsGridlines = 1
programmableFilter1Display.PolarAxes.NumberOfRadialAxes = 0
programmableFilter1Display.PolarAxes.AutoSubdividePolarAxis = 1
programmableFilter1Display.PolarAxes.NumberOfPolarAxis = 0
programmableFilter1Display.PolarAxes.MinimumRadius = 0.0
programmableFilter1Display.PolarAxes.MinimumAngle = 0.0
programmableFilter1Display.PolarAxes.MaximumAngle = 90.0
programmableFilter1Display.PolarAxes.RadialAxesOriginToPolarAxis = 1
programmableFilter1Display.PolarAxes.Ratio = 1.0
programmableFilter1Display.PolarAxes.PolarAxisColor = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.PolarArcsColor = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.LastRadialAxisColor = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.SecondaryPolarArcsColor = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.SecondaryRadialAxesColor = [1.0, 1.0, 1.0]
programmableFilter1Display.PolarAxes.PolarAxisTitleVisibility = 1
programmableFilter1Display.PolarAxes.PolarAxisTitle = 'Radial Distance'
programmableFilter1Display.PolarAxes.PolarAxisTitleLocation = 'Bottom'
programmableFilter1Display.PolarAxes.PolarLabelVisibility = 1
programmableFilter1Display.PolarAxes.PolarLabelFormat = '%-#6.3g'
programmableFilter1Display.PolarAxes.PolarLabelExponentLocation = 'Labels'
programmableFilter1Display.PolarAxes.RadialLabelVisibility = 1
programmableFilter1Display.PolarAxes.RadialLabelFormat = '%-#3.1f'
programmableFilter1Display.PolarAxes.RadialLabelLocation = 'Bottom'
programmableFilter1Display.PolarAxes.RadialUnitsVisibility = 1
programmableFilter1Display.PolarAxes.ScreenSize = 10.0
programmableFilter1Display.PolarAxes.PolarAxisTitleOpacity = 1.0
programmableFilter1Display.PolarAxes.PolarAxisTitleFontFamily = 'Arial'
programmableFilter1Display.PolarAxes.PolarAxisTitleFontFile = ''
programmableFilter1Display.PolarAxes.PolarAxisTitleBold = 0
programmableFilter1Display.PolarAxes.PolarAxisTitleItalic = 0
programmableFilter1Display.PolarAxes.PolarAxisTitleShadow = 0
programmableFilter1Display.PolarAxes.PolarAxisTitleFontSize = 12
programmableFilter1Display.PolarAxes.PolarAxisLabelOpacity = 1.0
programmableFilter1Display.PolarAxes.PolarAxisLabelFontFamily = 'Arial'
programmableFilter1Display.PolarAxes.PolarAxisLabelFontFile = ''
programmableFilter1Display.PolarAxes.PolarAxisLabelBold = 0
programmableFilter1Display.PolarAxes.PolarAxisLabelItalic = 0
programmableFilter1Display.PolarAxes.PolarAxisLabelShadow = 0
programmableFilter1Display.PolarAxes.PolarAxisLabelFontSize = 12
programmableFilter1Display.PolarAxes.LastRadialAxisTextOpacity = 1.0
programmableFilter1Display.PolarAxes.LastRadialAxisTextFontFamily = 'Arial'
programmableFilter1Display.PolarAxes.LastRadialAxisTextFontFile = ''
programmableFilter1Display.PolarAxes.LastRadialAxisTextBold = 0
programmableFilter1Display.PolarAxes.LastRadialAxisTextItalic = 0
programmableFilter1Display.PolarAxes.LastRadialAxisTextShadow = 0
programmableFilter1Display.PolarAxes.LastRadialAxisTextFontSize = 12
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextOpacity = 1.0
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextFontFamily = 'Arial'
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextBold = 0
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextItalic = 0
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextShadow = 0
programmableFilter1Display.PolarAxes.SecondaryRadialAxesTextFontSize = 12
programmableFilter1Display.PolarAxes.EnableDistanceLOD = 1
programmableFilter1Display.PolarAxes.DistanceLODThreshold = 0.7
programmableFilter1Display.PolarAxes.EnableViewAngleLOD = 1
programmableFilter1Display.PolarAxes.ViewAngleLODThreshold = 0.7
programmableFilter1Display.PolarAxes.SmallestVisiblePolarAngle = 0.5
programmableFilter1Display.PolarAxes.PolarTicksVisibility = 1
programmableFilter1Display.PolarAxes.ArcTicksOriginToPolarAxis = 1
programmableFilter1Display.PolarAxes.TickLocation = 'Both'
programmableFilter1Display.PolarAxes.AxisTickVisibility = 1
programmableFilter1Display.PolarAxes.AxisMinorTickVisibility = 0
programmableFilter1Display.PolarAxes.ArcTickVisibility = 1
programmableFilter1Display.PolarAxes.ArcMinorTickVisibility = 0
programmableFilter1Display.PolarAxes.DeltaAngleMajor = 10.0
programmableFilter1Display.PolarAxes.DeltaAngleMinor = 5.0
programmableFilter1Display.PolarAxes.PolarAxisMajorTickSize = 0.0
programmableFilter1Display.PolarAxes.PolarAxisTickRatioSize = 0.3
programmableFilter1Display.PolarAxes.PolarAxisMajorTickThickness = 1.0
programmableFilter1Display.PolarAxes.PolarAxisTickRatioThickness = 0.5
programmableFilter1Display.PolarAxes.LastRadialAxisMajorTickSize = 0.0
programmableFilter1Display.PolarAxes.LastRadialAxisTickRatioSize = 0.3
programmableFilter1Display.PolarAxes.LastRadialAxisMajorTickThickness = 1.0
programmableFilter1Display.PolarAxes.LastRadialAxisTickRatioThickness = 0.5
programmableFilter1Display.PolarAxes.ArcMajorTickSize = 0.0
programmableFilter1Display.PolarAxes.ArcTickRatioSize = 0.3
programmableFilter1Display.PolarAxes.ArcMajorTickThickness = 1.0
programmableFilter1Display.PolarAxes.ArcTickRatioThickness = 0.5
programmableFilter1Display.PolarAxes.Use2DMode = 0
programmableFilter1Display.PolarAxes.UseLogAxis = 0

# reset view to fit data
renderView1.ResetCamera(False)

# hide data in view
Hide(threshold1, renderView1)

# show color bar/color legend
programmableFilter1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# turn off scalar coloring
ColorBy(programmableFilter1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(twindLUT, renderView1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# change representation type
programmableFilter1Display.SetRepresentationType('Outline')
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=programmableFilter1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.UseDual = 0
slice1.Crinkleslice = 0
slice1.Triangulatetheslice = 1
slice1.Mergeduplicatedpointsintheslice = 1
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [458.75457763671875, 0.0, -0.00012969970703125]
slice1.SliceType.Normal = [1.0, 0.0, 0.0]
slice1.SliceType.Offset = 0.0

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [458.75457763671875, 0.0, -0.00012969970703125]
slice1.HyperTreeGridSlicer.Normal = [1.0, 0.0, 0.0]
slice1.HyperTreeGridSlicer.Offset = 0.0
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [458.75457763671875, 0.0, 0.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Selection = None
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['CELLS', 'Twind']
slice1Display.LookupTable = twindLUT
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
slice1Display.ScaleFactor = 60.19299468994141
slice1Display.SelectScaleArray = 'Twind'
slice1Display.GlyphType = 'Arrow'
slice1Display.UseGlyphTable = 0
slice1Display.GlyphTableIndexArray = 'Twind'
slice1Display.UseCompositeGlyphTable = 0
slice1Display.UseGlyphCullingAndLOD = 0
slice1Display.LODValues = []
slice1Display.ColorByLODIndex = 0
slice1Display.GaussianRadius = 3.0096497344970703
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
slice1Display.SelectInputVectors = [None, '']
slice1Display.NumberOfSteps = 40
slice1Display.StepSize = 0.25
slice1Display.NormalizeVectors = 1
slice1Display.EnhancedLIC = 1
slice1Display.ColorMode = 'Blend'
slice1Display.LICIntensity = 0.8
slice1Display.MapModeBias = 0.0
slice1Display.EnhanceContrast = 'Off'
slice1Display.LowLICContrastEnhancementFactor = 0.0
slice1Display.HighLICContrastEnhancementFactor = 0.0
slice1Display.LowColorContrastEnhancementFactor = 0.0
slice1Display.HighColorContrastEnhancementFactor = 0.0
slice1Display.AntiAlias = 0
slice1Display.MaskOnSurface = 1
slice1Display.MaskThreshold = 0.0
slice1Display.MaskIntensity = 0.0
slice1Display.MaskColor = [0.5, 0.5, 0.5]
slice1Display.GenerateNoiseTexture = 0
slice1Display.NoiseType = 'Gaussian'
slice1Display.NoiseTextureSize = 128
slice1Display.NoiseGrainSize = 2
slice1Display.MinNoiseValue = 0.0
slice1Display.MaxNoiseValue = 0.8
slice1Display.NumberOfNoiseLevels = 1024
slice1Display.ImpulseNoiseProbability = 1.0
slice1Display.ImpulseNoiseBackgroundValue = 0.0
slice1Display.NoiseGeneratorSeed = 1
slice1Display.CompositeStrategy = 'AUTO'
slice1Display.UseLICForLOD = 0
slice1Display.WriteLog = ''

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
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(calculator1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# create a new 'Annotate Time Filter'
annotateTimeFilter1 = AnnotateTimeFilter(registrationName='AnnotateTimeFilter1', Input=calculator1)
annotateTimeFilter1.Format = 'Time: {time:f}'
annotateTimeFilter1.Shift = 0.0
annotateTimeFilter1.Scale = 1.0

# Properties modified on annotateTimeFilter1
annotateTimeFilter1.Format = 'Time: {time:.1f} $t_{{\\rm cc, ini}}$'
annotateTimeFilter1.Scale = 0.1

# show data in view
annotateTimeFilter1Display = Show(annotateTimeFilter1, renderView1, 'TextSourceRepresentation')

# trace defaults for the display properties.
annotateTimeFilter1Display.TextPropMode = '2D Text Widget'
annotateTimeFilter1Display.Interactivity = 1
annotateTimeFilter1Display.WindowLocation = 'Upper Left Corner'
annotateTimeFilter1Display.Position = [0.05, 0.05]
annotateTimeFilter1Display.Opacity = 1.0
annotateTimeFilter1Display.FontFamily = 'Arial'
annotateTimeFilter1Display.FontFile = ''
annotateTimeFilter1Display.Bold = 0
annotateTimeFilter1Display.Italic = 0
annotateTimeFilter1Display.Shadow = 0
annotateTimeFilter1Display.FontSize = 18
annotateTimeFilter1Display.Justification = 'Center'
annotateTimeFilter1Display.VerticalJustification = 'Center'
annotateTimeFilter1Display.ShowBorder = 'Only on hover'
annotateTimeFilter1Display.BackgroundColor = [1.0, 1.0, 1.0, 0.2]
annotateTimeFilter1Display.BorderThickness = 0.0
annotateTimeFilter1Display.CornerRadius = 0.0
annotateTimeFilter1Display.Padding = 1
annotateTimeFilter1Display.LineSpacing = 1.0
annotateTimeFilter1Display.CellOffset = 0
annotateTimeFilter1Display.InteriorLinesWidth = 1
annotateTimeFilter1Display.InteriorLinesColor = [0.0, 0.0, 0.0]
annotateTimeFilter1Display.InteriorLinesVisibility = 0
annotateTimeFilter1Display.BasePosition = [0.0, 0.0, 0.0]
annotateTimeFilter1Display.TopPosition = [0.0, 1.0, 0.0]
annotateTimeFilter1Display.FlagSize = 1.0
annotateTimeFilter1Display.BillboardPosition = [0.0, 0.0, 0.0]
annotateTimeFilter1Display.DisplayOffset = [0, 0]

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.WindowLocation = 'Any Location'
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.Position = [0.31953125000000004, 0.9566666666666667]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.Position = [0.31953125000000004, 0.92]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.FontSize = 3
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.FontSize = 34
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(calculator1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# create a new 'Annotate Time Filter'
annotateTimeFilter2 = AnnotateTimeFilter(registrationName='AnnotateTimeFilter2', Input=calculator1)
annotateTimeFilter2.Format = 'Time: {time:f}'
annotateTimeFilter2.Shift = 0.0
annotateTimeFilter2.Scale = 1.0
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2
annotateTimeFilter2.Format = '$ \\ \\approx $ {time:.1f} Myr'
annotateTimeFilter2.Scale = 0.00659429395

# show data in view
annotateTimeFilter2Display = Show(annotateTimeFilter2, renderView1, 'TextSourceRepresentation')

# trace defaults for the display properties.
annotateTimeFilter2Display.TextPropMode = '2D Text Widget'
annotateTimeFilter2Display.Interactivity = 1
annotateTimeFilter2Display.WindowLocation = 'Upper Left Corner'
annotateTimeFilter2Display.Position = [0.05, 0.05]
annotateTimeFilter2Display.Opacity = 1.0
annotateTimeFilter2Display.FontFamily = 'Arial'
annotateTimeFilter2Display.FontFile = ''
annotateTimeFilter2Display.Bold = 0
annotateTimeFilter2Display.Italic = 0
annotateTimeFilter2Display.Shadow = 0
annotateTimeFilter2Display.FontSize = 18
annotateTimeFilter2Display.Justification = 'Center'
annotateTimeFilter2Display.VerticalJustification = 'Center'
annotateTimeFilter2Display.ShowBorder = 'Only on hover'
annotateTimeFilter2Display.BackgroundColor = [1.0, 1.0, 1.0, 0.2]
annotateTimeFilter2Display.BorderThickness = 0.0
annotateTimeFilter2Display.CornerRadius = 0.0
annotateTimeFilter2Display.Padding = 1
annotateTimeFilter2Display.LineSpacing = 1.0
annotateTimeFilter2Display.CellOffset = 0
annotateTimeFilter2Display.InteriorLinesWidth = 1
annotateTimeFilter2Display.InteriorLinesColor = [0.0, 0.0, 0.0]
annotateTimeFilter2Display.InteriorLinesVisibility = 0
annotateTimeFilter2Display.BasePosition = [0.0, 0.0, 0.0]
annotateTimeFilter2Display.TopPosition = [0.0, 1.0, 0.0]
annotateTimeFilter2Display.FlagSize = 1.0
annotateTimeFilter2Display.BillboardPosition = [0.0, 0.0, 0.0]
annotateTimeFilter2Display.DisplayOffset = [0, 0]

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2Display
annotateTimeFilter2Display.WindowLocation = 'Any Location'
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2Display
annotateTimeFilter2Display.Position = [0.5423437500000002, 0.9580555555555555]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2Display
annotateTimeFilter2Display.Position = [0.5423437500000002, 0.92]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2Display
annotateTimeFilter2Display.FontSize = 3
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on annotateTimeFilter2Display
annotateTimeFilter2Display.FontSize = 34
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(data0025fltxmf)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# create a new 'Ruler'
ruler1 = Ruler(registrationName='Ruler1')
ruler1.Point1 = [-0.5, 0.0, 0.0]
ruler1.Point2 = [0.5, 0.0, 0.0]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler1
ruler1.Point1 = [550.0, 24.0, 0.0]
ruler1.Point2 = [570.0, 24.0, 0.0]

# show data in view
ruler1Display = Show(ruler1, renderView1, 'RulerSourceRepresentation')

# trace defaults for the display properties.
ruler1Display.Visibility = 1
ruler1Display.LabelFormat = '%6.3g'
ruler1Display.Scale = 1.0
ruler1Display.RulerMode = 0
ruler1Display.NumberOfTicks = 5
ruler1Display.Graduation = 1.0
ruler1Display.AxisColor = [0.0, 1.0, 0.0]
ruler1Display.AxisLineWidth = 2.0
ruler1Display.Opacity = 1.0
ruler1Display.FontFamily = 'Arial'
ruler1Display.FontFile = ''
ruler1Display.Bold = 0
ruler1Display.Italic = 0
ruler1Display.Shadow = 0
ruler1Display.FontSize = 18
ruler1Display.Justification = 'Left'

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler1Display
ruler1Display.LabelFormat = '%6.3g pc'
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler1Display
ruler1Display.Scale = 3.0
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler1Display
ruler1Display.NumberOfTicks = 2
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=ruler1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(data0025fltxmf)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# create a new 'Ruler'
ruler2 = Ruler(registrationName='Ruler2')
ruler2.Point1 = [-0.5, 0.0, 0.0]
ruler2.Point2 = [0.5, 0.0, 0.0]
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=ruler2)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler2
ruler2.Point1 = [550.0, 40.0, 0.0]
ruler2.Point2 = [560.0, 40.0, 0.0]

# show data in view
ruler2Display = Show(ruler2, renderView1, 'RulerSourceRepresentation')

# trace defaults for the display properties.
ruler2Display.Visibility = 1
ruler2Display.LabelFormat = '%6.3g'
ruler2Display.Scale = 1.0
ruler2Display.RulerMode = 0
ruler2Display.NumberOfTicks = 5
ruler2Display.Graduation = 1.0
ruler2Display.AxisColor = [0.0, 1.0, 0.0]
ruler2Display.AxisLineWidth = 2.0
ruler2Display.Opacity = 1.0
ruler2Display.FontFamily = 'Arial'
ruler2Display.FontFile = ''
ruler2Display.Bold = 0
ruler2Display.Italic = 0
ruler2Display.Shadow = 0
ruler2Display.FontSize = 18
ruler2Display.Justification = 'Left'

# update the view to ensure updated data information
renderView1.Update()
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler2Display
ruler2Display.LabelFormat = '%6.3g $R_{\\rm cl}$'
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler2Display
ruler2Display.RulerMode = 1
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Properties modified on ruler2Display
ruler2Display.Graduation = 20.0
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(calculator1)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=slice1.SliceType)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set scalar coloring
ColorBy(slice1Display, ('CELLS', 'temperature'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(twindLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get 2D transfer function for 'temperature'
temperatureTF2D = GetTransferFunction2D('temperature')
temperatureTF2D.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
temperatureTF2D.Boxes = []
temperatureTF2D.ScalarRangeInitialized = 0
temperatureTF2D.Range = [0.0, 1.0, 0.0, 1.0]
temperatureTF2D.OutputDimensions = [10, 10]

# get color transfer function/color map for 'temperature'
temperatureLUT = GetColorTransferFunction('temperature')
temperatureLUT.AutomaticRescaleRangeMode = "Grow and update on 'Apply'"
temperatureLUT.InterpretValuesAsCategories = 0
temperatureLUT.AnnotationsInitialized = 0
temperatureLUT.ShowCategoricalColorsinDataRangeOnly = 0
temperatureLUT.RescaleOnVisibilityChange = 0
temperatureLUT.EnableOpacityMapping = 0
temperatureLUT.TransferFunction2D = temperatureTF2D
temperatureLUT.Use2DTransferFunction = 0
temperatureLUT.RGBPoints = [35690.703125, 0.231373, 0.298039, 0.752941, 773160.8515625, 0.865003, 0.865003, 0.865003, 1510631.0, 0.705882, 0.0156863, 0.14902]
temperatureLUT.UseLogScale = 0
temperatureLUT.UseOpacityControlPointsFreehandDrawing = 0
temperatureLUT.ShowDataHistogram = 0
temperatureLUT.AutomaticDataHistogramComputation = 0
temperatureLUT.DataHistogramNumberOfBins = 10
temperatureLUT.ColorSpace = 'Diverging'
temperatureLUT.UseBelowRangeColor = 0
temperatureLUT.BelowRangeColor = [0.0, 0.0, 0.0]
temperatureLUT.UseAboveRangeColor = 0
temperatureLUT.AboveRangeColor = [0.5, 0.5, 0.5]
temperatureLUT.NanColor = [1.0, 1.0, 0.0]
temperatureLUT.NanOpacity = 1.0
temperatureLUT.Discretize = 1
temperatureLUT.NumberOfTableValues = 256
temperatureLUT.ScalarRangeInitialized = 1.0
temperatureLUT.HSVWrap = 0
temperatureLUT.VectorComponent = 0
temperatureLUT.VectorMode = 'Magnitude'
temperatureLUT.AllowDuplicateScalars = 1
temperatureLUT.Annotations = []
temperatureLUT.ActiveAnnotatedValues = []
temperatureLUT.IndexedColors = []
temperatureLUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'temperature'
temperaturePWF = GetOpacityTransferFunction('temperature')
temperaturePWF.Points = [35690.703125, 0.0, 0.5, 0.0, 1510631.0, 1.0, 0.5, 0.0]
temperaturePWF.AllowDuplicateScalars = 1
temperaturePWF.UseLogScale = 0
temperaturePWF.ScalarRangeInitialized = 1
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Rescale transfer function
temperatureLUT.RescaleTransferFunction(31000.0, 4700000.0)

# Rescale transfer function
temperaturePWF.RescaleTransferFunction(31000.0, 4700000.0)

# Rescale 2D transfer function
temperatureTF2D.RescaleTransferFunction(31000.0, 4700000.0, 0.0, 1.0)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# convert to log space
temperatureLUT.MapControlPointsToLogSpace()

# Properties modified on temperatureLUT
temperatureLUT.UseLogScale = 1
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
temperatureLUT.ApplyPreset('Black-Body Radiation', True)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# get color legend/bar for temperatureLUT in view renderView1
temperatureLUTColorBar = GetScalarBar(temperatureLUT, renderView1)
temperatureLUTColorBar.AutoOrient = 1
temperatureLUTColorBar.Orientation = 'Vertical'
temperatureLUTColorBar.WindowLocation = 'Lower Right Corner'
temperatureLUTColorBar.Position = [0.89, 0.02]
temperatureLUTColorBar.Title = 'temperature'
temperatureLUTColorBar.ComponentTitle = ''
temperatureLUTColorBar.TitleJustification = 'Centered'
temperatureLUTColorBar.HorizontalTitle = 0
temperatureLUTColorBar.TitleOpacity = 1.0
temperatureLUTColorBar.TitleFontFamily = 'Arial'
temperatureLUTColorBar.TitleFontFile = ''
temperatureLUTColorBar.TitleBold = 0
temperatureLUTColorBar.TitleItalic = 0
temperatureLUTColorBar.TitleShadow = 0
temperatureLUTColorBar.TitleFontSize = 16
temperatureLUTColorBar.LabelOpacity = 1.0
temperatureLUTColorBar.LabelFontFamily = 'Arial'
temperatureLUTColorBar.LabelFontFile = ''
temperatureLUTColorBar.LabelBold = 0
temperatureLUTColorBar.LabelItalic = 0
temperatureLUTColorBar.LabelShadow = 0
temperatureLUTColorBar.LabelFontSize = 16
temperatureLUTColorBar.ScalarBarThickness = 16
temperatureLUTColorBar.ScalarBarLength = 0.33
temperatureLUTColorBar.DrawBackground = 0
temperatureLUTColorBar.BackgroundColor = [1.0, 1.0, 1.0, 0.5]
temperatureLUTColorBar.BackgroundPadding = 2.0
temperatureLUTColorBar.DrawScalarBarOutline = 0
temperatureLUTColorBar.ScalarBarOutlineColor = [1.0, 1.0, 1.0]
temperatureLUTColorBar.ScalarBarOutlineThickness = 1
temperatureLUTColorBar.AutomaticLabelFormat = 1
temperatureLUTColorBar.LabelFormat = '%-#6.3g'
temperatureLUTColorBar.DrawTickMarks = 1
temperatureLUTColorBar.DrawTickLabels = 1
temperatureLUTColorBar.UseCustomLabels = 0
temperatureLUTColorBar.CustomLabels = []
temperatureLUTColorBar.AddRangeLabels = 1
temperatureLUTColorBar.RangeLabelFormat = '%-#6.1e'
temperatureLUTColorBar.DrawDataRange = 0
temperatureLUTColorBar.DataRangeLabelFormat = '%-#6.1e'
temperatureLUTColorBar.DrawAnnotations = 1
temperatureLUTColorBar.AddRangeAnnotations = 0
temperatureLUTColorBar.AutomaticAnnotations = 0
temperatureLUTColorBar.DrawNanAnnotation = 0
temperatureLUTColorBar.NanAnnotation = 'NaN'
temperatureLUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
temperatureLUTColorBar.ReverseLegend = 0

# Properties modified on temperatureLUTColorBar
temperatureLUTColorBar.Title = 'Temperature (K)'
temperatureLUTColorBar.TitleFontSize = 22
temperatureLUTColorBar.LabelFontSize = 20
temperatureLUTColorBar.DrawScalarBarOutline = 1
temperatureLUTColorBar.AutomaticLabelFormat = 0
temperatureLUTColorBar.LabelFormat = '%-#6.1e'
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# set active source
SetActiveSource(threshold1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)
# Adjust camera
source = GetActiveSource()
bounds = source.GetDataInformation().GetBounds()

bounds_dx = bounds[1] - bounds[0]
bounds_dy = bounds[3] - bounds[2]
bounds_dz = bounds[5] - bounds[4]
bounds_cx = (bounds[0] + bounds[1])/2.0
bounds_cy = (bounds[2] + bounds[3])/2.0
bounds_cz = (bounds[4] + bounds[5])/2.0

far  = 1
near = 0
pos = max(bounds_dx, bounds_dy)
camUp = [0.0, 1.0, 0.0]
camPos = [bounds_cx, bounds_cy,  pos*far]
camFoc = [bounds_cx, bounds_cy, -pos*near]

# current camera placement for renderView1
renderView1.CameraPosition = camPos # [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = camFoc # [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera
'''
# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
'''
# change scalar bar placement
temperatureLUTColorBar.Orientation = 'Horizontal'
temperatureLUTColorBar.WindowLocation = 'Any Location'
temperatureLUTColorBar.Position = [0.1603320312499999, 0.11055555555555571]
temperatureLUTColorBar.ScalarBarLength = 0.3300000000000002
# Adjust camera
'''
# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
'''
# change scalar bar placement
temperatureLUTColorBar.ScalarBarLength = 0.7839062499999983
# Adjust camera
'''
# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraParallelScale = 337.7343818397026

# reset view to fit data
renderView1.ResetCamera(True)
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
'''
# change scalar bar placement
temperatureLUTColorBar.Position = [0.15876953124999987, 0.08000000000000017]
# Adjust camera
'''
# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
'''
# layout/tab size in pixels
layout1.SetSize(1280, 720)
'''
# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
'''
renderView1.CameraPosition = camPos # [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = camFoc # [458.75457763671875, 0.0, -0.00012969970703125]

# save screenshot
SaveScreenshot('/freya/ptmp/mpa/adutt/CCinCC85/cc85/output-c100,m1.496,T4e4,t0.20,r70.671/vis/temperature.%04d.png'%file_no, layout1, ImageResolution=[1280, 720],
    FontScaling='Scale fonts proportionally',
    OverrideColorPalette='',
    StereoMode='No change',
    TransparentBackground=0, 
    # PNG options
    CompressionLevel='0',
    MetaData=['Application', 'ParaView'])
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026
# Adjust camera

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1280, 720)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [458.75457763671875, 0.0, 1304.905317679263]
renderView1.CameraFocalPoint = [458.75457763671875, 0.0, -0.00012969970703125]
renderView1.CameraViewAngle = 17.682291666666668
renderView1.CameraParallelScale = 337.7343818397026

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
