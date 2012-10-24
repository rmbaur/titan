import numpy as np
from scipy.ndimage import gaussian_filter


def gauss_blur(data, blursize):
	
	blur = gaussian_filter(data, blursize)
	
	return data - blur