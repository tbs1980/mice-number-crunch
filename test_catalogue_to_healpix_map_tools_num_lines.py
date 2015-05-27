import catalogue_to_healpix_map_tools

col_ra = 1
col_dec = 2
col_gamma_1 = 4
col_gamma_2 = 5

n_side = 2048

c2m = catalogue_to_healpix_map_tools.converter(
    "/resource/data/MICE/catalogues/test_shear.ssv",
    col_ra,col_dec,col_gamma_1,col_gamma_2,n_side)

#c2m = catalogue_to_healpix_map_tools.converter(
#    "/resource/data/MICE/catalogues/mice_v2_0_shear_order_by_unique_gal_id.ssv",
#    col_ra,col_dec,col_gamma_1,col_gamma_2,n_side)

#print c2m.get_num_lines()
offset_val =  c2m.line_offset_val(10)

with open("/resource/data/MICE/catalogues/test_shear.ssv") as f:
    f.seek(offset_val)
    print f.readline()
