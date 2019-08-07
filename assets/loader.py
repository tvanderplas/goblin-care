
from PIL import Image
from pywavefront import Wavefront

cube_obj = Wavefront('cube.obj')
light_fs = open('light.fs')
light_vs = open('light.vs')
menu_png = Image.open('menu.png')
object_fs = open('object.fs')
object_vs = open('object.vs')
sedan_body_obj = Wavefront('sedan_body.obj')
sedan_glass_obj = Wavefront('sedan_glass.obj')
square_obj = Wavefront('square.obj')
uv_test_png = Image.open('uv_test.png')
