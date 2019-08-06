
#version 330 core
layout (location = 0) in vec2 vertex_texture_coord;
layout (location = 1) in vec3 vertex_normal;
layout (location = 2) in vec3 vertex_position;

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
	position = vec3(model * vec4(vertex_position, 1.0));
	normal = normalize(mat3(transpose(inverse(model))) * vertex_normal);
	color = self_color;
	texture_coord = vertex_texture_coord;
}
