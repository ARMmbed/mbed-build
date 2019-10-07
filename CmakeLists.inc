cmake_minimum_required (VERSION 2.8.11)
project (CMAKE_TRIAL)

add_subdirectory (lib)

add_executable (cmakeTrial main.c)

target_link_libraries (cmakeTrial LINK_PUBLIC library-a library-b)