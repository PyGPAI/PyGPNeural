#version 430

uniform int width;
uniform int height;
uniform int colors;
uniform int whichBuffer;
const float edgeBrightness = 0.0;

const uint RPOS   = 0;
const uint GPOS = 1;
const uint BPOS  = 2;

layout (std430, binding = 0) buffer InputBuff {
    float image[];
};

layout (std430, binding = 1) buffer InputBuff2 {
    float image2[];
};

float get_pixel_color(ivec2 pos, uint color){
    if(pos.x>width || pos.x<0){
        return edgeBrightness;
    }
    if(pos.y>height || pos.y<0){
        return edgeBrightness;
    }
    if(whichBuffer==0){
        return image[(pos.y*colors*width)+(pos.x*colors)+color];
    }else{
        return image2[(pos.y*colors*width)+(pos.x*colors)+color];
    }
}

float get_surround_square_avg(ivec2 pos, int rad, uint col){
    float surround = 0;
    float num = 0;
    for(int i=0; i<2*rad+1; ++i){
        surround += get_pixel_color(pos + ivec2(i-rad, -rad), col);
        surround += get_pixel_color(pos + ivec2(i-rad, rad), col);
        num+=2;
    }
    for(int j=1; j<2*rad; ++j){
        surround += get_pixel_color(pos + ivec2(-rad, j-rad), col);
        surround += get_pixel_color(pos + ivec2(rad, j-rad), col);
        num+=2;
    }
    return surround/num;
}

void set_pixel_color(ivec2 pos, uint color, float val){
    if(pos.x>width || pos.x<0){
        return;
    }
    if(pos.y>height || pos.y<0){
        return;
    }
    if(whichBuffer==0){
        image2[(pos.y*colors*width)+(pos.x*colors)+color] = val;
    }else{
        image[(pos.y*colors*width)+(pos.x*colors)+color] = val;
    }
}

layout (local_size_x = 1, local_size_y = 1) in;
void main() {
    ivec3 ourPos = ivec3(gl_GlobalInvocationID.xyz);
    int index = (ourPos.x*colors*height)+(ourPos.y*colors);
    int move_x = colors*height;
    int move_y = colors;
    int move_c = 1;


    //vec2 new_coord = fisheye(tex_pos, 2.0);    //rgc_dot +=

    float rsq = get_surround_square_avg(ourPos.xy, 1, RPOS);
    float r = get_pixel_color(ourPos.xy, RPOS);
    float gsq = get_surround_square_avg(ourPos.xy, 1, GPOS);
    float g = get_pixel_color(ourPos.xy, GPOS);
    float bsq = get_surround_square_avg(ourPos.xy, 1, BPOS);
    float b = get_pixel_color(ourPos.xy, BPOS);

    if( r > rsq+1){
        set_pixel_color(ourPos.xy, RPOS, r);
    }else{
        set_pixel_color(ourPos.xy, RPOS, 0);
    }

    if(g > gsq+1){
        set_pixel_color(ourPos.xy, GPOS, g);
    }else{
        set_pixel_color(ourPos.xy, GPOS, 0);
    }

    if(b > bsq+1){
        set_pixel_color(ourPos.xy, BPOS, b);
    }else{
        set_pixel_color(ourPos.xy, BPOS, 0);
    }

    //color = vec4(vec3(texelFetch(tex, ivec2(tex_pos*720), 0).bgr), 1.0);
}
