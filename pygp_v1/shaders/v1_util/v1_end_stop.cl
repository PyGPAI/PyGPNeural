#ifndef _V1_END_STOP__
#define _V1_END_STOP__

//todo: Too noisy. Redesign.

void orient_group_to_end_stop(
    int2 coord,
    __global uchar* orient_group_out,
    __global uchar* end_stop_out
){{
    end_stop_out[gindex2(coord)*8+0]= 0;
    end_stop_out[gindex2(coord)*8+1]= 0;
    end_stop_out[gindex2(coord)*8+2]= 0;
    end_stop_out[gindex2(coord)*8+3]= 0;
    end_stop_out[gindex2(coord)*8+4]= 0;
    end_stop_out[gindex2(coord)*8+5]= 0;
    end_stop_out[gindex2(coord)*8+6]= 0;
    end_stop_out[gindex2(coord)*8+7]= 0;

    short endStopTemp[8];

    endStopTemp[0]= 0;
    endStopTemp[1]= 0;
    endStopTemp[2]= 0;
    endStopTemp[3]= 0;
    endStopTemp[4]= 0;
    endStopTemp[5]= 0;
    endStopTemp[6]= 0;
    endStopTemp[7]= 0;

    int2 getCoord;
    for(int i=0;i<=0;++i){{
        getCoord = coord+(int2)(i, 0);
        end_stop_out[gindex2(coord)*8+0] -= orient_group_out[gindex2(getCoord)*4+2];
        endStopTemp[0] += orient_group_out[gindex2(getCoord)*4+0];

        getCoord = coord+(int2)(i, -i);
        end_stop_out[gindex2(coord)*8+1] -= orient_group_out[gindex2(getCoord)*4+3];
        endStopTemp[1] += orient_group_out[gindex2(getCoord)*4+1];

        getCoord = coord+(int2)(0, i);
        end_stop_out[gindex2(coord)*8+2] -= orient_group_out[gindex2(getCoord)*4+0];
        endStopTemp[2] += orient_group_out[gindex2(getCoord)*4+2];

        getCoord = coord+(int2)(i, i);
        end_stop_out[gindex2(coord)*8+3] -= orient_group_out[gindex2(getCoord)*4+1];
        endStopTemp[3] += orient_group_out[gindex2(getCoord)*4+3];
    }}
    for(int i=-1;i<=-1;++i){{
        getCoord = coord-(int2)(i, 0);
        endStopTemp[4] -=  (orient_group_out[gindex2(getCoord)*4+0]);
        //end_stop_out[gindex2(coord)*8+4] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+2]), (short)(255));

        getCoord = coord-(int2)(i, -i);
        endStopTemp[5] -=  (orient_group_out[gindex2(getCoord)*4+1]);
        //end_stop_out[gindex2(coord)*8+5] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+3]), (short)(255));

        getCoord = coord-(int2)(0, i);
        endStopTemp[6] -=  (orient_group_out[gindex2(getCoord)*4+2]);
        //end_stop_out[gindex2(coord)*8+6] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+0]), (short)(255));

        getCoord = coord-(int2)(i, i);
        endStopTemp[7] -= (orient_group_out[gindex2(getCoord)*4+3]);
        //end_stop_out[gindex2(coord)*8+7] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+1]), (short)(255));
    }}

    for(int i=0;i<=0;++i){{
        getCoord = coord-(int2)(i, 0);
        end_stop_out[gindex2(coord)*8+4] -= orient_group_out[gindex2(getCoord)*4+2];
        endStopTemp[4] += orient_group_out[gindex2(getCoord)*4+0];

        getCoord = coord-(int2)(i, -i);
        end_stop_out[gindex2(coord)*8+5] -= orient_group_out[gindex2(getCoord)*4+3];
        endStopTemp[5] += orient_group_out[gindex2(getCoord)*4+1];

        getCoord = coord-(int2)(0, i);
        end_stop_out[gindex2(coord)*8+6] -= orient_group_out[gindex2(getCoord)*4+0];
        endStopTemp[6] += orient_group_out[gindex2(getCoord)*4+2];

        getCoord = coord-(int2)(i, i);
        end_stop_out[gindex2(coord)*8+7] -= orient_group_out[gindex2(getCoord)*4+1];
        endStopTemp[7] += orient_group_out[gindex2(getCoord)*4+3];
    }}

    for(int i=1;i<=1;++i){{
        getCoord = coord+(int2)(i, 0);
        endStopTemp[0] -= (orient_group_out[gindex2(getCoord)*4+0]);
        //end_stop_out[gindex2(coord)*8+0] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+2]), (short)(255));

        getCoord = coord+(int2)(i, -i);
        endStopTemp[1] -= (orient_group_out[gindex2(getCoord)*4+1]);
        //end_stop_out[gindex2(coord)*8+1] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+3]), (short)(255));

        getCoord = coord+(int2)(0, i);
        endStopTemp[2] -= (orient_group_out[gindex2(getCoord)*4+2]);
        //end_stop_out[gindex2(coord)*8+0] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+0]), (short)(255));

        getCoord = coord+(int2)(i, i);
        endStopTemp[3] -= (orient_group_out[gindex2(getCoord)*4+3]);

        //end_stop_out[gindex2(coord)*8+3] -= 255 - min((short)(orient_group_out[gindex2(getCoord)*4+1]), (short)(255));

    }}

    //add temp first

    for(int k=0; k<8;++k){{
        for(int j=1; j<=3;++j){{
            end_stop_out[gindex2(coord)*8+k] = max((short)(0), (short)(end_stop_out[gindex2(coord)*8+k] - (endStopTemp[(k+j)%8]>>2)));
            end_stop_out[gindex2(coord)*8+k] = max((short)(0), (short)(end_stop_out[gindex2(coord)*8+k] - (endStopTemp[(k-j)%8]>>2)));
        }}
    }}

    for(int k=0; k<8;++k){{
        if (end_stop_out[gindex2(coord)*8+k]<0){{
            end_stop_out[gindex2(coord)*8+k]=0;
        }}
    }}
}}

void end_stop_dbg(
    int2 coord,
    __global uchar* end_stop,
    __global uchar* orient_dbg_out
){{
        //orientation of line, 0-252

    short4 end = (short4)(
        (short)(end_stop[gindex2(coord)*8+0])+(short)(end_stop[gindex2(coord)*8+4]),
        (short)(end_stop[gindex2(coord)*8+1])+(short)(end_stop[gindex2(coord)*8+5]),
        (short)(end_stop[gindex2(coord)*8+2])+(short)(end_stop[gindex2(coord)*8+6]),
        (short)(end_stop[gindex2(coord)*8+3])+(short)(end_stop[gindex2(coord)*8+7])
    );

    orient_dbg_out[gindex2(coord)*3+0] = (
                                         0+
                                         end.x*85+
                                         end.y*170+
                                         end.z*255
                                        )
                                                        /
                                        (
                                         end.x +
                                         end.y +
                                         end.z +
                                         end.w
                                         );

    //std dev of line, approx
    orient_dbg_out[gindex2(coord)*3+1] =
                                        (
                                        abs(end.x - end.y)+
                                        abs(end.y - end.z)+
                                        abs(end.z - end.w)+
                                        abs(end.w - end.x)
                                        );

    //prominence of line
    orient_dbg_out[gindex2(coord)*3+2] = (end.x +
                                          end.y +
                                          end.z +
                                          end.w );
}}

#endif