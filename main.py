# scroll down to the "if __name__ == '__main__':" bit to change parameters

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

GRAVITY = -9.81


# does the math and returns height and velocity for each time
def simulate(height0, t, grav=GRAVITY, v0=0):
	h = (np.square(t) * grav / 2) + (v0 * t) + height0
	vel = grav * t + v0
	return h, vel


# calculates kinetic energy
def kineticEnergy(mass, vel):
	return mass * np.square(vel) / 2


# calculates grav potential energy
def gravPotEnergy(mass, h, grav=GRAVITY):
	return mass * h * abs(grav)


# predicts impact so we know how many times we need to simulate
def predictImpact(h, v=0, g=GRAVITY):
	# oh boy here comes some math... i think quadratic formula is the way to go...
	# ax^2 + bx + c = 0
	# a would = g/2, buuuut since we are multiplying later, we can just divide the coefficients by 2
	# this saves us 2 operations
	# b = v
	# c = h

	radicalBoi = sqrt(v ** 2 - (2 * g * h))
	pBoi = (-v + radicalBoi)/g
	mBoi = (-v - radicalBoi)/g

	return max(pBoi, mBoi)


if __name__ == '__main__':
	m = 1 # mass in kg
	height = 42 # drop height
	dT = 1/200 # how big each time-step is (in seconds)

	dur = predictImpact(height)

	# setup what times the simulation is ran for
	times = np.arange(0, dur, dT)
	times = np.append(times, dur/2) # add the half way point
	times = np.sort(times)
	times = np.unique(times) # make sure there are no duplicates

	# all the math
	alt, vel = simulate(height, times)
	ke = kineticEnergy(m, vel)
	pe = gravPotEnergy(m, alt)
	total = ke + pe

	"""
	print("ke------------------")
	print(ke)
	print("pe------------------")
	print(pe)
	"""
	print("variance in total energy: " + str(np.max(total) - np.min(total)))

	# find all the important info for middle time
	index = np.where(times == dur/2)[0] # makes sure only get 1 index if a duplicate snuck through the np.unique()
	print("ke:     " + str(ke[index]))
	print("pe:     " + str(pe[index]))
	print("height: " + str(alt[index]))

	# plot lines
	plt.plot(times, ke, label="kinetic energy")
	plt.plot(times, pe, label="potential energy")
	plt.plot(times, total, label="total energy")
	plt.plot([dur/2, dur/2], [0, np.max(total)], label="halftime line")
	plt.legend()
	plt.show()
