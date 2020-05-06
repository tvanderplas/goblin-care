
import context
import sys
from PIL import Image
import numpy as np
from assets import tornado_png, rainbow_tornado_png

find_color = [255, 255, 255, 255]
replace_color = [255, 255, 255, 0]

source = Image.open(tornado_png).convert('RGBA')
target = np.array(source)

mask = np.all(target == find_color, axis=-1)
target[mask] = replace_color
target = Image.fromarray(target)
target.save('corrected.png', 'PNG')
