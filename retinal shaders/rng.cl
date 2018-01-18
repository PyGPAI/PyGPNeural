//#include "cl_defs.h"

//#define UNSAFE_MODE

__constant uint p1 = 0x9E3779B1;
__constant uint p2 = 0x85EBCA77;
__constant uint p3 = 0xC2B2AE3D;
__constant uint p4 = 0x27D4EB2F;
__constant uint p5 = 0x165667B1;


//OpenCV implementation of xxhash32. Ported from https://github.com/szensk/luaxxhash
uint uint_xxhash32(uint* data, uint len, uint seed){{
    int i=0; int n=0;
    const uchar* bytes = (const uchar*)(data);
    const uint*  words = (const uint*)(data);

    uint h32;
    if(len>=16){{
        uint limit = len - 16;
        uint v[4];
        v[0] = seed + p1 + p2;      v[1] = seed + p2;
        v[2] = seed;                v[3] = seed - p1;
        while(i<=limit){{
            for(int j=0; j<3;j++){{
                v[j] = v[j] + words[n] * p2;
                v[j] = rotate(v[j], (uint)13); v[j] = v[j] * p1;
                i = i + 4; n = n + 1;
            }}
        }}
        h32 = rotate(v[0], (uint)1) + rotate(v[1], (uint)7) + rotate(v[2], (uint)12) + rotate(v[3], (uint)18);
    }}else{{
        h32 = seed + p5;
    }}
    h32 = h32 + len;

    int limit = len - 4;

    while(i < limit){{
        h32 = (h32 + (words[n]*p3));
        h32 = rotate(h32, (uint)17) * p4;
        i+=4; n++;
    }}

    while(i < len){{
        h32 = h32 + bytes[i<<2]*p5;
        h32 = rotate(h32,(uint)11)*p1;
        i++;
    }}

    h32 = h32^(h32>>15);
    h32 = h32 * p2;
    h32 = h32^(h32>>13);
    h32 = h32*p3;

    return h32^(h32>>16);
}}

//#define TEST_UNIFORM

//simple partial box muller transform
float uniformToNormal(uint rand_in)
{{
	float u1 = rand_in * (1.0 / 4294967295);
	float rnd = sqrt(-2.0 * log(u1));
	if(rand_in&1){{
	    return rnd;
	}}
	return -rnd;
}}

float normal(uint rand_in, float mean, float variance)
{{
	float u1 = rand_in * (1.0 / 4294967295);
	float rnd = sqrt(-2.0 * log(u1));
	if(rand_in&1){{
	    return rnd*variance + mean;
	}}
	return -rnd*variance + mean;
}}


#ifdef TESTING
__constant int width = {};
__constant int height = {};
__constant int colors = {};

#ifdef TEST_UNIFORM

#define gindex3( p ) p.x*width*colors+p.y*colors+p.z
#define gindex2( p ) p.x*width+p.y

__kernel void xxhash_test(
    const __global uchar* rgb_in,
    const uint seed,
    __global uchar* rgb_out
    )
{{
    int3 coordr = (int3)(get_global_id(0), get_global_id(1), 0);
    int3 coordg = (int3)(get_global_id(0), get_global_id(1), 1);
    int3 coordb = (int3)(get_global_id(0), get_global_id(1), 2);

    int2 outcoord = (int2)(get_global_id(0), get_global_id(1));

    uint rgb[2];
    rgb[0] = get_global_id(1); rgb[1] = get_global_id(0);

    uint xxhash = uint_xxhash32(rgb, 2, seed);

    rgb_out[gindex3(coordr)] = (uchar)(xxhash);
    rgb_out[gindex3(coordg)] = (uchar)(xxhash>>8);
    rgb_out[gindex3(coordb)] = (uchar)(xxhash>>16);

}}

#endif

#define TEST_NORMAL

#ifdef TEST_NORMAL

#define gindex3( p ) p.x*width*colors+p.y*colors+p.z
#define gindex2( p ) p.x*width+p.y

__kernel void xxhash_test(
    const __global uchar* rgb_in,
    const uint seed,
    __global uchar* rgb_out
    )
{{
    int3 coordr = (int3)(get_global_id(0), get_global_id(1), 0);
    int3 coordg = (int3)(get_global_id(0), get_global_id(1), 1);
    int3 coordb = (int3)(get_global_id(0), get_global_id(1), 2);

    int2 outcoord = (int2)(get_global_id(0), get_global_id(1));

    uint rgb[2];
    rgb[0] = get_global_id(1); rgb[1] = get_global_id(0);

    uint xxhash = uint_xxhash32(rgb, 2, seed);
    float n = normal(xxhash, 230, 16);

    rgb_out[gindex3(coordr)] = (uchar)min(max((uchar)(n),(uchar)0),(uchar)255);
    rgb_out[gindex3(coordg)] = rgb_out[gindex3(coordr)];
    rgb_out[gindex3(coordb)] = rgb_out[gindex3(coordr)];

}}

#endif
#endif