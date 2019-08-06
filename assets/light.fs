
#version 330 core
out vec4 fragment_color;

in vec3 position;
in vec3 normal;
in vec3 color;
in vec2 texture_coord;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D texture;

void main()
{
	fragment_color = vec4(color, 0.0);
}
