
//todo: use boost preprocessor and name changing to define types before include, modify ifndef, and modify functions
#ifndef __V1__GET_PIXEL__
#define __V1__GET_PIXEL__

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

int4 guardGetArray4(
    int2 pos,
    const __global uchar *edge_in,
    int4 edge_default
){{
    if(pos.x<0 || pos.y<0 || pos.x>height_in || pos.y>width_in){{
        return edge_default;
    }}
    else{{
        return (int4)(edge_in[gindex2( pos )*4], edge_in[gindex2( pos )*4+1],
            edge_in[gindex2( pos )*4+2], edge_in[gindex2( pos )*4+3]);
    }}
}}

int4 rotate4_90(
    int4 in
){{
    uint4 mask = (uint4)(2, 3, 0, 1);
    return shuffle(in, mask);
}}

int8 guardGetArray8(
    int2 pos,
    const __global uchar *edge_in,
    int8 edge_default
){{
    if(pos.x<0 || pos.y<0 || pos.x>height_in || pos.y>width_in){{
        return edge_default;
    }}
    else{{
        //return (int)(edge_in[gindex2( pos )]);
    }}
}}

#endif