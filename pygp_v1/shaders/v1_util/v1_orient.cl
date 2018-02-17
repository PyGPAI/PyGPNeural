#ifndef _V1_ORIENT__
#define _V1_ORIENT__

#include "v1_compass.cl"

void excite_and_inhibit_orient(
    short4* totalNeuronGroup,
    short4* inputNeuronGroup
){{
    totalNeuronGroup->x += inputNeuronGroup->x;
    totalNeuronGroup->y += inputNeuronGroup->y;
    totalNeuronGroup->z += inputNeuronGroup->z;
    totalNeuronGroup->w += inputNeuronGroup->w;
    totalNeuronGroup->x -= inputNeuronGroup->z;
    totalNeuronGroup->y -= inputNeuronGroup->w;
    totalNeuronGroup->z -= inputNeuronGroup->x;
    totalNeuronGroup->w -= inputNeuronGroup->y;
}}

void set_from_compass(
    int2 coord,
    short4* storeOrient,
    __global uchar* edge
){{
    storeOrient->x = get_north(coord,edge, edge[gindex2(coord)])     ;
    storeOrient->y = get_north_east(coord,edge, edge[gindex2(coord)]);
    storeOrient->z = get_east(coord,edge, edge[gindex2(coord)])      ;
    storeOrient->w = get_south_east(coord,edge, edge[gindex2(coord)]);
}}

void blob_to_orient(
    int2 coord,
    __global uchar* by_out,
    __global uchar* yb_out,
    __global uchar* bw_out,
    __global uchar* rg_out,
    __global uchar* gr_out,
    __global uchar* orient_out
){{
    short4 temp;
    short4 tempTemp;

    set_from_compass(coord, &temp, by_out);

    set_from_compass(coord, &tempTemp, yb_out);
    excite_and_inhibit_orient(&temp, &tempTemp);

    set_from_compass(coord, &tempTemp, bw_out);
    excite_and_inhibit_orient(&temp, &tempTemp);

    set_from_compass(coord, &tempTemp, rg_out);
    excite_and_inhibit_orient(&temp, &tempTemp);

    set_from_compass(coord, &tempTemp, gr_out);
    excite_and_inhibit_orient(&temp, &tempTemp);

    temp.x = max((short)(temp.x), (short)(0));
    temp.y = max((short)(temp.y), (short)(0));
    temp.z = max((short)(temp.z), (short)(0));
    temp.w = max((short)(temp.w), (short)(0));

    orient_out[gindex2(coord)*4+0] = min((short)(temp.x>>2),(short)(255));
    orient_out[gindex2(coord)*4+1] = min((short)(temp.y>>2),(short)(255));
    orient_out[gindex2(coord)*4+2] = min((short)(temp.z>>2),(short)(255));
    orient_out[gindex2(coord)*4+3] = min((short)(temp.w>>2),(short)(255));
}}

#endif