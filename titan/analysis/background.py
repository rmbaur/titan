import numpy as np
from libtiff import TIFF as tiff

def bkg_subtract(data, bkg_loc):
	
	bkg = tiff.open(bkg_loc, mode='r').read_image().astype('f')
	return data - bkg