
#version 150

precision mediump float;

in vec2 vertex_texture_coord;
in vec3 vertex_normal;
in vec3 vertex_position;

out vec3 position;
out vec3 normal;
out vec3 color;
out vec2 texture_coord;

uniform mat4 transform;
uniform mat4 model;
uniform vec3 self_color;

void main()
{
	gl_Position = transform * vec4(vertex_position, 1.0);
	position = vec3(transform * vec4(vertex_position, 1.0));
	normal = vertex_normal;
	color = self_color;
	texture_coord = vertex_texture_coord;
}
