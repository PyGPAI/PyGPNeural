#include <iostream>

#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include "../pglsl/pglsl_stdlib/bitPack.h"


TEST_CASE("TEST SET32CHUNCKBIT"){
    uint32_t uint32ChunkUpper = 0;

    SET32CHUNCKBIT(uint32ChunkUpper, 0, 0, 0, true);

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 0 )==1);
    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 1, 0, 0 )==0);

    SET32CHUNCKBIT(uint32ChunkUpper, 1, 0, 0, true);

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 1, 0, 0 )==2);

    SET32CHUNCKBIT(uint32ChunkUpper, 0, 0, 0, false);
    SET32CHUNCKBIT(uint32ChunkUpper, 1, 0, 0, false);
    SET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 1, true );

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 1 )==16);

    SET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 1, false );
    SET32CHUNCKBIT( uint32ChunkUpper, 0, 1, 0, true );

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 1, 0 )==65536);

}

TEST_CASE("TEST GET32CHUNCKBIT"){
    uint32_t uint32ChunkUpper = 1;

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 0 )==1);
    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 1, 0, 0 )==0);

    uint32ChunkUpper = 3;

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 1, 0, 0 )==2);

    uint32ChunkUpper = 16;

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 0, 1 )==16);

    uint32ChunkUpper = 65536;

    REQUIRE(GET32CHUNCKBIT( uint32ChunkUpper, 0, 1, 0 )==65536);
}