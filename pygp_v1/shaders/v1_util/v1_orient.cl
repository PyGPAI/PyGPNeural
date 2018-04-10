#ifndef _V1_ORIENT__
#define _V1_ORIENT__

#include "v1_compass.cl"

void excite_and_inhibit_orient(
    short4* totalNeuronGroup,
    short4* inputNeuronGroup
){{
    totalNeuronGroup->x = min(totalNeuronGroup->x + inputNeuronGroup->x, 255<<2);
    totalNeuronGroup->y = min(totalNeuronGroup->y + inputNeuronGroup->y, 255<<2);
    totalNeuronGroup->z = min(totalNeuronGroup->z + inputNeuronGroup->z, 255<<2);
    totalNeuronGroup->w = min(totalNeuronGroup->w + inputNeuronGroup->w, 255<<2);
    totalNeuronGroup->x = max(totalNeuronGroup->x-inputNeuronGroup->z,0);
    totalNeuronGroup->y = max(totalNeuronGroup->y-inputNeuronGroup->w,0);
    totalNeuronGroup->z = max(totalNeuronGroup->z-inputNeuronGroup->x,0);
    totalNeuronGroup->w = max(totalNeuronGroup->w-inputNeuronGroup->y,0);
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

    orient_out[gindex2(coord)*4+0] = min((short)(temp.x),(short)(255));
    orient_out[gindex2(coord)*4+1] = min((short)(temp.y),(short)(255));
    orient_out[gindex2(coord)*4+2] = min((short)(temp.z),(short)(255));
    orient_out[gindex2(coord)*4+3] = min((short)(temp.w),(short)(255));
}}


int4 get_oriented_surround_square_avg(
    int2 pos,
    int rad,
    const __global uchar* orient_in,
    int4 orient_default
){{
    int4 surround = orient_default;
    int num = 1;

    for(int i=0; i<2*rad+1; ++i){{
        int2 top = pos+(int2)(i-rad, -rad);
        int2 bot = pos+(int2)(i-rad,rad);

        int2 d = top - pos;


        int4 tg = guardGetArray4(top, orient_in, orient_default);
        surround.x = surround.x - abs(d.x)*tg.x + abs(d.x)*tg.z
                                + abs(d.y)*tg.x - abs(d.y)*tg.z;
        surround.y = surround.y - abs((d.x-d.y)/2)*tg.y + abs((d.x-d.y)/2)*tg.w
                                + abs((d.x+d.y)/2)*tg.y - abs((d.x-d.y)/2)*tg.w;
        surround.z = surround.z + abs(d.x)*tg.z - abs(d.x)*tg.x
                                - abs(d.y)*tg.z + abs(d.y)*tg.x;
        surround.w = surround.w + abs((d.x-d.y)/2)*tg.w - abs((d.x-d.y)/2)*tg.y
                                - abs((d.x+d.y)/2)*tg.w + abs((d.x-d.y)/2)*tg.y;

        d = bot - pos;
        int4 bg = guardGetArray4(top, orient_in, orient_default);
        surround.x = surround.x - abs(d.x)*bg.x + abs(d.x)*bg.z
                                + abs(d.y)*bg.x - abs(d.y)*bg.z;
        surround.y = surround.y - abs((d.x-d.y)/2)*bg.y + abs((d.x-d.y)/2)*bg.w
                                + abs((d.x+d.y)/2)*bg.y - abs((d.x-d.y)/2)*bg.w;
        surround.z = surround.z + abs(d.x)*bg.z - abs(d.x)*bg.x
                                - abs(d.y)*bg.z + abs(d.y)*bg.x;
        surround.w = surround.w + abs((d.x-d.y)/2)*bg.w - abs((d.x-d.y)/2)*bg.y
                                - abs((d.x+d.y)/2)*bg.w + abs((d.x-d.y)/2)*bg.y;

        num += 2;
    }}
    for(int j=0; j<2*rad+1; ++j){{
        int2 left  = pos+(int2)(-rad, j-rad);
        int2 right = pos+(int2)(rad,j-rad);

        int2 d = left - pos;

        int4 tg = guardGetArray4(left, orient_in, orient_default);
        surround.x = surround.x - abs(d.x)*tg.x + abs(d.x)*tg.z
                                + abs(d.y)*tg.x - abs(d.y)*tg.z;
        surround.y = surround.y - abs((d.x-d.y)/2)*tg.y + abs((d.x-d.y)/2)*tg.w
                                + abs((d.x+d.y)/2)*tg.y - abs((d.x-d.y)/2)*tg.w;
        surround.z = surround.z + abs(d.x)*tg.z - abs(d.x)*tg.x
                                - abs(d.y)*tg.z + abs(d.y)*tg.x;
        surround.w = surround.w + abs((d.x-d.y)/2)*tg.w - abs((d.x-d.y)/2)*tg.y
                                - abs((d.x+d.y)/2)*tg.w + abs((d.x-d.y)/2)*tg.y;

        d = right - pos;
        int4 bg = guardGetArray4(right, orient_in, orient_default);
        surround.x = surround.x - abs(d.x)*bg.x + abs(d.x)*bg.z
                                + abs(d.y)*bg.x - abs(d.y)*bg.z;
        surround.y = surround.y - abs((d.x-d.y)/2)*bg.y + abs((d.x-d.y)/2)*bg.w
                                + abs((d.x+d.y)/2)*bg.y - abs((d.x-d.y)/2)*bg.w;
        surround.z = surround.z + abs(d.x)*bg.z - abs(d.x)*bg.x
                                - abs(d.y)*bg.z + abs(d.y)*bg.x;
        surround.w = surround.w + abs((d.x-d.y)/2)*bg.w - abs((d.x-d.y)/2)*bg.y
                                - abs((d.x+d.y)/2)*bg.w + abs((d.x-d.y)/2)*bg.y;

        num += 2;
    }}
    return surround/2;
}}

int4 excite_and_inhibit_orient_surround(
    int2 coord,
    __global uchar* orient
){{

    int4 orient_default = (int4)(orient[gindex2( coord )*4], orient[gindex2( coord )*4+1],
            orient[gindex2( coord )*4+2], orient[gindex2( coord )*4+3]);

    int4 temp = get_oriented_surround_square_avg(coord, 1, orient, orient_default);

    return temp;
}}

#endif