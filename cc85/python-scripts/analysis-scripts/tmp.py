import numpy as np
import pickle
import paraview
import sys

filename = sys.argv[1]

# print("Before:")
with open(f'./paraview-cloud-analysis_data-dump/{filename}.pickle', 'rb') as handle:
    data = pickle.load(handle)
    # print(type(data['12']['cloud_volume_elems']))
    for key in list(data.keys()):
        data[key]['cloud_volume_elems'] = np.array(data[key]['cloud_volume_elems'])
# print("After:")
# print(type(data['12']['cloud_volume_elems']))

with open(f'./paraview-cloud-analysis_data-dump/{filename}.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
