
import context
import sys
from PIL import Image
import numpy as np
from assets.paths import tornado_png, rainbow_tornado_png

find_color = [255, 255, 255, 255]
replace_color = [255, 255, 255, 0]

source = Image.open(tornado_png)
target = np.array(source)
if target.shape[2] == 3:
	alpha = np.array([[[255] * 112] * 100]).reshape(100, 112, 1)
	target = np.insert(target, 3, 255, axis=2)
mask = np.all(target == find_color, axis=-1)
target[mask] = replace_color
target = Image.fromarray(target)
target.save('corrected.png', 'PNG')
