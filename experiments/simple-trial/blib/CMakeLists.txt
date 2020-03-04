# Declares 'blib' as a library, and specifies the source code that is included
add_library (blib blib.c)

target_include_directories (blib PUBLIC include)
