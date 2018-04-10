#ifndef _V1_END_STOP__
#define _V1_END_STOP__

//todo: Too noisy. Redesign.

void orient_group_to_end_stop(
    int2 coord,
    __global uchar* orient_group_out,
    __global uchar* end_stop_out
){{



    float n = orient_group_out[gindex2(coord)*4];
    float ne = orient_group_out[gindex2(coord)*4+1]/sqrt(2.0);
    float e = orient_group_out[gindex2(coord)*4+2];
    float se = orient_group_out[gindex2(coord)*4+3]/sqrt(2.0);

    float2 direction = (float2)(e+ne+se,n+ne-se);
    float2 direction_out =(float2)(e+ne+se, -n+ne-se);
    float2 direction_out2 =(float2)(e+ne-se, n+ne+se);

    if (length(direction_out)>length(direction)){{
        direction = direction_out;
    }}
    if (length(direction_out2)> length(direction)){{
        direction=direction_out2;
    }}

    direction=normalize(direction);

    //ne = orient_group_out[gindex2(coord)*4+1];
    //se = orient_group_out[gindex2(coord)*4+3];

    for (int tail = 4;tail<=5;tail++){{
        float2 p = (float2)(coord.x,coord.y)-tail*direction;
        int2 pos;
        pos.x = (int)(p.x); pos.y = (int)(p.y);

        float n2 = orient_group_out[gindex2(pos)*4];
        float ne2 = orient_group_out[gindex2(pos)*4+1];
        float e2 = orient_group_out[gindex2(pos)*4+2];
        float se2 = orient_group_out[gindex2(pos)*4+3];

        n=n+n2;
        ne=ne+ne2;
        e=e+e2;
        se=se+se2;
    }}

    for (int head = 2;head<=7;head++){{
        float2 p = (float2)(coord.x,coord.y)+head*direction;
        int2 pos;
        pos.x = (int)(p.x); pos.y = (int)(p.y);

        float n2 = orient_group_out[gindex2(pos)*4];
        float ne2 = orient_group_out[gindex2(pos)*4+1];
        float e2 = orient_group_out[gindex2(pos)*4+2];
        float se2 = orient_group_out[gindex2(pos)*4+3];

        n=n-n2-ne2*(sqrt(2.0)/2.0)-se2*(sqrt(2.0)/2.0);
        ne=ne-ne2-n2*(sqrt(2.0)/2.0)-e2*(sqrt(2.0)/2.0);
        e=e-e2-ne2*(sqrt(2.0)/2.0)-se2*(sqrt(2.0)/2.0);
        se=se-se2-e2*(sqrt(2.0)/2.0)-n2*(sqrt(2.0)/2.0);
    }}

    end_stop_out[gindex2(coord)*8]= (uchar)fmax(fmin((float)n,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+1]= (uchar)fmax(fmin((float)ne*2,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+2]= (uchar)fmax(fmin((float)e,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+3]= (uchar)fmax(fmin((float)se*2,(float)255.0), (float)0.0);

    n = orient_group_out[gindex2(coord)*4];
    ne = orient_group_out[gindex2(coord)*4+1];
    e = orient_group_out[gindex2(coord)*4+2];
    se = orient_group_out[gindex2(coord)*4+3];

    for (int tail = 4;tail<=5;tail++){{
        float2 p = (float2)(coord.x,coord.y)+tail*direction;
        int2 pos;
        pos.x = (int)(p.x); pos.y = (int)(p.y);

        float n2 = orient_group_out[gindex2(pos)*4];
        float ne2 = orient_group_out[gindex2(pos)*4+1];
        float e2 = orient_group_out[gindex2(pos)*4+2];
        float se2 = orient_group_out[gindex2(pos)*4+3];

        n=n+n2;
        ne=ne+ne2;
        e=e+e2;
        se=se+se2;
    }}

    for (int head = 2;head<=7;head++){{
        float2 p = (float2)(coord.x,coord.y)-head*direction;
        int2 pos;
        pos.x = (int)(p.x); pos.y = (int)(p.y);

        float n2 = orient_group_out[gindex2(pos)*4];
        float ne2 = orient_group_out[gindex2(pos)*4+1];
        float e2 = orient_group_out[gindex2(pos)*4+2];
        float se2 = orient_group_out[gindex2(pos)*4+3];

        n=n-n2-ne2*(sqrt(2.0)/2.0)-se2*(sqrt(2.0)/2.0);
        ne=ne-ne2-n2*(sqrt(2.0)/2.0)-e2*(sqrt(2.0)/2.0);
        e=e-e2-ne2*(sqrt(2.0)/2.0)-se2*(sqrt(2.0)/2.0);
        se=se-se2-e2*(sqrt(2.0)/2.0)-n2*(sqrt(2.0)/2.0);
    }}

    end_stop_out[gindex2(coord)*8+4]= (uchar)fmax(fmin((float)n,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+5]= (uchar)fmax(fmin((float)ne*2,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+6]= (uchar)fmax(fmin((float)e,(float)255.0), (float)0.0);
    end_stop_out[gindex2(coord)*8+7]= (uchar)fmax(fmin((float)se*2,(float)255.0), (float)0.0);

}}

void end_stop_dbg(
    int2 coord,
    __global uchar* end_stop,
    __global uchar* orient_dbg_out
){{
        //orientation of line, 0-252

    int end[8];
    end[0]=end_stop[gindex2(coord)*8];
    end[1]=end_stop[gindex2(coord)*8+1];
    end[2]=end_stop[gindex2(coord)*8+2];
    end[3]=end_stop[gindex2(coord)*8+3];
    end[4]=end_stop[gindex2(coord)*8+4];
    end[5]=end_stop[gindex2(coord)*8+5];
    end[6]=end_stop[gindex2(coord)*8+6];
    end[7]=end_stop[gindex2(coord)*8+7];

    orient_dbg_out[gindex2(coord)*3+0] = (uchar)((
                                         0+
                                         end[1]*36+
                                         end[2]*73+
                                         end[3]*109+
                                         end[4]*146+
                                         end[5]*182+
                                         end[6]*219+
                                         end[7]*255
                                        )
                                                        /
                                        (
                                         end[0]+
                                         end[1]+
                                         end[2]+
                                         end[3]+
                                         end[4]+
                                         end[5]+
                                         end[6]+
                                         end[7]
                                         ));

    //std dev of line, approx
    orient_dbg_out[gindex2(coord)*3+1] =(uchar)
                                        (
                                        abs(end[0] - end[1])+
                                        abs(end[1] - end[2])+
                                        abs(end[2] - end[3])+
                                        abs(end[3] - end[4])+
                                        abs(end[4] - end[5])+
                                        abs(end[5] - end[6])+
                                        abs(end[6] - end[7])+
                                        abs(end[7] - end[0])
                                        );

    //prominence of line
    orient_dbg_out[gindex2(coord)*3+2] = (uchar)(end[0]+
                                          end[1]+
                                          end[2]+
                                          end[3]+
                                          end[4]+
                                          end[5]+
                                          end[6]+
                                          end[7]);

}}

#endif