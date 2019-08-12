
from random import uniform, choice
from math import atan, cos, sin

def randedge(distance, x_min, x_max, y_min, y_max):
	edge = choice([
		[uniform(x_min + distance, x_max - distance), y_max + distance],# top
		[uniform(x_min + distance, x_max - distance), y_min - distance],# bottom
		[x_min - distance, uniform(y_min + distance, y_max - distance)],# left
		[x_max + distance, uniform(y_min + distance, y_max - distance)],# right
	])
	return edge

def moveTo(initial, final, speed):
	displacement_x = final[0] - initial[0]
	displacement_y = final[1] - initial[1]
	slope = float(displacement_y / (displacement_x if displacement_x != 0 else 1))
	inclination = atan(slope)
	delta_x = speed * cos(inclination)
	delta_y = speed * sin(inclination)
	return [delta_x, delta_y] if displacement_x > 0 else [-delta_x, -delta_y]
