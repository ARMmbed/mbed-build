# Each subdirectory needs to be added individually.
add_subdirectory (alib)
add_subdirectory (blib)

add_executable (cmakeTrial main.c)

target_link_libraries (cmakeTrial LINK_PUBLIC alib blib)
