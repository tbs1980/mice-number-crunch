import numpy as np
import healpy as hp

# read the footprint
foot_print = hp.read_map('/share/data1/sbalan/EUCLID/henrique/Euclid_footprint_4096.fits')

# read the star-mask
star_mask = hp.read_map('/share/data1/sbalan/EUCLID/henrique/StarMask4096.fits')

foot_print *= star_mask

hp.write_map('/share/data1/sbalan/EUCLID/henrique/Euclid_footprint_and_StarMask4096.fits',foot_print)
