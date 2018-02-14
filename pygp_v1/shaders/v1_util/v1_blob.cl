#ifndef _V1_BLOB__
#define _V1_BLOB__

#include "v1_util/v1_get_pixel.cl"
#include "v1_util/v1_center_surround.cl"

void rgb_to_blob(
    int2 coord,
    const __global uchar* rgb_in,
    const uint seed,
    __global uchar* by_out,
    __global uchar* yb_out,
    __global uchar* bw_out,
    __global uchar* rg_out,
    __global uchar* gr_out
){{
    int3 c = guardGetColor(coord, rgb_in, edge_color);

    int3 csq4 = get_sparse_surround_square_avg(coord, 4, 2, seed, rgb_in, c);

    int redVGreen = ((int)(c.y)-csq4.z);
    int greenVRed = ((int)(c.z)-csq4.y);

    int blueVYellow = ((int)(c.x)-((csq4.z + csq4.y)/2));
    int yellowVBlue = ((((int)(c.z) + (int)(c.y))/2)-csq4.x);

    int c_grey = ( c.x + c.y + c.z ) /3;
    int csq4_grey = ( csq4.x + csq4.y + csq4.z ) /3;

    int blackWhite = (c_grey-csq4_grey);

    by_out[gindex2(coord)] = (uchar)(blueVYellow+127);
    yb_out[gindex2(coord)] = (uchar)(yellowVBlue+127);
    bw_out[gindex2(coord)] = (uchar)(blackWhite+127);
    rg_out[gindex2(coord)] = (uchar)(redVGreen+127);
    gr_out[gindex2(coord)] = (uchar)(greenVRed+127);
}}

#endif