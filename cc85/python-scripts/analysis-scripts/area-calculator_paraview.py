import sys
# state file generated using paraview version 5.11.2
import paraview

if len(sys.argv)!=4:
    print("Wrong usage!")
    sys.exit(1)

paraview.compatibility.major = 5
paraview.compatibility.minor = 11

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
renderView1.ViewSize = [2154, 911]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [176.6770477294922, 0.0, -3.063678741455078e-05]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [178.76016333320737, 0.5182680976143551, 5.325553576269024]
renderView1.CameraFocalPoint = [176.6770477294922, 6.241770410960253e-16, -3.0636787412747814e-05]
renderView1.CameraViewUp = [-0.037459350555676695, 0.995906175613681, -0.08226594939875892]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 1.7982078392464544
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

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
layout1.SplitVertical(0, 0.876738)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, spreadSheetView2)
layout1.SetSize(2154, 1312)

# ----------------------------------------------------------------
# restore active view
SetActiveView(spreadSheetView2)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

output_dir = sys.argv[1]
file_no = int(sys.argv[2])
label = sys.argv[3]

print(f'Working on: {output_dir}/data.{file_no:04d}.flt.xmf')

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
cutoff_T_wind8e4.UpperThreshold = 80000.0
cutoff_T_wind8e4.ThresholdMethod = 'Above Upper Threshold'

# create a new 'Threshold'
cloud_material = Threshold(registrationName='cloud_material', Input=cutoff_T_wind8e4)
cloud_material.Scalars = ['CELLS', 'temperature']
cloud_material.LowerThreshold = 80000.0
cloud_material.UpperThreshold = 80000.0
cloud_material.ThresholdMethod = 'Below Lower Threshold'

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=cloud_material)

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=extractSurface1)
cellSize1.ComputeSum = 1

# create a new 'Integrate Variables'
integrateVariables_surface = IntegrateVariables(registrationName='IntegrateVariables_surface', Input=cellSize1)

# create a new 'Programmable Filter'
script = f"""
import os

dump_file = "./area-data_{label}.txt"
if os.path.exists(dump_file) and {file_no}==0:
  os.remove(dump_file)

mode = 'a' if os.path.isfile(dump_file) else 'w'
if mode == 'a':
    with open(dump_file, 'r') as txtfile:
        last_line = txtfile.readlines()[-1]
else:
    last_line = ''

data = inputs[0]
area = data.CellData.GetArray("Area")[0]

with open(dump_file, mode) as txtfile:
    if mode == 'w':
        txtfile.write(f"{label}\\n")
    to_write = f"{file_no} {{area:.3f}}\\n"
    if to_write != last_line:
        txtfile.write(to_write)
print("Done!")
"""
programmableFilter1 = ProgrammableFilter(registrationName='ProgrammableFilter1', Input=integrateVariables_surface)
programmableFilter1.Script = script
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.PythonPath = ''

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from cloud_material
cloud_materialDisplay = Show(cloud_material, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
cloud_materialDisplay.Representation = 'Outline'
cloud_materialDisplay.ColorArrayName = ['POINTS', '']
cloud_materialDisplay.SelectTCoordArray = 'None'
cloud_materialDisplay.SelectNormalArray = 'None'
cloud_materialDisplay.SelectTangentArray = 'None'
cloud_materialDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
cloud_materialDisplay.SelectOrientationVectors = 'None'
cloud_materialDisplay.ScaleFactor = 0.21132872104644776
cloud_materialDisplay.SelectScaleArray = 'Twind'
cloud_materialDisplay.GlyphType = 'Arrow'
cloud_materialDisplay.GlyphTableIndexArray = 'Twind'
cloud_materialDisplay.GaussianRadius = 0.010566436052322388
cloud_materialDisplay.SetScaleArray = [None, '']
cloud_materialDisplay.ScaleTransferFunction = 'PiecewiseFunction'
cloud_materialDisplay.OpacityArray = [None, '']
cloud_materialDisplay.OpacityTransferFunction = 'PiecewiseFunction'
cloud_materialDisplay.DataAxesGrid = 'GridAxesRepresentation'
cloud_materialDisplay.PolarAxes = 'PolarAxesRepresentation'
cloud_materialDisplay.ScalarOpacityUnitDistance = 0.27821804757204355
cloud_materialDisplay.OpacityArrayName = ['CELLS', 'Twind']
cloud_materialDisplay.SelectInputVectors = [None, '']
cloud_materialDisplay.WriteLog = ''

# show data from extractSurface1
extractSurface1Display = Show(extractSurface1, renderView1, 'GeometryRepresentation')

# get 2D transfer function for 'temperature'
temperatureTF2D = GetTransferFunction2D('temperature')
temperatureTF2D.ScalarRangeInitialized = 1
temperatureTF2D.Range = [10000.0, 80000.0, 0.0, 1.0]

# get color transfer function/color map for 'temperature'
temperatureLUT = GetColorTransferFunction('temperature')
temperatureLUT.AutomaticRescaleRangeMode = 'Never'
temperatureLUT.TransferFunction2D = temperatureTF2D
temperatureLUT.RGBPoints = [10000.0, 0.267004, 0.004874, 0.329415, 10274.539999999972, 0.26851, 0.009605, 0.335427, 10549.010000000028, 0.269944, 0.014625, 0.341379, 10823.55, 0.271305, 0.019942, 0.347269, 11098.019999999986, 0.272594, 0.025563, 0.353093, 11372.560000000027, 0.273809, 0.031497, 0.358853, 11647.030000000013, 0.274952, 0.037752, 0.364543, 11921.569999999985, 0.276022, 0.044167, 0.370164, 12196.110000000026, 0.277018, 0.050344, 0.375715, 12470.580000000013, 0.277941, 0.056324, 0.381191, 12745.119999999984, 0.278791, 0.062145, 0.386592, 13019.589999999971, 0.279566, 0.067836, 0.391917, 13294.130000000012, 0.280267, 0.073417, 0.397163, 13568.599999999999, 0.280894, 0.078907, 0.402329, 13843.13999999997, 0.281446, 0.08432, 0.407414, 14117.680000000011, 0.281924, 0.089666, 0.412415, 14392.149999999998, 0.282327, 0.094955, 0.417331, 14666.68999999997, 0.282656, 0.100196, 0.42216, 14941.160000000025, 0.28291, 0.105393, 0.426902, 15215.699999999997, 0.283091, 0.110553, 0.431554, 15490.169999999984, 0.283197, 0.11568, 0.436115, 15764.710000000025, 0.283229, 0.120777, 0.440584, 16039.249999999996, 0.283187, 0.125848, 0.44496, 16313.719999999983, 0.283072, 0.130895, 0.449241, 16588.260000000024, 0.282884, 0.13592, 0.453427, 16862.73000000001, 0.282623, 0.140926, 0.457517, 17137.269999999982, 0.28229, 0.145912, 0.46151, 17411.740000000038, 0.281887, 0.150881, 0.465405, 17686.28000000001, 0.281412, 0.155834, 0.469201, 17960.749999999996, 0.280868, 0.160771, 0.472899, 18235.290000000037, 0.280255, 0.165693, 0.476498, 18509.83000000001, 0.279574, 0.170599, 0.479997, 18784.299999999996, 0.278826, 0.17549, 0.483397, 19058.840000000033, 0.278012, 0.180367, 0.486697, 19333.31000000002, 0.277134, 0.185228, 0.489898, 19607.84999999999, 0.276194, 0.190074, 0.493001, 19882.319999999978, 0.275191, 0.194905, 0.496005, 20156.860000000022, 0.274128, 0.199721, 0.498911, 20431.399999999994, 0.273006, 0.20452, 0.501721, 20705.86999999998, 0.271828, 0.209303, 0.504434, 20980.410000000018, 0.270595, 0.214069, 0.507052, 21254.880000000005, 0.269308, 0.218818, 0.509577, 21529.419999999976, 0.267968, 0.223549, 0.512008, 21803.889999999967, 0.26658, 0.228262, 0.514349, 22078.430000000008, 0.265145, 0.232956, 0.516599, 22352.96999999998, 0.263663, 0.237631, 0.518762, 22627.440000000035, 0.262138, 0.242286, 0.520837, 22901.980000000003, 0.260571, 0.246922, 0.522828, 23176.449999999993, 0.258965, 0.251537, 0.524736, 23450.990000000034, 0.257322, 0.25613, 0.526563, 23725.46000000002, 0.255645, 0.260703, 0.528312, 23999.999999999993, 0.253935, 0.265254, 0.529983, 24274.54000000003, 0.252194, 0.269783, 0.531579, 24549.01000000002, 0.250425, 0.27429, 0.533103, 24823.549999999992, 0.248629, 0.278775, 0.534556, 25098.01999999998, 0.246811, 0.283237, 0.535941, 25372.56000000002, 0.244972, 0.287675, 0.53726, 25647.030000000006, 0.243113, 0.292092, 0.538516, 25921.569999999978, 0.241237, 0.296485, 0.539709, 26196.11000000002, 0.239346, 0.300855, 0.540844, 26470.580000000005, 0.237441, 0.305202, 0.541921, 26745.120000000046, 0.235526, 0.309527, 0.542944, 27019.590000000033, 0.233603, 0.313828, 0.543914, 27294.130000000005, 0.231674, 0.318106, 0.544834, 27568.59999999999, 0.229739, 0.322361, 0.545706, 27843.140000000032, 0.227802, 0.326594, 0.546532, 28117.680000000004, 0.225863, 0.330805, 0.547314, 28392.149999999987, 0.223925, 0.334994, 0.548053, 28666.69000000003, 0.221989, 0.339161, 0.548752, 28941.160000000014, 0.220057, 0.343307, 0.549413, 29215.699999999986, 0.21813, 0.347432, 0.550038, 29490.169999999976, 0.21621, 0.351535, 0.550627, 29764.710000000017, 0.214298, 0.355619, 0.551184, 30039.24999999999, 0.212395, 0.359683, 0.55171, 30313.719999999976, 0.210503, 0.363727, 0.552206, 30588.260000000017, 0.208623, 0.367752, 0.552675, 30862.73, 0.206756, 0.371758, 0.553117, 31137.270000000044, 0.204903, 0.375746, 0.553533, 31411.74000000003, 0.203063, 0.379716, 0.553925, 31686.280000000002, 0.201239, 0.38367, 0.554294, 31960.74999999999, 0.19943, 0.387607, 0.554642, 32235.29000000003, 0.197636, 0.391528, 0.554969, 32509.83, 0.19586, 0.395433, 0.555276, 32784.29999999999, 0.1941, 0.399323, 0.555565, 33058.840000000026, 0.192357, 0.403199, 0.555836, 33333.31000000001, 0.190631, 0.407061, 0.556089, 33607.849999999984, 0.188923, 0.41091, 0.556326, 33882.32000000004, 0.187231, 0.414746, 0.556547, 34156.860000000015, 0.185556, 0.41857, 0.556753, 34431.39999999999, 0.183898, 0.422383, 0.556944, 34705.87000000004, 0.182256, 0.426184, 0.55712, 34980.41000000002, 0.180629, 0.429975, 0.557282, 35254.88, 0.179019, 0.433756, 0.55743, 35529.42000000004, 0.177423, 0.437527, 0.557565, 35803.89000000003, 0.175841, 0.44129, 0.557685, 36078.43, 0.174274, 0.445044, 0.557792, 36352.96999999997, 0.172719, 0.448791, 0.557885, 36627.44000000003, 0.171176, 0.45253, 0.557965, 36901.979999999996, 0.169646, 0.456262, 0.55803, 37176.44999999998, 0.168126, 0.459988, 0.558082, 37450.99000000003, 0.166617, 0.463708, 0.558119, 37725.460000000014, 0.165117, 0.467423, 0.558141, 37999.999999999985, 0.163625, 0.471133, 0.558148, 38274.54000000002, 0.162142, 0.474838, 0.55814, 38549.01000000001, 0.160665, 0.47854, 0.558115, 38823.54999999999, 0.159194, 0.482237, 0.558073, 39098.01999999997, 0.157729, 0.485932, 0.558013, 39372.56000000001, 0.15627, 0.489624, 0.557936, 39647.03, 0.154815, 0.493313, 0.55784, 39921.570000000036, 0.153364, 0.497, 0.557724, 40196.11000000001, 0.151918, 0.500685, 0.557587, 40470.58, 0.150476, 0.504369, 0.55743, 40745.12000000004, 0.149039, 0.508051, 0.55725, 41019.590000000026, 0.147607, 0.511733, 0.557049, 41294.13, 0.14618, 0.515413, 0.556823, 41568.59999999998, 0.144759, 0.519093, 0.556572, 41843.14000000002, 0.143343, 0.522773, 0.556295, 42117.67999999999, 0.141935, 0.526453, 0.555991, 42392.14999999998, 0.140536, 0.530132, 0.555659, 42666.69000000002, 0.139147, 0.533812, 0.555298, 42941.16000000001, 0.13777, 0.537492, 0.554906, 43215.69999999998, 0.136408, 0.541173, 0.554483, 43490.170000000035, 0.135066, 0.544853, 0.554029, 43764.71000000001, 0.133743, 0.548535, 0.553541, 44039.24999999998, 0.132444, 0.552216, 0.553018, 44313.72000000004, 0.131172, 0.555899, 0.552459, 44588.26000000001, 0.129933, 0.559582, 0.551864, 44862.729999999996, 0.128729, 0.563265, 0.551229, 45137.27000000004, 0.127568, 0.566949, 0.550556, 45411.74000000002, 0.126453, 0.570633, 0.549841, 45686.27999999999, 0.125394, 0.574318, 0.549086, 45960.749999999985, 0.124395, 0.578002, 0.548287, 46235.29000000002, 0.123463, 0.581687, 0.547445, 46509.829999999994, 0.122606, 0.585371, 0.546557, 46784.30000000005, 0.121831, 0.589055, 0.545623, 47058.840000000026, 0.121148, 0.592739, 0.544641, 47333.310000000005, 0.120565, 0.596422, 0.543611, 47607.85000000005, 0.120092, 0.600104, 0.54253, 47882.32000000003, 0.119738, 0.603785, 0.5414, 48156.86000000001, 0.119512, 0.607464, 0.540218, 48431.39999999997, 0.119423, 0.611141, 0.538982, 48705.87000000003, 0.119483, 0.614817, 0.537692, 48980.41000000001, 0.119699, 0.61849, 0.536347, 49254.87999999999, 0.120081, 0.622161, 0.534946, 49529.420000000035, 0.120638, 0.625828, 0.533488, 49803.890000000014, 0.12138, 0.629492, 0.531973, 50078.42999999999, 0.122312, 0.633153, 0.530398, 50352.97000000003, 0.123444, 0.636809, 0.528763, 50627.44000000002, 0.12478, 0.640461, 0.527068, 50901.979999999996, 0.126326, 0.644107, 0.525311, 51176.45000000005, 0.128087, 0.647749, 0.523491, 51450.99000000002, 0.130067, 0.651384, 0.521608, 51725.46, 0.132268, 0.655014, 0.519661, 52000.000000000044, 0.134692, 0.658636, 0.517649, 52274.540000000015, 0.137339, 0.662252, 0.515571, 52549.01, 0.14021, 0.665859, 0.513427, 52823.55000000004, 0.143303, 0.669459, 0.511215, 53098.02000000003, 0.146616, 0.67305, 0.508936, 53372.560000000005, 0.150148, 0.676631, 0.506589, 53647.029999999984, 0.153894, 0.680203, 0.504172, 53921.570000000036, 0.157851, 0.683765, 0.501686, 54196.11, 0.162016, 0.687316, 0.499129, 54470.58000000006, 0.166383, 0.690856, 0.496502, 54745.120000000024, 0.170948, 0.694384, 0.493803, 55019.59000000002, 0.175707, 0.6979, 0.491033, 55294.12999999999, 0.180653, 0.701402, 0.488189, 55568.60000000004, 0.185783, 0.704891, 0.485273, 55843.14000000002, 0.19109, 0.708366, 0.482284, 56117.679999999986, 0.196571, 0.711827, 0.479221, 56392.150000000045, 0.202219, 0.715272, 0.476084, 56666.69000000001, 0.20803, 0.718701, 0.472873, 56941.16, 0.214, 0.722114, 0.469588, 57215.70000000004, 0.220124, 0.725509, 0.466226, 57490.17000000003, 0.226397, 0.728888, 0.462789, 57764.71000000001, 0.232815, 0.732247, 0.459277, 58039.250000000044, 0.239374, 0.735588, 0.455688, 58313.72000000003, 0.24607, 0.73891, 0.452024, 58588.26000000007, 0.252899, 0.742211, 0.448284, 58862.730000000054, 0.259857, 0.745492, 0.444467, 59137.270000000026, 0.266941, 0.748751, 0.440573, 59411.74000000001, 0.274149, 0.751988, 0.436601, 59686.27999999999, 0.281477, 0.755203, 0.432552, 59960.750000000044, 0.288921, 0.758394, 0.428426, 60235.290000000015, 0.296479, 0.761561, 0.424223, 60509.82999999998, 0.304148, 0.764704, 0.419943, 60784.30000000004, 0.311925, 0.767822, 0.415586, 61058.84000000001, 0.319809, 0.770914, 0.411152, 61333.31, 0.327796, 0.77398, 0.40664, 61607.850000000035, 0.335885, 0.777018, 0.402049, 61882.32000000003, 0.344074, 0.780029, 0.397381, 62156.86, 0.35236, 0.783011, 0.392636, 62431.40000000004, 0.360741, 0.785964, 0.387814, 62705.870000000024, 0.369214, 0.788888, 0.382914, 62980.409999999996, 0.377779, 0.791781, 0.377939, 63254.880000000056, 0.386433, 0.794644, 0.372886, 63529.42000000002, 0.395174, 0.797475, 0.367757, 63803.890000000014, 0.404001, 0.800275, 0.362552, 64078.43000000005, 0.412913, 0.803041, 0.357269, 64352.97000000002, 0.421908, 0.805774, 0.35191, 64627.44000000001, 0.430983, 0.808473, 0.346476, 64901.97999999998, 0.440137, 0.811138, 0.340967, 65176.45000000004, 0.449368, 0.813768, 0.335384, 65450.990000000005, 0.458674, 0.816363, 0.329727, 65725.45999999999, 0.468053, 0.818921, 0.323998, 66000.00000000003, 0.477504, 0.821444, 0.318195, 66274.54000000001, 0.487026, 0.823929, 0.312321, 66549.01000000007, 0.496615, 0.826376, 0.306377, 66823.55000000005, 0.506271, 0.828786, 0.300362, 67098.02000000002, 0.515992, 0.831158, 0.294279, 67372.56000000006, 0.525776, 0.833491, 0.288127, 67647.03000000006, 0.535621, 0.835785, 0.281908, 67921.57000000002, 0.545524, 0.838039, 0.275626, 68196.10999999999, 0.555484, 0.840254, 0.269281, 68470.58000000005, 0.565498, 0.84243, 0.262877, 68745.12000000002, 0.575563, 0.844566, 0.256415, 69019.59000000001, 0.585678, 0.846661, 0.249897, 69294.12999999998, 0.595839, 0.848717, 0.243329, 69568.60000000003, 0.606045, 0.850733, 0.236712, 69843.14000000001, 0.616293, 0.852709, 0.230052, 70117.68000000005, 0.626579, 0.854645, 0.223353, 70392.14999999997, 0.636902, 0.856542, 0.21662, 70666.69, 0.647257, 0.8584, 0.209861, 70941.16, 0.657642, 0.860219, 0.203082, 71215.70000000004, 0.668054, 0.861999, 0.196293, 71490.17000000001, 0.678489, 0.863742, 0.189503, 71764.70999999999, 0.688944, 0.865448, 0.182725, 72039.25000000003, 0.699415, 0.867117, 0.175971, 72313.72000000002, 0.709898, 0.868751, 0.169257, 72588.26000000007, 0.720391, 0.87035, 0.162603, 72862.73000000004, 0.730889, 0.871916, 0.156029, 73137.27000000002, 0.741388, 0.873449, 0.149561, 73411.74, 0.751884, 0.874951, 0.143228, 73686.28000000004, 0.762373, 0.876424, 0.137064, 73960.75000000003, 0.772852, 0.877868, 0.131109, 74235.29000000001, 0.783315, 0.879285, 0.125405, 74509.83000000005, 0.79376, 0.880678, 0.120005, 74784.30000000003, 0.804182, 0.882046, 0.114965, 75058.84, 0.814576, 0.883393, 0.110347, 75333.31000000006, 0.82494, 0.88472, 0.106217, 75607.85000000003, 0.83527, 0.886029, 0.102646, 75882.32000000002, 0.845561, 0.887322, 0.099702, 76156.86000000006, 0.85581, 0.888601, 0.097452, 76431.40000000004, 0.866013, 0.889868, 0.095953, 76705.87000000001, 0.876168, 0.891125, 0.09525, 76980.40999999999, 0.886271, 0.892374, 0.095374, 77254.88000000005, 0.89632, 0.893616, 0.096335, 77529.42000000001, 0.906311, 0.894855, 0.098125, 77803.89, 0.916242, 0.896091, 0.100717, 78078.42999999998, 0.926106, 0.89733, 0.104071, 78352.97000000002, 0.935904, 0.89857, 0.108131, 78627.44, 0.945636, 0.899815, 0.112838, 78901.98000000004, 0.9553, 0.901065, 0.118128, 79176.45000000003, 0.964894, 0.902323, 0.123941, 79450.99000000008, 0.974417, 0.90359, 0.130215, 79725.45999999999, 0.983868, 0.904867, 0.136897, 80000.00000000003, 0.993248, 0.906157, 0.143936]
temperatureLUT.NanColor = [1.0, 0.0, 0.0]
temperatureLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
extractSurface1Display.Representation = 'Surface'
extractSurface1Display.ColorArrayName = ['CELLS', 'temperature']
extractSurface1Display.LookupTable = temperatureLUT
extractSurface1Display.SelectTCoordArray = 'None'
extractSurface1Display.SelectNormalArray = 'None'
extractSurface1Display.SelectTangentArray = 'None'
extractSurface1Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractSurface1Display.SelectOrientationVectors = 'None'
extractSurface1Display.ScaleFactor = 3.1379013061523438
extractSurface1Display.SelectScaleArray = 'Twind'
extractSurface1Display.GlyphType = 'Arrow'
extractSurface1Display.GlyphTableIndexArray = 'Twind'
extractSurface1Display.GaussianRadius = 0.15689506530761718
extractSurface1Display.SetScaleArray = [None, '']
extractSurface1Display.ScaleTransferFunction = 'PiecewiseFunction'
extractSurface1Display.OpacityArray = [None, '']
extractSurface1Display.OpacityTransferFunction = 'PiecewiseFunction'
extractSurface1Display.DataAxesGrid = 'GridAxesRepresentation'
extractSurface1Display.PolarAxes = 'PolarAxesRepresentation'
extractSurface1Display.SelectInputVectors = [None, '']
extractSurface1Display.WriteLog = ''

# setup the color legend parameters for each legend in this view

# get color legend/bar for temperatureLUT in view renderView1
temperatureLUTColorBar = GetScalarBar(temperatureLUT, renderView1)
temperatureLUTColorBar.Orientation = 'Horizontal'
temperatureLUTColorBar.WindowLocation = 'Any Location'
temperatureLUTColorBar.Position = [0.34447539461467036, 0.9099904489016237]
temperatureLUTColorBar.Title = 'temperature'
temperatureLUTColorBar.ComponentTitle = ''
temperatureLUTColorBar.ScalarBarLength = 0.32999999999999985

# set color bar visibility
temperatureLUTColorBar.Visibility = 1

# show color legend
extractSurface1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup the visualization in view 'spreadSheetView2'
# ----------------------------------------------------------------

# show data from programmableFilter1
programmableFilter1Display = Show(programmableFilter1, spreadSheetView2, 'SpreadSheetRepresentation')

# trace defaults for the display properties.
programmableFilter1Display.Assembly = ''

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'temperature'
temperaturePWF = GetOpacityTransferFunction('temperature')
temperaturePWF.Points = [10000.0, 0.0, 0.5, 0.0, 80000.0, 1.0, 0.5, 0.0]
temperaturePWF.ScalarRangeInitialized = 1
'''
# ----------------------------------------------------------------
# restore active source
SetActiveSource(programmableFilter1)
# ----------------------------------------------------------------
'''

if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
