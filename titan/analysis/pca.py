"""
This method computes DPC values according to the algorithm defined in

J Xu, W Jin, L Chai, Q Xu, "Phase extraction from randomly phase-shifted 
interferograms by combining principal component analysis and least squares method",
Optics Express 19 (21) 2011

"""

import numpy as np
import matplotlib.mlab as mlab


def pca_fit(data):
	
	# Access the data from the Dataset proxy as a numpy array
	data = data[:]
	
	means = np.mean(data, axis=0)
	
	# Put the data into the shape required by the PCA implementation
	# but keep track of the shape for later
	shape = data.shape
	data = (data.reshape((data.shape[0], -1))).T
	
	pcadata = mlab.PCA(data)
	
	phi = np.arctan2(pcadata.Y[:, 0], pcadata.Y[:, 1])
	phi = phi.reshape((shape[1], shape[2]))
	
	return np.array([means, phi])