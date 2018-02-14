#ifndef _V1_DEBUG__
#define _V1_DEBUG__

void orient_dbg(
    int2 coord,
    __global uchar* orient_out,
    __global uchar* orient_dbg_out
){{
        //orientation of line, 0-252
    orient_dbg_out[gindex2(coord)*3+0] = (
                                         (short)(0)+
                                         (short)(orient_out[gindex2(coord)*4+1])*(short)(85)+
                                         (short)(orient_out[gindex2(coord)*4+2])*(short)(170)+
                                         (short)(orient_out[gindex2(coord)*4+3])*(short)(255)
                                        )
                                                        /
                                        (
                                         (short)(orient_out[gindex2(coord)*4+0]) +
                                         (short)(orient_out[gindex2(coord)*4+1]) +
                                         (short)(orient_out[gindex2(coord)*4+2]) +
                                         (short)(orient_out[gindex2(coord)*4+3])
                                         );

    //std dev of line, approx
    orient_dbg_out[gindex2(coord)*3+1] =
                                        (
                                        abs((short)(orient_out[gindex2(coord)*4+0])-(short)(orient_out[gindex2(coord)*4+1]))+
                                        abs((short)(orient_out[gindex2(coord)*4+1])-(short)(orient_out[gindex2(coord)*4+2]))+
                                        abs((short)(orient_out[gindex2(coord)*4+2])-(short)(orient_out[gindex2(coord)*4+3]))+
                                        abs((short)(orient_out[gindex2(coord)*4+3])-(short)(orient_out[gindex2(coord)*4+0]))
                                        );

    //prominence of line
    orient_dbg_out[gindex2(coord)*3+2] = ((short)(orient_out[gindex2(coord)*4+0]>>1) +
                                          (short)(orient_out[gindex2(coord)*4+1]>>1) +
                                          (short)(orient_out[gindex2(coord)*4+2]>>1) +
                                          (short)(orient_out[gindex2(coord)*4+3]>>1) );
}}

#endif