#include "rng.cl"

__constant int width_in = {};
__constant int height_in = {};
__constant int3 edge_color = {}; //note, will allocate for uchar4. See if you can use that empty mem for something.

#define gindex2( p ) (p.x*width_in+p.y)

int3 guardGetColor(
    int2 pos,
    const __global uchar *rgb_in,
    int3 rgb_default
){{
    if(pos.x<0 || pos.y<0 || pos.x>height_in || pos.y>width_in){{
        return rgb_default;
    }}
    else{{
        return (int3)(rgb_in[gindex2( pos )*3], rgb_in[gindex2( pos )*3+1], rgb_in[gindex2( pos )*3+2]);
    }}
}}

int guardGetEdge(
    int2 pos,
    const __global uchar *edge_in,
    int edge_default
){{
    if(pos.x<0 || pos.y<0 || pos.x>height_in || pos.y>width_in){{
        return edge_default;
    }}
    else{{
        return (int)(edge_in[gindex2( pos )]);
    }}
}}

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

int get_north(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 west  = pos+(int2)(-1, 0);
    int2 east = pos+(int2)( 1, 0);

    int w = guardGetEdge(west , edge_in, edge_default);
    int e = guardGetEdge(east , edge_in, edge_default);
    return abs(w-e);
}}

int get_north_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 nw_pos = pos+(int2)(-1, -1);
    int2 se_os  = pos+(int2)( 1, 1);

    int nw = guardGetEdge(nw_pos , edge_in, edge_default);
    int se = guardGetEdge(se_os , edge_in, edge_default);
    return abs(nw-se);
}}

int get_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 n_pos = pos+(int2)( 0,-1);
    int2 s_pos = pos+(int2)( 0, 1);

    int n = guardGetEdge(n_pos , edge_in, edge_default);
    int s = guardGetEdge(s_pos , edge_in, edge_default);
    return abs(n-s);
}}

int get_south_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 ne_pos = pos+(int2)(1, -1);
    int2 sw_os  = pos+(int2)( -1, 1);

    int ne = guardGetEdge(ne_pos , edge_in, edge_default);
    int sw = guardGetEdge(sw_os , edge_in, edge_default);
    return abs(ne-sw);
}}

int get_north_sparse(
    int2 pos,
    int sparsity,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 west  = pos+(int2)(-sparsity, 0);
    int2 east = pos+(int2)( sparsity, 0);

    int w = guardGetEdge(west , edge_in, edge_default);
    int e = guardGetEdge(east , edge_in, edge_default);
    return abs(w-e);
}}

int get_north_east_sparse(
    int2 pos,
    int sparsity,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 nw_pos = pos+(int2)(-sparsity, -sparsity);
    int2 se_os  = pos+(int2)( sparsity, sparsity);

    int nw = guardGetEdge(nw_pos , edge_in, edge_default);
    int se = guardGetEdge(se_os , edge_in, edge_default);
    return abs(nw-se);
}}

int get_east_sparse(
    int2 pos,
    int sparsity,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 n_pos = pos+(int2)( 0,-sparsity);
    int2 s_pos = pos+(int2)( 0, sparsity);

    int n = guardGetEdge(n_pos , edge_in, edge_default);
    int s = guardGetEdge(s_pos , edge_in, edge_default);
    return abs(n-s);
}}

int get_south_east_sparse(
    int2 pos,
    int sparsity,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 ne_pos = pos+(int2)(sparsity, -sparsity);
    int2 sw_os  = pos+(int2)( -sparsity, sparsity);

    int ne = guardGetEdge(ne_pos , edge_in, edge_default);
    int sw = guardGetEdge(sw_os , edge_in, edge_default);
    return abs(ne-sw);
}}

/*short4 compass_team_fight(int2 pos,
                        __global short* orient

){{
    short4 ret = (short4)(0);

    __constant float addVal = 8;
    __constant float subVal = 2;

    for(int i=0; i<5; ++i){{
        int2 top = pos+(int2)(i-2,-2);
        int2 bot = pos+(int2)(i-2, 2);

        for(int k=0; k<4; ++k){{
            ret.x+=orient[gindex2(top)*4+0]*((k==0)?addVal:-subVal*((k==2)?subVal:1.0));
            ret.y+=orient[gindex2(top)*4+1]*((k==1)?addVal:-subVal*((k==3)?subVal:1.0));
            ret.z+=orient[gindex2(top)*4+2]*((k==2)?addVal:-subVal*((k==0)?subVal:1.0));
            ret.w+=orient[gindex2(top)*4+3]*((k==3)?addVal:-subVal*((k==1)?subVal:1.0));

            ret.x+=orient[gindex2(bot)*4+0]*((k==0)?addVal:-subVal*((k==2)?subVal:1.0));;
            ret.y+=orient[gindex2(bot)*4+1]*((k==1)?addVal:-subVal*((k==3)?subVal:1.0));
            ret.z+=orient[gindex2(bot)*4+2]*((k==2)?addVal:-subVal*((k==0)?subVal:1.0));
            ret.w+=orient[gindex2(bot)*4+3]*((k==3)?addVal:-subVal*((k==1)?subVal:1.0));
        }}
    }}

    for(int i=0; i<3; ++i){{
        int2 left  = pos+(int2)(-2, i-2);
        int2 right = pos+(int2)(2,i-2);

        for(int k=0; k<4; ++k){{
            ret.x+=orient[gindex2(left)*4+0]*((k==0)?addVal:-subVal*((k==2)?subVal:1.0));
            ret.y+=orient[gindex2(left)*4+1]*((k==1)?addVal:-subVal*((k==3)?subVal:1.0));
            ret.z+=orient[gindex2(left)*4+2]*((k==2)?addVal:-subVal*((k==0)?subVal:1.0));
            ret.w+=orient[gindex2(left)*4+3]*((k==3)?addVal:-subVal*((k==1)?subVal:1.0));

            ret.x+=orient[gindex2(right)*4+0]*((k==0)?addVal:-subVal*((k==2)?subVal:1.0));
            ret.y+=orient[gindex2(right)*4+1]*((k==1)?addVal:-subVal*((k==3)?subVal:1.0));
            ret.z+=orient[gindex2(right)*4+2]*((k==2)?addVal:-subVal*((k==0)?subVal:1.0));
            ret.w+=orient[gindex2(right)*4+3]*((k==3)?addVal:-subVal*((k==1)?subVal:1.0));
        }}
    }}

    return ret;
}}*/

__kernel void blob(
    const __global uchar* rgb_in,
    const uint seed,
    __global uchar* by_out,
    __global uchar* yb_out,
    __global uchar* bw_out,
    __global uchar* rg_out,
    __global uchar* gr_out,
    __global short* orient_out,
    __global uchar* orient_dbg_out
){{
    int2 coord = (int2)(get_global_id(0), get_global_id(1));

    int3 c = guardGetColor(coord, rgb_in, edge_color);

    int3 csq1 = get_surround_square_avg(coord, 1, rgb_in, c);

    int3 csq4 = get_sparse_surround_square_avg(coord, 4, 2, seed, rgb_in, c);

    int redVGreen = ((int)(c.y)-csq4.z);
    int greenVRed = ((int)(c.z)-csq4.y);
    //int redGreen  = (greenVRed + redVGreen)/2;

    int blueVYellow = ((int)(c.x)-((csq4.z + csq4.y)/2));
    int yellowVBlue = ((((int)(c.z) + (int)(c.y))/2)-csq4.x);
    //int blueYellow  = (blueVYellow + yellowVBlue)/2;

    int c_grey = ( c.x + c.y + c.z ) /3;
    int csq1_grey = ( csq1.x + csq1.y + csq1.z ) /3;
    int csq4_grey = ( csq4.x + csq4.y + csq4.z ) /3;

    int blackWhite = (c_grey-csq4_grey + c_grey - csq1_grey)/2;

    by_out[gindex2(coord)] = (uchar)(blueVYellow+127);
    yb_out[gindex2(coord)] = (uchar)(yellowVBlue+127);
    bw_out[gindex2(coord)] = (uchar)(blackWhite+127);
    rg_out[gindex2(coord)] = (uchar)(redVGreen+127);
    gr_out[gindex2(coord)] = (uchar)(greenVRed+127);

    orient_out[gindex2(coord)*4+0] = get_north(coord,by_out, by_out[gindex2(coord)])     ;
    orient_out[gindex2(coord)*4+1] = get_north_east(coord,by_out, by_out[gindex2(coord)]);
    orient_out[gindex2(coord)*4+2] = get_east(coord,by_out, by_out[gindex2(coord)])      ;
    orient_out[gindex2(coord)*4+3] = get_south_east(coord,by_out, by_out[gindex2(coord)]);

    short4 temp;


    temp.x = get_north(coord,yb_out, yb_out[gindex2(coord)])     ;
    temp.y = get_north_east(coord,yb_out, yb_out[gindex2(coord)]);
    temp.z = get_east(coord,yb_out, yb_out[gindex2(coord)])      ;
    temp.w = get_south_east(coord,yb_out, yb_out[gindex2(coord)]);

    orient_out[gindex2(coord)*4+0] += temp.x;
    orient_out[gindex2(coord)*4+1] += temp.y;
    orient_out[gindex2(coord)*4+2] += temp.z;
    orient_out[gindex2(coord)*4+3] += temp.w;
    orient_out[gindex2(coord)*4+0] -= temp.z;
    orient_out[gindex2(coord)*4+1] -= temp.w;
    orient_out[gindex2(coord)*4+2] -= temp.x;
    orient_out[gindex2(coord)*4+3] -= temp.y;

    temp.x = get_north(coord,bw_out, bw_out[gindex2(coord)])     ;
    temp.y = get_north_east(coord,bw_out, bw_out[gindex2(coord)]);
    temp.z = get_east(coord,bw_out, bw_out[gindex2(coord)])      ;
    temp.w = get_south_east(coord,bw_out, bw_out[gindex2(coord)]);
    orient_out[gindex2(coord)*4+0] += temp.x;
    orient_out[gindex2(coord)*4+1] += temp.y;
    orient_out[gindex2(coord)*4+2] += temp.z;
    orient_out[gindex2(coord)*4+3] += temp.w;
    orient_out[gindex2(coord)*4+0] -= temp.z;
    orient_out[gindex2(coord)*4+1] -= temp.w;
    orient_out[gindex2(coord)*4+2] -= temp.x;
    orient_out[gindex2(coord)*4+3] -= temp.y;

    temp.x = get_north(coord,rg_out, rg_out[gindex2(coord)])     ;
    temp.y = get_north_east(coord,rg_out, rg_out[gindex2(coord)]);
    temp.z = get_east(coord,rg_out, rg_out[gindex2(coord)])      ;
    temp.w = get_south_east(coord,rg_out, rg_out[gindex2(coord)]);

    orient_out[gindex2(coord)*4+0] += temp.x;
    orient_out[gindex2(coord)*4+1] += temp.y;
    orient_out[gindex2(coord)*4+2] += temp.z;
    orient_out[gindex2(coord)*4+3] += temp.w;
    orient_out[gindex2(coord)*4+0] -= temp.z;
    orient_out[gindex2(coord)*4+1] -= temp.w;
    orient_out[gindex2(coord)*4+2] -= temp.x;
    orient_out[gindex2(coord)*4+3] -= temp.y;

    temp.x = get_north(coord,gr_out, gr_out[gindex2(coord)])     ;
    temp.y = get_north_east(coord,gr_out, gr_out[gindex2(coord)]);
    temp.z = get_east(coord,gr_out, gr_out[gindex2(coord)])      ;
    temp.w = get_south_east(coord,gr_out, gr_out[gindex2(coord)]);

    orient_out[gindex2(coord)*4+0] += temp.x;
    orient_out[gindex2(coord)*4+1] += temp.y;
    orient_out[gindex2(coord)*4+2] += temp.z;
    orient_out[gindex2(coord)*4+3] += temp.w;
    orient_out[gindex2(coord)*4+0] -= temp.z;
    orient_out[gindex2(coord)*4+1] -= temp.w;
    orient_out[gindex2(coord)*4+2] -= temp.x;
    orient_out[gindex2(coord)*4+3] -= temp.y;

    for(int k=0; k<4;++k){{
    if (orient_out[gindex2(coord)*4+k]<0){{
    orient_out[gindex2(coord)*4+k]=0;
    }}
    }}

    //orientation of line, 0-252
    orient_dbg_out[gindex2(coord)*3+0] = (
                                         0+
                                         orient_out[gindex2(coord)*4+1]*85+
                                         orient_out[gindex2(coord)*4+2]*170+
                                         orient_out[gindex2(coord)*4+3]*255
                                        )
                                                        /
                                        (
                                         orient_out[gindex2(coord)*4+0] +
                                         orient_out[gindex2(coord)*4+1] +
                                         orient_out[gindex2(coord)*4+2] +
                                         orient_out[gindex2(coord)*4+3]
                                         );

    //std dev of line, approx
    orient_dbg_out[gindex2(coord)*3+1] =
                                        (
                                        abs(orient_out[gindex2(coord)*4+0]-orient_out[gindex2(coord)*4+1])+
                                        abs(orient_out[gindex2(coord)*4+1]-orient_out[gindex2(coord)*4+2])+
                                        abs(orient_out[gindex2(coord)*4+2]-orient_out[gindex2(coord)*4+3])+
                                        abs(orient_out[gindex2(coord)*4+3]-orient_out[gindex2(coord)*4+0])
                                        )/4;

    //prominence of line
    orient_dbg_out[gindex2(coord)*3+2] = (orient_out[gindex2(coord)*4+0] +
                                          orient_out[gindex2(coord)*4+1] +
                                          orient_out[gindex2(coord)*4+2] +
                                          orient_out[gindex2(coord)*4+3] )/4;

}}