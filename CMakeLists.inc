add_subdirectory (alib blib)

add_executable (cmakeTrial main.c)

target_link_libraries (cmakeTrial LINK_PUBLIC alib blib)
