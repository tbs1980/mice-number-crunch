import numpy as np
import healpy as hp
import logging
import os.path
import time

class converter:
    """
    A class for coverting galaxy catalogues to healpix maps
    """

    def __init__(self,file_name,col_ra,col_dec,col_z,col_gamma_1,col_gamma_2,n_side,z_bounds,mask_file_name=None):
        """
        A constructor for creating a catalogue to HEALPix map converter. (ra,dec)
        coordinates are assumed to be in degrees.

        @param file_name file name of the input catalogue
        @param col_ra column number of right angle
        @param col_z column number of the z
        @param col_dec column number of declination
        @param col_gamma_1 column number of ellipticity 1
        @param col_gamma_2 column number of ellipticity 2
        @param n_side number sides of the HEALPix map
        @param z_bounds boundaries of the z
        @param mask_file_name file name of the mask in healpix format

        """

        # save the input params
        self.file_name = file_name
        self.col_ra = col_ra
        self.col_dec = col_dec
        self.col_gamma_1 = col_gamma_1
        self.col_gamma_2 = col_gamma_2
        self.n_side = n_side
        self.col_z = col_z
        self.z_bounds = z_bounds
        self.mask_file_name = mask_file_name

        if len(z_bounds) != 2 :
            raise RuntimeError("We were expecting a list of two numbers for the bounds")
        if z_bounds[0] < 0 :
            raise RuntimeError("Z min cannot be a negative number")
        if z_bounds[0]> z_bounds[1]:
            raise RuntimeError("Z min should be less than Z max")

        # start a logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # create healpix maps objects
        self.g = []
        self.g_ninv = []
        self.G1 = []
        self.G2 = []
        self.G1_ninv = []
        self.G2_ninv = []


        self.line_offset = []

        # read the mask
        if self.mask_file_name != None :
            self.mask = hp.read_map(mask_file_name)
        else:
            self.mask = hp.ones(hp.nside2npix(n_side))

        if self.n_side != hp.npix2nside(len(self.mask)):
            raise ValueError("Nside of the mask does not agree with the nside for making maps.")

        self.rotation_of_phi = 0.


    def get_num_lines(self):
        """
        Get the number of lines in a catalogue file.
        """
        with open(self.file_name) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def build_line_offset_index(self):
        """
        Build the line offset index of the entire catalogue so that we can access
        a line in a catalogue without going through a looop.
        """
        # http://stackoverflow.com/questions/620367/how-to-jump-to-a-particular-line-in-a-huge-text-file
        # Read in the file once and build a list of line offsets
        log_str = " Building the line offset index of " + self.file_name
        self.logger.info(log_str)


        offset = 0
        start_time = time.time()
        with open(self.file_name) as f:
            for line in f:
                self.line_offset.append(offset)
                offset += len(line)
            f.seek(0)

        # Now, to skip to line n (with the first line being line 0), just do
        # file.seek(line_offset[n])
        end_time = time.time()
        total_time = end_time - start_time
        log_str = " Time taken for Building the line offset index =  " + str(total_time)
        self.logger.info(log_str)

    def line_offset_val(self,line_number):
        """
        Get the line offset so that we can use f.seek() to reach a desired line
        in a text file.

        @param line_number line number for which offset is sought
        """
        if len(self.line_offset) == 0 :
            self.build_line_offset_index()

        return self.line_offset[line_number]


    def accumulate_objects(self):
        """
        A method that goes through the catalogues and accumulate objects into
        HEALPix maps. It stores the values in member objects.
        """

        log_str = " Accumulating the objects from " + self.file_name
        self.logger.info(log_str)

        # start a timer
        start_time = time.time()

        # create empty healpix maps
        # 1) number counts
        n_pix = hp.nside2npix(self.n_side)
        self.g = np.zeros(n_pix)
        self.g_ninv = np.zeros(n_pix)
        # 2) elllipticities
        self.G1 = np.zeros(n_pix)
        self.G2 = np.zeros(n_pix)
        self.G1_ninv = np.zeros(n_pix)
        self.G2_ninv = np.zeros(n_pix)

        # conversion factor from degrees to radians
        deg2rad = np.pi/180.

        # open the catalogue file
        with open(self.file_name) as f:
            # skip header
            f.readline()

            # accumulate objects
            i = 0
            for line in f:
                #print line
                # get the entries from a line
                ents = line.split()

                if i % 100000000 == 0:
                    log_str = " Number of objects processed = " + str(i) + " id = " + ents[0]
                    self.logger.info(log_str)

                # get the ra,dec,etc from the entries
                ra_val = float(ents[self.col_ra])
                dec_val = float(ents[self.col_dec])
                z_val = float(ents[self.col_z])
                G1_val = float(ents[self.col_gamma_1])
                G2_val = float(ents[self.col_gamma_2])

                # check if we fall in the correct bin
                if z_val >= self.z_bounds[0] and z_val < self.z_bounds[1] :
                    #print "zval = ",z_val, "we are inside the bounds"
                    # convert (ra,dec) -> (theta,phi)
                    theta = -deg2rad*dec_val + np.pi/2.
                    phi = deg2rad*(ra_val - self.rotation_of_phi)


                    try:
                        pix = hp.ang2pix(self.n_side,theta,phi)
                        if self.mask[pix] > 0.:
                            #print "we have an observed pixel"
                            # increase the object count in the pixel
                            self.g[pix] += 1

                            delta1 = G1_val - self.G1[pix]
                            self.G1[pix] += delta1/float(self.g[pix])
                            self.G1_ninv[pix] += delta1*(G1_val - self.G1[pix])

                            delta2 = G2_val - self.G2[pix]
                            self.G2[pix] += delta2/float(self.g[pix])
                            self.G2_ninv[pix] += delta2*(G2_val - self.G2[pix])
                    except:
                        #log_str = " Unexpected value of theta = " + str(theta) + " for #object " + str(i)
                        #self.logger.info(log_str)
                        pass

                # 500,000,000
                #if i >= 1e3:
                #    break

                i = i + 1

        # find the mean number of galaxies in the catalogue
        n_bar  = np.mean(self.g[ np.where(self.mask>0) ])
        log_str = " Mean number of galaxies after accumulation =  " + str(n_bar)
        self.logger.info(log_str)

        # var for each pixel = 1/n_bar and n_inv is the iverse of var
        self.g_ninv[ np.where(self.mask>0) ] = 1./n_bar

        # compute the inverse variance of shears 1 and 2
        # we require 1/var = 1/sigma^2
        #for pix in range(n_pix):
        #    if self.G1_ninv[pix] > 0. and  self.G2_ninv[pix] > 0. :
        #        self.G1_ninv[pix] = float(self.g[pix]-1.)/self.G1_ninv[pix]
        #        self.G2_ninv[pix] = float(self.g[pix]-1.)/self.G2_ninv[pix]
        #    else :
        #        self.g[pix] = 0#hp.pixelfunc.UNSEEN
        #        self.G1[pix] = 0#hp.pixelfunc.UNSEEN
        #        self.G2[pix] = 0#hp.pixelfunc.UNSEEN
        #        self.G1_ninv[pix] = 0#hp.pixelfunc.UNSEEN
        #        self.G2_ninv[pix] = 0#hp.pixelfunc.UNSEEN

        log_str = " Computing the nInv values"
        self.logger.info(log_str)

        self.G1_ninv[np.where(self.G1_ninv>0.)] = (self.g[np.where(self.G1_ninv>0.)]-1.)/self.G1_ninv[np.where(self.G1_ninv>0.)]
        self.G2_ninv[np.where(self.G2_ninv>0.)] = (self.g[np.where(self.G2_ninv>0.)]-1.)/self.G2_ninv[np.where(self.G2_ninv>0.)]

        end_time = time.time()

        total_time = end_time - start_time
        log_str = " Time taken for accumulation =  " + str(total_time)
        self.logger.info(log_str)

    def write_maps(self,output_path):
        """
        Write HEALPix maps.

        @param output_path output path
        """
        dir_name = os.path.dirname(output_path)
        log_str = " Writing the output fits files to  " + dir_name
        self.logger.info(log_str)

        file_tag = os.path.split(output_path)[1]

        #g_file_name = os.path.join(dir_name,str(file_tag)+"_g_data.fits")
        #hp.write_map(g_file_name,self.g)

        #g_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_g_ninv.fits")
        #hp.write_map(g_ninv_file_name,self.g_ninv)

        G_file_name = os.path.join(dir_name,str(file_tag)+"_G_data.fits")
        hp.write_map(G_file_name,m=[self.G1,self.G2])

        G_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_G_ninv.fits")
        hp.write_map(G_ninv_file_name,m=[self.G1_ninv,self.G2_ninv])

        #gG_file_name = os.path.join(dir_name,str(file_tag)+"_gG_data.fits")
        #hp.write_map(gG_file_name,m=[self.g,self.G1,self.G2])

        #gG_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_gG_ninv.fits")
        #hp.write_map(gG_ninv_file_name,m=[self.g_ninv,self.G1_ninv,self.G2_ninv])

    def write_png_maps(self,output_path):
        """
        Write HEALPix maps as png files.

        @param output_path output path
        """
        import matplotlib.pyplot as plt

        dir_name = os.path.dirname(output_path)
        log_str = " Writing the output png files to  " + dir_name
        self.logger.info(log_str)

        file_tag = os.path.split(output_path)[1]

        g_file_name = os.path.join(dir_name,str(file_tag)+"_g_data.png")
        hp.mollview(self.g)
        plt.savefig(g_file_name)

        g_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_g_ninv.png")
        hp.mollview(self.g_ninv)
        plt.savefig(g_ninv_file_name)

        G1_file_name = os.path.join(dir_name,str(file_tag)+"_G1_data.png")
        hp.mollview(self.G1)
        plt.savefig(G1_file_name)

        G1_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_G1_ninv.png")
        hp.mollview(self.G1_ninv)
        plt.savefig(G1_ninv_file_name)

        G2_file_name = os.path.join(dir_name,str(file_tag)+"_G2_data.png")
        hp.mollview(self.G2)
        plt.savefig(G2_file_name)

        G2_ninv_file_name = os.path.join(dir_name,str(file_tag)+"_G2_ninv.png")
        hp.mollview(self.G2_ninv)
        plt.savefig(G2_ninv_file_name)
