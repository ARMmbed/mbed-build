# Define the configuration as a separate target library called gen_config. This can then be referenced
# by dependencies and linked in properly by CMake without having to specify cross-directory paths.

# Note that this library contains only a single header, so there is no actual code and hence no
# lib.a file is generated. Hence the use of the INTERFACE word here.
add_library(gen_config INTERFACE)

target_include_directories(gen_config INTERFACE .)
