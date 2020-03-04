add_library(device_key
        source/DeviceKey.cpp
        source/DeviceKey.h
)

target_include_directories (device_key
    PUBLIC
    .
    source
)

target_link_libraries(device_key gen_config)
target_link_libraries(device_key platform)
