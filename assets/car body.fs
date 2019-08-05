
#version 330 core
out vec4 FragColor;

in vec3 position;
in vec3 normal;
in vec3 color;

uniform vec3 light_color;
uniform vec3 light_position;

void main()
{
	// ambient
	float ambientStrength = 0.1;
	vec3 ambient = ambientStrength * light_color;

	vec3 light_direction = normalize(light_position - position);
	float diff = max(dot(normal, light_direction), 0.0);
	vec3 diffuse = diff * light_color;
	vec3 result = (ambient + diffuse) * color;
	FragColor = vec4(result, 1.0);
}
