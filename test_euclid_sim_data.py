import catalogue_to_healpix_map_tools

col_ra = 0
col_dec = 1
col_z = 2
col_gamma_1 = 3
col_gamma_2 = 4

n_side = 256
file_name = '/Users/sbalan/Projects/MICE_EUCLID/euclidcat01_100k.dat'
z_bounds = [0.55,0.65]

c2m = catalogue_to_healpix_map_tools.converter(file_name,col_ra,col_dec,col_z,col_gamma_1,col_gamma_2,n_side,z_bounds)

c2m.accumulate_objects()

c2m.write_maps("/Users/sbalan/Projects/MICE_EUCLID/euclid_sim")
c2m.write_png_maps("/Users/sbalan/Projects/MICE_EUCLID/euclid_sim")

