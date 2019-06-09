
import sys
from PIL import Image
import numpy as np

source = Image.open(sys.argv[-1])
target = np.array(source)
target[target > 230] = 255
target = Image.fromarray(target)
target.save('corrected.png', 'PNG')
