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
	x1 = 0.0
	y1 = 0.0
	write_frames = numpy.zeros(read_frames.shape, 'int16')
	for n,x0 in enumerate(read_frames):
		y0 = b0*x0 + b1*x1 + a1*y1
		x1 = x0
		y1 = y0
		write_frames[n] = to_int16(y0)

	# write
	scipy.io.wavfile.write('biliner_transform.wav', samplerate, write_frames)

def to_int16(x):
	if x < -2**15:
		x = -2**15
	elif x > 2**15-1:
		x = 2**15-1
	return numpy.int16(x)

if __name__ == '__main__':
	main()
