add_library(mbed_os mbed.h)

target_include_directories (mbed_os
    PUBLIC
      .
)

add_subdirectory(rtos)
add_subdirectory(platform)
add_subdirectory(events)
add_subdirectory(drivers)
add_subdirectory(hal)
add_subdirectory(cmsis)
add_subdirectory(components)
add_subdirectory(targets)
add_subdirectory(features/mbedtls)
add_subdirectory(features/cellular)
add_subdirectory(features/frameworks)
add_subdirectory(features/lorawan)
add_subdirectory(features/lwipstack)
add_subdirectory(features/nanostack)
add_subdirectory(features/netsocket)
add_subdirectory(features/nfc)
add_subdirectory(features/storage)
add_subdirectory(features/device_key)

target_link_libraries(mbed_os rtos platform events drivers hal cmsis components targets mbedtls cellular frameworks lorawan lwipstack nanostack netsocket nfc storage device_key gen_config)
