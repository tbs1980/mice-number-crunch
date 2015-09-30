import catalogue_to_healpix_map_tools

col_ra = 0
col_dec = 1
col_z = 2
col_gamma_1 = 3
col_gamma_2 = 4

n_side = 256
file_name = '/share/data1/sbalan/EUCLID/henrique/toSree01/euclidcat01.dat'
z_bounds = [0.55,0.65]

c2m = catalogue_to_healpix_map_tools.converter(file_name,col_ra,col_dec,col_z,col_gamma_1,col_gamma_2,n_side,z_bounds)

c2m.accumulate_objects()

c2m.write_maps('/share/data1/sbalan/EUCLID/henrique/process_data/maps/ns_256')
c2m.write_png_maps('/share/data1/sbalan/EUCLID/henrique/process_data/maps/ns_256')

