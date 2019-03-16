
from random import randint, choice
import pygame as pg
from math import atan, cos, sin

def randedge(distance):
	edge = choice([
		[randint(distance, pg.display.Info().current_w - distance), distance],# top
		[randint(distance, pg.display.Info().current_w - distance), pg.display.Info().current_h - distance],# bottom
		[distance, randint(distance, pg.display.Info().current_h - distance)],# left
		[pg.display.Info().current_w - distance, randint(distance, pg.display.Info().current_h - distance)],# right
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
