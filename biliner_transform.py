# -*- coding: utf-8 -*-
import scipy.io.wavfile, numpy, math

cutoff = 5000.0

def main():
	# read
	samplerate, read_frames = scipy.io.wavfile.read('in.wav')
	if read_frames.ndim != 1:
		# mono only
		return

	T = 1.0/samplerate
	omega_c = 2.0*math.pi*cutoff
	b0 = math.tan(omega_c*T/2.0)/(1.0+math.tan(omega_c*T/2.0))
	b1 = math.tan(omega_c*T/2.0)/(1.0+math.tan(omega_c*T/2.0))
	a1 = (1.0-math.tan(omega_c*T/2.0))/(1.0+math.tan(omega_c*T/2.0))

	# filter
	x1, y1 = 0.0, 0.0
	write_frames = []
	for x0 in read_frames:
		y0 = b0*x0 + b1*x1 + a1*y1
		write_frames.append(y0)
		x1, y1 = x0, y0

	# write
	scipy.io.wavfile.write('biliner_transform.wav',
							samplerate,
							numpy.clip(write_frames,-2**15, 2**15-1).astype("int16"))

if __name__ == '__main__':
	main()
