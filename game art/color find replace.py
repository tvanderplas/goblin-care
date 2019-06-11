
import sys
from PIL import Image
import numpy as np

find_color = [255, 0, 0, 255]
replace_color = [255, 255, 255, 255]

source = Image.open(sys.argv[-1])
target = np.array(source)
mask = np.all(target == find_color, axis=-1)
target[mask] = replace_color
target = Image.fromarray(target)
target.save('corrected.png', 'PNG')
