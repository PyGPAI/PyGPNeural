//#include "cl_defs.h"

#include "rng.cl"

__constant int width = {};
__constant int height = {};
__constant int colors = {};
__constant uchar edge_brightness = {};

#define gindex3( p ) p.x*width*colors+p.y*colors+p.z
#define gindex2( p ) p.x*width+p.y

uchar guardGetColor(
    int3 pos,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    if (pos.x<0 || pos.y<0 || pos.x>height || pos.y>width){{
        return rgb_default;
    }}
    else{{
        return (rgb_in[gindex3( pos )]);
    }}
}}

uchar get_surround_square_avg(
    int3 pos,
    uint rad,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    uint surround = 0;
    uint num = 0;

    for(int i=0; i<2*rad+1; ++i){{
        int3 top = pos+(int3)(i-rad,-rad,0);
        int3 bot = pos+(int3)(i-rad,rad, 0);

        surround += guardGetColor(top, rgb_in, rgb_default);
        surround += guardGetColor(bot, rgb_in, rgb_default);

        num+=2;
    }}
    for(int j=1; j<2*rad; ++j){{

        int3 left = pos+(int3)(-rad,j-rad,0);
        int3 rigt = pos+(int3)(rad,j-rad,0);

        surround += guardGetColor(left, rgb_in, rgb_default);
        surround += guardGetColor(rigt, rgb_in, rgb_default);

        num+=2;

    }}
    return surround/num;
}}

uint get_some_surround_square_avg(
    int3 pos,
    uint rad,
    uint skip,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    uint surround = 0;
    uint num = 0;

    for(int i=0; i<2*rad+1; i+=skip){{
        int3 top = pos+(int3)(i-rad,-rad,0);
        int3 bot = pos+(int3)(i-rad,rad, 0);

        surround += guardGetColor(top, rgb_in, rgb_default);
        surround += guardGetColor(bot, rgb_in, rgb_default);

        num+=2;
    }}
    for(int j=1; j<2*rad; j+=skip){{

        int3 left = pos+(int3)(-rad,j-rad,0);
        int3 rigt = pos+(int3)(rad,j-rad,0);

        surround += guardGetColor(left, rgb_in, rgb_default);
        surround += guardGetColor(rigt, rgb_in, rgb_default);

        num+=2;

    }}
    return surround/num;
}}

uint get_sparse_surround_square_avg(
    int3 pos,
    uint rad,
    uint skip,
    uint seed,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    uint surround = 0;
    uint num = 0;

    uint upos[3];
    upos[0] = pos.x ;upos[1] = pos.y; upos[2] = pos.z;


    float normx = fabs(normal(uint_xxhash32(upos, 3, seed), 0, rad));
    float normy = fabs(normal(uint_xxhash32(upos, 3, seed+1), 0, rad));
    float norms = fabs(normal(uint_xxhash32(upos, 3, seed+2), skip, skip>>2));

    for(int i=0; i<(rad<<1)+1; i+=skip){{
        int3 top = pos+(int3)(i-normx,-normy,0);
        int3 bot = pos+(int3)(i-normx,normy, 0);

        surround += guardGetColor(top, rgb_in, rgb_default);
        surround += guardGetColor(bot, rgb_in, rgb_default);

        num+=2;
    }}
    for(int j=1; j<2*rad; j+=skip){{

        int3 left = pos+(int3)(-normx,j-normy,0);
        int3 rigt = pos+(int3)(normx,j-normy,0);

        surround += guardGetColor(left, rgb_in, rgb_default);
        surround += guardGetColor(rigt, rgb_in, rgb_default);

        num+=2;

    }}
    return surround/num;
}}

__kernel void rgc(
    const __global uchar* rgb_in,
    const uint seed

#ifdef RELATIVE_COLOR_FILTER
    ,__global uchar* relative_color_out
#endif

#ifdef EDGE_FILTER
    ,__global uchar* edge_out
#endif

#ifdef TIME_FILTER
    ,__global uchar* avg_time_out
#endif

    )

{{
    int3 coord = (int3)(get_global_id(0), get_global_id(1), get_global_id(2));

#ifdef EDGE_FILTER
    int2 outcoord = (int2)(get_global_id(0), get_global_id(1));
#endif

    uchar c = guardGetColor(coord, rgb_in, edge_brightness);
#ifdef EDGE_FILTER
    int csq3 =get_surround_square_avg(coord, 1, rgb_in, c);
#endif

#ifdef RELATIVE_COLOR_FILTER
    int csq1 = get_some_surround_square_avg(coord, 1, 1, rgb_in, c);
    int csq4 = get_sparse_surround_square_avg(coord, 4, 2, seed, rgb_in, c);
    #ifdef RELATIVE_TIME_FILTER
    csq4 = (csq4 + get_sparse_surround_square_avg(coord, 4, 2, seed, avg_time_out, c)*2)/3;
    #endif
#endif

#ifdef EDGE_FILTER
    int edgeDiff  = max((int)(c)-csq3,(int)0)/2 ;
    int edgeDiff2 = max(csq3-(int)(c),(int)0)/2 ;
#endif

#ifdef RELATIVE_COLOR_FILTER
    int colorDiff  = max((int)(c)-csq4,(int)0)/2 + max((int)(c)-csq1, (int)0)/2;
    int colorDiff2 = max(csq4-(int)(c),(int)0)/2 + max(csq1-(int)(c), (int)0)/2;

    relative_color_out[gindex3( coord )]
    =min(max((int)(127+((colorDiff-colorDiff2)*2

))
    , (int)0), 255);
#endif

#ifdef EDGE_FILTER
    if(get_global_id(2)==0){{
        edge_out[gindex2( outcoord )] = 127;
    }}
    edge_out[gindex2( outcoord )]
    =min(
        max(
            (
            (int)(edge_out[gindex2( outcoord )])+(edgeDiff-edgeDiff2)*4
            ),
             0
            ),
         255
         );
#endif

#ifdef TIME_FILTER
    uint id[3];id[0]=coord.x;id[1]=coord.y;id[2]=coord.z;
    if((uint_xxhash32(id, 3, seed)&1)== 0 && c > avg_time_out[gindex3( coord )]){{
            avg_time_out[gindex3( coord )]=min(max((int)(avg_time_out[gindex3( coord )]+1), (int)0), 255);;
    }}
    else if((uint_xxhash32(id, 3, seed)&1)== 0 && c < avg_time_out[gindex3( coord )]){{
        avg_time_out[gindex3( coord )]=min(max((int)(avg_time_out[gindex3( coord )]-1), (int)0), 255);;;
    }}
#endif

}}