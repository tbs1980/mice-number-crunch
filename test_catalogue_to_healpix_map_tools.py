import catalogue_to_healpix_map_tools

col_ra = 1
col_dec = 2
col_gamma_1 = 4
col_gamma_2 = 5

n_side = 4096
#n_side = 2048
#n_side = 1024
#n_side = 512

#c2m = catalogue_to_healpix_map_tools.converter(
#    "/resource/data/MICE/catalogues/test_shear.ssv",
#    col_ra,col_dec,col_gamma_1,col_gamma_2,n_side)

c2m = catalogue_to_healpix_map_tools.converter(
    "/resource/data/MICE/catalogues/mice_v2_0_shear_order_by_unique_gal_id.ssv",
    col_ra,col_dec,col_gamma_1,col_gamma_2,n_side)

c2m.accumulate_objects()
#c2m.write_maps("/resource/data/MICE/temp_maps/test")
#c2m.write_png_maps("/resource/data/MICE/temp_maps/test")

c2m.write_maps("/resource/data/MICE/maps/4096/mice_v2_0_shear")
c2m.write_png_maps("/resource/data/MICE/maps/4096/mice_v2_0_shear")

#c2m.write_maps("/resource/data/MICE/maps/2048/mice_v2_0_shear")
#c2m.write_png_maps("/resource/data/MICE/maps/2048/mice_v2_0_shear")

#c2m.write_maps("/resource/data/MICE/maps/1024/mice_v2_0_shear")
#c2m.write_png_maps("/resource/data/MICE/maps/1024/mice_v2_0_shear")

#c2m.write_maps("/resource/data/MICE/maps/512/mice_v2_0_shear")
#c2m.write_png_maps("/resource/data/MICE/maps/512/mice_v2_0_shear")



