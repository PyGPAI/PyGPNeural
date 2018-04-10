//#include "cl_defs.h"

#include "rng.cl"

#define IMAGE_HANDLING_PARAMETERS const uint prev_res_x, const uint prev_res_y, \
                                  const uint res_x, const uint res_y, \
                                  const uint colors

#define GIVE_IMAGE_PARAMETERS prev_res_x, prev_res_y, \
                                       res_x, res_y, \
                                       colors

#define gindex3( p ) p.x*prev_res_y*colors+p.y*colors+p.z
#define gindex2( p ) p.x*prev_res_y+p.y

#define gindex3_cur( p ) p.x*res_y*colors+p.y*colors+p.z
#define gindex2_cur( p ) p.x*res_y+p.y

uchar guardGetColor(
    IMAGE_HANDLING_PARAMETERS,
    int3 pos,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    if (pos.x<0 || pos.y<0 || pos.x>prev_res_x || pos.y>prev_res_y){{
        return rgb_default;
    }}
    else{{
        return (rgb_in[gindex3( pos )]);
    }}
}}

uchar guardGetColorFloat(
    IMAGE_HANDLING_PARAMETERS,
    float2 pos, int color,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    uchar color_top_left = guardGetColor(GIVE_IMAGE_PARAMETERS,
                                         (int3)((int)(pos.x), (int)(pos.y), color),
                                         rgb_in, rgb_default);
    uchar color_top_right = guardGetColor(GIVE_IMAGE_PARAMETERS,
                                         (int3)((int)(pos.x+1), (int)(pos.y), color),
                                         rgb_in, rgb_default);
    uchar color_bottom_left = guardGetColor(GIVE_IMAGE_PARAMETERS,
                                         (int3)((int)(pos.x), (int)(pos.y+1), color),
                                         rgb_in, rgb_default);
    uchar color_bottom_right = guardGetColor(GIVE_IMAGE_PARAMETERS,
                                         (int3)((int)(pos.x+1), (int)(pos.y+1), color),
                                         rgb_in, rgb_default);

    float right_percentage = pos.x - (int)(pos.x);
    float bottom_percentage = pos.y - (int)(pos.y);

    float avg_color = ((
    (color_top_left+color_bottom_left)*(1-right_percentage) +
    (color_top_right+color_bottom_right)*right_percentage)/2 +
                      ((color_top_left+color_top_right)*(1-bottom_percentage) + (color_bottom_left+color_bottom_right)*bottom_percentage)/2)/2;

    return (uchar)(avg_color);
}}

uchar get_surround_square_avg(
    IMAGE_HANDLING_PARAMETERS,
    float2 pos, int color,
    uint rad,
    const __global uchar* rgb_in,
    uchar rgb_default
){{
    uint surround = 0;
    uint num = 0;

    for(int i=0; i<2*rad+1; ++i){{
        float2 top = pos+(float2)(i-rad,-rad);
        float2 bot = pos+(float2)(i-rad,rad);

        surround += guardGetColorFloat(GIVE_IMAGE_PARAMETERS,top, color, rgb_in, rgb_default);
        surround += guardGetColorFloat(GIVE_IMAGE_PARAMETERS,bot, color, rgb_in, rgb_default);

        num+=2;
    }}
    for(int j=1; j<2*rad; ++j){{

        float2 left = pos+(float2)(-rad,j-rad);
        float2 rigt = pos+(float2)(rad,j-rad);

        surround += guardGetColorFloat(GIVE_IMAGE_PARAMETERS,left, color, rgb_in, rgb_default);
        surround += guardGetColorFloat(GIVE_IMAGE_PARAMETERS,rigt, color, rgb_in, rgb_default);

        num+=2;

    }}
    return surround/num;
}}

/*uint get_some_surround_square_avg(
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
}}*/




__kernel void rgc(
    IMAGE_HANDLING_PARAMETERS,
    const __global uchar* rgb_in,
    __global uchar* rgb_out

#ifdef RELATIVE_COLOR_FILTER
    ,__global uchar* relative_color_out
#endif

#ifdef EDGE_FILTER
    ,__global uchar* edge_out
#endif
    )

{{
    int3 coord = (int3)(get_global_id(0), get_global_id(1), get_global_id(2));
    float2 pos = (float2)((float)(coord.x)*(float)(prev_res_x)/(float)(res_x), (float)(coord.y)*(float)(prev_res_y)/(float)(res_y));

    uchar c = guardGetColorFloat(GIVE_IMAGE_PARAMETERS,pos, coord.z, rgb_in, (uchar)(0));

    rgb_out[gindex3_cur( coord )] = c;

#ifdef EDGE_FILTER
    int2 outcoord = (int2)(get_global_id(0), get_global_id(1));

    int csq3 =get_surround_square_avg(GIVE_IMAGE_PARAMETERS,pos, coord.z, 1, rgb_in, c);
#endif

#ifdef RELATIVE_COLOR_FILTER
    int csq1 = get_surround_square_avg(GIVE_IMAGE_PARAMETERS,pos, coord.z, 1, rgb_in, c);
#endif

#ifdef EDGE_FILTER
    int edgeDiff  = max((int)(c)-csq3,(int)0)/2 ;
    int edgeDiff2 = max(csq3-(int)(c),(int)0)/2 ;
#endif

#ifdef RELATIVE_COLOR_FILTER
    int colorDiff  = max((int)(c)-csq1, (int)0)/2;
    int colorDiff2 = max(csq1-(int)(c), (int)0)/2;

    relative_color_out[gindex3_cur( coord )]
    =min(max((int)(127+((colorDiff-colorDiff2)*2

))
    , (int)0), 255);
#endif

#ifdef EDGE_FILTER
    if(get_global_id(2)==0){{
        edge_out[gindex2_cur( outcoord )] = 127;
    }}
    edge_out[gindex2_cur( outcoord )]
    =min(
        max(
            (
            (int)(edge_out[gindex2_cur( outcoord )])+(edgeDiff-edgeDiff2)*4
            ),
             0
            ),
         255
         );
#endif

#ifdef TIME_FILTER
    uint id[3];id[0]=coord.x;id[1]=coord.y;id[2]=coord.z;
    if((uint_xxhash32(id, 3, seed)&1)== 0 && c > avg_time_out[gindex3( coord )]){{
            avg_time_out[gindex3_cur( coord )]=min(max((int)(avg_time_out[gindex3( coord )]+1), (int)0), 255);;
    }}
    else if((uint_xxhash32(id, 3, seed)&1)== 0 && c < avg_time_out[gindex3( coord )]){{
        avg_time_out[gindex3_cur( coord )]=min(max((int)(avg_time_out[gindex3( coord )]-1), (int)0), 255);;;
    }}
#endif

}}