
from os.path import dirname, realpath, join
dir_path = dirname(realpath(__file__))

with open(join(dir_path, 'ui.fs'), 'r') as shader_file:
    ui_fs = shader_file.read()
    shader_file.close()
with open(join(dir_path, 'ui.vs'), 'r') as shader_file:
    ui_vs = shader_file.read()
    shader_file.close()
with open(join(dir_path, 'light.fs'), 'r') as shader_file:
    light_fs = shader_file.read()
    shader_file.close()
with open(join(dir_path, 'light.vs'), 'r') as shader_file:
    light_vs = shader_file.read()
    shader_file.close()
with open(join(dir_path, 'object.fs'), 'r') as shader_file:
    object_fs = shader_file.read()
    shader_file.close()
with open(join(dir_path, 'object.vs'), 'r') as shader_file:
    object_vs = shader_file.read()
    shader_file.close()

cube_obj = join(dir_path, 'cube.obj')
menu_png = join(dir_path, 'menu.png')
sedan_body_obj = join(dir_path, 'sedan_body.obj')
sedan_glass_obj = join(dir_path, 'sedan_glass.obj')
sedan_tires_obj = join(dir_path, 'sedan_tires.obj')
sedan_wheels_obj = join(dir_path, 'sedan_wheels.obj')
square_obj = join(dir_path, 'square.obj')
uv_test_png = join(dir_path, 'uv_test.png')
text_image_png = join(dir_path, 'text image.png')
desert_road_png = join(dir_path, 'desert road.png')
bullet_png = join(dir_path, 'bullet.png')
green_goblin_png = join(dir_path, 'green goblin.png')
rainbow_tornado_png = join(dir_path, 'rainbow_tornado.png')
splat_png = join(dir_path, 'splat.png')
tornado_png = join(dir_path, 'tornado.png')
treasure_png = join(dir_path, 'treasure.png')
window_close_png = join(dir_path, 'window close.png')
window_close_active_png = join(dir_path, 'window close active.png')
fractal_png = join(dir_path, 'fractal.png')
pink_bubbles_png = join(dir_path, 'pink bubbles.png')
depot_png = join(dir_path, 'depot.png')
blue_squares_png = join(dir_path, 'blue squares.png')
red_gloop_png = join(dir_path, 'red gloop.png')
buy_png = join(dir_path, 'buy.png')
rainbow_bullet_png = join(dir_path, 'rainbow bullet.png')
controls_png = join(dir_path, 'controls.png')
