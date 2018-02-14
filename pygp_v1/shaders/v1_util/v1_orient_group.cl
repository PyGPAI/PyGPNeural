#ifndef _V1_ORIENT_GROUP__
#define _V1_ORIENT_GROUP__

#include "v1_util/v1_get_pixel.cl"

#define ORIENT_GROUP__SUM_GROUP

#ifdef ORIENT_GROUP__SUM_GROUP

void orient_to_orient_group(
    int2 coord,
    __global uchar* orient_out,
    __global uchar* orient_group_out
){{
    int4 temp = (int4)(0);

    int2 getCoord;
    for(int i=-1;i<=1;++i){{
        for(int j=-1;j<=1;++j){{
            getCoord = coord+(int2)(i, j);

            temp += guardGetArray4(getCoord, orient_out, temp);
            temp -= rotate4_90(guardGetArray4(getCoord, orient_out, temp));
        }}
    }}

    temp.x = max((short)(0), (short)(temp.x));
    temp.y = max((short)(0), (short)(temp.y));
    temp.z = max((short)(0), (short)(temp.z));
    temp.w = max((short)(0), (short)(temp.w));

    temp.x >>= 3;
    temp.y >>= 3;
    temp.z >>= 3;
    temp.w >>= 3;

    orient_group_out[gindex2(coord)*4+0] = temp.x;
    orient_group_out[gindex2(coord)*4+1] = temp.y;
    orient_group_out[gindex2(coord)*4+2] = temp.z;
    orient_group_out[gindex2(coord)*4+3] = temp.w;

    for(int k=0; k<4;++k){{
        if (orient_group_out[gindex2(coord)*4+k]<0){{
            orient_group_out[gindex2(coord)*4+k]=0;
        }}
    }}
}}

#endif

#ifdef ORIENT_GROUP__MAX_GROUP

void orient_to_orient_group(
    int2 coord,
    __global uchar* orient_out,
    __global uchar* orient_group_out
){{
    short tempMax = 0;
    int maxk;

    //int maxi, maxj,

    int2 getCoord;
    for(int i=-1;i<=1;++i){{
        for(int j=-1;j<=1;++j){{
            getCoord = coord+(int2)(i, j);
            for(int k=0;k<=3;++k){{
                if(orient_out[gindex2(getCoord)*4+k] > tempMax){{
                    tempMax = orient_out[gindex2(getCoord)*4+k];
                    //maxi = i;
                    //maxj = j;
                    maxk = k;
                }}
            }}
        }}
    }}

    int competeK = (maxk+2)&3;
    int competeMax;

    for(int i=-1;i<=1;++i){{
        for(int j=-1;j<=1;++j){{
            tempMax = max((short)(0), (short)(tempMax - orient_out[gindex2(getCoord)*4+competeK]));
            competeMax = min((short)(tempMax), (short)(competeMax + orient_out[gindex2(getCoord)*4+competeK]));
        }}
    }}

    orient_group_out[gindex2(coord)*4+0] = 0;
    orient_group_out[gindex2(coord)*4+1] = 0;
    orient_group_out[gindex2(coord)*4+2] = 0;
    orient_group_out[gindex2(coord)*4+3] = 0;

    orient_group_out[gindex2(coord)*4+maxk] = tempMax;
    //orient_group_out[gindex2(coord)*4+(maxk+1)&3] = tempMax>>1;
    //orient_group_out[gindex2(coord)*4+competeK] = competeMax;
    //orient_group_out[gindex2(coord)*4+(competeK+1)&3] = competeMax>>1;

}}

#endif

#endif