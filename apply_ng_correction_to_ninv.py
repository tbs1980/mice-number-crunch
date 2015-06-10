import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

input_data_path = "/resource/data/MICE/maps/"

res = "512"

# read the g_ninv
g_ninv_file_name  = input_data_path  + res + "/mice_v2_0_shear_g_ninv.fits"
g_ninv = hp.read_map(g_ninv_file_name)

# read the G_ninv
G_ninv_file_name = input_data_path + res + "/mice_v2_0_shear_G_ninv.fits"
G0_ninv = hp.read_map(G_ninv_file_name,field=0)
G1_ninv = hp.read_map(G_ninv_file_name,field=1)

# get n_bar from the g_ninv
n_bar  = np.mean(1./g_ninv[g_ninv>0])
print "n_bar = ",n_bar

# multiply G0 and G1 ninv by n_bar

G0_ninv *= n_bar
G1_ninv *= n_bar

# now write new maps

G_ninv_out_file_name = input_data_path + res + "/mice_v2_0_shear_G_corr_ninv.fits"
hp.write_map(G_ninv_out_file_name,m=[G0_ninv,G1_ninv])


G0_ninv_png_out_file_name = input_data_path + res + "/mice_v2_0_shear_G0_corr_ninv.png"
hp.mollview(G0_ninv)
plt.savefig(G0_ninv_png_out_file_name)

G1_ninv_png_out_file_name = input_data_path + res + "/mice_v2_0_shear_G1_corr_ninv.png"
hp.mollview(G1_ninv)
plt.savefig(G1_ninv_png_out_file_name)


