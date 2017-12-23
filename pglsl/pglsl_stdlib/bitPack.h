#ifndef __BIT_PACK_H_
#define __BIT_PACK_H_

//starts at top left. x,z<4, y<2
#define GET32CHUNCKBIT( uint32Chunck, posx, posy, posz )\
    (uint32Chunck & 1<<(posy*16+posz*4+posx))

//setVal should only be 0 or 1
#define SET32CHUNCKBIT( uint32Chunck, posx, posy, posz, setVal )\
        uint32Chunck ^= (GET32CHUNCKBIT( uint32Chunck, posx, posy, posz )>0? \
            !setVal<<(posy*16+posz*4+posx) : \
            setVal<<(posy*16+posz*4+posx) \
        )


//here, array pos is (x,z)/4, y/2
#define GET32CHUNKFROMUINT32ARRAY(uint32Array, posx, posy, posz) \
    uint32Array[posy*2+posz+posx/4]

#define GET32ARRAYBIT(uint32Array, posx, posy, posz) \
    GET32CHUNCKBIT( GET32CHUNKFROMUINT32ARRAY(uint32Array, posx, posy, posz), posx, posy, posz )

#define SET32ARRAYBIT(uint32Array, posx, posy, posz) \
    SET32CHUNCKBIT( GET32CHUNKFROMUINT32ARRAY(uint32Array, posx, posy, posz), posx, posy, posz )


#endif