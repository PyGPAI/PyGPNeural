#ifndef __V1_CENTER_SURROUND__
#define __V1_CENTER_SURROUND__

#include "v1_get_pixel.cl"

int3 get_surround_square_avg(
    int2 pos,
    uint rad,
    const __global uchar* rgb_in,
    int3 rgb_default
){{
    int3 surround = 0;
    int num = 0;

    for(int i=0; i<2*rad+1; ++i){{
        int2 top = pos+(int2)(i-rad, -rad);
        int2 bot = pos+(int2)(i-rad,rad);

        surround += guardGetColor(top, rgb_in, rgb_default);
        surround += guardGetColor(bot, rgb_in, rgb_default);

        num += 2;
    }}
    for(int j=0; j<2*rad+1; ++j){{
        int2 left  = pos+(int2)(-rad, j-rad);
        int2 right = pos+(int2)(rad,j-rad);

        surround += guardGetColor(left , rgb_in, rgb_default);
        surround += guardGetColor(right, rgb_in, rgb_default);

        num += 2;
    }}
    return surround/num;
}}

int3 get_sparse_surround_square_avg(
    int2 pos,
    uint rad,
    uint skip,
    uint seed,
    const __global uchar* rgb_in,
    int3 rgb_default
){{
    int3 surround = 0;
    int num = 0;

    uint upos[2];
    upos[0] = pos.x; upos[1] = pos.y;

    float normx = fabs(normal(uint_xxhash32(upos, 2, seed), 0, rad));
    float normy = fabs(normal(uint_xxhash32(upos, 2, seed+1), 0, rad));
    float norms = fabs(normal(uint_xxhash32(upos, 2, seed+2), skip, skip>>2));

    for(int i=0; i<(rad<<1)+1; i+=skip){{
        int2 top = pos+(int2)(i-normx, -normy);
        int2 bot = pos+(int2)(i-normx,normy);

        surround += guardGetColor(top, rgb_in, rgb_default);
        surround += guardGetColor(bot, rgb_in, rgb_default);

        num += 2;
    }}
    for(int j=0; j<(rad<<1)+1; j+=skip){{
        int2 left  = pos+(int2)(-normx, j-normy);
        int2 right = pos+(int2)(normx,j-normy);

        surround += guardGetColor(left , rgb_in, rgb_default);
        surround += (int3)guardGetColor(right, rgb_in, rgb_default);

        num += 2;
    }}
    return surround/num;
}}

#endif