
#version 150

precision mediump float;

in vec3 position;
in vec4 color;
in vec2 texture_coord;

out vec4 fragment_color;

uniform vec3 light_color;
uniform vec3 light_position;
uniform sampler2D textureObj;
uniform int texture_mode;

void main()
{
	if (texture_mode == 0) {
		fragment_color = color;
	} else {
		vec4 tex_color = texture(textureObj, texture_coord);
		if(tex_color.a == 0.0)
			discard;
		fragment_color = tex_color;
	}
}
