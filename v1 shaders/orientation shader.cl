#define gindex2( p ) p.x*width+p.y

__constant int kernel_width = {};

uchar guardGetColor(
    int2 pos,
    const __global uchar* rgb_in
){{
    if (pos.x<0 || pos.y<0 || pos.x>height || pos.y>width){{
        return edge_brightness;
    }}
    else{{
        return (rgb_in[gindex2( pos )]);
    }}
}}

void get_vertical_avgs(
    int2 pos,
    uchar avg_line,
)

__kernel void rot(
    const __global uchar* rgc_in,
    const __global int* rots,
    const uint rotation_steps,
    const uint line_width,
    __global uchar* rot_out)
{{
    float2 coord = (float2)(get_global_id(0), get_global_id(1));

    int rots[rotation_steps];

    int step;
    float radians = 0;
    for(step = 0;step<rotation_steps; step++){{
        radians+=3.14159*2.0/step;
        int dot;
        float2 newPos=coord;
        for(dot=0;dot<line_width;dot++){{
            newPos.x += cos(radians);
            newPos.y += sin(radians);
            rots[step]+=guardGetColor((int2)(newPos), rgc_in);
        }}
        newPos=coord;
        for(dot=0;dot<line_width;dot++){{
            newPos.x -= cos(radians);
            newPos.y -= sin(radians);
            rots[step]+=guardGetColor((int2)(newPos), rgc_in);
        }}

        //compete with perp lines
        uint oppOfMe = rotation_steps/2 + step;
        rots[oppOfMe]-=rots[step];
    }}

}}