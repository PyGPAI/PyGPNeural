//#include "cl_defs.h"

//#define UNSAFE_MODE



__constant int width = {};
__constant int height = {};
__constant int colors = {};
__constant float edge_brightness = {};

#define gindex3( p ) p.x*width*colors+p.y*colors+p.z

uint guardGetColor(
    int3 pos,
    const __global uint* rgb_in
){{
    if (pos.x<0 || pos.y<0 || pos.x>height || pos.y>width){{
        return edge_brightness;
    }}
    else{{
        return (rgb_in[gindex3( pos )]);
    }}
}}

uint get_surround_square_avg(
    int3 pos,
    uint rad,
    const __global uint* rgb_in
){{
    uint surround = 0;
    uint num = 0;

    for(int i=0; i<2*rad+1; ++i){{
        int3 top = pos+(int3)(i-rad,-rad,0);
        int3 bot = pos+(int3)(i-rad,rad, 0);

        surround += guardGetColor(top, rgb_in);
        surround += guardGetColor(bot, rgb_in);

        num+=2;
    }}
    for(int j=1; j<2*rad; ++j){{

        int3 left = pos+(int3)(-rad,j-rad,0);
        int3 rigt = pos+(int3)(rad,j-rad,0);

        surround += guardGetColor(left, rgb_in);
        surround += guardGetColor(rigt, rgb_in);

        num+=2;

    }}
    return surround/num;
}}

// todo: pass in uint 32 values. Use bit masking and keep track of mod 4 to work on individual uint8s
// todo: pass in random seed and use it w/ global values to determine radius for current pixel
// todo: add exhaustion arrays in, replace +5 with them.
__kernel void rgc(
    const __global uint* rgb_in,
    __global uint* rgc_out)
{{
    int3 coord = (int3)(get_global_id(0), get_global_id(1), get_global_id(2));

    uint csq1 = get_surround_square_avg(coord, 1, rgb_in);

    uint c = guardGetColor(coord, rgb_in);

    //rgc_out[gindex3( coord )] = 0;

    if( c > csq1+5){{
        rgc_out[gindex3( coord )] = 255;
    }}
    else{{
        rgc_out[gindex3( coord )] = 0;
    }}


}}