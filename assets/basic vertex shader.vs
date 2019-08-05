
#version 330 core
layout (location = 0) in vec2 texture_coord;
layout (location = 1) in vec3 vertex_normal;
layout (location = 2) in vec3 vertex_position;

out vec3 position;
out vec3 normal;
out vec3 color;

uniform mat4 transform;
uniform mat4 model;

void main()
{
	gl_Position = transform * vec4(vertex_position, 1.0);
	position = vec3(transform * vec4(vertex_position, 1.0));
	normal = vertex_normal;
	color = vec3(0.5, 0.5, 0.5);
}
