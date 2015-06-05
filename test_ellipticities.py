import numpy as np
import healpy as hp

import catalogue_to_healpix_map_tools

rad2degree = 180./np.pi

#make some fake data
n_side = 512

#define a pixel and find its ra and dec
theta, phi = hp.pix2ang(n_side,0)

ra = rad2degree*phi + 180.
dec = -rad2degree*(theta-np.pi/2.)

n_gals = 10000

gal_id = np.asarray(range(n_gals))
ra_vec = np.ones(n_gals)*ra
dec_vec = np.ones(n_gals)*dec
e0 = np.random.normal(0,1,n_gals)
e1 = np.random.normal(0,1,n_gals)

np.savetxt("./test_cat.ssv",np.asarray([gal_id,ra_vec,dec_vec,e0,e1]).T,
    fmt=['%d','%.6e','%.6e','%.8e','%.8e'],header="unique_gal_id ra_gal_mag dec_gal_mag gamma1 gamma2")

col_ra = 1
col_dec = 2
col_gamma_1 = 3
col_gamma_2 = 4

# now read the catalogue and pring the sigmas
c2m = catalogue_to_healpix_map_tools.converter(
    "./test_cat.ssv",
    col_ra,col_dec,col_gamma_1,col_gamma_2,n_side)
c2m.accumulate_objects()

print "e0 mu = ",np.mean(e0),c2m.G1[0]
print "e1 mu = ",np.mean(e1),c2m.G2[0]
print "e0 ninv = ",1./np.var(e0),c2m.G1_ninv[0]
print "e1 ninv = ",1./np.var(e1),c2m.G2_ninv[0]
