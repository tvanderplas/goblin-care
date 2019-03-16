
import random
import pygame as pg
import math

def randedge(distance):
	edge = random.choice([
		[random.randint(distance, pg.display.Info().current_w - distance), distance],# top
		[random.randint(distance, pg.display.Info().current_w - distance), pg.display.Info().current_h - distance],# bottom
		[distance, random.randint(distance, pg.display.Info().current_h - distance)],# left
		[pg.display.Info().current_w - distance, random.randint(distance, pg.display.Info().current_h - distance)],# right
	])
	return edge

def moveTo(initial, final, speed):
	displacement_x = final[0] - initial[0]
	displacement_y = final[1] - initial[1]
	slope = float(displacement_y / (displacement_x if displacement_x != 0 else 1))
	inclination = math.atan(slope)
	delta_x = speed * math.cos(inclination)
	delta_y = speed * math.sin(inclination)
	return [delta_x, delta_y] if displacement_x > 0 else [-delta_x, -delta_y]
