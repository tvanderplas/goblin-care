
from random import randint, choice
from math import atan, cos, sin

def randedge(distance, screen_width, screen_height):
	edge = choice([
		[randint(distance, screen_width - distance), distance],# top
		[randint(distance, screen_width - distance), screen_height - distance],# bottom
		[distance, randint(distance, screen_height - distance)],# left
		[screen_width - distance, randint(distance, screen_height - distance)],# right
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
