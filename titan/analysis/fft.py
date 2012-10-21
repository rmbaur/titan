import numpy as np

def fft_fit(data, periods, perperiod):
	data = data[:periods * perperiod]
	ft = np.fft.rfft(data, axis=0)
	a0 = np.abs(ft[0] / (periods * perperiod))
	a1 = np.abs(ft[periods] * 2 / (periods * perperiod))
	phi = np.angle(ft[periods])
	return {'absorption': a0, 'darkfield': a1, 'phase': phi}