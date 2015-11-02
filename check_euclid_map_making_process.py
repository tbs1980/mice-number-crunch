import numpy as np
import healpy as hp
import logging
import os.path
import time


def accumulate_objects(cat_file_name,col_ra,col_dec,col_z,col_g1,col_g2,true_g_map_file_name,mask_file_name,n_side):
    # open the true gamma file
    gamma_map = hp.read_map(true_g_map_file_name,field=1)

    # open the mask
    mask = hp.read_map(mask_file_name)
    
    deg2rad = np.pi/180.

    with open(cat_file_name) as f:
        # skip the header
        f.readline()

        z_bounds = [0.,100.]

        # accumulate objects
        i = 0
        for line in f:
            ents = line.split()
            #print ents
            ra_val = float(ents[col_ra])
            dec_val = float(ents[col_dec])
            z_val = float(ents[col_z])
            G1_val = float(ents[col_g1])
            G2_val = float(ents[col_g2])

            if z_val >= z_bounds[0] and z_val < z_bounds[1] :
                theta = -deg2rad*dec_val + np.pi/2.
                #phi = deg2rad*(ra_val - 180.)
                phi = deg2rad*(ra_val)

                try:
                    pix = hp.ang2pix(n_side,theta,phi)
                    if mask[pix] > 0.:
                        print "the value of G from cat and map are", G1_val,gamma_map[pix]
                except:
                    pass

            if i > 1000:
                break

            i = i + 1


# now do the processing

cat_file_name = "/share/splinter/hsxavier/hsxavier/tosree02/test-ellip-noise0-catalog.dat"
col_ra = 0
col_dec = 1
col_z = 2
col_g1 = 4
col_g2 = 5
true_g_map_file_name = "/share/splinter/hsxavier/hsxavier/tosree02/test-ellip-noise0-lensingmap-f2z9.fits"
mask_file_name =  "/share/data1/sbalan/EUCLID/henrique/Euclid_footprint_and_StarMask4096.fits"
n_side = 4096

accumulate_objects(cat_file_name,col_ra,col_dec,col_z,col_g1,col_g2,true_g_map_file_name,mask_file_name,n_side)


        
