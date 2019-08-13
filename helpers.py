
from random import uniform, choice
from math import atan, cos, sin, sqrt
import screen

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

def get_vector(magnitude, x1, y1, x2, y2):
	x = x1 - x2; y = y1 - y2
	hypotenuse = sqrt((x**2) + (y**2))
	normal_x = x / hypotenuse
	normal_y = y / hypotenuse
	return (normal_x * magnitude, normal_y * magnitude)

def pixel_to_view(x, y):
	vx = x / (screen.width / 2) - 1
	vy = y / (screen.height / 2) - 1
	return (vx, -vy)

def collide(entity1, entity2):
	if any([
			(entity1.box.lx < entity2.box.lx < entity1.box.ux),
			(entity1.box.lx < entity2.box.ux < entity1.box.ux),
			(entity2.box.lx < entity1.box.lx < entity2.box.ux),
			(entity2.box.lx < entity1.box.ux < entity2.box.ux)
		]) and any([
			(entity1.box.ly < entity2.box.ly < entity1.box.uy),
			(entity1.box.ly < entity2.box.uy < entity1.box.uy),
			(entity2.box.ly < entity1.box.ly < entity2.box.uy),
			(entity2.box.ly < entity1.box.uy < entity2.box.uy)
		]):
		return True
	return False

def collide_any(entity, group):
	answer = False
	for member in group:
		if collide(member, entity):
			answer = True
			break
	return answer

def get_collided(entity, group):
	answer = []
	for member in group:
		if collide(member, entity):
			answer.append(member)
	return answer

def group_collide(group1, group2, kill1:bool, kill2:bool):
	answer = []
	for entity1 in group1:
		for entity2 in group2:
			if collide(entity1, entity2):
				answer.append(entity1)
				if kill1:
					entity1.kill()
				if kill2:
					entity2.kill()
	return answer
