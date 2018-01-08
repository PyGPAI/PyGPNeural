//#include "cl_defs.h"

//#define UNSAFE_MODE

#define gindex3( p , w, h, d) (p.x*w*d)+(p.y*d)+p.z
#define sindex3( p , w, h, d) (p.x*w*d)+(p.y*d)+p.z

__constant int width = {};
__constant int height = {};
__constant int colors = {};

const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST;

enum colorEnum{{
    red,
    green,
    blue
}};

inline uint getColor(uint4 pixel, int color){{
    switch(color){{
        case red:
            return pixel.x;
        case green:
            return pixel.y;
        case blue:
            return pixel.z;
        default:
            return pixel.w;
    }}
}}

__constant float edge_brightness = {};

/*get_pixel_color: gets pixel color value
    pos.x: horizontal position
    pos.y: vertical position
    pos.z: 0:red, 1:green, 2:blue
    rgb_in: color input
*/


float get_surround_square_avg(
    int2 pos,
    uint rad,
    read_only image2d_t rgb_in,
    int color
){{
    float surround = 0;
    float num = 0;

    for(int i=0; i<2*rad+1; ++i){{
        int2 left = pos+(int2)(i-rad,-rad);
        int2 right =pos+(int2)(i-rad,rad);
        /*if(left>0 && left<width){{

        }}*/

        surround += getColor(read_imageui(rgb_in, sampler, pos+(int2)(i-rad,rad)),color);
        num+=2;
    }}
    for(int j=1; j<2*rad; ++j){{
        surround += getColor(read_imageui(rgb_in, sampler, pos+(int2)(-rad,j-rad)),color);
        surround += getColor(read_imageui(rgb_in, sampler, pos+(int2)(rad,j-rad)),color);
        num+=2;
    }}
    return surround/num;
}}


__kernel void rgc(
    const __global uint8* rgb_in,
    __global uint8* rgc_out)
{{
    uint3 coord = (uint3)(get_global_id(0), get_global_id(1), get_global_id(2));

    /*float rsq = 0;
    float r = getColor(read_imageui(rgb_in, sampler, coord),red);
    float gsq = 200;
    float g = getColor(read_imageui(rgb_in, sampler, coord),green);
    float bsq = 5;
    float b = getColor(read_imageui(rgb_in, sampler, coord),blue);*/

    //uint4 colorOut = (0,128,0,255);

    /*if( r > rsq+1){{
        colorOut.x = 255;
    }}

    if(g > gsq+1){{
        colorOut.y = 255;
    }}

    if(b > bsq+1){{
        colorOut.z = 255;
    }}*/
    //rgc_out[coord.y*height*colors+coord.x*colors + coord.z] = rgb_in[coord.y*height*colors+coord.x*colors + coord.z]/2;

    rgc_out[coord.x] = 255;
    //write_imageui(rgc_out, coord, colorOut);
}}