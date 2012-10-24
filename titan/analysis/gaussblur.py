import numpy as np
from scipy.ndimage import gaussian_filter


def gauss_blur(data, blursize):
	
	for i in range(len(data)):
		blur = gaussian_filter(data[i], blursize)
		data[i] -= blur
		
	return data