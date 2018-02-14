#include "rng.cl"

__constant int width_in = {};
__constant int height_in = {};
__constant int3 edge_color = {}; //note, will allocate for uchar4. See if you can use that empty mem for something.
__constant int sparsity = 1;

#include "v1_util/v1_get_pixel.cl"
#include "v1_util/v1_center_surround.cl"
#include "v1_util/v1_compass.cl"
#include "v1_util/v1_blob.cl"
#include "v1_util/v1_orient.cl"
#include "v1_util/v1_orient_group.cl"
#include "v1_util/v1_debug.cl"

__kernel void blob(
    const __global uchar* rgb_in,
    const uint seed,
    __global uchar* by_out,
    __global uchar* yb_out,
    __global uchar* bw_out,
    __global uchar* rg_out,
    __global uchar* gr_out,
    __global uchar* orient_out,
    __global uchar* orient_group_out,
    __global uchar* orient_dbg_out
){{
    int2 coord = (int2)(get_global_id(0), get_global_id(1));

    rgb_to_blob(
        coord,
        rgb_in,
        seed,
        by_out,
        yb_out,
        bw_out,
        rg_out,
        gr_out
    );


    blob_to_orient(
        coord,
        by_out,
        yb_out,
        bw_out,
        rg_out,
        gr_out,
        orient_out
    );

    orient_to_orient_group(coord, orient_out, orient_group_out);

    orient_dbg(
        coord,
        orient_group_out,
        orient_dbg_out
    );

}}