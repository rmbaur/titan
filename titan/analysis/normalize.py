import numpy as np


def normalize(data, reference):
	absorption = data[0] / reference[0]
	phase = data[1] - reference[1]
	try: 
		darkfield = data[2] / reference[2]
		return np.array([absorption, phase, darkfield])
	except IndexError:
		return np.array([absorption, phase])
		