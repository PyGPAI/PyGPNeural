#ifndef __V1_COMPASS_CL__
#define __V1_COMPASS_CL__

#include "v1_center_surround.cl"

int get_north(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 west  = pos+(int2)(-sparsity, 0);
    int2 east = pos+(int2)( sparsity, 0);

    int w = guardGetEdge(west , edge_in, edge_default);
    int c = guardGetEdge(pos, edge_in, edge_default);
    int e = guardGetEdge(east , edge_in, edge_default);
    return abs(w-c + e-c);
}}

int get_north_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 nw_pos = pos+(int2)(-sparsity, -sparsity);
    int2 se_os  = pos+(int2)( sparsity, sparsity);

    int nw = guardGetEdge(nw_pos , edge_in, edge_default);
    int c = guardGetEdge(pos, edge_in, edge_default);
    int se = guardGetEdge(se_os , edge_in, edge_default);
    return abs(nw-c + se-c);
}}

int get_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 n_pos = pos+(int2)( 0,-sparsity);
    int2 s_pos = pos+(int2)( 0, sparsity);

    int n = guardGetEdge(n_pos , edge_in, edge_default);
    int c = guardGetEdge(pos, edge_in, edge_default);
    int s = guardGetEdge(s_pos , edge_in, edge_default);
    return abs(n-c + s-c);
}}

int get_south_east(
    int2 pos,
    const __global uchar* edge_in,
    int edge_default
){{
    int2 ne_pos = pos+(int2)(sparsity, -sparsity);
    int2 sw_os  = pos+(int2)( -sparsity, sparsity);

    int ne = guardGetEdge(ne_pos , edge_in, edge_default);
    int c = guardGetEdge(pos, edge_in, edge_default);
    int sw = guardGetEdge(sw_os , edge_in, edge_default);
    return abs(ne-c + sw-c);
}}

#endif