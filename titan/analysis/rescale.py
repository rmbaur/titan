import numpy as np

def rescale(data, counts):
	
	return data / counts.reshape((-1, 1, 1))