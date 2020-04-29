
#version 150

precision mediump float;

out vec4 fragment_color;

in vec3 position;
in vec3 normal;
in vec4 color;
in vec2 texture_coord;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D textureObj;
uniform int texture_mode;

void main()
{
	// ambient
	float ambientStrength = 0.1;
	vec3 ambient = ambientStrength * light_color;

	vec3 light_direction = normalize(light_position - position);
	float diff = max(dot(normal, light_direction), 0.0);
	vec3 diffuse = diff * light_color;
	vec4 result = vec4(ambient + diffuse, 1.0) * color;
	if (texture_mode == 0) {
		fragment_color = result;
	} else {
		vec4 tex_color = texture(textureObj, texture_coord);
		if(tex_color.a == 0.0)
			discard;
		fragment_color = texture(textureObj, texture_coord);
	}
}
