
#version 330 core
out vec4 fragment_color;

in vec3 position;
in vec3 normal;
in vec3 color;
in vec2 texture_coord;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D textureObj;

void main()
{
	// ambient
	float ambientStrength = 0.1;
	vec3 ambient = ambientStrength * light_color;

	vec3 light_direction = normalize(light_position - position);
	float diff = max(dot(normal, light_direction), 0.0);
	vec3 diffuse = diff * light_color;
	vec3 result = (ambient + diffuse) * color;
	fragment_color = texture2D(textureObj, texture_coord);
}
