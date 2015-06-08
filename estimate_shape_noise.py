import numpy as np
import healpy as hp

#res = "2048"
#res = "512"
res = "4096"

input_data_prefix = "/resource/data/MICE/maps/"
output_data_prefix = "/arxiv/projects/MICEDataAnalysis/ForEuclidMeetingLausanne/spice_pcl_analysis/"

ninv_file_name = input_data_prefix + res + "/mice_v2_0_shear_G_ninv.fits"

# read the n_inv data
m0 = hp.read_map(ninv_file_name,field=0)
m1 = hp.read_map(ninv_file_name,field=1)

sig0 = np.mean(np.sqrt(1./m0[np.where(m0>0)]))
sig1 = np.mean(np.sqrt(1./m1[np.where(m1>0)]))

output_file_name = output_data_prefix + res + "/mice_v2_0_shear_shape_noise.dat"

strsig = str(sig0) + "\t" + str(sig1)
with open(output_file_name, 'w') as f:
    f.write(strsig)
