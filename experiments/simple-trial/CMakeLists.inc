add_executable (cmakeTrial main.c)

if(NOT DEFINED EXCLUDE_LIB_ALIB)
    add_subdirectory (alib)
    target_link_libraries (cmakeTrial LINK_PUBLIC alib)
endif()

if(NOT DEFINED EXCLUDE_LIB_BLIB)
    add_subdirectory (blib)
    target_link_libraries (cmakeTrial LINK_PUBLIC blib)
endif()

add_subdirectory (c-lib_with_subdirs)
target_link_libraries (cmakeTrial LINK_PUBLIC clib)


# This is how a compiler #define value is specified.
add_compile_definitions(CONFIG_PARAM_1="config_param1")

if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -pedantic -Werror)
endif()
