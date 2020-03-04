add_library(hal
  LowPowerTickerWrapper.cpp
  mbed_compat.c
  mbed_critical_section_api.c
  mbed_flash_api.c
  mbed_gpio.c
  mbed_gpio_irq.c
  mbed_itm_api.c
  mbed_lp_ticker_api.c
  mbed_lp_ticker_wrapper.cpp
  mbed_pinmap_common.c
  mbed_pinmap_default.c
  mbed_ticker_api.c
  mbed_us_ticker_api.c
  mpu/mbed_mpu_v7m.c
  mpu/mbed_mpu_v8m.c
  static_pinmap.cpp
  usb/mbed_usb_phy.cpp
)

target_link_libraries(hal platform)
target_link_libraries(hal cmsis)
target_link_libraries(hal targets)

target_include_directories (hal
    PUBLIC
      .
      usb
      storage_abstraction
)
