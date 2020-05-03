
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
