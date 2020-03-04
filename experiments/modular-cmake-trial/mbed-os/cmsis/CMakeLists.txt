add_library(cmsis
  TARGET_CORTEX_M/mbed_tz_context.c
)

target_include_directories (cmsis
    PUBLIC
        .
        TARGET_CORTEX_M
)

target_link_libraries(cmsis gen_config)
