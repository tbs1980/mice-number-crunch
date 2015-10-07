import catalogue_to_healpix_map_tools
import sys
import time

def create_maps(n_side,intpu_file_name,z_bounds,output_path):
    col_ra = 0
    col_dec = 1
    col_z = 2
    col_gamma_1 = 3
    col_gamma_2 = 4

    #n_side = 256
    #file_name = '/share/data1/sbalan/EUCLID/henrique/toSree01/euclidcat01.dat'
    #z_bounds = [0.55,0.65]
    
    if z_bounds[0] >= z_bounds[1] :
        raise RuntimeError("z-max should be greater than z-min")

    c2m = catalogue_to_healpix_map_tools.converter(intpu_file_name,col_ra,col_dec,col_z,col_gamma_1,col_gamma_2,n_side,z_bounds)

    c2m.accumulate_objects()
    
    output_path += "_"+str(z_bounds[0])+"_"+str(z_bounds[1])+"_ns_"+str(n_side)
    
    print output_path

    #c2m.write_maps('/share/data1/sbalan/EUCLID/henrique/process_data/maps/ns_256')
    c2m.write_maps(output_path)
    #c2m.write_png_maps('/share/data1/sbalan/EUCLID/henrique/process_data/maps/ns_256')


if __name__ == "__main__":
    if len(sys.argv) == 6 :
        start_time = time.time()
        
        n_side = int(sys.argv[1])
        intpu_file_name = sys.argv[2]
        z_bounds_start = float(sys.argv[3])
        z_bounds_end = float(sys.argv[4])
        output_path = sys.argv[5]
        
        z_bounds = [z_bounds_start,z_bounds_end]
        
        create_maps(n_side,intpu_file_name,z_bounds,output_path)
        
        print ""
        print (time.time() - start_time) / 60.0, 'minutes'
    else:
        print "usage: python ",sys.argv[0], "<nside> <input_file> <z_min> <z_max> <output_path>"
         
    
    
