
#version 150

precision mediump float;

in vec3 position;
in vec3 normal;
in vec4 color;
in vec2 texture_coord;

out vec4 fragment_color;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D textureObj;
uniform int texture_mode;

void main()
{
	// ambient
	float ambientStrength = 0.1;
	vec3 ambient = ambientStrength * light_color;

	// diffuse
	vec3 light_direction = normalize(light_position - position);
	float diff = max(dot(normal, light_direction), 0.0);
	vec3 diffuse = diff * light_color;

	if (texture_mode == 0) {
		vec4 diffuse_color = vec4(ambient + diffuse, 1.0) * color;
		fragment_color = diffuse_color;
	} else {
		vec4 tex_color = texture(textureObj, texture_coord);
		if(tex_color.a == 0.0)
			discard;
		fragment_color = vec4(ambient + diffuse, 1.0) * tex_color;
	}
}
