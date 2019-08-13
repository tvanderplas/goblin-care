
from random import uniform, choice
from math import sqrt
import screen
from fonts.paths import calibri_ttf
from assets.paths import text_image_png
from PIL import Image, ImageDraw, ImageFont

def text_image(size, image_color, text, text_color, text_position):
	img = Image.new('RGB', size, color = image_color)
	text_location = (size[0] * text_position, size[1] / 8)
	font_ = ImageFont.truetype(calibri_ttf, size[1] * 7 // 8)
	decoration = ImageDraw.Draw(img)
	decoration.text(text_location, text, font=font_, fill=text_color)
	img.save(text_image_png)
	return text_image_png

def randedge(distance, x_min, x_max, y_min, y_max):
	edge = choice([
		[uniform(x_min + distance, x_max - distance), y_max + distance],# top
		[uniform(x_min + distance, x_max - distance), y_min - distance],# bottom
		[x_min - distance, uniform(y_min + distance, y_max - distance)],# left
		[x_max + distance, uniform(y_min + distance, y_max - distance)],# right
	])
	return edge

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
