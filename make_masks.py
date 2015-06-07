import numpy as np
import healpy as hp
import matplotlib.pyplot as plt


for res in ["4096"]:
    n_inv_file_name = "/resource/data/MICE/maps/"+res+"/mice_v2_0_shear_g_ninv.fits"
    print "reading",n_inv_file_name

    mask = hp.read_map(n_inv_file_name)

    mask[mask<=0] = 0
    mask[mask>0] = 1

    mask_out_file = "/resource/data/MICE/maps/"+res+"/mice_v2_0_shear_mask.fits"

    hp.write_map(mask_out_file,mask)

    mask_out_file_png = "/resource/data/MICE/maps/"+res+"/mice_v2_0_shear_mask.png"
    hp.mollview(mask)
    plt.savefig(mask_out_file_png)
    #plt.clf()
