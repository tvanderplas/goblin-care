
#version 330 core
out vec3 fragment_color;

in vec3 position;
in vec3 normal;
in vec3 color;
in vec2 texture_coord;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D texture;

void main()
{
	fragment_color = vec3(texture_coord, 0.0);
}
