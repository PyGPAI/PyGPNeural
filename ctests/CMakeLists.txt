cmake_minimum_required(VERSION 3.8)
project(glslTesting)

set(CMAKE_CXX_STANDARD 11)

set(PGLSL_STDLIB_DIR ../pglsl/pglsl_stdlib)

include_directories(${PGLSL_STDLIB_DIR})

set(SOURCE_FILES testBitPack.cpp catch.hpp ${PGLSL_STDLIB_DIR}/bitPack.h)
add_executable(TestBitPack ${SOURCE_FILES})